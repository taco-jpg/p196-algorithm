#!/usr/bin/env python3
"""Exhaustive check of the per-edge inequalities used in the two counter potential proofs (bases 2..130).
Counter graph: x in [1,2b-2], kappa in {0,1}.  non-overflow (x+k<=b-1): x'=2x+k ; overflow (x+k>=b): x'=(x mod b)+1.
(U) upper bound  p <= bitlen(b)*G :  psi(x)=-floor(log2 x): non-ov edge: psi' - psi = -1 exactly ; ov edge: psi'-psi <= bitlen(b)-1.
(L) lower bound  p >= 2G         :  pi(x)=floor(log2 x)  : non-ov edge: pi'-pi = +1 exactly ; ov edge: pi'-pi <= -1 EXCEPT the edge x=b-1 (k=1) -> b,
                                    which is always followed by the forced overflow b -> 1; the two together change pi by -floor(log2(b-1)) <= -2 iff b>=5."""
import sys
fl=lambda x:x.bit_length()-1
bad=[]
for b in range(2,131):
    L=b.bit_length()
    maxdrop=0; exc=set()
    for x in range(1,2*b-1):
        for k in (0,1):
            if x+k<=b-1:
                nx=2*x+k
                if nx>2*b-2: continue
                assert fl(nx)-fl(x)==1
            else:
                nx=(x%b)+1
                assert 1<=nx<=b
                drop=fl(x)-fl(nx)   # = psi' - psi  (psi=-fl)
                maxdrop=max(maxdrop,drop)
                if fl(nx)-fl(x)>-1:  exc.add((x,k,nx))
    if maxdrop!=L-1: bad.append(('U',b,maxdrop,L-1))
    if exc!={(b-1,1,b)} and not (b==2 and exc<= {(1,1,2)}): bad.append(('Lexc',b,sorted(exc)))
    if b>=5 and fl(b-1)<2: bad.append(('Lpair',b))
    # the successor of x=b is forced overflow: b+k>=b for k in 0,1
print("violations:",bad if bad else "none for b=2..130")
