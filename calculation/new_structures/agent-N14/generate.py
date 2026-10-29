#!/usr/bin/env python3
"""Recreate the rooted decimal p=72, K=5 carry-driven strip by seed 14.
The arbitrary incoming top carry is a *control input*, not a real centre.
"""
import random
K=5
r=random.Random(14)
found={}
def step(x,ctop):
    c=[0]*K;c[-1]=ctop
    for j in range(K-1,0,-1): c[j-1]=(x[j]+c[j])//10
    gam=(x[0]+c[0])//10
    low=[0]*K
    for j in range(1,K):low[j]=(x[j-1]+low[j-1])//10
    nxt=[]
    for j in range(K):
        hi=(1 if j==0 else (x[j-1]+c[j-1])%10) if gam else (x[j]+c[j])%10
        nxt.append((x[j]+low[j])%10+hi)
    return tuple(nxt),gam
for run in range(5000):
    x=tuple([r.randrange(1,19)]+[r.randrange(19) for _ in range(K-1)])
    visited={};trace=[]
    for t in range(300):
        if x in visited:
            segment=trace[visited[x]:]
            g=''.join(str(s[1]) for s in segment);p=len(g)
            if 28<=p<=80 and all(g!=g[:d]*(p//d) for d in range(1,p) if p%d==0):
                found[(p,g)]=segment
            break
        visited[x]=t
        u=r.randrange(2);nxt,g=step(x,u)
        trace.append((x,g,u));x=nxt
        if x[0]==0:break
for (p,g),trace in found.items():
    if p==72:
        print("gamma="+g)
        print("top="+''.join(str(v[2]) for v in trace))
        print("rows="+ ';'.join(','.join(map(str,v[0])) for v in trace))
        break
else:raise RuntimeError("No 72-clock strip found")
