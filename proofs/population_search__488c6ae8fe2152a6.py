#!/usr/bin/env python3
"""Exact finite discovery of extreme-population obstructions.

This is discovery, not a universal proof.  PopulationObstructions.lean
checks the selected actual integer transitions in the Lean kernel.
All q words are listed least-significant-column first.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import argparse
import json


def digits(n):
    return [int(x) for x in str(n)[::-1]]


def pairs(ds):
    return [a + b for a, b in zip(ds, ds[::-1])]


def qstep(q):
    carry = 0
    out = []
    for x in q:
        carry, d = divmod(x + carry, 10)
        out.append(d)
    if carry:
        out.append(carry)
    return pairs(out), out, carry


def population(q):
    return [q.count(0), q.count(18)]


def runs(q):
    return [sum(x == v and (i == 0 or q[i - 1] != v)
                for i, x in enumerate(q)) for v in (0, 18)]


def minimal_realization(q):
    ds = [0] * len(q)
    for i in range(len(q) // 2):
        high = max(1 if i == 0 else 0, q[i] - 9)
        ds[-1 - i] = high
        ds[i] = q[i] - high
    if len(q) % 2:
        ds[len(q) // 2] = q[len(q) // 2] // 2
    n = sum(d * 10**i for i, d in enumerate(ds))
    assert digits(n) == ds and pairs(ds) == q
    return n, ds


def witness(q, nq, out, overflow, n=None):
    if n is None:
        n, ds = minimal_realization(q)
    else:
        ds = digits(n)
        assert pairs(ds) == q
    reverse = int(str(n)[::-1])
    m = n + reverse
    assert digits(m) == out
    assert pairs(digits(m)) == nq
    return dict(n=n, reverse=reverse, next=m, digits=ds, next_digits=out,
                q=q, next_q=nq, width=len(q), next_width=len(nq),
                overflow=bool(overflow), population=population(q),
                next_population=population(nq), runs=runs(q),
                next_runs=runs(nq),
                input_palindrome=(ds == ds[::-1]),
                output_palindrome=(out == out[::-1]))


def search(max_width):
    results = dict(schema=1, parameters=dict(base=10, min_width=1,
        max_width=max_width, enumeration="all symmetric q in [0,18], q[0]>0; even center",
        realization="smallest positive integer at each q",
        counts="all physical columns, including the center once",
        runs="maximal nonempty constant 0 or 18 runs, across the full word",
        criteria="both population coordinates increase; both run coordinates increase; simultaneous births from zero",
        status="finite exact discovery; no universal positive claim inferred"),
        per_width=[], witnesses={})
    for width in range(1, max_width + 1):
        delta_hist = Counter()
        totals = Counter()
        best = {}
        for left in product(range(19), repeat=width // 2):
            for center in (range(0, 19, 2) if width % 2 else (None,)):
                q = list(left) + ([] if center is None else [center]) + list(left[::-1])
                if not q[0]:
                    continue
                nq, out, overflow = qstep(q)
                p, np = population(q), population(nq)
                r, nr = runs(q), runs(nq)
                delta = tuple(b-a for a, b in zip(p+r, np+nr))
                delta_hist[(int(bool(overflow)),) + delta] += 1
                totals["words"] += 1
                branch = "overflow" if overflow else "nooverflow"
                totals[branch] += 1
                checks = {
                    "both_population_increase": all(x > 0 for x in delta[:2]),
                    "both_runs_increase": all(x > 0 for x in delta[2:]),
                    "births_from_no_extremes": p == [0, 0] and all(x > 0 for x in np),
                    "all_four_increase": all(x > 0 for x in delta),
                }
                for criterion, ok in checks.items():
                    if not ok:
                        continue
                    totals[criterion] += 1
                    totals[branch + ":" + criterion] += 1
                    key = branch + ":" + criterion
                    w = witness(q, nq, out, overflow)
                    if key not in best or w["n"] < best[key]["n"]:
                        best[key] = w
                    if key not in results["witnesses"] or w["n"] < results["witnesses"][key]["n"]:
                        results["witnesses"][key] = w
        results["per_width"].append(dict(width=width, totals=dict(sorted(totals.items())),
            delta_histogram=[dict(overflow=bool(k[0]), population_delta=list(k[1:3]),
                                 runs_delta=list(k[3:]), words=v)
                            for k, v in sorted(delta_hist.items())], best=best))
    return results


def scan_orbit(seed, steps):
    """Retain every tested actual integer and statistic, not just successes."""
    n = seed
    trace = []
    first = {}
    totals = Counter()
    for time in range(steps):
        q = pairs(digits(n))
        nq, out, overflow = qstep(q)
        w = witness(q, nq, out, overflow, n=n)
        delta = [b - a for a, b in zip(w["population"] + w["runs"],
                                      w["next_population"] + w["next_runs"])]
        checks = {
            "both_population_increase": all(x > 0 for x in delta[:2]),
            "both_runs_increase": all(x > 0 for x in delta[2:]),
            "births_from_no_extremes": w["population"] == [0, 0]
                and all(x > 0 for x in w["next_population"]),
            "all_four_increase": all(x > 0 for x in delta),
        }
        record = dict(time=time, **w, population_delta=delta[:2], runs_delta=delta[2:])
        trace.append(record)
        branch = "overflow" if overflow else "nooverflow"
        for criterion, ok in checks.items():
            if ok:
                totals[criterion] += 1
                totals[branch + ":" + criterion] += 1
                first.setdefault(criterion, record)
                first.setdefault(branch + ":" + criterion, record)
        n = w["next"]
    return dict(parameters=dict(seed=seed, steps=steps,
        indexing="transition at time t is orbit(seed,t) to orbit(seed,t+1)"),
        totals=dict(sorted(totals.items())), first_witnesses=first, trace=trace)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-width", type=int, default=8)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("population_results.json"))
    parser.add_argument("--orbit-seed", type=int, default=196)
    parser.add_argument("--orbit-steps", type=int, default=100)
    args = parser.parse_args()
    result = search(args.max_width)
    result["actual_orbit_scan"] = scan_orbit(args.orbit_seed, args.orbit_steps)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"parameters": result["parameters"],
                      "totals": [{"width": x["width"], **x["totals"]}
                                 for x in result["per_width"]],
                      "witnesses": result["witnesses"],
                      "orbit_first_all_four": result["actual_orbit_scan"]["first_witnesses"].get("all_four_increase"),
                      "orbit_totals": result["actual_orbit_scan"]["totals"]}, indent=2))
