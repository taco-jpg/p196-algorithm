#!/usr/bin/env python3
"""One bounded all-length attempt for the documented p11 driver repeated thrice.

The parent engine remains exact but may be undecided at a state or resource cap.
No output of this harness is a full B/C certificate or a Lean theorem.
"""
from __future__ import annotations

import argparse
import json
import sys

from long_center import run
from schedule_optimizer import optimize


E = "10100110011" * 3
G = "11100010000" * 3


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary")
    parser.add_argument("--schedule", choices=("balanced", "first-six", "last-six", "min-first"),
                        default="min-first")
    parser.add_argument("--cap", type=int, default=4_000_000)
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("--memory-mb", type=int, default=4096)
    args = parser.parse_args()
    patterns = {"balanced": "01000010000" * 3,
                "first-six": "1" * 6 + "0" * 27,
                "last-six": "0" * 27 + "1" * 6}
    if args.schedule == "min-first":
        selected = optimize(E, G, 10)
        trim = selected["pattern"]
        print(json.dumps({"selection": selected}, sort_keys=True), flush=True)
    else:
        trim = patterns[args.schedule]
    result = run(args.binary, 10, E, G, 1, 1, trim, all_lengths=True,
                 cap=args.cap, timeout=args.timeout, memory_mb=args.memory_mb, sizes=True)
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    if result.returncode:
        print(f"STATUS=UNDECIDED process_returncode={result.returncode}")
        return 2
    done = [line for line in result.stdout.splitlines() if line.startswith("DONE ")]
    if len(done) != 1:
        raise RuntimeError("missing or ambiguous engine completion record")
    fields = dict(part.split("=", 1) for part in done[0].split() if "=" in part)
    status = fields.get("status")
    if status == "none":
        print("STATUS=NO_CENTER_FOR_THIS_DRIVER_AND_SCHEDULE")
        return 0
    if status == "hit":
        print("STATUS=CENTER_FEASIBLE_RECONSTRUCT_AND_REPLAY_REQUIRED")
        return 0
    print(f"STATUS=UNDECIDED engine_status={status}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
