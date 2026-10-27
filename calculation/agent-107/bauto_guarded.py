#!/usr/bin/env python3
"""Guard the existing B automaton's CLI and completion reporting.

Build once:
    python3 calculation/agent-107/bauto_guarded.py --build /tmp/bauto-107
    /tmp/bauto-107 10 11 11 -g 11100010000 -w

Or compile temporarily and run:
    python3 calculation/agent-107/bauto_guarded.py 10 16 16 -g 1000100010001000

Native options: -w, -v, -g BITS, -part INDEX COUNT, -cap STATES,
-depth LAYERS. Exit 0 means every selected stream was exhausted, 3 means
at least one selected stream remains undecided, and 2 means an input/build
error. Inspect STREAM records for accepted streams even on exit 3.

The mathematical transition functions are read from the existing repository
source. Only its main routine is replaced, in a temporary translation unit.
No original source is changed and no duplicate automaton is committed.
"""

from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "neutral_band" / "structure" / "bauto.cpp"
DRIVER = HERE / "bauto_driver.cpp.inc"
MAIN_MARKER = "\nint main(int argc,char**argv){"


def build(output: Path) -> dict:
    original = SOURCE.read_bytes()
    driver = DRIVER.read_bytes()
    text = original.decode("utf-8")
    if text.count(MAIN_MARKER) != 1:
        raise ValueError("upstream main boundary changed; inspect before adapting")
    prefix = text.split(MAIN_MARKER, 1)[0]
    source_hash = hashlib.sha256(original).hexdigest()
    driver_hash = hashlib.sha256(driver).hexdigest()
    unit = (prefix + "\n#define AGENT107_SOURCE_SHA \"" + source_hash + "\"\n"
            + "#define AGENT107_DRIVER_SHA \"" + driver_hash + "\"\n"
            + driver.decode("utf-8"))
    output = output.resolve()
    if not output.parent.is_dir():
        raise ValueError("build output directory does not exist")
    compiler = os.environ.get("CXX", "c++")
    with tempfile.TemporaryDirectory(prefix="p196-agent107-build-") as scratch:
        cpp = Path(scratch) / "guarded.cpp"
        cpp.write_text(unit, encoding="utf-8")
        subprocess.run([compiler, "-O2", "-std=c++17", str(cpp), "-o", str(output)],
                       check=True)
    return {"type": "BUILD", "binary": str(output),
            "source_sha256": source_hash, "driver_sha256": driver_hash}


def main() -> int:
    args = sys.argv[1:]
    try:
        if args[:1] == ["--build"]:
            if len(args) != 2:
                raise ValueError("usage: bauto_guarded.py --build OUTPUT")
            print(json.dumps(build(Path(args[1])), sort_keys=True))
            return 0
        with tempfile.TemporaryDirectory(prefix="p196-agent107-run-") as scratch:
            binary = Path(scratch) / "bauto_guarded"
            build(binary)
            return subprocess.run([str(binary), *args]).returncode
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"type": "ERROR", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
