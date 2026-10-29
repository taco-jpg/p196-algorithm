#!/usr/bin/env python3
"""Independent ordinary-integer validation, no use of transfer.py."""
from pathlib import Path

p=Path(__file__).with_name('decimal_p72_w5.txt')
r=dict(line.strip().split('=',1) for line in p.read_text().splitlines())
g=r['gamma'];top=[int(c) for c in r['top']]
rows=[list(map(int,s.split(','))) for s in r['rows'].split(';')]
assert len(g)==len(top)==len(rows)==72
assert all(not(g==g[:d]*(72//d)) for d in range(1,72) if 72%d==0)
def val(a):return sum(v*10**i for i,v in enumerate(a))
def dig(n):
    d=[]
    while n:n,z=divmod(n,10);d.append(z)
    return d or [0]
def local(rows,top):
    faults=[]
    for t in range(72):
        cap=18 if top[t] else 0
        W=rows[t]+[cap]+rows[t][::-1]
        D=dig(val(W))
        pair=[D[i]+D[-1-i] for i in range(len(D))]
        if len(D)!=len(W)+int(g[t]) or pair[:5]!=rows[(t+1)%72]:
            faults.append(t)
    return faults
assert local(rows,top)==[]
bad=top[:];bad[0]=1-bad[0]
assert 0 in local(rows,bad), 'corrupted carry must be detected'
# Construct an actual N0, whose pairword at time 0 contains the chosen cap.
core=[11,18,10,18,11]
P=rows[0]+core+rows[0][::-1]
d=[0]*len(P)
for i in range(len(P)//2):
    hi=1 if i==0 else max(0,P[i]-9)
    d[i]=P[i]-hi;d[-1-i]=hi
d[len(P)//2]=P[len(P)//2]//2
seed=val(d)
assert seed==110102959969697
N=seed
for t in range(11):
    D=dig(N)
    pair=[D[i]+D[-1-i] for i in range(len(D))]
    if t<10:assert pair[:5]==rows[t],(t,pair[:5],rows[t])
    else:assert pair[:5]!=rows[t]
    N=N+val(D[::-1])
print('PASS: 72/72 big-integer localized transitions; corrupted carry rejected')
print('PASS: genuine seed 110102959969697 matches 5-column strip t=0..9, fails t=10')
