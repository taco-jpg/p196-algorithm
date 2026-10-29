#!/usr/bin/env python3
"""Exact local carry-reset and screw-phase check for the rooted p12/m9 T* U3 bulk.

Run from the repository root:
    python3 calculation/new_structures/Q36/tstar_screw.py

Finite-width decimal runs are independent arithmetic controls, not a survival
claim. The all-width statement is the local transfer formula plus exhaustive
enumeration of its 30-state phase graph.
"""
from pathlib import Path
import json
import os

ROOT = Path(os.environ["Q36_REPO_ROOT"]) if "Q36_REPO_ROOT" in os.environ else Path(__file__).resolve().parents[3]
P12 = ROOT / "calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt"
B9 = ROOT / "calculation/decimal_frontier/lattice_formats/cert_b9_rec0.json"
B50 = ROOT / "calculation/neutral_band/agent10_base50/cert_b50.json"
WIDTHS = (20, 40, 80, 160)


def digits_to_int(d, b):
    n = 0
    for x in reversed(d):
        n = n * b + x
    return n


def int_to_digits(n, b):
    assert n > 0
    d = []
    while n:
        n, x = divmod(n, b)
        d.append(x)
    return d


def schoolbook_step(d, b):
    carry, out = 0, []
    for i in range(len(d)):
        x = d[i] + d[-1-i] + carry
        out.append(x % b)
        carry = x // b
    if carry:
        out.append(carry)
    return out


def bigint_step(d, b):
    # Independent ordinary-integer implementation, not the carry-array routine.
    if b == 10:
        n = int("".join(map(str, d[::-1])))
        r = int("".join(map(str, d)))
        return list(map(int, str(n + r)[::-1]))
    return int_to_digits(digits_to_int(d, b) + digits_to_int(d[::-1], b), b)


def pairword(d):
    return [x + d[-1-i] for i, x in enumerate(d)]


def split_pairword(P, b):
    assert P == P[::-1] and all(0 <= x <= 2*(b-1) for x in P)
    d = [0] * len(P)
    for i in range(len(P)//2):
        j = len(P)-1-i
        hi = min(P[i], b-1)
        d[i], d[j] = P[i]-hi, hi
    if len(P) % 2:
        assert P[len(P)//2] % 2 == 0
        d[len(P)//2] = P[len(P)//2]//2
    assert d[-1] != 0 and pairword(d) == P
    return d


def repeat(W, n):
    return [W[i % len(W)] for i in range(n)]


def read_tstar():
    lines = [[int(x) for x in s.split()] for s in P12.read_text().splitlines()]
    assert len(lines) == 38 and lines[0] == [12, 34, 9, 10]
    gamma, W0, B0 = lines[1], lines[2], lines[26]
    assert gamma == [int(t % 12 in (0, 4, 8)) for t in range(12)]
    assert sum(gamma) == 3
    assert sum(gamma[t % 12] for t in range(40)) == 10
    assert sum(gamma[t % 12] for t in range(120)) == 30
    assert len(W0) == 9 and len(B0) == 34 and B0[0] == 10
    return B0, W0, gamma


def has_reflection_axis(w):
    return any(all(w[i] == w[(a-i) % len(w)] for i in range(len(w)))
               for a in range(len(w)))


def check_base9():
    cert = json.loads(B9.read_text())
    p = cert["p"]
    assert p == 10 and len(cert["B_t"]) == len(cert["w_t"]) == p
    assert cert["gam"] == [1,1,0,0,0,1,1,0,0,0]
    assert sum(cert["gam"]) == 4 and len(cert["w_t"][0]) == 4
    assert all(has_reflection_axis(w) for w in cert["w_t"])
    for q in WIDTHS:
        l = 4*q + 2
        d = split_pairword(cert["B_t"][0] + repeat(cert["w_t"][0], l)
                           + cert["B_t"][0][::-1], 9)
        for t in range(20):
            assert pairword(d) == (cert["B_t"][t % p]
                    + repeat(cert["w_t"][t % p], l)
                    + cert["B_t"][t % p][::-1])
            nxt = schoolbook_step(d, 9)
            assert nxt == bigint_step(d, 9)
            assert len(nxt)-len(d) == cert["gam"][t % p]
            l += cert["gam"][t % p]
            want = (cert["B_t"][(t+1) % p]
                    + repeat(cert["w_t"][(t+1) % p], l)
                    + cert["B_t"][(t+1) % p][::-1])
            assert pairword(nxt) == want
            assert nxt != nxt[::-1]
            d = nxt
    print("PASS base-9 Lean control: 20 edges at q=20,40,80,160; Gamma=4, m=4; all ten phases have a reflection axis.")


def make_base50(edge, h):
    return (edge["B"] + [49]*h + edge["C"] + [49]*h
            + edge["B"][::-1])


def check_base50():
    cert = json.loads(B50.read_text())
    assert cert["base"] == 50 and len(cert["edges"]) == 4
    for h0 in WIDTHS:
        h = h0
        d = split_pairword(make_base50(cert["edges"][0], h), 50)
        for t in range(16):
            edge = cert["edges"][t % 4]
            assert pairword(d) == make_base50(edge, h)
            assert d != d[::-1]
            nxt = schoolbook_step(d, 50)
            assert nxt == bigint_step(d, 50)
            h += edge["u"] + edge["v"] - edge["gamma"]
            d = nxt
        assert h == h0 + 4
    print("PASS base-50 computed control: 16 edges at h=20,40,80,160; gap gain=4.")


def candidates():
    out = []
    for a in range(0, 19, 2):
        u = [9, a, 18-a]
        for r in range(3):
            v = tuple(u[r:] + u[:r])
            if v not in out:
                out.append(v)
    assert len(out) == 30 and len(set(out)) == 30
    assert all(sum(u) == 27 and len(set(u)) == 3 for u in out)
    return out


def normalize(word, incoming, b=10):
    out, c = [], incoming
    for x in word:
        z = x + c
        out.append(z % b)
        c = z // b
    return out, c


def reset_normalized_word(word):
    """Any coefficient other than 9 makes the outgoing carry independent of 0/1 input."""
    assert any(x != 9 for x in word)
    c0 = normalize(word, 0)[1]
    c1 = normalize(word, 1)[1]
    assert c0 == c1
    digits, out = normalize(word, c0)
    assert out == c0
    return c0, digits


def bulk_step(U, gamma):
    """All-width interior transfer for U^k | centre | reverse(U)^k."""
    assert len(U) == 3 and any(x != 9 for x in U)
    _, low_digits = reset_normalized_word(list(U))
    _, high_digits = reset_normalized_word(list(U[::-1]))
    nxt = tuple(low_digits[r] + high_digits[(gamma-1-r) % 3]
                for r in range(3))
    assert all(0 <= x <= 18 for x in nxt)
    return nxt


def rotate_left(U, r):
    return tuple(U[r:] + U[:r])


def macro_map(U, gamma):
    x = U
    for t in range(12):
        x = bulk_step(x, gamma[t])
    return x


def verify_screw_map(gamma):
    S = set(candidates())
    for U0 in S:
        seq = [U0]
        for t in range(120):
            nxt = bulk_step(seq[-1], gamma[t % 12])
            assert nxt in S, (U0, t, nxt)
            seq.append(nxt)
        assert seq[120] == U0
        assert all(len(set(x)) == 3 for x in seq[:-1])
        assert all(seq[(t+40) % 120] == rotate_left(list(seq[t]), 1)
                   for t in range(120)), U0
        assert all(seq[(t+80) % 120] == rotate_left(list(seq[t]), 2)
                   for t in range(120)), U0

    M = {U: macro_map(U, gamma) for U in S}
    seen, cycle_lengths = set(), []
    for U0 in S:
        if U0 in seen:
            continue
        x, length = U0, 0
        while x not in seen:
            seen.add(x)
            length += 1
            x = M[x]
        assert x == U0
        cycle_lengths.append(length)
    assert sorted(cycle_lengths) == [10, 10, 10]
    assert len(seen) == 30
    print("PASS exact T* local map: 30 states, 3 macro-cycles of length 10.")
    print("PASS screw phase: U[t+40]=rot_left(U[t],1), U[t+80]=rot_left(U[t],2), U[t+120]=U[t].")
    print("PASS phase-complete asymmetry: all 3,600 phase states have three distinct coefficients.")


def check_tstar_integer_controls(B0, W0, gamma):
    centres = (([5], [10]), ([1,17], [12,12]))
    checked = 0
    for q in WIDTHS:
        k = q
        for U in candidates():
            for J, C in centres:
                H = B0 + repeat(W0, 9*q) + J + list(U)*k
                P = H + C + H[::-1]
                d = split_pairword(P, 10)
                start = len(B0) + 9*q + len(J)
                expected = bulk_step(U, gamma[0])
                first = schoolbook_step(d, 10)
                assert first == bigint_step(d, 10)
                assert pairword(first)[start+9:start+12] == list(expected)
                d = split_pairword(P, 10)
                for t in range(120):
                    nxt = schoolbook_step(d, 10)
                    assert nxt == bigint_step(d, 10)
                    assert len(nxt)-len(d) == gamma[t % 12], (q, U, J, C, t)
                    d = nxt
                    checked += 1
    assert checked == len(WIDTHS)*30*2*120
    print(f"PASS T* physical controls: {checked:,} digit-array/BigInt edges; q=k=20,40,80,160; odd/even centre controls.")
    print("These are arithmetic controls only; no finite-horizon survival claim is made.")


def main():
    B0, W0, gamma = read_tstar()
    check_base9()
    check_base50()
    verify_screw_map(gamma)
    check_tstar_integer_controls(B0, W0, gamma)


if __name__ == "__main__":
    main()
