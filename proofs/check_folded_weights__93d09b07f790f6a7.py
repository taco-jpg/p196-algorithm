#!/usr/bin/env python3
"""Literal-decimal audit of positive folded product-weight obstructions."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


def palindrome(n):
    s = str(n)
    return s == s[::-1]


def raa(n):
    return n + int(str(n)[::-1])


def pair_word(n):
    ds = tuple(map(int, str(n)))
    return tuple(a + b for a, b in zip(ds, ds[::-1]))


def reflect(half):
    return tuple(half) + tuple(half)[::-1]


def realize(half):
    digits = [0] * (2 * len(half))
    for i, q in enumerate(half):
        high = min(9, q)
        digits[i] = high
        digits[-1 - i] = q - high
    n = int("".join(map(str, digits)))
    assert pair_word(n) == reflect(half)
    return n


def predecessor_half(bits, k, d=1):
    half = [5] + [9] * (d - 1)
    for bit in bits:
        half += [14, 14, 4, 4] if bit else [9] * 4
        half += [9] * (d - 1)
    return tuple(half + [14] + [18] * k)


def target_half(r, k, d=1):
    return (11,) + (9,) * (r * (d + 3) + d) + (18,) * k


def verify_family_member(qhalf, rhalf):
    q = reflect(qhalf)
    r = reflect(rhalf)
    assert len(q) == len(r)
    assert 18 in q and 18 in r
    n = realize(qhalf)
    n1, n2 = raa(n), raa(raa(n))
    assert len(str(n1)) == len(q), "the constructed transition must not overflow"
    assert pair_word(n1) == r
    assert not palindrome(n) and not palindrome(n1) and not palindrome(n2)
    return n, n1, n2


def product(xs):
    out = 1
    for x in xs:
        out *= x
    return out


def window_potential(word):
    """One fixed, positive, translation-invariant potential at each range."""
    return 1 + (sum((i + 1) * x for i, x in enumerate(word))
                + sum(x * y for x, y in zip(word, word[1:]))) % 7


def window_weight(half, d):
    assert len(half) >= d
    width_factor = (2 * len(half) + 1) ** 2
    return width_factor * product(
        window_potential(half[i:i+d]) for i in range(len(half) - d + 1)
    )


def fraction_record(x):
    return {"numerator": x.numerator, "denominator": x.denominator}


def main():
    product_records = []
    checked = 0
    weights = [
        [1] * 19,
        [1 + (7 * x + x * x) % 11 for x in range(19)],
        [1 + (3 * x + 5) % 7 for x in range(19)],
    ]
    for r in range(11):
        for k in (1, 2, 3):
            rh = target_half(r, k)
            seen = set()
            totals = [0] * len(weights)
            digest = hashlib.sha256()
            for bits in itertools.product((0, 1), repeat=r):
                qh = predecessor_half(bits, k)
                assert qh not in seen
                seen.add(qh)
                n, n1, n2 = verify_family_member(qh, rh)
                for i, a in enumerate(weights):
                    totals[i] += product(a[x] for x in qh)
                digest.update(f"{qh};{n};{n1};{n2}\n".encode())
                checked += 1
            assert len(seen) == 2**r
            for a, total in zip(weights, totals):
                expected = a[5] * a[14] * a[18]**k * (
                    a[9]**4 + a[14]**2 * a[4]**2
                )**r
                assert total == expected
                ratio = Fraction(total, product(a[x] for x in rh))
                formula = Fraction(a[5] * a[14], a[11] * a[9]) * (
                    1 + Fraction(a[4] * a[14], a[9]**2)**2
                )**r
                assert ratio == formula
            product_records.append({
                "r": r, "k": k, "width": 2 * len(rh),
                "distinct_predecessors_checked": len(seen),
                "sha256_literal_controls": digest.hexdigest(),
            })

    range_records = []
    range_checked = 0
    for d in range(1, 6):
        z = (9,) * (d - 1) + (14, 14, 4, 4) + (9,) * (d - 1)
        beta = Fraction(
            product(window_potential(z[i:i+d]) for i in range(d + 3)),
            window_potential((9,) * d) ** (d + 3),
        )
        assert beta > 0
        for k in (1, 3):
            qzero = predecessor_half((), k, d)
            rzero = target_half(0, k, d)
            prefactor = Fraction(window_weight(qzero, d), window_weight(rzero, d))
            start_factor = Fraction(
                window_potential((5,) + (9,) * (d - 1)),
                window_potential((11,) + (9,) * (d - 1)),
            )
            end_factor = Fraction(1)
            for j in range(min(k, d - 1) + 1):
                end_factor *= Fraction(
                    window_potential((9,) * (d - 1 - j) + (14,) + (18,) * j),
                    window_potential((9,) * (d - j) + (18,) * j),
                )
            assert prefactor == start_factor * end_factor
            for r in range(7):
                rh = target_half(r, k, d)
                baseline = window_weight(predecessor_half((0,) * r, k, d), d)
                total = 0
                digest = hashlib.sha256()
                for bits in itertools.product((0, 1), repeat=r):
                    qh = predecessor_half(bits, k, d)
                    n, n1, n2 = verify_family_member(qh, rh)
                    weight = window_weight(qh, d)
                    assert Fraction(weight, baseline) == beta ** sum(bits)
                    total += weight
                    digest.update(f"{bits};{weight};{n};{n1};{n2}\n".encode())
                    range_checked += 1
                ratio = Fraction(total, window_weight(rh, d))
                assert ratio == prefactor * (1 + beta) ** r
                range_records.append({
                    "d": d, "k": k, "r": r, "width": 2 * len(rh),
                    "distinct_predecessors_checked": 2**r,
                    "beta": fraction_record(beta),
                    "prefactor": fraction_record(prefactor),
                    "incoming_subset_weight_ratio": fraction_record(ratio),
                    "sha256_literal_controls": digest.hexdigest(),
                })

    output = {
        "status": "PASS",
        "verification_level": "written all-parameter proof with literal finite integer controls; not Lean",
        "product_weight_predecessors_checked": checked,
        "finite_range_predecessors_checked": range_checked,
        "positive_product_assignments": weights,
        "product_weight_records": product_records,
        "finite_range_records": range_records,
        "scope": "A safe incoming-weight bound is obstructed. No forward-contraction or Lychrel-existence claim is made.",
    }
    path = Path(__file__).with_name("check_folded_weights.json")
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({
        "status": "PASS", "product_controls": checked,
        "finite_range_controls": range_checked, "saved": str(path),
    }, indent=2))


if __name__ == "__main__":
    main()
