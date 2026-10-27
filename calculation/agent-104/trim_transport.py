#!/usr/bin/env python3
"""Replay the additive-offset center-trim transport used by Agent 104's Lean proof.

Credit Agents 7/107 for the mathematical padding/trim-transport theorem.  This
audits the simple, nonoptimal construction a_i=sum(v[:i])+sum(w[i:]), not their
optimal-padding algorithm.  Equal natural totals K imply 0<=a_i<=2K, so padding
adds at most 4K center coefficients.  B, B2 and every exterior trim u are fixed.

Fixtures are read from existing Lean certificates by the exact repository
mirror; no certificate or normalization implementation is copied here.
Default tests cover all eight source bases, every distinct cyclic rotation,
and every natural target schedule for one and two repetitions (K=1,2).
Run with python3 -O as well: every check remains active without assert.
"""

import argparse
import importlib.util
from itertools import product
import json
from math import comb
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_BASES = {2, 4, 8, 11, 16, 17, 26, 32}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def naturals(values, name):
    require(isinstance(values, (tuple, list)), name + " must be a list or tuple")
    require(all(type(value) is int and value >= 0 for value in values),
            name + " must contain natural integers (excluding bool)")
    return tuple(values)


def additive_offsets(source_trims, target_trims):
    """Return a_0,...,a_P, including the equal initial/final offsets K."""
    source = naturals(source_trims, "source trims")
    target = naturals(target_trims, "target trims")
    require(len(source) == len(target), "trim-schedule lengths differ")
    total = sum(source)
    require(total == sum(target), "trim-schedule totals differ")
    prefix, suffix = 0, total
    offsets = []
    for old, new in zip(source, target):
        offsets.append(prefix + suffix)
        prefix += old
        suffix -= new
    offsets.append(prefix + suffix)
    require(offsets[0] == offsets[-1] == total, "offset endpoints do not agree")
    require(all(0 <= a <= 2 * total for a in offsets), "offset exceeds 2K")
    require(all(offsets[i] + old == new + offsets[i + 1]
                for i, (old, new) in enumerate(zip(source, target))),
            "additive transport equation fails")
    return offsets


def load_mirror():
    path = ROOT / "calculation/neutral_band_search.py"
    spec = importlib.util.spec_from_file_location("a104_transport_exact_mirror", path)
    require(spec is not None and spec.loader is not None, "cannot load exact mirror")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_edges(mirror, base, edges):
    require(type(base) is int and base >= 2, "base must be a natural integer >=2")
    require(isinstance(edges, (list, tuple)) and len(edges) > 0,
            "source certificate must be a nonempty list or tuple")
    copied = []
    for edge in edges:
        require(isinstance(edge, (list, tuple)) and len(edge) == 6,
                "source edge must have six fields")
        words = [list(naturals(word, "coefficient word")) for word in edge[:4]]
        u, v = naturals(edge[4:], "source edge trims")
        copied.append((*words, u, v))
    require(mirror.cycleOK(base, copied, copied[0][0], copied[0][1]),
            "source certificate does not pass the exact mirror")
    return copied


def transport(mirror, base, edges, target_trims):
    source = source_edges(mirror, base, edges)
    target = naturals(target_trims, "target trims")
    offsets = additive_offsets([edge[5] for edge in source], target)
    total = sum(target)
    h = base - 1
    padded = lambda a, center: [h] * a + center + [h] * a
    result = []
    for i, (B, C, B2, C2, u, _) in enumerate(source):
        new_C = padded(offsets[i], C)
        new_C2 = padded(offsets[i + 1], C2)
        edge = (B, new_C, B2, new_C2, u, target[i])
        require(edge[0] == source[i][0] and edge[2] == source[i][2]
                and edge[4] == source[i][4], "exterior data changed")
        require(len(new_C) - len(C) == 2 * offsets[i] <= 4 * total,
                "source center width increase exceeds 4K")
        require(len(new_C2) - len(C2) == 2 * offsets[i + 1] <= 4 * total,
                "destination center width increase exceeds 4K")
        require((mirror.e2(base, B, new_C), mirror.gam(base, B, new_C))
                == (mirror.e2(base, B, C), mirror.gam(base, B, C)),
                "center carry or overflow stream changed")
        require(mirror.edgeOK(base, edge), "transported edge fails exact replay")
        result.append(edge)
    require(mirror.cycleOK(base, result, result[0][0], result[0][1]),
            "transported cycle fails exact replay")
    require(sum(edge[4] + edge[5] for edge in result)
            == sum(edge[4] + edge[5] for edge in source), "cycle gain changed")
    return result, offsets


def schedules(total, length):
    """Every weak composition, including entries greater than one."""
    if length == 0:
        if total == 0:
            yield ()
    elif length == 1:
        yield (total,)
    else:
        for head in range(total + 1):
            for tail in schedules(total - head, length - 1):
                yield (head,) + tail


def distinct_rotations(edges):
    seen = set()
    for i in range(len(edges)):
        rotated = edges[i:] + edges[:i]
        key = tuple((*(tuple(word) for word in edge[:4]), *edge[4:])
                    for edge in rotated)
        if key not in seen:
            seen.add(key)
            yield rotated


def arithmetic_controls():
    count = 0
    require(additive_offsets([], []) == [0], "empty arithmetic schedule fails")
    count += 1
    for length in range(1, 5):
        for total in range(4):
            choices = tuple(schedules(total, length))
            require(len(set(choices)) == len(choices) == comb(length + total - 1, total),
                    "arithmetic schedule coverage mismatch")
            for source, target in product(choices, repeat=2):
                offsets = additive_offsets(source, target)
                # A separate direct-sum formula checks the running-sum implementation.
                expected = [sum(source[:i]) + sum(target[i:]) for i in range(length + 1)]
                require(offsets == expected, "offset formula mismatch")
                count += 1
    return count


def rejection_controls(mirror, fixture):
    base, edges = fixture
    original = [edge[5] for edge in edges]
    total, period = sum(original), len(original)
    bad_u = [(*edge[:4], -1, edge[5]) if i == 0 else edge
             for i, edge in enumerate(edges)]
    bad_v = [(*edge[:5], -1) if i == 0 else edge for i, edge in enumerate(edges)]
    tests = [
        ("short arithmetic schedule", lambda: additive_offsets([1], [])),
        ("long arithmetic schedule", lambda: additive_offsets([], [0])),
        ("different arithmetic totals", lambda: additive_offsets([1, 0], [0, 0])),
        ("negative source count", lambda: additive_offsets([-1, 2], [1, 0])),
        ("negative target count", lambda: additive_offsets([1, 0], [-1, 2])),
        ("boolean source count", lambda: additive_offsets([True], [1])),
        ("boolean target count", lambda: additive_offsets([1], [True])),
        ("fractional source count", lambda: additive_offsets([1.0], [1])),
        ("string target count", lambda: additive_offsets([1], ["1"])),
        ("nonsequence source", lambda: additive_offsets(None, [])),
        ("nonsequence target", lambda: additive_offsets([], None)),
        ("short certificate schedule", lambda: transport(mirror, base, edges, original[:-1])),
        ("long certificate schedule", lambda: transport(mirror, base, edges, original + [0])),
        ("different certificate totals", lambda: transport(mirror, base, edges, [total + 1] + [0]*(period - 1))),
        ("negative certificate schedule", lambda: transport(mirror, base, edges, [-1, total + 1] + [0]*(period - 2))),
        ("negative source exterior trim", lambda: transport(mirror, base, bad_u, original)),
        ("negative source center trim", lambda: transport(mirror, base, bad_v, original)),
        ("empty certificate", lambda: transport(mirror, base, [], [])),
        ("malformed source edge", lambda: transport(mirror, base, [edges[0][:5]], [0])),
        ("invalid base", lambda: transport(mirror, 1, edges, original)),
    ]
    for name, check in tests:
        try:
            check()
        except RuntimeError:
            continue
        raise RuntimeError("malformed input was accepted: " + name)
    return len(tests)


def run(repetitions):
    mirror = load_mirror()
    fixtures = sorted(mirror._lean_certs())
    require(len(fixtures) == 8 and {base for base, _ in fixtures} == EXPECTED_BASES,
            "known source certificate set changed")
    require(sum(len(edges) for _, edges in fixtures) == 56, "source edge count changed")
    arithmetic = arithmetic_controls()
    rejected = rejection_controls(mirror, fixtures[0])
    full_cases = return_controls = edge_replays = max_increase = 0
    for base, original in fixtures:
        source_edges(mirror, base, original)
        require(sum(edge[5] for edge in original) == 1, "source center trim budget changed")
        for repeat in repetitions:
            expanded = original * repeat
            period, total = len(expanded), repeat
            rotations = list(distinct_rotations(expanded))
            expected_schedules = comb(period + total - 1, total)
            case_count = return_count = 0
            for edges in rotations:
                seen_schedules = set()
                for target in schedules(total, period):
                    require(target not in seen_schedules, "duplicate target schedule")
                    seen_schedules.add(target)
                    result, offsets = transport(mirror, base, edges, target)
                    max_increase = max(max_increase, 2 * max(offsets))
                    case_count += 1
                    edge_replays += period
                    # A concentrated K=2 output supplies a valid source trim >1.
                    # Restore the original trim schedule with further padding.
                    if total > 1 and target == (total,) + (0,)*(period - 1):
                        restored, again = transport(mirror, base, result,
                                                    [edge[5] for edge in edges])
                        require([edge[5] for edge in restored] == [edge[5] for edge in edges],
                                "return-schedule control changed the target")
                        max_increase = max(max_increase, 2 * max(again))
                        return_count += 1
                        edge_replays += period
                require(len(seen_schedules) == expected_schedules,
                        "incomplete natural target-schedule coverage")
            require(case_count == len(rotations) * expected_schedules,
                    "incomplete rotation coverage")
            full_cases += case_count
            return_controls += return_count
            print("FIXTURE " + json.dumps({"base": base, "repetitions": repeat,
                  "P": period, "K": total, "distinct_rotations": len(rotations),
                  "schedules_per_rotation": expected_schedules, "cycle_replays": case_count,
                  "return_schedule_controls": return_count}, sort_keys=True), flush=True)
    print("TRANSPORT_PASS " + json.dumps({"status": "COMPUTED", "bases": len(fixtures),
          "source_edges": 56, "arithmetic_pairs": arithmetic,
          "malformed_inputs_rejected": rejected, "complete_schedule_replays": full_cases,
          "return_schedule_controls": return_controls, "total_cycle_replays": full_cases + return_controls,
          "transformed_edge_replays": edge_replays, "max_added_center_coefficients": max_increase,
          "optimized_python": not __debug__}, sort_keys=True), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repetitions", nargs="+", type=int, choices=(1, 2), default=[1, 2])
    args = parser.parse_args()
    run(sorted(set(args.repetitions)))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print("CHECK FAILED: " + str(error), file=sys.stderr)
        sys.exit(1)
