#!/usr/bin/env python3
"""Resource-bounded all-length experiment using exact segment decision DAGs."""
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
    parser.add_argument("--base", type=int, default=10)
    parser.add_argument("--e", default="101010010101" * 4)
    parser.add_argument("--g", default="100010001000" * 4)
    parser.add_argument("--v", default="00001000" * 6)
    parser.add_argument("--nodes", type=int, default=1_000_000)
    parser.add_argument("--ops", type=int, default=20_000_000)
    parser.add_argument("--layers", type=int, default=120)
    parser.add_argument("--seconds", type=float, default=120)
    parser.add_argument("--memory-gib", type=int, default=4)
    parser.add_argument("--witness", action="store_true")
    args = parser.parse_args()
    if not (0 < args.seconds <= 1800 and 1 <= args.memory_gib <= 8):
        parser.error("resource limits must be <=1800 seconds and <=8 GiB")
    cmd = [str(args.binary.resolve()), str(args.base), args.e, args.g, "1", "1",
           "-v", args.v, "-allm", "-nodes", str(args.nodes), "-ops", str(args.ops),
           "-layers", str(args.layers)]
    if args.witness:
        cmd.append("-w")

    def limits():
        size = args.memory_gib * 1024**3
        resource.setrlimit(resource.RLIMIT_AS, (size, size))
        cpu = int(args.seconds) + 2
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))

    start = time.monotonic()
    result = {"command": shlex.join(cmd), "wall_limit_seconds": args.seconds,
              "address_space_gib": args.memory_gib, "status": "UNDECIDED"}
    try:
        run = subprocess.run(cmd, capture_output=True, text=True, timeout=args.seconds,
                             preexec_fn=limits, check=False)
    except subprocess.TimeoutExpired as error:
        def decode(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        result.update(returncode=None, reason="WALL_TIMEOUT", stdout=decode(error.stdout),
                      stderr=decode(error.stderr))
    else:
        result.update(returncode=run.returncode, stdout=run.stdout, stderr=run.stderr)
        markers = [line for line in run.stdout.splitlines() if line.startswith("MDD_DONE ")]
        if run.returncode == 0 and len(markers) == 1 and "UNDECIDED" not in run.stdout + run.stderr:
            fields = dict(re.findall(r"(\w+)=([^ ]+)", markers[0]))
            result["done"] = fields
            period = int(fields.get("period", "0"))
            classes = int(fields.get("classes", "0"))
            mlo = int(fields.get("mlo", "0"))
            if (fields.get("scope") == "allm" and fields.get("status") == "none"
                    and fields.get("hits") == "0" and period > 0 and classes == 2 * period
                    and mlo > 2 * len(args.e) and not re.search(r"^FEASIBLE", run.stdout, re.M)):
                result.update(status="NONE", reason="COMPLETE_ALL_LENGTH_DECISION")
            elif fields.get("scope") == "allm" and fields.get("status") == "hit":
                result.update(status="FEASIBLE", reason="INDEPENDENT_WITNESS_REPLAY_REQUIRED")
            else:
                result["reason"] = "MISSING_COMPLETE_ALL_LENGTH_RESULT"
        else:
            result["reason"] = "INCOMPLETE_OR_UNSUPPORTED"
    result["wall_seconds"] = round(time.monotonic() - start, 6)
    result["peak_child_rss_kib"] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] in {"NONE", "FEASIBLE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
