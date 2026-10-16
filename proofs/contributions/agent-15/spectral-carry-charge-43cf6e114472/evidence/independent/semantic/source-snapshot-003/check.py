#!/usr/bin/env python3
"""Rebuild the complete standalone spectral carry-charge project from source.

The output directory must be new. Source copies and complete logs are retained.
No existing project objects are imported. The installed Lean standard library
is the pinned external dependency; its executable and shared library are hashed.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

MODULES = ["SpectralWeights", "BinaryCode", "ChargeSymmetry", "SourceFormula"]
NAMESPACE = "P196.Agent15.SpectralCarry"
FLAGS = ["--trust=0", "-j1", "-DElab.async=false"]
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    lean = args.lean.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = output / "source"
    logs = output / "logs"
    source.mkdir()
    logs.mkdir()
    root = Path(__file__).resolve().parent
    env = os.environ.copy()
    env["LEAN_PATH"] = str(source)
    records = []
    pins = {}
    exports = []
    for module in MODULES:
        original = root / (module + ".lean")
        target = source / original.name
        shutil.copyfile(original, target)
        pins[module] = {"sha256": digest(target), "bytes": target.stat().st_size}
        text = target.read_text()
        # Names are also checked by the independent module-origin audit.
        for kind, name in re.findall(r"^(?:@\[[^\n]*\]\s*)?(def|theorem)\s+([A-Za-z0-9_']+)", text, re.M):
            exports.append({"kind": kind, "name": NAMESPACE + "." + name})
    (output / "source-pins.json").write_text(json.dumps(pins, indent=2) + "\n")
    (output / "exports.json").write_text(json.dumps(exports, indent=2) + "\n")
    compiler = {"path": str(lean), "sha256": digest(lean)}
    shared = lean.parent.parent / "lib" / "lean" / "libleanshared.so"
    if shared.exists():
        compiler["shared_library_sha256"] = digest(shared)

    def run(name, argv):
        started = time.monotonic()
        result = subprocess.run(argv, cwd=source, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (logs / (name + ".log")).write_text(result.stdout)
        records.append({"name": name, "argv": [str(x) for x in argv],
                        "cwd": str(source), "LEAN_PATH": str(source),
                        "exit_code": result.returncode,
                        "seconds": time.monotonic() - started})
        return result

    version = run("lean-version", [lean, "--version"])
    ok = version.returncode == 0 and "version 4.19.0" in version.stdout and "6caaee842e94" in version.stdout
    for module in MODULES:
        if not ok:
            break
        result = run(module, [lean, *FLAGS, "-o", module + ".olean", module + ".lean"])
        ok = result.returncode == 0
    if ok:
        audit = "import SourceFormula\n" + "\n".join(
            "#print " + entry["name"] + "\n#print axioms " + entry["name"] for entry in exports
        ) + "\n"
        (source / "PublicAudit.lean").write_text(audit)
        result = run("PublicAudit", [lean, *FLAGS, "PublicAudit.lean"])
        ok = result.returncode == 0
        if ok:
            dependencies = []
            seen = set()
            for match in re.finditer(r"'([^']+)' (does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])", result.stdout, re.S):
                name = match.group(1)
                axioms = [] if match.group(2).startswith("does not") else [a.strip() for a in match.group(3).split(",") if a.strip()]
                dependencies.append({"name": name, "axioms": axioms})
                seen.add(name)
                ok = ok and set(axioms) <= ALLOWED
            ok = ok and seen == {entry["name"] for entry in exports}
            (output / "public-axioms.json").write_text(json.dumps(dependencies, indent=2) + "\n")
    unchanged = all(digest(source / (module + ".lean")) == pins[module]["sha256"] for module in MODULES)
    ok = ok and unchanged and digest(lean) == compiler["sha256"]
    receipt = {"status": "PASS" if ok else "FAIL", "modules": MODULES,
               "source_pins": pins, "public_exports": exports, "compiler": compiler,
               "commands": records, "source_unchanged": unchanged,
               "scope": "Complete selected local source closure and literal public declarations; independent module-origin audit is separate."}
    (output / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "output": str(output),
                      "commands": len(records), "public_exports": len(exports)}))
    if not ok:
        for record in records:
            if record["exit_code"]:
                print((logs / (record["name"] + ".log")).read_text())
        raise SystemExit(1)


if __name__ == "__main__":
    main()
