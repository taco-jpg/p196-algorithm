#!/usr/bin/env python3
"""Independent divmod-based full position recurrence; no symbolic proof case splits."""
import sys,json
from pathlib import Path
w=json.loads(Path(sys.argv[1]).read_text());G=w['g']
assert len(G)==21

def replay(n):
    base=w['base']+w['step']*n
    A=[w['first'][j]+n*w['firstSlope'][j] for j in range(22)]
    C=[w['second'][j]+n*w['secondSlope'][j] for j in range(22)]
    assert A[0]==A[21] and C[0]==C[21]
    for t,letter in enumerate(G):
        gamma=int(letter);x,y=A[t],C[t]
        ca=w['c0'][t];cb=w['c1'][t]
        assert 1<=x<=2*base-2 and 0<=y<=2*base-2
        assert (x+ca)//base==gamma
        xnext=(x+0)%base+(1 if gamma else (x+ca)%base)
        low=(x+0)//base;high=ca;partner=(x+ca)%base
        assert (y+cb)//base==high
        ynext=(y+low)%base+(partner if gamma else (y+cb)%base)
        assert A[t+1]==xnext and C[t+1]==ynext,(n,t)
    return base,A[0],C[0]
for n in (0,1,2,3,10,100,1000,1000000):
    print('INDEPENDENT REPLAY PASS',replay(n))
print('Independent checker uses actual integer quotients and remainders on every edge')
