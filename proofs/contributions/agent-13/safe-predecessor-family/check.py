#!/usr/bin/env python3
"""Agent #13: clean Lean 4.19.0 build and transitive axiom audit.
Usage: python3 check.py --lean /absolute/path/to/lean --out /new/audit/directory
No network, compiler-trusted evaluation, or reused project objects.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MODULES = ("LychrelDigitSums", "Family", "TargetSafety", "Counting")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    lean = args.lean.resolve(strict=True)
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    here = Path(__file__).resolve().parent
    repo = here.parents[3]
    base = repo / "proofs/research/continuation/LychrelDigitSums.lean"
    version = subprocess.check_output([str(lean), "--version"], text=True)
    (out / "lean-version.txt").write_text(version)
    if "version 4.19.0," not in version or "6caaee842e94" not in version:
        raise SystemExit("The exact pinned Lean 4.19.0 compiler is required.")
    theorem_names: list[str] = []
    source_hashes: dict[str, str] = {}
    steps: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="agent13-clean-") as temp:
        build = Path(temp)
        for name in MODULES:
            src = base if name == "LychrelDigitSums" else here / (name + ".lean")
            data = src.read_bytes()
            source_hashes[str(src.relative_to(repo))] = hashlib.sha256(data).hexdigest()
            (build / src.name).write_bytes(data)
            if name != "LychrelDigitSums":
                theorem_names += re.findall(r"^theorem\s+(\w+)", data.decode(), re.MULTILINE)
        audit = "import Counting\n\n" + "\n".join(
            "#print axioms Agent13SafeFamily." + n for n in theorem_names
        ) + "\n"
        (build / "AllAxioms.lean").write_text(audit)
        (out / "AllAxioms.lean").write_text(audit)
        env = os.environ.copy()
        env["LEAN_PATH"] = str(build)
        for name in (*MODULES, "AllAxioms"):
            cmd = [str(lean), "-o", name + ".olean", name + ".lean"]
            start = time.monotonic()
            with (out / (name + ".log")).open("wb") as log:
                result = subprocess.run(cmd, cwd=build, env=env, stdout=log,
                                        stderr=subprocess.STDOUT, timeout=600, check=False)
            steps.append({"module": name, "command": cmd, "exit": result.returncode,
                          "seconds": round(time.monotonic() - start, 3)})
            (out / "build-steps.json").write_text(json.dumps(steps, indent=2) + "\n")
            if result.returncode:
                raise SystemExit(f"Build failed: {name}; see retained log.")
        text = (out / "AllAxioms.log").read_text()
        reports = re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", text)
        expected = {"Agent13SafeFamily." + n for n in theorem_names}
        if {name for name, _ in reports} != expected:
            raise SystemExit("Axiom report does not exactly cover all exported theorems.")
        for name, ax in reports:
            actual = {a.strip() for a in ax.split(",") if a.strip()}
            if not actual <= ALLOWED_AXIOMS:
                raise SystemExit(f"Rejected transitive axioms for {name}: {actual}")
    report = {"agent": 13, "source_snapshot": "c2b6977e43a79caa5ff3bb88801f3ba896986f38",
              "verification": "LEAN_CHECKED; clean local rebuild; not independent-agent review",
              "version": version.strip(), "source_sha256": source_hashes,
              "theorem_count": len(theorem_names), "axiom_audits": len(reports),
              "permitted_foundational_axioms": sorted(ALLOWED_AXIOMS), "steps": steps}
    (out / "RESULT.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
