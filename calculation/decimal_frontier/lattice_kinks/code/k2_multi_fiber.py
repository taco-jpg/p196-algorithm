#!/usr/bin/env python3
"""All-k exponential one-step pairword fibre using disjoint p12/m9 t=1 collision motifs."""
import sys
from pathlib import Path
from k2_gate_extension import load, word, ordinary, bigint_pairs
PATTERN=(9,5,0,15,3,12,14)
ORIGINAL=(4,5,10,14,13,12,9)

def construct(k,mask,odd=False,src=None):
    assert k>=1 and 0<=mask<1<<k
    gam,W,cup,B=load(src)
    n=200+18*k+int(odd)
    P=word(1,n,W,B)
    Q=P[:]
    for a in range(k):
        j=59+9*a
        assert tuple(P[j:j+7])==ORIGINAL
        assert j+7+12<n//2
        if (mask>>a)&1:
            for u,x in enumerate(PATTERN):Q[j+u]=Q[n-1-j-u]=x
    return P,Q

def check(k,src,odd=False):
    P,_=construct(k,0,odd,src)
    target=ordinary(P)
    seen=set()
    for mask in range(1<<k):
        _,Q=construct(k,mask,odd,src)
        # All Q differ on a disjoint set, so this set must be 2^k.
        key=tuple(Q)
        assert key not in seen,('nonunique',k,mask)
        seen.add(key)
        assert ordinary(Q)==target,('pair mismatch',k,mask)
        if k<=7 and (mask<8 or mask==(1<<k)-1):
            assert bigint_pairs(Q)==bigint_pairs(P)==target
    assert len(seen)==1<<k
    print('K',k,'parity',int(odd),'N',len(P),'distinct',len(seen),'same successor pairword PASS',flush=True)

def main():
    src=sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).resolve().parents[1]/'data'/'lat_p12m9.txt')
    G,W,C,B=load(src)
    for k in range(1,11):
        check(k,src,odd=False)
        check(k,src,odd=True)
    check(12,src,odd=False)
    print('ALL-K PROOF: each 7-site motif is a baseline-to-baseline two-sided carry path; 2 unchanged periodic sites separate motifs; concatenating k accepting local paths keeps output pairword unchanged. Count verified for k<=12.')
if __name__=='__main__':main()
