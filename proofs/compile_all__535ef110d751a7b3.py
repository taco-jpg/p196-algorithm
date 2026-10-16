"""Rebuild the complete uniform-escape proof from source with Lean 4.19.0.

Usage: python3 compile_all.py /absolute/path/to/lean
Only the Python standard library and the specified Lean installation are used.
The existing standalone dependency is copied from continuation/, not replaced.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
MODULES = [
    "LychrelDigitSums", "SharedProfile", "ProfileDynamics", "ProfileIsolation",
    "UniformEscape", "DecimalEmbedding", "UniformDecimal",
    "SharpProfileBounds", "SharpUniformEscape", "SharpUniformDecimal",
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lean", help="Lean 4.19.0 executable")
    args = parser.parse_args()
    compiler = str(Path(args.lean).resolve())
    version = subprocess.run([compiler, "--version"], text=True,
                             capture_output=True, check=True).stdout.strip()
    if "version 4.19.0" not in version:
        raise SystemExit("This checkpoint is pinned to Lean 4.19.0: " + version)
    logs = [version + "\n"]
    checks = []
    hashes = {}
    with tempfile.TemporaryDirectory(prefix="uniform-escape-") as temp:
        build = Path(temp)
        for module in MODULES:
            source = ((PROJECT / "continuation") if module == "LychrelDigitSums"
                      else HERE) / (module + ".lean")
            hashes[source.name] = hashlib.sha256(source.read_bytes()).hexdigest()
            shutil.copy2(source, build / source.name)
        environment = dict(os.environ, LEAN_PATH=str(build))
        for module in MODULES:
            start = time.monotonic()
            result = subprocess.run(
                [compiler, "-o", module + ".olean", module + ".lean"],
                cwd=build, env=environment, text=True, capture_output=True,
            )
            item = {"module": module, "exit_code": result.returncode,
                    "seconds": time.monotonic() - start}
            checks.append(item)
            logs.append("\n" + json.dumps(item) + "\n" + result.stdout + result.stderr)
            (HERE / "replay.log").write_text("".join(logs))
            print(json.dumps(item), flush=True)
            if result.returncode:
                raise SystemExit(result.returncode)
        audit = """import UniformDecimal
import SharpUniformDecimal
#print axioms DecimalProfile.uniform_escape
#print axioms DecimalProfile.NumericBridge.mass_numeric_iter
#print axioms DecimalUniformEscape.digitSum_uniform_window
#print axioms DecimalUniformEscape.digitSum_uniform_window_196
#print axioms DecimalProfile.sharpEscapeBound_eq
#print axioms DecimalProfile.sharp_uniform_escape
#print axioms DecimalUniformEscape.digitSum_uniform_window_sharp
#print axioms DecimalUniformEscape.digitSum_uniform_window_196_sharp
"""
        (build / "Audit.lean").write_text(audit)
        result = subprocess.run([compiler, "Audit.lean"], cwd=build,
                                env=environment, text=True, capture_output=True)
        logs.append("\nFinal axiom audit\n" + result.stdout + result.stderr)
        (HERE / "replay.log").write_text("".join(logs))
        if result.returncode:
            raise SystemExit(result.returncode)
        for line in result.stdout.splitlines():
            if "depends on axioms:" in line:
                names = line.split("depends on axioms:", 1)[1].strip().strip("[]")
                if not set(names.split(", ")) <= {"propext", "Classical.choice", "Quot.sound"}:
                    raise SystemExit("Unexpected axiom dependency: " + line)
        record = {"status": "PASS", "compiler": version, "modules": checks,
                  "source_sha256": hashes, "axiom_audit": result.stdout.splitlines()}
        (HERE / "replay.json").write_text(json.dumps(record, indent=2) + "\n")
        print("Full source rebuild and axiom audit passed.")


if __name__ == "__main__":
    main()
