#!/usr/bin/env python3
"""Independent Python integer oracle for agent X24 inverse fibres."""
from itertools import product
from random import Random
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
def seed(r,bits):
    lo=B+W*r
    c=[0]+[1+9*x for x in bits]
    p=lo+c+c[::-1]+lo[::-1]
    digs=[0]*len(p)
    for i in range(len(p)//2):
        digs[i]=p[i]//2
        digs[len(p)-1-i]=p[i]-digs[i]
    assert 0<digs[-1]<=9 and max(digs)<=9
    return int(''.join(map(str,digs[::-1])))
def R(n):return n+int(str(n)[::-1])
def pal(n):s=str(n);return s==s[::-1]
def main():
    count=0
    for r in (1,2,5,12,20):
        for k in range(1,9):
            first=set();after=None
            for bits in product((0,1),repeat=k):
                n=seed(r,bits);s=R(n);z=R(s)
                assert not pal(n) and not pal(s) and s not in first
                first.add(s)
                if after is None:after=z
                assert z==after
                count+=1
            assert len(first)==2**k
    rng=Random(20261028)
    for _ in range(60):
        k=rng.choice((9,16,32,64,100,200));r=rng.choice((1,2,10,20))
        a=seed(r,[0]*k);bits=[rng.randrange(2) for i in range(k)]
        if not any(bits):bits[0]=1
        b=seed(r,bits)
        assert R(a)!=R(b) and R(R(a))==R(R(b))
        assert not pal(a) and not pal(b) and not pal(R(a)) and not pal(R(b))
    print(f"PASS exhaustive={count} random=60, k<=200")
if __name__=="__main__":main()
