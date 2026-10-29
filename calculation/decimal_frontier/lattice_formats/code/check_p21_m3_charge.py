#!/usr/bin/env python3
"""Independent 42-step row classification, using two cyclic fixed-point carry trials."""
from itertools import product
from collections import Counter
g=[int(c) for c in '001001010101001010101']*2

def nxt(r,bit):
    if r==(9,9,9):return None
    carries=[]
    for backwards in (False,True):
        good=[]
        for start in (0,1):
            val=start;v={}
            for j in range(3):
                i=(-j)%3 if backwards else j
                v[i]=val;val=(r[i]+val)//10
            if val==start:good.append([v[i] for i in range(3)])
        assert len(good)==1
        carries.append(good[0])
    a,d=carries
    return tuple((r[i]+a[i])%10+(r[(i-bit)%3]+d[(i-bit)%3])%10 for i in range(3))

def block(r):
    for bit in g[:21]:
        r=nxt(r,bit)
        if r is None:return None
    return r

def main():
    hist=Counter();cycles=set();n=0;rotations=0
    for r0 in product(range(19),repeat=3):
        r1=block(r0)
        if r1 is None or r1==r0 or block(r1)!=r0:continue
        if len(set(r0))==1:continue
        if not any(all(r0[i]==r0[(axis-i)%3] for i in range(3)) for axis in range(3)):continue
        cycles.add(tuple(sorted((r0,r1))))
        r=r0;z=[]
        for bit in g:
            a,d=[],[]
            for backward,v in ((False,a),(True,d)):
                for start in (0,1):
                    carry=start;cs=[0]*3
                    for j in range(3):
                        i=(-j)%3 if backward else j
                        cs[i]=carry;carry=(r[i]+carry)//10
                    if carry==start:v.extend(cs);break
            assert len(a)==len(d)==3
            z.append((a[0],(r[0]+d[0])//10,(r[2]+d[2])%10 if bit else 0,bit))
            r=nxt(r,bit)
        assert r==r0
        def q(zs):
            return sum(pow(2,(-t)%6,9)*(L-H+bit*Y) for t,(L,H,Y,bit) in enumerate(zs))%9
        v=q(z);assert v in (3,6);hist[v]+=1
        for sh in range(42):
            assert q(z[sh:]+z[:sh]) in (3,6);rotations+=1
        n+=1
    print('INDEPENDENT CHECK',dict(hist),'cycle_pairs',len(cycles),'rotations',rotations)
    assert n==30 and hist=={3:15,6:15} and len(cycles)==15 and rotations==1260
if __name__=='__main__':main()
