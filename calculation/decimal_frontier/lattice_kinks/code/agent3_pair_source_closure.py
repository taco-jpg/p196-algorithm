#!/usr/bin/env python3
"""Exact two-step midpoint-source alphabets and relaxed rec2 charge closure.

PAPER PROOF in reports/Agent3PairSourceClosure.md. Standard library only.
A relaxed source DP is NOT a centre SAT solver and its witnesses are NOT orbits.
"""
from pathlib import Path
from random import Random
import sys


def load(path):
    v=list(map(int,Path(path).read_text().split()))
    p,nb,m,b=v[:4];gam=v[4:4+p];v=v[4+p:]
    assert (p,nb,m,b)==(8,11,48,10)
    assert len(v)==p*(2*m+nb)
    W=[v[t*m:(t+1)*m] for t in range(p)]
    cup=[v[p*m+t*m:p*m+(t+1)*m] for t in range(p)]
    B=[v[2*p*m+t*nb:2*p*m+(t+1)*nb] for t in range(p)]
    d=[]
    for t in range(p):
        sols=[]
        for seed in (0,1):
            row=[None]*m;row[-1]=seed
            for j in range(m-1,0,-1):
                row[j-1]=int(W[t][j]+row[j]>=10)
            if seed==int(W[t][0]+row[0]>=10):sols.append(row)
        assert len(sols)==1,(t,sols)
        d.append(sols[0])
        assert all(cup[t][(j+1)%m]==int(W[t][j]+cup[t][j]>=10) for j in range(m))
        assert sum(pow(10,j,99)*W[t][j] for j in range(m))%99==0
        assert max(sum(W[t][(j+k)%m]==9 for k in range(3)) for j in range(m))<3
    return p,nb,m,gam,W,cup,B,d


def check_closure(lat, laps=(1,2,3)):
    p,nb,m,gam,W,cup,B,d=lat
    assert gam==[1,0,1,0,1,0,1,0]
    def cell(t,i):return B[t%p][i] if i<nb else W[t%p][(i-nb)%m]
    def bulk(t,L,h):return sum(pow(10,i,99)*cell(t,i) for i in range(L,h))%99
    V_even=set(range(10))
    V_odd={(-40*k-18*(k>=5)-9*c)%99 for k in range(10) for c in (0,1)}
    assert len(V_even)==10 and len(V_odd)==20
    print('pair alphabets (scaled by 10^h): even-start=10, odd-start=20')
    for laps_count in laps:
        for o in range(4):
            stats=set();bad_defects=set()
            for r in range(48):
                L=nb+2+r;j=(L-nb)%m;qL=pow(10,L,99)
                n=400+o;S={0};sizes=[]
                for pair in range(96*laps_count):
                    t=2*pair; t0=t%8;t1=(t+1)%8
                    assert gam[t0]==1 and gam[t1]==0
                    h=(n+1)//2
                    q=pow(10,h if n%2==0 else h-1,99)
                    V=V_even if n%2==0 else V_odd
                    X0=qL*(W[t0][(j-1)%m]+cup[t0][j]-10*d[t0][(j-2)%m])
                    X1=qL*(cup[t1][j]-10*d[t1][(j-1)%m])
                    sources={(2*X0+X1+q*v)%99 for v in V}
                    S={(22*s+x)%99 for s in S for x in sources}
                    sizes.append(len(S));n+=1
                assert n==400+o+96*laps_count
                assert bulk(0,L,(n+1)//2)==bulk(0,L,(401+o)//2)
                expected=99 if o%2==0 else 90
                assert len(S)==expected,(laps_count,o,r,len(S))
                stats.add((sizes[0],sizes[1],sizes[-1]))
                if o%2:
                    missing=set(range(99))-S
                    assert len(missing)==9
                    bad_mods={x%11 for x in missing}
                    assert len(bad_mods)==1
                    bad_Q=next(iter(bad_mods))
                    bad_D=(bad_Q-bulk(0,L,(401+o)//2))%11
                    bad_defects.add(bad_D)
                    assert bad_D==8,(laps_count,o,r,bad_D)
                else:
                    assert S==set(range(99))
            print(f'laps={laps_count}, o={o}: source cardinalities {sorted(stats)}, forbidden D0={sorted(bad_defects)}')
    print('PASS: all 48 spatial cuts, four length classes, 192/384/576 steps; D0 != 8 for o=1,3')


def check_physical(lat):
    p,nb,m,gam,W,cup,B,d=lat
    def cell(t,i):return B[t%p][i] if i<nb else W[t%p][(i-nb)%m]
    def charge(P,L):return sum(pow(10,i,99)*P[i] for i in range(L,(len(P)+1)//2))%99
    def step(P):
        c=[0];O=[]
        for x in P:
            s=x+c[-1];O.append(s%10);c.append(s//10)
        g=c[-1]
        if g:O.append(1)
        return [O[i]+O[-1-i] for i in range(len(O))],c,g,O
    def source(P,c,g,O):
        n=len(P);h=(n+1)//2;R=h-1;q=pow(10,R,99)
        if n%2==0 and g==0:return (-9*q*c[h])%99
        if n%2==1 and g==0:return (q*(c[R]-10*c[h]))%99
        if n%2==0 and g==1:return (10*q*O[h])%99
        return (q*(-10*P[R]-9*c[h]))%99
    rng=Random(4741963)
    Ve=set(range(10))
    Vo={(-40*k-18*(k>=5)-9*c)%99 for k in range(10) for c in (0,1)}
    count=0
    for o in range(4):
        n=400+o;h=(n+1)//2
        for _ in range(100):
            w=rng.randrange(8,35)
            low=[cell(0,i) for i in range(h)]
            for i in range(h-w,h):low[i]=rng.randrange(19)
            if n%2:low[-1]=2*rng.randrange(10)
            P=low+low[::-1] if n%2==0 else low+low[-2::-1]
            assert len(P)==n and P==P[::-1]
            L=50;j=(L-nb)%m;qL=pow(10,L,99);Z=[]
            for t in range(4):
                assert all(P[i]==cell(t,i) for i in range(L))
                P2,c,g,O=step(P)
                assert g==gam[t]
                X=(qL*(cell(t,L-1)+cup[t][j]-10*d[t][(j-2)%m]) if g
                   else qL*(cup[t][j]-10*d[t][(j-1)%m]))%99
                assert c[L]==cup[t][j]
                assert c[len(P)-L]==d[t][(j-1)%m]
                assert c[len(P)-L+1]==d[t][(j-2)%m]
                z=source(P,c,g,O)
                assert charge(P2,L)==((11 if g else 2)*charge(P,L)+X+z)%99
                Z.append(z);P=P2
            ncur=n
            for pair in range(2):
                hcur=(ncur+1)//2
                q=pow(10,hcur if ncur%2==0 else hcur-1,99)
                v=((2*Z[2*pair]+Z[2*pair+1])*pow(q,-1,99))%99
                assert v in (Ve if ncur%2==0 else Vo),(o,pair,v)
                ncur+=1
            count+=1
    print(f'PASS: {count} physical four-step rec2 centre windows, {4*count} carry-exact transitions')


def main():
    default=Path(__file__).resolve().parents[1]/'data/lat2.txt'
    lat=load(sys.argv[1] if len(sys.argv)>1 else default)
    check_physical(lat)
    check_closure(lat)


if __name__=='__main__':main()
