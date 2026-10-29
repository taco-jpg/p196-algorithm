#!/usr/bin/env python3
"""Independent relation product for reset barrier; separate from primary direct replay."""

def relation(b,L,g,Y,H=None):
    return {x: {z for c in (0,1) if (H is None or (x+c)//b==H)
                for z in ((x+L)%b+(Y if g else (x+c)%b),)
                if 0<=z<=2*b-2}
            for x in range(2*b-1)}

def compose(A,B):
    return {x:set().union(*(B[y] for y in ys)) if ys else set() for x,ys in A.items()}

def main():
    for b in range(2,301):
        one=relation(b,0,1,0)
        two=compose(one,relation(b,1,0,0,1))
        assert all(v in ({0},set()) for v in two.values()),b
        for q in range(8):
            if b >= (1<<(q+1)):
                mat=two
                for _ in range(q):mat=compose(mat,relation(b,1,0,0))
                target=compose(mat,relation(b,0,0,0,1))
                assert not any(target.values()),(b,q)
    print('PASS independent full-integer-relation composition b=2..300, every q=0..7 with b>=2^(q+1)')

if __name__=='__main__':main()
