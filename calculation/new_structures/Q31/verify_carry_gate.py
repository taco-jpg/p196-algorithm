#!/usr/bin/env python3
"""Independent controls for Q31's conditional T* mod-5 carry-charge reduction.

Run from the repository root:
    python3 calculation/new_structures/Q31/verify_carry_gate.py

The paper lemma is all-width and conditional on a phase-lifted U3 bulk with
fixed finite collars. These finite source/target controls are arithmetic checks,
not a 120-step seam return or a decimal Lychrel certificate.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P12 = ROOT / "calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt"
WIDTHS = (20, 40, 80, 160)
CENTRES = (([5], [10]), ([1, 17], [12, 12]))  # (J, C), odd/even C lengths


def candidates():
    out = []
    for a in range(0, 19, 2):
        motif = [9, a, 18-a]
        for r in range(3):
            row = tuple(motif[r:] + motif[:r])
            if row not in out:
                out.append(row)
    assert len(out) == 30 and all(sum(u) == 27 for u in out)
    return out


def repeat_period(word, length):
    return [word[i % len(word)] for i in range(length)]


def pairword(d):
    return [d[i] + d[-1-i] for i in range(len(d))]


def realize_pairword(P):
    assert P == P[::-1] and all(0 <= x <= 18 for x in P)
    d = [0] * len(P)
    for i in range(len(P) // 2):
        high = min(9, P[i])
        d[i] = P[i] - high
        d[-1-i] = high
    if len(P) % 2:
        assert P[len(P)//2] % 2 == 0
        d[len(P)//2] = P[len(P)//2] // 2
    assert d[-1] > 0 and pairword(d) == P
    return d


def schoolbook_step(d):
    carry, out = 0, []
    for i in range(len(d)):
        x = d[i] + d[-1-i] + carry
        out.append(x % 10)
        carry = x // 10
    if carry:
        out.append(carry)
    return out


def bigint_step(d):
    # Independent ordinary-integer calculation of n + reverse_decimal(n).
    n = int("".join(map(str, d[::-1])))
    reverse_n = int("".join(map(str, d)))
    return list(map(int, str(n + reverse_n)[::-1]))


def normalize_pairword(P):
    carry, out, cuts = 0, [], [0]
    carry_count = 0
    for x in P:
        carry_count += carry  # incoming carry at this coefficient
        s = x + carry
        out.append(s % 10)
        carry = s // 10
        cuts.append(carry)
    gamma = carry
    if carry:
        out.append(carry)
    return out, cuts, gamma, carry_count


def build(B, W, q, k, J, U, C):
    H = B + repeat_period(W, 9*q) + J + list(U)*k
    P = H + C + H[::-1]
    assert P == P[::-1]
    return P, len(B) + 9*q + len(J)


def check_word(P, u_start, k, gamma0):
    d = realize_pairword(P)
    normalized, cuts, gamma, carry_count = normalize_pairword(P)
    actual, school = bigint_step(d), schoolbook_step(d)
    assert actual == school == normalized
    assert len(actual) - len(d) == gamma == gamma0
    # Q01's proved complementary carry law on the k-2 interior U copies.
    for copy in range(1, k-1):  # 1,...,k-2
        for offset in range(3):
            i = u_start + 3*copy + offset
            assert cuts[i] + cuts[len(P)-i] == 1, (copy, offset, i)
    return carry_count


def read_root():
    rows = [[int(x) for x in line.split()]
            for line in P12.read_text().splitlines() if line.strip()]
    assert len(rows) == 38 and rows[0] == [12, 34, 9, 10]
    gamma, W, B = rows[1], rows[2], rows[26]
    assert gamma == [int(t % 12 in (0, 4, 8)) for t in range(12)]
    assert len(W) == 9 and len(B) == 34 and B[0] == 10
    return B, W, gamma


def main():
    B, W, gamma = read_root()
    Urows = candidates()
    odd_gate_rows = [u for u in Urows if (u[0] - u[1] + u[2]) % 11 == 0]
    assert odd_gate_rows == [(9, 8, 10), (10, 8, 9)]

    checked_pairs = 0
    prefactors = {}
    for U in Urows:
        for J, C in CENTRES:
            key = (tuple(J), tuple(C))
            for q in WIDTHS:
                for k in WIDTHS:
                    P0, start0 = build(B, W, q, k, J, U, C)
                    P1, start1 = build(B, W, q, k+5, J, U, C)
                    c0 = check_word(P0, start0, k, gamma[0])
                    c1 = check_word(P1, start1, k+5, gamma[0])
                    assert c1 - c0 == 15, (U, J, C, q, k, c0, c1)
                    assert sum(P1) - sum(P0) == 270
                    assert len(P1) - len(P0) == 30
                    prefactors.setdefault(key, set()).add(pow(10, len(P0)-1, 13))
                    prefactors[key].add(pow(10, len(P1)-1, 13))
                    checked_pairs += 1
    assert checked_pairs == 960
    assert all(len(v) == 1 for v in prefactors.values())
    print("Q31_BIGINT_CONTROLS_PASS: 960 source/target pairs; 1,920 exact integer-addition checks")
    print("Carry-count slope: C(k+5)-C(k)=15; coefficient-sum change=270; length change=30")
    print("Mod-13 factor 10^(L-1) is constant across q,k for each fixed (J,C) collar")
    print("Conditional odd-centre A(U)=0 rows: (9,8,10), (10,8,9); do not prune even-centre cases")
    print("Scope: controls only; no physical seam return or decimal Lychrel certificate")


if __name__ == "__main__":
    main()