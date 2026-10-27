#!/usr/bin/env python3
"""Independent period-20 exterior census, with fail-closed coverage checks.

Corroborates Agent 4's prior #311/#323 computation. This program compiles the
explicit-tuple implementation, checks known positives by whole-integer
arithmetic, enumerates every overflow necklace, and exhausts the surviving
graphs. No center compatibility or Lean theorem follows from this computation.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time

import p20_coverage

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer_normalize(base, word, carry):
    """Normalize by evaluating the whole word, independent of column recursion."""
    value = carry + sum(coefficient * base**j for j, coefficient in enumerate(word))
    outgoing, value = divmod(value, base**len(word))
    digits = []
    for _ in word:
        value, digit = divmod(value, base)
        digits.append(digit)
    require(value == 0 and outgoing in (0, 1), "invalid normalized carry")
    return digits, outgoing


def replay_witness(base, g, hit):
    words, expected_e = hit["B"], hit["e"]
    require(len(words) == len(g) == len(expected_e), "witness period mismatch")
    trims = []
    for t, word in enumerate(words):
        require(all(type(x) is int and 0 <= x <= 2 * base - 2 for x in word),
                "coefficient outside bounds")
        require(not word or word[0] > 0, "zero exterior head")
        require(not word or word[-1] != base - 1, "witness was not canonical")
        low, e = integer_normalize(base, word, 0)
        high, overflow = integer_normalize(base, word[::-1], 1 - e)
        require(e == int(expected_e[t]) and overflow == int(g[t]),
                "witness carry/overflow mismatch")
        high.reverse()
        if overflow:
            low.append((base - 1) * (1 - e))
            high.insert(0, 1)
        require(len(low) == len(high), "raw exterior length mismatch")
        raw = [x + y for x, y in zip(low, high)]
        trim = 0
        while raw and raw[-1] == base - 1:
            raw.pop()
            trim += 1
        require(raw == words[(t + 1) % len(words)], "full exterior cycle failed")
        trims.append(trim)
    require(sum(trims) == g.count("1"), "exterior length budget failed")
    return {"e": expected_e, "width": hit["width"], "edges": len(words),
            "sum_u": sum(trims), "max_canonical_width": max(map(len, words))}


def call_solver(binary, base, g, states, seconds, witness=False):
    command = [str(binary), str(base), g, "--states", str(states),
               "--seconds", str(seconds), "--memory-mib", "4096"]
    if witness:
        command.append("--witness")
    try:
        process = subprocess.run(command, capture_output=True, text=True,
                                 timeout=seconds + 5)
    except subprocess.TimeoutExpired:
        return {"base": base, "g": g, "status": "PROCESS_TIMEOUT_UNDECIDED",
                "complete": False, "accepts": []}
    if process.returncode:
        return {"base": base, "g": g, "status": "PROCESS_ERROR_UNDECIDED",
                "complete": False, "returncode": process.returncode,
                "diagnostic": process.stderr[-240:], "accepts": []}
    try:
        result = json.loads(process.stdout)
    except json.JSONDecodeError:
        return {"base": base, "g": g, "status": "MALFORMED_OUTPUT_UNDECIDED",
                "complete": False, "accepts": []}
    require(result["base"] == base and result["g"] == g, "solver query mismatch")
    require(result["period"] == len(g) and result["prefix_width"] == 0,
            "the census requires unrestricted spatial width")
    if result["complete"]:
        require(result["status"] == "EXHAUSTED" and result["frontier"] == 0 and
                result["boundary_expansion_completed"] and
                not result["partial_expansion"] and
                result["processed_interior"] == result["interior_states"],
                "invalid exhausted verdict")
    else:
        require(result["status"] != "EXHAUSTED", "contradictory terminal verdict")
    return result


def positive_controls(binary, states, seconds):
    # Previously documented exterior returns, not new discoveries.
    controls = [(2, "10", "10"), (4, "100", "100"),
                (10, "11100010000", "10100110011"),
                (10, "100010001000", "100101011010"),
                (20, "10001000", "10100101")]
    results = []
    for base, g, expected_e in controls:
        result = call_solver(binary, base, g, states, seconds, witness=True)
        require(result["complete"], "positive control did not finish")
        require(expected_e in {hit["e"] for hit in result["accepts"]},
                "known positive carry stream disappeared")
        witnesses = [replay_witness(base, g, hit) for hit in result["accepts"]]
        results.append({"base": base, "g": g, "states": result["states"],
                        "max_depth": result["max_depth"], "witnesses": witnesses})
    return results


def run(binary, args):
    begin = time.monotonic()
    coverage_tests = p20_coverage.selftest()
    coverage, _, words = p20_coverage.census(20)
    controls = positive_controls(binary, args.states, args.seconds)
    records = []
    deadline = time.monotonic() + args.batch_seconds
    for number, g in enumerate(words, 1):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            record = {"base": 10, "g": g, "status": "NOT_RUN_UNDECIDED",
                      "complete": False, "accepts": []}
        else:
            record = call_solver(binary, 10, g, args.states,
                                 min(args.seconds, remaining), witness=True)
            if record["accepts"]:
                record["independent_witness_replay"] = [
                    replay_witness(10, g, hit) for hit in record["accepts"]]
        records.append(record)
        if args.progress and number % 50 == 0:
            print(json.dumps({"processed": number, "total": len(words),
                              "terminal_counts": dict(Counter(r["status"] for r in records))}),
                  flush=True)
    counts = Counter(record["status"] for record in records)
    negative = (len(records) == len(words) and
                all(r["complete"] and not r["accepts"] for r in records))
    reached = [r for r in records if "states" in r]
    largest = max(reached, key=lambda r: r["states"]) if reached else None
    result = {"status": "COMPUTED_P20_EXTERIOR_NEGATIVE" if negative else "UNDECIDED_OR_ACCEPTED",
              "scope": "Base10 period20 exterior cycles, all widths; no center or Lean claim.",
              "source_sha256": hashlib.sha256((HERE / "exterior_tuple.cpp").read_bytes()).hexdigest(),
              "coverage": coverage, "coverage_tests": coverage_tests,
              "positive_controls": controls, "records": records,
              "terminal_counts": dict(counts), "total_states": sum(r["states"] for r in reached),
              "total_generated_columns": sum(r["generated_columns"] for r in reached),
              "max_peak_rss_mib": max((r["peak_rss_mib"] for r in reached), default=0),
              "max_graph": None if largest is None else {
                  k: largest[k] for k in ("g", "states", "max_depth", "peak_rss_mib")},
              "elapsed_seconds": round(time.monotonic() - begin, 6)}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    summary = {k: v for k, v in result.items() if k not in ("records", "positive_controls")}
    summary["positive_control_count"] = len(controls)
    summary["positive_streams_replayed"] = sum(len(c["witnesses"]) for c in controls)
    summary["positive_edges_replayed"] = sum(w["edges"] for c in controls for w in c["witnesses"])
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0 if negative else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, help="use this compiled tuple solver")
    parser.add_argument("--states", type=int, default=2000000)
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--batch-seconds", type=float, default=900)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--output", type=Path, help="optional mathematical per-word results")
    args = parser.parse_args()
    if not (1 <= args.states <= 20000000 and 0 < args.seconds <= 1190 and
            0 < args.batch_seconds <= 1500):
        parser.error("budgets: states1..20M, seconds(0,1190], batch-seconds(0,1500]")
    if args.binary:
        raise SystemExit(run(args.binary.resolve(), args))
    with tempfile.TemporaryDirectory(prefix="agent116-exterior-") as directory:
        binary = Path(directory) / "exterior_tuple"
        subprocess.run(["c++", "-O3", "-std=c++17", "-Wall", "-Wextra", "-pedantic",
                        str(HERE / "exterior_tuple.cpp"), "-o", str(binary)],
                       check=True, timeout=90)
        raise SystemExit(run(binary, args))


if __name__ == "__main__":
    main()
