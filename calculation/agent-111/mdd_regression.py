#!/usr/bin/env python3
"""Independent integration checks for the Agent 111 MDD center adapter.

The explicit solver is a representation differential, not an independent
arithmetic proof.  Reconstructed positive witnesses are separately replayed by
the whole-integer oracle in center_controls.py.  A cap never counts as a
completed comparison.  No stdout transcripts are written to the repository.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import re

from center_controls import (
    alternating_trim, center_step, inspect_certificate, pad_to_schedule,
    read_certificates, require,
)
from long_center import run


def bits(values):
    return "".join(map(str, values))


def parsed(result):
    require(result.returncode == 0, "solver process failed: " + result.stderr[-2000:])
    require(not re.search(r"CAPPED|NOPERIOD|UNDECIDED|UNSUPPORTED", result.stdout),
            "incomplete run is not a negative: " + result.stdout[-2000:])
    rows = re.findall(r"^DONE (.*)$", result.stdout, re.M)
    require(len(rows) == 1, "missing or duplicate completed status")
    fields = dict(re.findall(r"(\w+)=(\S+)", rows[0]))
    require(fields.get("status") in {"hit", "none"}, "nonterminal status")
    sizes = re.findall(r"^detect sizes:(.*)$", result.stderr, re.M)
    if not sizes:
        counts = re.findall(r"^MDD_LAYER layer=\d+ mode=generic tuples=(\S+)", result.stdout, re.M)
        if counts:
            sizes = [" ".join(counts)]
    require(len(sizes) == 1, "missing generic frontier counts")
    require(all(x.isdigit() for x in sizes[0].split()), "inexact frontier count")
    feasible = set(re.findall(r"^(FEASIBLE(?:_CLASS)?) .*?\bm0=(\d+)",
                              result.stdout, re.M))
    keys = ("status", "jstar", "period", "mlo", "classes", "feasible_classes")
    require(all(k in fields for k in keys), "incomplete all-length metadata")
    return tuple(fields[k] for k in keys), tuple(map(int, sizes[0].split())), feasible


def replay(stdout, base, e, g, v):
    edges = 0
    for line in stdout.splitlines():
        if not line.startswith(("FEASIBLE ", "FEASIBLE_CLASS ")):
            continue
        centers = {int(i): tuple(map(int, word.split(","))) if word else ()
                   for i, word in re.findall(r"\bC(\d+)=\[([^\]]*)\]", line)}
        require(set(centers) == set(range(len(e))), "missing reconstructed center")
        for i in range(len(e)):
            require(center_step(base, centers[i], int(e[i]), int(g[i]), int(v[i]))
                    == centers[(i + 1) % len(e)], "integer witness replay failed")
            edges += 1
    return edges


def all_length_cases(certificates):
    # Includes the no-trim legacy fallback, single segments, positive long
    # transients, empty frontiers, and the three established decimal negatives.
    yield 2, "10", "00", "00"
    yield 3, "01", "00", "00"
    for base in (2, 4, 8, 16, 26, 32):
        e, g = inspect_certificate(base, certificates[base])
        yield base, bits(e), bits(g), bits(alternating_trim(g))
    rng = random.Random(111033)
    for _ in range(24):
        p = rng.choice((2, 3, 4, 5, 6))
        g = [0] * p
        for i in rng.sample(range(p), 2):
            g[i] = 1
        v = [0] * p
        v[rng.randrange(p)] = 1
        yield rng.choice((2, 3, 4, 10)), bits(rng.randrange(2) for _ in range(p)), bits(g), bits(v)
    yield 10, "10100110011", "11100010000", "01000010000"
    yield 10, "10100110011" * 2, "11100010000" * 2, "01000010000" * 2
    yield 10, "101010010101" * 2, "100010001000" * 2, "00001000" * 3


def compare_all_lengths(binary, baseline, certificates, timeout, memory_mb):
    comparisons = positive = negative = generic_layers = witness_edges = 0
    for base, e, g, v in all_length_cases(certificates):
        # The same numeric cap has different meanings: explicit tuples versus
        # all historical DAG nodes.  Only completed uncapped answers compare.
        old = run(baseline, base, e, g, 1, 1, v, all_lengths=True,
                  cap=1000000, timeout=timeout, witness=False, sizes=True,
                  memory_mb=memory_mb)
        new = run(binary, base, e, g, 1, 1, v, all_lengths=True,
                  cap=1000000, timeout=timeout, witness=True, sizes=True,
                  memory_mb=memory_mb)
        a, b = parsed(old), parsed(new)
        require(a == b, f"explicit/MDD all-length mismatch b={base} e={e} g={g} v={v}\n{a}\n{b}")
        witness_edges += replay(new.stdout, base, e, g, v)
        comparisons += 1
        generic_layers += len(a[1])
        if a[0][0] == "hit":
            positive += 1
        else:
            negative += 1
    return {"all_length_comparisons": comparisons, "positive_patterns": positive,
            "negative_patterns": negative, "exact_generic_frontier_counts": generic_layers,
            "integer_replayed_witness_edges": witness_edges}


def source_positives(binary, certificates, timeout, memory_mb):
    cases = witness_edges = 0
    for base, source in sorted(certificates.items()):
        e, g = inspect_certificate(base, source)
        for level in (0, 1):
            v = alternating_trim(g, level)
            padded, _ = pad_to_schedule(base, source, v)
            width = len(padded[0].C)
            result = run(binary, base, bits(e), bits(g), width, width, bits(v),
                         cap=1000000, timeout=timeout, witness=True, memory_mb=memory_mb)
            require(result.returncode == 0 and "status=hit" in result.stdout
                    and not re.search(r"CAPPED|NOPERIOD|UNDECIDED", result.stdout),
                    f"known base-{base} positive lost: {result.stdout[-1000:]} {result.stderr[-1000:]}")
            edges = replay(result.stdout, base, bits(e), bits(g), bits(v))
            require(edges == len(source), "wrong fixed-width witness count")
            witness_edges += edges
            cases += 1
    return {"source_positive_cases": cases, "integer_replayed_witness_edges": witness_edges}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("binary", type=Path)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--memory-mb", type=int, default=4096)
    args = parser.parse_args()
    certificates = read_certificates(Path(__file__).resolve().parents[2])
    print("SOURCE_POSITIVES " + json.dumps(source_positives(
        args.binary, certificates, args.timeout, args.memory_mb), sort_keys=True), flush=True)
    print("ALL_LENGTH_DIFFERENTIAL " + json.dumps(compare_all_lengths(
        args.binary, args.baseline, certificates, args.timeout, args.memory_mb), sort_keys=True), flush=True)
    print("ALL MDD INTEGRATION CONTROLS PASSED")


if __name__ == "__main__":
    main()
