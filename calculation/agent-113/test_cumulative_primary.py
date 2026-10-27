#!/usr/bin/env python3
"""Second-author all-width comparisons against Agent 101's PR #357.

The independently written global carry-tuple solver is the reference here.
An independent positional-integer replay checks every positive in both engines.
NONE/EXHAUSTED are compared only after complete decisions; limits are failures
of this deliberately small regression, never mathematical negative results.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import subprocess
import time

from center_reachability import CenterProblem


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def bits(xs):
    return "".join(map(str, xs))


def cases():
    for base in range(2, 6):
        for period in range(2, 5):
            for g in itertools.product((0, 1), repeat=period):
                if not sum(g) or sum(g) % 2:
                    continue
                for places in itertools.combinations(range(period), sum(g)//2):
                    v = tuple(int(i in places) for i in range(period))
                    for e in itertools.product((0, 1), repeat=period):
                        yield base, bits(e), bits(g), bits(v)


def replay(case, words, initial_width):
    """Use positional integer division, not the carry-layer recurrence."""
    base, es, gs, vs = case
    require(isinstance(words, list) and len(words) == len(es), "bad witness period")
    require(type(initial_width) is int and len(words[0]) == initial_width,
            "bad witness initial width")
    for t, word in enumerate(words):
        require(isinstance(word, list) and word and word == word[::-1],
                "empty or asymmetric center")
        require(all(type(x) is int and 0 <= x <= 2*base-2 for x in word),
                "out-of-range coefficient")
        n = int(es[t]) + sum(x * base**j for j, x in enumerate(word))
        require(n // base**len(word) == 1-int(es[t]), "wrong terminal carry")
        digits = [(n // base**j) % base for j in range(len(word))]
        if gs[t] == "1":
            digits.append((base-1)*int(es[t]))
        raw = [a+b for a, b in zip(digits, reversed(digits))]
        if vs[t] == "1":
            require(len(raw) >= 3 and raw[0] == raw[-1] == base-1,
                    "invalid neutral trim")
            raw = raw[1:-1]
        require(raw == words[(t+1) % len(words)], "temporal center mismatch")


def primary(binary, case, cap, seconds):
    command = [binary, str(case[0]), *case[1:], "--cap", str(cap),
               "--seconds", str(seconds), "--memory-mb", "2048"]
    proc = subprocess.run(command, capture_output=True, text=True, timeout=seconds+5)
    lines = [line for line in proc.stdout.splitlines() if line.startswith("{")]
    require(len(lines) == 1, f"primary returned no unique JSON: {case}: {proc.stdout}")
    result = json.loads(lines[0])
    require(proc.returncode in (0, 2, 3), f"primary failed: {case}: {proc.stderr}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary", required=True)
    parser.add_argument("--cap", type=int, default=50000)
    parser.add_argument("--seconds", type=int, default=5)
    args = parser.parse_args()
    require(Path(args.primary).is_file(), "primary executable is missing")
    require(args.cap > 0 and 0 < args.seconds <= 1800, "invalid test budgets")
    started = time.monotonic()
    counts = dict(cases=0, agreements=0, feasible=0, exhausted=0,
                  witnesses_replayed=0, short_case_witnesses=0, guards=0)
    for case in cases():
        problem = CenterProblem(*case)
        own = problem.all_widths(cap=args.cap, seconds=args.seconds, witness=True)
        other = primary(args.primary, case, args.cap, args.seconds)
        normalized = "EXHAUSTED" if other["status"] == "NONE" else other["status"]
        require(own["status"] in ("FEASIBLE", "EXHAUSTED") and
                normalized in ("FEASIBLE", "EXHAUSTED"),
                f"incomplete small comparison: {case}: {own}: {other}")
        require(own["status"] == normalized, f"DISAGREEMENT: {case}: {own}: {other}")
        counts["cases"] += 1
        counts["agreements"] += 1
        counts["feasible" if normalized == "FEASIBLE" else "exhausted"] += 1
        if normalized == "FEASIBLE":
            replay(case, own.get("centers"), own.get("initial_width"))
            replay(case, other.get("C"), other.get("m0"))
            counts["witnesses_replayed"] += 2
            if own["initial_width"] < 3-problem.dmin:
                counts["short_case_witnesses"] += 1
    require(counts["cases"] == 2240, "exhaustive family count changed")
    positive = (11, "011011", "001001", "000001")
    problem = CenterProblem(*positive)
    for result in (problem.all_widths(cap=1, seconds=5),
                   problem.all_widths(cap=50000, seconds=1e-9),
                   primary(args.primary, positive, 1, 5)):
        require(result["status"] == "UNDECIDED", f"limit became decision: {result}")
        counts["guards"] += 1
    # Primary deliberately rejects zero trims; this does not contradict the
    # independent implementation's additional exact zero-overflow support.
    zero = primary(args.primary, (2, "10", "00", "00"), 50000, 5)
    require(zero["status"] == "UNDECIDED", "unsupported primary scope became negative")
    counts["guards"] += 1
    print(json.dumps(dict(status="PASS", classification="COMPUTED", counts=counts,
                          seconds=round(time.monotonic()-started, 6)), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
