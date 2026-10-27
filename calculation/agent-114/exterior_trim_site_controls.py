#!/usr/bin/env python3
"""COMPUTED controls for the credited Agent7 exterior trim-site arithmetic.

Run normally and with optimized Python from the repository root:
    python3 calculation/agent-114/exterior_trim_site_controls.py
    python3 -O calculation/agent-114/exterior_trim_site_controls.py

The previous Agent114 controls supply independent whole-integer normalization
and edge checking; their suffix/cycle fixture utilities are explicitly reused.
This file checks terminal formulas, overflow suffix conservation, all legal
partial trims in its stated finite domains, and all eight known cycles.
It makes no new search, period-completion, or certificate-existence claim.
All premise and acceptance guards remain active under Python -O.
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


def trim_site(base, e, last, entering):
    if (not natural(base) or base < 2 or not natural(e) or e > 1
            or not natural(entering) or entering > 1
            or not natural(last) or last > 2 * (base - 1)):
        raise ValueError("trim-site parameters require a base, bounded coefficient, and bits")
    return (e, last, entering) in (
        (0, (base - 2) // 2, (base - 2) % 2),
        (1, (3 * base - 1) // 2, (3 * base - 1) % 2),
    )


def source_data(base, B, C):
    if not arithmetic.hyp(base, B, C):
        raise ValueError("the complete Hyp premise is required")
    state = arithmetic.state(base, B, C)
    entering = arithmetic.norm_integer(base, B[:-1], 0)[1] if B else 0
    depth = canonical.strip_suffix(base, B)[1]
    raw_depth = canonical.strip_suffix(base, state.next_b)[1]
    return state, entering, depth, raw_depth


def chosen_centers(base, B):
    e = arithmetic.norm_integer(base, B, 0)[1]
    return ((base,), (0, base)) if e == 0 else ((0,), (base, 0))


class Controls:
    def __init__(self, mirror):
        self.mirror = mirror
        self.count = Counter()

    def edge(self, base, edge, data, mirror, category):
        require(arithmetic.edge_ok(base, edge), "constructed accepted edge failed")
        state, entering, depth, raw_depth = data
        target_depth = canonical.strip_suffix(base, edge.B2)[1]
        require(edge.u + target_depth == raw_depth, "literal trim/suffix accounting failed")
        if state.gam:
            require(edge.u + target_depth == depth, "overflow suffix conservation failed")
            self.count["overflow_edge_conservation"] += 1
            if edge.u:
                require(depth > 0, "positive overflow trim has a canonical source")
                self.count["noncanonical_positive_overflow_trims"] += 1
        if depth == 0 and edge.u > 0:
            require(edge.B and state.gam == 0, "canonical positive trim needs nonoverflow")
            require(trim_site(base, state.e1, edge.B[-1], entering),
                    "canonical positive trim misses the exact boundary threshold")
            self.count["canonical_positive_trim_thresholds"] += 1
        if mirror:
            require(self.mirror.edgeOK(base, edge.mirror_data()), "independent edge/mirror mismatch")
            self.count["mirror_edge_comparisons"] += 1
        self.count[category] += 1
        self.count["accepted_edge_controls"] += 1

    def source(self, base, B, C, mirror, category):
        data = source_data(base, B, C)
        state, entering, depth, raw_depth = data
        require(state.e2 == 1 - state.e1 and state.gam in (0, 1), "carry premise failed")
        require(len(state.next_b) == len(B) + state.gam, "raw exterior length changed")
        if B:
            z, e, h = B[-1], state.e1, base - 1
            require(entering in (0, 1) and (z + entering) // base == e,
                    "prefix carry does not reconstruct terminal carry")
            nonoverflow_last = (z + entering) % base + (z + 1 - e) % base
            overflow_last = h * (1 - e) + (z + 1 - e) % base
            expected = overflow_last if state.gam else nonoverflow_last
            require(state.next_b[-1] == expected, "exact terminal coefficient formula failed")
            self.count["overflow_terminal_formulas" if state.gam else "nonoverflow_terminal_formulas"] += 1
            if state.gam:
                require((state.next_b[-1] == h) == (z == h),
                        "overflow neutral terminal equivalence failed")
                self.count["overflow_neutral_last_equivalences"] += 1
            elif depth == 0:
                # Under Hyp + gam=0 + canonical source this local equivalence
                # is true. It does not validate a chosen target or whole cycle.
                require((state.next_b[-1] == h) == trim_site(base, e, z, entering),
                        "nonoverflow canonical local threshold equivalence failed")
                self.count["canonical_local_threshold_equivalences"] += 1
        else:
            require(state.e1 == 0 and state.e2 == state.gam == 1
                    and state.next_b == (base,), "empty exterior must have raw successor [b]")
            self.count["empty_exterior_sources"] += 1
        if state.gam:
            require(raw_depth == depth, "overflow changed maximal neutral suffix depth")
            self.count["overflow_suffix_depth_identities"] += 1
        if mirror:
            Bm, Cm = list(B), list(C)
            m = self.mirror
            require((state.e1, state.e2, state.gam, state.next_b, state.next_c) ==
                    (m.e1(base, Bm), m.e2(base, Bm, Cm), m.gam(base, Bm, Cm),
                     tuple(m.nextB(base, Bm, Cm)), tuple(m.nextC(base, Bm, Cm))),
                    "whole-integer transition/mirror mismatch")
            self.count["mirror_state_comparisons"] += 1
        splits = canonical.all_suffix_splits(base, state.next_b)
        require(max(u for _, u in splits) == raw_depth, "independent suffix enumeration mismatch")
        for B2, u in splits:
            for C2, v in canonical.all_center_splits(base, state.next_c):
                self.edge(base, Edge(B, C, B2, C2, u, v), data, mirror,
                          "all_legal_partial_trim_edges")
        self.count[category] += 1
        self.count["Hyp_source_controls"] += 1
        self.count["asymmetric_center_sources"] += C != tuple(reversed(C))
        return data


def exhaustive_controls(control):
    serial = 0
    for base in range(2, 13):
        alphabet = range(2 * base - 1)
        for width in range(4):
            for B in product(alphabet, repeat=width):
                if B and B[0] == 0:
                    continue
                control.count["all_base_exterior_words"] += 1
                for C in chosen_centers(base, B):
                    control.source(base, B, C, width <= 2 or serial % 257 == 0,
                                   "all_base_sources")
                    serial += 1
    # A separate complete wider decimal slice; widths<=3 are already covered.
    for index, B in enumerate(product(range(19), repeat=4)):
        if B[0] == 0:
            continue
        C = chosen_centers(10, B)[0]
        control.source(10, B, C, index % 257 == 0, "decimal_width4_sources")


def known_controls(control):
    sources = control.mirror._lean_certs()
    expected = {2: 4, 4: 6, 8: 8, 11: 6, 16: 10, 17: 6, 26: 4, 32: 12}
    require({base: len(es) for base, es in sources} == expected, "known-source inventory changed")
    for base, rows in sources:
        edges = tuple(Edge(*(tuple(w) for w in row[:4]), row[4], row[5]) for row in rows)
        stripped = canonical.canonical_edges(base, edges)
        control.count["known_bases"] += 1
        control.count["known_original_edges"] += len(edges)
        for cycle in (edges, stripped):
            B, C = cycle[0].B, cycle[0].C
            require(chains.literal_cycle_ok(base, cycle, B, C), "known cycle failed independent replay")
            require(control.mirror.cycleOK(base, [e.mirror_data() for e in cycle], list(B), list(C)),
                    "known cycle failed mirror replay")
            control.count["known_original_or_canonical_cycles"] += 1
            for edge in cycle:
                data = control.source(base, edge.B, edge.C, True, "known_phase_sources")
                control.edge(base, edge, data, True, "known_exact_edges")
        for old, new in zip(edges, stripped):
            before = arithmetic.state(base, old.B, old.C)
            after = arithmetic.state(base, new.B, new.C)
            require((before.e1, before.e2, before.gam) == (after.e1, after.e2, after.gam),
                    "canonicalization changed known streams")
            if after.gam:
                require(new.u == 0, "canonical known overflow has positive exterior trim")
                control.count["known_canonical_overflow_u_zero"] += 1
        require(sum(e.u + e.v for e in edges) == sum(e.u + e.v for e in stripped),
                "canonical known cycle gain changed")


def premise_and_scope_controls(control):
    # The threshold tuple without the nonoverflow premise is insufficient.
    B, C = (10, 0, 4), (10,)
    data = control.source(10, B, C, True, "scope_countercontrol_sources")
    s, t, q, _ = data
    require(q == 0 and trim_site(10, s.e1, B[-1], t) and s.gam == 1
            and s.next_b == (1, 1, 4, 14), "threshold/overflow countercontrol changed")
    control.count["threshold_without_nonoverflow_countercontrols"] += 1
    # Hyp + gam=0 does give a neutral terminal coefficient here, but cannot
    # validate an arbitrary chosen target or force selection of positive u.
    B, C = (4,), (10,)
    data = control.source(10, B, C, True, "scope_countercontrol_sources")
    s, t, _, _ = data
    require(s.gam == 0 and trim_site(10, s.e1, B[-1], t) and s.next_b == (9,),
            "genuine nonoverflow trim site changed")
    untrimmed = Edge(B, C, (9,), (0,), 0, 0)
    require(arithmetic.edge_ok(10, untrimmed), "legal zero-trim choice failed")
    require(not arithmetic.edge_ok(10, replace(untrimmed, B2=(8,))),
            "trim-site gates incorrectly validate a wrong target")
    require(not arithmetic.edge_ok(10, replace(untrimmed, B2=(), u=2)),
            "one neutral coefficient incorrectly permits two trims")
    control.count["wrong_target_or_trim_rejections"] += 2
    control.count["site_does_not_force_selected_positive_u"] += 1
    # A noncanonical decimal exterior can legally trim on an overflow step.
    edge = Edge((9,), (10,), (10,), (0, 0), 1, 0)
    data = control.source(10, edge.B, edge.C, True, "scope_countercontrol_sources")
    control.edge(10, edge, data, True, "scope_countercontrol_edges")
    require(data[0].gam == 1 and data[2] == edge.u == 1,
            "canonical-source premise countercontrol changed")
    control.count["noncanonical_overflow_countercontrols"] += 1
    # Fixed-width u=gam is different from maximal trimming on a canonical B.
    edge = Edge((2, 1, 1), (0, 0), (1, 0, 1), (2, 0, 2), 1, 0)
    data = control.source(2, edge.B, edge.C, True, "scope_countercontrol_sources")
    control.edge(2, edge, data, True, "scope_countercontrol_edges")
    require(data[0].gam == edge.u == 1 and data[3] == 2
            and len(edge.B) == len(edge.B2) == 3
            and canonical.canonical_edge(2, edge).u == 0,
            "fixed-width and canonical trim models were confused")
    control.count["fixed_width_overflow_countercontrols"] += 1
    # Removing the flip premise makes the complementary terminal formula fail.
    bad = arithmetic.state(10, (1,), (0,))
    require(not arithmetic.hyp(10, (1,), (0,)) and bad.next_b == (2,)
            and (1 + 0) % 10 + (1 + 1 - bad.e1) % 10 == 3,
            "missing-flip countercontrol changed")
    control.count["missing_flip_formula_countercontrols"] += 1


def malformed_controls(control):
    cases = [(b, (4,), (10,)) for b in (-1, 0, 1, True, 10.5)]
    cases += [(10, B, C) for B, C in ((None, (10,)), ((-1,), (10,)),
                                     ((True,), (10,)), ((19,), (10,)), ((0,), (10,)),
                                     ((4,), None), ((4,), (False,)), ((4,), (19,)),
                                     ((4,), ()), ((1,), (0,)))]
    for base, B, C in cases:
        try:
            source_data(base, B, C)
        except ValueError:
            control.count["invalid_source_premise_rejections"] += 1
        else:
            raise RuntimeError("invalid Hyp premise accepted")
    site_cases = ((1, 0, 0, 0), (True, 0, 0, 0), (10, True, 4, 0),
                  (10, 2, 4, 0), (10, 0, -1, 0), (10, 0, 19, 0),
                  (10, 0, 4, 2), (10, 0, 4, 0.5))
    for args in site_cases:
        try:
            trim_site(*args)
        except ValueError:
            control.count["invalid_threshold_parameter_rejections"] += 1
        else:
            raise RuntimeError("invalid threshold parameters accepted")


def main():
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("agent114_trim_site_mirror",
                                                root / "calculation/neutral_band_search.py")
    require(spec is not None and spec.loader is not None, "repository mirror unavailable")
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    control = Controls(mirror)
    exhaustive_controls(control)
    known_controls(control)
    premise_and_scope_controls(control)
    malformed_controls(control)
    print("COMPUTED exterior trim-site controls; bases=2..12 B<=3; decimal B=4")
    print(json.dumps(dict(sorted(control.count.items())), sort_keys=True))
    print("ALL EXTERIOR TRIM SITE CONTROLS PASSED")


if __name__ == "__main__":
    main()
