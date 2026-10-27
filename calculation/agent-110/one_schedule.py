#!/usr/bin/env python3
"""One prescribed trim schedule suffices for an unrestricted-length C decision.

Agent 7: neutral-padding covariance. Agent 107: general schedule equivalence.
Agent 110: balanced two-width corollary, independent controls, guarded runner.
No assertion in this runner establishes a full B/C certificate or a Lean result.
"""
import argparse
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path


# The unchanged C++ solver parses widths as signed 32-bit int and evaluates
# m[t] + g[t] + 1 before dividing by two. Both profiles satisfy m[t] <= W.
MAX_PROFILE_WIDTH = (1 << 31) - 3


def bitstream(value):
    if not value or any(c not in "01" for c in value):
        raise ValueError("streams must be nonempty binary strings")
    return value


def schedule(g, mode="balanced"):
    bitstream(g)
    total = g.count("1")
    if total % 2:
        raise ValueError("odd total overflow cannot close a center; repeat the stream")
    if mode == "clustered":
        return "1" * (total // 2) + "0" * (len(g) - total // 2)
    if mode not in ("balanced", "balanced-opposite"):
        raise ValueError("unknown schedule mode")
    offset = int(mode == "balanced-opposite")
    prefix = 0
    result = []
    for digit in g:
        new = prefix + int(digit)
        result.append(str((new + offset) // 2 - (prefix + offset) // 2))
        prefix = new
    return "".join(result)


def length_offsets(g, v):
    result = [0]
    for gg, vv in zip(g, v):
        result.append(result[-1] + int(gg) - 2 * int(vv))
    return result


def classify(stdout, returncode, pattern, all_lengths=True):
    """Fail closed on interruption, contradictions, or incomplete allm output."""
    if returncode != 0:
        return "UNDECIDED", "solver exited unsuccessfully"
    rows = [dict(re.findall(r"([a-z_]+)=([^\s]+)", line))
            for line in stdout.splitlines() if line.startswith("DONE ")]
    if len(rows) != 1 or rows[0].get("v") != pattern:
        return "UNDECIDED", "missing or mismatched single-pattern completion"
    row = rows[0]
    if re.search(r"^(?:CAPPED|NOPERIOD)\b", stdout, re.M):
        return "UNDECIDED", "at least one frontier or length class was undecided"
    if row.get("status") == "none":
        if re.search(r"^FEASIBLE(?:_CLASS)?\b", stdout, re.M):
            return "UNDECIDED", "contradictory feasible and none output"
        if not all_lengths:
            return "NO_CENTER_AT_PROFILE", "complete none at the prescribed width profile"
        try:
            if int(row["period"]) < 1 or int(row["classes"]) < 1:
                raise ValueError("incomplete classes")
            if int(row["feasible_classes"]) != 0:
                raise ValueError("contradictory class counts")
        except (KeyError, ValueError):
            return "UNDECIDED", "missing valid eventual-length class coverage"
        return "NO_CENTER_ALL_LENGTHS", "complete allm none for one equivalent schedule"
    if row.get("status") == "hit":
        if not re.search(r"^FEASIBLE(?:_CLASS)?\b", stdout, re.M):
            return "UNDECIDED", "hit lacks a feasible length record"
        return "CENTER_FEASIBLE", "replay a full witness before any certificate claim"
    return "UNDECIDED", "solver reported an undecided or unknown status"


def selftest():
    expected = [
        ("11100010000", "01000010000"),
        ("11100010000" * 2, "0100001000001000010000"),
        ("100010001000" * 2, "000010000000100000001000"),
    ]
    for g, v in expected:
        if schedule(g) != v or set(length_offsets(g, v)) != {0, 1}:
            raise RuntimeError("balanced schedule regression")
    pattern = "10"
    none = "DONE idx=0 v=10 status=none jstar=3 period=1 classes=2 feasible_classes=0"
    cases = [
        (none, 0, "NO_CENTER_ALL_LENGTHS"),
        (none, 1, "UNDECIDED"),
        (none + "\nNOPERIOD b=10", 0, "UNDECIDED"),
        (none + "\nCAPPED b=10", 0, "UNDECIDED"),
        (none + "\nFEASIBLE b=10", 0, "UNDECIDED"),
        (none.replace("classes=2", "classes=0"), 0, "UNDECIDED"),
        (none.replace("period=1", "period=0"), 0, "UNDECIDED"),
        (none.replace("v=10", "v=01"), 0, "UNDECIDED"),
        (none + "\n" + none, 0, "UNDECIDED"),
        ("DONE v=10 status=none", 0, "UNDECIDED"),
        ("DONE v=10 status=capped", 0, "UNDECIDED"),
        ("DONE v=10 status=noperiod", 0, "UNDECIDED"),
        ("DONE v=10 status=hit", 0, "UNDECIDED"),
        ("FEASIBLE b=2\nDONE v=10 status=hit", 0, "CENTER_FEASIBLE"),
        ("", 0, "UNDECIDED"),
    ]
    for output, rc, expected_status in cases:
        actual = classify(output, rc, pattern)[0]
        if actual != expected_status:
            raise RuntimeError(f"classification regression: {actual} != {expected_status}")

    # Exercise the CLI boundary before any subprocess can run. In particular,
    # W=2**32 used to reach atoi as widths -1/0 and falsely report no center.
    from contextlib import redirect_stdout
    from io import StringIO
    from unittest.mock import patch

    command = [str(Path(__file__)), "/unused/cauto_fast", "--base", "2",
               "--e", "1010", "--g", "1010", "--width"]
    rejected_widths = (MAX_PROFILE_WIDTH + 1, (1 << 31) - 1,
                       1 << 31, 1 << 32, 1 << 63)
    for width in rejected_widths:
        output = StringIO()
        with patch.object(sys, "argv", command + [str(width)]), redirect_stdout(output), \
                patch.object(subprocess, "run", side_effect=RuntimeError("unsupported width launched")):
            rc = main()
        result = json.loads(output.getvalue().splitlines()[-1])
        if rc != 2 or result.get("status") != "UNDECIDED":
            raise RuntimeError("unsupported width was classified as a completed decision")
    # The largest supported bound reaches both exact profiles; simulate an
    # interrupted solver rather than allocating a billion-layer computation.
    output = StringIO()
    interrupted = subprocess.CompletedProcess([], 1, stdout="", stderr="")
    with patch.object(sys, "argv", command + [str(MAX_PROFILE_WIDTH)]), redirect_stdout(output), \
            patch.object(subprocess, "run", return_value=interrupted) as run:
        rc = main()
    widths = [call.args[0][4:6] for call in run.call_args_list]
    if rc != 2 or widths != [[str(MAX_PROFILE_WIDTH - 1)] * 2,
                            [str(MAX_PROFILE_WIDTH)] * 2]:
        raise RuntimeError("supported integer boundary lost its exact profiles")
    print(json.dumps({"schedule_controls": len(expected),
                      "status_controls": len(cases),
                      "integer_width_controls": len(rejected_widths) + 1, "status": "PASS"}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("executable", nargs="?", type=Path)
    parser.add_argument("--base", type=int, default=10)
    parser.add_argument("--e")
    parser.add_argument("--g")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--schedule", choices=("balanced", "balanced-opposite", "clustered"),
                        default="balanced")
    parser.add_argument("--cap", type=int, default=1_000_000)
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--witness", action="store_true")
    parser.add_argument("--legacy", action="store_true")
    parser.add_argument("--width", type=int,
                        help="exact two-profile decision for uniform center width <= W (W >= 2)")
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return 0
    try:
        if args.repeat < 1 or not 2 <= args.base <= 62:
            raise ValueError("require repeat >= 1 and 2 <= base <= 62")
        e = bitstream(args.e or "") * args.repeat
        g = bitstream(args.g or "") * args.repeat
        if len(e) != len(g):
            raise ValueError("e and g lengths differ")
        if not 0 < args.seconds <= 1500 or not 1 <= args.cap <= 30_000_000:
            raise ValueError("require 0 < seconds <= 1500 and 1 <= cap <= 30000000")
        if args.width is not None and args.width < 2:
            raise ValueError("the two-profile width reduction requires W >= 2")
        v = schedule(g, args.schedule)
    except ValueError as exc:
        parser.error(str(exc))
    jobs = [(v, None)] if args.width is None else [
        (schedule(g, "balanced"), args.width - 1),
        (schedule(g, "balanced-opposite"), args.width)]
    plan = {"base": args.base, "period": len(g), "e": e, "g": g, "v": v,
            "sum_g": g.count("1"), "sum_v": v.count("1"),
            "length_offsets": length_offsets(g, v),
            "legacy_packed_bits": 2 * len(g) + 6 * g.count("1") + 7 * v.count("1"),
            "binary_patterns_replaced": math.comb(len(g), v.count("1")),
            "scope": "fixed driver; no B existence claim", "uniform_width_cap": args.width,
            "profiles": [{"v": pat, "m0": m0} for pat, m0 in jobs]}
    print(json.dumps(plan, sort_keys=True), flush=True)
    if args.plan:
        return 0
    # This first runner deliberately targets the unchanged repository MAXP=32 solver.
    if len(g) > 32:
        print(json.dumps({"status": "UNDECIDED", "reason": "unchanged cauto_fast supports P <= 32"}))
        return 2
    if args.width is not None and args.width > MAX_PROFILE_WIDTH:
        print(json.dumps({"status": "UNDECIDED", "reason":
                          f"unchanged cauto_fast requires W <= {MAX_PROFILE_WIDTH} for signed-int m+g+1"}))
        return 2
    if plan["legacy_packed_bits"] > 256:
        print(json.dumps({"status": "UNDECIDED", "reason": "legacy/fallback packed key exceeds 256 bits"}))
        return 2
    if args.executable is None:
        parser.error("provide the compiled cauto_fast executable or use --plan")
    start = time.monotonic()
    outcomes = []
    for pat, m0 in jobs:
        size = str(m0 if m0 is not None else 1)
        command = [str(args.executable.resolve()), str(args.base), e, g, size, size,
                   "-v", pat, "-cap", str(args.cap)]
        if m0 is None:
            command.append("-allm")
        if args.witness:
            command.append("-w")
        if args.legacy:
            command.append("-legacy")
        try:
            remaining = args.seconds - (time.monotonic() - start)
            if remaining <= 0:
                raise subprocess.TimeoutExpired(command, args.seconds)
            run = subprocess.run(command, text=True, capture_output=True, timeout=remaining,
                                 check=False)
            status, reason = classify(run.stdout, run.returncode, pat, all_lengths=m0 is None)
            if run.stdout:
                print(run.stdout, end="" if run.stdout.endswith("\n") else "\n")
            if run.stderr:
                print(run.stderr, file=sys.stderr, end="" if run.stderr.endswith("\n") else "\n")
        except subprocess.TimeoutExpired:
            status, reason = "UNDECIDED", "wall-time cap"
        except OSError as exc:
            status, reason = "UNDECIDED", str(exc)
        outcomes.append(status)
        print(json.dumps({"profile_status": status, "reason": reason,
                          "command": command}, sort_keys=True), flush=True)
        if status == "CENTER_FEASIBLE":
            break
    if "CENTER_FEASIBLE" in outcomes:
        status = "CENTER_FEASIBLE"
    elif "UNDECIDED" in outcomes or len(outcomes) != len(jobs):
        status = "UNDECIDED"
    else:
        status = "NO_CENTER_ALL_LENGTHS" if args.width is None else "NO_CENTER_WIDTH_AT_MOST"
    print(json.dumps({"status": status, "uniform_width_cap": args.width,
                      "seconds": time.monotonic() - start, "profiles": outcomes}, sort_keys=True))
    return 2 if status == "UNDECIDED" else 0


if __name__ == "__main__":
    sys.exit(main())
