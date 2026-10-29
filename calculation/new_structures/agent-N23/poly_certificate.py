#!/usr/bin/env python3
"""Exact sparse-polynomial validator for affinely pumped, possibly multi-band digit words.
Word is LSB-first as alternating literal and repeated parts. A repeated part
{'motif':[...],'slope':a,'offset':c} means motif repeated a*q+c times.
Equality to a reverse-and-add successor is verified as a rational polynomial
identity in Z=base**q. No bounded-length simulation is used for soundness.
"""
from fractions import Fraction
from math import gcd
import json,sys

def build_word(parts,q):
    z=[]
    for x in parts:
        if 'digits' in x: z+=x['digits']
        else: z+=x['motif']*(x['slope']*q+x['offset'])
    return z

def phi(d, block_decimal_digits):
    if block_decimal_digits==1:return d
    k=block_decimal_digits; s=str(d).zfill(k)
    return int(s[::-1])

def reflected(parts,k):
    return [{'digits':[phi(x,k) for x in part['digits'][::-1]]} if 'digits' in part
            else {'motif':[phi(x,k) for x in part['motif'][::-1]],
                  'slope':part['slope'],'offset':part['offset']}
            for part in parts[::-1]]

def add_to(a,p,v):
    a[p]=a.get(p,Fraction())+v
    if not a[p]:del a[p]

def polynomial(parts,B):
    """Value(word(q)) = sum_e coeff[e] * Z**e, Z=B**q, exact fractions."""
    ans={};s=0;v=0
    for part in parts:
        if 'digits' in part:
            for i,d in enumerate(part['digits']):
                assert 0<=d<B
                if d:add_to(ans,s,Fraction(d*pow(B,v+i)))
            v+=len(part['digits'])
        else:
            motif=part['motif'];a=part['slope'];c=part['offset'];m=len(motif)
            assert m>0 and a>=0 and c>=0 and all(0<=d<B for d in motif)
            val=sum(x*pow(B,i) for i,x in enumerate(motif))
            f=Fraction(val*pow(B,v),pow(B,m)-1)
            add_to(ans,s,-f)
            add_to(ans,s+a*m,f*pow(B,m*c))
            s+=a*m;v+=c*m
    return ans

def minus(*polys):
    ans={}
    for sign,p in polys:
        for e,x in p.items(): add_to(ans,e,sign*x)
    return ans

def shift(parts,delta):
    return [{**p,'offset':p['offset']+p['slope']*delta} if 'motif' in p else p
            for p in parts]

def is_nonzero_for_all_ge(poly, B, qmin):
    """Exact positive-integer-root argument: an integer root divides constant term."""
    if not poly:return False
    es=sorted(poly); lower=es[0]
    denomin=1
    for v in poly.values():denomin=denomin*v.denominator//gcd(denomin,v.denominator)
    ints={e-lower:int(v*denomin) for e,v in poly.items()}
    c=abs(ints[0]); assert c>0
    Z=pow(B,qmin);q=qmin
    while Z<=c:
        if sum(v*pow(Z,e) for e,v in ints.items())==0:return False
        Z*=B;q+=1
    return True

def check(data):
    B=data['base'];k=data.get('decimal_block_digits',1);qmin=data['qmin'];T=data['phases']
    assert qmin>=0 and B==(10**k if k>1 else B) and B>=2
    gain=data.get('cycle_parameter_gain')
    if gain is not None:
        assert gain>=0
        edges=[(t,t+1,0) for t in range(len(T)-1)]+[(len(T)-1,0,gain)]
    else:
        edges=[(t,t+1,0) for t in range(len(T)-1)]
    for t,t2,delta in edges:
        src=T[t];dest=T[t2];a=src['parts'];b=shift(dest['parts'],delta)
        assert all('digits' in p or p['offset']>=0 for p in a+b)
        assert 'digits' in a[-1] and a[-1]['digits'] and a[-1]['digits'][-1]>= (10**(k-1) if k>1 else 1)
        apr=polynomial(a,B);arp=polynomial(reflected(a,k),B);nxt=polynomial(b,B)
        residue=minus((1,apr),(1,arp),(-1,nxt))
        assert not residue, ('edge mismatch',t,len(residue),str(residue)[:200])
        palindrome_difference=minus((1,apr),(-1,arp))
        assert is_nonzero_for_all_ge(palindrome_difference,B,qmin), ('palindrome at some q',t)
        for q in (qmin,qmin+1,qmin+3):
            d=build_word(a,q);r=build_word(reflected(a,k),q);target=build_word(b,q)
            assert len(d)==len(r)
            assert sum(x*B**i for i,x in enumerate(d))+sum(x*B**i for i,x in enumerate(r))==sum(x*B**i for i,x in enumerate(target))
    if gain is None:
        z=T[-1]['parts'];last=z[-1]['digits'][-1];first=z[0]['digits'][0]
        leading=int(str(last)[0]);trailing=first%10
        assert leading!=trailing, ('terminal nonpal witness absent',leading,trailing)
    print(f"POLYNOMIAL IDENTITY PASS base={B} blocks={k} edges={len(edges)} q>={qmin} "
          + (f"CYCLE gain={gain}; all nonpalindromic" if gain is not None else "OPEN PATH; nonpalindromic through terminal"))

if __name__=='__main__':
    with open(sys.argv[1]) as f:data=json.load(f)
    check(data)
