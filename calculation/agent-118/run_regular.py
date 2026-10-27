#!/usr/bin/env python3
"""Bounded all-repetition regular-language experiment for the p12 driver."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import resource
import shlex
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("--layers", type=int, default=7)
    parser.add_argument("--states", type=int, default=200000)
    parser.add_argument("--edges", type=int, default=3000000)
    parser.add_argument("--ops", type=int, default=100000000)
    parser.add_argument("--seconds", type=float, default=120)
    parser.add_argument("--memory-gib", type=int, default=4)
    parser.add_argument("--compare", action="store_true")
    parser.add_argument("--no-prune", action="store_true")
    args = parser.parse_args()
    if not (0 < args.seconds <= 1800 and 1 <= args.memory_gib <= 8):
        parser.error("resource limits must be <=1800 seconds and <=8 GiB")
    if min(args.layers, args.states, args.edges, args.ops) < 1:
        parser.error("all computational limits must be positive")
    command = [str(args.binary.resolve()), "--layers", str(args.layers),
               "--states", str(args.states), "--edges", str(args.edges),
               "--ops", str(args.ops)]
    if args.compare:
        command.append("--compare")
    if args.no_prune:
        command.append("--no-prune")

    def limits():
        memory = args.memory_gib * 1024**3
        resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
        cpu = int(args.seconds) + 2
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))

    result = {"command": shlex.join(command), "status": "UNDECIDED",
              "wall_limit_seconds": args.seconds, "address_space_gib": args.memory_gib}
    start = time.monotonic()
    try:
        run = subprocess.run(command, text=True, capture_output=True,
                             preexec_fn=limits, timeout=args.seconds, check=False)
    except subprocess.TimeoutExpired as error:
        def decode(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        result.update(returncode=None, reason="WALL_TIMEOUT", stdout=decode(error.stdout),
                      stderr=decode(error.stderr))
    else:
        result.update(returncode=run.returncode, stdout=run.stdout, stderr=run.stderr)
        markers = [line for line in run.stdout.splitlines() if line.startswith("REG_DONE ")]
        if run.returncode == 0 and len(markers) == 1 and "UNDECIDED" not in run.stdout + run.stderr:
            fields = dict(re.findall(r"(\w+)=([^ ]+)", markers[0]))
            result["done"] = fields
            fixed_at = int(fields.get("fixed_at", "0"))
            tails = int(fields.get("tail_checks", "0"))
            if (fields.get("status") == "none"
                    and fields.get("scope") == "all_repetitions_all_widths"
                    and fixed_at >= 1 and tails == 2 * (fixed_at + 1)):
                result.update(status="NONE", reason="EXACT_UNIFORM_FIXEDPOINT_AND_EMPTY_TAILS")
            elif fields.get("status") == "potential_center":
                result.update(status="POTENTIAL_CENTER", reason="FULL_COEFFICIENT_WITNESS_REQUIRED")
            else:
                result["reason"] = "MISSING_COMPLETE_REGULAR_LANGUAGE_RESULT"
        else:
            result["reason"] = "INCOMPLETE_OR_UNSUPPORTED"
    result["wall_seconds"] = round(time.monotonic() - start, 6)
    result["peak_child_rss_kib"] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] in {"NONE", "POTENTIAL_CENTER"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
