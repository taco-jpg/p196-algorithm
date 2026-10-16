#!/usr/bin/env python3
"""Compile the exact cardinality source and validate every printed axiom set."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--deps", required=True, type=Path)
    args = parser.parse_args()
    development = Path(__file__).resolve().parent
    contribution = development.parents[1]
    source = contribution / "FamilyCardinality.lean"
    log = development / "final.log"
    obj = development / "FamilyCardinality.olean"
    deps = args.deps.resolve()
    lean = args.lean.resolve()
    assert digest(contribution / "FamilyDefinitions.lean") == digest(
        deps / "FamilyDefinitions.lean"
    ), "Dependency definitions differ from the current contribution source"
    text = source.read_text()
    declaration_names = re.findall(r"^(?:private )?(?:def|theorem) (\w+)", text, re.M)
    printed_names = re.findall(r"^#print axioms (\w+)$", text, re.M)
    assert set(declaration_names) == set(printed_names), "Incomplete axiom audit"
    env = os.environ.copy()
    env["LEAN_PATH"] = str(deps)
    argv = [str(lean), "-o", str(obj), source.name]
    result = subprocess.run(argv, cwd=contribution, env=env, capture_output=True, text=True)
    output = result.stdout + result.stderr
    log.write_text(output)
    entries = re.findall(
        r"'([^']+)' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)",
        output,
    )
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    axiom_sets = {
        name: [item.strip() for item in values.split(",") if item.strip()]
        for name, values in entries
    }
    unexpected = {
        name: values for name, values in axiom_sets.items() if not set(values) <= allowed
    }
    success = result.returncode == 0 and len(entries) == len(printed_names) and not unexpected
    record = {
        "status": "PASS" if success else "FAIL",
        "compiler": str(lean),
        "argv": argv,
        "cwd": str(contribution),
        "LEAN_PATH": str(deps),
        "source": source.name,
        "source_sha256": digest(source),
        "dependency_source_sha256": {
            name: digest(deps / name)
            for name in ["PeriodObstructions.lean", "ActualWordBridge.lean", "FamilyDefinitions.lean"]
        },
        "returncode": result.returncode,
        "audited_declarations": len(entries),
        "expected_declarations": len(printed_names),
        "axiom_sets": axiom_sets,
        "unexpected_axioms": unexpected,
        "log_sha256": digest(log),
        "object_sha256": digest(obj) if success else None,
    }
    (development / "verification.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({key: record[key] for key in [
        "status", "returncode", "source_sha256", "audited_declarations", "unexpected_axioms"
    ]}, indent=2))
    if not success:
        print(output, file=sys.stderr)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
