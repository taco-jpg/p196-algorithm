#!/usr/bin/env python3
"""Exact p<=24 base-10 overflow-necklace skip check for bauto3's >127 key guard.
Tests the position-zero necessary condition only; no Lychrel certificate claim.
"""
from itertools import combinations


def canonical(w):
    return all(w <= w[k:] + w[:k] for k in range(1, len(w)))


def edges(base, q, g):
    for c in (0, 1):
        if (q + c) // base != g:
            continue
        nxt = q % base + (1 if g else (q + c) % base)
        if 1 <= nxt <= 2 * base - 2:
            yield nxt


def position_zero_accept(base, word):
    for q0 in range(1, 2 * base - 1):
        states = {q0}
        for ch in word:
            states = {nxt for q in states for nxt in edges(base, q, int(ch))}
            if not states:
                break
        if q0 in states:
            return True
    return False


def old_skipped_necklaces():
    for period in range(1, 25):
        for zeros_count in range(period + 1):
            ones = period - zeros_count
            if 2 * period + 4 * ones <= 127:
                continue
            for zeros in combinations(range(period), zeros_count):
                chars = ['1'] * period
                for z in zeros:
                    chars[z] = '0'
                word = ''.join(chars)
                if canonical(word):
                    yield period, word


def main():
    psi = {1: 3, 2: 2, 3: 2, 10: 2}
    psi.update({q: 1 for q in range(4, 10)})
    for q in range(1, 19):
        psi.setdefault(q, 0)
    for q in range(1, 19):
        for g in (0, 1):
            for nxt in edges(10, q, g):
                assert psi[nxt] - psi[q] >= 2 * g - 1, (q, g, nxt)
    assert position_zero_accept(9, '1100011000')
    assert position_zero_accept(13, '1010010000')
    assert position_zero_accept(10, '10101010')
    counts = {}
    for period, word in old_skipped_necklaces():
        counts[period] = counts.get(period, 0) + 1
        assert 2 * word.count('1') > period, (period, word)
        assert not position_zero_accept(10, word), (period, word)
    assert counts == {22: 2, 23: 13, 24: 545}, counts
    assert sum(counts.values()) == 560
    print('PASS: potential inequalities on every admissible base-10 edge')
    print('PASS: base-9/base-13/base-10 position-zero positive controls')
    print('PASS: 560/560 old-skipped canonical necklaces have no position-zero cycle')
    print('Counts:', counts)


if __name__ == '__main__':
    main()
