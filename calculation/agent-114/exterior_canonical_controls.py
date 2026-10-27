#!/usr/bin/env python3
"""COMPUTED regression for maximal neutral exterior canonicalization.

Commands from the repository root:
    python3 calculation/agent-114/exterior_canonical_controls.py
    python3 -O calculation/agent-114/exterior_canonical_controls.py

The credited independent whole-integer edge arithmetic and literal chain
verifier are reused from Agent114's earlier controls. This file independently
implements maximal suffix stripping, checks all legal partial trims on its
bounded exhaustive domain, and compares complete cycles with the repository
mirror. Agent7's canonicalization and Agent107's retiming arguments retain
their attribution. These finite tests are neither a new theorem nor a new
certificate. All guards remain active under optimized Python.
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

Edge = arithmetic.Edge
require = arithmetic.require
natural = arithmetic.natural
natural_word = arithmetic.natural_word


def strip_suffix(base, word):
    """Return the core and exact maximal neutral suffix depth."""
    if not natural(base) or base < 2 or not natural_word(word):
        raise ValueError("suffix stripping requires a base >= 2 and natural word")
    end = len(word)
    while end and word[end - 1] == base - 1:
        end -= 1
    return tuple(word[:end]), len(word) - end


def canonical_edge(base, edge):
    """Canonicalize a typed edge with legal source; acceptance is not assumed."""
    if not chains.edge_shape(edge) or not arithmetic.hyp(base, edge.B, edge.C):
        raise ValueError("canonical edge requires natural fields and a Hyp-valid source")
    B, _ = strip_suffix(base, edge.B)
    B2, _ = strip_suffix(base, edge.B2)
    raw = arithmetic.state(base, B, edge.C).next_b
    _, u = strip_suffix(base, raw)
    return Edge(B, tuple(edge.C), B2, tuple(edge.C2), u, edge.v)


def canonical_edges(base, edges):
    if not isinstance(edges, (list, tuple)):
        raise ValueError("an edge sequence is required")
    return tuple(canonical_edge(base, edge) for edge in edges)


def all_suffix_splits(base, raw):
    """Separate exhaustive equality test, without the backwards-strip loop."""
    return tuple((tuple(raw[:len(raw)-k]), k) for k in range(len(raw) + 1)
                 if tuple(raw) == tuple(raw[:len(raw)-k]) + (base - 1,) * k)


def all_center_splits(base, raw):
    for v in range(len(raw) // 2 + 1):
        C2 = tuple(raw[v:len(raw)-v]) if v else tuple(raw)
        if tuple(raw) == (base - 1,) * v + C2 + (base - 1,) * v:
            yield C2, v


class Controls:
    def __init__(self, mirror):
        self.mirror = mirror
        self.count = Counter()

    def edge(self, base, edge, category):
        require(arithmetic.edge_ok(base, edge), "original edge fixture is not accepted")
        canonical = canonical_edge(base, edge)
        require(arithmetic.edge_ok(base, canonical), "canonical accepted edge failed")
        source_core, source_depth = strip_suffix(base, edge.B)
        target_core, target_depth = strip_suffix(base, edge.B2)
        require(edge.B == source_core + (base - 1,) * source_depth
                and edge.B2 == target_core + (base - 1,) * target_depth,
                "maximal suffix decomposition failed")
        require(canonical.B == source_core and canonical.B2 == target_core,
                "canonical endpoints disagree")
        require(canonical.u + source_depth == edge.u + target_depth,
                "canonical trim/padding accounting failed")
        restored = arithmetic.transport(base, canonical, source_depth, target_depth, edge.u)
        require(restored == edge, "padding the canonical edge did not restore the original")
        raw = arithmetic.state(base, source_core, edge.C).next_b
        alternatives = all_suffix_splits(base, raw)
        normalized = tuple((word, u) for word, u in alternatives
                           if not word or word[-1] != base - 1)
        require(normalized == ((target_core, canonical.u),),
                "normalized target/maximal trim was not uniquely forced")
        require(canonical.u == max(u for _, u in alternatives), "trim was not maximal")
        require(canonical_edge(base, canonical) == canonical, "edge canonicalization is not idempotent")
        original_state = arithmetic.state(base, edge.B, edge.C)
        canonical_state = arithmetic.state(base, canonical.B, canonical.C)
        require((original_state.e1, original_state.e2, original_state.gam) ==
                (canonical_state.e1, canonical_state.e2, canonical_state.gam),
                "canonicalization changed a carry/overflow bit")
        require(original_state.next_c == canonical_state.next_c, "center successor changed")
        require((canonical.C, canonical.C2, canonical.v) == (edge.C, edge.C2, edge.v),
                "center data changed")
        for candidate in (edge, canonical):
            require(self.mirror.edgeOK(base, candidate.mirror_data()),
                    "independent accepted edge disagrees with repository mirror")
            self.count["mirror_edge_comparisons"] += 1
        self.count[category] += 1
        self.count["accepted_edge_controls"] += 1
        self.count["empty_source_B_edges"] += not edge.B
        self.count["empty_canonical_source_edges"] += not source_core
        self.count["empty_canonical_target_edges"] += not target_core
        self.count["nonmaximal_original_u_edges"] += target_depth > 0
        self.count["positive_source_suffix_edges"] += source_depth > 0
        self.count["unsymmetric_C_edges"] += edge.C != tuple(reversed(edge.C))
        return canonical

    def chain(self, base, edges, B, C, category, expected=None):
        require(chains.literal_chain_ok(base, edges, B, C), "original chain is not accepted")
        canonical = tuple(self.edge(base, e, "chain_edge_controls") for e in edges)
        core, initial_depth = strip_suffix(base, B)
        require(chains.literal_chain_ok(base, canonical, core, C), "canonical chain failed")
        old_end_b, old_end_c = chains.endpoints(edges, B, C)
        end_core, terminal_depth = strip_suffix(base, old_end_b)
        require(chains.endpoints(canonical, core, C) == (end_core, old_end_c),
                "canonical chain endpoint identity failed")
        old_gain = sum(e.u + e.v for e in edges)
        new_gain = sum(e.u + e.v for e in canonical)
        require(new_gain + initial_depth == old_gain + terminal_depth,
                "canonical open-chain telescope failed")
        require(len(canonical) == len(edges), "canonical chain length changed")
        old_stream = tuple((s.e1, s.e2, s.gam) for s in
                           (arithmetic.state(base, e.B, e.C) for e in edges))
        new_stream = tuple((s.e1, s.e2, s.gam) for s in
                           (arithmetic.state(base, e.B, e.C) for e in canonical))
        require(old_stream == new_stream, "whole canonical stream changed")
        if expected is not None:
            require(canonical == expected, "padding/retiming changed the canonical edge sequence")
        is_cycle = chains.literal_cycle_ok(base, edges, B, C)
        is_canonical_cycle = chains.literal_cycle_ok(base, canonical, core, C)
        if is_cycle:
            require(is_canonical_cycle and old_gain == new_gain,
                    "accepted cycle or its total gain was not preserved")
            self.count["accepted_cycle_controls"] += 1
        for es, start_b, answer in ((edges, B, is_cycle), (canonical, core, is_canonical_cycle)):
            reference = self.mirror.cycleOK(base, [e.mirror_data() for e in es], list(start_b), list(C))
            require(reference == answer, "literal cycle checker disagrees with mirror")
            self.count["mirror_cycle_comparisons"] += 1
        self.count[category] += 1
        self.count["chain_controls"] += 1
        self.count["empty_chain_controls"] += not edges
        return canonical


def exhaustive_controls(control):
    for base in range(2, 6):
        alphabet = range(2 * base - 1)
        for nb in range(3):
            for B in product(alphabet, repeat=nb):
                for nc in range(4):
                    for C in product(alphabet, repeat=nc):
                        if not arithmetic.hyp(base, B, C):
                            continue
                        control.count["exhaustive_Hyp_sources"] += 1
                        s = arithmetic.state(base, B, C)
                        for B2, u in all_suffix_splits(base, s.next_b):
                            for C2, v in all_center_splits(base, s.next_c):
                                control.edge(base, Edge(B, C, B2, C2, u, v),
                                             "exhaustive_all_partial_trim_edges")


def known_controls(control):
    sources = control.mirror._lean_certs()
    expected = {2: 4, 4: 6, 8: 8, 11: 6, 16: 10, 17: 6, 26: 4, 32: 12}
    require({base: len(es) for base, es in sources} == expected, "source inventory changed")
    for base, rows in sources:
        edges = tuple(Edge(*(tuple(w) for w in row[:4]), row[4], row[5]) for row in rows)
        B, C = edges[0].B, edges[0].C
        require(chains.literal_cycle_ok(base, edges, B, C), "source cycle failed")
        canonical = control.chain(base, edges, B, C, "known_original_cycles")
        control.count["known_bases"] += 1
        control.count["known_original_edges"] += len(edges)
        old_u = tuple(e.u for e in edges)
        require(sum(old_u) == 2, "source exterior trim total changed")
        for target in chains.compositions(2, len(edges)):
            control.count["all_equal_total_schedules"] += 1
            for extra in (0, 3):
                offsets = chains.all_nat_offsets(old_u, target, extra)
                lifted = chains.transport_chain(base, edges, offsets, target)
                control.chain(base, lifted, lifted[0].B, C, "retimed_cycles", canonical)
        for reserve in (1, 8, 257):
            lifted = chains.transport_chain(base, edges, (reserve,) * (len(edges) + 1), old_u)
            control.chain(base, lifted, lifted[0].B, C, "constant_padding_cycles", canonical)
        for phase in range(len(edges)):
            rotated = edges[phase:] + edges[:phase]
            for length in range(len(edges) + 1):
                control.chain(base, rotated[:length], rotated[0].B, rotated[0].C,
                              "known_rotated_prefixes")


def rejected_cycle_counterexample(control):
    # Original source is the known four-edge base2 certificate. Padding only
    # edge1's source and increasing its u preserves every LOCAL edge check,
    # but breaks the edge0 -> edge1 link. Canonicalization erases that mismatch.
    rejected = (
        Edge((2,), (0, 0), (1, 0), (2, 0, 2), 0, 0),
        Edge((1, 0, 1), (2, 0, 2), (2,), (0, 2, 0), 2, 0),
        Edge((2,), (0, 2, 0), (1, 0), (2, 1, 1, 2), 0, 0),
        Edge((1, 0), (2, 1, 1, 2), (2,), (0, 0), 1, 1),
    )
    B, C = (2,), (0, 0)
    canonical = tuple(control.edge(2, e, "rejected_cycle_local_edges") for e in rejected)
    require(not chains.literal_chain_ok(2, rejected, B, C), "counterexample chain was accepted")
    require(not chains.literal_cycle_ok(2, rejected, B, C), "counterexample cycle was accepted")
    require(chains.literal_cycle_ok(2, canonical, B, C), "counterexample canonical cycle failed")
    require(not control.mirror.cycleOK(2, [e.mirror_data() for e in rejected], list(B), list(C)),
            "mirror accepted counterexample")
    require(control.mirror.cycleOK(2, [e.mirror_data() for e in canonical], list(B), list(C)),
            "mirror rejected canonical counterexample")
    control.count["mirror_cycle_comparisons"] += 2
    control.count["rejected_to_accepted_cycle_counterexamples"] += 1
    control.count["counterexample_original_gain"] = sum(e.u + e.v for e in rejected)
    control.count["counterexample_canonical_gain"] = sum(e.u + e.v for e in canonical)
    return rejected[0]


def malformed_controls(control, edge):
    base = 2
    bad_edges = [None]
    bad_edges += [replace(edge, **change) for change in (
        {"u": -1}, {"v": -1}, {"u": True}, {"v": 0.5},
        {"B": (-1,)}, {"C": (True,)}, {"B2": (-1,)}, {"C2": (0.5,)},
        {"B": (0,)}, {"B": (3,)}, {"C": (3,)}, {"C": ()},
    )]
    cases = [(base, e) for e in bad_edges]
    cases += [(b, edge) for b in (-1, 0, 1, True, 2.5)]
    for b, e in cases:
        try:
            canonical_edge(b, e)
        except ValueError:
            control.count["malformed_canonical_edge_rejections"] += 1
        else:
            raise RuntimeError("malformed canonical edge input accepted")
    strip_cases = ((-1, ()), (0, ()), (1, ()), (True, ()), (2.5, ()),
                   (2, None), (2, (-1,)), (2, (True,)), (2, (0.5,)))
    for b, word in strip_cases:
        try:
            strip_suffix(b, word)
        except ValueError:
            control.count["malformed_suffix_rejections"] += 1
        else:
            raise RuntimeError("malformed suffix input accepted")
    require(canonical_edges(base, ()) == (), "empty canonical list changed")
    require(not chains.literal_cycle_ok(base, (), (), ()), "empty cycle accepted")
    control.count["empty_cycle_guard"] += 1
    for es in (None, (None,), (replace(edge, u=-1),)):
        try:
            canonical_edges(base, es)
        except ValueError:
            control.count["malformed_canonical_list_rejections"] += 1
        else:
            raise RuntimeError("malformed edge sequence accepted")


def main():
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("agent114_canonical_mirror",
                                                root / "calculation/neutral_band_search.py")
    require(spec is not None and spec.loader is not None, "repository mirror unavailable")
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    control = Controls(mirror)
    exhaustive_controls(control)
    known_controls(control)
    edge = rejected_cycle_counterexample(control)
    malformed_controls(control, edge)
    print("COMPUTED exterior-canonical controls; exhaustive bases=2..5 B<=2 C<=3")
    print(json.dumps(dict(sorted(control.count.items())), sort_keys=True))
    print("ALL EXTERIOR CANONICAL CONTROLS PASSED")


if __name__ == "__main__":
    main()
