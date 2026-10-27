#!/usr/bin/env python3
"""Agent 6: fourth-exterior-coordinate obstruction for the projected
42-step R3,D7 walk of PR #361. NOT a full decimal no-go.
Python stdlib only: python3 calculation/agent-6/prefix4_witness_obstruction.py
"""
from collections import deque
from random import Random

FIRST21 = [
 (14,3,7),(5,8,10),(10,17,1),(1,9,9),(3,9,9),(7,9,9),
 (15,9,9),(6,5,9),(12,11,9),(3,5,1),(6,10,2),(13,0,6),
 (4,4,6),(8,8,12),(16,17,5),(7,15,13),(15,11,7),
 (6,8,9),(12,16,18),(3,10,16),(7,1,13)]
B = FIRST21 + FIRST21
G = '101000101001001010100101000101001001010100'
P=len(G)
assert P==42 and len(B)==P

def projected_step(a):
    """All projected successors: unresolved inward carry in {0,1}."""
    n=len(a);ret=set()
    for high in (0,1):
        h=[0]*(n+1);h[n]=high
        for k in range(n-1,-1,-1):h[k]=(a[k]+h[k+1])//10
        g=h[0];low=0;digit=[]
        for x in a:
            digit.append((x+low)%10);low=(x+low)//10
        r=[(a[k]+h[k+1])%10 for k in range(n)]
        out=tuple(digit[k]+(1 if g and k==0 else r[k-1] if g else r[k]) for k in range(n))
        ret.add((g,out))
    return ret

def graph():
    n=19;total=P*n;arc=[[] for _ in range(total)];indeg=[0]*total
    for t in range(P):
        for x in range(n):
            u=t*n+x
            for g,d in projected_step(B[t]+(x,)):
                if g==int(G[t]) and d[:3]==B[(t+1)%P]:
                    v=((t+1)%P)*n+d[3]
                    if v not in arc[u]:arc[u].append(v);indeg[v]+=1
    count=sum(map(len,arc));q=deque(i for i in range(total) if indeg[i]==0)
    dist=[0]*total;removed=0
    while q:
        u=q.popleft();removed+=1
        for v in arc[u]:
            dist[v]=max(dist[v],dist[u]+1)
            indeg[v]-=1
            if not indeg[v]:q.append(v)
    assert removed==total
    print('R4_WITNESS_LIFT_ACYCLIC states=',total,' arcs=',count,
          ' removed=',removed,' residual=',total-removed,
          ' max_path_edges=',max(dist),sep='')

def norm(w,e):
    ds=[]
    for x in w:
        ds.append((x+e)%10);e=(x+e)//10
    return tuple(ds),e

def directB(b):
    db,e=norm(b,0)
    dr,g=norm(b[::-1],1-e)
    if g:raw=tuple(a+c for a,c in zip(db+(9*(1-e),),(1,)+dr[::-1]))
    else:raw=tuple(a+c for a,c in zip(db,dr[::-1]))
    return raw,g

def random_audit(n=50000):
    r=Random(61027)
    for _ in range(n):
        width=r.randrange(0,30)
        b=[r.randrange(19) for _ in range(width)]
        if b and not b[0]:b[0]=1+r.randrange(18)
        raw,g=directB(tuple(b))
        a=tuple((b+[9]*4)[:4]);target=tuple((raw+(9,9,9,9))[:4])
        assert (g,target) in projected_step(a),(b,g,a,target)
        while raw and raw[-1]==9:
            raw=raw[:-1]
            assert (g,tuple((raw+(9,9,9,9))[:4])) in projected_step(a)
    print('R4_ARITHMETIC_RANDOM_CHECKS=',n,' PASS',sep='')

if __name__=='__main__':
    random_audit();graph()
