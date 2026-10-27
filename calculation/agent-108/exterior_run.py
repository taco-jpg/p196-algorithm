#!/usr/bin/env python3
"""Guarded build/run entry point for the nonuniform decimal exterior MDD.

python3 calculation/agent-108/exterior_run.py selftest
python3 calculation/agent-108/exterior_run.py run 110001001000110001001000
python3 calculation/agent-108/exterior_run.py run 110001001000110001001000 --e 010100110100101011001011 --witness
python3 calculation/agent-108/exterior_run.py run 110001001000110001001000 --live
python3 calculation/agent-108/exterior_run.py live-selftest

FEASIBLE is an exterior-only existence result and stops at the first matching
terminal. A candidate full certificate additionally requires a compatible
center, mirror cycleOK, and the separate registered Lean gate.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from saturation_run import limited

HERE = Path(__file__).resolve().parent
TARGET_G = "110001001000110001001000"
TARGET_E = "010100110100101011001011"


def build(output: Path) -> None:
    subprocess.run([os.environ.get("CXX", "c++"), "-O2", "-std=c++17",
                    str(HERE / "exterior_mdd.cpp"), "-o", str(output)], check=True)


def selftest(binary: Path) -> None:
    py = [sys.executable] + (["-O"] if sys.flags.optimize else [])
    for command in [
        py + [str(HERE / "count_checks.py")],
        py + [str(HERE / "exterior_tiles.py"), "--mdd", str(binary)],
        py + [str(HERE / "exterior_controls.py"), "engine", "--binary", str(binary)],
    ]:
        subprocess.run(command, check=True, timeout=300)
    for reason, limits in [
        ("node_cap", ["20", "100000000", "100", "10"]),
        ("operation_cap", ["1000000", "1000", "100", "10"]),
        ("depth_cap", ["1000000", "100000000", "1", "10"]),
    ]:
        process = subprocess.run([str(binary), TARGET_G, *limits],
                                 text=True, capture_output=True, timeout=15)
        records = [json.loads(line) for line in process.stdout.splitlines()]
        if process.returncode != 3 or records[-1].get("status") != "UNDECIDED" or records[-1].get("reason") != reason:
            raise RuntimeError(("Wrong incomplete-result status", reason, records))
    print("RESOURCE_GUARDS node/operation/depth remain UNDECIDED PASS", flush=True)
    # This is a capacity/control check only, not a decision on the held P48
    # repeated-center completion problem. It deliberately stops at width 2.
    code, records = limited([str(binary), TARGET_G * 2, "1000000", "100000000", "2", "30",
                             "--e", TARGET_E * 2], 30, 4)
    result = next((r for r in records if r.get("type") == "RESULT"), {})
    if code != 3 or result.get("reason") != "depth_cap" or result.get("period") != 48:
        raise RuntimeError(("P48 support control failed", records))
    print("P48_CAPACITY_CONTROL supported=True final=UNDECIDED/depth_cap PASS", flush=True)
    expected = [1,64,256,1088,16752,44368,249216,202564,276380,286144,
                220196,187392,151668,256644,245568,244208,369040,444672,
                535936,433352,422000,573536,599296,339168,177672,295192,
                339000,235128,136016,261224,306616,208224,214768,166208,
                40592,48288,31232,13248,2560,0]
    for target_e in (None, TARGET_E):
        command = [str(binary), TARGET_G, "1500000", "300000000", "1000", "120"]
        if target_e:
            command += ["--e", target_e]
        code, records = limited(command, 120, 4)
        layers = [r for r in records if r.get("type") == "LAYER"]
        final = next((r for r in records if r.get("type") == "RESULT"), {})
        status = "EXHAUSTED_NO_B_FOR_E" if target_e else "EXHAUSTED_NO_B"
        if (code or final.get("status") != status or final.get("reason") != "empty_layer"
                or [int(r["states"]) for r in layers] != expected
                or any(int(r["accepts"]) for r in layers)):
            raise RuntimeError(("SQ5 reproduction failed", target_e, records))
    print("SQ5_REPRODUCTION all_e_and_fixed_e layers=40 empty_width=39 PASS", flush=True)
    print("ALL NONUNIFORM EXTERIOR CHECKS PASSED", flush=True)


def live_selftest(binary: Path, directory: Path) -> None:
    py = [sys.executable] + (["-O"] if sys.flags.optimize else [])
    subprocess.run(py + [str(HERE / "live_invariants.py")], check=True, timeout=120)
    structural = directory / "live_gc_structure"
    subprocess.run([os.environ.get("CXX", "c++"), "-O2", "-std=c++17",
                    str(HERE / "live_gc_structure.cpp"), "-o", str(structural)], check=True)
    subprocess.run([str(structural)], check=True, timeout=120)
    # The historical evaluator is still present. The separately authored tuple
    # oracle adds an independent arithmetic/set reference for all small cases.
    for suite in ("full", "sq5"):
        subprocess.run(py + [str(HERE / "live_memory_checks.py"),
                            "--reference", str(binary), "--candidate", str(binary),
                            "--suite", suite], check=True, timeout=600)
    print("ALL LIVE MEMORY CHECKS PASSED", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("run", "selftest", "live-selftest"))
    parser.add_argument("g", nargs="?")
    parser.add_argument("--e")
    parser.add_argument("--nodes", type=int, default=1500000)
    parser.add_argument("--operations", type=int, default=300000000)
    parser.add_argument("--depth", type=int, default=1000)
    parser.add_argument("--seconds", type=int, default=120)
    parser.add_argument("--gib", type=int, default=4)
    parser.add_argument("--witness", action="store_true")
    parser.add_argument("--live", action="store_true",
                        help="collect dead nodes and use bounded-root exact recurrence/replay")
    parser.add_argument("--collect-every", type=int, default=None,
                        help="completed-image collection cadence (requires --live; default 1)")
    args = parser.parse_args()
    if (not 1 <= args.seconds <= 1700 or not 1 <= args.gib <= 8
            or args.nodes < 2 or args.operations < 1 or args.depth < 0):
        parser.error("invalid resource limits")
    if args.mode == "run" and args.g is None:
        parser.error("run requires an overflow word")
    if args.collect_every is not None and (not args.live or not 1 <= args.collect_every <= 1000000):
        parser.error("--collect-every requires --live and a positive cadence <=1000000")
    with tempfile.TemporaryDirectory(prefix="p196-agent108-exterior-") as temp:
        binary = Path(temp) / "exterior_mdd"
        build(binary)
        if args.mode == "selftest":
            selftest(binary)
            return 0
        if args.mode == "live-selftest":
            live_selftest(binary, Path(temp))
            return 0
        command = [str(binary), args.g, str(args.nodes), str(args.operations),
                   str(args.depth), str(args.seconds)]
        if args.e is not None:
            command += ["--e", args.e]
        if args.witness:
            command.append("--witness")
        if args.live:
            command.append("--live")
        if args.collect_every is not None:
            command += ["--collect-every", str(args.collect_every)]
        code, records = limited(command, args.seconds, args.gib)
        for record in records:
            print(json.dumps(record, sort_keys=True))
        return code


if __name__ == "__main__":
    raise SystemExit(main())
