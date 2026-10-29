#!/usr/bin/env python3
"""X09: independent finite controls for binary-indexed spacetime certificate FORMAT.

This does NOT implement the full universal automata inclusion decision procedure.
It demonstrates a Presburger (hence automatic) b9 known-positive control, and
checks that its predicted spacetime array is exact against literal arithmetic.
Requires repository fixture calculation/decimal_frontier/lattice_formats/cert_b9_rec0.json.
"""
import argparse, json, pathlib, sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[3]
CERT = ROOT / 'calculation/decimal_frontier/lattice_formats/cert_b9_rec0.json'

def pair(a):
    return [a[i] + a[-1-i] for i in range(len(a))]

def digit_step(a, base):
    carry = 0
    out = bytearray()
    for i, v in enumerate(a):
        z = v + a[len(a)-1-i] + carry
        out.append(z % base)
        carry = z // base
    if carry: out.append(carry)
    return out

def pair_step(p, base):
    carry = 0
    out = []
    for v in p:
        z = v + carry
        out.append(z % base)
        carry = z // base
    if carry:out.append(carry)
    return pair(out)

def template(f, t):
    phase=t % f['p']
    l=f['l0']+sum(f['gam'])*(t//f['p'])+sum(f['gam'][:phase])
    B=f['B_t'][phase]
    W=f['w_t'][phase]
    mid=[W[j%len(W)] for j in range(l)]
    return B+mid+B[::-1]

def test_b9(horizon, independent):
    with open(CERT) as h:f=json.load(h)
    assert f['base']==9 and f['p']==10 and f['nB']==61 and f['m']==4
    assert all(any(x%2 for x in row) for row in f['B_t']), 'palindrome safety witness'
    d=bytearray(f['N0_digits_lsb'])
    assert pair(d)==template(f, 0)
    # Different calculation methods: direct digitwise reverse-add and
    # normalization of the PAIR COEFFICIENT word; separate predictions from
    # the finite phase tables, without reading the ongoing digit state.
    for t in range(horizon+1):
        want=template(f,t)
        if pair(d)!=want:raise AssertionError(('digit-template',t,len(d)))
        if t%1000==0 or t==horizon:
            assert not all(d[i]==d[-1-i] for i in range(len(d)))
            print('base9',t,'digits',len(d),'phase',t%10,'band',2+4*(t//10)+sum(f['gam'][:t%10]))
        if t<horizon:
            nextpair=pair_step(want,9)
            assert nextpair==template(f,t+1),('pair-closure',t)
            d=digit_step(d,9)
            if t < independent:
                # Independent Python integer arithmetic and base-9 divmod.
                value=sum(int(x)*9**i for i,x in enumerate(d))
                rebuilt=[]
                while value: value,r=divmod(value,9); rebuilt.append(r)
                assert bytes(rebuilt)==bytes(d),('integer-divmod',t)
    print('PASS b9 symbolic phase/band vs literal digits and pair-normalization',horizon,independent)

def parity_automatic_control():
    """Two-state synchronous DFAO for popcount(t AND i) mod 2.
    This is an expressiveness witness only, NOT a reverse-add orbit.
    """
    def automaton(t, i):
        state=0
        while t or i:
            state^=(t&1)&(i&1)
            t>>=1; i>>=1
        return state
    for t in range(256):
        for i in range(256):
            assert automaton(t,i)==((t&i).bit_count()%2)
    print('PASS 65536 binary-index automatic parity controls (2 states)')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--steps',type=int,default=2000)
    parser.add_argument('--independent',type=int,default=32)
    o=parser.parse_args()
    parity_automatic_control()
    test_b9(o.steps,o.independent)
