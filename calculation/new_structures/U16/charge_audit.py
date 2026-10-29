#!/usr/bin/env python3
"""U16 exact Q9/Q99/Q999 charge audit for rooted p12/m9 templates.

The algebraic recurrence is universal for genuine decimal pairwords. The sampled
120-step controls are only differential checks, not all-width return claims.
Standard library only; run from repository root:
  python3 calculation/new_structures/U16/charge_audit.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(20000)

LAT = Path("calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt")
MODS = (9, 99, 999)

# Three controls cover a previously reported phase-0 seam, an odd-centre
# mod-99-admissible family, and an even-centre branch not subject to Q39 gates.
CASES = {
    "R02_seam19": {
        "J": [12,14,9,16,2,4,3,11,10,11,4,11,8,8,10,9,7,9,16],
        "U": [8,9,10], "C": [5,12,5], "k": lambda q: 4*q,
    },
    "odd_C_mod99_gate": {
        "J": [11], "U": [9,8,10], "C": [0], "k": lambda q: 4*q,
    },
    "even_C_control": {
        "J": [5], "U": [9,2,16], "C": [8,8], "k": lambda q: 4*q,
    },
}


def load_root(path: Path = LAT):
    lines = path.read_text().strip().splitlines()
    p, nb, m, base = map(int, lines[0].split())
    assert (p, nb, m, base) == (12, 34, 9, 10)
    gamma = list(map(int, lines[1].split()))
    W = [list(map(int, lines[2+i].split())) for i in range(p)]
    B = [list(map(int, lines[2+2*p+i].split())) for i in range(p)]
    assert gamma == [1,0,0,0]*3
    assert len(B[0]) == 34 and len(W[0]) == 9
    return B[0], W[0], gamma


def template(B, W, J, U, C, q, k):
    H = B + W*q + J + U*k
    return H + C + H[::-1]


def pairword(digits):
    return [digits[i] + digits[-1-i] for i in range(len(digits))]


def digits_from_int(n):
    return [int(ch) for ch in str(n)[::-1]]


def value_of_digits(digits):
    return int("".join(str(x) for x in digits[::-1]))


def reverse_add_bigint(n):
    s = str(n)
    return n + int(s[::-1])


def r30_digits(n):
    """Port of R30 parametric.py's independent divmod digit extraction."""
    out = []
    while n:
        out.append(n % 10)
        n //= 10
    return out or [0]


def r30_value(word):
    """Port of R30 parametric.py's value() over an LSD-first word."""
    value = 0
    for a in reversed(word):
        value = value*10 + a
    return value


def reverse_add_r30_style(n):
    d = r30_digits(n)
    return n + r30_value(d[::-1])


def r30_actual_pair(n):
    d = r30_digits(n)
    return [a+b for a,b in zip(d, reversed(d))]


def canonical_digits(P):
    """Realise a symmetric coefficient word as decimal digits, LSD first."""
    n = len(P)
    d = [0]*n
    for i in range(n//2):
        lo = min(P[i], 9)
        hi = P[i] - lo
        assert 0 <= lo <= 9 and 0 <= hi <= 9
        d[i], d[n-1-i] = lo, hi
    if n % 2:
        mid = n//2
        assert P[mid] % 2 == 0, "odd-length pairword midpoint must be even"
        d[mid] = P[mid]//2
    assert pairword(d) == P
    assert d[-1] != 0
    return d


def digit_array_step(d):
    """Independent fresh-buffer schoolbook reverse-and-add."""
    P = pairword(d)
    carries = [0]
    out = []
    for p in P:
        z = p + carries[-1]
        out.append(z % 10)
        carries.append(z // 10)
    if carries[-1]:
        out.append(carries[-1])
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out, P, carries


def qval(P, modulus):
    # Horner evaluation of the LSD-first coefficient polynomial.
    value = 0
    for p in P[::-1]:
        value = (10*value + p) % modulus
    return value


def q999_kappa(carries):
    # 10^(-1) == 100 modulo 999, so no modular division is needed.
    value = 0
    weight = 1
    for c in carries:
        value = (value + c*weight) % 999
        weight = (100*weight) % 999
    return value


def template_charge_table():
    rows = []
    for a in range(0, 19, 2):
        base = (9, a, 18-a)
        for r in range(3):
            U = base[r:] + base[:r]
            qu = qval(list(U), 999)
            qrev = qval(list(U[::-1]), 999)
            f = [(qu + pow(10,c,999)*qrev) % 999 for c in range(3)]
            zeros = [c for c,x in enumerate(f) if x == 0]
            assert zeros == [(1+r) % 3], (a,r,U,f,zeros)
            rows.append({"a":a,"rotation":r,"U":list(U),"Q999_U":qu,
                         "Q999_revU":qrev,"F_c0_c1_c2":f,"conserving_C_len_mod3":zeros[0]})
    assert len({tuple(row["U"]) for row in rows}) == 30
    return rows


def audit_case(B, W, name, q):
    case = CASES[name]
    J, U, C = case["J"], case["U"], case["C"]
    k = case["k"](q)
    P0 = template(B, W, J, U, C, q, k)
    target = template(B, W, J, U, C, q, k+5)
    digits = canonical_digits(P0)
    n = value_of_digits(digits)
    assert pairword(digits) == P0
    assert reverse_add_bigint(n) == value_of_digits(digit_array_step(digits)[0])

    source_q = {m:qval(P0,m) for m in MODS}
    hlen = len(B) + len(W)*q + len(J) + len(U)*k
    delta_formula = (5*pow(10,hlen,999) *
                     (qval(U,999) + pow(10,len(C),999)*qval(U[::-1],999))) % 999
    assert (qval(target,999)-source_q[999]) % 999 == delta_formula
    assert qval(target,99) == (55*source_q[99]) % 99
    Aprod999 = 1
    S111 = 0
    overflows = 0
    for t in range(120):
        next_digits, P, carries = digit_array_step(digits)
        next_n = reverse_add_bigint(n)
        assert next_n == reverse_add_r30_style(n), (name,q,t,"R30-style integer mismatch")
        assert value_of_digits(next_digits) == next_n, (name,q,t,"integer mismatch")
        assert next_digits == digits_from_int(next_n), (name,q,t,"digit mismatch")
        Pnext = pairword(next_digits)
        assert Pnext == r30_actual_pair(next_n), (name,q,t,"R30-style pairword mismatch")
        g = carries[-1]
        overflows += g
        A999 = (1 + pow(10,g,999)) % 999
        kappa = q999_kappa(carries)
        X999 = pow(10, len(P)-1+g, 999)*kappa % 999
        predicted = (A999*qval(P,999) - 99*X999) % 999
        assert qval(Pnext,999) == predicted, (name,q,t,"Q999 recurrence")
        assert qval(Pnext,99) == ((1+pow(10,g,99))*qval(P,99))%99, (name,q,t,"Q99 recurrence")
        assert qval(Pnext,9) == (2*qval(P,9))%9, (name,q,t,"Q9 recurrence")
        # Since 99*X only matters modulo 999 through X mod 111.
        S111 = (A999*S111 + X999) % 111
        Aprod999 = A999*Aprod999 % 999
        digits, n = next_digits, next_n

    assert overflows == 30
    assert Aprod999 == 73
    P120 = pairword(digits)
    Qtarget999 = qval(target,999)
    Qactual999 = qval(P120,999)
    diff = (Qtarget999 - Aprod999*source_q[999]) % 999
    assert diff % 9 == 0
    target_cocycle_residual = (diff//9 + 11*S111) % 111
    diff_actual = (Qactual999 - Aprod999*source_q[999]) % 999
    assert diff_actual % 9 == 0
    actual_cocycle_residual = (diff_actual//9 + 11*S111) % 111
    assert actual_cocycle_residual == 0
    mismatches = [i for i,(x,y) in enumerate(zip(P120,target)) if x != y]
    first = mismatches[0] if mismatches else None
    return {
        "case":name,"q":q,"k":k,"pairword_length":len(P0),"overflows":overflows,
        "Q9_source_target":[source_q[9],qval(target,9)],
        "Q99_source_target":[source_q[99],qval(target,99)],
        "Q999_source_target_actual120":[source_q[999],Qtarget999,Qactual999],
        "macro_multiplier_Q999":Aprod999,"carry_cocycle_S_mod111":S111,
        "target_cocycle_residual_mod111":target_cocycle_residual,
        "actual_cocycle_residual_mod111":actual_cocycle_residual,
        "first_template_mismatch":first,"mismatch_count":len(mismatches),
        "full_endpoint_return":P120 == target,
    }


def main():
    B,W,gamma = load_root()
    assert pow(2,120,9) == 1
    assert (pow(2,90,99)*pow(11,30,99)) % 99 == 55
    assert (pow(2,90,999)*pow(11,30,999)) % 999 == 73
    rows = template_charge_table()
    print("U3_TEMPLATE_Q999_CONSERVATION_TABLE_PASS", len(rows), "words")
    print(json.dumps(rows, separators=(",",":")))
    for name in CASES:
        for q in (20,40,80,160):
            row = audit_case(B,W,name,q)
            assert row["macro_multiplier_Q999"] == 73
            assert row["overflows"] == 30
            print("BIGINT_AND_DIGIT_ARRAY_PASS", json.dumps(row, separators=(",",":")), flush=True)
    print("U16_CHARGE_AUDIT_PASS; sampled controls are not return claims")


if __name__ == "__main__":
    main()
