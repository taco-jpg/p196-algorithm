#!/usr/bin/env python3
"""Y09: exact two-sided 2-cell collapse controls, independently of repository code.

Run: python3 check_two_cell.py
Checks ALL two-cell bulk coefficients in bases 2..60; then checks
canonical ordinary big-integer reverse-and-add for 720 parameter pairs.
This is a verification of the algebraic lemma, not an all-time certificate.
"""
from random import Random


def cyclic_carries(w, b):
    m = len(w)
    for low_start in (0, 1):
        low = [low_start]
        for x in w:
            low.append((x + low[-1]) // b)
        if low[-1] != low_start:
            continue
        for high_start in (0, 1):
            high = [None] * (m + 1)
            high[m] = high_start
            for i in range(m - 1, -1, -1):
                high[i] = (w[i] + high[i + 1]) // b
            if high[0] == high_start:
                yield low, high


def bulk_step(w, b, gamma):
    m = len(w)
    assert all(0 <= x <= 2 * b - 2 for x in w)
    out = []
    for low, high in cyclic_carries(w, b):
        lo = [(w[i] + low[i]) % b for i in range(m)]
        hi = [(w[i] + high[i+1]) % b for i in range(m)]
        result = tuple(lo[i] + hi[(i-gamma) % m] for i in range(m))
        out.append((result, lo, hi))
    return out


def base_digits(n, b):
    digits = []
    while n:
        digits.append(n % b)
        n //= b
    return digits


def ordinary_pairword_step(w, b, copies=24):
    # Build an actual ordinary canonical number with mirrored pairword.
    half = list(w) * copies
    pair = half + half[::-1]
    digits = [0] * len(pair)
    for i in range(len(pair)//2):
        high = min(pair[i], b-1)
        low = pair[i] - high
        digits[i], digits[-i-1] = low, high
    assert digits[-1] != 0
    n = sum(x*b**i for i, x in enumerate(digits))
    # No pairword/normalization helper in this independent integer oracle.
    a = base_digits(n, b)
    reverse = sum(x*b**i for i, x in enumerate(a[::-1]))
    new = base_digits(n + reverse, b)
    g = len(new) - len(a)
    assert g in (0, 1)
    pnext = [new[i] + new[-1-i] for i in range(len(new))]
    return g, tuple(pnext[12:14]), pnext


def run():
    total = 0
    for b in range(2, 61):
        for a in range(2*b-1):
            for d in range(2*b-1):
                w=(a,d)
                for output, lo, hi in bulk_step(w,b,1):
                    assert output[0] == output[1], (b,w,output)
                    if w != (b-1,b-1):
                        assert lo == hi, (b,w,lo,hi)
                    total += 1
                # Once uniform, both output coefficients always uniform,
                # also if uniform equals the neutral b-1 coefficient.
                if a == d:
                    for g in (0,1):
                        assert all(x[0][0] == x[0][1] for x in bulk_step(w,b,g))
    assert tuple(x[0] for x in bulk_step((1,1,15,15),9,1)) == ((8,2,8,14),)
    assert tuple(x[0] for x in bulk_step((9,18,9,0),10,1)) == ((10,8,8,10),)
    rng=Random(20261028)
    checked=0
    for b in (3,4,9,10,11,13,26,50,146,1286):
        for j in range(72):
            a = 1 + rng.randrange(2*b-2)
            d = rng.randrange(2*b-1)
            w=(a,d)
            g, got, _ = ordinary_pairword_step(w,b)
            predictions = {x[0] for x in bulk_step(w,b,g)}
            assert got in predictions, (b,w,g,got,predictions)
            checked += 1
    print('PASS all-base algebraic bulk checks:',total,'carry combinations across bases 2..60')
    print('PASS independent ordinary big-integer replay:',checked,'one-step words across 10 bases')
    print('PASS primitive spatial period 4 positive controls b9/b10 (sharpness)')


if __name__=='__main__': run()
