#!/usr/bin/env python3
"""Exact finite all-overflow transition graph of period-5 palindrome-compatible pairword fibre."""
from collections import deque, Counter
from itertools import product
import json, sys

def cyclic_carry(r,reverse):
    solutions=[]
    for c0 in (0,1):
        c=c0; track=[0]*5
        for j in range(5):
            i=(-j if reverse else j)%5
            track[i]=c;c=(r[i]+c)//10
        if c==c0:solutions.append(tuple(track))
    return solutions

def f(r,g):
    lo=cyclic_carry(r,False)
    hi=cyclic_carry(r,True)
    if len(lo)!=1 or len(hi)!=1:return None
    c1,c2=lo[0],hi[0]
    return tuple((r[i]+c1[i])%10+(r[(i-g)%5]+c2[(i-g)%5])%10 for i in range(5))

def reflect(r,delta):return all(r[i]==r[(delta-i)%5] for i in range(5))

def compute(start=(17,3,14,3,17),delta=4):
    assert reflect(start,delta)
    s=(tuple(start),delta)
    seen={s:0};Q=deque([s]);edges={};depths={s:0}; bad=[]; even=[]
    while Q:
        st=Q.popleft();r,d=st
        if not any(v%2 for v in r): even.append(st)
        successors=[]
        for g in (0,1):
            y=f(r,g)
            if y is None:bad.append((st,g));continue
            new=(y,(d+g)%5)
            if not reflect(y,new[1]):raise Exception(('reflection fails',st,g,new))
            successors.append(new)
            if new not in seen:
                seen[new]=len(seen);depths[new]=depths[st]+1;Q.append(new)
        edges[st]=successors
    print('START',s,'reachable',len(seen),'max_depth',max(depths.values()),'ambiguousEdges',len(bad),'evenCentreStates',len(even));print('FIRST even',[(x,depths[x]) for x in even[:5]],'FIRST ambiguous',[(x[0],x[1],depths[x[0]]) for x in bad[:5]])
    outdeg=Counter(len(v) for v in edges.values());print('outdeg',outdeg)
    # reverse reachability / Tarjan SCC
    sys.setrecursionlimit(200000)
    ix=0;indices={};low={};on=set();stack=[];scc=[]
    def visit(u):
        nonlocal ix
        indices[u]=low[u]=ix;ix+=1;stack.append(u);on.add(u)
        for v in edges[u]:
            if v not in indices:visit(v);low[u]=min(low[u],low[v])
            elif v in on:low[u]=min(low[u],indices[v])
        if indices[u]==low[u]:
            comp=[]
            while True:
                w=stack.pop();on.remove(w);comp.append(w)
                if w==u:break
            scc.append(comp)
    for u in edges:
        if u not in indices:visit(u)
    loops=[]; safe=[]
    for group in scc:
        if len(group)>1 or any(x in edges[x] for x in group):
            loops.append(group)
            if all(any(v%2 for v in x[0]) for x in group):safe.append(group)
    print('SCC',len(scc),'recurrent',len(loops),'sizes',Counter(map(len,loops)).most_common(10),'odd_only recurrent',len(safe))
    print('largest samples',[(len(c),c[0]) for c in sorted(loops,key=len,reverse=True)[:8]])
    return len(seen)

if __name__=='__main__':compute()
