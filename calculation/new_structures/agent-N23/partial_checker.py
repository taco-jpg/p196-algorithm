#!/usr/bin/env python3
"""Exact partial-high-block extension of poly_certificate.py (no padding assumption)."""
from fractions import Fraction
from poly_certificate import polynomial,reflected,phi,minus,is_nonzero_for_all_ge
import json,sys
def true_decimal_reverse(parts,B,k):
    last=parts[-1]
    assert 'digits' in last and last['digits']
    high=last['digits'][-1]
    assert 0<high<B
    h=len(str(high)) if k>1 else 1
    assert 1<=h<=k
    trimmed=parts[:-1]+[{'digits':last['digits'][:-1]}]
    if not trimmed[-1]['digits']:trimmed.pop()
    z=polynomial(reflected(trimmed,k),B)
    out={e:Fraction(10**h)*v for e,v in z.items()}
    out[0]=out.get(0,Fraction())+phi(high,h)
    return {e:v for e,v in out.items() if v}
def verify(data):
    B=data['base'];k=data['decimal_block_digits'];q0=data['qmin'];ph=data['phases']
    assert B==10**k and q0>=0
    for t,s in enumerate(ph):
        a=s['parts'];p=polynomial(a,B);r=true_decimal_reverse(a,B,k)
        assert is_nonzero_for_all_ge(minus((1,p),(-1,r)),B,q0), ('possible palindrome',t)
        if t+1<len(ph):
            nxt=polynomial(ph[t+1]['parts'],B)
            assert not minus((1,p),(1,r),(-1,nxt)), ('wrong transition',t)
        for q in (q0,q0+1,q0+3):
            d=[]
            for x in a:d+=x['digits'] if 'digits' in x else x['motif']*(x['slope']*q+x['offset'])
            n=sum(v*B**i for i,v in enumerate(d))
            assert sum(c*(B**(q*e)) for e,c in r.items())==int(str(n)[::-1])
    print(f"PASS radix-{B} genuine decimal reversal, {len(ph)-1} exact polynomial steps for all q>={q0}; all {len(ph)} states nonpalindromic")
if __name__=='__main__':verify(json.load(open(sys.argv[1])))
