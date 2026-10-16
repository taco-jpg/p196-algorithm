#!/usr/bin/env python3
"""Compile the exact history-family source with its staged original interfaces."""

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
    build = args.build.resolve()
    source = root / "HistoryFamily.lean"
    dependency_hashes = {}
    for name in ["TwoLayerCertificate.lean", "HistoryInterfaces.lean", "ActualHistories.lean"]:
        original = root / name
        staged = build / name
        if not original.is_file() or not staged.is_file():
            raise RuntimeError(f"Required actual dependency source is not ready: {name}")
        assert sha(original) == sha(staged), f"Dependency source mismatch: {name}"
        dependency_hashes[name] = sha(original)
    family_source = root.parent / "finite-horizon-overflow-20261016/FamilyCardinality.lean"
    assert sha(family_source) == sha(build / "FamilyCardinality.lean"), "Existing allBits source mismatch"
    dependency_hashes["FamilyCardinality.lean"] = sha(family_source)
    text = source.read_text()
    declarations = re.findall(r"^(?:private )?(?:abbrev|def|theorem) (\w+)", text, re.M)
    printed = re.findall(r"^#print axioms (\w+)$", text, re.M)
    assert set(declarations) == set(printed), "Missing declaration axiom check"
    assert not re.search(r"\b(?:sorry|admit|native_decide)\b", text), "Excluded proof mechanism"
    obj = evidence / "HistoryFamily.olean"
    argv = [str(args.lean.resolve()), "-o", str(obj), source.name]
    env = os.environ.copy()
    env["LEAN_PATH"] = str(build)
    result = subprocess.run(argv, cwd=root, env=env, capture_output=True, text=True)
    output = result.stdout + result.stderr
    log = evidence / "final.log"
    log.write_text(output)
    entries = re.findall(
        r"'([^']+)' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)", output
    )
    axiom_sets = {
        name: [a.strip() for a in values.split(",") if a.strip()]
        for name, values in entries
    }
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    unexpected = {name: values for name, values in axiom_sets.items() if set(values) - allowed}
    passed = result.returncode == 0 and len(entries) == len(printed) and not unexpected
    report = {
        "status": "PASS" if passed else "FAIL",
        "source_sha256": sha(source),
        "dependency_source_sha256": dependency_hashes,
        "argv": argv,
        "cwd": str(root),
        "LEAN_PATH": str(build),
        "exit_code": result.returncode,
        "audited_declarations": len(entries),
        "expected_declarations": len(printed),
        "axiom_sets": axiom_sets,
        "unexpected_axioms": unexpected,
        "log_sha256": sha(log),
        "object_sha256": sha(obj) if passed else None,
    }
    (evidence / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in (
        "status", "exit_code", "source_sha256", "audited_declarations", "unexpected_axioms"
    )}, indent=2))
    if not passed:
        print(output)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
