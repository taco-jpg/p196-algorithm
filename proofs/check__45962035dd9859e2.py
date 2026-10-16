#!/usr/bin/env python3
"""Fresh source build and complete public-declaration axiom audit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
DEP = ROOT / "proofs/contributions/agent6-complementary-bulk"
MODULES = [(DEP / (n + ".lean")) for n in
           ("ExteriorCore", "ExteriorCapTwo", "ExteriorCoverage")]
MODULES.append(HERE / "RadixExterior.lean")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lean")
    ap.add_argument("--evidence", type=Path, required=True)
    args = ap.parse_args()
    evidence = args.evidence.resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    build = evidence / "build"
    build.mkdir()
    env = dict(os.environ, LEAN_PATH=str(build))
    report = {"status": "INCOMPLETE", "modules": [], "commands": [],
              "allowed_axioms": ["propext", "Classical.choice", "Quot.sound"]}

    def run(label, cmd):
        started = time.monotonic()
        proc = subprocess.run(cmd, cwd=build, env=env, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = evidence / (label + ".log")
        log.write_text(proc.stdout)
        record = {"command": cmd, "exit_code": proc.returncode,
                  "seconds": time.monotonic() - started,
                  "log": log.name, "log_sha256": digest(log)}
        report["commands"].append(record)
        (evidence / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
        if proc.returncode:
            raise RuntimeError(f"{label} failed; see {log}")
        return proc.stdout

    version = run("version", [args.lean, "--version"])
    if "4.19.0" not in version or "6caaee842e94" not in version:
        raise RuntimeError("Expected official Lean 4.19.0 release commit")
    for src in MODULES:
        shutil.copy2(src, build / src.name)
        report["modules"].append({"source": str(src.relative_to(ROOT)),
                                  "sha256": digest(src)})
        run(src.stem, [args.lean, "-DmaxHeartbeats=0", "-DmaxRecDepth=100000",
                       "-o", src.stem + ".olean", src.name])

    source = (HERE / "RadixExterior.lean").read_text()
    forbidden = re.findall(r"\b(?:sorry|admit|native_decide|axiom|unsafe)\b", source)
    if forbidden:
        raise RuntimeError(f"Forbidden proof token: {forbidden}")
    names = re.findall(r"^theorem\s+(\w+)", source, re.M)
    audit = "import RadixExterior\n" + "\n".join(
        "#print axioms Agent110.RadixExterior." + n for n in names) + "\n"
    (build / "AxiomAudit.lean").write_text(audit)
    stdout = run("AxiomAudit", [args.lean, "AxiomAudit.lean"])
    reports = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", stdout, re.S)
    reports += [(n, "") for n in re.findall(r"'([^']+)' does not depend on any axioms", stdout)]
    if len(reports) != len(names):
        raise RuntimeError(f"Expected {len(names)} audits, found {len(reports)}")
    used = sorted({a.strip() for _, axioms in reports for a in axioms.split(",") if a.strip()})
    if set(used) - set(report["allowed_axioms"]):
        raise RuntimeError(f"Unexpected axioms {used}")
    report.update(status="PASS", new_theorems=len(names), audited_names=[n for n, _ in reports],
                  actual_axiom_union=used, source_scan="PASS")
    (evidence / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "new_theorems": len(names),
                      "actual_axiom_union": used}))


if __name__ == "__main__":
    main()
