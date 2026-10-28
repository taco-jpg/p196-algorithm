#!/usr/bin/env python3
"""Exact nonbaseline two-sided transfer DAG delay bound for all p12/m9 temporal phases."""
from functools import lru_cache
from pathlib import Path
import sys
from k2_gate_extension import load, rows, steps
from k2_overflow_transfer import table,step

def decide(start,advance,isbase):
    color={};order=[];edges={};cycle=[]
    def dfs(u):
        if isbase(u):return
        if color.get(u)==1:
            cycle.append(u);return
        if color.get(u)==2:return
        color[u]=1
        nex=list(advance(u));edges[u]=nex
        for v in nex:
            if not isbase(v):dfs(v)
        color[u]=2;order.append(u)
    for s in start:dfs(s)
    if cycle:return None,len(edges),sum(len(v) for v in edges.values()),cycle
    longest={}
    for u in order:
        longest[u]=max([1 if isbase(v) else 1+longest[v] for v in edges[u]] or [0])
    maxdelay=max([1 if isbase(s) else 1+longest[s] for s in start] or [0])
    return maxdelay,len(edges),sum(len(v) for v in edges.values()),[]

def run(path):
    G,W,C,B=load(path)
    mx=0;one=[]
    for t in range(12):
        if G[t]==0:
            tab=rows(t,W,B)
            for r in range(9):
                _,_,a,b,_,_=tab[r]
                starts=[(rr,aa,bb) for rr,aa,bb,x in steps(tab,r,a,b,True)]
                def advance(u):
                    rr,aa,bb=u
                    return [(nr,na,nb) for nr,na,nb,x in steps(tab,rr,aa,bb)]
                def isbase(u):
                    rr,aa,bb=u
                    return (aa,bb)==(tab[rr][2],tab[rr][3])
                res=decide(starts,advance,isbase)
                one.append((t,r,*res));mx=max(mx,res[0] or 0)
        else:
            tab=table(t,W,B)
            for r in range(9):
                q,prev,s,a,b,*_=tab[r]
                starts=[state for state,x in step(tab,r,a,b,prev,True)]
                def advance(u):
                    rr,aa,bb,v=u
                    return [state for state,x in step(tab,rr,aa,bb,v)]
                def isbase(u):
                    rr,aa,bb,v=u
                    return (aa,bb,v)==(tab[rr][3],tab[rr][4],tab[rr][1])
                res=decide(starts,advance,isbase)
                one.append((t,r,*res));mx=max(mx,res[0] or 0)
    for t in range(12):
        rr=[x for x in one if x[0]==t]
        print('t',t,'gam',G[t],'delays',[x[2] for x in rr],'states',[x[3] for x in rr], 'edges',[x[4] for x in rr])
        assert all(not x[5] for x in rr)
    maxima=[max(x[2] for x in one if x[0]==t) for t in range(12)]
    assert maxima==[9,11,7,0]*3, maxima
    assert mx==11
    assert all(x[3]<=684 for x in one)
    print('GLOBAL MAX MATCHING EXCURSION',mx,'phase maxima',maxima,'state ceiling',684)

if __name__=='__main__':
    run(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).resolve().parents[1]/'data'/'lat_p12m9.txt'))
