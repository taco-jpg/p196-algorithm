#!/usr/bin/env python3
"""Computed regressions for Agent108's decimal alternating exterior charge.

The charge calculation is independent of the transition oracle:
    K_b(B) = 2 * sum_i (-1)^i B_i + (b-1) * (-1)^len(B).

This script uses the exact A120 Python mirror for raw transitions and edgeOK,
then checks K'=2K mod(b+1) on nonoverflow edges, K'=0 on overflow
edges, and exact invariance under every legal exterior neutral suffix trim.
It also checks ordinary integer reverse-and-add through an independently
evaluated template value and canonical base-b integer reversal.

Exhaustive scope: every valid decimal exterior of length <=4, with the
complementary center carry supplied by a one-coefficient center.  A120's
exterior transition depends on the center only through that carry.  Every
legal neutral exterior trim is included; the center trim is zero here.
Seeded wide controls and all eight existing Lean-source certificates are
additional regressions, not an exhaustive claim over their larger domains.

Run from repository root:
    python3 calculation/agent-108/charge_checks.py

These computations are distinct from the companion Lean proof.  Running
this script alone does not constitute LEAN-VERIFIED status or prove a new
certificate exists.  Other-base controls do not claim a new general-base
paper result; that research scope belongs to Agent107.
"""

from collections import Counter
from itertools import product
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror


def charge(base, exterior):
    alternating = sum(exterior[::2]) - sum(exterior[1::2])
    parity = 1 if len(exterior) % 2 == 0 else -1
    return 2 * alternating + (base - 1) * parity


def require(condition, description):
    if not condition:
        raise RuntimeError(description)


def value(base, coefficients):
    result = 0
    for coefficient in reversed(coefficients):
        result = base * result + coefficient
    return result


def reverse_integer(base, number):
    result = 0
    while number:
        number, digit = divmod(number, base)
        result = base * result + digit
    return result


def template_value(base, exterior, center, gap):
    neutral = [base - 1] * gap
    return value(base, exterior + neutral + center + neutral + exterior[::-1])


def trailing_neutral_count(base, word):
    count = 0
    for coefficient in reversed(word):
        if coefficient != base - 1:
            break
        count += 1
    return count


def paired_neutral_count(base, word):
    count = 0
    while 2 * count + 2 <= len(word):
        if word[count] != base - 1 or word[-1 - count] != base - 1:
            break
        count += 1
    return count


def raw_check(base, exterior, center):
    require(mirror.hyp(base, exterior, center), "Invalid regression source")
    overflow = mirror.gam(base, exterior, center)
    successor = mirror.nextB(base, exterior, center)
    expected = 0 if overflow else 2 * charge(base, exterior)
    require((charge(base, successor) - expected) % (base + 1) == 0,
            ("Raw charge law", base, exterior, center, overflow, successor))
    return overflow, successor, mirror.nextC(base, exterior, center)


def edge_check(base, edge, integer_gap=None):
    exterior, center, target_b, target_c, trim_b, trim_c = edge
    require(mirror.edgeOK(base, edge), ("Mirror rejected regression edge", base, edge))
    overflow, raw_b, _ = raw_check(base, exterior, center)
    require(charge(base, target_b) == charge(base, raw_b),
            ("Trim charge", base, edge))
    expected = 0 if overflow else 2 * charge(base, exterior)
    require((charge(base, target_b) - expected) % (base + 1) == 0,
            ("Edge charge law", base, edge))
    if integer_gap is not None:
        source_value = template_value(base, exterior, center, integer_gap)
        target_gap = integer_gap - overflow + trim_b + trim_c
        target_value = template_value(base, target_b, target_c, target_gap)
        require(source_value + reverse_integer(base, source_value) == target_value,
                ("Ordinary integer transition", base, edge, integer_gap))
    return overflow


def exhaustive_decimal():
    counts = Counter()
    words = [()]
    for length in range(1, 5):
        words.extend((head,) + tail for head in range(1, 19)
                     for tail in product(range(19), repeat=length - 1))
    for coefficients in words:
        exterior = list(coefficients)
        first_carry = mirror.e1(10, exterior)
        center = [18 if first_carry == 0 else 0]
        overflow, raw_b, raw_c = raw_check(10, exterior, center)
        counts["sources"] += 1
        counts[f"raw_g{overflow}"] += 1
        for trim in range(trailing_neutral_count(10, raw_b) + 1):
            target = raw_b[:-trim] if trim else raw_b[:]
            edge = (exterior, center, target, raw_c, trim, 0)
            edge_check(10, edge)
            counts["legal_trim_edges"] += 1
            counts["nonzero_trim_edges"] += int(trim > 0)
    require(counts["sources"] == 19 ** 4, "Decimal enumeration incomplete")
    print("DECIMAL_EXHAUSTIVE", dict(sorted(counts.items())))
    return counts


def neutral_corner_cases():
    counts = Counter()
    for base in (2, 4, 8, 10, 11, 16, 17, 26, 32):
        for length in range(65):
            exterior = [base - 1] * length
            center = [2 * (base - 1)]
            overflow, raw_b, raw_c = raw_check(base, exterior, center)
            require(overflow == 1, "Neutral source should overflow")
            require(charge(base, exterior) == base - 1, "Neutral charge")
            require(charge(base, raw_b) == base + 1, "Neutral successor charge")
            for trim in range(length + 1):
                target = raw_b[:-trim] if trim else raw_b[:]
                edge_check(base, (exterior, center, target, raw_c, trim, 0))
                counts["trim_edges"] += 1
            counts["sources"] += 1
    print("EMPTY_AND_NEUTRAL", dict(sorted(counts.items())))
    return counts


def known_certificates():
    counts = Counter()
    certificates = mirror._lean_certs()
    require({base for base, _ in certificates} == {2, 4, 8, 11, 16, 17, 26, 32},
            "Expected eight known certificate bases")
    for base, edges in certificates:
        require(mirror.cycleOK(base, edges, edges[0][0], edges[0][1]),
                ("Known certificate rejected", base))
        gap = 2 + sum(mirror.gam(base, edge[0], edge[1]) for edge in edges)
        for edge in edges:
            overflow = edge_check(base, edge, integer_gap=gap)
            require(charge(base, edge[0]) % (base + 1) == 0,
                    ("Known cyclic vertex charge", base, edge[0]))
            gap += edge[4] + edge[5] - overflow
            counts["edges"] += 1
            counts["integer_transitions"] += 1
        counts["bases"] += 1
        print(f"KNOWN_CERTIFICATE base={base} edges={len(edges)} cycleOK=True charge_residues=0")
    print("KNOWN_TOTAL", dict(sorted(counts.items())))
    return counts


def seeded_wide_controls():
    generator = random.Random(10820261027)
    counts = Counter()
    for index in range(10000):
        base = 10 if index % 2 == 0 else generator.randrange(2, 37)
        length = generator.randrange(81)
        exterior = [generator.randrange(2 * base - 1) for _ in range(length)]
        if exterior:
            exterior[0] = generator.randrange(1, 2 * base - 1)
        first_carry = mirror.e1(base, exterior)
        center = [generator.randrange(2 * base - 1)
                  for _ in range(generator.randrange(41))]
        center.append(2 * (base - 1) if first_carry == 0 else 0)
        overflow, raw_b, raw_c = raw_check(base, exterior, center)
        trim_b = generator.randrange(trailing_neutral_count(base, raw_b) + 1)
        trim_c = generator.randrange(paired_neutral_count(base, raw_c) + 1)
        target_b = raw_b[:-trim_b] if trim_b else raw_b[:]
        target_c = raw_c[trim_c:-trim_c] if trim_c else raw_c[:]
        edge = (exterior, center, target_b, target_c, trim_b, trim_c)
        edge_check(base, edge, integer_gap=generator.randrange(2, 13))
        padding = generator.randrange(33)
        require(charge(base, exterior + [base - 1] * padding) == charge(base, exterior),
                ("Padding invariance", base, exterior, padding))
        counts["samples"] += 1
        counts["integer_transitions"] += 1
        counts["padding_checks"] += 1
        counts[f"g{overflow}"] += 1
        counts["decimal_samples"] += int(base == 10)
    print("SEEDED_WIDE seed=10820261027", dict(sorted(counts.items())))
    return counts


def main():
    exhaustive_decimal()
    neutral_corner_cases()
    known_certificates()
    seeded_wide_controls()
    print("ALL COMPUTED CHARGE CHECKS PASSED")


if __name__ == "__main__":
    main()
