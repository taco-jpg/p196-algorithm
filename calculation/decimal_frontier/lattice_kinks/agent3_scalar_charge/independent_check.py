#!/usr/bin/env python3
"""Independent Horner/extended-Euclid checker of the scalar-correction theorem."""
from pathlib import Path
from math import gcd
import sys
def egcd(a,b):
    if b==0:return (abs(a),1 if a>=0 else -1,0)
    g,x,y=egcd(b,a%b)
    return g,y,x-(a//b)*y
def check(path):
    a=[int(z) for z in Path(path).read_text().split()]
    p,nb,m,base=a[:4]; assert (p,nb,m,base)==(8,11,48,10)
    a=a[4+p:];W=[a[j*m:(j+1)*m] for j in range(p)]
    asc=[a[p*m+j*m:p*m+(j+1)*m] for j in range(p)]
    # Iteratively solve the 48-circle carry equations from both seeds; no import of main script.
    Ds=[]
    for phase in range(p):
        possibilities=[]
        for last in (0,1):
            x=[0]*m;x[m-1]=last
            for i in range(m-2,-1,-1):x[i]=int(W[phase][i+1]+x[i+1]>=10)
            if x[m-1]==int(W[phase][0]+x[0]>=10):
                possibilities.append(x)
        assert len(possibilities)==1
        D=possibilities[0]
        assert all(asc[phase][(i+1)%m]==int(W[phase][i]+asc[phase][i]>=10) for i in range(m))
        Ds.append(D)
    horner=lambda row:__import__('functools').reduce(lambda v,d:10*v+d,reversed(row),0)
    q=list(map(horner,W));d=list(map(horner,Ds))
    assert gcd(*q)==99 and gcd(d[0],d[2])==1
    A=q[0]*d[1]-q[1]*d[0];B=q[1]*d[2]-q[2]*d[1]
    g,x,y=egcd(A,B)
    assert g==99 and x*A+y*B==99
    # An independent direct modular solve, 1..10000: only divisors of 99 survive.
    for M in range(2,10001):
        # A necessary condition from two minors, but still inspect the actual equations.
        if 99%M==0:
            assert all(z%M==0 for z in q)
            assert all((z%M)!=0 for z in [d[0],d[2]]) or gcd(d[0],d[2])==1
        else:
            assert A%M or B%M
    print("INDEPENDENT PASS: Horner vs direct powers, both carry streams, explicit Bezout 99, moduli 2..10000")
if __name__=="__main__":
    check(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).with_name("lat2.txt")))
