#!/usr/bin/env python3
"""Prove the scoped 360-step epoch transition using R30's symbolic checker.

Claim checked: for all independent q,k >= 2048, the canonical family
(B W^q [5] U^k 10 reverse(...)) advances in 360 ordinary decimal RAA steps
to a different family with q' = q-8, k' = k-90, U'=(4,9,14), and fixed
finite seam/centre words extracted once from a concrete seed. This is an exact
one-epoch transition, NOT an all-time Lychrel certificate: q and k decrease.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "calculation" / "new_structures" / "R30"))
from parametric import E, R, Q, K, run, clean, reverse, step, zip_pair, load_lattice
from replay_360 import B as BIG_B, W as BIG_W, final_pairword

J0 = [5]
U0 = [9, 14, 4]
C0 = [10]
U1 = [4, 9, 14]
Q_LOSS = 8
K_LOSS = 90
C_GROWTH = 272
QMIN = 2048
KMIN = 2048

def family(B, W, J, U, C, qexp=Q, kexp=K):
    h = [run(B), R(tuple(W), qexp), run(J), R(tuple(U), kexp)]
    return clean(h + [run(C)] + reverse(h))

def extract_candidate(B, W):
    # One concrete orbit is used only to discover finite constants; the
    # independent symbolic equality below proves the transition uniformly.
    p, overflow = final_pairword(160, 320, J0, U0, C0)
    assert sum(overflow) == 90
    assert overflow == [1, 0, 0, 0] * 90
    q2, k2 = 160 - Q_LOSS, 320 - K_LOSS
    c_len = len(C0) + C_GROWTH
    c_start = (len(p) - c_len) // 2
    j_start = len(B) + len(W) * q2
    j_end = c_start - len(U1) * k2
    J1 = p[j_start:j_end]
    C1 = p[c_start:c_start+c_len]
    assert len(J1) == 252
    assert len(C1) == 273
    assert C1 == C1[::-1]
    assert C1[len(C1)//2] % 2 == 0
    assert all(0 <= x <= 18 for x in J1 + C1)
    # Independent concrete-width control, not used as the universal proof.
    for q, k in [(120, 200), (160, 320)]:
        got, ov = final_pairword(q, k, J0, U0, C0)
        assert sum(ov) == 90 and ov == [1, 0, 0, 0] * 90
        expected = (B + W*(q-Q_LOSS) + J1 + U1*(k-K_LOSS) + C1
                    + (U1*(k-K_LOSS))[::-1] + J1[::-1]
                    + (W*(q-Q_LOSS))[::-1] + B[::-1])
        assert got == expected, (q, k, "independent concrete template mismatch")
    return J1, C1

def main():
    data_path = ROOT / "calculation" / "decimal_frontier" / "lattice_kinks" / "data" / "lat_p12m9.txt"
    B, W, _gamma = load_lattice(data_path)
    assert B == BIG_B and W == BIG_W
    assert B[0] > 0 and C0 == C0[::-1] and C0[0] % 2 == 0
    assert all(0 <= x <= 18 for x in B + W + J0 + U0 + C0)
    J1, C1 = extract_candidate(B, W)

    current = family(B, W, J0, U0, C0)
    gamma = []
    missing_odd = []
    for t in range(360):
        offset = E()
        witness = None
        for atom in current:
            for i, coefficient in enumerate(atom.word):
                if coefficient & 1 and atom.n.val(QMIN, KMIN) >= 1:
                    witness = str(offset + E(c=i))
                    break
            if witness is not None:
                break
            offset += atom.length()
        if witness is None:
            missing_odd.append(t)
        current, g = step(current, QMIN, KMIN)
        gamma.append(g)

    expected = family(B, W, J1, U1, C1, Q-E(c=Q_LOSS), K-E(c=K_LOSS))
    equality = zip_pair(current, expected, QMIN, KMIN, compare=True)
    assert equality.get("return") is True, equality
    assert gamma == [1, 0, 0, 0] * 90
    assert sum(gamma) == 90
    assert not missing_odd, missing_odd
    print("SYMBOLIC_TRANSITION_PASS")
    print("scope: all independent q,k >= 2048")
    print("steps=360; overflow clock=(1000)^90; overflow sum=90")
    print("source T0: J=[5], U=(9,14,4), C=[10]")
    print("target T1: q'=q-8, k'=k-90, U'=(4,9,14), |J'|=252, |C'|=273")
    print("odd pair-coefficient guard: all 360 intermediate states")
    print("checker comparison:", equality)
    print("LIMITATION: q and k decrease; this transition alone is not an all-time certificate.")

if __name__ == "__main__":
    main()
