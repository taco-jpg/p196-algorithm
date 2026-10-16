#!/usr/bin/env python3
"""Exact two-path finite witness verifier for Group I (u,v,r)=(1,7,3).

No external dependencies. This is FINITE arithmetic evidence only, not Lean.

Usage:
  python3 -B verify_core17_r3.py --write finite_evidence.json
  python3 -B verify_core17_r3.py --check finite_evidence.json
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path

R, P, U, V = 3, 1, 1, 7
L = 2 * R + 7


def original_initial_word() -> tuple[int, ...]:
    """Literal DelayedOverlapGate.fiveWord/initial, columns low to high."""
    out = []
    for i in range(L):
        if i in (0, 1, 2*R+5, 2*R+6):
            c = P
        elif i in (R+1, R+5):
            c = U
        elif i in (R+2, R+4):
            c = U+V
        elif i == R+3:
            c = 2*V
        else:
            c = 0
        out.append(c)
    return tuple(out)


def canonical_seed_enumeration(q: tuple[int, ...]) -> list[int]:
    """Exhaustive ordered digit splits, NOT multiplicity of the infinite Nat->Nat function tail."""
    choices = []
    for i in range(L//2):
        pairs = []
        for low in range(10):
            high = q[i] - low
            if 0 <= high <= 9 and (i != 0 or high > 0):
                pairs.append((low, high))
        choices.append(pairs)
    assert q[L//2] % 2 == 0 and 0 <= q[L//2]//2 <= 9
    result = []
    for arr in itertools.product(*choices):
        d = [0] * L
        for i, (lo, hi) in enumerate(arr):
            d[i], d[L-1-i] = lo, hi
        d[L//2] = q[L//2] // 2
        assert all(0 <= v <= 9 for v in d) and d[-1] > 0
        assert all(d[i]+d[L-1-i] == q[i] for i in range(L))
        n = sum(v * 10**i for i, v in enumerate(d))
        assert len(str(n)) == L
        result.append(n)
    return sorted(result)


def reverse_numeric(n: int) -> int:
    """Arithmetic reversal by Euclidean quotient and remainder, without strings."""
    out = 0
    while n:
        out, n = 10*out + n%10, n//10
    return out


def reverse_textual(n: int) -> int:
    """Independent implementation for comparison."""
    return int(str(n)[::-1])


def text_palindrome(n: int) -> bool:
    s = str(n)
    return s == s[::-1]


def normalize_coefficients(q: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Decimal carry recurrence, including a terminal carry/width increase."""
    digits = []
    carries = [0]
    c = 0
    for v in q:
        x = v + c
        digits.append(x % 10)
        c = x // 10
        carries.append(c)
    assert 0 <= c <= 1
    if c:
        digits.append(c)
    assert all(0 <= d <= 9 for d in digits)
    assert digits[-1] > 0
    return tuple(digits), tuple(carries)


def next_pair_word(digits: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(digits[i] + digits[len(digits)-1-i] for i in range(len(digits)))


def positional_value(digits: tuple[int, ...]) -> int:
    return sum(d * 10**i for i, d in enumerate(digits))


def build_record() -> dict:
    q = original_initial_word()
    assert q == (1, 1, 0, 0, 1, 8, 14, 8, 1, 0, 0, 1, 1)
    assert q == q[::-1] and all(0 <= v <= 18 for v in q)
    seeds = canonical_seed_enumeration(q)
    assert len(seeds) == 36 and len(set(seeds)) == 36
    # Direct ordinary integer reverse-add, for all 36 canonical seeds.
    ref_orbit = None
    for seed in seeds:
        value = seed
        seq = [value]
        for t in range(1, 12):
            assert reverse_numeric(value) == reverse_textual(value)
            value += reverse_numeric(value)
            seq.append(value)
        assert all(not text_palindrome(x) for x in seq[1:11])
        assert text_palindrome(seq[11])
        if ref_orbit is None:
            ref_orbit = seq
        else:
            assert seq[1:] == ref_orbit[1:]
    assert ref_orbit is not None
    assert ref_orbit[0] == 1000007810010
    assert ref_orbit[1] == 1100194810011
    assert ref_orbit[11] == 8819059559509188
    # Independently reconstruct all eleven transitions from canonical
    # mirrored pair coefficients and decimal carries. This uses neither
    # textual nor arithmetic reversal of the integer at any transition.
    pair = q
    column_trace = []
    for time in range(11):
        normal_digits, carries = normalize_coefficients(pair)
        ordinary_out = positional_value(normal_digits)
        assert ordinary_out == ref_orbit[time+1]
        row = {
            "transition": time+1,
            "source_pair_width": len(pair),
            "source_pair_low_to_high": list(pair),
            "incoming_carries_at_0_to_width": list(carries),
            "output_digits_low_to_high": list(normal_digits),
            "output_ordinary_integer": str(ordinary_out),
            "output_width": len(normal_digits),
        }
        pair = next_pair_word(normal_digits)
        column_trace.append(row)
    # Explicit split-count proof by product, counting integer digit words,
    # not unconstrained Nat->Nat representation tails.
    pair_counts = [sum(0 <= q[i]-low <= 9 and (i != 0 or q[i]-low > 0)
                       for low in range(10)) for i in range(L//2)]
    assert pair_counts == [1, 2, 1, 1, 2, 9]
    assert __import__('math').prod(pair_counts) == len(seeds)
    record = {
        "schema_version": 1,
        "agent": "Agent #114, independent s2124Z session",
        "scope": "original Group I core (u,v)=(1,7), r=3 only",
        "source": {"label": "renewal_pass/tails/STATUS.md, remaining cases",
                   "historical_blob": "00f3e3fed54ee8f3823038b10289523d2a2f1aa8",
                   "description": "old finite observation, not a claim of novelty"},
        "evidence_level": "TWO EXACT FINITE ARITHMETIC ALGORITHMS; NOT LEAN-CHECKED",
        "all_time_claim": False,
        "input_pair_width": L,
        "initial_pair_word_low_to_high": list(q),
        "ordered_digit_pair_choices_per_half_column": pair_counts,
        "canonical_decimal_seed_count": len(seeds),
        "canonical_integer_seeds_as_decimal_strings": [str(s) for s in seeds],
        "representative_seed": str(ref_orbit[0]),
        "representative_orbit_times_0_to_11": [str(x) for x in ref_orbit],
        "positive_time_first_palindrome": 11,
        "palindrome_at_11": str(ref_orbit[11]),
        "earlier_positive_times_all_nonpalindromic": True,
        "all_canonical_integer_seeds_agree_after_one_step": True,
        "independent_column_normalization_transitions": column_trace,
        "seed_list_sha256": hashlib.sha256(
            ("\n".join(str(s) for s in seeds)+"\n").encode()
        ).hexdigest(),
        "scope_limit": "Only 36 finite 13-digit canonical integer seeds; proves no other r, no infinite orbit statement, and no claim about 196",
    }
    return record


def canonical_bytes(record: dict) -> bytes:
    return (json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False)+"\n").encode()


def main() -> None:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", type=Path)
    g.add_argument("--check", type=Path)
    args = ap.parse_args()
    b = canonical_bytes(build_record())
    if args.write:
        args.write.write_bytes(b)
        print(f"GENERATED {args.write} bytes={len(b)} sha256={hashlib.sha256(b).hexdigest()}")
    else:
        assert args.check.read_bytes() == b, "Saved JSON differs from complete regeneration"
        print(f"PASS exact regenerate-and-compare bytes={len(b)} sha256={hashlib.sha256(b).hexdigest()}")
    print("FINITE PASS: 36 canonical integer seeds; first positive palindrome exactly at t=11")


if __name__ == '__main__':
    main()
