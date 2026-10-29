#!/usr/bin/env python3
"""Independent whole-decimal-integer replay for the 72-step rec2/U3 wall repair.

No pairword next-step engine is used: every orbit step adds an ordinary integer
and the decimal reversal of its canonical digit string.
"""
import csv
import os
import sys
sys.set_int_max_str_digits(0)
BASE = os.path.dirname(os.path.abspath(__file__))
W = [[int(x) for x in r] for r in csv.reader(open(os.path.join(BASE,"rows.csv")))]
B = [[int(x) for x in r] for r in csv.reader(open(os.path.join(BASE,"B.csv")))]
U = [10,4,10]

def seed(q,k,d):
    H = B[0] + W[0] * q + [3,4] + U * k + [10,4]
    j = len(B[0]) + len(W[0]) * q
    H[j+2] += d
    H[j+4] -= d
    assert min(H)>=0 and max(H)<=18 and H[-1]%2==0
    p = H+H[-2::-1]
    out = [0] * len(p)
    for i in range(len(p)//2):
        hi=min(9,p[i])
        out[i]=p[i]-hi
        out[-1-i]=hi
    out[len(p)//2]=p[len(p)//2]//2
    assert out[-1]!=0
    return int(''.join(str(z) for z in reversed(out)))

def replay(q,k,d):
    n=seed(q,k,d)
    n0=len(str(n))
    assert n%11==0
    for t in range(73):
        s=str(n)
        assert s!=s[::-1],("pal",q,k,d,t)
        length=len(s)
        assert length == n0 + (t+1)//2, (q,k,d,t,length)
        for i in range(11):
            assert int(s[-1-i])+int(s[i]) == B[t%8][i],("root",q,k,d,t,i)
        if t==72:
            p=[int(s[-1-i])+int(s[i]) for i in range((length+1)//2)]
            assert p[11:11+48*q] == W[0]*q, ("outer wall not returned",q,k,d)
            return n
        new=n+int(s[::-1])
        assert len(str(new)) - len(s) == (t%2==0), ("overflow",q,k,d,t)
        n=new

if __name__ == '__main__':
    for q,k in [(5,34),(6,36),(8,36),(10,80),(16,80),(32,160),(64,160),(128,240)]:
        a=replay(q,k,-5)
        b=replay(q,k,4)
        assert a==b, ("nonconfluence at 72",q,k)
        u,v=seed(q,k,-5),seed(q,k,4)
        for step in range(2):
            u+=int(str(u)[::-1])
            v+=int(str(v)[::-1])
        assert u==v, ("two-step confluence",q,k)
        print("PASS",q,k,"initial digits",len(str(seed(q,k,-5))),"at72",len(str(a)),"d=-5 and d=4 coalesce by t2")