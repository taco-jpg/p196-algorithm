#!/usr/bin/env python3
"""Symbolically check four successive 360-step AA56 epoch-map edges.

For each edge, finite J_n/C_n constants are discovered from one genuine
integer orbit, then the R30 symbolic pairword checker verifies the full edge
for every independent q,k >= 2048. This does NOT prove an infinite orbit:
the checked map consumes q and k on every edge.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "calculation" / "new_structures" / "R30"))
from parametric import E, R, Q, K, run, clean, reverse, step, zip_pair, load_lattice
from replay_360 import final_pairword, B as BIG_B, W as BIG_W

J = [5]
U = [9, 14, 4]
C = [10]
U_OUT = [4, 9, 14]
QMIN = 2048
KMIN = 2048
SAMPLE_Q = 1000
SAMPLE_K = 1000

def family(B, W, J, U, C, qexp=Q, kexp=K):
    h = [run(B), R(tuple(W), qexp), run(J), R(tuple(U), kexp)]
    return clean(h + [run(C)] + reverse(h))

def symbolic_edge(B, W, J, U, C, Jnext, Unext, Cnext, n):
    qloss = 8
    kloss = 89 + n
    current = family(B, W, J, U, C)
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
    expected = family(B, W, Jnext, Unext, Cnext,
                      Q-E(c=qloss), K-E(c=kloss))
    equality = zip_pair(current, expected, QMIN, KMIN, compare=True)
    assert equality.get("return") is True, (n, equality)
    assert gamma == [1, 0, 0, 0] * 90, (n, gamma)
    assert sum(gamma) == 90
    assert not missing_odd, (n, missing_odd)
    return equality

def main():
    global J, U, C, SAMPLE_Q, SAMPLE_K
    data_path = ROOT / "calculation" / "decimal_frontier" / "lattice_kinks" / "data" / "lat_p12m9.txt"
    B, W, _gamma = load_lattice(data_path)
    assert B == BIG_B and W == BIG_W
    assert B[0] > 0 and C == C[::-1] and C[0] % 2 == 0
    assert all(0 <= x <= 18 for x in B + W + J + U + C)

    for n in range(1, 5):
        qnext = SAMPLE_Q - 8
        kloss = 89 + n
        knext = SAMPLE_K - kloss
        cnext_len = 3*n*n + 267*n + 3
        p, overflow = final_pairword(SAMPLE_Q, SAMPLE_K, J, U, C)
        assert overflow == [1, 0, 0, 0] * 90 and sum(overflow) == 90
        cstart = (len(p) - cnext_len) // 2
        jstart = len(B) + len(W)*qnext
        jend = cstart - len(U_OUT)*knext
        Jnext = p[jstart:jend]
        Cnext = p[cstart:cstart+cnext_len]
        assert len(Jnext) == 252*n, (n, len(Jnext), 252*n)
        assert len(Cnext) == cnext_len
        assert Cnext == Cnext[::-1], n
        assert Cnext[len(Cnext)//2] % 2 == 0, n
        assert all(0 <= x <= 18 for x in Jnext + Cnext), n
        concrete_expected = (B + W*qnext + Jnext + U_OUT*knext + Cnext
                             + (U_OUT*knext)[::-1] + Jnext[::-1]
                             + (W*qnext)[::-1] + B[::-1])
        assert p == concrete_expected, (n, "sample does not match extracted family")

        equality = symbolic_edge(B, W, J, U, C, Jnext, U_OUT, Cnext, n)
        print(f"EPOCH_{n}_SYMBOLIC_PASS q'=q-8 k'=k-{kloss} "
              f"|J'|={len(Jnext)} |C'|={len(Cnext)} "
              f"symbolic_length={equality['length']}")
        J, U, C = Jnext, U_OUT, Cnext
        SAMPLE_Q, SAMPLE_K = qnext, knext

    print("SCOPE: four individually universal 360-step edges, each for all independent q,k >= 2048.")
    print("Every edge has overflow clock (1000)^90 and an odd pair-coefficient guard at all phases.")
    print("LIMITATION: q decreases by 8 per edge and k decreases by 90,91,92,93; no cycle or all-time certificate is proved.")

if __name__ == "__main__":
    main()
