#!/usr/bin/env python3
"""Independent, inexpensive review controls for the package checker.

This script runs no Lean process and performs no Git operation.  It snapshots
the package's Python/JSON/document inputs, checks pinned repository source bytes,
and exercises the audit parser against an actual earlier ten-module audit plus
specific corrupted copies.  A successful result is not a 17-module Lean build.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import types


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check-sha256", required=True)
    parser.add_argument("--pins-sha256", required=True)
    parser.add_argument("--reproduce-sha256", required=True)
    args = parser.parse_args()
    package, repo, output = args.package.resolve(), args.repo.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    expected = {"check.py": args.check_sha256, "source-pins.json": args.pins_sha256,
                "REPRODUCE.md": args.reproduce_sha256}
    inputs = {}
    for name, pin in expected.items():
        data = (package / name).read_bytes()
        if digest(data) != pin:
            raise RuntimeError(f"Frozen review input changed: {name}")
        (output / name).write_bytes(data)
        inputs[name] = data

    checker = types.ModuleType("agent108_independent_package_review")
    checker.__file__ = str(output / "check.py")
    exec(compile(inputs["check.py"], str(output / "check.py"), "exec"), checker.__dict__)
    pins = checker.load_pins(output / "source-pins.json")
    sources, source_records = checker.verify_sources(pins, repo)
    source_rows = [declaration for row in source_records for declaration in row["source_declarations"]]
    if len(source_rows) != 578 or len(sources) != 17:
        raise RuntimeError("Expected exact reviewed 17-source / 578-explicit-declaration inventory")

    earlier = package / "review/independent-window-incoming/attempts/001"
    earlier_record = json.loads((earlier / "verification.json").read_text())
    truthful = (earlier / "WindowModuleAxioms.stdout.log").read_text()
    previous_hash = "3c9c411ed0c387cd7d006f151f53ba45e977e4858887a07615ae18004a1d9861"
    if digest(truthful.encode()) != previous_hash:
        raise RuntimeError("Prior independently verified literal-axiom log changed")
    declarations = [{**row, "source_name": "Agent108.WindowWeights." + row["short_name"]}
                    for row in earlier_record["source_declaration_correspondence"]]
    modules = {row["module"] for row in declarations}
    parsed = checker.parse_audit(truthful, modules, declarations)
    if not parsed["pass"]:
        raise RuntimeError("Faithful earlier audit was not accepted")

    controls = []
    def audit_negative(name: str, mutated: str) -> None:
        try:
            result = checker.parse_audit(mutated, modules, declarations)
            rejected = not result["pass"]
            record = {"name": name, "rejected": rejected,
                      "parser_returned_pass": result["pass"]}
        except Exception as error:
            record = {"name": name, "rejected": True,
                      "exception": type(error).__name__, "message": str(error)}
        record["mutated_log_sha256"] = digest(mutated.encode())
        controls.append(record)
        if not record["rejected"]:
            raise RuntimeError("Negative audit control was accepted: " + name)

    first = parsed["safe_axiom_reports"][0]
    audit_negative("wrong-printed-name", truthful.replace(
        "'" + first["printed_name"] + "'", "'Injected.WrongPrintedDeclaration'", 1))
    match = re.search(r"^AUDIT_BEGIN\|([^\n]+)\n.*?^AUDIT_END\|\1\n?", truthful, re.M | re.S)
    if match is None:
        raise RuntimeError("Could not locate the real first safe-declaration block")
    audit_negative("missing-safe-report", truthful[:match.start()] + truthful[match.end():])
    if "propext" not in truthful:
        raise RuntimeError("Expected actual propext report for unknown-axiom control")
    audit_negative("disallowed-logical-axiom", truthful.replace("propext", "sorryAx", 1))

    first_source = pins["sources"][0]
    corrupted = bytes([sources[first_source["module"]][0] ^ 1]) + sources[first_source["module"]][1:]
    for name, operation in (
        ("source-byte-corruption", lambda: checker.validate_source(first_source, corrupted)),
        ("source-path-escape", lambda: checker.repo_file(repo, "../outside-source.lean")),
    ):
        try:
            operation()
        except Exception as error:
            controls.append({"name": name, "rejected": True,
                             "exception": type(error).__name__, "message": str(error)})
        else:
            raise RuntimeError("Negative source control was accepted: " + name)

    command = [sys.executable, "-B", str(output / "check.py"), "--repo-root", str(repo), "--check-inputs"]
    process = subprocess.run(command, capture_output=True, text=True, check=False)
    (output / "input-check.stdout.log").write_text(process.stdout)
    (output / "input-check.stderr.log").write_text(process.stderr)
    if process.returncode != 0:
        raise RuntimeError("Real --check-inputs command failed")
    input_result = json.loads(process.stdout)
    if (input_result["status"] != "INPUTS_VERIFIED_ONLY" or
            input_result["proof_compilation_performed"] or input_result["axiom_audit_performed"]):
        raise RuntimeError("Input-only command claimed mathematical verification")

    audit_source = checker.make_audit_source(pins["build_order"])
    (output / "GeneratedAudit.lean").write_text(audit_source)
    for name in pins["build_order"]:
        if json.dumps(name) not in audit_source:
            raise RuntimeError("Generated audit omitted a selected exact module origin")
    if 'modules.contains modName.toString' not in audit_source:
        raise RuntimeError("Expected exact module-origin selection in inspected audit generator")
    if 'if !info.isUnsafe && !info.isPartial then' not in audit_source:
        raise RuntimeError("Expected inspected safe/nonpartial declaration selection")
    if tuple(checker.LEAN_FLAGS) != ("--trust=0", "-j1", "-DElab.async=false"):
        raise RuntimeError("Inspected Lean compile flags changed")

    unchanged = all((package / name).read_bytes() == data for name, data in inputs.items())
    if not unchanged:
        raise RuntimeError("Package input changed during static review")
    result = {
        "status": "STATIC_REVIEW_AND_PYTHON_CONTROLS_PASS",
        "pass": True,
        "proof_compilation_performed": False,
        "new_lean_audit_performed": False,
        "original_project_olean_rebuild_performed": False,
        "package_sha256": expected,
        "source_count": len(sources),
        "explicit_source_count": len(source_rows),
        "source_declarations_by_module": {row["module"]: len(row["source_declarations"]) for row in source_records},
        "earlier_real_audit_reparsed": {"sha256": previous_hash,
            "all_origin_count": parsed["all_origin_count"],
            "safe_nonpartial_count": parsed["safe_nonpartial_count"],
            "explicit_source_count": parsed["explicit_source_count"]},
        "negative_controls": controls,
        "input_check": {"command": command, "exit_code": process.returncode, "result": input_result},
        "generated_audit_source_sha256": digest(audit_source.encode()),
        "package_inputs_unchanged_after": unchanged,
        "limitations": [
            "These controls use an earlier real ten-module log to test the parser; the parent must compile all 17 sources and execute the generated full audit.",
            "The generated audit is inspected as source in this review, not compiled here.",
            "Lean and external Mathlib cache provenance are reviewed in the package documentation; this script does not rebuild them."
        ]
    }
    (output / "review-result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("status", "source_count", "explicit_source_count", "package_sha256", "negative_controls")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
