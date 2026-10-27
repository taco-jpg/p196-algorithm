#!/usr/bin/env python3
"""Independent integer-arithmetic audit of Agent117's center-head theorem.

No repository mirror, column normalization, or other Agent117 script is
imported.  Whole positional integers determine the normalized digit blocks.
Positive witnesses concern ONE edge only, never a common center orbit.
"""
from __future__ import annotations

import argparse
from itertools import product


HEADS = tuple(x for x in range(19) if x != 9)


def integer_edge(c, e, g):
    """Exact center edge, using one whole integer rather than carry iteration."""
    c = tuple(c)
    if not c or c != c[::-1] or c[0] == 9:
        raise ValueError("nonempty normalized symmetric source required")
    if any(type(a) is not int or not 0 <= a <= 18 for a in c):
        raise ValueError("coefficient out of range")
    if e not in (0, 1) or g not in (0, 1):
        raise ValueError("binary carry and overflow required")
    modulus = 10 ** len(c)
    value = e + sum(a * 10 ** j for j, a in enumerate(c))
    if value // modulus != 1 - e:
        raise ValueError("source fails carry flip")
    digits = tuple((value // 10 ** j) % 10 for j in range(len(c)))
    if g:
        digits += (9 * e,)
    raw = tuple(a + b for a, b in zip(digits, digits[::-1]))
    target = raw
    v = 0
    while len(target) >= 2 and target[0] == target[-1] == 9:
        target = target[1:-1]
        v += 1
    if not target or target[0] == 9:
        return None
    en = int(target[0] < 9)
    endvalue = en + sum(a * 10 ** j for j, a in enumerate(target))
    if endvalue // (10 ** len(target)) != 1 - en:
        raise AssertionError("target head did not force its carry")
    return en, target[0], v, target


def permitted(e, x, g, v, y):
    if x not in HEADS or y not in HEADS or e != int(x < 9):
        return False
    if g not in (0, 1) or type(v) is not int or v < 0:
        return False
    if g:
        return v == 0 and y == x + (10 if e else -10)
    if v == 0:
        z = x - 10 * (1 - e)
        return y in (2 * z + e, 2 * z + e + 1)
    if x != (4 if e else 14):
        return False
    if v == 2 and y == (18 if e else 0):
        return False
    return True


def carry_tile(c, left, right, inward):
    if (c + inward) // 10 != right:
        return None
    outleft = (c + left) // 10
    digit_sum = (c + left) % 10 + (c + inward) % 10
    return outleft, inward, digit_sum


def construct(e, x, g, v, y, length):
    """Realize a permitted local edge at every length >= 2*v+3."""
    if not permitted(e, x, g, v, y) or length < 2 * v + 3:
        raise ValueError("forbidden head edge or insufficient witness length")
    if g:
        return (x,) + (0,) * (length - 2) + (x,)
    if v == 0:
        for inward in (0, 1):
            if carry_tile(x, e, 1 - e, inward)[2] == y:
                return (x,) + (18 * inward,) * (length - 2) + (x,)
        raise AssertionError("permitted nontrim edge lacks inward carry")
    if v == 1:
        prefix = (x,)
    elif v == 2:
        prefix = (x, x)
    else:
        prefix = (x, x) + (9,) * (v - 3) + (18 - x,)
    left, right = e, 1 - e
    for c in prefix:
        tiles = [carry_tile(c, left, right, h) for h in (0, 1)]
        tiles = [t for t in tiles if t is not None and t[2] == 9]
        if len(tiles) != 1:
            raise AssertionError("trim prefix is not a unique neutral tile")
        left, right, _ = tiles[0]
    for c in range(19):
        for inward in (0, 1):
            tile = carry_tile(c, left, right, inward)
            if tile is not None and tile[2] == y:
                inner = ((c,) + (18 * inward,) * (length - 2 * v - 2)
                         + (c,))
                return prefix + inner + prefix[::-1]
    raise AssertionError("permitted reset edge lacks a core")


def construct_with_invariants(e, x, g, v, y, length):
    """Also enforce every applicable odd-center cycle invariant.

    Every even length >=2v+4 and every odd length >=2v+5 is allowed.
    The middle symbol of an odd source is even and its alternating sum is
    9 modulo11.  Reset digits nearest the fixed prefix isolate that interior
    adjustment from the already determined outer carry equations.
    """
    if length < 2 * v + (5 if length % 2 else 4):
        raise ValueError("insufficient length for invariant-compatible core")
    raw_witness = construct(e, x, g, v, y, length)
    outside = raw_witness[:v + 1]
    inward = raw_witness[v + 1] // 18
    inner_length = length - 2 * len(outside)
    if length % 2 == 0:
        inner = (10 * inward,) * inner_length
        return outside + inner + outside[::-1]
    for reset in (range(10, 19) if inward else range(9)):
        for middle in range(0, 19, 2):
            inner = [reset] + [0] * (inner_length - 2) + [reset]
            inner[inner_length // 2] = middle
            candidate = outside + tuple(inner) + outside[::-1]
            if sum((-1) ** j * c for j, c in enumerate(candidate)) % 11 == 9:
                return candidate
    raise AssertionError("residue-covering core construction failed")


def check_odd_invariants(c):
    if len(c) % 2:
        if c[len(c) // 2] % 2 or sum((-1) ** j * a for j, a in enumerate(c)) % 11 != 9:
            raise AssertionError(("odd-center invariant", c))


def tile_audit():
    expected = {
        (1, 0, 4, 0, 0), (1, 0, 9, 1, 0),
        (0, 0, 4, 0, 1), (0, 1, 9, 0, 1),
        (0, 1, 14, 1, 1), (1, 1, 14, 1, 0),
    }
    observed = set()
    for left, right, c, inward in product(range(2), range(2), range(19), range(2)):
        tile = carry_tile(c, left, right, inward)
        if tile is not None and tile[2] == 9:
            observed.add((left, right, c, tile[0], tile[1]))
    if observed != expected:
        raise AssertionError((observed, expected))
    print(f"neutral_tile_audit triples={len(observed)} PASS")


def exhaustive(max_length):
    sources = 0
    edges = 0
    broken_targets = 0
    for n in range(1, max_length + 1):
        for half in product(range(19), repeat=(n + 1) // 2):
            if half[0] == 9:
                continue
            c = half + half[:n // 2][::-1]
            e = int(c[0] < 9)
            sources += 1
            for g in (0, 1):
                out = integer_edge(c, e, g)
                if out is None:
                    broken_targets += 1
                    continue
                en, y, v, _ = out
                if not permitted(e, c[0], g, v, y) or en != int(y < 9):
                    raise AssertionError((c, e, g, out))
                edges += 1
    print(f"integer_exhaustive max_length={max_length} sources={sources} accepted_edges={edges} invalid_targets={broken_targets} PASS")


def constructive(max_trim):
    instances = 0
    local_classes = 0
    for x in HEADS:
        e = int(x < 9)
        for g in (0, 1):
            for v in range(max_trim + 1):
                for y in HEADS:
                    if not permitted(e, x, g, v, y):
                        continue
                    local_classes += 1
                    for extra in (3, 4, 9):
                        n = 2 * v + extra
                        c = construct(e, x, g, v, y, n)
                        out = integer_edge(c, e, g)
                        if len(c) != n or out is None or out[:3] != (int(y < 9), y, v):
                            raise AssertionError((e, x, g, v, y, n, c, out))
                        if len(out[3]) != n + g - 2 * v:
                            raise AssertionError("length identity fails")
                        instances += 1
    print(f"constructive_integer_audit max_trim={max_trim} local_classes={local_classes} witnesses={instances} PASS")


def invariant_constructive(max_trim):
    tested = 0
    for x in HEADS:
        e = int(x < 9)
        for g in (0, 1):
            for v in range(max_trim + 1):
                for y in HEADS:
                    if not permitted(e, x, g, v, y):
                        continue
                    for extra in (4, 5, 10, 11, 31):
                        n = 2 * v + extra
                        c = construct_with_invariants(e, x, g, v, y, n)
                        out = integer_edge(c, e, g)
                        check_odd_invariants(c)
                        if len(c) != n or out is None or out[:3] != (int(y < 9), y, v):
                            raise AssertionError(("invariant constructor", e, x, g, v, y, n, c, out))
                        check_odd_invariants(out[3])
                        tested += 1
    print(f"invariant_constructor max_trim={max_trim} prescribed_length_witnesses={tested} PASS")


def driver_lifts():
    # Exact projected loops supplied by the independently written head search.
    # Each row is lifted separately; the finite centers are NOT one orbit.
    rows = [
        ("p11", "10100110011", "11100010000",
         (4,14,4,14,11,2,5,15,10,0,1), (0,0,0,2,0,0,0,0,0,0,0), 12),
        ("p12k2", "101010010101" * 2, "100010001000" * 2,
         (2,12,5,12,4,14,13,6,14,4,10,1,3,13,6,13,6,16,13,6,14,4,10,0),
         (0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), 20),
    ]
    for label, E, G, heads, trims, start_length in rows:
        sources = []
        targets = []
        lengths = []
        length = start_length
        for i, (ee, gg, v, x) in enumerate(zip(E, G, trims, heads)):
            e, g = int(ee), int(gg)
            y = heads[(i + 1) % len(heads)]
            c = construct_with_invariants(e, x, g, v, y, length)
            out = integer_edge(c, e, g)
            check_odd_invariants(c)
            if out is None or out[:3] != (int(E[(i + 1) % len(E)]), y, v):
                raise AssertionError((label, i, c, out))
            check_odd_invariants(out[3])
            sources.append(c)
            targets.append(out[3])
            lengths.append(length)
            length += g - 2 * v
            if len(out[3]) != length:
                raise AssertionError("projected length mismatch")
        if length != start_length:
            raise AssertionError("projected lengths do not close")
        inconsistent = sum(t != sources[(i + 1) % len(sources)]
                           for i, t in enumerate(targets))
        if inconsistent == 0:
            raise AssertionError("unexpected full center cycle: inspect immediately")
        print(f"driver_local_lifts label={label} edges={len(sources)} initial_length={start_length} min_length={min(lengths)} max_length={max(lengths)} unequal_full_interfaces={inconsistent} PROJECTED_ONLY")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=7)
    parser.add_argument("--max-trim", type=int, default=20)
    args = parser.parse_args()
    if not 1 <= args.max_length <= 8 or not 1 <= args.max_trim <= 100:
        parser.error("audit bounds: 1 <= max-length <= 8; 1 <= max-trim <= 100")
    tile_audit()
    exhaustive(args.max_length)
    constructive(args.max_trim)
    invariant_constructive(args.max_trim)
    driver_lifts()
