#!/usr/bin/env python3
"""Compile the exact source and reject every nonstandard theorem dependency."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
NAMESPACE = "Agent9.ExteriorErasure."


def verify(lean: str, root: Path) -> dict:
    source = root / "ExteriorErasure.lean"
    text = source.read_text(encoding="utf-8")
    names = {NAMESPACE + name for name in re.findall(r"^theorem (\w+)", text, re.M)}
    if not names:
        raise RuntimeError("No theorem declarations found")
    version = subprocess.run([lean, "--version"], check=True, capture_output=True,
                             text=True, timeout=30).stdout.strip()
    if "version 4.19.0," not in version:
        raise RuntimeError(f"Wrong toolchain: {version}")
    result = subprocess.run([lean, source.name], cwd=root, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            timeout=180)
    log = result.stdout
    (root / "ExteriorErasure.compiler.log").write_text(log, encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(f"Lean failed with code {result.returncode}; see compiler log")
    if "sorryAx" in log or "Lean.ofReduceBool" in log:
        raise RuntimeError("Rejected an admitted or native-reduction dependency")
    dependencies = {}
    pattern = r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)"
    for name, raw in re.findall(pattern, log):
        if name in dependencies:
            raise RuntimeError(f"Duplicate theorem audit: {name}")
        dependencies[name] = sorted(x.strip() for x in raw.split(",") if x.strip())
    if set(dependencies) != names:
        raise RuntimeError(f"Audit coverage mismatch: {set(dependencies) ^ names}")
    for name, axioms in dependencies.items():
        if set(axioms) - ALLOWED:
            raise RuntimeError(f"Unaccepted dependencies: {name}: {axioms}")
    record = {
        "status": "PASS", "source": source.name,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "compiler_log_sha256": hashlib.sha256(log.encode()).hexdigest(),
        "lean_version": version, "exit_code": result.returncode,
        "theorem_count": len(names), "dependencies": dependencies,
        "scope": "Self-contained exact exterior formulas, not the entire repository or P196",
    }
    (root / "verification.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", default="lean", help="Lean 4.19.0 executable")
    args = parser.parse_args()
    record = verify(args.lean, Path(__file__).resolve().parent)
    print(json.dumps({k: v for k, v in record.items() if k != "dependencies"}, indent=2))


if __name__ == "__main__":
    main()
