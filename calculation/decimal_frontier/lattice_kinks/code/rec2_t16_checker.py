#!/usr/bin/env python3
"""Independent exact tuple-state / topological checker for rec2 T=16.
No shared state encodings, reachability, or cycle algorithms with the C++ code.
Run from repo root with calculation/decimal_frontier/lattice_kinks/data/lat2.txt.
"""
from pathlib import Path
from collections import deque
from itertools import product
import sys

def load(path):
    raw=list(map(int,Path(path).read_text().split()))
    p,nb,m,b=raw[:4];assert (p,nb,m,b)==(8,11,48,10)
    k=4;g=raw[k:k+p];k+=p
    W=[raw[k+t*m:k+(t+1)*m] for t in range(p)];k+=p*m
    C=[raw[k+t*m:k+(t+1)*m] for t in range(p)];k+=p*m
    B=[raw[k+t*nb:k+(t+1)*nb] for t in range(p)]
    assert k+p*nb==len(raw)
    def cell(t,x):return B[t%p][x] if x<nb else W[t%p][(x-nb)%m]
    def asc(t,x):
        for d in range(1,97):
            if cell(t,x-d)!=9:return int(cell(t,x-d)>=10)
        raise ValueError('ambiguous ascending carry')
    def desc(t,x):
        for d in range(1,97):
            if cell(t,x+d)!=9:return int(cell(t,x+d)>=10)
        raise ValueError('ambiguous descending carry')
    for t in range(p):
        for j in range(m):
            x=nb+2*m+j
            assert asc(t,x)==C[t][j]
            up=(cell(t,x)+asc(t,x))%10
            hi=(cell(t,x-1)+desc(t,x-1))%10 if g[t] else (cell(t,x)+desc(t,x))%10
            assert up+hi==cell(t+1,x)
    return nb,m,g+g,cell,asc,desc

def successors(s,g):
    a,G,prior=s
    output=set()
    for initial in range(19):
        def walk(t,v,aa,gg,dd,word):
            if t==16:
                if v==initial:output.add(((aa,gg,dd),word))
                return
            for din in (0,1):
                if int(v+din>=10)!=G[t]:continue
                u=(v+a[t])%10
                low=(v+din)%10
                v2=u+(prior[t] if g[t] else low)
                if v2>18:continue
                walk(t+1,v2,aa+(int(v+a[t]>=10),),gg+(din,),
                     dd+((low if g[t] else 0),),word+(v,))
        walk(0,initial,(),(),(),())
    return output

def boundaries(j,lat):
    nb,m,g,cell,asc,desc=lat;x=nb+2*m+j
    low=tuple(asc(t,x) for t in range(16))
    left=tuple(cell(t,x-1) for t in range(16))
    gs=[(0,1) if g[t] and left[t]!=9 else (desc(t,x-1),) for t in range(16)]
    return [(low,G,tuple((left[t]+G[t])%10 if g[t] else 0 for t in range(16)))
            for G in product(*gs)]

def control(lat):
    nb,m,g,cell,asc,desc=lat
    for j in range(m):
        x=nb+2*m+j
        a=tuple(asc(t,x) for t in range(16))
        G=tuple(desc(t,x-1) for t in range(16))
        dd=tuple((cell(t,x-1)+G[t])%10 if g[t] else 0 for t in range(16))
        expected=(tuple(asc(t,x+1) for t in range(16)),
                  tuple(desc(t,x) for t in range(16)),
                  tuple((cell(t,x)+desc(t,x))%10 if g[t] else 0 for t in range(16)))
        word=tuple(cell(t,x) for t in range(16))
        assert (expected,word) in successors((a,G,dd),g)
    print("CONTROL: all 48 exact lattice temporal words and spatial links accepted")

def decide(j,lat,cap=2000000):
    nb,m,g,cell,asc,desc=lat;x=nb+2*m+j
    init=boundaries(j,lat)
    roots={n for s in init for n,w in successors(s,g)
           if all(w[t]!=cell(t,x) for t in range(16))}
    nodes=set(roots);queue=deque(roots);adj={}
    while queue:
        n=queue.popleft()
        outs={q for q,w in successors(n,g)}
        adj[n]=outs
        for q in outs:
            if q not in nodes:
                nodes.add(q);queue.append(q)
        assert len(nodes)<=cap,"CAP"
    indegree={n:0 for n in nodes}
    for outs in adj.values():
        for v in outs:indegree[v]+=1
    peel=deque(n for n in nodes if indegree[n]==0)
    removed=0
    while peel:
        n=peel.popleft();removed+=1
        for q in adj[n]:
            indegree[q]-=1
            if indegree[q]==0:peel.append(q)
    return len(init),len(roots),len(nodes),sum(map(len,adj.values())),len(nodes)-removed

def main():
    if len(sys.argv)!=2:sys.exit("usage: rec2_t8_checker.py lat2.txt")
    lat=load(sys.argv[1]);control(lat)
    total_states=total_edges=0
    for j in range(48):
        ni,ns,nv,ne,cycles=decide(j,lat)
        print(f"j={j} initial={ni} first_defect={ns} visited={nv} edges={ne} cyclic={cycles}")
        assert cycles==0,(j,cycles)
        total_states+=nv;total_edges+=ne
    print("RESULT: all 48 exact T=16 stationary first-defect classes EXHAUSTED")
    print("TOTAL visited",total_states,"distinct directed edges",total_edges)
    assert (total_states,total_edges)==(1317912,1269072)

if __name__=="__main__":main()
