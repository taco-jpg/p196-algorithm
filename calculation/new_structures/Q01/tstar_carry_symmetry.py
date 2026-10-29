#!/usr/bin/env python3
"""Q01 T*: exact carry-reflection law, with independent canonical big integers.

Run at repository root:
  python3 calculation/new_structures/Q01/tstar_carry_symmetry.py

The proof is symbolic; numeric tests cross-check the actual normalization and
the all-width interior cut identity on the published rooted p12/m9 data.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WIDTHS = (20, 40, 80, 160)
CENTRES = ([12], [8, 8])  # odd and even centre lengths, both canonical pairwords
J = [5]


def value(word):
    n = 0
    for digit in reversed(word):
        n = n * 10 + digit
    return n


def digits(n):
    out = []
    while n:
        n, d = divmod(n, 10)
        out.append(d)
    return out or [0]


def reverse_value(n):
    return value(digits(n)[::-1])


def pairword(n):
    d = digits(n)
    return [d[i] + d[-1-i] for i in range(len(d))]


def realize_pairword(P):
    assert P == P[::-1]
    d = [0] * len(P)
    for i in range(len(P) // 2):
        high = min(9, P[i])
        low = P[i] - high
        assert 0 <= low <= 9 and 0 <= high <= 9
        d[i] = low
        d[-1-i] = high
    if len(P) % 2:
        assert P[len(P)//2] % 2 == 0
        d[len(P)//2] = P[len(P)//2] // 2
    assert d[-1] > 0
    n = value(d)
    assert pairword(n) == P
    return n


def repeat(word, copies):
    return word * copies


def carry_step(x, c):
    return (x + c) // 10


def block_carry(word, c):
    for x in word:
        c = carry_step(x, c)
    return c


def steady_path(word):
    out0 = block_carry(word, 0)
    out1 = block_carry(word, 1)
    assert out0 == out1, (word, out0, out1)
    path = [out0]
    for x in word:
        path.append(carry_step(x, path[-1]))
    assert path[-1] == out0
    return out0, path


def all_u3_rows():
    rows = []
    seen = set()
    for a in range(0, 19, 2):
        motif = [9, a, 18-a]
        for r in range(3):
            U = motif[r:] + motif[:r]
            key = tuple(U)
            if key not in seen:
                seen.add(key)
                rows.append(U)
    assert len(rows) == 30
    return rows


def read_root():
    rows = (ROOT / "calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt").read_text().splitlines()
    p, nB, m, base = map(int, rows[0].split())
    assert (p, nB, m, base) == (12, 34, 9, 10)
    W = [list(map(int, s.split())) for s in rows[2:2+p]]
    B = [list(map(int, s.split())) for s in rows[2+2*p:2+3*p]]
    assert len(W) == len(B) == p
    assert all(len(w) == m for w in W)
    assert all(len(b) == nB for b in B)
    return B[0], W[0]


def normalize_pairword(P):
    c = 0
    out = []
    cuts = [0]  # cuts[i] is the actual carry after i coefficients
    for x in P:
        s = x + c
        out.append(s % 10)
        c = s // 10
        cuts.append(c)
    if c:
        out.append(c)
    return out, cuts, c


def main():
    B, W = read_root()
    Urows = all_u3_rows()
    checks = 0
    cut_checks = 0

    # Exact symbolic gate: both oriented block maps are constant and complementary,
    # and their steady cut paths are complementary under reflection.
    for U in Urows:
        revU = U[::-1]
        outU, s = steady_path(U)
        outR, r = steady_path(revU)
        assert outR == 1 - outU, (U, outU, outR)
        assert all(s[j] + r[3-j] == 1 for j in range(4)), (U, s, r)

    for U in Urows:
        for q in WIDTHS:
            for k in WIDTHS:
                for C in CENTRES:
                    H = B + repeat(W, q) + J + repeat(U, k)
                    P = H + C + H[::-1]
                    n = realize_pairword(P)
                    # Independently execute ordinary integer reverse-and-add.
                    actual = n + reverse_value(n)
                    normalized, cuts, gamma = normalize_pairword(P)
                    assert value(normalized) == actual
                    assert digits(actual) == normalized
                    assert pairword(n) == P

                    u_start = len(B) + len(W) * q + len(J)
                    for copy in range(1, k-1):
                        # Copies 1..k-2 are beyond the finite outer/centre collars.
                        for offset in range(4):
                            cut = u_start + 3*copy + offset
                            mirror_cut = len(P) - cut
                            assert cuts[cut] + cuts[mirror_cut] == 1, (
                                U, q, k, C, copy, offset,
                                cuts[cut], cuts[mirror_cut]
                            )
                            cut_checks += 1
                    checks += 1

    assert checks == 960
    assert cut_checks == 280320
    print("PAPER_PROOF_CONTROL: all 30 U3 rows have complementary steady carry paths")
    print(f"BIGINT_CONTROLS_PASS: {checks} canonical sources; {cut_checks} reflected interior cuts")
    print("Scope: local all-width carry symmetry only; no full seam return or Lychrel claim")


if __name__ == "__main__":
    main()
