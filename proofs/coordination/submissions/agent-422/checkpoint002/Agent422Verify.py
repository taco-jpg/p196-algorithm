#!/usr/bin/env python3
"""Clean, offline Lean build and transitive axiom audit for Agent #422 modules.

Usage: python3 proofs/Agent422Verify.py --lean /absolute/path/to/lean \
         --output /absolute/new/output/directory
The output directory must not exist. No cached project .olean is imported.
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
import time

MODULES = ("Agent422BaseDigits", "Agent422NormalizationSharpness", "Agent422OverflowRuns")
DECIMAL_BLOB = "c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506"
ALLOWED_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}


def without_comments(text: str) -> str:
    """Strip nested Lean block comments and line comments for token checks."""
    output: list[str] = []
    i = depth = 0
    while i < len(text):
        if text.startswith("/-", i):
            depth += 1
            i += 2
        elif depth and text.startswith("-/", i):
            depth -= 1
            i += 2
        elif depth:
            output.append("\n" if text[i] == "\n" else " ")
            i += 1
        elif text.startswith("--", i):
            j = text.find("\n", i)
            i = len(text) if j < 0 else j
        else:
            output.append(text[i])
            i += 1
    if depth:
        raise ValueError("Unclosed Lean block comment")
    return "".join(output)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path, env: dict[str, str], log: Path,
        timeout: int) -> dict[str, object]:
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=cwd, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        data = exc.stdout or b""
        log.write_text(data.decode(errors="replace") if isinstance(data, bytes) else data)
        raise RuntimeError(f"Build timed out after {timeout}s; see {log}") from exc
    log.write_text(result.stdout)
    record = {"command": command, "exit_status": result.returncode,
              "elapsed_seconds": round(time.monotonic() - started, 3),
              "log": log.name}
    if result.returncode:
        raise RuntimeError(f"Command failed with exit {result.returncode}; see {log}")
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, help="Lean 4.19.0 executable")
    parser.add_argument("--output", type=Path, required=True,
                        help="New output directory; existing paths are rejected")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--decimal-source", type=Path,
                        help="Optional exact original Lychrel196Research.lean; rebuilt from source")
    args = parser.parse_args()
    modules = list(MODULES)
    if args.decimal_source is not None:
        modules.append("Agent422DecimalCompatibility")
    executable = shutil.which(args.lean)
    if not executable:
        raise FileNotFoundError(f"Lean executable not found: {args.lean}")
    lean = str(Path(executable).resolve())
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    source = out / "source"
    source.mkdir()
    env = dict(os.environ)
    env["LEAN_PATH"] = str(source)
    root = Path(__file__).resolve().parent
    manifest: dict[str, object] = {
        "agent": "Agent #422", "status": "STARTED", "modules": modules,
        "allowed_foundational_axioms": sorted(ALLOWED_AXIOMS),
        "source_sha256": {}, "builds": [],
        "review_level": "self-review and clean rebuild; not independent review",
        "integration_status": "not asserted by this verifier",
    }
    try:
        version = subprocess.check_output([lean, "--version"], text=True).strip()
        manifest["toolchain"] = version
        if "version 4.19.0," not in version:
            raise RuntimeError(f"Unexpected toolchain: {version}")
        exports: list[str] = []
        for module in modules:
            src = root / f"{module}.lean"
            text = src.read_text()
            code = without_comments(text)
            forbidden = re.findall(r"\b(?:sorry|admit|sorryAx|axiom|native_decide)\b", code)
            if forbidden:
                raise RuntimeError(f"Excluded proof token in {module}: {forbidden}")
            namespaces = re.findall(r"^namespace\s+(\w+)\s*$", code, re.MULTILINE)
            if namespaces != [module]:
                raise RuntimeError(f"Unexpected namespace organization in {module}")
            names = re.findall(r"^theorem\s+(\w+)", code, re.MULTILINE)
            if not names:
                raise RuntimeError(f"No theorem exports found in {module}")
            exports.extend(f"{module}.{name}" for name in names)
            shutil.copy2(src, source / src.name)
            manifest["source_sha256"][src.name] = sha256(src)
        if args.decimal_source is not None:
            original = args.decimal_source.resolve()
            data = original.read_bytes()
            blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            if blob != DECIMAL_BLOB:
                raise RuntimeError(f"Original decimal dependency pin mismatch: {blob}")
            original_code = without_comments(data.decode("utf-8"))
            forbidden = re.findall(r"\b(?:sorry|admit|sorryAx|axiom|native_decide)\b", original_code)
            if forbidden:
                raise RuntimeError(f"Excluded token in original decimal dependency: {forbidden}")
            shutil.copy2(original, source / "Lychrel196Research.lean")
            manifest["decimal_dependency"] = {"git_blob": blob, "sha256": sha256(original),
                "original_commit": "2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5"}
        for module in modules:
            if module == "Agent422DecimalCompatibility":
                manifest["builds"].append(run(
                    [lean, "-o", "Lychrel196Research.olean", "Lychrel196Research.lean"],
                    source, env, out / "Lychrel196Research.log", args.timeout))
            manifest["builds"].append(run(
                [lean, "-o", f"{module}.olean", f"{module}.lean"], source,
                env, out / f"{module}.log", args.timeout))
        audit = "\n".join(f"import {module}" for module in modules) + "\n\n"
        audit += "\n".join(f"#print axioms {name}" for name in exports) + "\n"
        (source / "Agent422Audit.lean").write_text(audit)
        manifest["audit"] = run([lean, "Agent422Audit.lean"], source, env,
                                out / "axioms.log", args.timeout)
        text = (out / "axioms.log").read_text()
        actual: dict[str, list[str]] = {}
        for name, axioms in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", text):
            actual[name] = [a.strip() for a in axioms.split(",") if a.strip()]
        for name in re.findall(r"'([^']+)' does not depend on any axioms", text):
            actual[name] = []
        if set(actual) != set(exports):
            raise RuntimeError("Axiom output does not exactly match the expected export set")
        rejected = {name: sorted(set(items) - ALLOWED_AXIOMS)
                    for name, items in actual.items() if set(items) - ALLOWED_AXIOMS}
        if rejected:
            raise RuntimeError(f"Unapproved transitive axioms: {rejected}")
        manifest["exported_theorems"] = actual
        manifest["theorem_count"] = len(exports)
        manifest["status"] = "LEAN_CHECKED"
        manifest["scope_warning"] = (
            "Theorem counts are audit metadata, not counts of independent discoveries. "
            "No complete-repository coverage or Lychrel existence conclusion follows.")
        print(json.dumps({"status": manifest["status"], "theorems": len(exports),
                          "modules": modules, "output": str(out)}, indent=2))
        return 0
    except Exception as exc:
        manifest["status"] = "FAILED"
        manifest["error"] = str(exc)
        raise
    finally:
        (out / "verification.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
