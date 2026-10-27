#!/usr/bin/env python3
"""Credited cross-reproduction of Agent118 P48 and Agent116 base20 controls.

Primary P48: PR369, commit19e13c356d9a917cf8bce074be71607f6b7cdd87.
Base20 source query: PR356, commitb7a718b78d67cf54d362232ba1b8f90fbec23af8,
reports/agent-116-T7.md, constructive width27 query before canonical rotation.
This script uses Agent111's independently implemented delayed-output MDD.
It does not copy either primary implementation or claim discovery credit.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from center_controls import require
from long_center import run
from mdd_regression import replay


def complete(result, status):
    require(result.returncode == 0, f"process unresolved: {result.returncode} {result.stderr[-2000:]}")
    require(not re.search(r"CAPPED|NOPERIOD|UNDECIDED|UNSUPPORTED|MDD_ERROR", result.stdout + result.stderr),
            "incomplete run is not a completed cross-check")
    rows = re.findall(r"^DONE (.*)$", result.stdout, re.M)
    require(len(rows) == 1, "missing/duplicate completion record")
    fields = dict(re.findall(r"(\w+)=(\S+)", rows[0]))
    require(fields.get("status") == status, f"unexpected cross-check outcome: {fields}")
    return fields


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    args = parser.parse_args()

    e, g, v = "101010010101" * 4, "100010001000" * 4, "00001000" * 6
    result = run(args.binary, 10, e, g, 1, 1, v, all_lengths=True,
                 cap=1000000, timeout=60, memory_mb=4096, sizes=True)
    fields = complete(result, "none")
    expected = [1000000, 935560192, 8574299136, 8868958208,
                9157137472, 9312887872, 9312887872]
    rows = re.findall(r"^detect sizes:(.*)$", result.stderr, re.M)
    require(len(rows) == 1 and list(map(int, rows[0].split())) == expected,
            "P48 generic frontier counts differ from the primary result")
    require(all(fields.get(k) == value for k, value in
                {"jstar": "6", "period": "1", "mlo": "97", "classes": "2",
                 "feasible_classes": "0", "tails": "98"}.items()),
            "P48 periodicity/complete width-tail coverage differs")
    require(not re.search(r"^FEASIBLE", result.stdout, re.M), "unexpected P48 positive")
    print("AGENT118_P48_CROSSCHECK " + json.dumps(
        {"generic_frontiers": expected, "terminal": fields}, sort_keys=True), flush=True)

    e, g, v = "10100101", "10001000", "00100000"
    result = run(args.binary, 20, e, g, 27, 27, v, cap=1000000,
                 timeout=60, memory_mb=4096, witness=True)
    fields = complete(result, "hit")
    edges = replay(result.stdout, 20, e, g, v)
    require(edges == 8, "base20 witness is missing a phase")
    print("AGENT116_BASE20_POSITIVE " + json.dumps(
        {"width": 27, "integer_replayed_edges": edges, "terminal": fields},
        sort_keys=True), flush=True)
    print("ALL CREDITED CROSS-CHECKS PASSED")


if __name__ == "__main__":
    main()
