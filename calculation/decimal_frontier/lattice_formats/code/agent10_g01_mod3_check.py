#!/usr/bin/env python3
"""Independent finite edge checks for the all-base mod-3 PAPER PROOF.

The theorem is algebraic and holds for every b>=2 with b % 3 == 1.
This script spot-checks all legal cut-state edges in a finite base range.
"""

def succ(b, L, H, y, first=False):
    l0,l1 = L&1,(L>>1)&1
    h0,h1 = H&1,(H>>1)&1
    for x0 in range(1 if first else 0,2*b-1):
        for c0 in (0,1):
            if (x0+c0)//b != h0:
                continue
            x1=(x0+l0)%b+(x0+c0)%b
            if x1>2*b-2 or x0 != (x1+l1)%b+y:
                continue
            for c1 in (0,1):
                if (x1+c1)//b != h1:
                    continue
                a=(x0+l0)//b; e=(x1+l1)//b
                yield a+2*e,c0+2*c1,(x1+c1)%b


def inv(L,H,y):
    return (y-((L>>1)&1)+(H&1)-((H>>1)&1))%3


def main():
    checks=0
    for b in range(4,101,3):
        for v in succ(b,0,2,1,True):
            assert (v[0] in (1,2)) and inv(*v)==1,(b,v)
            checks+=1
        for L in (1,2):
            for H in range(4):
                for y in range(b):
                    for v in succ(b,L,H,y):
                        assert v[0] in (1,2)
                        assert inv(*v)==inv(L,H,y),(b,(L,H,y),v)
                        checks+=1
        for L,H,y in ((2,1,b-1),(1,2,0)):
            assert inv(L,H,y)!=1
    print('PASS: exact mod-3 invariant for b=4,7,...,100; checked',checks,'edges')
    print('PASS: accepted L=2/H=1/y=b-1 and L=1/H=2/y=0 violate invariant 1')

if __name__=='__main__':
    main()
