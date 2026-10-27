#!/usr/bin/env python3
"""Small concrete adapter/witness controls, suitable for ASan/UBSan builds."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess

from center_controls import (alternating_trim, inspect_certificate, pad_to_schedule,
                             read_certificates, require)
from mdd_regression import replay


def bits(word):
    return "".join(map(str, word))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    args = parser.parse_args()
    binary = args.binary.resolve()
    root = Path(__file__).resolve().parents[2]
    certificates = read_certificates(root)
    cases = []
    for base, repeat, compare in ((2, 1, True), (26, 1, True), (2, 2, True), (8, 6, False)):
        edges = certificates[base] * repeat
        e, g = inspect_certificate(base, edges)
        trim = alternating_trim(g)
        padded, _ = pad_to_schedule(base, edges, trim)
        width = len(padded[0].C)
        lengths = [len(edge.C) for edge in padded]
        require(min((m + 1) // 2 for m in lengths) < max((m + 1) // 2 for m in lengths),
                "positive control must exercise inactive tail segments")
        cases.append((base, e, g, trim, width, compare, True))
    cases.append((10, tuple(map(int, "10100110011" * 3)),
                  tuple(map(int, "11100010000" * 3)),
                  tuple(map(int, "01000010000" * 3)), 2, True, False))
    totals = {"adapter_runs": 0, "complete_frontier_comparisons": 0,
              "integer_replayed_witness_edges": 0, "positive_inactive_tail_cases": 0,
              "period33_bounded_negative_cases": 0}
    env = os.environ.copy()
    env["ASAN_OPTIONS"] = "detect_leaks=0"  # leak inspection is unavailable under the host ptrace sandbox
    for base, e, g, trim, width, compare, positive in cases:
        command = [str(binary), str(base), bits(e), bits(g), str(width), str(width),
                   "-v", bits(trim), "-cap", "200000", "-work-cap", "2000000", "-w"]
        if compare:
            command.extend(["-diff", "-diff-limit", "100000"])
        result = subprocess.run(command, text=True, capture_output=True, env=env, timeout=30, check=False)
        require(result.returncode == 0, f"adapter failed: {result.stdout}\n{result.stderr}")
        require("AddressSanitizer" not in result.stderr and "runtime error:" not in result.stderr,
                f"sanitizer finding: {result.stderr}")
        require(f"status={'hit' if positive else 'none'}" in result.stdout,
                f"control unresolved/wrong result: {result.stdout}\n{result.stderr}")
        counts = re.findall(r"\bdiff_images=(\d+)", result.stdout)
        require(len(counts) == 1 and (not compare or int(counts[0]) > 0),
                "missing full-frontier differential count")
        totals["complete_frontier_comparisons"] += int(counts[0])
        if positive:
            checked = replay(result.stdout, base, e, g, trim)
            require(checked == len(e), "incomplete reconstructed witness")
            totals["integer_replayed_witness_edges"] += checked
            totals["positive_inactive_tail_cases"] += 1
        else:
            totals["period33_bounded_negative_cases"] += 1
        totals["adapter_runs"] += 1
    print("MDD_ADAPTER_SMOKE " + json.dumps(totals, sort_keys=True))


if __name__ == "__main__":
    main()
