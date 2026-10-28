#!/usr/bin/env python3
"""E1 decimal canonical-root forbidden-factor necklace count.

At base b=10, a cyclic factor 1101 (r=1) or 11001 (r=2)
forces an impossible canonical-root first-column trajectory, by the
11 0^r 1 bound b <= 2^(r+1). Rotating a time-closed first-column
trajectory preserves all canonical-root equations. The factor starts
at a 1, hence its rotated x0 >= b-1 > 0, so the "first" constraint
is also preserved. Therefore every phase of such a necklace is excluded.

The density condition 2*G<=p is a separate NECESSARY constraint for
the first-column automaton, not a sufficient criterion for an SCC.

A_d: number of rooted length-d cyclic binary words with <= d//2 ones,
avoiding 1101 and 11001 (including factors across the boundary).
Compute A_d as the weighted trace of an exact 4-bit de Bruijn walk.
B_d: same without forbidden factors, sum binomials.

Burnside: necklaces(p)=(1/p)*sum_{d|p} phi(p/d)*A_d
Primitive necklaces: (1/p)*sum_{d|p} mu(p/d)*A_d.
The second formula follows from Mobius inversion of rooted words.
Apply also to B_d, then subtract for excluded necklaces.
"""
import argparse
import csv
from math import comb


def divisors(n):
    return [d for d in range(1,n+1) if n%d==0]


def phi(n):
    return sum(1 for k in range(1,n+1) if gcd(k,n)==1)


def gcd(x,y):
    while y:x,y=y,x%y
    return x


def mu(n):
    factors=0
    p=2
    while p*p<=n:
        if n%p==0:
            n//=p;factors+=1
            if n%p==0:return 0
        p+=1
    if n>1:factors+=1
    return -1 if factors%2 else 1


def rooted_avoid(n):
    # Trace M(z)^n, where the 16 states store the previous four bits.
    # Reject the new bit 1 after suffix 110 (giving 1101), or after
    # full four-bit suffix 1100 (giving 11001).
    total=0
    for start in range(16):
        dp={(start,0):1}
        for _ in range(n):
            nxt={}
            for (state,weight),value in dp.items():
                for bit in (0,1):
                    if bit and (state&7)==6:continue
                    if bit and state==12:continue
                    ns=((state<<1)|bit)&15
                    key=(ns,weight+bit)
                    nxt[key]=nxt.get(key,0)+value
            dp=nxt
        total+=sum(v for (s,w),v in dp.items() if s==start and 2*w<=n)
    return total


def rooted_all(n):
    return sum(comb(n,w) for w in range(n//2+1))


def direct_counts(n):
    allroot=avoidroot=0
    allneck=set()
    avoidneck=set()
    for mask in range(1<<n):
        bits=tuple((mask>>i)&1 for i in range(n))
        if 2*sum(bits)>n:continue
        allroot+=1
        rots=tuple(bits[i:]+bits[:i] for i in range(n))
        can=min(rots)
        allneck.add(can)
        if all(not all(bits[(i+j)%n]==v for j,v in enumerate(word))
               for word in ((1,1,0,1),(1,1,0,0,1))
               for i in range(n)):
            avoidroot+=1
            avoidneck.add(can)
    return allroot,avoidroot,len(allneck),len(avoidneck)


def all_counts(n_max=32, brute_upto=16):
    A={};B={};rows=[]
    for n in range(1,n_max+1):
        A[n]=rooted_avoid(n); B[n]=rooted_all(n)
        divs=divisors(n)
        sum_b=sum(phi(n//d)*B[d] for d in divs)
        sum_a=sum(phi(n//d)*A[d] for d in divs)
        prim_b=sum(mu(n//d)*B[d] for d in divs)
        prim_a=sum(mu(n//d)*A[d] for d in divs)
        assert all(x%n==0 for x in (sum_b,sum_a,prim_b,prim_a)),n
        bt,at,bp,ap=(sum_b//n,sum_a//n,prim_b//n,prim_a//n)
        if n<=brute_upto:
            got=direct_counts(n)
            assert got==(B[n],A[n],bt,at),(n,got,(B[n],A[n],bt,at))
        assert 0<=ap<=at<=bt and 0<=bp<=bt
        rows.append(dict(p=n, density_admissible_necklaces=bt,
            excluded_necklaces=bt-at, surviving_necklaces=at,
            density_admissible_primitive=bp, excluded_primitive=bp-ap,
            surviving_primitive=ap))
    return rows


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--pmax',type=int,default=32)
    ap.add_argument('--brute-upto',type=int,default=16)
    ap.add_argument('--csv',default=None)
    a=ap.parse_args()
    rows=all_counts(a.pmax,a.brute_upto)
    for r in rows:
        print(*(r[k] for k in r))
    if a.csv:
        with open(a.csv,'w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]))
            w.writeheader();w.writerows(rows)
    print('PASS: weighted trace, Burnside/Mobius integrality, direct census controls')


if __name__=='__main__':
    main()
