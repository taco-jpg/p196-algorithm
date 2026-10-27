#!/usr/bin/env python3
"""Independent whole-center return graphs for every temporal repetition.

At a fixed initial width and balanced unit length ledger, one complete driver
unit is a partial FUNCTION on a finite set of symmetric centers. A cycle in
this graph is exactly a center return after some positive number of units.
This oracle therefore checks all repetition counts, not just bounded k, while
retaining its explicitly bounded coefficient-width scope.
"""
from __future__ import annotations

import argparse
from collections import deque
import itertools
import json
from pathlib import Path
import re

from center_controls import alternating_trim, center_step, finite_cases, require
from long_center import run


def bits(word):
    return "".join(map(str, word))


def return_graph(base, e, g, v, width):
    require(width >= 1 and len(e) == len(g) == len(v) and sum(g) == 2 * sum(v),
            "invalid fixed-unit return graph")
    states = []
    for half in itertools.product(range(2 * base - 1), repeat=(width + 1) // 2):
        states.append(half + half[:width // 2][::-1])
    index = {state: i for i, state in enumerate(states)}
    successors = [-1] * len(states)
    indegree = [0] * len(states)
    edges = 0
    for i, source in enumerate(states):
        current = source
        for ee, gg, vv in zip(e, g, v):
            current = center_step(base, current, ee, gg, vv)
            if current is None:
                break
        if current is not None:
            require(current in index, "unit image escaped the proved fixed-width universe")
            j = index[current]
            successors[i] = j
            indegree[j] += 1
            edges += 1
    queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
    removed = [False] * len(states)
    while queue:
        i = queue.popleft()
        removed[i] = True
        j = successors[i]
        if j >= 0:
            indegree[j] -= 1
            if indegree[j] == 0:
                queue.append(j)
    residual = sum(not x for x in removed)
    lengths = []
    seen = set()
    replayed = 0
    for start in range(len(states)):
        if removed[start] or start in seen:
            continue
        walk = []
        current = start
        while current not in seen:
            require(current >= 0 and not removed[current], "functional cycle reached a dead state")
            seen.add(current)
            walk.append(current)
            current = successors[current]
        require(current == start, "functional residual contains an unpeeled transient")
        lengths.append(len(walk))
        for a, b in zip(walk, walk[1:] + walk[:1]):
            center = states[a]
            for ee, gg, vv in zip(e, g, v):
                center = center_step(base, center, ee, gg, vv)
                require(center is not None, "extracted cyclic edge failed integer replay")
                replayed += 1
            require(center == states[b], "extracted return circuit failed closure")
    require(sum(lengths) == residual, "functional graph cycle accounting mismatch")
    return {"states": len(states), "edges": edges, "cyclic_states": residual,
            "cycles": len(lengths), "largest_repetition": max(lengths, default=0),
            "nontrivial_cycles": sum(x > 1 for x in lengths), "replayed_edges": replayed}


def cases():
    for base, e, g, v, width in finite_cases():
        if len(e) <= 6:
            yield base, e, g, v, min(width, 4)
    for source_e, source_g, copies, width in (("10100110011", "11100010000", 1, 6),
                                             ("101010010101", "100010001000", 2, 4)):
        e, g = tuple(map(int, source_e)) * copies, tuple(map(int, source_g)) * copies
        for level in (0, 1):
            yield 10, e, g, alternating_trim(g, level), width


def compare(binary=None):
    totals = {"patterns": 0, "fixed_width_all_k_graphs": 0, "center_states": 0,
              "return_edges": 0, "cyclic_states": 0, "cycles": 0,
              "nontrivial_cycles": 0, "replayed_edges": 0,
              "positive_widths": 0, "negative_widths": 0,
              "largest_repetition": 0, "engine_comparisons": 0}
    for base, e, g, v, maximum in cases():
        expected = set()
        for width in range(1, maximum + 1):
            result = return_graph(base, e, g, v, width)
            totals["fixed_width_all_k_graphs"] += 1
            totals["center_states"] += result["states"]
            totals["return_edges"] += result["edges"]
            for key in ("cyclic_states", "cycles", "nontrivial_cycles", "replayed_edges"):
                totals[key] += result[key]
            totals["largest_repetition"] = max(totals["largest_repetition"],
                                                result["largest_repetition"])
            if result["cyclic_states"]:
                expected.add(width)
                totals["positive_widths"] += 1
            else:
                totals["negative_widths"] += 1
        if binary:
            completed = run(binary, base, bits(e), bits(g), 1, maximum, bits(v),
                            cap=200000, timeout=30, memory_mb=4096)
            require(completed.returncode == 0, "regular engine error: " + completed.stderr[-2000:])
            require(not re.search(r"UNDECIDED|CAPPED|NOPERIOD|UNSUPPORTED", completed.stdout + completed.stderr),
                    "incomplete regular computation is not a negative")
            require(re.search(r"^DONE .*status=(?:hit|none)(?: |$)", completed.stdout, re.M),
                    "missing regular engine completion record")
            actual = {int(x) for x in re.findall(r"^FEASIBLE .*?\bm0=(\d+)", completed.stdout, re.M)}
            require(actual == expected,
                    f"all-k functional-graph mismatch b={base} e={bits(e)} g={bits(g)} v={bits(v)}: "
                    f"expected={sorted(expected)} actual={sorted(actual)}")
            totals["engine_comparisons"] += maximum
        totals["patterns"] += 1
    return totals


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path)
    args = parser.parse_args()
    print("ALL_K_RETURN_GRAPH_CONTROLS " + json.dumps(compare(args.binary), sort_keys=True))
