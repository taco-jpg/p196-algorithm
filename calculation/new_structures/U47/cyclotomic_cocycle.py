#!/usr/bin/env python3
"""Exact cyclotomic carry-cocycle identities for decimal reverse-and-add pairwords.

The code is a checker for the algebraic identities stated in the companion note.
It does not search for or certify a Lychrel number.
"""
from __future__ import annotations
from pathlib import Path
import argparse, random, sys
sys.set_int_max_str_digits(0)

PHI_DEGREE = 12  # Phi_5(x^3) = 1 + x^3 + x^6 + x^9 + x^12
MODULUS = 31


def pairs(d: list[int]) -> list[int]:
    return [d[i] + d[-1-i] for i in range(len(d))]


def step_digits(d: list[int]) -> tuple[list[int], int]:
    carry = 0
    out = []
    for i in range(len(d)):
        z = d[i] + d[-1-i] + carry
        out.append(z % 10)
        carry = z // 10
    if carry:
        out.append(carry)
    return out, carry


def value(d: list[int]) -> int:
    return int(''.join(map(str, d[::-1])))


def rem_phi(poly: list[int]) -> list[int]:
    """Remainder modulo x^12+x^9+x^6+x^3+1, coefficients LSD first."""
    a = poly[:]
    for i in range(len(a)-1, PHI_DEGREE-1, -1):
        z = a[i]
        if not z:
            continue
        a[i] = 0
        for shift in (0,3,6,9):
            a[i-PHI_DEGREE+shift] -= z
    return (a + [0]*PHI_DEGREE)[:PHI_DEGREE]


def eval_mod(poly: list[int], x: int, p: int = MODULUS) -> int:
    acc = 0
    for a in reversed(poly):
        acc = (acc*x + a) % p
    return acc


def carry_poly_step(P: list[int]) -> tuple[list[int], int, list[int], int, int]:
    """Return P_next, gamma, K, n, L(2) for the exact polynomial recurrence."""
    n = len(P)
    carries = [0]
    digits = []
    carry = 0
    for p in P:
        z = p + carry
        digits.append(z % 10)
        carry = z // 10
        carries.append(carry)
    gamma = carry
    if gamma:
        digits.append(gamma)
    # K(x)=sum_{i=1}^{n-1} c_i*x^(i-1) + gamma*x^(n-1).
    K = [carries[i+1] for i in range(n-1)] + [gamma]
    # P_next=(1+x^gamma)P-(10-x)K-x^(n+gamma-2)(10x-1)K(x^-1).
    R = [0]*(n+gamma+1)
    for i,p in enumerate(P):
        R[i] += p
        R[i+gamma] += p
    for i,v in enumerate(K):
        R[i] -= 10*v
        R[i+1] += v
    for j,v in enumerate(K):
        if not v:
            continue
        e1, e0 = n+gamma-1-j, n+gamma-2-j
        if e1 >= 0:
            R[e1] -= 10*v
        if e0 >= 0:
            R[e0] += v
        else:
            raise AssertionError('nonzero negative exponent')
    P_next = pairs(digits)
    while len(R) > len(P_next) and R[-1] == 0:
        R.pop()
    R += [0]*(len(P_next)-len(R))
    assert R == P_next, 'exact polynomial carry-cocycle identity failed'
    k2 = eval_mod(K, 2)
    k16 = eval_mod(K, 16)
    L2 = (8*k2 + 19*pow(2, n+gamma-2, MODULUS)*k16) % MODULUS
    return P_next, gamma, K, n, L2


def cocycle_syndrome_at_2(gammas: list[int], L2s: list[int]) -> int:
    """S(2)=sum_t product_{s>t}(1+2^gamma_s) L_t(2) mod 31."""
    assert len(gammas) == len(L2s)
    w = 1
    S = 0
    for t in range(len(gammas)-1, -1, -1):
        S = (S + w*L2s[t]) % MODULUS
        w = w * (1 + pow(2, gammas[t], MODULUS)) % MODULUS
    return S


def pairword(q: int, k: int, B: list[int], W: list[int], J: list[int], U: list[int], C: list[int]) -> list[int]:
    assert len(W) == 9 and len(U) == 3
    H = B + W*q + J + U*k
    return H + C + H[::-1]


def source_digits(P: list[int]) -> list[int]:
    assert P == P[::-1] and P[0] > 0
    h = len(P)//2
    lo = [max(x-9, 0) for x in P[:h]]
    hi = [x-y for x,y in zip(P[:h], lo)]
    mid = [P[h]//2] if len(P)%2 else []
    if len(P)%2:
        assert P[h] % 2 == 0
    d = lo + mid + hi[::-1]
    assert d[-1] > 0 and all(0 <= x <= 9 for x in d)
    assert pairs(d) == P
    return d


def check_template_insertion() -> None:
    rng = random.Random(47031)
    B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
    W = [5,18,4,8,1,15,4,0,5]
    for _ in range(80):
        J = [rng.randrange(19) for _ in range(rng.randrange(1,8))]
        U = [rng.randrange(19) for _ in range(3)]
        C0 = [rng.randrange(10) for _ in range(2)]
        C = C0 + [rng.randrange(10)] + C0[::-1] if rng.randrange(2) else C0 + C0[::-1]
        q,k = rng.randrange(1,12), rng.randrange(1,12)
        p0 = pairword(q,k,B,W,J,U,C)
        p1 = pairword(q,k+5,B,W,J,U,C)
        assert rem_phi(p0) == rem_phi(p1)
        p2 = pairword(q+5,k,B,W,J,U,C)
        assert rem_phi(p0) == rem_phi(p2)


def check_step_identity() -> None:
    rng = random.Random(47032)
    for _ in range(100):
        n = rng.randrange(5,100)
        d = [rng.randrange(10) for _ in range(n)]
        d[-1] = rng.randrange(1,10)
        P = pairs(d)
        Pnext, gamma, K, oldn, L2 = carry_poly_step(P)
        dnext, gamma2 = step_digits(d)
        assert gamma == gamma2 and Pnext == pairs(dnext)
        # For an arbitrary single edge, the affine recurrence is exact over Z[x]/Phi.
        delta = (eval_mod(rem_phi(Pnext), 2) - eval_mod(rem_phi(P), 2)) % MODULUS
        # One-edge cocycle: P'=(1+2^gamma)P-L(2).
        assert delta == ((1+pow(2,gamma,MODULUS))*eval_mod(rem_phi(P),2)-L2-eval_mod(rem_phi(P),2)) % MODULUS


def check_120_cocycle() -> None:
    rng = random.Random(47033)
    for _ in range(4):
        n = rng.randrange(20,90)
        d = [rng.randrange(10) for _ in range(n)]
        d[-1] = rng.randrange(1,10)
        N = value(d)
        gammas, L2s = [], []
        P0 = pairs(d)
        for _t in range(120):
            P = pairs(d)
            Pnext, gamma, K, oldn, L2 = carry_poly_step(P)
            gammas.append(gamma); L2s.append(L2)
            N += int(str(N)[::-1])
            d, gamma2 = step_digits(d)
            assert gamma == gamma2 and value(d) == N and pairs(d) == Pnext
        # For these actual orbits, check the weighted-cocycle identity directly.
        S = cocycle_syndrome_at_2(gammas, L2s)
        delta = (eval_mod(rem_phi(pairs(d)),2)-eval_mod(rem_phi(P0),2)) % MODULUS
        A = 1
        for g in gammas:
            A = A*(1+pow(2,g,MODULUS)) % MODULUS
        assert delta == ((A-1)*eval_mod(rem_phi(P0),2)-S) % MODULUS


def self_test() -> None:
    assert sum(pow(2,i,31) for i in (0,3,6,9,12)) % 31 == 0
    assert pow(2,90,31)*pow(3,30,31) % 31 == 1
    check_template_insertion()
    check_step_identity()
    check_120_cocycle()
    print('PASS: Phi5(x^3) insertion, exact carry-polynomial recurrence, and mod-31 cocycle controls')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', action='store_true')
    a = ap.parse_args()
    if a.self_test:
        self_test()
    else:
        ap.print_help()

if __name__ == '__main__':
    main()
