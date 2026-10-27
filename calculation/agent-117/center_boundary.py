#!/usr/bin/env python3
"""All-width NECESSARY normalized center-head/trim projection (base 10).

This is deliberately not a center or certificate checker.  A reset means that
at least one neutral pair was removed; its unseen interior is existentially
relaxed.  --drivers exhibits balanced projected loops, not actual centers.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Edge:
    e: int
    z: int
    g: int
    en: int
    zn: int
    trim: int
    inward: int


def coefficient(e: int, z: int) -> int:
    return z + 10 * (1 - e)


def head_edges(e: int, z: int, g: int) -> tuple[Edge, ...]:
    """Exact outer-column equations; trim interiors are overapproximated."""
    if e not in (0, 1) or g not in (0, 1) or not 0 <= z <= 8:
        raise ValueError("expected binary e,g and reduced head 0..8")
    if g:
        return (Edge(e, z, 1, 1 - e, z, 0, -1),)
    ans = []
    for inward in (0, 1):
        raw = 2 * z + e + inward
        if raw == 9:
            for en in (0, 1):
                for zn in range(9):
                    ans.append(Edge(e, z, 0, en, zn, 1, inward))
        else:
            en = int(raw < 9)
            zn = raw - 10 * (1 - en)
            ans.append(Edge(e, z, 0, en, zn, 0, inward))
    return tuple(ans)


def exact_trim_head_allowed(e: int, v: int, target_head: int) -> bool:
    """Exact existential target-head table, conditional on a positive trim.

    The source head must separately be 4 (e=1) or 14 (e=0).  Interior
    realizations are constructed and audited by trim_language_audit.py.
    """
    if e not in (0, 1) or type(v) is not int or v < 1:
        return False
    if target_head not in tuple(range(9)) + tuple(range(10, 19)):
        return False
    return not (v == 2 and target_head == (18 if e else 0))


def balanced_trace(E: str, G: str, repetitions: int):
    """Find a closed projected trace with integer length balance, if any.

    Any genuine normalized center loop of this temporal length projects here.
    Absence is therefore a necessary-model obstruction. Presence is ONLY a
    projection witness: it supplies no finite center word.
    """
    if not E or len(E) != len(G) or set(E + G) - {"0", "1"}:
        raise ValueError("nonempty equal-length binary driver strings required")
    if repetitions < 1:
        raise ValueError("positive repetition count required")
    es = tuple(map(int, E * repetitions))
    gs = tuple(map(int, G * repetitions))
    total_g = sum(gs)
    if total_g == 0 or total_g % 2:
        return None
    budget = total_g // 2
    for initial in range(9):
        states = {(initial, 0, False): ()}
        for t, (e, g) in enumerate(zip(es, gs)):
            en = es[(t + 1) % len(es)]
            nxt = {}
            for (z, used, accepts_two), path in sorted(states.items()):
                for edge in head_edges(e, z, g):
                    if edge.en != en or used + edge.trim > budget:
                        continue
                    accepts_two_next = accepts_two or bool(
                        edge.trim and exact_trim_head_allowed(
                            edge.e, 2, coefficient(edge.en, edge.zn)))
                    key = (edge.zn, used + edge.trim, accepts_two_next)
                    if key not in nxt:
                        nxt[key] = path + (edge,)
            states = nxt
        hits = [(used, path) for (z, used, accepts_two), path in states.items()
                if z == initial and 1 <= used <= budget
                and (budget - used != 1 or accepts_two)]
        if hits:
            used, path = min(hits, key=lambda q: q[0])
            trims = [edge.trim for edge in path]
            extra = budget - used
            if extra == 1:
                index = next(i for i, edge in enumerate(path)
                             if edge.trim and exact_trim_head_allowed(
                                 edge.e, 2, coefficient(edge.en, edge.zn)))
                trims[index] += 1
            elif extra:
                trims[trims.index(1)] += extra
            verify_projected_trace(path, trims)
            return path, trims
    return None


def verify_projected_trace(path, trims):
    if not path or len(path) != len(trims):
        raise ValueError("empty/mismatched projected loop")
    for i, (edge, v) in enumerate(zip(path, trims)):
        nxt = path[(i + 1) % len(path)]
        if (edge.en, edge.zn) != (nxt.e, nxt.z):
            raise ValueError("open projected path")
        if edge not in head_edges(edge.e, edge.z, edge.g):
            raise ValueError("invalid local projected edge")
        if type(v) is not int or v < 0 or bool(v) != bool(edge.trim):
            raise ValueError("trim count inconsistent with reset")
        if v and not exact_trim_head_allowed(edge.e, v,
                                             coefficient(edge.en, edge.zn)):
            raise ValueError("forbidden exact trim/head combination")
    if sum(edge.g for edge in path) != 2 * sum(trims):
        raise ValueError("projected center length fails to close")


def normalize(c):
    c = list(c)
    while len(c) >= 2 and c[0] == c[-1] == 9:
        c = c[1:-1]
    return c


def column_norm(c, carry):
    out = []
    for x in c:
        carry, digit = divmod(x + carry, 10)
        out.append(digit)
    return out, carry


def audit_source(c, e, g):
    """Independently normalize a full symmetric word and check projection."""
    c = normalize(c)
    if not c or c[0] == 9:
        return 0
    d, out = column_norm(c, e)
    if out != 1 - e:
        return 0
    if e != int(c[0] < 9):
        raise AssertionError("head does not determine legal input carry")
    if g:
        d = d + [9 * e]
    raw = [a + b for a, b in zip(d, reversed(d))]
    target = normalize(raw)
    v = (len(raw) - len(target)) // 2
    if not target or target[0] == 9:
        return 0
    en = int(target[0] < 9)
    if column_norm(target, en)[1] != 1 - en:
        raise AssertionError("nonneutral symmetric head should force flip")
    z = c[0] - 10 * (1 - e)
    zn = target[0] - 10 * (1 - en)
    if not any((a.en, a.zn, a.trim) == (en, zn, int(v > 0))
               for a in head_edges(e, z, g)):
        raise AssertionError((c, e, g, target, v))
    return 1


def selftest():
    import itertools
    checked = 0
    for length in range(1, 6):
        for half in itertools.product(range(19), repeat=(length + 1) // 2):
            c = half + half[:length // 2][::-1]
            for e in (0, 1):
                for g in (0, 1):
                    checked += audit_source(c, e, g)
    rng = random.Random(117)
    random_checked = 0
    for _ in range(20000):
        length = rng.randrange(1, 81)
        h = [rng.randrange(19) for _ in range((length + 1) // 2)]
        c = h + h[:length // 2][::-1]
        c = normalize(c)
        if c and c[0] != 9:
            random_checked += audit_source(c, int(c[0] < 9), rng.randrange(2))
    print(f"full_word_projection exhaustive_edges={checked} random_edges={random_checked} PASS")
    for E, G in (("10100110011", "11100010000"),
                 ("101010010101", "100010001000")):
        for k in range(1, 7):
            hit = balanced_trace(E, G, k)
            expected = len(E) == 11 or k % 2 == 0
            if bool(hit) != expected:
                raise AssertionError((E, G, k, hit))
    print("driver_projection repetitions=1..6 PASS")


def drivers():
    for name, E, G, k in (("p11", "10100110011", "11100010000", 1),
                          ("p12", "101010010101", "100010001000", 2)):
        hit = balanced_trace(E, G, k)
        if hit is None:
            print(f"{name} k={k} NO_BALANCED_PROJECTION")
            continue
        path, trims = hit
        print(f"{name} k={k} PROJECTED_ONLY steps={len(path)} G={sum(map(int, G))*k} V={sum(trims)} events={sum(a.trim for a in path)}")
        print("heads=" + ",".join(str(coefficient(a.e, a.z)) for a in path))
        print("inward=" + ",".join(str(a.inward) for a in path))
        print("trims=" + ",".join(map(str, trims)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--drivers", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
    if args.drivers or not args.selftest:
        drivers()
