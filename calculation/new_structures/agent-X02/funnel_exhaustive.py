#!/usr/bin/env python3
"""Independent base-10 bigint truth-table and complete binary-word controls."""
from itertools import product

def digits(n):
    out=[]
    while n:
        out.append(n%10); n//=10
    return out

def one(n):
    d=digits(n)
    return n+int(''.join(map(str,d)))

def make_n0(a,bits):
    h=len(bits)+1
    p=[a+9]+[a+9 if x else a for x in bits]
    dd=[0]*(2*h)
    for j,q in enumerate(p):
        high=min(9,q)
        dd[j]=q-high; dd[-j-1]=high
    return sum(int(x)*10**i for i,x in enumerate(dd))

def pair(n):
    d=digits(n)
    return [d[i]+d[-1-i] for i in range(len(d))]

def main():
    tests=0
    for a in range(5,9):
        for h in range(1,12):
            want=int(str(a+1)+str(2*a-9)*(2*h-2)+str(2*a-10)+str(a))
            expect=[a]+[2*a]*(2*h-1)+[a]
            seen=set()
            for bits in product((0,1),repeat=h-1):
                n0=make_n0(a,bits)
                n1=one(n0); n2=one(n1)
                assert n2==want,(a,h,bits,n2,want)
                assert pair(n1)==expect,(a,h,bits,pair(n1),expect)
                assert digits(n0)!=digits(n0)[::-1]
                assert digits(n1)!=digits(n1)[::-1]
                assert digits(n2)!=digits(n2)[::-1]
                seen.add(n0); tests+=1
            assert len(seen)==2**(h-1)
    print('FUNNEL_EXHAUSTIVE_PASS',tests,'a=5..8 h=1..11')
if __name__=='__main__':main()
