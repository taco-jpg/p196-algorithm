#!/usr/bin/env python3
"""COMPUTED controls for padding every exterior to a common width M.

Run from the repository root, normally and with optimized Python:
    python3 calculation/agent-114/uniform_exterior_controls.py
    python3 -O calculation/agent-114/uniform_exterior_controls.py

The earlier Agent114 controls supply credited whole-integer normalization,
literal chain checks, and padding/canonicalization fixture utilities. This
file constructs fixed-width edges directly and checks the raw length law
against independent arithmetic, without reading Agent119's Lean proof.
Agent7's normalization and Agent107's retiming arguments retain attribution.
The bounded computations are regressions, not a new search or certificate.
"""

from collections import Counter
from dataclasses import replace
import importlib.util
from itertools import product
from pathlib import Path
import json
import sys

sys.dont_write_bytecode = True
import exterior_padding_controls as arithmetic
import exterior_cycle_controls as chains
import exterior_canonical_controls as canonical

Edge = arithmetic.Edge
require = arithmetic.require
natural = arithmetic.natural
natural_word = arithmetic.natural_word


def at_width(base, word, width):
    if not natural(base) or base < 2 or not natural(width) or not natural_word(word):
        raise ValueError("natural width/word and base >= 2 required")
    if len(word) > width:
        raise ValueError("requested width is smaller than the exterior")
    return tuple(word) + (base - 1,) * (width - len(word))


def uniform_edge(base, edge, width):
    """Fail closed on undersized widths, malformed fields, or rejected edges."""
    if not chains.edge_shape(edge):
        raise ValueError("natural edge fields required")
    B = at_width(base, edge.B, width)
    B2 = at_width(base, edge.B2, width)
    if not arithmetic.edge_ok(base, edge):
        raise ValueError("original edge must be accepted")
    overflow = arithmetic.state(base, edge.B, edge.C).gam
    return Edge(B, tuple(edge.C), B2, tuple(edge.C2), overflow, edge.v)


def uniform_chain(base, edges, B, C, width):
    start = at_width(base, B, width)
    if not chains.chain_shape(base, edges, B, C):
        raise ValueError("natural chain fields required")
    if not chains.literal_chain_ok(base, edges, B, C):
        raise ValueError("original chain must be accepted")
    transformed = tuple(uniform_edge(base, edge, width) for edge in edges)
    return transformed, start, tuple(C)


class Controls:
    def __init__(self, mirror):
        self.mirror = mirror
        self.count = Counter()

    def edge(self, base, edge, width, category):
        require(arithmetic.edge_ok(base, edge), "original edge fixture failed")
        before = arithmetic.state(base, edge.B, edge.C)
        require(before.gam in (0, 1), "overflow is not a bit")
        require(len(before.next_b) == len(edge.B) + before.gam,
                "independent raw exterior length law failed")
        require(len(edge.B) + before.gam == len(edge.B2) + edge.u,
                "accepted edge length accounting failed")
        fixed = uniform_edge(base, edge, width)
        require(len(fixed.B) == len(fixed.B2) == width, "exterior widths are not M")
        require(fixed.u == before.gam, "new exterior trim is not actual overflow")
        a, target_a = width - len(edge.B), width - len(edge.B2)
        require(a + edge.u == fixed.u + target_a, "padding counts do not balance")
        require(fixed == arithmetic.transport(base, edge, a, target_a, fixed.u),
                "direct fixed-width construction disagrees with padding transport")
        require(arithmetic.edge_ok(base, fixed), "fixed-width edge was rejected")
        after = arithmetic.state(base, fixed.B, fixed.C)
        require((after.e1, after.e2, after.gam) == (before.e1, before.e2, before.gam),
                "carry/overflow stream changed")
        require(after.next_c == before.next_c and
                (fixed.C, fixed.C2, fixed.v) == (edge.C, edge.C2, edge.v),
                "center dynamics or trim changed")
        require(len(after.next_b) == width + after.gam, "padded raw length law failed")
        require(uniform_edge(base, fixed, width) == fixed, "fixed-width map is not idempotent")
        for candidate in (edge, fixed):
            require(self.mirror.edgeOK(base, candidate.mirror_data()),
                    "whole-integer edge check disagrees with mirror")
            self.count["mirror_edge_comparisons"] += 1
        self.count[category] += 1
        self.count["accepted_edge_controls"] += 1
        self.count["unequal_original_width_edges"] += len(edge.B) != len(edge.B2)
        self.count["original_u_above_one_edges"] += edge.u > 1
        self.count["empty_source_B_edges"] += not edge.B
        self.count["unsymmetric_C_edges"] += edge.C != tuple(reversed(edge.C))
        raw_suffix = canonical.strip_suffix(base, after.next_b)[1]
        self.count["fixed_nonmaximal_trim_edges"] += fixed.u < raw_suffix
        return fixed

    def chain(self, base, edges, B, C, width, category, expected=None):
        require(chains.literal_chain_ok(base, edges, B, C), "original chain fixture failed")
        fixed, start, center = uniform_chain(base, edges, B, C, width)
        checked = tuple(self.edge(base, e, width, "chain_edge_controls") for e in edges)
        require(fixed == checked, "chain map disagrees with individual edges")
        require(chains.literal_chain_ok(base, fixed, start, center), "uniform chain failed")
        require(len(start) == width and len(fixed) == len(edges), "initial width/period changed")
        old_end_b, old_end_c = chains.endpoints(edges, B, C)
        require(chains.endpoints(fixed, start, center) ==
                (at_width(base, old_end_b, width), old_end_c), "endpoint identities failed")
        old_gain = sum(e.u + e.v for e in edges)
        new_gain = sum(e.u + e.v for e in fixed)
        require(old_gain + len(old_end_b) == new_gain + len(B),
                "open-chain gain telescope failed")
        old_stream = tuple((s.e1, s.e2, s.gam) for s in
                           (arithmetic.state(base, e.B, e.C) for e in edges))
        new_stream = tuple((s.e1, s.e2, s.gam) for s in
                           (arithmetic.state(base, e.B, e.C) for e in fixed))
        require(old_stream == new_stream, "whole stream changed")
        require(tuple(e.u for e in fixed) == tuple(g for _, _, g in old_stream),
                "fixed exterior trim schedule differs from overflow stream")
        if expected is not None:
            require(fixed == expected, "equivalent padded representatives gave different fixed cycles")
        old_cycle = chains.literal_cycle_ok(base, edges, B, C)
        new_cycle = chains.literal_cycle_ok(base, fixed, start, center)
        if old_cycle:
            require(new_cycle and old_gain == new_gain, "cycle acceptance or gain changed")
            self.count["accepted_cycle_controls"] += 1
        for es, source_b, source_c, answer in ((edges, B, C, old_cycle),
                                             (fixed, start, center, new_cycle)):
            reference = self.mirror.cycleOK(base, [e.mirror_data() for e in es],
                                            list(source_b), list(source_c))
            require(answer == reference, "literal cycle checker disagrees with mirror")
            self.count["mirror_cycle_comparisons"] += 1
        self.count[category] += 1
        self.count["chain_controls"] += 1
        self.count["empty_chain_controls"] += not edges
        return fixed


def minimum_width(edges, B):
    return max((len(B), *(len(w) for e in edges for w in (e.B, e.B2))))


def exhaustive_controls(control):
    for base in range(2, 6):
        alphabet = range(2 * base - 1)
        for nb in range(3):
            for B in product(alphabet, repeat=nb):
                for nc in range(3):
                    for C in product(alphabet, repeat=nc):
                        if not arithmetic.hyp(base, B, C):
                            continue
                        control.count["exhaustive_Hyp_sources"] += 1
                        s = arithmetic.state(base, B, C)
                        for B2, u in canonical.all_suffix_splits(base, s.next_b):
                            for C2, v in canonical.all_center_splits(base, s.next_c):
                                edge = Edge(B, C, B2, C2, u, v)
                                minimum = max(len(B), len(B2))
                                control.count["exhaustive_original_edges"] += 1
                                for extra in (0, 1, 4):
                                    control.edge(base, edge, minimum + extra, "exhaustive_fixed_edges")


def known_controls(control):
    sources = control.mirror._lean_certs()
    expected = {2: 4, 4: 6, 8: 8, 11: 6, 16: 10, 17: 6, 26: 4, 32: 12}
    require({base: len(es) for base, es in sources} == expected, "source inventory changed")
    for base, rows in sources:
        edges = tuple(Edge(*(tuple(w) for w in row[:4]), row[4], row[5]) for row in rows)
        B, C = edges[0].B, edges[0].C
        require(chains.literal_cycle_ok(base, edges, B, C), "source certificate rejected")
        control.count["known_bases"] += 1
        control.count["known_original_edges"] += len(edges)
        stripped = canonical.canonical_edges(base, edges)
        for extra in (0, 1, 8, 257):
            control.chain(base, edges, B, C, minimum_width(edges, B) + extra, "known_fixed_cycles")
        for extra in (0, 1, 8):
            control.chain(base, stripped, stripped[0].B, C,
                          minimum_width(stripped, stripped[0].B) + extra, "canonical_fixed_cycles")
        old_u = tuple(e.u for e in edges)
        require(sum(old_u) == 2, "source exterior trim total changed")
        for target in chains.compositions(2, len(edges)):
            control.count["all_equal_total_schedules"] += 1
            for reserve in (0, 4):
                offsets = chains.all_nat_offsets(old_u, target, reserve)
                retimed = chains.transport_chain(base, edges, offsets, target)
                for extra in (0, 1, 8):
                    width = minimum_width(retimed, retimed[0].B) + extra
                    reference, _, _ = uniform_chain(base, stripped, stripped[0].B, C, width)
                    control.chain(base, retimed, retimed[0].B, C, width,
                                  "retimed_fixed_cycles", reference)
        # Doubling a known certificate permits a natural trim count of four.
        doubled = edges + edges
        target = (4,) + (0,) * (len(doubled) - 1)
        offsets = chains.all_nat_offsets(tuple(e.u for e in doubled), target, 3)
        retimed = chains.transport_chain(base, doubled, offsets, target)
        for extra in (0, 8):
            control.chain(base, retimed, retimed[0].B, C,
                          minimum_width(retimed, retimed[0].B) + extra,
                          "repeated_trim_four_cycles")
        for phase in range(len(edges)):
            rotated = edges[phase:] + edges[:phase]
            for length in range(len(edges) + 1):
                prefix = rotated[:length]
                control.chain(base, prefix, rotated[0].B, rotated[0].C,
                              minimum_width(prefix, rotated[0].B), "known_rotated_prefixes")


def zero_width_and_nonmaximal_controls(control):
    for base in range(2, 33):
        control.chain(base, (), (), (), 0, "zero_width_empty_chains")
        s = arithmetic.state(base, (), (base,))
        edge = Edge((), (base,), s.next_b, s.next_c, 0, 0)
        require(arithmetic.edge_ok(base, edge), "empty exterior fixture failed")
        try:
            uniform_edge(base, edge, 0)
        except ValueError:
            control.count["zero_width_edge_rejections"] += 1
        else:
            raise RuntimeError("M=0 silently truncated a positive target width")
    # Known base2 overflow edge: canonical u=0, but its M=3 representative has
    # u=gam=1 while its raw neutral suffix has depth2, retaining one neutral.
    edge = Edge((2,), (0, 0), (1, 0), (2, 0, 2), 0, 0)
    fixed = control.edge(2, edge, 3, "nonmaximal_model_countercontrols")
    raw = arithmetic.state(2, fixed.B, fixed.C).next_b
    require((fixed.B, raw, fixed.B2, fixed.u) ==
            ((2, 1, 1), (1, 0, 1, 1), (1, 0, 1), 1), "fixed countercontrol changed")
    require(canonical.canonical_edge(2, fixed).u == 0 and
            canonical.strip_suffix(2, raw)[1] == 2, "maximal and fixed-width models confused")
    return edge


def malformed_controls(control, edge):
    cases = [(b, edge, 3) for b in (-1, 0, 1, True, 2.5)]
    cases += [(2, edge, width) for width in (-1, True, 0.5, None, 0, 1)]
    cases += [(2, bad, 3) for bad in (None, replace(edge, u=-1), replace(edge, v=True),
                                    replace(edge, B=(-1,)), replace(edge, C=(0.5,)),
                                    replace(edge, B2=(True,)), replace(edge, C2=(-1,)),
                                    replace(edge, u=1), replace(edge, B=(0,)))]
    for base, candidate, width in cases:
        try:
            uniform_edge(base, candidate, width)
        except ValueError:
            control.count["malformed_or_undersized_edge_rejections"] += 1
        else:
            raise RuntimeError("invalid fixed-width edge request accepted")
    chain_cases = ((None, edge.B, edge.C, 3), ((None,), edge.B, edge.C, 3),
                   ((), (1, 1), (), 1), ((), (-1,), (), 1), ((), (), (True,), 0),
                   ((edge,), edge.B + (0,), edge.C, 3),
                   ((edge, edge), edge.B, edge.C, 3),
                   ((edge,), edge.B, edge.C, 1))
    for es, B, C, width in chain_cases:
        try:
            uniform_chain(2, es, B, C, width)
        except ValueError:
            control.count["malformed_or_undersized_chain_rejections"] += 1
        else:
            raise RuntimeError("invalid fixed-width chain request accepted")


def main():
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("agent114_uniform_mirror",
                                                root / "calculation/neutral_band_search.py")
    require(spec is not None and spec.loader is not None, "repository mirror unavailable")
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    control = Controls(mirror)
    exhaustive_controls(control)
    known_controls(control)
    edge = zero_width_and_nonmaximal_controls(control)
    malformed_controls(control, edge)
    print("COMPUTED uniform-exterior controls; exhaustive bases=2..5 B<=2 C<=2")
    print(json.dumps(dict(sorted(control.count.items())), sort_keys=True))
    print("ALL UNIFORM EXTERIOR CONTROLS PASSED")


if __name__ == "__main__":
    main()
