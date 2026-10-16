#!/usr/bin/env python3
"""Compile the finite two-history certificate and audit every declaration."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lean", type=Path, required=True)
    ap.add_argument("--build", type=Path, required=True)
    args = ap.parse_args()
    evidence = Path(__file__).resolve().parent
    root = evidence.parents[1]
    source = root / "TwoLayerCertificate.lean"
    dependency = root / "dependencies/agent9/InverseFibers.lean"
    expected_dep = "64f4fa5df54d9365b1b3706eceeab3d3f358eb1040a95e3057ac4d9f82806b70"
    assert sha(dependency) == expected_dep, "Retained Agent9 dependency mismatch"
    build = args.build.resolve()
    assert sha(build / "InverseFibers.lean") == expected_dep, "Build dependency source mismatch"
    source_text = source.read_text()
    declarations = re.findall(r"^(?:private )?(?:abbrev|def|theorem) (\w+)", source_text, re.M)
    audits = re.findall(r"^#print axioms (\w+)$", source_text, re.M)
    assert set(declarations) == set(audits), "Declaration missing from axiom audit"
    assert not re.search(r"\b(?:sorry|admit|native_decide)\b", source_text), "Excluded proof mechanism"
    obj = evidence / "TwoLayerCertificate.olean"
    argv = [str(args.lean.resolve()), "-o", str(obj), source.name]
    env = os.environ.copy()
    env["LEAN_PATH"] = str(build)
    proc = subprocess.run(argv, cwd=root, env=env, capture_output=True, text=True)
    output = proc.stdout + proc.stderr
    log = evidence / "final.log"
    log.write_text(output)
    entries = re.findall(
        r"'([^']+)' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)", output
    )
    axiom_sets = {
        name: [a.strip() for a in content.split(",") if a.strip()]
        for name, content in entries
    }
    unexpected = {name: values for name, values in axiom_sets.items() if set(values) - {"propext"}}
    ok = proc.returncode == 0 and len(entries) == len(audits) and not unexpected
    result = {
        "status": "PASS" if ok else "FAIL",
        "source": source.name,
        "source_sha256": sha(source),
        "dependency_sha256": expected_dep,
        "dependency_blob": "cade8ace6359fe8246a29ec781859e3a39b00e11",
        "argv": argv,
        "cwd": str(root),
        "LEAN_PATH": str(build),
        "exit_code": proc.returncode,
        "audited_declarations": len(entries),
        "expected_declarations": len(audits),
        "axiom_sets": axiom_sets,
        "unexpected_axioms": unexpected,
        "log_sha256": sha(log),
        "object_sha256": sha(obj) if ok else None,
        "preserved_attempts": [
            {"attempt": 1, "status": "REJECTED", "exit_code": 1,
             "reason": "Std lacked a Decidable universal quantifier over Joint=Prod; replaced by explicit finite component quantifiers."},
            {"attempt": 2, "status": "PASS", "exit_code": 0,
             "reason": "Explicit Fin4 component quantifiers compile; all axiom checks contain at most propext."},
        ],
    }
    (evidence / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "status", "exit_code", "source_sha256", "audited_declarations", "unexpected_axioms"
    )}, indent=2))
    if not ok:
        print(output)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
