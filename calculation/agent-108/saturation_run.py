#!/usr/bin/env python3
"""Build/run the scoped saturation experiment with explicit process limits.

Examples (repository root):
  python3 calculation/agent-108/saturation_run.py mdd 8
  python3 calculation/agent-108/saturation_run.py quotient 8 --states 5000000 --seconds 120
  python3 calculation/agent-108/saturation_run.py scalar 8 --states 25000000 --seconds 240
  python3 calculation/agent-108/saturation_run.py selftest

All runs are single process. Default address-space budget is 4 GiB; wall and
native budgets are at most 1710/1700 seconds. External resource termination,
missing terminal records, and explicit native caps remain UNDECIDED.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent


def build(engine: str, output: Path, sanitize: bool = False) -> None:
    source = HERE / ("saturation_mdd.cpp" if engine == "mdd" else "saturation_g8.cpp")
    flags = ["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"] if sanitize else ["-O2"]
    subprocess.run([os.environ.get("CXX", "c++"), *flags, "-std=c++17", str(source), "-o", str(output)], check=True)


def limited(command: list[str], seconds: int, gib: int) -> tuple[int, list[dict]]:
    def limits() -> None:
        resource.setrlimit(resource.RLIMIT_AS, (gib * 1024**3, gib * 1024**3))
        resource.setrlimit(resource.RLIMIT_CPU, (seconds + 5, seconds + 6))

    start = time.monotonic()
    try:
        process = subprocess.run(command, text=True, capture_output=True,
                                 timeout=seconds + 10, preexec_fn=limits)
    except subprocess.TimeoutExpired:
        return 3, [{"type": "PROCESS", "status": "UNDECIDED", "reason": "external_wall_cap",
                    "seconds": time.monotonic() - start}]
    records = []
    for line in process.stdout.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError as error:
            raise RuntimeError("Native program emitted malformed JSON") from error
        if not isinstance(item, dict):
            raise RuntimeError("Expected native JSON record")
        records.append(item)
    if process.stderr:
        print(process.stderr, file=sys.stderr, end="")
    complete = [r for r in records if r.get("type") == "RESULT"]
    code = process.returncode
    if code < 0 or not complete:
        records.append({"type": "PROCESS", "status": "UNDECIDED", "reason": "no_terminal_result",
                        "native_exit": code})
        code = 3
    records.append({"type": "PROCESS_METRICS", "wall_seconds": time.monotonic() - start,
                    "address_space_limit_GiB": gib, "native_exit": process.returncode})
    return code, records


def guards(binary: Path) -> None:
    malformed = [[], ["0", "100", "100", "20", "10"], ["11", "100", "100", "20", "10"],
                 ["8", "1", "100", "20", "10"], ["8", "100", "0", "20", "10"],
                 ["8", "100", "100", "20", "0"], ["8", "100", "100", "20", "1701"],
                 ["-8", "100", "100", "20", "10"], ["8x", "100", "100", "20", "10"],
                 ["8", "100", "100", "20", "10", "--unknown"],
                 ["8", "100", "100", "20", "10", "--export-layer"],
                 ["8", "184467440737095516160", "100", "20", "10"]]
    for args in malformed:
        result = subprocess.run([str(binary), *args], text=True, capture_output=True, timeout=10)
        if result.returncode != 2 or "EXHAUSTED_NO_B" in result.stdout:
            raise RuntimeError(("Malformed input was not rejected", args, result.stdout, result.stderr))
    cases = [("node_cap", ["8", "20", "100000000", "100", "10"]),
             ("operation_cap", ["8", "1000000", "1000", "100", "10"]),
             ("depth_cap", ["8", "1000000", "100000000", "2", "10"])]
    for reason, args in cases:
        result = subprocess.run([str(binary), *args], text=True, capture_output=True, timeout=15)
        records = [json.loads(line) for line in result.stdout.splitlines()]
        if result.returncode != 3 or not records or records[-1].get("status") != "UNDECIDED" or records[-1].get("reason") != reason:
            raise RuntimeError(("Bad resource-cap status", reason, result.stdout, result.stderr))
    # Finite-set input is validated before any requested image is accepted.
    for data in ("-1\n", "1 2560\n", "2 272\n", "1 272 extra\n"):
        result = subprocess.run([str(binary), "--image", "1", "0"], input=data,
                                text=True, capture_output=True, timeout=10)
        if result.returncode != 2:
            raise RuntimeError(("Malformed finite set accepted", data))
    print("MDD_GUARDS malformed=16 resource_caps=3 PASS", flush=True)


def selftest(directory: Path) -> None:
    mdd, scalar = directory / "mdd", directory / "scalar"
    build("mdd", mdd)
    build("scalar", scalar)
    guards(mdd)
    # Preserve an acceptance already inserted in a capped partial next layer.
    # The parent layer is 52, while this known p12 witness has width 53.
    partial = subprocess.run([str(scalar), "3", "97000", "400", "30", "--witness"],
                             text=True, capture_output=True, timeout=35)
    partial_result = json.loads(partial.stdout.splitlines()[-1])
    if (partial.returncode != 3 or partial_result["status"] != "UNDECIDED"
            or partial_result["reason"] != "state_cap" or partial_result["depth"] != 52
            or not partial_result["witnesses"]):
        raise RuntimeError("Capped partial layer lost a reached positive witness")
    from saturation_oracle import mirror_check_witness
    for found in partial_result["witnesses"]:
        if found["depth"] != 53:
            raise RuntimeError("Wrong partial-layer witness width")
        mirror_check_witness(10, "1000" * 3, tuple(map(int, found["e"])), found["B_t"])
    print("SCALAR_PARTIAL_LAYER cap=97000 parent_depth=52 witness_depth=53 PASS", flush=True)
    commands = [
        [sys.executable, str(HERE / "saturation_tiles.py"), "--mdd", str(mdd)],
        [sys.executable, str(HERE / "saturation_oracle.py"), "selftest"],
        [sys.executable, str(HERE / "saturation_oracle.py"), "differential", "--binary", str(scalar)],
        [sys.executable, str(HERE / "saturation_oracle.py"), "mdd-differential", "--binary", str(mdd)],
    ]
    for command in commands:
        subprocess.run(command, check=True, timeout=300)
    code, records = limited([str(mdd), "8", "1000000", "200000000", "400", "60"], 60, 4)
    final = next((r for r in records if r.get("type") == "RESULT"), {})
    counts = [int(r["states"]) for r in records if r.get("type") == "LAYER"]
    expected = [1, 256, 65536, 1766720, 13060352, 2930273, 9280, 27904,
                2105280, 1986368, 414240, 146720, 32, 0]
    if code or final.get("status") != "EXHAUSTED_NO_B" or counts != expected:
        raise RuntimeError(("P32 experiment did not reproduce", records))
    print("SATURATION_G8_REPRODUCTION layers=14 terminal_accepts=0 PASS", flush=True)
    print("ALL SATURATION CHECKS PASSED", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("mdd", "scalar", "quotient", "selftest"))
    parser.add_argument("G", type=int, nargs="?")
    parser.add_argument("--states", type=int, default=1000000)
    parser.add_argument("--nodes", type=int, default=1000000)
    parser.add_argument("--operations", type=int, default=200000000)
    parser.add_argument("--depth", type=int, default=400)
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--gib", type=int, default=4)
    parser.add_argument("--witness", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.seconds <= 1700 or not 1 <= args.gib <= 8 or args.states < 1 or args.nodes < 2 or args.operations < 1 or args.depth < 0:
        parser.error("invalid resource limits")
    if args.mode != "selftest" and (args.G is None or not 1 <= args.G <= 10):
        parser.error("G must be 1..10")
    with tempfile.TemporaryDirectory(prefix="p196-agent108-saturation-") as temp:
        directory = Path(temp)
        if args.mode == "selftest":
            selftest(directory)
            return 0
        binary = directory / "search"
        build(args.mode, binary)
        if args.mode == "mdd":
            command = [str(binary), str(args.G), str(args.nodes), str(args.operations), str(args.depth), str(args.seconds)]
        else:
            command = [str(binary), str(args.G), str(args.states), str(args.depth), str(args.seconds), "--layers"]
            if args.mode == "quotient":
                command.append("--quotient")
        if args.witness:
            command.append("--witness")
        code, records = limited(command, args.seconds, args.gib)
        for record in records:
            print(json.dumps(record, sort_keys=True))
        return code


if __name__ == "__main__":
    raise SystemExit(main())
