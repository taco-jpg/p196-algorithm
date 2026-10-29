#!/usr/bin/env python3
"""Independent explicit O(b*p) integer DP, compares every suffix domain to intervals.
Uses direct forward tests / table elimination, no symbolic regime formulas.
"""
import random
from agent16_interval_preimage import suffix_domains, parent_edges, diagonal_parent, six_parents, candidate_starts

def direct_domains(b,g,L,H,Y):
    p=len(g);i=iter(Y);yd=[next(i) if bit else 0 for bit in g]
    domains=[None]*(p+1)
    domains[p]=set(range(2*b-1))
    for t in range(p-1,-1,-1):
        allowed=set()
        for x in range(2*b-1):
            for c in (0,1):
                if (x+c)//b!=H[t]:continue
                y=(x+L[t])%b+(yd[t] if g[t] else (x+c)%b)
                if y in domains[t+1]:allowed.add(x)
        domains[t]=allowed
    return domains

def main():
    rng=random.Random(160474)
    count=0
    for b in range(2,22):
        for p in range(1,11):
            for _ in range(35):
                g=tuple(rng.randrange(2) for _ in range(p))
                L=tuple(rng.randrange(2) for _ in range(p))
                H=tuple(rng.randrange(2) for _ in range(p))
                Y=tuple(rng.randrange(b) for bit in g if bit)
                fast=suffix_domains(b,g,L,H,Y)
                slow=direct_domains(b,g,L,H,Y)
                for t in range(p+1):
                    exact=set(x for lo,hi in fast[t] for x in range(lo,hi+1))
                    assert exact==slow[t],(b,p,t,g,L,H,Y,fast[t],slow[t])
                count+=1
    for r in range(4,7):
        b=1<<(r+1);p=2*r+4
        g=tuple(int(t in (0,r+1,r+2)) for t in range(p))
        for k,params in enumerate(six_parents(r)):
            L,H,Y=diagonal_parent(r,*params)
            yd=dict(zip((0,r+1,r+2),Y))
            brute={}
            for x0 in range(2*b-1):
                todo=[(0,x0,(),())]
                while todo:
                    t,x,xs,cs=todo.pop()
                    if t==p:
                        if x==x0:
                            z=(tuple((xs[v]+L[v])//b for v in range(p)),cs,
                               tuple((xs[v]+cs[v])%b for v in (0,r+1,r+2)))
                            brute.setdefault(z,[]).append((xs,cs))
                        continue
                    if not 0<=x<=2*b-2:continue
                    for c in (0,1):
                        if (x+c)//b!=H[t]:continue
                        nx=(x+L[t])%b+(yd[t] if g[t] else (x+c)%b)
                        todo.append((t+1,nx,xs+(x,),cs+(c,)))
            accelerated=parent_edges(r,(L,H,Y),candidate_starts(b,k))
            assert accelerated==brute,(r,k,len(accelerated),len(brute))
    print('PASS independent all-start carry DFS vs interval-accelerated boundary-parent edges r=4..6')
    print('PASS',count,'independent random exact domain comparisons: b2..21, p1..10, every temporal suffix')

if __name__=='__main__':main()
