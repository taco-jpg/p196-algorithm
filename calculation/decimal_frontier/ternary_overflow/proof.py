#!/usr/bin/env python3
"""Agent-13 exact 100-case finite lemma for 3-letter substitution, Python3/std-lib.

The paper proof in reports/Agent13TernaryOverflowObstruction.md explains
why checking these cases decides the ALL-base, ALL-nonneutral-coding
one-step, overflow-one obstruction for arbitrarily long ternary factors.
"""
from functools import lru_cache
from itertools import product

MU={'0':'01','1':'02','2':'00'}
DIGRAMS=frozenset(('00','01','02','10','20'))

@lru_cache(None)
def language(n):
    assert n>=1
    if n==1: return frozenset('012')
    if n==2: return DIGRAMS
    k=(n+2)//2
    assert k<n
    words=set()
    for x in language(k):
        y=''.join(MU[c] for c in x)
        for offset in (0,1):
            if offset+n<=len(y):
                words.add(y[offset:offset+n])
    return frozenset(words)

def equality_pattern(word):
    assigned={}
    return tuple(assigned.setdefault(a,len(assigned)) for a in word)

def restricted_growth_partitions(k):
    """Every possible equality pattern among k freely chosen symbol values."""
    def recur(seq):
        if len(seq)==k:
            yield tuple(seq);return
        for x in range(max(seq)+2):
            yield from recur(seq+[x])
    return list(recur([0])) if k>0 else [()]

def overflow_one_type_word(word):
    """At reflected centre interior, each output is sum of neighboring
    canonical values f(a_i)+f(a_(i-1)). The only possible pair types
    are 00->0, 01/10->1, 02/20->2, because the source has no 11/12/22.
    """
    assert len(word)>=2
    result=[]
    for a,b in zip(word,word[1:]):
        assert min(a,b)=='0', (a,b)
        result.append(int(max(a,b)))
    return tuple(result)

def certify():
    assert language(2)==DIGRAMS
    A=sorted(language(8))
    B=sorted(language(6))
    assert len(A)==20 and len(B)==16
    output_patterns={equality_pattern(w) for w in B}
    partitions=restricted_growth_partitions(3)
    assert len(partitions)==5
    tested=0;rejected=0;found=[]
    for x in A:
        types=overflow_one_type_word(x)
        assert len(types)==7
        # Source eight digits produce a six-interior output at positions
        # i=1,...,6, using predecessor i-1, so discard last (unused) edge.
        types=types[:6]
        for part in partitions:
            pattern=equality_pattern(tuple(part[t] for t in types))
            tested+=1
            if pattern in output_patterns:
                found.append((x,part,pattern))
            else:
                rejected+=1
    assert tested==100 and rejected==100 and found==[]
    return len(A),len(B),len(output_patterns),len(partitions),tested

if __name__=='__main__':
    a,b,p,k,n=certify()
    print('FINITE-LEMMA PASS: |L8|=%d |L6|=%d target_patterns=%d partitions=%d checked=%d incompatible=%d' %(a,b,p,k,n,n))
    print('SCOPE: all bases >=2, all coefficient maps avoiding b-1, overflowing step only; not a base-10 Lychrel proof')
