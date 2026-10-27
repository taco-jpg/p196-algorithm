#!/usr/bin/env python3
"""Bounded, fail-closed runner for Agent 118's all-length center experiment."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import resource
import shlex
import subprocess
import time


def run_case(binary: Path, base: int, e: str, g: str, v: str,
             cap: int = 100_000, seconds: float = 120,
             memory_gib: int = 4, witness: bool = True) -> dict:
    if not (2 <= base <= 62 and len(e) == len(g) == len(v) > 0
            and set(e + g + v) <= {"0", "1"}
            and g.count("1") == 2 * v.count("1")):
        raise ValueError("invalid base, stream, or trim balance")
    if not (1 <= cap < 2**31 and 0 < seconds <= 1800 and 1 <= memory_gib <= 8):
        raise ValueError("resource budget outside the supported sandbox scope")
    cmd = [str(binary.resolve()), str(base), e, g, "1", "1", "-v", v,
           "-allm", "-sz", "-cap", str(cap)]
    if witness:
        cmd.append("-w")

    def limits():
        limit = memory_gib * 1024**3
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
        cpu = int(seconds) + 2
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))

    start = time.monotonic()
    result = {"base": base, "period": len(e), "e": e, "g": g, "v": v,
              "command": shlex.join(cmd), "state_cap": cap,
              "wall_cap_seconds": seconds, "address_space_gib": memory_gib}
    try:
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=seconds,
                              preexec_fn=limits, check=False)
    except subprocess.TimeoutExpired as error:
        def decode(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else (value or "")
        result.update(status="UNDECIDED", reason="WALL_TIMEOUT",
                      returncode=None, stdout=decode(error.stdout), stderr=decode(error.stderr))
    else:
        result.update(returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
        done = [line for line in proc.stdout.splitlines() if line.startswith("DONE ")]
        bad = re.search(r"(?:NOPERIOD|CAPPED|UNDECIDED)", proc.stdout + proc.stderr)
        if proc.returncode != 0 or bad or len(done) != 1:
            result.update(status="UNDECIDED", reason="INCOMPLETE_OR_UNSUPPORTED")
        else:
            fields = dict(re.findall(r"(\w+)=([^ ]+)", done[0]))
            result["done"] = fields
            if fields.get("status") == "none":
                period = int(fields.get("period", "0"))
                classes = int(fields.get("classes", "0"))
                mlo = int(fields.get("mlo", "0"))
                if (period > 0 and classes == 2 * period and mlo > 2 * len(e)
                        and not re.search(r"^FEASIBLE", proc.stdout, re.M)):
                    result.update(status="NONE", reason="COMPLETE_ALL_LENGTH_DECISION")
                else:
                    result.update(status="UNDECIDED", reason="MISSING_ALL_LENGTH_COVERAGE")
            elif fields.get("status") == "hit":
                result.update(status="FEASIBLE", reason="INDEPENDENT_WITNESS_REPLAY_REQUIRED")
            else:
                result.update(status="UNDECIDED", reason="NONTERMINAL_STATUS")
    result["wall_seconds"] = round(time.monotonic() - start, 6)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("--base", type=int, default=10)
    parser.add_argument("--e", default="101010010101" * 4)
    parser.add_argument("--g", default="100010001000" * 4)
    parser.add_argument("--v", default="00001000" * 6)
    parser.add_argument("--cap", type=int, default=100_000)
    parser.add_argument("--seconds", type=float, default=120)
    parser.add_argument("--memory-gib", type=int, default=4)
    parser.add_argument("--no-witness", action="store_true")
    args = parser.parse_args()
    result = run_case(args.binary, args.base, args.e, args.g, args.v, args.cap,
                      args.seconds, args.memory_gib, not args.no_witness)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] in {"NONE", "FEASIBLE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
