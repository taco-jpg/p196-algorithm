#!/usr/bin/env python3
"""Explicit all-k period-two g=01 neutral-band exterior paths.

An exact path of k+1 *spatial columns* from the initial cut (0,2,1)
to a neutral accepting cut in base b=3*2**k-4. This is a finite
checker for the PAPER PROOF of the formulas, not an oracle for all k.
"""
import sys


def step(b, state, column, first=False):
    L,H,Y=state; x0,x1,c0,c1=column
    l0,l1=L&1,(L>>1)&1;h0,h1=H&1,(H>>1)&1
    assert (1 if first else 0)<=x0<=2*b-2 and 0<=x1<=2*b-2
    assert c0 in (0,1) and c1 in (0,1)
    assert (x0+c0)//b==h0 and (x1+c1)//b==h1
    assert x1==(x0+l0)%b+(x0+c0)%b
    assert x0==(x1+l1)%b+Y
    return ((x0+l0)//b+2*((x1+l1)//b), c0+2*c1, (x1+c1)%b)


def certificate(k):
    assert k>=1
    b=3*2**k-4
    edges=[]; current=(0,2,1)
    def add(col,expected):
        nonlocal current
        out=step(b,current,col,first=(len(edges)==0))
        assert out==expected,(k,b,len(edges),current,col,out,expected)
        edges.append((current,col,out));current=out
    if k==1:
        add((1,2,0,0),(2,0,0))
    else:
        add((b-2,2*b-3,1,0),(2,1,b-3))
        r=k//2
        if k%2==0:  # k=2r
            for j in range(r-1):
                A=3*4**j
                add((b+A-1,2*A-2,0,1),(1,2,2*A-1))
                add((b-2*A-1,2*b-4*A,1,0),(2,1,b-4*A))
            A=3*4**(r-1)   # b=4*A-4
            assert b==4*A-4
            add((b+A-2,2*A-3,1,1),(1,3,b//2))
            add((3*b//2-1,b-1,0,1),(1,2,0))
        else:  # k=2r+1, r>=1
            for j in range(r):
                A=3*4**j
                add((b+A-1,2*A-2,0,1),(1,2,2*A-1))
                if j!=r-1:
                    add((b-2*A-1,2*b-4*A,1,0),(2,1,b-4*A))
            A=3*4**(r-1)   # b=8*A-4
            assert b==8*A-4
            add((b-2*A,2*b-4*A+1,0,0),(2,0,b//2-1))
    if k%2==1:
        add((b//2-1,b-1,1,0),(2,1,b-1))
    assert len(edges)==k+1, (k,len(edges))
    L,H,Y=current
    assert all((L>>t&1)+(H>>t&1)==1 for t in range(2))
    assert Y==(b-1)*(L>>1&1)
    return b,edges


def main():
    n=int(sys.argv[1]) if len(sys.argv)>1 else 200
    for k in range(1,n+1):
        b,path=certificate(k)
        if k<=8 or k==n:
            print(f'k={k} b={b} path_length={len(path)} accepting={path[-1][2]}')
    print(f'PASS: explicit accepting-path arithmetic checked for all 1<=k<={n}')


if __name__=='__main__':
    main()
