#!/usr/bin/env python3
"""Find concrete centre-only cycles (fixed points of the lap map, e determined by the centre itself) for given gam streams in base b.
Gives synthetic positive controls (e,g) for the regular-language engine: the engine must NOT say 'no centre' for them.
usage: cenfind.py b pmax Wmax"""
import sys, itertools
b=int(sys.argv[1]); PM=int(sys.argv[2]); W=int(sys.argv[3])
def step(C,g):
    m=len(C)
    for e in (0,1):
        car=e; dc=[]
        for x in C:
            v=x+car; dc.append(v%b); car=v//b
        if car==1-e: break
    else: return None
    if g==0: d2=[dc[i]+dc[m-1-i] for i in range(m)]
    else:
        y=(b-1)*e; dt=dc+[y]; d2=[dt[i]+dt[m-i] for i in range(m+1)]
    lo,hi=0,len(d2)-1
    while hi-lo+1>=2 and d2[lo]==b-1 and d2[hi]==b-1: lo+=1; hi-=1
    if hi-lo+1<=0: return None
    return tuple(d2[lo:hi+1]),e
def pals(L):
    h=(L+1)//2
    for half in itertools.product(range(2*b-1),repeat=h):
        if L%2==1 and half[-1]%2: continue
        if L>=2 and half[0]==b-1: continue
        yield tuple(half)+tuple(half[:L//2][::-1])
def necklaces(p):
    seen=set()
    for mask in range(1<<p):
        s=tuple((mask>>t)&1 for t in range(p))
        rots=[s[i:]+s[:i] for i in range(p)]
        if min(rots)!=s: continue
        yield s
found=0
for p in range(2,PM+1):
    for gs in necklaces(p):
        G=sum(gs)
        if G%2 or G==0: continue
        for L in range(1,W+1):
            for C in pals(L):
                cur=C; es=[]; ok=True
                for t in range(p):
                    r=step(cur,gs[t])
                    if r is None: ok=False; break
                    cur,e=r; es.append(e)
                if ok and cur==C:
                    print(f"CENTRE b={b} p={p} g={''.join(map(str,gs))} e={''.join(map(str,es))} C={C}",flush=True); found+=1
print("found",found)
