#!/usr/bin/env python3
"""Resource wrapper for the exact all-G saturated-exterior language pilot."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import resource
import shlex
import subprocess
import time


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("--layers", type=int, default=80)
    parser.add_argument("--states", type=int, default=500000)
    parser.add_argument("--edges", type=int, default=5000000)
    parser.add_argument("--ops", type=int, default=100000000)
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--memory-gib", type=int, default=2)
    parser.add_argument("--fixed-blocks", type=int)
    parser.add_argument("--stop-at-known", action="store_true")
    parser.add_argument("--witness", action="store_true")
    parser.add_argument("--no-prune", action="store_true")
    parser.add_argument("--backward", action="store_true")
    parser.add_argument("--residue-seed", action="store_true")
    args = parser.parse_args()
    if not (0 < args.seconds <= 1800 and 1 <= args.memory_gib <= 8):
        parser.error("each run must use <=1800 seconds and <=8 GiB")
    if min(args.layers, args.states, args.edges, args.ops) < 1:
        parser.error("all computational limits must be positive")
    command = [str(args.binary.resolve()), "--layers", str(args.layers),
               "--states", str(args.states), "--edges", str(args.edges), "--ops", str(args.ops)]
    if args.fixed_blocks is not None:
        command.extend(["--fixed-blocks", str(args.fixed_blocks)])
    for name in ("stop_at_known", "witness", "no_prune", "backward", "residue_seed"):
        if getattr(args, name):
            command.append("--" + name.replace("_", "-"))

    def limits() -> None:
        memory = args.memory_gib * 1024**3
        resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
        cpu = int(args.seconds) + 2
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))

    result = {"command": shlex.join(command), "status": "UNDECIDED",
              "wall_limit_seconds": args.seconds, "address_space_gib": args.memory_gib}
    start = time.monotonic()
    try:
        run = subprocess.run(command, text=True, capture_output=True, timeout=args.seconds,
                             preexec_fn=limits, check=False)
    except subprocess.TimeoutExpired as error:
        def decode(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        result.update(returncode=None, reason="WALL_TIMEOUT", stdout=decode(error.stdout),
                      stderr=decode(error.stderr))
    else:
        result.update(returncode=run.returncode, stdout=run.stdout, stderr=run.stderr)
        markers = [line for line in run.stdout.splitlines() if line.startswith("BREG_DONE ")]
        if run.returncode == 0 and len(markers) == 1 and "UNDECIDED" not in run.stdout + run.stderr:
            fields = dict(re.findall(r"(\w+)=([^ ]+)", markers[0]))
            result["done"] = fields
            def integer(name, default=-1):
                try:
                    return int(fields.get(name, str(default)))
                except ValueError:
                    return -1
            wanted_scope = "fixed_G_control" if args.fixed_blocks else "all_G_all_widths"
            wanted_mode = "backward" if args.backward else "forward"
            complete = fields.get("scope") == wanted_scope and fields.get("mode") == wanted_mode
            complete &= fields.get("residue_seed", "0") == str(int(args.residue_seed))
            status = fields.get("status")
            if status in {"known_drivers_only", "no_exterior"}:
                if wanted_mode == "forward":
                    complete &= (integer("cycle_start") >= 1 and integer("period") >= 1
                                 and integer("terminal_checks") == integer("cycle_start") + integer("period") + 1
                                 and integer("known_seen") == int(status == "known_drivers_only"))
                else:
                    complete &= (status == "known_drivers_only" and integer("fixed_at") >= 0
                                 and integer("final_index") == integer("fixed_at") + 1
                                 and integer("first_intersection_empty") == 1
                                 and integer("terminal_seed_excludes_known") == 1)
            elif status in {"new_driver", "known_driver_control"}:
                complete &= integer("width") >= 1 and integer("blocks") >= 1
                if args.fixed_blocks:
                    complete &= integer("blocks") == args.fixed_blocks
                if status == "known_driver_control":
                    complete &= args.fixed_blocks is not None and args.stop_at_known and not args.backward
                needs_witness = status == "new_driver" or args.witness
                if needs_witness:
                    witnesses = [dict(re.findall(r"(\w+)=([^ ]+)", line))
                                 for line in run.stdout.splitlines() if line.startswith("BREG_WITNESS ")]
                    complete &= (fields.get("verified") == "1" and len(witnesses) == 1
                                 and witnesses[0].get("verified") == "1"
                                 and witnesses[0].get("width") == fields.get("width")
                                 and witnesses[0].get("blocks") == fields.get("blocks"))
            else:
                complete = False
            if complete:
                prefix = "CONTROL_" if args.fixed_blocks else ""
                result.update(status=prefix + status.upper(), reason="COMPLETE_EXACT_LANGUAGE_RESULT")
            else:
                result["reason"] = "MISSING_COMPLETE_SCOPED_OBLIGATIONS"
        else:
            result["reason"] = "INCOMPLETE_OR_UNSUPPORTED"
    result["wall_seconds"] = round(time.monotonic() - start, 6)
    result["peak_child_rss_kib"] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    print(json.dumps(result, sort_keys=True))
    return 2 if result["status"] == "UNDECIDED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
