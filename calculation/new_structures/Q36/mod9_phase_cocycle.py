#!/usr/bin/env python3
"""Exact phase-resolved mod-9 seam-charge gate for the T* p12/m9 family.

Run from the repository root:
    python3 calculation/new_structures/Q36/mod9_phase_cocycle.py
"""
from tstar_screw import P12, candidates


def sigma(word):
    return sum(word)


def mod9(x):
    return x % 9


def main():
    lines = [[int(x) for x in s.split()] for s in P12.read_text().splitlines()]
    assert len(lines) == 38 and lines[0] == [12, 34, 9, 10]
    W, B = lines[2:14], lines[26:38]
    assert len(W) == len(B) == 12
    assert all(sigma(U) == 27 for U in candidates())

    got = [(mod9(sigma(B[t])), mod9(sigma(W[t]))) for t in (0, 4, 8)]
    assert got == [(1, 6), (5, 6), (3, 6)], got
    assert mod9(14*sigma(W[0]) - 2*sigma(W[4])) == 0
    assert mod9(8*sigma(W[0]) - 2*sigma(W[8])) == 0

    # If q_t=q+delta_t and sigma(U_t)=27, let
    # K_t=2*sigma(J_t)+sigma(C_t). Then sigma(P_t)=2*sigma(B_t)
    # +2*q_t*sigma(W_t)+K_t (mod 9). Since sigma(P_(t+s))=2^s sigma(P_t),
    # the checkpoint gates follow exactly.
    for k0 in range(9):
        for d40 in range(3):
            k40 = mod9(7*k0 + 4 - 3*d40)
            assert k40 % 3 == (k0 + 1) % 3
            assert k40 != k0, (k0, d40, k40)
        for d80 in range(3):
            k80 = mod9(4*k0 + 2 - 3*d80)
            assert k80 % 3 == (k0 + 2) % 3
            assert k80 != k0, (k0, d80, k80)

    print("PASS rooted sums: (sigma(B),sigma(W)) mod 9 at phases 0,4,8 are (1,6),(5,6),(3,6).")
    print("PASS checkpoint gates: K40=7*K0+4-3*delta40, K80=4*K0+2-3*delta80 mod 9.")
    print("PASS seam-charge cocycle: K40=K0+1 and K80=K0+2 mod 3, independent of centre parity.")
    print("Scope: affine q-shift phase families with sigma(U)=27; no seam return or Lychrel proof.")


if __name__ == "__main__":
    main()
