#!/usr/bin/env python3
"""Finite controls for center-only canonicalization of accepted certificates.

Run from any directory with Python 3; no third-party packages are needed.
Strip maximal matching neutral pairs from both centers, retain B/B2/u, and
compute the new v by actually stripping nextC at the canonical source.  The
unchanged neutral_band_search mirror checks all accepted edges and cycles.

These finite controls are not a mathematical proof.  Preservation is tested
on accepted inputs; no arbitrary-input iff is claimed.  A concrete malformed
chain/cycle of locally valid edges becomes accepted after normalization and
is printed as a counterexample to that stronger assertion.  The local chain
adapter follows A120Certificate's seam/edge recursion; complete cycles always
use mirror.cycleOK.  Explicit require checks also run under python -O.
"""

from collections import Counter
from itertools import product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror


KNOWN_BASES = {2, 4, 8, 11, 16, 17, 26, 32}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pad(base, amount, center):
    return [max(0, base - 1)] * amount + center + [max(0, base - 1)] * amount


def strip_center(base, center):
    """Return the core and maximal number of neutral pairs, using two indices."""
    neutral = max(0, base - 1)
    left, right = 0, len(center)
    while right - left >= 2 and center[left] == neutral and center[right - 1] == neutral:
        left += 1
        right -= 1
    return center[left:right], left


def strip_by_run_lengths(base, center):
    """Independent finite-control oracle from the two end-run lengths."""
    neutral = max(0, base - 1)
    leading = next((i for i, value in enumerate(center) if value != neutral), len(center))
    trailing = next((i for i, value in enumerate(reversed(center)) if value != neutral), len(center))
    depth = min(leading, trailing, len(center) // 2)
    return center[depth:len(center) - depth], depth


def canonical_edge(base, edge):
    """Compute the new trim from the actual successor, never from balance."""
    exterior, center, target_b, target_c, u, _ = edge
    core, _ = strip_center(base, center)
    target_core, _ = strip_center(base, target_c)
    _, new_v = strip_center(base, mirror.nextC(base, exterior, core))
    return exterior, core, target_b, target_core, u, new_v


def padded_edge(base, edge, source_padding, target_padding):
    exterior, center, target_b, target_c, u, v = edge
    new_v = v + source_padding - target_padding
    require(min(source_padding, target_padding, new_v) >= 0,
            "Padding schedule must have natural parameters and balanced trims")
    return (exterior, pad(base, source_padding, center), target_b,
            pad(base, target_padding, target_c), u, new_v)


def chain_ok(base, edges, exterior, center):
    """Adapter of A120Certificate.chainOK using the unchanged edge checker."""
    for edge in edges:
        if (edge[0], edge[1]) != (exterior, center) or not mirror.edgeOK(base, edge):
            return False
        exterior, center = edge[2:4]
    return True


def check_strip(counts, base, center):
    core, depth = strip_center(base, center)
    require((core, depth) == strip_by_run_lengths(base, center),
            f"Strip algorithms disagree: {(base, center)}")
    require(pad(base, depth, core) == center, "Strip reconstruction failed")
    require(strip_center(base, core) == (core, 0), "Core is not maximally stripped")
    require(len(core) + 2 * depth == len(center), "Strip length identity failed")
    if base >= 2:
        _, mirror_core, _, mirror_depth = mirror.trim(base, [], center)
        require((core, depth) == (mirror_core, mirror_depth), "Mirror center trim differs")
    counts["strip_words"] += 1
    counts["strip_nonzero_depth"] += depth > 0
    counts["strip_empty_words"] += not center
    counts["strip_nonsymmetric_words"] += center != center[::-1]


def check_edge(counts, base, edge, label):
    require(mirror.edgeOK(base, edge), f"Control edge is not accepted: {label}")
    exterior, center, target_b, target_c, u, v = edge
    core, depth = strip_center(base, center)
    target_core, target_depth = strip_center(base, target_c)
    actual_core, actual_depth = strip_center(base, mirror.nextC(base, exterior, core))
    normalized = canonical_edge(base, edge)
    require(normalized == (exterior, core, target_b, target_core, u, actual_depth),
            f"Canonical edge changed exterior data or did not use actual trim: {label}")
    require(actual_core == target_core, f"Actual successor has a different core: {label}")
    require(depth + actual_depth == v + target_depth, f"Depth balance failed: {label}")
    require(mirror.edgeOK(base, normalized), f"Canonical edge is not accepted: {label}")
    require(mirror.hyp(base, exterior, core), f"Canonical source lost Hyp: {label}")
    require(mirror.e1(base, exterior) == mirror.e1(base, normalized[0]) and
            mirror.e2(base, exterior, center) == mirror.e2(base, exterior, core) and
            mirror.gam(base, exterior, center) == mirror.gam(base, exterior, core),
            f"Canonicalization changed a carry or overflow: {label}")
    require(mirror.nextB(base, exterior, center) == mirror.nextB(base, exterior, core),
            f"Canonicalization changed the raw exterior successor: {label}")
    require(strip_center(base, core) == (core, 0) and
            strip_center(base, target_core) == (target_core, 0),
            f"A canonical center is not maximal: {label}")
    require(canonical_edge(base, normalized) == normalized, f"Edge is not idempotent: {label}")
    require(len(core) <= len(center) and len(target_core) <= len(target_c),
            f"A center grew under canonicalization: {label}")
    _, old_maximal_trim = strip_center(base, mirror.nextC(base, exterior, center))
    require(v <= old_maximal_trim, f"Accepted edge overtrims its successor: {label}")
    counts["edge_controls"] += 1
    counts["edge_nonmaximal_input_trim"] += v < old_maximal_trim
    counts["edge_trim_changed"] += actual_depth != v
    counts["edge_source_narrowed"] += len(core) < len(center)
    counts["edge_empty_exterior"] += not exterior
    counts["edge_nonsymmetric_center"] += center != center[::-1]
    counts["edge_trim_gt_one"] += v > 1
    return normalized


def totals(base, edges):
    return (sum(mirror.gam(base, edge[0], edge[1]) for edge in edges),
            sum(edge[4] for edge in edges), sum(edge[5] for edge in edges),
            sum(edge[4] + edge[5] for edge in edges))


def check_cycle(counts, base, edges, label):
    require(bool(edges), "Expected a nonempty control cycle")
    exterior, center = edges[0][:2]
    require(mirror.cycleOK(base, edges, exterior, center), f"Input cycle failed: {label}")
    normalized = [check_edge(counts, base, edge, (label, i)) for i, edge in enumerate(edges)]
    core, _ = strip_center(base, center)
    require(mirror.cycleOK(base, normalized, exterior, core), f"Canonical cycle failed: {label}")
    require(chain_ok(base, normalized, exterior, core), f"Canonical chain failed: {label}")
    require(len(normalized) == len(edges), f"Listed edge count changed: {label}")
    require([(edge[0], edge[2], edge[4]) for edge in normalized] ==
            [(edge[0], edge[2], edge[4]) for edge in edges],
            f"A cycle exterior or exterior trim changed: {label}")
    require(totals(base, normalized) == totals(base, edges),
            f"Cycle overflow/u/v/gain totals changed: {label}")
    before_widths = [2 * len(edge[0]) + len(edge[1]) for edge in edges]
    after_widths = [2 * len(edge[0]) + len(edge[1]) for edge in normalized]
    require(all(after <= before for before, after in zip(before_widths, after_widths)) and
            max(after_widths) <= max(before_widths), f"Cycle interface width increased: {label}")
    require([canonical_edge(base, edge) for edge in normalized] == normalized,
            f"Cycle normalization is not idempotent: {label}")
    counts["cycle_controls"] += 1
    counts["cycle_listed_edges"] += len(edges)
    counts["cycle_strictly_narrowed"] += sum(after_widths) < sum(before_widths)


def word_controls(counts):
    # Includes empty words, odd/even all-neutral words, nonsymmetric words,
    # invalid bases, and out-of-bound coefficients; only stripping is tested.
    for base in (0, 1, 2, 3, 10):
        neutral = max(0, base - 1)
        alphabet = sorted({0, neutral, 2 * neutral + 1})
        for length in range(7):
            for word in product(alphabet, repeat=length):
                check_strip(counts, base, list(word))


def certificate_controls(counts, controls):
    for base, edges in controls:
        counts["known_bases"] += 1
        counts["known_edges"] += len(edges)
        check_cycle(counts, base, edges, ("original", base))
        for amount in (1, 3):
            padded = [padded_edge(base, edge, amount, amount) for edge in edges]
            check_cycle(counts, base, padded, ("uniform", base, amount))

        gain_index = next(i for i, edge in enumerate(edges) if edge[5] > 0)
        for floor in (0, 2):
            phases = [floor] * len(edges)
            phases[(gain_index + 1) % len(edges)] += 1
            require(len(set(phases)) > 1, "Expected phase-dependent padding")
            padded = [padded_edge(base, edge, phases[i], phases[(i + 1) % len(edges)])
                      for i, edge in enumerate(edges)]
            check_cycle(counts, base, padded, ("phase", base, floor))
            counts["cycle_phase_dependent"] += 1

        # Start with depth two, drop it, then repay it from later center gains.
        # Three copies give accepted closed controls containing a trim > 1.
        padded = []
        amount = 2
        for i, edge in enumerate(edges * 3):
            target_amount = 0 if i == 0 else min(2, amount + edge[5])
            padded.append(padded_edge(base, edge, amount, target_amount))
            amount = target_amount
        require(amount == 2 and padded[0][5] > 1, "Phase schedule did not close")
        check_cycle(counts, base, padded, ("phase-three-copies", base))
        counts["cycle_phase_dependent"] += 1


def directed_edge_controls(counts):
    for base, exterior, center in ((2, [], [2]), (2, [], [0, 2]),
                                  (2, [2], [0, 1]), (3, [3], [0, 2]),
                                  (10, [], [0, 10]), (10, [10], [0, 9])):
        seed = mirror.step(base, exterior, center)
        require(seed is not None, "Directed source must satisfy Hyp")
        for source_padding in (0, 1, 3):
            for target_padding in range(source_padding + seed[5] + 1):
                edge = padded_edge(base, seed, source_padding, target_padding)
                check_edge(counts, base, edge, ("directed", base, source_padding, target_padding))
                counts["directed_edge_controls"] += 1


def repaired_seam_witness(counts, controls):
    base = 2
    edges = next(edges for b, edges in controls if b == base)
    malformed = [padded_edge(base, edges[0], 1, 1)] + edges[1:]
    exterior, center = malformed[0][:2]
    require(all(mirror.edgeOK(base, edge) for edge in malformed),
            "Counterexample requires every original local edge to be accepted")
    before_chain = chain_ok(base, malformed, exterior, center)
    before_cycle = mirror.cycleOK(base, malformed, exterior, center)
    require(before_chain is False and before_cycle is False, "Malformed input was accepted")
    normalized = [check_edge(counts, base, edge, ("witness", i))
                  for i, edge in enumerate(malformed)]
    core, _ = strip_center(base, center)
    after_chain = chain_ok(base, normalized, exterior, core)
    after_cycle = mirror.cycleOK(base, normalized, exterior, core)
    require(after_chain is True and after_cycle is True and normalized == edges,
            "Normalization did not repair the explicit base-two counterexample")
    seam_target, seam_source = malformed[0][3], malformed[1][1]
    require(seam_target != seam_source and
            strip_center(base, seam_target)[0] == strip_center(base, seam_source)[0],
            "Counterexample must isolate a seam repaired by center stripping")
    counts["repaired_seam_witnesses"] += 1
    return (f"NO_ARBITRARY_IFF_WITNESS base=2 changed_edge=0 padding=1 "
            f"locally_accepted_edges={len(malformed)} "
            f"before_chain={before_chain} after_chain={after_chain} "
            f"before_cycle={before_cycle} after_cycle={after_cycle} "
            f"seam_target={seam_target} seam_source={seam_source} canonical_center={normalized[0][3]}")


def main():
    controls = mirror._lean_certs()
    require(len(controls) == 8 and {base for base, _ in controls} == KNOWN_BASES,
            "Expected exactly the eight existing Lean-source certificate bases")
    require(all(edges for _, edges in controls), "An existing certificate is empty")
    counts = Counter()
    word_controls(counts)
    certificate_controls(counts, controls)
    directed_edge_controls(counts)
    witness = repaired_seam_witness(counts, controls)
    for key in ("strip_nonzero_depth", "strip_empty_words", "strip_nonsymmetric_words",
                "edge_nonmaximal_input_trim", "edge_trim_changed", "edge_source_narrowed",
                "edge_empty_exterior", "edge_nonsymmetric_center", "edge_trim_gt_one",
                "cycle_strictly_narrowed", "cycle_phase_dependent", "repaired_seam_witnesses"):
        require(counts[key] > 0, f"Missing required coverage: {key}")
    print("CENTER CANONICALIZATION FINITE CONTROLS PASS (not a mathematical proof)")
    for prefix in ("known_", "strip_", "edge_", "cycle_", "directed_", "repaired_"):
        print(" ".join(f"{key}={counts[key]}" for key in sorted(counts) if key.startswith(prefix)))
    print(witness)


if __name__ == "__main__":
    main()
