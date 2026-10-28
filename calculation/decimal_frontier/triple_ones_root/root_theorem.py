#!/usr/bin/env python3
"""Exact all-r all-k decimal root theorem for g=(111 0^r)^k.
Run: python3 root_theorem.py --rmax 60 --kmax 12
Uses only Python standard library. This checker is finite control evidence;
the all-parameter proof is in reports/Agent12TripleOnesRoot.md.
"""
import argparse
from collections import defaultdict

def block_transitions(r):
    g=(1,1,1)+(0,)*r
    results=[]
    for x0 in range(1,19):
        def dfs(t,x,carry):
            if t==len(g):
                results.append((x0,x,tuple(carry)))
                return
            for c in (0,1):
                if (x+c)//10 != g[t]:
                    continue
                nx=x%10 + (1 if g[t] else (x+c)%10)
                assert 0<=nx<=18
                dfs(t+1,nx,carry+[c])
        dfs(0,x0,[])
    return results

def paths_by_matrix(r,k):
    edges=block_transitions(r)
    q={z:1 for z in range(1,19)}
    for _ in range(k):
        nq=defaultdict(int)
        for start,end,carries in edges:
            if q[start]:
                nq[end]+=q[start]
        q=nq
    # This is only a total path count, NOT a closed path count; enumerate
    # exact loop returns separately below.
    ans=0
    for z in range(1,19):
        q={z:1}
        for _ in range(k):
            nq=defaultdict(int)
            for start,end,carries in edges:
                if start in q:
                    nq[end]+=q[start]
            q=nq
        ans+=q.get(z,0)
    return ans

def controls(rmax,kmax):
    assert rmax>=6 and kmax>=1
    for r in range(1,rmax+1):
        paths=block_transitions(r)
        expected={1:8,2:16,3:32,4:12}.get(r,0)
        assert len(paths)==expected,(r,len(paths),expected)
        assert {x for x,y,_ in paths} <= {18}
        if r==4:
            self_loops=[p for p in paths if p[0]==p[1]]
            assert len(self_loops)==4
            assert {c for _,_,c in self_loops}=={
                (a,1,b,0,0,1,0) for a in range(2) for b in range(2)}
        for k in range(1,kmax+1):
            actual=paths_by_matrix(r,k)
            predicted=4**k if r==4 else 0
            assert actual==predicted,(r,k,actual,predicted)
        if r<=6:
            print('r',r,'block_paths',len(paths),'closed_counts_k1_to_4',
                  [paths_by_matrix(r,k) for k in range(1,5)])
    print('PASS',rmax*kmax,'root-period checks; no cap')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--rmax',type=int,default=60)
    p.add_argument('--kmax',type=int,default=12)
    a=p.parse_args();controls(a.rmax,a.kmax)
