#!/usr/bin/env python3
"""Agent-13 F1 neutral-letter exact all-boundary carry test.

The fixed word is 0->01,1->02,2->00. A coefficient table contains exactly
one neutral decimal value 9, and the two other coefficients are distinct.
All length-16 source factors and both arbitrary entering carries on EACH
side are checked for an overflow-one interior 6-cell output. Requires no
external solver, arbitrary memory or sampled source prefix.
"""
from itertools import permutations
from functools import lru_cache
MU={'0':'01','1':'02','2':'00'}

@lru_cache(None)
def factor_language(n):
    if n==1:return frozenset('012')
    if n==2:return frozenset(['00','01','02','10','20'])
    k=(n+2)//2
    assert k<n
    return frozenset(s[j:j+n] for w in factor_language(k)
        for s in [''.join(MU[c] for c in w)] for j in (0,1) if j+n<=len(s))

def equality(w):
    symbols={};result=[]
    for t in w:
        if t not in symbols:symbols[t]=len(symbols)
        result.append(symbols[t])
    return tuple(result)

def carry_digits(word,c):
    ds=[]
    for v in word:
        v+=c;ds.append(v%10);c=v//10
    return ds

def inspect():
    assert len(factor_language(4))==10
    assert all(c*4 not in factor_language(4) for c in '012')
    src=sorted(factor_language(16));dst={equality(t) for t in factor_language(6)}
    assert len(src)==40 and len(factor_language(6))==16
    pairs=0;entry_cases=0;survivors=[]
    for coeff in permutations(range(19),3):
        if 9 not in coeff:continue
        for s in src:
            a=[coeff[ord(x)-48] for x in s]
            opts=[]
            for left in (0,1):
                lower=carry_digits(a,left)
                for right in (0,1):
                    upper=carry_digits(a[::-1],right)
                    # gamma=1: pair lower i with mirrored coefficient i-1.
                    out=tuple(lower[i]+upper[len(a)-i] for i in range(5,11))
                    opts.append(out)
                    entry_cases+=1
            assert opts[0]==opts[1]==opts[2]==opts[3], (coeff,s,opts)
            pairs+=1
            if equality(opts[0]) in dst:
                survivors.append((coeff,s,opts[0]))
    assert pairs==918*40 and entry_cases==4*pairs
    assert len(survivors)==0,survivors[:4]
    return pairs,entry_cases

if __name__=='__main__':
    pairs,entries=inspect()
    print(f'NEUTRAL ALL-BOUNDARY PASS: 918 tables x 40 exact L16 factors = {pairs} sources; {entries} boundary-carry cases, zero compatible L6 destinations')
    print('SCOPE: decimal overflow=1, one-step ternary substitution only; NOT a full decimal Lychrel proof')
