#!/usr/bin/env python3
"""Q01: independent whole-integer controls for the clock/growth necessary condition.

Run from repository root:
  python3 calculation/new_structures/Q01/cert_spec_check.py

Only the positive controls are certificates, and only by their pre-existing proofs.
The decimal runs here deliberately test the exterior/clock for ONE period, not forever.
"""
from __future__ import annotations
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WIDTHS = (20, 40, 80, 160)

def value(word, base):
    out = 0
    for digit in reversed(word):
        out = out * base + digit
    return out

def digits(number, base):
    assert number > 0
    out = []
    while number:
        number, d = divmod(number, base)
        out.append(d)
    return out

def pairword(number, base):
    d = digits(number, base)
    return [x+y for x,y in zip(d, reversed(d))]

def realize_pairword(P, base):
    """Make a canonical integer having the prescribed mirrored digit sums."""
    assert P == list(reversed(P))
    n = len(P)
    d = [0] * n
    for i in range(n//2):
        hi = min(base-1, P[i])
        lo = P[i]-hi
        assert 0 <= lo < base and 0 <= hi < base
        d[i], d[-1-i] = lo, hi
    if n % 2:
        assert P[n//2] % 2 == 0
        d[n//2] = P[n//2]//2
    assert d[-1] != 0
    out = value(d, base)
    assert pairword(out, base) == P
    return out

def advance(n, base):
    d = digits(n, base)
    # Independent full-integer reverse-and-add, not the pairword normalizer.
    next_n = n + value(list(reversed(d)), base)
    # Cross-check the identity from the independently assembled pairword.
    assert next_n == value(pairword(n, base), base)
    assert len(digits(next_n, base)) in (len(d), len(d)+1)
    return next_n

def block(W, length):
    return [W[i % len(W)] for i in range(length)]

def merged(B, W, length):
    return B + block(W, length) + list(reversed(B))

def paired(B, W, C, q):
    half = B + W*q
    return half + C + list(reversed(half))

def base9_control():
    s = (ROOT/'lean/P196/LatticeBand/Base9.lean').read_text()
    B, W = {}, {}
    for typ, phase, body in re.findall(
        r'def ([BW])(\d+) : List Nat := \[([^\]]+)\]', s):
        row = [int(v.strip()) for v in body.split(',')]
        (B if typ == 'B' else W)[int(phase)] = row
    assert len(B) == len(W) == 10
    assert len(B[0]) == 61 and len(W[0]) == 4
    for q in WIDTHS:
        length = 4*q+2
        n = realize_pairword(merged(B[0], W[0], length), 9)
        gamma = []
        for t in range(20):
            assert pairword(n, 9) == merged(B[t%10], W[t%10], length)
            d = digits(n, 9)
            assert d != list(reversed(d))
            nn = advance(n, 9)
            g = len(digits(nn, 9)) - len(d)
            gamma.append(g)
            length += g
            n = nn
        assert gamma[:10] == [1,1,0,0,0,0,1,1,0,0]
        assert length == 4*q+10
    print('BASE9_LEAN_CERT_CONTROL_PASS: 20 full steps at q=20,40,80,160; two +4 cycles')

def base50_control():
    source = ROOT/'calculation/neutral_band/agent10_base50/cert_b50.json'
    edges = json.loads(source.read_text())['edges']
    assert len(edges) == 4
    for q in WIDTHS:
        length = q
        e0 = edges[0]
        n = realize_pairword(paired(e0['B'], [49], e0['C'], length), 50)
        gamma = []
        for t in range(12):
            e = edges[t%4]
            assert pairword(n, 50) == paired(e['B'], [49], e['C'], length)
            d = digits(n, 50)
            assert d != list(reversed(d))
            nn = advance(n, 50)
            g = len(digits(nn, 50))-len(d)
            assert g == e['gamma']
            gamma.append(g)
            nxt = edges[(t+1)%4]
            leftover = len(digits(nn,50))-2*len(nxt['B'])-len(nxt['C'])
            assert leftover % 2 == 0
            length = leftover//2
            n = nn
        assert gamma == [0,1,0,1]*3
        assert length == q+3
    print('BASE50_NEUTRAL_CERT_CONTROL_PASS: 12 full steps at q=20,40,80,160; three +1 cycles')

def read_lattice(path):
    rows = (ROOT/path).read_text().strip().splitlines()
    p, nB, m, base = map(int, rows[0].split())
    gamma = list(map(int, rows[1].split()))
    W = [list(map(int, s.split())) for s in rows[2:2+p]]
    B = [list(map(int, s.split())) for s in rows[2+2*p:2+3*p]]
    assert len(B) == len(W) == p
    assert all(len(x)==m for x in W)
    assert all(len(x)==nB for x in B)
    return p, m, gamma, B, W

def decimal_control(name, p, m, gamma, B, W):
    assert len(gamma) == p
    for q in WIDTHS:
        # An even midpoint coefficient is needed to realize an odd-length pairword.
        n = realize_pairword(paired(B[0], W[0], [8], q), 10)
        for t in range(p):
            P = pairword(n, 10)
            assert P[:len(B[t])+m] == B[t] + W[t]
            d = digits(n, 10)
            nn = advance(n, 10)
            assert len(digits(nn,10))-len(d) == gamma[t]
            n = nn
    print(name+': ONE exterior period of real integers at q=20,40,80,160, NOT a certificate')

def arithmetic():
    # (name, temporal clock p, overflows S per period, spatial period m,
    #  copies of a complete spatial block inserted in an exact phase return)
    fixtures = [
        ('base9 merged',10,4,4,1,10,1),
        ('base50 paired',4,2,1,2,4,1),
        ('decimal p8/m20 paired',8,4,20,2,80,1),
        ('decimal p8/m48 paired',8,4,48,2,192,1),
        ('decimal p12/m9 paired, pre-charge',12,3,9,2,72,1),
        ('decimal p8/m20 merged',8,4,20,1,40,1),
        ('decimal p8/m48 merged',8,4,48,1,96,1),
        ('decimal p12/m9 merged',12,3,9,1,36,1),
    ]
    for name,p,S,m,c,k,g in fixtures:
        h = math.gcd(c*m, S)
        assert k == p*(c*m//h) and g == S//h
        assert (k//p)*S == c*m*g
        print('CLOCK_LENGTH_PASS',name,'k_min',k,'g_min',g)
    p,m,gamma,B,W=read_lattice(
        'calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt')
    assert sum(W[0]) == 60
    # k=72*g, and 2^k == 1 mod 9; fixed centre requires 2*g*60 == 0 mod 9.
    assert all((2*g*sum(W[0]))%9 != 0 for g in (1,2))
    assert (2*3*sum(W[0]))%9 == 0
    assert (2**72-1)%9 == 0
    print('DECIMAL_P12_FIXED_CENTRE_CHARGE_PASS: k_min_charge=216, g_min_charge=3 (already Y18)')

def main():
    arithmetic()
    base9_control()
    base50_control()
    p8 = json.loads(
        (ROOT/'calculation/new_structures/agent-N10/phase.json').read_text())
    assert p8['gammas'] == [1,0,1,0,1,0,1,0]
    assert sum(p8['W0']) % 9 == 0
    decimal_control('DECIMAL_P8_M20_REC0_CLOCK_CONTROL_PASS',8,20,p8['gammas'],
                    p8['phase_B'],p8['phase_W'])
    for name,path in (
        ('DECIMAL_P8_M48_REC2_CLOCK_CONTROL_PASS',
         'calculation/decimal_frontier/lattice_kinks/data/lat2.txt'),
        ('DECIMAL_P12_M9_CLOCK_CONTROL_PASS',
         'calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt')):
        p,m,gamma,B,W=read_lattice(path)
        decimal_control(name,p,m,gamma,B,W)
    print('Q01_CERT_SPEC_CONTROLS_PASS (no decimal all-time conclusion)')

if __name__ == '__main__':
    main()
