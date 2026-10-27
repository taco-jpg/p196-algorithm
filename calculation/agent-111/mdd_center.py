#!/usr/bin/env python3
"""Build Agent111's exact MDD engine with the pinned existing local transfer.

The generated header is temporary. The engine preserves long_center's CLI;
use long_center.run() for bounded execution. Extra engine flags are -diff,
-diff-limit N, -work-cap N, and -layers N. -cap limits cumulative MDD nodes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

import long_center


def build(output: str | Path, sanitize: bool = False, compiler: str = "c++") -> Path:
    directory = Path(__file__).resolve().parent
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    flags = ["-std=c++17", "-O2"]
    if sanitize:
        flags = ["-std=c++17", "-O1", "-g", "-fsanitize=address,undefined",
                 "-fno-omit-frame-pointer", "-fno-pie", "-no-pie"]
    with tempfile.TemporaryDirectory(prefix="agent111-mdd-") as temp:
        header = Path(temp) / "a111_existing.hpp"
        header.write_text(long_center.patched_source(), encoding="utf-8")
        subprocess.run([compiler, *flags, "-I", temp, str(directory / "mdd_center.cpp"),
                        "-o", str(output)], check=True, timeout=180)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build"])
    parser.add_argument("output", type=Path)
    parser.add_argument("--sanitize", action="store_true")
    parser.add_argument("--compiler", default="c++")
    args = parser.parse_args()
    binary = build(args.output, args.sanitize, args.compiler)
    print(json.dumps({"binary": str(binary), "source_sha256": long_center.SOURCE_SHA256,
                      "local_header_sha256": hashlib.sha256(long_center.patched_source().encode()).hexdigest(),
                      "sanitize": args.sanitize}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
