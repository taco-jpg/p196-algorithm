#!/usr/bin/env python3
"""Finite controls for common-center padding/unpadding equivalences.

Run from any directory with Python 3; no third-party packages are needed.
Both sides of every iff are evaluated using the unchanged neutral_band_search
mirror.  The mirror has no chainOK entry point, so chain_ok below is a small
adapter for the seam/edge recursion in A120Certificate.  Complete cycles use
mirror.cycleOK, including closure, nonemptiness, and the gain condition.

The deterministic domains include rejected inputs, independently chosen edge
targets, and the eight existing Lean-source certificates.  These are finite
controls, not a mathematical proof or a search for new certificates.  Explicit
require calls remain active under python -O.
"""

from collections import Counter
from itertools import product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror


PADDINGS = (0, 1, 2, 4)
EDGE_PADDINGS = (0, 1, 3)
KNOWN_BASES = {2, 4, 8, 11, 16, 17, 26, 32}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pad(base, amount, center):
    # Nat subtraction agrees with the Lean definition even at base zero.
    neutral = max(0, base - 1)
    return [neutral] * amount + center + [neutral] * amount


def transport(base, edge, source_padding, target_padding, new_trim):
    exterior, center, target_b, target_c, u, v = edge
    require(min(source_padding, target_padding, new_trim) >= 0,
            "Transport parameters must be natural numbers")
    require(source_padding + v == new_trim + target_padding,
            "Unbalanced edge transport")
    return (exterior, pad(base, source_padding, center), target_b,
            pad(base, target_padding, target_c), u, new_trim)


def chain_ok(base, edges, exterior, center):
    """Adapter of A120Certificate.chainOK using the unchanged edge checker."""
    for edge in edges:
        if (edge[0], edge[1]) != (exterior, center):
            return False
        if not mirror.edgeOK(base, edge):
            return False
        exterior, center = edge[2:4]
    return True


def record_iff(counts, family, original, transformed, context):
    require(type(original) is bool and type(transformed) is bool,
            f"Non-Boolean {family} result: {context}")
    require(original == transformed,
            f"{family} iff failed: {context}; {original} != {transformed}")
    counts[f"{family}_pairs"] += 1
    counts[f"{family}_{'accepted' if original else 'rejected'}"] += 1


def words(alphabet, max_length):
    return [list(word) for length in range(max_length + 1)
            for word in product(alphabet, repeat=length)]


def check_hyp(counts, base, exterior, center):
    original = mirror.hyp(base, exterior, center)
    for amount in PADDINGS:
        actual = mirror.hyp(base, exterior, pad(base, amount, center))
        record_iff(counts, "hyp", original, actual,
                   (base, exterior, center, amount))
        counts["hyp_zero_padding"] += amount == 0
        counts["hyp_invalid_base"] += base < 2
        counts["hyp_empty_exterior"] += not exterior
        counts["hyp_empty_center"] += not center
        counts["hyp_nonsymmetric_center"] += center != center[::-1]


def check_edge(counts, base, edge, group, expected=None):
    original = mirror.edgeOK(base, edge)
    if expected is not None:
        require(original is expected, f"Unexpected {group} edge result: {(base, edge)}")
    for source_padding in EDGE_PADDINGS:
        for target_padding in range(source_padding + edge[5] + 1):
            new_trim = source_padding + edge[5] - target_padding
            padded = transport(base, edge, source_padding, target_padding, new_trim)
            actual = mirror.edgeOK(base, padded)
            record_iff(counts, "edge", original, actual,
                       (group, base, edge, source_padding, target_padding, new_trim))
            counts[f"edge_{group}_pairs"] += 1
            counts[f"edge_{group}_{'accepted' if original else 'rejected'}"] += 1
            counts["edge_source_zero_padding"] += source_padding == 0
            counts["edge_target_zero_padding"] += target_padding == 0
            if original:
                counts["edge_accepted_original_trim_gt_one"] += edge[5] > 1
                counts["edge_accepted_new_trim_gt_one"] += new_trim > 1


def check_walk(counts, base, edges, exterior, center, label,
               expected_chain=None, expected_cycle=None):
    original_chain = chain_ok(base, edges, exterior, center)
    original_cycle = mirror.cycleOK(base, edges, exterior, center)
    if expected_chain is not None:
        require(original_chain is expected_chain, f"Unexpected chain result: {label}")
    if expected_cycle is not None:
        require(original_cycle is expected_cycle, f"Unexpected cycle result: {label}")
    for amount in PADDINGS:
        padded = [transport(base, edge, amount, amount, edge[5]) for edge in edges]
        padded_center = pad(base, amount, center)
        actual_chain = chain_ok(base, padded, exterior, padded_center)
        actual_cycle = mirror.cycleOK(base, padded, exterior, padded_center)
        record_iff(counts, "chain", original_chain, actual_chain, (label, amount))
        record_iff(counts, "cycle", original_cycle, actual_cycle, (label, amount))
        counts["walk_zero_padding"] += amount == 0
        counts["walk_empty"] += not edges
        counts["walk_open_accepted_chain"] += original_chain and not original_cycle and bool(edges)
        if original_chain:
            require(sum(edge[4] + edge[5] for edge in edges) ==
                    sum(edge[4] + edge[5] for edge in padded),
                    f"Uniform padding changed gain: {label}")
            require(sum(mirror.gam(base, edge[0], edge[1]) for edge in edges) ==
                    sum(mirror.gam(base, edge[0], edge[1]) for edge in padded),
                    f"Uniform padding changed overflow sum: {label}")
        if original_cycle and any(edge[5] > 1 for edge in edges):
            counts["cycle_accepted_trim_gt_one"] += 1


def changed(word):
    """Change one coefficient, keeping the length whenever the word is nonempty."""
    return [word[0] + 1] + word[1:] if word else [0]


def bad_edges(base, edge):
    exterior, center, target_b, target_c, u, v = edge
    return [
        (exterior, center, changed(target_b), target_c, u, v),
        (exterior, center, target_b, changed(target_c), u, v),
        (exterior, center, target_b, target_c, u + 1, v),
        (exterior, center, target_b, target_c, u, v + 1),
        ([0] + exterior, center, target_b, target_c, u, v),
        (exterior, center + [2 * (base - 1) + 1], target_b, target_c, u, v),
    ]


def bounded_controls(counts):
    # All words of length at most two, including an out-of-range coefficient.
    # Base ten uses explicit boundary coefficients instead of a large word box.
    for base in (0, 1, 2, 3, 10):
        alphabet = range(2 * max(0, base - 1) + 2) if base < 10 else (0, 1, 8, 9, 10, 18, 19)
        domain = words(alphabet, 2)
        for exterior, center in product(domain, repeat=2):
            check_hyp(counts, base, exterior, center)

    # Sources and targets are chosen independently, not extracted from nextB/C.
    # Every u,v in this finite set is tried, including center trim three.
    for base in (0, 1, 2, 3):
        domain = words(range(2 * max(0, base - 1) + 2), 1)
        for exterior, center, target_b, target_c in product(domain, repeat=4):
            for u, v in product((0, 1, 3), repeat=2):
                check_edge(counts, base, (exterior, center, target_b, target_c, u, v),
                           "independent")

    for base in (0, 1, 2, 10):
        for exterior, center in product(([], [0], [1, 0]), repeat=2):
            check_walk(counts, base, [], exterior, center, ("empty", base), True, False)
        bad = ([0], [], [], [], 0, 3)
        check_edge(counts, base, bad, "invalid", False)
        check_walk(counts, base, [bad], bad[0], bad[1], ("invalid", base), False, False)


def directed_controls(counts, controls):
    seeds = [(base, edge) for base, edges in controls for edge in edges]
    # Empty exterior and nonsymmetric centers are allowed when Hyp holds.
    for base, exterior, center in ((2, [], [2]), (2, [], [0, 2]),
                                  (2, [2], [0, 1]), (3, [3], [0, 2]),
                                  (10, [], [0, 10]), (10, [10], [0, 9])):
        edge = mirror.step(base, exterior, center)
        require(edge is not None, "A directed positive source no longer satisfies Hyp")
        seeds.append((base, edge))
        check_walk(counts, base, [edge], exterior, center, ("directed", base, edge), True)
    for base, edge in seeds:
        check_hyp(counts, base, edge[0], edge[1])
        for amount in (0, 2, 4):
            # Put extra neutral layers in the source while retaining the target;
            # this gives accepted original edges with trim two or more.
            expanded = transport(base, edge, amount, 0, edge[5] + amount)
            check_edge(counts, base, expanded, "positive", True)
            for bad in bad_edges(base, expanded):
                check_edge(counts, base, bad, "modified", False)


def certificate_controls(counts, controls):
    for base, edges in controls:
        exterior, center = edges[0][:2]
        require(mirror.cycleOK(base, edges, exterior, center),
                f"Existing base-{base} control failed the unchanged mirror")
        counts["known_bases"] += 1
        counts["known_edges"] += len(edges)
        for offset in range(len(edges)):
            rotated = edges[offset:] + edges[:offset]
            initial_b, initial_c = rotated[0][:2]
            for length in range(len(rotated) + 1):
                check_walk(counts, base, rotated[:length], initial_b, initial_c,
                           ("prefix", base, offset, length), True,
                           True if length == len(rotated) else None)

        # Every edge in this malformed chain is individually accepted.  The
        # failure is the repeated first edge's seam, not its local edge check.
        require(edges[0][:2] != edges[0][2:4], "Expected a non-self-loop first edge")
        broken_seam = [edges[0]] + edges
        require(all(mirror.edgeOK(base, edge) for edge in broken_seam),
                "Malformed-seam control contains an invalid local edge")
        check_walk(counts, base, broken_seam, exterior, center,
                   ("seam", base), False, False)
        counts["malformed_seam_controls"] += 1
        check_walk(counts, base, edges, changed(exterior), center,
                   ("initial-exterior", base), False, False)
        check_walk(counts, base, edges, exterior, changed(center),
                   ("initial-center", base), False, False)
        for index, bad in enumerate(bad_edges(base, edges[0])):
            check_walk(counts, base, [bad] + edges[1:], exterior, center,
                       ("modified-certificate", base, index), False, False)

        # A valid open chain has a larger initial center and the original end.
        opened = [transport(base, edges[0], 4, 0, edges[0][5] + 4)] + edges[1:]
        check_walk(counts, base, opened, exterior, pad(base, 4, center),
                   ("open-trim", base), True, False)

        # Three copies supply enough center gain to repay a drop of two layers.
        # The first edge trims at least two; the final padded state closes.
        closed = []
        amount = 2
        for index, edge in enumerate(edges * 3):
            target_amount = 0 if index == 0 else min(2, amount + edge[5])
            closed.append(transport(base, edge, amount, target_amount,
                                    amount + edge[5] - target_amount))
            amount = target_amount
        require(amount == 2 and closed[0][5] > 1,
                "Failed to construct the positive closed trim>1 control")
        check_walk(counts, base, closed, exterior, pad(base, 2, center),
                   ("closed-trim", base), True, True)

    exterior, center = controls[0][1][0][:2]
    for base in (0, 1):
        check_walk(counts, base, controls[0][1], exterior, center,
                   ("invalid-certificate-base", base), False, False)


def main():
    controls = mirror._lean_certs()
    require(len(controls) == 8 and {base for base, _ in controls} == KNOWN_BASES,
            "Expected exactly the eight existing Lean-source certificate bases")
    require(all(edges for _, edges in controls), "An existing certificate is empty")
    counts = Counter()
    bounded_controls(counts)
    directed_controls(counts, controls)
    certificate_controls(counts, controls)
    for family in ("hyp", "edge", "chain", "cycle", "edge_independent"):
        require(counts[f"{family}_accepted"] > 0 and counts[f"{family}_rejected"] > 0,
                f"Missing positive or negative coverage for {family}")
    for key in ("hyp_zero_padding", "hyp_invalid_base", "hyp_empty_exterior",
                "hyp_empty_center", "hyp_nonsymmetric_center", "edge_source_zero_padding",
                "edge_target_zero_padding", "edge_accepted_original_trim_gt_one",
                "edge_accepted_new_trim_gt_one", "walk_zero_padding", "walk_empty",
                "walk_open_accepted_chain", "cycle_accepted_trim_gt_one"):
        require(counts[key] > 0, f"Missing required coverage: {key}")
    require(counts["malformed_seam_controls"] == 8, "Missing malformed-seam controls")
    print("UNPADDING FINITE CONTROLS PASS (not a mathematical proof)")
    for prefix in ("known_", "hyp_", "edge_", "chain_", "cycle_", "walk_", "malformed_"):
        print(" ".join(f"{key}={counts[key]}" for key in sorted(counts) if key.startswith(prefix)))


if __name__ == "__main__":
    main()
