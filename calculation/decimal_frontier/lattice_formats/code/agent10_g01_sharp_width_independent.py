#!/usr/bin/env python3
"""Independent original-equation enumeration, never uses affine/corridor assumptions.

Run: python3 agent10_g01_sharp_width_independent.py
Checks all b=2..256 through width 8, all 2-time columns without
one-carry pruning, plus base26 positive and family instances to m=10.
"""

def original_edges(base,state,first):
    (L,H,Y)=state
    l0,l1=L&1,(L>>1)&1
    h0,h1=H&1,(H>>1)&1
    out=set()
    for x0 in range(1 if first else 0,2*base-1):
        for c0 in (0,1):
            if (x0+c0)//base != h0: continue
            x1=(x0+l0)%base+(x0+c0)%base
            if x1>2*base-2 or (x1+l1)%base+Y != x0: continue
            for c1 in (0,1):
                if (x1+c1)//base != h1: continue
                LL=(x0+l0)//base+2*((x1+l1)//base)
                HH=c0+2*c1
                YY=(x1+c1)%base
                out.add((LL,HH,YY))
    return out

def acc(base,state):
    L,H,Y=state
    return (L&1)+(H&1)==1 and ((L>>1)&1)+((H>>1)&1)==1 and Y==(base-1)*((L>>1)&1)

def until(base, max_width):
    layer={(0,2,1)}
    for depth in range(1,max_width+1):
        layer=set().union(*(original_edges(base,state,depth==1) for state in layer)) if layer else set()
        if any(acc(base,s) for s in layer):return depth
    return None

def main():
    tested=0
    for base in range(2,257):
        first=until(base,8)
        if first is not None:
            assert base <=3*2**(first-1)-4,(base,first)
        tested+=1
    assert until(26,8)==8
    for m in range(2,11):
        base=3*2**(m-1)-4
        assert until(base,m)==m,(m,base)
        assert until(base+1,m) is None,(m,base+1)
    print('PASS: independent original-equation complete bounded-width scan b=2..256, m<=8')
    print('PASS: sharp boundary family m=2..10 and b_m+1 exclusions')
    print('CONTROL PASS: base26 g=01 first accepting width=8')

if __name__=='__main__':main()
