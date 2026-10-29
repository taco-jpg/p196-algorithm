#!/usr/bin/env python3
"""Phase-resolved odd-centre mod-11 gate for the T* p12/m9 family.

Run from the repository root:
    python3 calculation/new_structures/Q36/odd_centre_phase_gate.py

This is a necessary-condition checker for odd-length palindromic centres only.
It does not prune even centres and does not certify a physical seam return.
"""
from tstar_screw import P12, bulk_step, candidates, read_tstar, rotate_left


def A(word):
    return sum(x if i % 2 == 0 else -x for i, x in enumerate(word))


def mod11(x):
    return x % 11


def read_phase_rows():
    lines = [[int(x) for x in s.split()] for s in P12.read_text().splitlines()]
    assert len(lines) == 38 and lines[0] == [12, 34, 9, 10]
    gamma = lines[1]
    W = lines[2:14]
    B = lines[26:38]
    assert len(W) == len(B) == 12
    return gamma, W, B


def phase_gate_truth_table(gamma, W, B):
    # For H=B ++ W^q ++ J ++ U^k and odd palindromic C:
    # A(P)=2*A(H)+(-1)^(q+|J|+k)*A(C) (mod 11).
    # Exhaust all q/k parities and all possible alternating charges of J,C.
    for t in range(12):
        b, w = mod11(A(B[t])), mod11(A(W[t]))
        assert mod11(2*b + w) == 0, (t, b, w)
        for U in candidates():
            u = mod11(A(U))
            for jparity in (0, 1):
                s = 1 if jparity == 0 else -1
                for jcharge in range(11):
                    for ccharge in range(11):
                        values = []
                        for qparity in (0, 1):
                            for kparity in (0, 1):
                                ah = (b + qparity*w
                                      + ((-1)**qparity)*jcharge
                                      + ((-1)**(qparity+jparity))*kparity*u)
                                ap = (2*ah
                                      + ((-1)**(qparity+jparity+kparity))*ccharge) % 11
                                values.append(ap)
                        all_zero = all(v == 0 for v in values)
                        gate = (ccharge == u and
                                (2*jcharge + s*u + 2*b) % 11 == 0)
                        assert all_zero == gate, (t, U, jparity, jcharge, ccharge)
    print("PASS odd-centre A(P) truth table: all 12 root phases, 30 U states, both J parities, all J/C charges.")


def screw_checkpoint_gate(gamma, B):
    checks = 0
    constant_j_cases = []
    for U0 in candidates():
        seq = [U0]
        for t in range(120):
            seq.append(bulk_step(seq[-1], gamma[t % 12]))
        assert seq[40] == rotate_left(list(U0), 1)
        assert seq[80] == rotate_left(list(U0), 2)
        assert seq[120] == U0
        checkpoints = (0, 40, 80)
        ccharges = [mod11(A(seq[t])) for t in checkpoints]
        assert len(set(ccharges)) == 3, (U0, ccharges)
        for jparity in (0, 1):
            s = 1 if jparity == 0 else -1
            j_targets = [mod11(-2*A(B[t % 12]) - s*A(seq[t]))
                         for t in checkpoints]  # target for 2*A(J_t)
            if len(set(j_targets)) == 1:
                constant_j_cases.append((U0, jparity, j_targets[0]))
            checks += 1
    assert checks == 60
    assert set(constant_j_cases) == {
        ((18, 9, 0), 1, 9),
        ((0, 9, 18), 0, 2),
    }, constant_j_cases
    print("PASS 30 U seeds: odd-centre A(C_t) targets are pairwise distinct at t=0,40,80.")
    print("PASS junction target enumerated: nonconstant in 58/60 seed/parity cases; exact two exceptions retained.")
    print("Scope: a fixed odd C cannot span all three checkpoints; phase-mutating centres remain possible.")


def main():
    B0, W0, gamma = read_tstar()
    gamma, W, B = read_phase_rows()
    assert gamma == [int(t % 12 in (0, 4, 8)) for t in range(12)]
    assert B[0] == B0 and W[0] == W0
    phase_gate_truth_table(gamma, W, B)
    screw_checkpoint_gate(gamma, B)


if __name__ == "__main__":
    main()
