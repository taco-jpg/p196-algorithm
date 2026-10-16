#!/usr/bin/env python3
"""Focused negative checks for the proof verifier's acceptance gates."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("finite_horizon_verify", HERE.parent / "verify.py")
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--repo", required=True, type=Path)
    args = parser.parse_args()
    checks = []

    def checked(label, action, reject=False):
        try:
            action()
        except verify.VerificationError as error:
            if not reject:
                raise
            checks.append({"check": label, "result": "PASS", "rejection": str(error)})
        else:
            if reject:
                raise RuntimeError("Verifier unexpectedly accepted: " + label)
            checks.append({"check": label, "result": "PASS"})

    ordinary = '/- sorry /- unsafe -/ native_decide -/\ntheorem test : True := by trivial\n'
    checked("comments do not trigger false rejection", lambda: verify.source_scan(verify.code_only(ordinary)))
    for token, fragment in {
        "sorry": "theorem test : False := by sorry",
        "native_decide": "theorem test : True := by native_decide",
        "custom axiom": "axiom fabricated : False",
        "unsafe": "unsafe def forged : Nat := 0",
        "kernel bypass": "set_option debug.skipKernelTC true",
        "implementation replacement": "@[implemented_by forged] def proof := True",
        "qualified compiler axiom": "def forged := _root_.Lean.ofReduceBool",
    }.items():
        checked(token, lambda fragment=fragment: verify.source_scan(verify.code_only(fragment)), reject=True)
    checked("standard axiom set", lambda: verify.parse_axiom_records(
        "'example' depends on axioms: [propext, Classical.choice, Quot.sound]"))
    for axiom in ["sorryAx", "Lean.ofReduceBool", "Invented.axiom"]:
        checked("reject axiom " + axiom,
                lambda axiom=axiom: verify.parse_axiom_records(f"'example' depends on axioms: [{axiom}]"), reject=True)

    manifest = json.loads((HERE.parent / "source-pins.json").read_text())
    first = manifest["modules"][0]
    with tempfile.TemporaryDirectory(prefix="p196-verifier-guards-") as directory:
        scratch = Path(directory)
        fake_repo = scratch / "repo"
        source = fake_repo / first["source"]
        source.parent.mkdir(parents=True)
        source.write_bytes((args.repo / first["source"]).read_bytes() + b"\n-- changed bytes\n")
        build = scratch / "hash-mismatch-build"
        argv = [sys.executable, str(HERE.parent / "verify.py"), "--lean", str(args.lean),
                "--repo", str(fake_repo), "--build-dir", str(build)]
        process = subprocess.run(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        report = json.loads((build / "verification.json").read_text())
        if process.returncode != 1 or report["status"] != "FAIL" or "Source hash mismatch" not in report["error"]:
            raise RuntimeError("Altered pinned source was not rejected by the CLI")
        checks.append({"check": "altered pinned source rejected by CLI", "result": "PASS", "exit_code": process.returncode})
        original_report = (build / "verification.json").read_bytes()
        process = subprocess.run(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        if process.returncode != 2 or (build / "verification.json").read_bytes() != original_report:
            raise RuntimeError("Nonempty build directory was not preserved")
        checks.append({"check": "nonempty evidence directory preserved", "result": "PASS", "exit_code": process.returncode})
    result = {"result": "PASS", "verifier_sha256": verify.file_digest(HERE.parent / "verify.py"), "checks": checks}
    verify.write_json(HERE / "verifier-guard-checks.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
