#!/usr/bin/env python3
"""Clean-source build and complete transitive theorem-axiom audit for Agent 11."""
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

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CONTRIB = HERE.parents[1]
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
PREREQUISITES = [
    CONTRIB / "2026-10-14-base-uniqueness-formal/SignedDigitUniqueness.lean",
    *[CONTRIB / f"2026-10-15-base-reflection-formal/{name}.lean" for name in
      ("BaseReflection", "ResetNormalization", "PhysicalWidth", "SeamSafety")],
    CONTRIB / "2026-10-15-base-reverse-add-formal/ReverseAdd.lean",
]
OWN_MODULES = ["HighBaseNormalization", "HighBasePairs", "HighBaseThreshold", "HighBaseNumeric", "HighBaseFirstHit"]
SOURCE_PATHS = PREREQUISITES + [HERE / f"{m}.lean" for m in OWN_MODULES]

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lean", help="Lean 4.19.0 executable")
    parser.add_argument("--out", type=Path, required=True, help="new run-specific output directory")
    args = parser.parse_args()
    lean = shutil.which(args.lean)
    if lean is None:
        raise SystemExit(f"Lean executable not found: {args.lean}")
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    version = subprocess.check_output([lean, "--version"], text=True).strip()
    if "version 4.19.0," not in version:
        raise SystemExit(f"Expected Lean 4.19.0: {version}")
    actual_modules = {p.stem for p in HERE.glob("*.lean")}
    if actual_modules != set(OWN_MODULES):
        raise SystemExit(f"Unreconciled proof build coverage: {actual_modules ^ set(OWN_MODULES)}")
    theorem_names, definition_names, source_hashes = [], [], {}
    for p in SOURCE_PATHS:
        text = p.read_text()
        # Every accepted source is explicit; historical attempts are never imported.
        if re.search(r"\b(?:sorry|admit|sorryAx|axiom|native_decide|ofReduceBool|trustCompiler)\b", text):
            raise SystemExit(f"Excluded proof token in accepted source: {p}")
        namespace = "Agent11HighBase" if p.parent == HERE else p.stem
        prefix = r"^(?:@\[[^\]]*\]\s*)?"
        theorem_names += [f"{namespace}.{n}" for n in re.findall(prefix + r"(?:theorem|lemma)\s+(\w+)", text, re.M)]
        definition_names += [f"{namespace}.{n}" for n in re.findall(prefix + r"(?:noncomputable\s+)?def\s+(\w+)", text, re.M)]
        data = p.read_bytes()
        source_hashes[str(p.relative_to(REPO))] = {
            "sha256": sha(data),
            "git_blob_sha1": hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest(),
        }
    names = theorem_names + definition_names
    if len(set(names)) != len(names) or not theorem_names:
        raise SystemExit("Duplicate declarations or empty theorem audit")
    report = {
        "result": "INCOMPLETE", "lean_version": version,
        "source_snapshot": "74df59c5ecb6cb30fb3c88b1d5b26fdb9526d6c4",
        "fresh_source_rebuild": True, "sources": source_hashes,
        "commands": [], "allowed_axioms": sorted(ALLOWED),
        "independent_semantic_review": False,
    }
    (out / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    with tempfile.TemporaryDirectory(prefix="agent11-clean-") as directory:
        build = Path(directory)
        env = dict(os.environ, LEAN_PATH=str(build))
        with (out / "compile.log").open("w") as log:
            log.write(version + "\n")
            def run(module: str, emit: bool) -> str:
                cmd = [lean] + (["-o", f"{module}.olean"] if emit else []) + [f"{module}.lean"]
                started = time.monotonic()
                proc = subprocess.run(cmd, cwd=build, env=env, text=True, capture_output=True, timeout=180)
                report["commands"].append({"command": cmd, "exit_status": proc.returncode,
                    "seconds": round(time.monotonic() - started, 3)})
                log.write("\nCOMMAND " + " ".join(cmd) + "\nEXIT " + str(proc.returncode) + "\n" + proc.stdout + proc.stderr)
                log.flush()
                if proc.returncode:
                    (out / "result.json").write_text(json.dumps(report, indent=2) + "\n")
                    raise SystemExit(f"Failed: {module}; retained log at {out}")
                return proc.stdout
            for p in SOURCE_PATHS:
                shutil.copy2(p, build / p.name)
                run(p.stem, True)
            audit = "import " + OWN_MODULES[-1] + "\n" + "\n".join("#print axioms " + n for n in names) + "\n"
            (build / "AllAxioms.lean").write_text(audit)
            (out / "AllAxioms.lean").write_text(audit)
            text = run("AllAxioms", False)
            records = {n: sorted(x.strip() for x in ax.split(",") if x.strip())
                for n, ax in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text)}
            for n in re.findall(r"'([^']+)' does not depend on any axioms", text):
                records[n] = []
            if set(records) != set(names):
                raise SystemExit(f"Incomplete axiom coverage: {set(names) ^ set(records)}")
            if any(not set(axioms) <= ALLOWED for axioms in records.values()):
                raise SystemExit("Unapproved transitive axiom")
    for p in SOURCE_PATHS:
        if sha(p.read_bytes()) != source_hashes[str(p.relative_to(REPO))]["sha256"]:
            raise SystemExit("Sources changed during checking")
    report.update(result="PASS", axiom_audit=records, theorem_count=len(theorem_names),
                  definition_count=len(definition_names),
                  own_theorem_count=sum(n.startswith("Agent11HighBase.") for n in theorem_names),
                  own_definition_count=sum(n.startswith("Agent11HighBase.") for n in definition_names))
    (out / "result.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(f"PASS: {report['theorem_count']} theorems, {report['definition_count']} definitions; "
          f"Agent 11: {report['own_theorem_count']} theorems, {report['own_definition_count']} definitions")

if __name__ == "__main__":
    main()
