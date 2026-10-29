#!/usr/bin/env python3
"""Exact decimal one-column carry transfer: clock lifts and live horizon."""
from collections import deque
from pathlib import Path

def load(path=None):
    path=Path(path) if path else Path(__file__).with_name('decimal_p72_w5.txt')
    parts=dict(line.strip().split('=',1) for line in path.read_text().splitlines())
    g=parts['gamma'];top=tuple(map(int,parts['top']))
    rows=[tuple(map(int,r.split(','))) for r in parts['rows'].split(';')]
    assert len(g)==len(top)==len(rows)==72
    assert all(len(row)==5 and row[0]>0 for row in rows)
    return g,top,rows

def relation(g,L,H,Y):
    """Exact p-step reachability graph over the 19 possible x at one column."""
    p=len(g);out={}
    for z0 in range(19):
        seen={z0}
        for t in range(p):
            nxt=set()
            for z in seen:
                for u in (0,1):
                    if (z+u)//10!=H[t]:continue
                    zp=(z+L[t])%10+(Y[t] if g[t]=='1' else (z+u)%10)
                    nxt.add(zp)
            seen=nxt
            if not seen:break
        if seen:out[z0]=seen
    return out

def shortest_lift(g,L,H,Y):
    """Shortest directed R-cycle; its length multiplies the time period."""
    R=relation(g,L,H,Y);best=None
    for start in R:
        q=deque([(start,(start,))]);visited={start}
        while q:
            z,path=q.popleft()
            for zn in R.get(z,()):
                if zn==start:
                    if best is None or len(path)<len(best):best=path
                    q.clear();break
                if zn not in visited:
                    visited.add(zn);q.append((zn,path+(zn,)))
    return best

def cut(g,top,rows):
    p=len(g);L=[];Y=[]
    for t in range(p):
        v=0
        for x in rows[t]:v=(x+v)//10
        L.append(v)
        Y.append((rows[t][-1]+top[t])%10 if g[t]=='1' else -1)
    return tuple(L),top,tuple(Y)

def horizon(g,L,H,Y,limit=10000):
    """Longest live prefix; returning None indicates a repeated nonempty set."""
    S=set(range(19));seen=set()
    for t in range(limit):
        key=(t%len(g),frozenset(S))
        if key in seen:return None
        seen.add(key)
        j=t%len(g);N=set()
        for z in S:
            for u in (0,1):
                if (z+u)//10 == H[j]:
                    N.add((z+L[j])%10+(Y[j] if g[j]=='1' else (z+u)%10))
        if not N:return t+1
        S=N
    raise RuntimeError("limit reached without a decision")

if __name__=='__main__':
    assert shortest_lift('01',(1,0),(1,1),(-1,8)) is not None
    lift=shortest_lift('01',(1,0),(1,1),(-1,8))
    assert len(lift)==2,lift
    g,H,rows=load();L,H,Y=cut(g,H,rows)
    assert shortest_lift(g,L,H,Y) is None
    assert horizon(g,L,H,Y)==10
    print('PASS: p2 -> p4 abstract carry lift; p72/K5 extra column dies at step 10')
