#!/usr/bin/env python3
"""Self-contained COMPUTED controls for neutral center trim-site arithmetic.

Run from the repository root, normally and with optimized Python:
    python3 calculation/agent-114/center_trim_site_controls.py
    python3 -O calculation/agent-114/center_trim_site_controls.py

Normalization uses whole positional integers, independently of the repository
mirror's digit-by-digit carry loop. The mirror supplies differential checks
and the eight existing source fixtures only. Agent7's padding/trim arguments
and Agent119's center-normalization work retain their attribution. No helper
module from either agent is imported. These finite regressions are not a new
search, certificate, or proof. All guards remain active under Python -O.
"""

from collections import Counter
from dataclasses import dataclass, replace
import importlib.util
from itertools import product
from pathlib import Path
import json
import sys

sys.dont_write_bytecode = True


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def natural(value):
    return type(value) is int and value >= 0


def natural_word(word):
    return isinstance(word, (tuple, list)) and all(natural(x) for x in word)


def norm_integer(base, word, carry):
    if not natural(base) or base < 2 or not natural_word(word) or not natural(carry):
        raise ValueError("natural word/carry and base >= 2 required")
    number = 0
    for coefficient in reversed(word):
        number = base * number + coefficient
    number += carry
    digits = []
    for _ in word:
        number, digit = divmod(number, base)
        digits.append(digit)
    return tuple(digits), number


@dataclass(frozen=True)
class State:
    e: int
    f: int
    g: int
    db: tuple
    dc: tuple
    dr: tuple
    nb: tuple
    nc: tuple


def state(base, B, C):
    db, e = norm_integer(base, B, 0)
    dc, f = norm_integer(base, C, e)
    dr, g = norm_integer(base, tuple(reversed(B)), f)
    low, high, center = db, tuple(reversed(dr)), dc
    if g != 0:
        # Natural subtraction also defines the raw map outside Hyp.
        low += ((base - 1) * max(0, 1 - e),)
        high = (1,) + high
        center += ((base - 1) * max(0, 1 - f),)
    nb = tuple(x + y for x, y in zip(low, high))
    nc = tuple(x + y for x, y in zip(center, reversed(center)))
    return State(e, f, g, db, dc, dr, nb, nc)


def hyp(base, B, C):
    if not natural(base) or base < 2 or not natural_word(B) or not natural_word(C):
        return False
    if any(x > 2 * (base - 1) for x in (*B, *C)) or (B and B[0] == 0):
        return False
    _, e = norm_integer(base, B, 0)
    _, f = norm_integer(base, C, e)
    return e != f


@dataclass(frozen=True)
class Edge:
    B: tuple
    C: tuple
    B2: tuple
    C2: tuple
    u: int
    v: int

    def mirror_data(self):
        return tuple(list(w) for w in (self.B, self.C, self.B2, self.C2)) + (self.u, self.v)


def edge_ok(base, edge):
    if (not isinstance(edge, Edge) or not natural(edge.u) or not natural(edge.v)
            or not natural_word(edge.B2) or not natural_word(edge.C2)
            or not hyp(base, edge.B, edge.C)):
        return False
    s = state(base, edge.B, edge.C)
    h = (base - 1,)
    return s.nb == tuple(edge.B2) + h * edge.u and s.nc == h * edge.v + tuple(edge.C2) + h * edge.v


def cycle_ok(base, edges, B, C):
    if (not isinstance(edges, (list, tuple)) or not edges
            or not natural_word(B) or not natural_word(C)):
        return False
    current = (tuple(B), tuple(C))
    gain = overflow = 0
    for edge in edges:
        if not edge_ok(base, edge) or (tuple(edge.B), tuple(edge.C)) != current:
            return False
        current = (tuple(edge.B2), tuple(edge.C2))
        gain += edge.u + edge.v
        overflow += state(base, edge.B, edge.C).g
    return current == (tuple(B), tuple(C)) and overflow <= gain


def pad(base, amount, C):
    if not natural(base) or base < 2 or not natural(amount) or not natural_word(C):
        raise ValueError("natural center/padding and base >= 2 required")
    neutral = (base - 1,) * amount
    return neutral + tuple(C) + neutral


def strip_pairs(base, C):
    if not natural(base) or base < 2 or not natural_word(C):
        raise ValueError("natural center and base >= 2 required")
    depth = 0
    while 2 * (depth + 1) <= len(C) and C[depth] == C[-depth-1] == base - 1:
        depth += 1
    core = tuple(C[depth:len(C)-depth]) if depth else tuple(C)
    return core, depth


def symmetric(word):
    return tuple(word) == tuple(reversed(word))


def trim_site(base, e, head, entering_last):
    if (not natural(base) or base < 2 or not natural(e) or e > 1
            or not natural(entering_last) or entering_last > 1
            or not natural(head) or head > 2 * (base - 1)):
        raise ValueError("bounded coefficient and binary carries required")
    return (e, head, entering_last) in (
        (0, (3 * base - 1) // 2, (3 * base - 1) % 2),
        (1, (base - 2) // 2, (base - 2) % 2),
    )


def facts(base, B, C):
    if not hyp(base, B, C):
        raise ValueError("complete Hyp premise required")
    s = state(base, B, C)
    core, depth = strip_pairs(base, C)
    raw_depth = strip_pairs(base, s.nc)[1]
    entering_last = norm_integer(base, C[:-1], s.e)[1]
    return s, core, depth, raw_depth, entering_last


def normalize_edge(base, edge):
    if not edge_ok(base, edge):
        raise ValueError("accepted edge required")
    source = strip_pairs(base, edge.C)[0]
    target = strip_pairs(base, edge.C2)[0]
    v = strip_pairs(base, state(base, edge.B, source).nc)[1]
    return Edge(tuple(edge.B), source, tuple(edge.B2), target, edge.u, v)


def suffix_splits(base, word):
    return tuple((tuple(word[:len(word)-u]), u) for u in range(len(word) + 1)
                 if tuple(word) == tuple(word[:len(word)-u]) + (base - 1,) * u)


def pair_splits(base, word):
    for v in range(len(word) // 2 + 1):
        middle = tuple(word[v:len(word)-v]) if v else tuple(word)
        if tuple(word) == pad(base, v, middle):
            yield middle, v


class Controls:
    def __init__(self, mirror):
        self.mirror = mirror
        self.count = Counter()
        self.serial = 0

    def edge(self, base, edge, data, mirror, category):
        require(edge_ok(base, edge), "accepted edge fixture failed")
        s, _, depth, raw_depth, t = data
        require(symmetric(edge.C2), "accepted symmetric trim target is not symmetric")
        require(edge.v + strip_pairs(base, edge.C2)[1] == raw_depth,
                "literal center trim/depth balance failed")
        if s.g == 1 and edge.C[0] != base - 1:
            require(edge.v == 0, "head-normal overflow edge trims the center")
            self.count["head_normal_overflow_v_zero"] += 1
        if symmetric(edge.C) and s.g == 1:
            require(edge.v + strip_pairs(base, edge.C2)[1] == depth,
                    "symmetric overflow depth accounting failed")
            self.count["symmetric_overflow_edge_depth_identities"] += 1
        if symmetric(edge.C) and depth == 0 and edge.v > 0:
            require(s.g == 0 and trim_site(base, s.e, edge.C[0], t),
                    "symmetric canonical positive trim misses its exact site")
            self.count["canonical_positive_center_trim_sites"] += 1
        if mirror:
            require(self.mirror.edgeOK(base, edge.mirror_data()), "edge/mirror disagreement")
            self.count["mirror_edge_comparisons"] += 1
        self.count[category] += 1
        self.count["accepted_edge_controls"] += 1
        self.count["asymmetric_source_edge_controls"] += not symmetric(edge.C)
        self.count["empty_target_center_edges"] += not edge.C2

    def padding(self, base, B, C, first, second):
        before = state(base, B, C)
        core, depth = strip_pairs(base, C)
        repeated = pad(base, second, pad(base, first, C))
        require(repeated == pad(base, first + second, C), "padding composition failed")
        after = state(base, B, repeated)
        require(hyp(base, B, repeated) and (after.e, after.f, after.g) ==
                (before.e, before.f, before.g), "padding lost Hyp or carries")
        require(after.nb == before.nb and after.nc == pad(base, first + second, before.nc),
                "center padding covariance failed")
        require(strip_pairs(base, repeated) == (core, depth + first + second),
                "padding/core/depth identity failed")
        edge = Edge(B, repeated, before.nb, before.nc, 0, first + second)
        self.edge(base, edge, facts(base, B, repeated), True, "repeated_padding_edges")
        self.count["repeated_padding_controls"] += 1

    def source(self, base, B, C, mirror, category, allow_padding=True):
        s = state(base, B, C)
        require(symmetric(s.nc), "raw nextC symmetry failed")
        core, depth = strip_pairs(base, C)
        require(pad(base, depth, core) == C and len(core) + 2 * depth == len(C),
                "maximal pair decomposition failed")
        splits = tuple(pair_splits(base, C))
        require(splits[-1] == (core, depth) and strip_pairs(base, core) == (core, 0),
                "separate pair enumeration or core idempotence failed")
        if mirror:
            m, Bm, Cm = self.mirror, list(B), list(C)
            require((s.e, s.f, s.g, s.db, s.dc, s.dr, s.nb, s.nc) ==
                    (m.e1(base, Bm), m.e2(base, Bm, Cm), m.gam(base, Bm, Cm),
                     tuple(m.DB(base, Bm)), tuple(m.DC(base, Bm, Cm)), tuple(m.DR(base, Bm, Cm)),
                     tuple(m.nextB(base, Bm, Cm)), tuple(m.nextC(base, Bm, Cm))),
                    "whole-integer state/mirror disagreement")
            self.count["mirror_state_comparisons"] += 1
        self.count[category] += 1
        self.count["raw_symmetry_controls"] += 1
        self.count["empty_source_center_inputs"] += not C
        if not hyp(base, B, C):
            self.count["raw_sources_outside_Hyp"] += 1
            return None
        data = facts(base, B, C)
        _, _, _, raw_depth, t = data
        require(C and core and core != (base - 1,) and hyp(base, B, core),
                "Hyp admits an empty/neutral singleton core or fails after stripping")
        cs = state(base, B, core)
        require((cs.e, cs.f, cs.g, cs.nb) == (s.e, s.f, s.g, s.nb)
                and s.nc == pad(base, depth, cs.nc), "core transition preservation failed")
        require(s.f == 1 - s.e and s.g in (0, 1), "Hyp binary carry relation failed")
        expected = ((C[0] + s.e) % base + (C[-1] + t) % base if s.g == 0
                    else (C[0] + s.e) % base + (base - 1) * s.e)
        require(s.nc[0] == expected, "exact center-head formula failed")
        if s.g == 1:
            require((s.nc[0] == base - 1) == (C[0] == base - 1),
                    "overflow neutral-head equivalence failed")
            self.count["overflow_neutral_head_equivalences"] += 1
            if symmetric(C):
                require(raw_depth == depth, "symmetric overflow changes center-pair depth")
                self.count["symmetric_overflow_depth_identities"] += 1
        if symmetric(C) and depth == 0:
            require(C[0] != base - 1, "symmetric Hyp core has a neutral head")
            if s.g == 0:
                require((s.nc[0] == base - 1) == trim_site(base, s.e, C[0], t),
                        "canonical symmetric local trim-site equivalence failed")
                self.count["canonical_local_site_equivalences"] += 1
        for B2, u in suffix_splits(base, s.nb):
            for C2, v in pair_splits(base, s.nc):
                self.edge(base, Edge(B, C, B2, C2, u, v), data, mirror,
                          "all_legal_partial_trim_edges")
        self.count["Hyp_source_controls"] += 1
        self.count["asymmetric_Hyp_sources"] += not symmetric(C)
        if allow_padding and self.serial % 127 == 0:
            for first, second in ((0, 0), (1, 2), (17, 4)):
                self.padding(base, B, C, first, second)
        self.serial += 1
        return data


def exhaustive_controls(control):
    serial = 0
    for base in range(2, 11):
        exteriors = ((), (1, 0), (base,), (1, 0, base))
        for width in range(4):
            for C in product(range(2 * base - 1), repeat=width):
                for B in exteriors:
                    control.source(base, B, C, width <= 2 or serial % 257 == 0,
                                   "arbitrary_center_small_sources")
                    serial += 1
        for width in (4, 5):
            for half in product(range(2 * base - 1), repeat=(width + 1) // 2):
                C = half + tuple(reversed(half[:width // 2]))
                for B in exteriors:
                    control.source(base, B, C, serial % 257 == 0,
                                   "symmetric_center_wider_sources")
                    serial += 1


def check_cycle(control, base, edges, category):
    B, C = edges[0].B, edges[0].C
    require(cycle_ok(base, edges, B, C), "independent known cycle replay failed")
    require(control.mirror.cycleOK(base, [e.mirror_data() for e in edges], list(B), list(C)),
            "known cycle/mirror disagreement")
    for edge in edges:
        data = control.source(base, edge.B, edge.C, True, "known_phase_sources", False)
        control.edge(base, edge, data, True, "known_exact_edges")
    control.count[category] += 1
    control.count["mirror_cycle_comparisons"] += 1


def known_controls(control):
    sources = control.mirror._lean_certs()
    expected = {2: 4, 4: 6, 8: 8, 11: 6, 16: 10, 17: 6, 26: 4, 32: 12}
    require({base: len(es) for base, es in sources} == expected, "source inventory changed")
    for base, rows in sources:
        edges = tuple(Edge(*(tuple(w) for w in row[:4]), row[4], row[5]) for row in rows)
        normalized = tuple(normalize_edge(base, edge) for edge in edges)
        check_cycle(control, base, edges, "known_original_cycles")
        check_cycle(control, base, normalized, "known_center_normalized_cycles")
        for old, new in zip(edges, normalized):
            q = strip_pairs(base, old.C)[1]
            q2 = strip_pairs(base, old.C2)[1]
            require(q + new.v == old.v + q2 and normalize_edge(base, new) == new,
                    "normalized edge balance/idempotence failed")
            before, after = state(base, old.B, old.C), state(base, new.B, new.C)
            require((before.e, before.f, before.g, old.B, old.B2, old.u) ==
                    (after.e, after.f, after.g, new.B, new.B2, new.u),
                    "center normalization changed exterior or stream")
            if after.g:
                require(new.v == 0, "canonical symmetric overflow center has positive trim")
                control.count["known_normalized_overflow_v_zero"] += 1
        require(sum(e.u + e.v for e in edges) == sum(e.u + e.v for e in normalized),
                "known center normalization changed cyclic gain")
        for amount in (1, 3, 17):
            padded = tuple(replace(e, C=pad(base, amount, e.C), C2=pad(base, amount, e.C2))
                           for e in edges)
            check_cycle(control, base, padded, "known_constant_padding_cycles")
            require(tuple(normalize_edge(base, e) for e in padded) == normalized,
                    "padded cycle normalized to a different center cycle")
        control.count["known_bases"] += 1
        control.count["known_original_edges"] += len(edges)


def scope_controls(control):
    edge = Edge((), (9, 10), (10,), (0,), 0, 1)
    data = control.source(10, edge.B, edge.C, True, "scope_countercontrol_sources", False)
    control.edge(10, edge, data, True, "asymmetric_overflow_countercontrol_edges")
    require(data[0].g == 1 and data[0].nc == (9, 0, 9) and data[2] == 0
            and not symmetric(edge.C) and edge.v == 1,
            "required asymmetric canonical-overflow counterexample changed")
    control.count["symmetry_premise_counterexamples"] += 1
    positive = Edge((1, 0), (14, 14), (2, 1), (), 0, 1)
    data = control.source(10, positive.B, positive.C, True, "scope_countercontrol_sources", False)
    control.edge(10, positive, data, True, "positive_site_scope_edges")
    require(not edge_ok(10, replace(positive, C2=(1,)))
            and not cycle_ok(10, (positive,), positive.B, positive.C),
            "a local trim site incorrectly certified a wrong target or closed cycle")
    control.count["local_site_not_full_edge_or_cycle_controls"] += 1
    # A neutral raw HEAD need not supply an entire removable PAIR.
    singleton = control.source(3, (1, 0, 3), (0,), True, "scope_countercontrol_sources", False)
    require(singleton[0].g == 0 and singleton[0].nc == (2,)
            and trim_site(3, singleton[0].e, 0, singleton[4])
            and tuple(pair_splits(3, singleton[0].nc)) == (((2,), 0),),
            "singleton trim-site/no-removable-pair countercontrol changed")
    control.count["singleton_site_without_positive_trim"] += 1
    for base in range(2, 11):
        for length in range(10):
            C = (base - 1,) * length
            core, q = strip_pairs(base, C)
            require(core in ((), (base - 1,)) and pad(base, q, core) == C,
                    "all-neutral even/odd core handling failed")
            for B in ((), (base,)):
                require(not hyp(base, B, C), "all-neutral center satisfies the flip")
                control.count["neutral_core_Hyp_exclusions"] += 1
        # Outside the bounded Hyp domain, only the unconditional raw symmetry
        # statement is tested; these cases are not sent to the restricted mirror.
        for B in ((), (5 * base,)):
            for C in ((), (3 * base,), (0, 4 * base, 1)):
                require(symmetric(state(base, B, C).nc), "raw arbitrary-natural symmetry failed")
                control.count["unbounded_coefficient_raw_symmetry_controls"] += 1


def malformed_controls(control):
    edge = Edge((), (9, 10), (10,), (0,), 0, 1)
    cases = [(b, edge) for b in (-1, 0, 1, True, 10.5)]
    cases += [(10, bad) for bad in (None, replace(edge, u=-1), replace(edge, v=True),
                                  replace(edge, B=(-1,)), replace(edge, C=(False,)),
                                  replace(edge, B2=(0.5,)), replace(edge, C2=(-1,)),
                                  replace(edge, C=()), replace(edge, C=(9,)),
                                  replace(edge, C=(19,)))]
    for base, candidate in cases:
        require(not edge_ok(base, candidate), "malformed edge accepted")
        require(not cycle_ok(base, (candidate,), (), (9, 10)), "malformed cycle accepted")
        control.count["malformed_checker_rejections"] += 1
    require(not cycle_ok(10, (), (), ()), "empty cycle accepted")
    control.count["empty_cycle_guard"] += 1
    requests = (
        (pad, (10, -1, ())), (pad, (10, True, ())), (pad, (10, 1, (False,))),
        (strip_pairs, (1, ())), (strip_pairs, (10, None)), (strip_pairs, (10, (-1,))),
        (norm_integer, (1, (), 0)), (norm_integer, (10, (True,), 0)),
        (norm_integer, (10, (), -1)), (facts, (10, (), ())),
        (trim_site, (10, 2, 14, 1)), (trim_site, (10, 0, 19, 1)),
        (trim_site, (10, 0, 14, True)), (normalize_edge, (10, replace(edge, v=-1))),
    )
    for operation, args in requests:
        try:
            operation(*args)
        except ValueError:
            control.count["malformed_operation_rejections"] += 1
        else:
            raise RuntimeError("malformed operation request accepted")


def main():
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("agent114_center_mirror",
                                                root / "calculation/neutral_band_search.py")
    require(spec is not None and spec.loader is not None, "repository mirror unavailable")
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    control = Controls(mirror)
    exhaustive_controls(control)
    known_controls(control)
    scope_controls(control)
    malformed_controls(control)
    print("COMPUTED center trim-site controls; bases=2..10 arbitrary C<=3, symmetric C=4..5")
    print(json.dumps(dict(sorted(control.count.items())), sort_keys=True))
    print("ALL CENTER TRIM SITE CONTROLS PASSED")


if __name__ == "__main__":
    main()
