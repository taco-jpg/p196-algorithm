#!/usr/bin/env python3
"""Independent arithmetic controls for neutral exterior padding.

Run from the repository root, normally or with ``python3 -O``:
    python3 calculation/agent-114/exterior_padding_controls.py

Normalization here constructs the entire positional integer before taking
quotients. The repository mirror is a separate differential control; its
``_lean_certs`` function supplies source data, never an acceptance decision.
All checks use explicit branches, including under optimized Python.
These finite COMPUTED controls are not a substitute for the Lean theorem.
"""

from collections import Counter
from dataclasses import dataclass, replace
import importlib.util
from itertools import product
import json
from pathlib import Path
import random
import sys

sys.dont_write_bytecode = True
SEED = 114


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def natural(value):
    return type(value) is int and value >= 0


def natural_word(word):
    return isinstance(word, (list, tuple)) and all(natural(x) for x in word)


def norm_integer(base, word, carry):
    """Fixed-width digits and terminal carry, using whole-word arithmetic."""
    if not natural(base) or base < 2 or not natural_word(word) or not natural(carry):
        raise ValueError("normalization requires a base >= 2 and natural inputs")
    number = 0
    for coefficient in reversed(word):
        number = number * base + coefficient
    number += carry
    digits = []
    for _ in word:
        number, digit = divmod(number, base)
        digits.append(digit)
    return tuple(digits), number


@dataclass(frozen=True)
class State:
    e1: int
    e2: int
    gam: int
    db: tuple
    dc: tuple
    dr: tuple
    next_b: tuple
    next_c: tuple


def state(base, exterior, center):
    db, e = norm_integer(base, exterior, 0)
    dc, f = norm_integer(base, center, e)
    dr, g = norm_integer(base, tuple(reversed(exterior)), f)
    if g == 0:
        next_b = tuple(x + y for x, y in zip(db, reversed(dr)))
        centered_digits = dc
    else:
        low = db + ((base - 1) * (1 - e),)
        high = (1,) + tuple(reversed(dr))
        next_b = tuple(x + y for x, y in zip(low, high))
        centered_digits = dc + ((base - 1) * (1 - f),)
    next_c = tuple(x + y for x, y in zip(centered_digits, reversed(centered_digits)))
    return State(e, f, g, db, dc, dr, next_b, next_c)


def hyp(base, exterior, center):
    if not natural(base) or base < 2:
        return False
    if not natural_word(exterior) or not natural_word(center):
        return False
    if any(x > 2 * (base - 1) for x in (*exterior, *center)):
        return False
    if exterior and exterior[0] == 0:
        return False
    _, e = norm_integer(base, exterior, 0)
    _, f = norm_integer(base, center, e)
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
        return (list(self.B), list(self.C), list(self.B2), list(self.C2), self.u, self.v)


def edge_ok(base, edge):
    """Natural-domain equivalent of edgeOK; malformed inputs return False."""
    if not isinstance(edge, Edge) or not natural(edge.u) or not natural(edge.v):
        return False
    if not natural_word(edge.B2) or not natural_word(edge.C2):
        return False
    if not hyp(base, edge.B, edge.C):
        return False
    s = state(base, edge.B, edge.C)
    neutral = base - 1
    return (
        s.next_b == tuple(edge.B2) + (neutral,) * edge.u
        and s.next_c == (neutral,) * edge.v + tuple(edge.C2) + (neutral,) * edge.v
    )


def cycle_ok(base, edges):
    if not edges:
        return False
    start = (edges[0].B, edges[0].C)
    current = start
    overflow = gain = 0
    for edge in edges:
        if (edge.B, edge.C) != current or not edge_ok(base, edge):
            return False
        overflow += state(base, edge.B, edge.C).gam
        gain += edge.u + edge.v
        current = (edge.B2, edge.C2)
    return current == start and overflow <= gain


def transport(base, edge, a, target_a, w):
    if not natural(base) or base < 2 or not all(natural(x) for x in (a, target_a, w)):
        raise ValueError("invalid padding parameters")
    if not natural(edge.u) or a + edge.u != w + target_a:
        raise ValueError("padding/trim balance is required")
    h = (base - 1,)
    return replace(edge, B=edge.B + h * a, B2=edge.B2 + h * target_a, u=w)


class Controls:
    def __init__(self, mirror):
        self.mirror = mirror
        self.count = Counter()

    def compare_state(self, base, exterior, center, independent):
        m = self.mirror
        B, C = list(exterior), list(center)
        reference = State(
            m.e1(base, B), m.e2(base, B, C), m.gam(base, B, C),
            tuple(m.DB(base, B)), tuple(m.DC(base, B, C)), tuple(m.DR(base, B, C)),
            tuple(m.nextB(base, B, C)), tuple(m.nextC(base, B, C)),
        )
        require(independent == reference, "whole-word arithmetic/mirror disagreement")
        self.count["mirror_state_comparisons"] += 1

    def identity(self, base, exterior, center, pads, category):
        require(hyp(base, exterior, center), "identity source fails Hyp")
        original = state(base, exterior, center)
        self.compare_state(base, exterior, center, original)
        self.count[category + "_sources"] += 1
        for a in pads:
            padded_b = exterior + (base - 1,) * a
            padded = state(base, padded_b, center)
            self.compare_state(base, padded_b, center, padded)
            require(hyp(base, padded_b, center), "padded Hyp failed")
            require((padded.e1, padded.e2, padded.gam) ==
                    (original.e1, original.e2, original.gam), "carry preservation failed")
            require(padded.db == original.db + ((base - 1) * (1 - original.e1),) * a,
                    "forward normalized digits failed")
            require(padded.dr == ((base - 1) * (1 - original.e2),) * a + original.dr,
                    "reverse normalized digits failed")
            require(padded.dc == original.dc, "center digits changed")
            require(padded.next_c == original.next_c, "nextC changed")
            require(padded.next_b == original.next_b + (base - 1,) * a,
                    "nextB covariance failed")
            self.count[category + "_identities"] += 1
            self.count["empty_B_identities"] += not exterior
        return original

    def equivalence(self, base, edge, a, target_a):
        w = edge.u + a - target_a
        lifted = transport(base, edge, a, target_a, w)
        before, after = edge_ok(base, edge), edge_ok(base, lifted)
        require(before == after, "edgeOK equivalence failed")
        require(self.mirror.edgeOK(base, edge.mirror_data()) == before,
                "original edge/mirror disagreement")
        require(self.mirror.edgeOK(base, lifted.mirror_data()) == after,
                "transported edge/mirror disagreement")
        self.count["true_edge_equivalences" if before else "false_edge_equivalences"] += 1
        return lifted


def exhaustive_sources(control):
    for base in range(2, 6):
        alphabet = range(2 * base - 1)
        for nb in range(3):
            for B in product(alphabet, repeat=nb):
                if B and B[0] == 0:
                    continue
                for nc in range(3):
                    for C in product(alphabet, repeat=nc):
                        if hyp(base, B, C):
                            control.identity(base, B, C, (0, 1, 2, 5), "exhaustive")


def random_sources(control):
    rng = random.Random(SEED)
    for base in range(2, 33):
        for i in range(128):
            nb = 0 if i % 8 == 0 else rng.randrange(9)
            B = tuple(rng.randrange(2 * base - 1) for _ in range(nb))
            if B:
                B = (rng.randrange(1, 2 * base - 1),) + B[1:]
            e = norm_integer(base, B, 0)[1]
            nc = rng.randrange(1, 11)
            C = [rng.randrange(2 * base - 1) for _ in range(nc)]
            # Force the required terminal carry, independently of interior carries.
            C[-1] = rng.randrange(base, 2 * base - 1) if e == 0 else rng.randrange(base - 1)
            if i % 2 == 0:
                for j in range(nc // 2):
                    C[j] = C[-1-j]
            C = tuple(C)
            s = control.identity(base, B, C, (0, 1, 3, 8), "seeded")
            if i % 4 != 0:
                continue
            suffix = 0
            while suffix < len(s.next_b) and s.next_b[-1-suffix] == base - 1:
                suffix += 1
            depth = 0
            while 2 * depth + 2 <= len(s.next_c) and s.next_c[depth] == s.next_c[-1-depth] == base - 1:
                depth += 1
            u, v = rng.randrange(suffix + 1), rng.randrange(depth + 1)
            edge = Edge(B, C, s.next_b[:len(s.next_b)-u],
                        s.next_c[v:len(s.next_c)-v] if v else s.next_c, u, v)
            require(edge_ok(base, edge), "constructed true edge rejected")
            a = rng.randrange(9)
            control.equivalence(base, edge, a, rng.randrange(edge.u + a + 1))
            mutations = (
                replace(edge, B2=edge.B2 + (0,)),
                replace(edge, C2=edge.C2 + (0,)),
                replace(edge, u=edge.u + 1),
                replace(edge, v=edge.v + 1),
                replace(edge, B=(0,) + edge.B[1:]),
            )
            for false_edge in mutations:
                require(not edge_ok(base, false_edge), "negative mutation accepted")
                control.equivalence(base, false_edge, a, rng.randrange(false_edge.u + a + 1))
        # Large finite offsets, with the empty exterior included in every base.
        control.identity(base, (), (base,), (64, 257), "large_padding")


def known_certificates(control):
    expected = {2: 4, 4: 6, 8: 8, 11: 6, 16: 10, 17: 6, 26: 4, 32: 12}
    sources = control.mirror._lean_certs()
    require({base: len(es) for base, es in sources} == expected, "known-source inventory changed")
    for base, rows in sources:
        edges = [Edge(*(tuple(x) for x in row[:4]), row[4], row[5]) for row in rows]
        require(cycle_ok(base, edges), "independent original certificate replay failed")
        control.count["known_bases"] += 1
        control.count["known_original_edges"] += len(edges)
        for edge in edges:
            for a in (0, 1, 2, 5, 9):
                for target_a in range(edge.u + a + 1):
                    control.equivalence(base, edge, a, target_a)
        old_u = [edge.u for edge in edges]
        schedules = [old_u[k:] + old_u[:k] for k in range(len(edges))]
        schedules += [[sum(old_u) if j == k else 0 for j in range(len(edges))]
                      for k in range(len(edges))]
        for new_u in schedules:
            prefixes = [0]
            for u, w in zip(old_u, new_u):
                prefixes.append(prefixes[-1] + u - w)
            require(prefixes[-1] == 0, "cycle schedule does not balance")
            for extra in (0, 3):
                offsets = [p - min(prefixes) + extra for p in prefixes]
                lifted = [control.equivalence(base, edge, offsets[i], offsets[i+1])
                          for i, edge in enumerate(edges)]
                require([edge.u for edge in lifted] == new_u, "transported trim schedule wrong")
                require(cycle_ok(base, lifted), "independent transported cycle replay failed")
                require(control.mirror.cycleOK(base, [edge.mirror_data() for edge in lifted],
                                               list(lifted[0].B), list(lifted[0].C)),
                        "transported cycle/mirror disagreement")
                require(sum(edge.u + edge.v for edge in lifted) ==
                        sum(edge.u + edge.v for edge in edges), "cyclic gain changed")
                control.count["known_transported_cycles"] += 1
                control.count["known_transported_cycle_edges"] += len(lifted)
    return sources[0][0], Edge(*(tuple(x) for x in sources[0][1][0][:4]),
                              sources[0][1][0][4], sources[0][1][0][5])


def malformed_controls(control, base, edge):
    cases = [(bad_base, edge) for bad_base in (-1, 0, 1, True)]
    cases += [(base, replace(edge, **change)) for change in (
        {"u": -1}, {"v": -1}, {"u": True}, {"v": 0.5},
        {"B": (-1,)}, {"C": (True,)}, {"B2": (-1,)}, {"C2": (0.5,)},
        {"B": (2 * base - 1,)}, {"C": (2 * base - 1,)},
    )]
    for b, candidate in cases:
        require(not edge_ok(b, candidate), "malformed acceptance guard failed")
        control.count["malformed_edge_rejections"] += 1
    for a, target_a, w in ((-1, 0, edge.u), (0, -1, edge.u),
                           (0, 0, -1), (0, 0, edge.u + 1), (True, 0, edge.u + 1)):
        try:
            transport(base, edge, a, target_a, w)
        except ValueError:
            control.count["malformed_transport_rejections"] += 1
        else:
            raise RuntimeError("invalid transport parameters accepted")


def main():
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("agent114_mirror", root / "calculation/neutral_band_search.py")
    require(spec is not None and spec.loader is not None, "repository mirror unavailable")
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    controls = Controls(mirror)
    exhaustive_sources(controls)
    random_sources(controls)
    base, edge = known_certificates(controls)
    malformed_controls(controls, base, edge)
    print("COMPUTED exterior-padding controls; seed=" + str(SEED))
    print(json.dumps(dict(sorted(controls.count.items())), sort_keys=True))
    print("ALL EXTERIOR PADDING CONTROLS PASSED")


if __name__ == "__main__":
    main()
