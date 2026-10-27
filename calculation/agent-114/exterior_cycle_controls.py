#!/usr/bin/env python3
"""COMPUTED controls for whole-chain exterior-padding transport.

Run normally and with optimized Python from the repository root:
    python3 calculation/agent-114/exterior_cycle_controls.py
    python3 -O calculation/agent-114/exterior_cycle_controls.py

The prior exterior_padding_controls module supplies its independent whole-
integer normalization and single-edge arithmetic, explicitly reused here.
The chain/cycle verifier and all-Nat schedule construction below are separate
implementations. The repository mirror is a differential control and source-
fixture reader only. Agent7's padding and Agent107's retiming arguments are
credited; these finite checks are not a new theorem or certificate discovery.
Every acceptance and input guard remains active under Python -O.
"""

from collections import Counter
from dataclasses import replace
import importlib.util
from math import comb
from pathlib import Path
import random
import sys
import json

sys.dont_write_bytecode = True
import exterior_padding_controls as arithmetic

Edge = arithmetic.Edge
require = arithmetic.require
natural = arithmetic.natural
natural_word = arithmetic.natural_word
SEED = 114002


def edge_shape(edge):
    return (isinstance(edge, Edge)
            and all(natural_word(w) for w in (edge.B, edge.C, edge.B2, edge.C2))
            and natural(edge.u) and natural(edge.v))


def chain_shape(base, edges, B, C):
    return (natural(base) and isinstance(edges, (list, tuple))
            and all(edge_shape(edge) for edge in edges)
            and natural_word(B) and natural_word(C))


def literal_chain_ok(base, edges, B, C):
    """Literal chained-source/edge check, including the empty-chain case."""
    if not chain_shape(base, edges, B, C):
        return False
    current_b, current_c = tuple(B), tuple(C)
    for edge in edges:
        if tuple(edge.B) != current_b or tuple(edge.C) != current_c:
            return False
        if not arithmetic.edge_ok(base, edge):
            return False
        current_b, current_c = tuple(edge.B2), tuple(edge.C2)
    return True


def endpoints(edges, B, C):
    """The Lean endpoint functions ignore intermediate chain validity."""
    result_b, result_c = tuple(B), tuple(C)
    for edge in edges:
        result_b, result_c = tuple(edge.B2), tuple(edge.C2)
    return result_b, result_c


def literal_cycle_ok(base, edges, B, C):
    if not chain_shape(base, edges, B, C) or not edges:
        return False
    if not literal_chain_ok(base, edges, B, C):
        return False
    if endpoints(edges, B, C) != (tuple(B), tuple(C)):
        return False
    overflow = sum(arithmetic.state(base, edge.B, edge.C).gam for edge in edges)
    return overflow <= sum(edge.u + edge.v for edge in edges)


def transport_chain(base, edges, offsets, target_u):
    """Require the natural domain, exact lengths, and every local balance."""
    if not natural(base) or base < 2:
        raise ValueError("transport base must be a natural at least two")
    if not isinstance(edges, (list, tuple)) or not all(edge_shape(e) for e in edges):
        raise ValueError("malformed edge list")
    if not natural_word(offsets) or not natural_word(target_u):
        raise ValueError("offsets and trims must be natural lists")
    if len(offsets) != len(edges) + 1 or len(target_u) != len(edges):
        raise ValueError("phase/edge lengths disagree")
    if any(offsets[i] + e.u != target_u[i] + offsets[i + 1]
           for i, e in enumerate(edges)):
        raise ValueError("local padding/trim balance fails")
    return tuple(arithmetic.transport(base, replace(e, B=tuple(e.B), B2=tuple(e.B2)),
                                      offsets[i], offsets[i + 1], target_u[i])
                 for i, e in enumerate(edges))


def all_nat_offsets(old_u, target_u, extra=0):
    """a_i = prefix(old_u,i) + suffix(target_u,i) + extra, without subtraction."""
    if not natural_word(old_u) or not natural_word(target_u) or not natural(extra):
        raise ValueError("schedules and reserve must be natural")
    if len(old_u) != len(target_u) or sum(old_u) != sum(target_u):
        raise ValueError("equal schedule length and total are required")
    prefix = [0]
    for u in old_u:
        prefix.append(prefix[-1] + u)
    suffix = [0] * (len(target_u) + 1)
    for i in range(len(target_u) - 1, -1, -1):
        suffix[i] = target_u[i] + suffix[i + 1]
    return tuple(p + s + extra for p, s in zip(prefix, suffix))


def compositions(total, length):
    """All weak compositions, with the unique empty zero-total schedule."""
    if length == 0:
        if total == 0:
            yield ()
        return
    for first in range(total + 1):
        for rest in compositions(total - first, length - 1):
            yield (first,) + rest


class Controls:
    def __init__(self, mirror):
        self.mirror = mirror
        self.count = Counter()
        self.rng = random.Random(SEED)

    def offsets(self, old_u, target_u, extra):
        offsets = all_nat_offsets(old_u, target_u, extra)
        # Separate slice-sum specification checks both scans and every phase.
        expected = tuple(sum(old_u[:i]) + sum(target_u[i:]) + extra
                         for i in range(len(old_u) + 1))
        require(offsets == expected, "prefix/suffix offset construction disagrees")
        require(offsets[0] == offsets[-1] == sum(old_u) + extra,
                "offset endpoints do not close")
        require(all(offsets[i] + u == target_u[i] + offsets[i + 1]
                    for i, u in enumerate(old_u)), "offset recurrence failed")
        self.count["schedule_offset_constructions"] += 1
        return offsets

    def random_offsets(self, edges):
        offsets = [self.rng.randrange(17)]
        new_u = []
        for edge in edges:
            following = self.rng.randrange(offsets[-1] + edge.u + 1)
            new_u.append(offsets[-1] + edge.u - following)
            offsets.append(following)
        return tuple(offsets), tuple(new_u)

    def check(self, base, edges, B, C, offsets, target_u, category):
        lifted = transport_chain(base, edges, offsets, target_u)
        padded_start = tuple(B) + (base - 1,) * offsets[0]
        before = literal_chain_ok(base, edges, B, C)
        after = literal_chain_ok(base, lifted, padded_start, C)
        require(before == after, "whole-chain acceptance equivalence failed")
        self.count["chain_true_iff" if before else "chain_false_iff"] += 1
        self.count[category] += 1
        if not edges:
            self.count["empty_chain_iff"] += 1
        original_end_b, original_end_c = endpoints(edges, B, C)
        require(endpoints(lifted, padded_start, C) ==
                (original_end_b + (base - 1,) * offsets[-1], original_end_c),
                "exact endpoint identities failed")
        self.count["endpoint_identities"] += 1
        old_gain = sum(e.u + e.v for e in edges)
        new_gain = sum(e.u + e.v for e in lifted)
        require(offsets[0] + old_gain == new_gain + offsets[-1],
                "open-chain gain telescope failed")
        self.count["gain_identities"] += 1
        original_stream, lifted_stream = [], []
        for old, new in zip(edges, lifted):
            require(arithmetic.hyp(base, old.B, old.C), "stream fixture source fails Hyp")
            require(new.C == old.C and new.C2 == old.C2 and new.v == old.v,
                    "center or center trim changed")
            a = arithmetic.state(base, old.B, old.C)
            b = arithmetic.state(base, new.B, new.C)
            original_stream.append((a.e1, a.e2, a.gam))
            lifted_stream.append((b.e1, b.e2, b.gam))
            self.count["edge_stream_identities"] += 1
        require(original_stream == lifted_stream, "exact carry/overflow stream changed")
        require(sum(s[2] for s in original_stream) == sum(s[2] for s in lifted_stream),
                "total overflow changed")
        self.count["overflow_sum_identities"] += 1
        old_cycle = literal_cycle_ok(base, edges, B, C)
        new_cycle = literal_cycle_ok(base, lifted, padded_start, C)
        for candidate, start_b, answer in ((edges, B, old_cycle),
                                           (lifted, padded_start, new_cycle)):
            reference = self.mirror.cycleOK(base, [e.mirror_data() for e in candidate],
                                            list(start_b), list(C))
            require(answer == reference, "independent cycle/mirror disagreement")
            self.count["mirror_cycle_comparisons"] += 1
        if offsets[0] == offsets[-1]:
            require(old_cycle == new_cycle, "closed-offset cycle equivalence failed")
            self.count["cycle_true_iff" if old_cycle else "cycle_false_iff"] += 1
        return lifted


def exercise_chain(control, base, edges, B, C, category):
    offsets, new_u = control.random_offsets(edges)
    require(literal_chain_ok(base, edges, B, C), "positive chain fixture rejected")
    control.check(base, edges, B, C, offsets, new_u, category)
    if not edges:
        return
    false_cases = [(edges, B + (0,), C), (edges, B, C + (0,))]
    k = control.rng.randrange(len(edges))
    for field in ("B2", "C2"):
        changed = list(edges)
        changed[k] = replace(edges[k], **{field: getattr(edges[k], field) + (0,)})
        false_cases.append((tuple(changed), B, C))
    for bad_edges, bad_b, bad_c in false_cases:
        require(not literal_chain_ok(base, bad_edges, bad_b, bad_c),
                "negative chain fixture unexpectedly accepted")
        control.check(base, bad_edges, bad_b, bad_c, offsets, new_u, "negative_chain_cases")


def known_controls(control):
    expected = {2: 4, 4: 6, 8: 8, 11: 6, 16: 10, 17: 6, 26: 4, 32: 12}
    sources = control.mirror._lean_certs()
    require({b: len(rows) for b, rows in sources} == expected, "source inventory changed")
    first = None
    for base, rows in sources:
        edges = tuple(Edge(*(tuple(w) for w in row[:4]), row[4], row[5]) for row in rows)
        if first is None:
            first = (base, edges)
        B, C = edges[0].B, edges[0].C
        require(literal_cycle_ok(base, edges, B, C), "original source certificate rejected")
        old_u = tuple(e.u for e in edges)
        require(sum(old_u) == 2, "source trim budget changed")
        schedules = tuple(compositions(2, len(edges)))
        require(len(schedules) == comb(len(edges) + 1, 2) == len(set(schedules)),
                "composition enumeration omitted or duplicated a schedule")
        control.count["known_bases"] += 1
        control.count["known_original_edges"] += len(edges)
        control.count["all_equal_total_schedules"] += len(schedules)
        for target in schedules:
            for extra in (0, 5):
                offsets = control.offsets(old_u, target, extra)
                lifted = control.check(base, edges, B, C, offsets, target, "exhaustive_schedule_cycles")
                require(tuple(e.u for e in lifted) == target, "prescribed schedule changed")
                require(literal_cycle_ok(base, lifted, lifted[0].B, C),
                        "retimed source certificate rejected")
                control.count["exhaustive_schedule_edges"] += len(edges)
        target = (sum(old_u),) + (0,) * (len(edges) - 1)
        offsets = control.offsets(old_u, target, 1024)
        control.check(base, edges, B, C, offsets, target, "large_reserve_cycles")
        for phase in range(len(edges)):
            rotated = edges[phase:] + edges[:phase]
            for length in range(len(edges) + 1):
                exercise_chain(control, base, rotated[:length], rotated[0].B, rotated[0].C,
                               "known_rotated_prefixes")
        # Individually accepted edges with incorrect links, preserving every local Hyp.
        disconnected = (edges[0], edges[0])
        require(all(arithmetic.edge_ok(base, e) for e in disconnected), "bad local fixture")
        require(not literal_chain_ok(base, disconnected, B, C), "disconnected fixture joined")
        target = tuple(e.u for e in disconnected)
        control.check(base, disconnected, B, C, (3, 3, 3), target, "disconnected_chain_cases")
    return first


def random_controls(control):
    rng = control.rng
    for base in range(2, 33):
        for trial in range(32):
            size = 0 if trial % 8 == 0 else rng.randrange(1, 9)
            B = tuple(rng.randrange(2 * base - 1) for _ in range(size))
            if B:
                B = (rng.randrange(1, 2 * base - 1),) + B[1:]
            carry = arithmetic.norm_integer(base, B, 0)[1]
            C = [rng.randrange(2 * base - 1) for _ in range(rng.randrange(1, 9))]
            C[-1] = rng.randrange(base, 2 * base - 1) if carry == 0 else rng.randrange(base - 1)
            C = tuple(C)
            start_b, start_c = B, C
            edges = []
            for _ in range(trial % 17):
                if not arithmetic.hyp(base, B, C):
                    break
                s = arithmetic.state(base, B, C)
                suffix = depth = 0
                while suffix < len(s.next_b) and s.next_b[-1-suffix] == base - 1:
                    suffix += 1
                while 2 * depth + 2 <= len(s.next_c) and s.next_c[depth] == s.next_c[-1-depth] == base - 1:
                    depth += 1
                u, v = rng.randrange(suffix + 1), rng.randrange(depth + 1)
                B2 = s.next_b[:len(s.next_b)-u]
                C2 = s.next_c[v:len(s.next_c)-v] if v else s.next_c
                edges.append(Edge(B, C, B2, C2, u, v))
                B, C = B2, C2
            exercise_chain(control, base, tuple(edges), start_b, start_c, "seeded_chains")
            if not start_b:
                control.count["seeded_empty_B_sources"] += 1
    # Arithmetic-only controls also cover natural counters far beyond machine words.
    for length in range(9):
        old = tuple((i + 1) * 10 ** 80 for i in range(length))
        control.offsets(old, tuple(reversed(old)), 10 ** 120)
        control.count["unbounded_integer_offset_controls"] += 1


def malformed_controls(control, base, edges):
    edge = edges[0]
    B, C = edge.B, edge.C
    listed = tuple(Edge(*(list(w) for w in (e.B, e.C, e.B2, e.C2)), e.u, e.v)
                   for e in edges)
    control.check(base, listed, B, C, (2,) * (len(edges) + 1),
                  tuple(e.u for e in edges), "list_word_representation_controls")
    mutations = ({"u": -1}, {"v": -1}, {"u": True}, {"v": 0.5},
                 {"B": (-1,)}, {"C": (True,)}, {"B2": (-1,)}, {"C2": (0.5,)})
    malformed = [(base, (replace(edge, **m),), B, C) for m in mutations]
    malformed += [(b, (edge,), B, C) for b in (-1, True, 2.5)]
    malformed += [(base, None, B, C), (base, (None,), B, C),
                  (base, (edge,), (-1,), C), (base, (edge,), B, (False,))]
    for b, es, start_b, start_c in malformed:
        require(not literal_chain_ok(b, es, start_b, start_c), "malformed chain accepted")
        require(not literal_cycle_ok(b, es, start_b, start_c), "malformed cycle accepted")
        control.count["malformed_checker_rejections"] += 1
    for b in (0, 1, 2, 10):
        require(literal_chain_ok(b, (), (), ()), "empty chain semantics changed")
        require(not literal_cycle_ok(b, (), (), ()), "empty cycle accepted")
        control.count["empty_semantic_guards"] += 1
    schedule_cases = ((None, (), 0), ((), None, 0), ((-1,), (-1,), 0),
                      ((True,), (1,), 0), ((1,), (1.0,), 0), ((1,), (), 0),
                      ((1,), (0,), 0), ((1,), (1,), -1), ((1,), (1,), True))
    for old, new, extra in schedule_cases:
        try:
            all_nat_offsets(old, new, extra)
        except ValueError:
            control.count["malformed_schedule_rejections"] += 1
        else:
            raise RuntimeError("invalid prescribed schedule accepted")
    valid = ((edge,), (0, 0), (edge.u,))
    transport_cases = [(b, *valid) for b in (-1, 0, 1, True, 2.5)]
    transport_cases += [(base, (None,), (0, 0), (edge.u,)),
                        (base, (replace(edge, u=-1),), (0, 0), (0,)),
                        (base, (edge,), (), (edge.u,)),
                        (base, (edge,), (0,), (edge.u,)),
                        (base, (edge,), (0, 0, 0), (edge.u,)),
                        (base, (edge,), (0, 0), ()),
                        (base, (edge,), (0, 0), (edge.u, edge.u)),
                        (base, (edge,), (-1, 0), (edge.u,)),
                        (base, (edge,), (True, 0), (edge.u,)),
                        (base, (edge,), (0, 0), (-1,)),
                        (base, (edge,), (0, 0), (True,)),
                        (base, (edge,), (0, 0), (edge.u + 1,)),
                        (base, (), (0, 1), ())]
    for b, es, offsets, target in transport_cases:
        try:
            transport_chain(b, es, offsets, target)
        except ValueError:
            control.count["malformed_transport_rejections"] += 1
        else:
            raise RuntimeError("invalid chain transport accepted")


def main():
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("agent114_cycle_mirror",
                                                root / "calculation/neutral_band_search.py")
    require(spec is not None and spec.loader is not None, "repository mirror unavailable")
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    control = Controls(mirror)
    base, edges = known_controls(control)
    random_controls(control)
    malformed_controls(control, base, edges)
    print("COMPUTED exterior-cycle controls; seed=" + str(SEED))
    print(json.dumps(dict(sorted(control.count.items())), sort_keys=True))
    print("ALL EXTERIOR CYCLE CONTROLS PASSED")


if __name__ == "__main__":
    main()
