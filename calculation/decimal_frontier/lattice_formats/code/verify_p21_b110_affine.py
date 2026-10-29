#!/usr/bin/env python3
"""For-all-n affine certificate for first TWO time-periodic exterior columns.
Fixed 21-step g and bases b=110+2395575*n, n>=0. NOT an integer Lychrel orbit.
"""
import json,sys
from pathlib import Path
w=json.loads(Path(sys.argv[1]).read_text())
G=w['g'];q=w['first'];r=w['second'];c0=w['c0'];c1=w['c1'];a=w['lowQuotient'];U=w['firstSlope'];V=w['secondSlope']
b=w['base'];B=w['step'];P=len(G)
assert (b,B,G,P)==(110,2395575,'001001010101001010101',21)
assert all(len(z)==P+1 for z in (q,r,U,V))
assert all(len(z)==P for z in (c0,c1,a))
assert (q[0],q[-1],r[0],r[-1])==(40,40,71,71)
assert (U[0],U[-1],V[0],V[-1])==(888615,888615,1555317,1555317)
for t,letter in enumerate(G):
    bit=int(letter);lc=bit
    assert all(x in (0,1) for x in (c0[t],c1[t],a[t]))
    assert 1<=q[t]<=2*b-2 and 0<=r[t]<=2*b-2
    assert 0<=U[t]<=2*B and 0<=V[t]<=2*B
    # Floor-quotient inequalities at n=0 and slope bounds establish all n>=0.
    assert (q[t]+c0[t])//b==bit
    assert bit*B<=U[t]<=(bit+1)*B
    assert (r[t]+lc)//b==a[t]
    assert a[t]*B<=V[t]<=(a[t]+1)*B
    assert (r[t]+c1[t])//b==c0[t]
    assert c0[t]*B<=V[t]<=(c0[t]+1)*B
    if not bit:
        assert q[t+1]==2*q[t]+c0[t]
        assert U[t+1]==2*U[t]
        assert r[t+1]==2*r[t]+c1[t]-b*(a[t]+c0[t])
        assert V[t+1]==2*V[t]-B*(a[t]+c0[t])
    else:
        assert q[t+1]==q[t]-b+1
        assert U[t+1]==U[t]-B
        assert r[t+1]==r[t]+1+q[t]+c0[t]-b*(a[t]+1)
        assert V[t+1]==V[t]+U[t]-B*(a[t]+1)
assert (q[-1],r[-1],U[-1],V[-1])==(q[0],r[0],U[0],V[0])
print('PAPER PROOF PASS: 21 exact affine transitions, all quotient/slope inequalities')
print('Every n>=0: b=110+2395575*n has a rooted closed first TWO-column trajectory')
print('Only a temporal head; no exterior SCC or Lychrel certificate is claimed')
