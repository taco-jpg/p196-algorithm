"""Compile every local Lean module in dependency order and retain axiom audits.

Usage: python verify_lean.py --output /path/to/logs [--lean /path/to/lean]
Only the pinned Lean 4.19.0 compiler is accepted. No network or Git writes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--lean", default="lean")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    version = subprocess.check_output([args.lean, "--version"], text=True)
    if not version.startswith("Lean (version 4.19.0,"):
        raise RuntimeError(f"Expected Lean 4.19.0, received {version.strip()}")
    (output / "version.txt").write_text(version)
    files = {p.stem: p for p in source.glob("*.lean")}
    if not files:
        raise RuntimeError("No Lean modules found")
    done: set[str] = set()
    active: set[str] = set()
    order: list[str] = []
    def visit(name: str) -> None:
        if name in done:
            return
        if name in active:
            raise RuntimeError(f"Cyclic local import: {name}")
        active.add(name)
        for line in files[name].read_text().splitlines():
            if line.startswith("import "):
                for dependency in line.split()[1:]:
                    if dependency in files:
                        visit(dependency)
        active.remove(name)
        done.add(name)
        order.append(name)
    for name in sorted(files):
        visit(name)
    records = []
    source_lines = []
    with tempfile.TemporaryDirectory(prefix="agent3-olean-") as temporary:
        env = dict(os.environ, LEAN_PATH=temporary)
        for name in order:
            path = files[name]
            data = path.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            source_lines.append(f"{digest}  {path.name}\n")
            if re.search(r"^\s*(?:private\s+)?axiom\s+", data.decode(), re.M):
                raise RuntimeError(f"Custom axiom declaration in {path.name}")
            result = subprocess.run([args.lean, "-o", str(Path(temporary) / f"{name}.olean"), str(path)],
                                    cwd=source, env=env, capture_output=True, text=True)
            log = result.stdout + result.stderr
            (output / f"{path.name}.log").write_text(log)
            (output / f"{path.name}.exit").write_text(f"{result.returncode}\n")
            if result.returncode or any(bad in log for bad in ("sorryAx", "Lean.ofReduceBool", "declaration uses 'sorry'")):
                raise RuntimeError(f"Unverified module: {path.name}; see retained log")
            declarations = []
            for line in log.splitlines():
                match = re.match(r"'([^']+)' (?:depends on axioms: \[([^]]*)\]|does not depend on any axioms)", line)
                if not match:
                    continue
                axioms = set(filter(None, (x.strip() for x in (match[2] or "").split(","))))
                if not axioms <= ALLOWED_AXIOMS:
                    raise RuntimeError(f"Unexpected axiom dependencies for {match[1]}: {axioms}")
                declarations.append({"name": match[1], "axioms": sorted(axioms)})
            if not declarations:
                raise RuntimeError(f"No axiom audits printed by {path.name}")
            records.append({"file": path.name, "source_sha256": digest, "exit": result.returncode,
                            "declarations": declarations, "log_sha256": hashlib.sha256(log.encode()).hexdigest()})
            print(f"PASS {path.name}: {len(declarations)} audited declarations", flush=True)
    (output / "source-sha256.txt").write_text("".join(source_lines))
    (output / "AUDIT.json").write_text(json.dumps({"version": version.strip(), "order": order,
                                                   "modules": records}, indent=2, sort_keys=True) + "\n")

if __name__ == "__main__":
    main()
