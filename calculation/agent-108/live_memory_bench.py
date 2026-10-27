#!/usr/bin/env python3
"""Measure one exterior-engine process with explicit computation budgets.

Compile separately before starting this script: child peak RSS must exclude
the compiler. This prints mathematical outcomes and metrics, writes no log,
and never turns an interrupted/capped execution into a negative result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("g")
    parser.add_argument("--e")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--collect-every", type=int, default=1)
    parser.add_argument("--witness", action="store_true")
    parser.add_argument("--nodes", type=int, default=1500000)
    parser.add_argument("--operations", type=int, default=300000000)
    parser.add_argument("--depth", type=int, default=1000)
    parser.add_argument("--seconds", type=int, default=120)
    parser.add_argument("--gib", type=int, default=4)
    args = parser.parse_args()
    if not (1 <= args.seconds <= 1700 and 1 <= args.gib <= 8
            and args.nodes >= 2 and args.operations >= 1
            and 0 <= args.depth <= 1000000
            and 1 <= args.collect_every <= 1000000):
        parser.error("invalid resource/cadence limit")
    binary = args.binary.resolve(strict=True)
    command = [str(binary), args.g, str(args.nodes), str(args.operations),
               str(args.depth), str(args.seconds)]
    if args.e is not None:
        command += ["--e", args.e]
    if args.live:
        command += ["--live", "--collect-every", str(args.collect_every)]
    if args.witness:
        command.append("--witness")

    def limits():
        resource.setrlimit(resource.RLIMIT_AS, (args.gib * 1024**3,) * 2)
        resource.setrlimit(resource.RLIMIT_CPU, (args.seconds + 5, args.seconds + 6))

    began = time.monotonic()
    try:
        process = subprocess.run(command, capture_output=True, text=True,
                                 timeout=args.seconds + 10, preexec_fn=limits)
    except subprocess.TimeoutExpired:
        print(json.dumps({"status": "UNDECIDED", "reason": "external_wall_cap",
                          "wall_seconds": time.monotonic() - began}))
        return 3
    wall = time.monotonic() - began
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    records = [json.loads(line) for line in process.stdout.splitlines()]
    layers = [r for r in records if r.get("type") == "LAYER"]
    finals = [r for r in records if r.get("type") == "RESULT"]
    final = finals[-1] if len(finals) == 1 and process.returncode >= 0 else {
        "status": "UNDECIDED", "reason": "missing_complete_result"}
    counts = [(r["depth"], int(r["states"]), int(r["accepts"])) for r in layers]
    result = {
        "command": command,
        "binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
        "exit": process.returncode,
        "wall_seconds": wall,
        "cpu_seconds": usage.ru_utime + usage.ru_stime,
        "peak_rss_KiB": usage.ru_maxrss,
        "address_space_GiB": args.gib,
        "complete_layers": len(layers),
        "complete_layer_state_occurrences": sum(row[1] for row in counts),
        "layer_counts": counts,
        "witness_records": sum(r.get("type") == "WITNESS" for r in records),
        "result": final,
        "stderr": process.stderr,
    }
    print(json.dumps(result, sort_keys=True))
    return 3 if final["status"] == "UNDECIDED" else process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
