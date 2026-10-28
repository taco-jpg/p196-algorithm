#!/usr/bin/env python3
"""Search for integer potentials psi(a) on post-overflow counter values a in [1,b] s.t.
   r + psi(a') - psi(a) <= m for all feasible (a, r, a'), m = floor(log2 b)."""
import math, itertools
def transitions(b):
    T=set()
    for a in range(1,b+1):
        # run of r non-overflow steps then overflow
        # x_0=a ; each non-ov step requires x+c<=b-1
        def rec(x,r):
            # overflow now?  need x+c>=b for some c in {0,1}
            for c in (0,1):
                if x+c>=b:
                    ap = (x%b)+1
                    T.add((a,r,ap))
                else:
                    if x<=2*b-2:
                        rec(2*x+c,r+1)
        rec(a,0)
    return T
for b in (3,5,6,7,9,10,11,12,13,17,20,26):
    m=b.bit_length()-1
    T=transitions(b)
    cands={'floor_log2':lambda a:int(math.floor(math.log2(a))),
           'ceil_log2':lambda a:int(math.ceil(math.log2(a))),
           'neg_floor':lambda a:-int(math.floor(math.log2(a))),
           'neg_ceil':lambda a:-int(math.ceil(math.log2(a))),
           'floor_log2_b_over_a':lambda a:int(math.floor(math.log2(b/a))),
           }
    res={}
    for name,psi in cands.items():
        bad=[(a,r,ap) for (a,r,ap) in T if r+psi(ap)-psi(a)>m]
        res[name]=len(bad)
    maxr=max(r for a,r,ap in T)
    print(b,"m=",m,"max run",maxr,res)
