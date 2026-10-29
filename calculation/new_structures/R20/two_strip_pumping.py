#!/usr/bin/env python3
"""Finite controls for the two-strip physical pairword pumping lemma.

The theorem/proof is stated in results/AgentR20TwoStripPumping.md. This file
checks its indexing and physical-realizability conventions against ordinary
integer reverse-and-add and exact schoolbook normalization. It is not a
search for, or a claim of, a decimal Lychrel certificate.
"""
from __future__ import annotations
import random


def normalize(P: list[int], b: int):
    """Schoolbook normalization of coefficient word P, LSD first."""
    carry = 0
    digits: list[int] = []
    carries = [0]
    for x in P:
        s = x + carry
        digits.append(s % b)
        carry = s // b
        carries.append(carry)
    assert carry in (0, 1), (b, max(P, default=0), carry)
    return digits, carries, carry


def pairword(digits: list[int]) -> list[int]:
    return [digits[i] + digits[-1 - i] for i in range(len(digits))]


def phi(P: list[int], b: int) -> list[int]:
    digits, _, gamma = normalize(P, b)
    if gamma:
        digits = digits + [gamma]
    return pairword(digits)


def insert(P: list[int], i: int, w: int, extra: int = 1) -> list[int]:
    """Insert extra further copies of P[i:i+w] and its mirror."""
    assert P == P[::-1]
    h = len(P) // 2
    assert 0 <= i and 0 < w and i + w <= h
    H = P[:h]
    C = [] if len(P) % 2 == 0 else [P[h]]
    V = H[i:i + w]
    H2 = H[:i] + V * extra + H[i:]
    return H2 + C + H2[::-1]


def ports(P: list[int], i: int, w: int, b: int):
    """Return the exact two carry loops and overflow-lag gate."""
    n = len(P)
    assert P == P[::-1] and 0 < i and i + w <= n // 2
    digits, c, gamma = normalize(P, b)
    j = i + w
    lower = (c[i], c[j])
    upper = (c[n - j], c[n - i])
    lag = (digits[n - i], digits[n - j])
    ok = lower[0] == lower[1] and upper[0] == upper[1]
    if gamma:
        ok = ok and lag[0] == lag[1]
    return ok, (lower, upper, lag, gamma)


def source_digits(P: list[int], b: int) -> list[int]:
    """Construct a real digit string whose mirrored digit sums are P."""
    assert P == P[::-1] and P[0] > 0 and all(0 <= x <= 2 * b - 2 for x in P)
    h = len(P) // 2
    H = P[:h]
    lo = [max(0, x - (b - 1)) for x in H]
    hi = [x - y for x, y in zip(H, lo)]
    C = []
    if len(P) % 2:
        assert P[h] % 2 == 0
        C = [P[h] // 2]
    d = lo + C + hi[::-1]
    assert all(0 <= x < b for x in d) and d[-1] > 0
    assert pairword(d) == P
    return d


def value(digits: list[int], b: int) -> int:
    n = 0
    for x in reversed(digits):
        n = n * b + x
    return n


def digits_of(n: int, b: int) -> list[int]:
    if n == 0:
        return [0]
    out = []
    while n:
        n, r = divmod(n, b)
        out.append(r)
    return out


def actual_step_pairword(P: list[int], b: int) -> list[int]:
    d = source_digits(P, b)
    n = value(d, b)
    r = value(d[::-1], b)
    return pairword(digits_of(n + r, b))


def random_pairword(rng: random.Random, b: int, half: int) -> list[int]:
    H = [rng.randrange(2 * b - 1) for _ in range(half)]
    H[0] = rng.randrange(1, 2 * b - 1)
    if rng.randrange(2):
        C = []
    else:
        C = [2 * rng.randrange(b)]
    return H + C + H[::-1]


def check_one_strip(rng: random.Random, trials: int = 3000) -> int:
    accepted = 0
    for _ in range(trials):
        b = rng.randrange(2, 17)
        P = random_pairword(rng, b, rng.randrange(40, 100))
        i = rng.randrange(1, len(P) // 2 - 8)
        w = rng.randrange(1, min(8, len(P) // 2 - i) + 1)
        ok, _ = ports(P, i, w, b)
        if not ok:
            continue
        Q = phi(P, b)
        assert Q == actual_step_pairword(P, b)
        for copies in (1, 2, 3):
            P1 = insert(P, i, w, copies)
            assert phi(P1, b) == actual_step_pairword(P1, b)
            assert phi(P1, b) == insert(Q, i, w, copies), (b, i, w, copies)
        accepted += 1
    assert accepted >= 30, accepted
    return accepted


def check_two_strips(rng: random.Random, trials: int = 1200) -> int:
    accepted = 0
    for _ in range(trials):
        b = rng.randrange(2, 17)
        P = random_pairword(rng, b, rng.randrange(100, 180))
        h = len(P) // 2
        W = [i for i in range(1, max(2, h // 3)) if i + 9 < h and ports(P, i, 9, b)[0]]
        U = [i for i in range(h // 2, h - 3) if ports(P, i, 3, b)[0]]
        choices = [(i, j) for i in W for j in U if i + 9 <= j]
        if not choices:
            continue
        iw, iu = rng.choice(choices)
        Q = phi(P, b)
        assert Q == actual_step_pairword(P, b)
        for wc in (1, 2, 3):
            P_w = insert(P, iw, 9, wc)
            assert phi(P_w, b) == actual_step_pairword(P_w, b)
            assert phi(P_w, b) == insert(Q, iw, 9, wc), (b, iw, iu, 'W', wc)
        for uc in (1, 2, 3):
            P_u = insert(P, iu, 3, uc)
            assert phi(P_u, b) == actual_step_pairword(P_u, b)
            assert phi(P_u, b) == insert(Q, iu, 3, uc), (b, iw, iu, 'U', uc)
        for wc in (1, 2, 3):
            for uc in (1, 2, 3):
                both_wu = insert(insert(P, iw, 9, wc), iu + 9 * wc, 3, uc)
                both_uw = insert(insert(P, iu, 3, uc), iw, 9, wc)
                assert both_wu == both_uw
                target_both = insert(insert(Q, iw, 9, wc), iu + 9 * wc, 3, uc)
                assert phi(both_wu, b) == target_both, (b, iw, iu, wc, uc)
                assert phi(both_wu, b) == actual_step_pairword(both_wu, b)
        accepted += 1
    assert accepted >= 10, accepted
    return accepted


def main() -> None:
    rng = random.Random(20261029)
    one = check_one_strip(rng)
    two = check_two_strips(rng)
    print(f'PASS: {one} one-strip and {two} two-strip exact carry-gated splice controls; bases 2..16.')


if __name__ == '__main__':
    main()
