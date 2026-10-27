#!/usr/bin/env python3
"""Choose a binary trim schedule minimizing cauto_fast's FIRST generic frontier.

The objective is exact, not a prediction of later frontier sizes or running time.
For one temporal segment, a 2*b-1 state coefficient DP counts its possible first
layer traces.  Different choices have distinct (local configuration, first
coefficient) outputs.  Global tuple assembly is injective on segment choices,
so the frontier cardinality is the product of segment counts.  A cyclic interval
partition DP minimizes this product over every binary schedule with G/2 trims.

This is a search-planning tool.  A zero objective only excludes sufficiently wide
centers for the selected schedule; the all-length solver must still check tails.
Arbitrary-schedule equivalence is a separately credited padding theorem.
"""
from __future__ import annotations

import argparse
from itertools import combinations, product
import json
from math import prod
from pathlib import Path
import random
import re
import subprocess
from typing import Sequence


def validate(e: str, g: str, base: int = 10) -> tuple[int, int]:
    if not isinstance(base, int) or isinstance(base, bool) or not 2 <= base <= 62:
        raise ValueError("base must be an integer in 2..62")
    if not e or len(e) != len(g) or set(e + g) - {"0", "1"}:
        raise ValueError("require equal nonempty binary e/g streams")
    if len(e) > 128:
        raise ValueError("planner supports periods at most 128")
    total = g.count("1")
    if total == 0 or total % 2:
        raise ValueError("require positive even overflow total")
    return len(e), total // 2


def segment_counts(e: str, g: str, base: int = 10) -> list[list[int]]:
    """table[start][length] counts traces ending in the neutral coefficient."""
    period, _ = validate(e, g, base)
    alphabet = 2 * base - 1
    transfers: list[list[list[int]]] = []
    for et, gt in zip(map(int, e), map(int, g)):
        step = [[] for _ in range(alphabet)]
        for coefficient in range(alphabet):
            for inward in (0, 1):
                if (coefficient + inward) // base != 1 - et:
                    continue
                left_digit = (coefficient + et) % base
                partner = ((coefficient + inward) % base
                           if gt == 0 else (base - 1) * et)
                step[coefficient].append(left_digit + partner)
        transfers.append(step)
    table = [[0] * (period + 1) for _ in range(period)]
    for start in range(period):
        counts = [1] * alphabet
        for length in range(1, period + 1):
            following = [0] * alphabet
            for coefficient, targets in enumerate(transfers[(start + length - 1) % period]):
                for target in targets:
                    following[target] += counts[coefficient]
            counts = following
            table[start][length] = counts[base - 1]
    return table


def _factors(pattern: str, table: list[list[int]]) -> list[dict[str, int]]:
    period = len(pattern)
    endpoints = [i for i, value in enumerate(pattern) if value == "1"]
    result = []
    for i, endpoint in enumerate(endpoints):
        start = (endpoint + 1) % period
        following = endpoints[(i + 1) % len(endpoints)]
        length = (following - start) % period + 1
        result.append({"start": start, "length": length,
                       "count": table[start][length]})
    return result


def pattern_cost(e: str, g: str, pattern: str, base: int = 10,
                 table: list[list[int]] | None = None) -> int:
    period, trims = validate(e, g, base)
    if len(pattern) != period or set(pattern) - {"0", "1"} or pattern.count("1") != trims:
        raise ValueError("trim schedule must be binary with G/2 ones")
    if table is None:
        table = segment_counts(e, g, base)
    return prod(x["count"] for x in _factors(pattern, table))


def optimize(e: str, g: str, base: int = 10) -> dict[str, object]:
    """Return a globally minimum-F1 pattern, exact cost, and segment factors."""
    period, trims = validate(e, g, base)
    table = segment_counts(e, g, base)
    best: tuple[int, str] | None = None
    for anchor in range(period):
        # k segments cover [anchor, anchor+distance).  Every cyclic partition
        # appears for at least one anchor immediately after a trim endpoint.
        states: dict[int, tuple[int, tuple[int, ...]]] = {0: (1, ())}
        for k in range(trims):
            following: dict[int, tuple[int, tuple[int, ...]]] = {}
            for distance, (cost, endpoints) in states.items():
                for end in range(distance + 1, period - (trims - k - 1) + 1):
                    value = cost * table[(anchor + distance) % period][end - distance]
                    current = following.get(end)
                    if current is None or value < current[0]:
                        following[end] = (value, endpoints + ((anchor + end - 1) % period,))
            states = following
        cost, endpoints = states[period]
        selected = set(endpoints)
        pattern = "".join("1" if t in selected else "0" for t in range(period))
        candidate = (cost, pattern)
        if best is None or candidate < best:
            best = candidate
    if best is None:
        raise RuntimeError("no cyclic partition despite a validated positive trim count")
    cost, pattern = best
    factors = _factors(pattern, table)
    if len(factors) != trims or prod(x["count"] for x in factors) != cost:
        raise RuntimeError("internal partition reconstruction mismatch")
    return {"base": base, "period": period, "overflows": 2 * trims,
            "trims": trims, "pattern": pattern, "first_frontier": cost,
            "factors": factors}


def _small_brute_selftest() -> dict[str, int]:
    cases = schedules = 0
    for base in (2, 3, 10):
        for period in range(2, 6):
            for g_bits in product("01", repeat=period):
                g = "".join(g_bits)
                if not g.count("1") or g.count("1") % 2:
                    continue
                for e_bits in product("01", repeat=period):
                    e = "".join(e_bits)
                    table = segment_counts(e, g, base)
                    best = None
                    for positions in combinations(range(period), g.count("1") // 2):
                        selected = set(positions)
                        pattern = "".join("1" if t in selected else "0" for t in range(period))
                        cost = pattern_cost(e, g, pattern, base, table)
                        best = cost if best is None else min(best, cost)
                        schedules += 1
                    result = optimize(e, g, base)
                    if result["first_frontier"] != best:
                        raise RuntimeError(f"partition mismatch: {base=} {e=} {g=}")
                    cases += 1
    return {"exhaustive_stream_cases": cases, "brute_schedules": schedules}


def _solver_selftest(solver: Path, count: int = 24) -> dict[str, int]:
    """Compare the independent F1 formula with existing cauto_fast -sz output."""
    rng = random.Random(111)
    tested = 0
    for attempt in range(count * 4):
        if tested == count:
            break
        base = rng.choice((2, 3, 4, 5, 10, 11))
        period = rng.randrange(2, 9)
        total = 2 * rng.randrange(1, min(3, period // 2) + 1)
        one_g = set(rng.sample(range(period), total))
        one_v = set(rng.sample(range(period), total // 2))
        e = "".join(str(rng.randrange(2)) for _ in range(period))
        g = "".join("1" if t in one_g else "0" for t in range(period))
        pattern = "".join("1" if t in one_v else "0" for t in range(period))
        expected = pattern_cost(e, g, pattern, base)
        cap = max(100, expected)
        command = [str(solver.resolve()), str(base), e, g, "1", "1", "-v", pattern,
                   "-allm", "-sz", "-cap", str(cap)]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=10)
        if completed.returncode:
            raise RuntimeError(f"solver exited {completed.returncode}: {completed.stderr[-1000:]}")
        match = re.search(r"^detect sizes:\s*(\d+)", completed.stderr, re.M)
        if not match:
            raise RuntimeError(f"missing first frontier size: {completed.stderr[-1000:]}")
        actual = int(match[1])
        if actual != expected:
            raise RuntimeError(f"F1 mismatch: {base=} {e=} {g=} {pattern=} {expected=} {actual=}")
        tested += 1
    if tested != count:
        raise RuntimeError("incomplete solver differential sample")
    return {"solver_first_frontier_checks": tested}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("e", nargs="?")
    parser.add_argument("g", nargs="?")
    parser.add_argument("--base", type=int, default=10)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--solver", type=Path)
    args = parser.parse_args(argv)
    if args.selftest:
        checks = _small_brute_selftest()
        if args.solver is not None:
            checks.update(_solver_selftest(args.solver))
        print(json.dumps(checks, sort_keys=True))
    if args.e is not None or args.g is not None:
        if args.e is None or args.g is None:
            parser.error("provide both e and g")
        print(json.dumps(optimize(args.e, args.g, args.base), sort_keys=True))
    elif not args.selftest:
        parser.error("provide e/g or --selftest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
