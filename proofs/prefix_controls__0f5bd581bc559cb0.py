#!/usr/bin/env python3
"""Independent finite controls of the new band-padded three-column bridge.

No source implementation or previous control script is imported. This tests
the new projection only; it is not a proof or a search for full certificates.
"""
from __future__ import annotations

import hashlib
import itertools
import json

PHASES = tuple(c for c in range(1, 18) if c != 9)


def norm(word, carry):
    digits = []
    for x in word:
        value = x + carry
        digits.append(value % 10)
        carry = value // 10
    return tuple(digits), carry


def pad(word, c):
    return (word + (c, c, c))[:3]


def raw_outer(c, B):
    carry_band = int(c >= 10)
    next_c = 2 * (c - 9 * carry_band)
    left, left_carry = norm(B, 0)
    right, gamma = norm(B[::-1], carry_band)
    entrance = c + left_carry - 10 * carry_band
    reflected = (1,) + right[::-1] if gamma else right[::-1] + (c - 9 * carry_band,)
    raw = tuple(x + y for x, y in zip(left + (entrance,), reflected, strict=True))
    return next_c, raw, gamma


def advance(s, incoming):
    # Independent ordinary column arithmetic on the three supplied columns.
    left, _ = norm(s, 0)
    right, gamma = norm(s[::-1], incoming)
    r = right[::-1]
    aligned = (1,) + r[:2] if gamma else r
    return tuple(x + y for x, y in zip(left, aligned, strict=True)), gamma


def source_words():
    for n in range(4):
        yield from itertools.product(range(19), repeat=n)
    # Full three-column coverage with both actual tail-carry outcomes and
    # propagation through runs of nines; longer tails are not an added premise.
    tails = ((0,), (10,), (9, 9), (10, 9), (9, 10), (18, 0, 9))
    for first in itertools.product(range(19), repeat=3):
        for tail in tails:
            yield first + tail


def run():
    counts = dict(sources=0, trim_controls=0, short_sources=0, long_sources=0,
                  input_zero=0, input_one=0, empty_targets=0, nonmaximal_trims=0)
    digest = hashlib.sha256()
    by_length = {}
    for c in PHASES:
        k = int(c >= 10)
        for B in source_words():
            counts['sources'] += 1
            by_length[len(B)] = by_length.get(len(B), 0) + 1
            cp, raw, gamma = raw_outer(c, B)
            if len(B) < 3:
                e = k
                counts['short_sources'] += 1
            else:
                e = norm(B[3:][::-1], k)[1]
                counts['long_sources'] += 1
            assert e in (0, 1)
            counts['input_one' if e else 'input_zero'] += 1
            expected = (pad(raw, cp), gamma)
            assert advance(pad(B, c), e) == expected
            maximal = 0
            for x in reversed(raw):
                if x != cp:
                    break
                maximal += 1
            for j in range(maximal + 1):
                target = raw[:len(raw)-j]
                assert advance(pad(B, c), e) == (pad(target, cp), gamma)
                counts['trim_controls'] += 1
                counts['empty_targets'] += not target
                counts['nonmaximal_trims'] += j < maximal
            digest.update(json.dumps((c, B, e, cp, raw, gamma, maximal), separators=(',', ':')).encode())
            digest.update(b'\n')
    # The padded prefix is a valid quotient projection, but is not necessarily
    # the literal physical first three columns when the outer band has length 2.
    c, A, g, h = 2, (5,), 2, 2
    X = (c,) * g + A + (18-c,) * h
    q = X + X[::-1]
    assert q[:3] != pad((), c)
    # A bounded tail can determine either incoming bit for the same prefix.
    B0, B1 = (1, 9, 9, 0), (1, 9, 9, 10)
    e0, e1 = norm(B0[3:][::-1], 0)[1], norm(B1[3:][::-1], 0)[1]
    assert pad(B0, 2) == pad(B1, 2) and (e0, e1) == (0, 1)
    assert advance(pad(B0, 2), e0) != advance(pad(B1, 2), e1)
    # Nonneutral Phase is essential for the short-block reset argument.
    cp, raw, gamma = raw_outer(9, (10,))
    assert advance(pad((10,), 9), 0) != (pad(raw, cp), gamma)
    return {
        'status': 'PASS',
        'scope': 'Finite controls of the new padded-prefix projection only; no theorem or certificate instance is inferred from enumeration.',
        'counts': counts,
        'source_lengths': by_length,
        'ordered_source_rows_sha256': digest.hexdigest(),
        'counterexamples_to_wrong_shortcuts': {
            'padded_is_not_always_physical_prefix': {
                'phase': 2, 'B': [], 'A': [5], 'C': [], 'g': 2, 'h': 2,
                'physical_template': q, 'physical_first_three': q[:3], 'padded_prefix': pad((), 2)},
            'input_carry_is_not_always_phase_carry': {
                'phase': 2, 'B0': B0, 'B1': B1, 'common_prefix': pad(B0, 2),
                'actual_input_bits': [e0, e1], 'outputs': [advance(pad(B0, 2), e0), advance(pad(B1, 2), e1)]},
            'neutral_phase_cannot_be_added': {
                'phase': 9, 'B': [10], 'advance_with_phase_bit': advance(pad((10,), 9), 0),
                'raw_padded_output': (pad(raw, cp), gamma)}
        }
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
