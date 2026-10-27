#!/usr/bin/env python3
"""Build the exact regular-language center engine with pinned local arithmetic.

The temporary upstream header comes from long_center.patched_source(). The
binary keeps the positional base/e/g/width CLI, but each width quantifies over
all positive repetitions of the supplied temporal unit. At least one trim is
required. Extra flags: -generic-only, -layers N, -edge-cap N, -work-cap N,
-export-layer N, -export-k N, -export-limit N. -cap bounds automaton states.
Use long_center.run() or its bounded subprocess helper for resource limits.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import resource
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
    with tempfile.TemporaryDirectory(prefix="agent111-regular-") as temp:
        header = Path(temp) / "a111_existing.hpp"
        header.write_text(long_center.patched_source(), encoding="utf-8")
        subprocess.run([compiler, *flags, "-I", temp, str(directory / "regular_center.cpp"),
                        "-o", str(output)], check=True, timeout=180)
    return output


def run(binary: str | Path, base: int, e: str, g: str, mlo: int, mhi: int, trim: str,
        *, all_lengths: bool = False, generic_only: bool = False,
        cap: int = 200000, edge_cap: int = 2000000, work_cap: int = 50000000,
        layers: int = 120, timeout: float = 30, memory_mb: int | None = 6144,
        witness: bool = False, sizes: bool = False,
        export_layer: int | None = None, export_k: int = 1,
        export_limit: int = 1000000) -> subprocess.CompletedProcess[str]:
    """Bounded all-repetition query; incomplete results never imply absence.

    memory_mb=None is only for small sanitizer controls, because ASan reserves
    a large virtual address range. Ordinary searches retain the address cap.
    """
    shape = long_center.validate(base, e, g, mlo, mhi, trim, cap)
    if not shape["trims"]:
        raise ValueError("regular local arithmetic requires at least one trim")
    if any(type(n) is not int or not 1 <= n < 2**63
           for n in (edge_cap, work_cap, layers, export_k, export_limit)):
        raise ValueError("regular limits must be positive signed-64-bit integers")
    if layers > 10000 or export_k > 10000:
        raise ValueError("layers and export_k must not exceed 10000")
    if export_layer is not None and (type(export_layer) is not int
            or not 0 <= export_layer <= 10000 or not (all_lengths or generic_only)):
        raise ValueError("export_layer requires generic mode and a layer in 0..10000")
    if not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or not 0 < timeout <= 1800:
        raise ValueError("wall timeout must be in (0,1800] seconds")
    if memory_mb is not None and (type(memory_mb) is not int or not 64 <= memory_mb <= 8192):
        raise ValueError("memory_mb must be in 64..8192, or None for sanitizer controls")
    command = [str(Path(binary).resolve()), str(base), e, g, str(mlo), str(mhi),
               "-v", trim, "-cap", str(cap), "-edge-cap", str(edge_cap),
               "-work-cap", str(work_cap), "-layers", str(layers)]
    command += [flag for enabled, flag in ((all_lengths, "-allm"),
               (generic_only, "-generic-only"), (witness, "-w"), (sizes, "-sz")) if enabled]
    if export_layer is not None:
        command += ["-export-layer", str(export_layer), "-export-k", str(export_k),
                    "-export-limit", str(export_limit)]

    def bounds() -> None:
        if memory_mb is not None:
            resource.setrlimit(resource.RLIMIT_AS, (memory_mb * 1024**2,) * 2)
        resource.setrlimit(resource.RLIMIT_CPU, (math.ceil(timeout) + 1, math.ceil(timeout) + 2))

    try:
        return subprocess.run(command, text=True, capture_output=True, timeout=timeout,
                              preexec_fn=bounds, check=False)
    except subprocess.TimeoutExpired as error:
        def text(value: str | bytes | None) -> str:
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        return subprocess.CompletedProcess(command, 124, text(error.stdout),
                                           text(error.stderr) + "\nUNDECIDED: wall timeout\n")


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
