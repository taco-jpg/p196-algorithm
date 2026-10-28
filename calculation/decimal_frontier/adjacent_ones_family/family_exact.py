#!/usr/bin/env python3
"""Base-10 all-r all-k canonical-root no-go for overflow (11 0^r)^k.

All r except r=3 have ZERO closed first coefficient. The exceptional
r=3 is excluded at SIX spatial columns by the separately committed
Agent12SixthColumnNoGoAllK exact finite transfer (reproduce its checker).
This program independently checks every finite root-block case and
completes exact temporal-word DP controls for any chosen finite r,k grid.
"""
import argparse
from collections import Counter


def block_edges(r):
    """All canonical first-column edges for one (11 0^r) time block."""
    assert r>=1
    g=(1,1)+(0,)*r
    E=[]
    for z in range(1,19):
        def dfs(t,x,hs,xs):
            if t==len(g):E.append((z,x,tuple(xs),tuple(hs)));return
            for c in (0,1):
                if (x+c)//10!=g[t]:continue
                y=x%10+(1 if g[t] else (x+c)%10)
                assert 0<=y<=18
                dfs(t+1,y,hs+[c],xs+[x])
        dfs(0,z,[],[])
    return E


def root_closed_count(r,k):
    """Independent original-time DP; no (r+2)-block graph is reused."""
    g=(1,1)+(0,)*r
    temporal=g*k
    n=0
    for start in range(1,19):
        dp={start:1}
        for bit in temporal:
            nxt={}
            for x,qty in dp.items():
                for carry in (0,1):
                    if (x+carry)//10!=bit:continue
                    y=x%10+(1 if bit else (x+carry)%10)
                    assert 0<=y<=18
                    nxt[y]=nxt.get(y,0)+qty
            dp=nxt
        n+=dp.get(start,0)
    return n


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--rmax',type=int,default=50)
    p.add_argument('--kmax',type=int,default=12)
    a=p.parse_args()
    assert a.rmax>=5 and a.kmax>=1
    edge_counts={1:4,2:8,3:16,4:6}
    endpoints={1:set((2,3)),2:set(range(4,8)),
               3:set(range(8,16)),4:set(range(16,19))}
    for r in range(1,a.rmax+1):
        E=block_edges(r)
        assert len(E)==edge_counts.get(r,0),(r,len(E))
        assert {z for z,w,x,c in E}<={9}
        assert {w for z,w,x,c in E}==endpoints.get(r,set()),r
        if r==3:
            assert Counter((z,w) for z,w,x,c in E)=={
                (9,w):2 for w in range(8,16)}
        for k in range(1,a.kmax+1):
            count=root_closed_count(r,k)
            expected=2**k if r==3 else 0
            assert count==expected,(r,k,count,expected)
        if r<=6:
            print('r',r,'one-block edges',len(E),'ends',sorted(endpoints.get(r,set())),
                  'root closed histories k1..%d'%a.kmax,
                  [root_closed_count(r,k) for k in range(1,min(a.kmax,5)+1)])
    print('PASS root classification every r<=%d, k<=%d; r=3 exception has 2^k closed roots.'%(a.rmax,a.kmax))
    print('For r=3, run sixcol_allk/sixcol_transfer.py to certify no SIX-column path for ALL k.')

if __name__=='__main__':main()
