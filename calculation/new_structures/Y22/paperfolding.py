#!/usr/bin/env python3
"""Independent canonical-decimal controls for the paper-folding U-word shard.

Run from the repository root:
    python3 calculation/new_structures/Y22/paperfolding.py

The proof of the fixed-collar obstruction is in REPORT.md. This script is a
reproducible ordinary-integer/digit-array diagnostic, not the proof itself.
"""
from pathlib import Path
import json
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

LAT = (Path(__file__).resolve().parents[2]
       / "decimal_frontier/lattice_kinks/data/lat_p12m9.txt")


def load_root():
    lines = LAT.read_text().strip().splitlines()
    p, bwidth, m, base = map(int, lines[0].split())
    assert (p, bwidth, m, base) == (12, 34, 9, 10)
    gamma = list(map(int, lines[1].split()))
    rows = [list(map(int, lines[2 + i].split())) for i in range(p)]
    roots = [list(map(int, lines[2 + 2*p + i].split())) for i in range(p)]
    assert gamma == [1, 0, 0, 0] * 3
    assert len(rows[0]) == 9 and len(roots[0]) == 34
    return roots[0], rows[0]


def paperfolding_bit(i):
    """Regular paper-folding word, zero-indexed: odd part of i+1 is 1 mod 4."""
    n = i + 1
    while n % 2 == 0:
        n //= 2
    return int(n % 4 == 1)


def coded_word(k):
    a, b = (9, 0, 18), (9, 2, 16)
    out = []
    for i in range(k):
        out.extend(b if paperfolding_bit(i) else a)
    return out


def template(root, row, q, k, junction=(5,), centre=(10,)):
    half = root + row*q + list(junction) + coded_word(k)
    assert list(centre) == list(centre)[::-1]
    return half + list(centre) + half[::-1]


def realize(pairword):
    """Canonical LSD-first digit vector whose symmetric sums are pairword."""
    assert pairword == pairword[::-1]
    digits = [0] * len(pairword)
    for i in range(len(pairword)//2):
        digits[i] = max(pairword[i] - 9, 0)
        digits[-1-i] = min(pairword[i], 9)
    if len(digits) % 2:
        middle = pairword[len(digits)//2]
        assert middle % 2 == 0
        digits[len(digits)//2] = middle // 2
    assert digits[-1] > 0 and all(0 <= d <= 9 for d in digits)
    return digits


def digits_to_int(digits):
    n = 0
    for digit in reversed(digits):
        n = 10*n + digit
    return n


def digit_array_step(digits):
    """Schoolbook digit-vector addition of N and reverse(N), no in-place writes."""
    out, carry, n = [], 0, len(digits)
    for i in range(n):
        z = digits[i] + digits[n-1-i] + carry
        out.append(z % 10)
        carry = z // 10
    if carry:
        out.append(carry)
    return out


def integer_step(n):
    return n + int(str(n)[::-1])


def integer_pairword(n):
    s = str(n)
    return [int(s[i]) + int(s[-1-i]) for i in range(len(s))]


def main():
    root, row = load_root()
    clock = [1, 0, 0, 0] * 30
    for q, k in ((20, 20), (40, 40), (80, 80), (160, 160)):
        source = template(root, row, q, k)
        target = template(root, row, q, k+5)
        digits = realize(source)
        n = digits_to_int(digits)
        assert integer_pairword(n) == source
        overflows, palindromes = [], []
        for t in range(120):
            if digits == digits[::-1]:
                palindromes.append(t)
            next_integer = integer_step(n)
            next_digits = digit_array_step(digits)
            assert digits_to_int(next_digits) == next_integer, (q, k, t)
            assert len(next_digits)-len(digits) == len(str(next_integer))-len(str(n)), (q, k, t)
            overflows.append(len(next_digits)-len(digits))
            n, digits = next_integer, next_digits
        if digits == digits[::-1]:
            palindromes.append(120)
        got = integer_pairword(n)
        first = next((i for i, (x, y) in enumerate(zip(got, target)) if x != y), None)
        if first is None and len(got) != len(target):
            first = min(len(got), len(target))
        mismatch_count = sum(x != y for x, y in zip(got, target)) + abs(len(got)-len(target))
        assert overflows == clock and sum(overflows) == 30
        assert not palindromes
        assert got != target
        print(json.dumps({
            "q": q, "k": k, "source_digits": len(source),
            "target_digits": len(target), "clock_exact": overflows == clock,
            "overflows": sum(overflows), "return": got == target,
            "first_mismatch": first, "mismatch_count": mismatch_count,
            "palindrome_times_0_to_120": palindromes,
            "int_vs_digit_array_steps_checked": 120,
        }, sort_keys=True))
    print("PAPERFOLDING_DECIMAL_CONTROLS_PASS")


if __name__ == "__main__":
    main()
