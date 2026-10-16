#!/usr/bin/env python3
"""Freshly compile the integer reflection bridge and every theorem dependency."""

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
REPO = HERE.parents[2]
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SOURCE_PATHS = [
    HERE.parent / "2026-10-14-base-uniqueness-formal" / "SignedDigitUniqueness.lean",
    HERE / "BaseReflection.lean",
    HERE / "ResetNormalization.lean",
    HERE / "PhysicalWidth.lean",
    HERE / "SeamSafety.lean",
]


def hashes() -> dict[str, dict[str, str]]:
    result = {}
    for path in SOURCE_PATHS:
        blob = path.read_bytes()
        result[str(path.relative_to(REPO))] = {
            "sha256": hashlib.sha256(blob).hexdigest(),
            "git_blob_sha1": hashlib.sha1(
                f"blob {len(blob)}\0".encode() + blob
            ).hexdigest(),
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lean", help="Lean 4.19.0 executable or environment wrapper")
    args = parser.parse_args()
    lean = shutil.which(args.lean)
    if lean is None:
        raise SystemExit(f"Lean executable unavailable: {args.lean}")
    report_path = HERE / "verification.json"
    log_path = HERE / "compile.log"
    # A previous successful report must not survive a failed current run.
    report_path.unlink(missing_ok=True)
    original_hashes = hashes()
    names = []
    for path in SOURCE_PATHS:
        source = path.read_text()
        forbidden = re.findall(r"\b(?:sorry|admit|axiom|native_decide)\b", source)
        if forbidden:
            raise SystemExit(f"Disallowed source tokens in {path.name}: {forbidden}")
        names.extend(f"{path.stem}.{name}" for name in
                     re.findall(r"^theorem\s+(\w+)", source, flags=re.MULTILINE))
    if not names:
        raise SystemExit("No theorem declarations found")
    version = subprocess.run(
        [lean, "--version"], check=True, text=True, capture_output=True
    ).stdout.strip()
    if "version 4.19.0" not in version:
        raise SystemExit(f"Expected Lean 4.19.0; found {version}")
    compile_times = {}
    with tempfile.TemporaryDirectory(prefix="p196-base-reflection-") as directory:
        build = Path(directory)
        env = dict(os.environ, LEAN_PATH=str(build))
        with log_path.open("w") as log:
            log.write(version + "\n")
            for path in SOURCE_PATHS:
                shutil.copyfile(path, build / path.name)
                started = time.monotonic()
                result = subprocess.run(
                    [lean, "-o", str(build / f"{path.stem}.olean"), str(build / path.name)],
                    cwd=build, env=env, text=True, capture_output=True,
                )
                compile_times[path.name] = round(time.monotonic() - started, 3)
                log.write(f"\n### {path.name}\n{result.stdout}{result.stderr}")
                log.flush()
                if result.returncode:
                    raise SystemExit(f"Compilation failed: {path.name}; see {log_path}")
            audit = build / "AllAxioms.lean"
            audit.write_text("import SeamSafety\n" + "\n".join(
                f"#print axioms {name}" for name in names
            ) + "\n")
            started = time.monotonic()
            result = subprocess.run(
                [lean, str(audit)], cwd=build, env=env, text=True, capture_output=True
            )
            compile_times["AllAxioms.lean"] = round(time.monotonic() - started, 3)
            log.write(f"\n### AllAxioms.lean\n{result.stdout}{result.stderr}")
            if result.returncode:
                raise SystemExit("Axiom-audit compilation failed")
            records = re.findall(
                r"'([^']+)' depends on axioms: \[([^\]]*)\]",
                result.stdout,
            )
            audited = {name: sorted(a.strip() for a in ax.split(",") if a.strip())
                       for name, ax in records}
            # Lean uses this spelling for a theorem needing no axioms.
            for name in re.findall(
                r"'([^']+)' does not depend on any axioms", result.stdout
            ):
                audited[name] = []
            if set(audited) != set(names):
                raise SystemExit(f"Incomplete audit: expected {names}; got {list(audited)}")
            for name, axioms in audited.items():
                if not set(axioms) <= ALLOWED_AXIOMS:
                    raise SystemExit(f"Unapproved axiom dependency in {name}: {axioms}")
    if hashes() != original_hashes:
        raise SystemExit("Sources changed during verification")
    report = {
        "result": "PASS",
        "lean_version": version,
        "fresh_source_rebuild": True,
        "theorem_count": len(names),
        "sources": original_hashes,
        "axiom_audit": audited,
        "compile_seconds": compile_times,
        "scope": "All-base integer reflection identities, actual reset-carry normalization and raw placement, and symmetry equivalence at canonical physical width with digit bounds/value/positive leading output. Actual/reset outgoing carry mismatch certifies nonpalindromicity. Every reset pattern is covered; no separate nested block-list equivalence or ordinary reverse-add iteration/infinite-orbit theorem.",
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(f"PASS: {len(names)} theorems audited after fresh source rebuild")
    print(report_path)


if __name__ == "__main__":
    main()
