#!/usr/bin/env python3
"""Reproduce the independent p11 all-repetition/all-width center exclusion.

Exact language equality and arithmetic are checked inside the engine. The
finite-k counts below are regression controls, not an all-k proof by themselves.
"""
from __future__ import annotations

import argparse
import json
import re

from regular_center import run


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary")
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--memory-mb", type=int, default=6144)
    args = parser.parse_args()
    result = run(args.binary, 10, "10100110011", "11100010000", 1, 1,
                 "01000010000", all_lengths=True, sizes=True, cap=500000,
                 edge_cap=12000000, work_cap=150000000,
                 timeout=args.timeout, memory_mb=args.memory_mb)
    print(result.stdout, end="")
    print(result.stderr, end="")
    incomplete = ("UNDECIDED", "CAPPED", "NOPERIOD", "INVALID_OR_UNSUPPORTED",
                  "REGULAR_ERROR")
    if result.returncode or any(x in result.stdout + result.stderr for x in incomplete):
        print("STATUS=UNDECIDED")
        return 2
    lines = result.stdout.splitlines()
    generic = [dict(re.findall(r"(\w+)=([^ ]+)", line)) for line in lines
               if line.startswith("REGULAR_LAYER ") and "mode=generic" in line]
    expected = [
        (35, 1225, 42875), (83, 7577, 657443),
        (243, 115033, 34755075), (563, 559193, 414911363),
        (755, 960601, 752450435), (755, 960601, 752450435),
    ]
    actual = [tuple(int(row[f"count{k}"]) for k in (1, 2, 3)) for row in generic]
    if actual != expected:
        raise RuntimeError(f"finite-k regression changed: {actual}")
    for row in generic[-2:]:
        if (int(row["states"]), int(row["edges"])) != (13876, 470714):
            raise RuntimeError("fixed-language size changed")
    periods = [line for line in lines if line.startswith("REGULAR_PERIOD ")]
    if periods != ["REGULAR_PERIOD jstar=5 period=1 equality=full_canonical_DFA"]:
        raise RuntimeError(f"missing exact language return: {periods}")
    done = [dict(re.findall(r"(\w+)=([^ ]+)", line)) for line in lines
            if line.startswith("DONE ")]
    required = {"status": "none", "quantifier": "all_positive_repetitions",
                "jstar": "5", "period": "1", "mlo": "23", "classes": "2",
                "feasible_classes": "0", "images": "40", "tails": "24"}
    if len(done) != 1 or any(done[0].get(k) != v for k, v in required.items()):
        raise RuntimeError(f"incomplete all-width conclusion: {done}")
    if any(line.startswith("FEASIBLE") for line in lines):
        raise RuntimeError("unexpected positive; inspect full arithmetic witness immediately")
    print("P11_REGULAR_INDEPENDENT " + json.dumps(required, sort_keys=True))
    print("STATUS=NO_CENTER_FOR_ANY_POSITIVE_REPETITION_OR_FINITE_WIDTH_OF_THIS_DRIVER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
