#!/usr/bin/env python3
"""Finite adversarial controls; not a proof of any certificate theorem.

No implementation under review is imported.  Raw blocks follow the displayed
mathematical formulas and are compared against literal integer reverse-and-add.
Every legal trim is tested, including zero/nonmaximal trim and empty exteriors.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

PHASES = tuple(c for c in range(1, 18) if c != 9)
UNITS = {2, 4, 8, 16, 14, 10}


def norm(w, carry):
    out = []
    for a in w:
        x = a + carry
        out.append(x % 10)
        carry = x // 10
    return tuple(out), carry


def add(a, b):
    assert len(a) == len(b)
    return tuple(x + y for x, y in zip(a, b))


def pair(w):
    return add(w, w[::-1])


def raw(c, B, A, C):
    d = 18 - c
    kc, kd = int(c >= 10), int(d >= 10)
    tc, td = c - 9 * kc, d - 9 * kd
    DB, e0 = norm(B, 0)
    DA, e1 = norm(A, kc)
    DC, e2 = norm(C, kd)
    DR, e3 = norm(A[::-1], kd)
    EB, gamma = norm(B[::-1], kc)
    u0, u1, u2, u3 = c + e0 - 10 * kc, d + e1 - 10 * kd, d + e2 - 10 * kd, c + e3 - 10 * kc
    if gamma:
        return 2 * tc, add(DB + (u0,), (1,) + EB[::-1]), add(DA + (u1,), (u3,) + DR[::-1]), pair(DC + (u2,)), gamma
    return 2 * tc, add(DB + (u0,), EB[::-1] + (tc,)), add((tc,) + DA + (u1,), (u3,) + DR[::-1] + (td,)), pair((td,) + DC + (u2,)), gamma


def template(c, B, A, C, g, h):
    X = B + (c,) * g + A + (18 - c,) * h
    return X + C + X[::-1]


def leading(w, a):
    return next((i for i, x in enumerate(w) if x != a), len(w))


def trimming(cp, Br, Ar, Cr):
    dp = 18 - cp
    for j in range(leading(Br[::-1], cp) + 1):
        Bp = Br[:len(Br) - j]
        for j1 in range(leading(Ar, cp) + 1):
            At = Ar[j1:]
            for j2 in range(leading(At[::-1], dp) + 1):
                Ap = At[:len(At) - j2]
                for k in range(min(leading(Cr, dp), leading(Cr[::-1], dp), len(Cr) // 2) + 1):
                    Cp = Cr[k:len(Cr) - k]
                    yield (Bp, Ap, Cp), (j, j1, j2, k)


def realize(q):
    assert q and q[0] > 0 and q == q[::-1]
    D = [0] * len(q)
    for i in range(len(q) // 2):
        D[-i-1] = min(q[i], 9)
        D[i] = q[i] - D[-i-1]
    if len(q) % 2:
        assert q[len(q) // 2] % 2 == 0
        D[len(q) // 2] = q[len(q) // 2] // 2
    n = sum(x * 10**i for i, x in enumerate(D))
    assert pair(tuple(map(int, str(n)[::-1]))) == q
    return n


def run():
    small = [()] + [(a,) for a in range(19)]
    centers = [()] + [(a,) for a in range(0, 19, 2)] + [(a, a) for a in range(19)]
    counts = dict(sources=0, arbitrary_trims=0, unit_clock_controls=0, literal_integer_sources=0,
                  empty_source_exterior=0, empty_target_exterior=0, nonmaximal_exterior_trims=0,
                  negative_local_gain=0)
    examples = {}
    digest = hashlib.sha256()
    for c, B, A, C in itertools.product(PHASES, small, small, centers):
        counts['sources'] += 1
        cp, Br, Ar, Cr, gamma = raw(c, B, A, C)
        q = template(c, B, A, C, 2, 2)
        D, outcarry = norm(q, 0)
        qp = pair(D + ((outcarry,) if outcarry else ()))
        assert qp == template(cp, Br, Ar, Cr, gamma, gamma)
        assert (len(Br), len(Ar), len(Cr)) == (len(B) + 1, len(A) + 2 - gamma, len(C) + 2 - gamma)
        positive = not B or B[0] > 0
        if positive:
            n = realize(q)
            m = n + int(str(n)[::-1])
            assert pair(tuple(map(int, str(m)[::-1]))) == qp
            counts['literal_integer_sources'] += 1
            p = B[0] if B else c
            e = norm(q[:-1], 0)[1]
            assert gamma == int(p + e >= 10)
            nextp = 2 * p + e if p + e < 10 else p % 10 + 1
        if not B:
            counts['empty_source_exterior'] += 1
        for (Bp, Ap, Cp), (j, j1, j2, k) in trimming(cp, Br, Ar, Cr):
            counts['arbitrary_trims'] += 1
            dg, dh = gamma - 2 + j + j1, gamma - 2 + j2 + k
            W, Wp = 2 * len(B) + 2 * len(A) + len(C), 2 * len(Bp) + 2 * len(Ap) + len(Cp)
            assert Wp + 2 * (dg + dh) == W + gamma
            assert template(cp, Bp, Ap, Cp, 2 + dg, 2 + dh) == qp
            if positive:
                assert (Bp[0] if Bp else cp) == nextp
            # A trim of a constant suffix leaves exterior mass unchanged.
            mass, massp = sum(B) - c * len(B), sum(Bp) - cp * len(Bp)
            assert (massp - 2 * mass + gamma * c) % 9 == 0
            F = 2 * sum(B) + 2 * sum(A) + sum(C)
            Fp = 2 * sum(Bp) + 2 * sum(Ap) + sum(Cp)
            assert (Fp + 2 * cp * (dg - dh) - 2 * F) % 9 == 0
            if c in UNITS:
                ci, cpi = pow(c, -1, 9), pow(cp, -1, 9)
                assert (2 * cpi * massp + gamma - 2 * ci * mass) % 9 == 0
                assert (cpi * Fp + 2 * (dg - dh) - ci * F) % 9 == 0
                counts['unit_clock_controls'] += 1
            row = dict(source=(c, B, A, C), target=(cp, Bp, Ap, Cp), trims=(j, j1, j2, k), gamma=gamma, gains=(dg, dh))
            if not Bp:
                counts['empty_target_exterior'] += 1
                examples.setdefault('empty_target_exterior', row)
            if j < leading(Br[::-1], cp):
                counts['nonmaximal_exterior_trims'] += 1
                examples.setdefault('nonmaximal_exterior_differs_from_deterministic_outerNext', row)
            if dg < 0 or dh < 0:
                counts['negative_local_gain'] += 1
                examples.setdefault('local_gains_need_not_be_nonnegative', row)
            digest.update(json.dumps(row, separators=(',', ':')).encode())
            digest.update(b'\n')
    examples['zero_exterior_invalidates_positive_scalar_budget'] = {
        'p': 0, 'e': 0, 'nextp': 0, 'gamma': 0,
        'failed_inequality': '1 <= 4*gamma + lowerPotential(p) - lowerPotential(nextp)',
        'note': 'This is outside Admissible0; retained to test that positivity is not silently dropped.'}
    return {'status': 'PASS', 'scope': 'Finite controls only; no certificate instance, all-width theorem, or independent Lean rebuild is asserted.',
            'enumeration': 'All 16 phases; B,A empty or one arbitrary coefficient; C empty, one even coefficient, or doubled coefficient; EVERY legal trim.',
            'counts': counts, 'ordered_rows_sha256': digest.hexdigest(), 'adversarial_examples': examples}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
