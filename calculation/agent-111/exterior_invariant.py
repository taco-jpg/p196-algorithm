#!/usr/bin/env python3
"""Build/run the independent exterior-invariant finite-product verifier.

No arithmetic row tables are accepted from the input. The C++ front end
derives them from b/e/g, then checks FIRST inclusion, generic closure and
terminal disjointness directly, without determinization or minimization.
With -backward it checks terminal inclusion, generic predecessor closure,
and disjointness from the physical FIRST image, with unchanged coefficient
ports when transposing the arithmetic symbol relation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import resource
import subprocess


def build(output: str | Path, sanitize: bool = False, compiler: str = "c++") -> Path:
    directory = Path(__file__).resolve().parent
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    flags = ["-std=c++17", "-O2", "-Wall", "-Wextra"]
    if sanitize:
        flags = ["-std=c++17", "-O1", "-g", "-fsanitize=address,undefined",
                 "-fno-omit-frame-pointer", "-fno-pie", "-no-pie", "-Wall", "-Wextra"]
    subprocess.run([compiler, *flags, str(directory / "exterior_invariant.cpp"),
                    "-o", str(output)], check=True, timeout=180)
    return output


def run(binary: str | Path, input_path: str | Path, *, timeout: float = 30,
        memory_mb: int | None = 4096, state_cap: int = 1000000,
        edge_cap: int = 10000000, work_cap: int = 100000000,
        backward: bool = False) -> subprocess.CompletedProcess[str]:
    """Run a supplied candidate; timeout/error/resource cap is UNDECIDED.

    Exit0=valid,1=rejected invariant,2=invalid/unsupported input,3=resource
    interruption,4=internal error,124=wall timeout. None are B-cycle claims.
    memory_mb=None is reserved for small ASan controls.
    backward=True selects the three dual obligations described above.
    """
    for name, value in (("state_cap", state_cap), ("edge_cap", edge_cap), ("work_cap", work_cap)):
        if type(value) is not int or not 1 <= value < 2**64:
            raise ValueError(f"{name} must be a positive uint64 integer")
    if state_cap >= 2**32 - 1:
        raise ValueError("state_cap exceeds the state identifier domain")
    if type(backward) is not bool:
        raise ValueError("backward must be a bool")
    if not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or not 0 < timeout <= 1800:
        raise ValueError("timeout must be in (0,1800] seconds")
    if memory_mb is not None and (type(memory_mb) is not int or not 64 <= memory_mb <= 8192):
        raise ValueError("memory_mb must be in64..8192 or None for sanitizer controls")
    path = Path(input_path).resolve()
    if not path.is_file():
        raise ValueError("input_path must name an existing invariant file")
    command = [str(Path(binary).resolve()), str(path), "-states-cap", str(state_cap),
               "-edges-cap", str(edge_cap), "-work-cap", str(work_cap)]
    if backward:
        command.append("-backward")

    def bounds() -> None:
        if memory_mb is not None:
            resource.setrlimit(resource.RLIMIT_AS, (memory_mb * 1024**2,) * 2)
        resource.setrlimit(resource.RLIMIT_CPU, (math.ceil(timeout) + 1, math.ceil(timeout) + 2))

    try:
        return subprocess.run(command, text=True, capture_output=True, timeout=timeout,
                              preexec_fn=bounds, check=False)
    except subprocess.TimeoutExpired as error:
        def decoded(value: str | bytes | None) -> str:
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        return subprocess.CompletedProcess(command, 124, decoded(error.stdout),
                                           decoded(error.stderr) + "\nUNDECIDED: wall timeout direction="
                                           + ("backward" if backward else "forward") + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build"])
    parser.add_argument("output", type=Path)
    parser.add_argument("--sanitize", action="store_true")
    parser.add_argument("--compiler", default="c++")
    args = parser.parse_args()
    binary = build(args.output, args.sanitize, args.compiler)
    directory = Path(__file__).resolve().parent
    hashes = {name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
              for name in ("exterior_invariant.hpp", "exterior_invariant.cpp")}
    print(json.dumps({"binary": str(binary), "sanitize": args.sanitize,
                      "source_sha256": hashes}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
