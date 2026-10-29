#!/usr/bin/env python3
"""Distinct q=14/k=100 calibration controls, not exhaustive 19**5 seam census."""
import json,sys
from collections import Counter
from phase10_cone import load,enclosure,audit
clock,Bs,Ws=load(sys.argv[1]);B=Bs[10];W=Ws[10]
states,_=enclosure(B,W,clock)
start,end=map(int,sys.argv[2:4]);assert 0<=start<=end<=19
U=[]
for a in range(0,19,2):
    w=[9,a,18-a]
    for r in range(3):U.append(w[r:]+w[:r])
assert len({tuple(x) for x in U})==30
hist=Counter()
for j in range(start,end):
    for u in U:
        for C in ([4,14,4],[4,4]):
            z=audit(B,W,states,[j,0,0,0,0],u,C,14,100)
            assert z['overflow_count']==30
            hist[z['first_mismatch']]+=1
print('RESULT_JSON',json.dumps({'start':start,'end':end,
    'count':sum(hist.values()),'return_count':hist[None],
    'histogram':sorted(hist.items(),key=lambda x:(x[0] is None,x[0] or 0))}))
