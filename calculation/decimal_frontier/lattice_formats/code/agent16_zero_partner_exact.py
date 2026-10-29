#!/usr/bin/env python3
"""Primary exhaustive check for the universal zero-partner carry-reset barrier.
This enumerates explicit carry/L choices and integer coefficients, not matrix products.
"""
from itertools import product

def forward(b,x,L,g,Y,c):
    assert 0 <= x <= 2*b-2
    return (x+L)%b + (Y if g else (x+c)%b)

def all_postreset(b,q):
    vals={0}
    for _ in range(q):
        vals={forward(b,x,L,0,0,c) for x,L,c in product(vals,(0,1),(0,1))}
        assert all(0 <= x <= 2*b-2 for x in vals)
    return vals

def reset_possible(b):
    # Explicit antecedent: g0=1,L0=0,Y0=0; g1=0,L1=1,H1=1.
    paths=[]
    for x0,c0,c1 in product(range(2*b-1),(0,1),(0,1)):
        x1=forward(b,x0,0,1,0,c0)
        if (x1+c1)//b != 1: continue
        x2=forward(b,x1,1,0,0,c1)
        paths.append((x0,x1,x2,c0,c1))
    return paths

def sharp(b,q):
    assert q>=1 and b==2**(q+1)-1
    x0=b-1; x1=forward(b,x0,0,1,0,0)
    assert x1==b-1 and (x1+1)//b==1
    x=forward(b,x1,1,0,0,1)
    assert x==0
    for _ in range(q):
        assert (x+1)//b==0
        x=forward(b,x,1,0,0,1)
    assert x==b-1 and (x+1)//b==1
    return x

def main():
    for b in range(2,201):
        r=reset_possible(b)
        assert r and all(x2==0 for _,_,x2,_,_ in r),(b,r)
        for q in range(8):
            if b>=2**(q+1):
                vals=all_postreset(b,q)
                assert max(vals)<=2**(q+1)-2
                assert all(x+1 < b for x in vals),(b,q,vals)
    for q in range(1,13):
        assert sharp(2**(q+1)-1,q)==2**(q+1)-2
    print('PASS explicit all-x/c reset b=2..200; all q=0..7 above cutoff; exact sharp witnesses q=1..12')

if __name__=='__main__':main()
