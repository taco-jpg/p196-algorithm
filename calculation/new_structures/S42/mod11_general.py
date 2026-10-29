#!/usr/bin/env python3
"""S42: all-width parity-correct mod-11 gate for a repeated coefficient band.

The paper lemma is the theorem below; finite controls are independent checks of
one mixed-U6 epoch-map candidate, not a decimal Lychrel certificate.
Run from the repository root: python3 calculation/new_structures/S42/mod11_general.py
"""
from itertools import product
import sys
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

B = (10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5)
W = (5,18,4,8,1,15,4,0,5)
G = (1,0,0,0,1,0,0,0,1,0,0,0)
A = (7,7,11,11,9,9)
B6 = (11,11,7,7,9,9)


def alt(x):
    return sum((-1)**i * a for i, a in enumerate(x))


assert len(B) % 2 == 0 and len(W) % 2 == 1
assert alt(B) % 11 == alt(W) % 11 == 0


def word(q, k, J, U, C):
    H = B + W*q + tuple(J) + tuple(U)*k
    return H + tuple(C) + H[::-1]


def source_digits(P):
    """Canonical LSD-first decimal source for a symmetric pair-coefficient word."""
    assert P == P[::-1] and P[0] > 0 and all(0 <= x <= 18 for x in P)
    n = len(P)
    d = [0]*n
    for i in range(n//2):
        lo = max(P[i]-9, 0)
        hi = P[i]-lo
        assert 0 <= lo <= 9 and 0 <= hi <= 9
        d[i], d[n-1-i] = lo, hi
    if n % 2:
        assert P[n//2] % 2 == 0
        d[n//2] = P[n//2]//2
    assert d[-1] != 0
    return d


def int_value(d):
    return int(''.join(map(str, reversed(d))))


def reverse_add_digits(d):
    out, carry = [], 0
    for i in range(len(d)):
        z = d[i] + d[-1-i] + carry
        out.append(z % 10)
        carry = z // 10
    if carry:
        out.append(carry)
    return out


def pairword(d):
    return tuple(d[i] + d[-1-i] for i in range(len(d)))


def bulk_step(u, gamma):
    """Independent two-ended cyclic carry fixed points for a spatial tile."""
    n = len(u)
    def carry(reverse):
        for init in (0, 1):
            c, v = init, [0]*n
            it = range(n-1, -1, -1) if reverse else range(n)
            for i in it:
                v[i] = c
                c = (u[i] + c)//10
            if c == init:
                return v
        raise AssertionError((u, reverse))
    lo, hi = carry(False), carry(True)
    dl = [(x+c) % 10 for x,c in zip(u,lo)]
    dh = [(x+c) % 10 for x,c in zip(u,hi)]
    return tuple(dl[i] + dh[(i-gamma) % n] for i in range(n))


def cut_charge(rows):
    """Exact Q mod 9 from the physical low/high carries on all six cuts."""
    T, m = len(rows), len(rows[0])
    gammas = tuple(G[t % 12] for t in range(T))
    lam = tuple(pow(2, -t, 9) for t in range(T))
    result = []
    for cut in range(m):
        Q = 0
        for t, row in enumerate(rows):
            def carry(reverse):
                for init in (0,1):
                    c, v = init, [0]*m
                    it = range(m-1,-1,-1) if reverse else range(m)
                    for i in it:
                        v[i] = c
                        c = (row[i]+c)//10
                    if c == init:
                        return v
                raise AssertionError((row,reverse))
            L, D = carry(False), carry(True)
            Y = (row[(cut-1)%m]+D[(cut-1)%m])%10 if gammas[t] else 0
            Q += lam[t]*(L[cut]-(row[cut]+D[cut])//10+gammas[t]*Y)
        result.append(Q%9)
    return tuple(result)


def check_general_formula():
    """Exhaustively test the derived formula on small words and both C parities."""
    alphabet = (0, 2, 9, 11, 18)
    words = [()]
    for n in range(1,4):
        words.extend(tuple(x) for x in product(alphabet, repeat=n))
    Jwords = [x for x in words if len(x) <= 2]
    Uwords = [x for x in words if 1 <= len(x) <= 3]
    cases = 0
    for J in Jwords:
        for U in Uwords:
            for k in range(4):
                for q in range(3):
                    H = B + W*q + J + U*k
                    for c in range(0,19,2):
                        for C in ((c,c),(c,)):
                            P = H + C + H[::-1]
                            exact = alt(P) % 11
                            if len(C) % 2 == 0:
                                predicted = 0
                            elif len(U) % 2:
                                eps = k % 2
                                bracket = 2*alt(J) + (-1)**len(J)*(2*eps*alt(U)+(-1)**k*alt(C))
                                predicted = ((-1)**q * bracket) % 11
                            else:
                                bracket = 2*alt(J) + (-1)**len(J)*(2*k*alt(U)+alt(C))
                                predicted = ((-1)**q * bracket) % 11
                            assert exact == predicted, (q,k,J,U,C,exact,predicted)
                            cases += 1
    print(f"GENERAL_FORMULA_PASS cases={cases}")



def progression_bracket(J, U, C, k):
    """Mod-11 bracket after removing the irrelevant factor (-1)^q."""
    if len(U) % 2:
        return 2*alt(J) + (-1)**len(J)*(2*(k % 2)*alt(U) + (-1)**k*alt(C))
    return 2*alt(J) + (-1)**len(J)*(2*k*alt(U) + alt(C))


def progression_gate(J, U, C, k0, delta):
    """Exact all-n condition on the reachable progression k=k0+delta*n."""
    if len(C) % 2 == 0:
        return True
    if len(U) % 2:
        if delta % 2:
            return (alt(U)-alt(C)) % 11 == 0 and (2*alt(J)+(-1)**len(J)*alt(C)) % 11 == 0
        return progression_bracket(J,U,C,k0) % 11 == 0
    base = progression_bracket(J,U,C,k0) % 11 == 0
    slope = (2*delta*alt(U)) % 11 == 0
    return base and slope


def check_progression_gate():
    """Check phase-indexed k progressions, including delta divisible by 11."""
    alphabet = (0,2,9,11,18)
    Jwords = [()] + [(x,) for x in alphabet]
    Uwords = [(x,) for x in alphabet] + list(product(alphabet, repeat=2))
    Codd = [(c,) for c in range(0,19,2)]
    Codd += [(a,b,a) for a in alphabet for b in (0,2,18)]
    checked = 0
    for J in Jwords:
        for U in Uwords:
            for C in Codd:
                for k0 in range(6):
                    for delta in range(12):
                        observed = all(progression_bracket(J,U,C,k0+delta*n) % 11 == 0 for n in range(11))
                        predicted = progression_gate(J,U,C,k0,delta)
                        assert observed == predicted, (J,U,C,k0,delta,observed,predicted)
                        checked += 1
    print(f"PROGRESSION_GATE_PASS cases={checked}; delta mod 11 and parity handled exactly")


def check_bulk_and_real_orbits():
    rows = []
    u = A
    for t in range(240):
        rows.append(u)
        u = bulk_step(u, G[t % 12])
    assert rows[120] == B6 and u == A
    assert all(sum(row) == 54 for row in rows)
    assert alt(A) % 11 == alt(B6) % 11 == 0
    assert cut_charge(rows) == (0,0,0,0,0,0)
    print("U6_BULK_PASS phase120=B6 phase240=A sum=54 alt=0 mod11 cutQ=(0,)*6")

    modes = (((9,), (18,), A), ((6,), (12,), B6), ((3,), (6,), A),
             ((9,), (18,), B6), ((6,), (12,), A), ((3,), (6,), B6))
    charges = []
    for J,C,U in modes[:3]:
        assert len(U) % 2 == 0 and alt(U) % 11 == 0
        assert (2*alt(J)-alt(C)) % 11 == 0
        charges.append((2*sum(J)+sum(C))%9)
    assert charges == [0,6,3]
    assert all((charges[(i+1)%3] - charges[i]) % 9 == 6 for i in range(3))
    print("MODE_GATES_PASS odd-centre phase gates=0; mod9 seam charges=0,6,3")

    for q in (20,40,80,160):
        k = 2*q
        J,C,U = modes[0]
        d = source_digits(word(q,k,J,U,C))
        n = int_value(d)
        first_diffs, palindromes = [], []
        clocks = []
        for t in range(720):
            s = str(n)
            if s == s[::-1]:
                palindromes.append(t)
            nd = reverse_add_digits(d)
            nn = n + int(s[::-1])
            assert int_value(nd) == nn, (q,k,t,"bigint/digit-array")
            clocks.append(len(nd)-len(d))
            d, n = nd, nn
            if (t+1) % 120 == 0:
                epoch = (t+1)//120
                if epoch < 6:
                    qe,ke = q+epoch,k+epoch
                    Je,Ce,Ue = modes[epoch]
                else:
                    qe,ke = q+6,k+6
                    Je,Ce,Ue = modes[0]
                actual = pairword(d)
                target = word(qe,ke,Je,Ue,Ce)
                mismatch = next((i for i,(x,y) in enumerate(zip(actual,target)) if x != y), None)
                assert mismatch is not None
                first_diffs.append(mismatch)
        if str(n) == str(n)[::-1]:
            palindromes.append(720)
        x = 34 + 9*q
        expected = [x-23,x-46,x-67,x-90,x-113,x-136]
        assert first_diffs == expected, (q,k,first_diffs,expected)
        assert clocks == [G[t%12] for t in range(720)]
        assert not palindromes
        print(f"TRUE_DECIMAL_CONTROL q={q} k={k} steps=720 clock=PASS palindromes=0 endpoint_mismatches={first_diffs}")


if __name__ == "__main__":
    check_general_formula()
    check_progression_gate()
    check_bulk_and_real_orbits()
