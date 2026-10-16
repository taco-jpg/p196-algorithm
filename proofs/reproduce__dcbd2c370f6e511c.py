#!/usr/bin/env python3
"""Rebuild the pinned Agent 122 candidate in a new directory; retain every log."""
from __future__ import annotations
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
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--repository", type=Path, default=HERE.parents[3])
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    build = args.output / "build"
    build.mkdir()
    report: dict = {"status": "RUNNING", "steps": [], "source_sha256": {}}
    def save() -> None:
        (args.output / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    def run(label: str, command: list[str]) -> str:
        started = time.monotonic()
        process = subprocess.run(command, cwd=build, env={**os.environ, "LEAN_PATH": str(build)},
                                 text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (args.output / f"{label}.log").write_text(process.stdout)
        report["steps"].append({"label": label, "command": command, "exit": process.returncode,
                                "seconds": time.monotonic() - started})
        save()
        if process.returncode:
            raise RuntimeError(f"{label} failed; full output retained")
        return process.stdout
    try:
        lean = str(args.lean.resolve())
        version = run("toolchain", [lean, "--version"])
        if "version 4.19.0," not in version or "6caaee842e94" not in version:
            raise RuntimeError("Expected the pinned Lean 4.19.0 release")
        report["lean_sha256"] = sha(args.lean)
        pins = json.loads((HERE / "dependency-pins.json").read_text())
        report["base_source_commit"] = pins["source_commit"]
        for rel, digest in pins["sha256"].items():
            path = args.repository / rel
            if sha(path) != digest:
                raise RuntimeError(f"Pinned source mismatch: {rel}")
            report["source_sha256"][rel] = digest
        research = args.repository / "proofs/research"
        base = (research / "Lychrel196Research.lean").read_text()
        continuation = (research / "continuation/LychrelDigitSums.lean").read_text()
        if base.removeprefix("import Std\n") not in continuation:
            raise RuntimeError("Base source is not byte-identically included in continuation")
        dependency_paths = [
            "proofs/research/continuation/LychrelDigitSums.lean",
            "proofs/contributions/agent-108/modular-autonomy/AutonomyDefs.lean",
            "proofs/contributions/agent-108/modular-autonomy/LeadingWitness.lean",
            "proofs/contributions/agent-13/safe-predecessor-family/Family.lean",
            "proofs/research/main_existence_attempt/ancestry_direct_pass/lean/FiniteAncestry.lean",
            "proofs/contributions/agent-12/FixedTarget.lean",
        ]
        dependencies = []
        for rel in dependency_paths:
            path = args.repository / rel
            destination = build / path.name
            shutil.copyfile(path, destination)
            if path.name == "AutonomyDefs.lean":
                content = destination.read_text()
                old = "import Lychrel196Research"
                if not content.startswith(old + "\n"):
                    raise RuntimeError("Unexpected import adapter input")
                destination.write_text(content.replace(old, "import LychrelDigitSums", 1))
                if sha(destination) != pins["import_adaptation"]["adapted_sha256"]:
                    raise RuntimeError("Unexpected adapted source bytes")
            dependencies.append(path.stem)
        modules = json.loads((HERE / "accepted-modules.json").read_text())
        for module in modules:
            source = HERE / f"{module}.lean"
            shutil.copyfile(source, build / source.name)
            report["source_sha256"][source.name] = sha(source)
        for module in dependencies + modules:
            run(module, [lean, "-o", f"{module}.olean", f"{module}.lean"])
        text = (args.output / "Audit.log").read_text()
        audited = {}
        for name, entries in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text):
            audited[name] = [entry.strip() for entry in entries.split(",") if entry.strip()]
        for name in re.findall(r"'([^']+)' does not depend on any axioms", text):
            audited[name] = []
        expected = []
        for module in modules:
            if module not in {"All", "Audit"}:
                expected += ["Agent122.Countermodel." + name for name in
                             re.findall(r"^theorem\s+(\w+)", (HERE / f"{module}.lean").read_text(), re.M)]
        if set(audited) != set(expected):
            raise RuntimeError("Audit does not match every candidate theorem export")
        for name, axioms in audited.items():
            if set(axioms) - ALLOWED_AXIOMS:
                raise RuntimeError(f"Excluded dependency for {name}: {axioms}")
        report.update(status="PASS", theorem_axioms=audited,
                      axiom_union=sorted({a for entries in audited.values() for a in entries}),
                      independent_review=False)
        save()
        return 0
    except Exception as error:
        report.update(status="FAIL", error=str(error))
        save()
        raise

if __name__ == "__main__":
    raise SystemExit(main())
