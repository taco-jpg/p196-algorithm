#!/usr/bin/env python3
"""Independent Python integer/decimal cross-check."""
from centre_scan_data import B,W,U
import sys
if hasattr(sys,"set_int_max_str_digits"):sys.set_int_max_str_digits(0)
def templ(q,k,ui,C):
    h=B+W*q+[5]+U[ui]*k
    return h+C+h[::-1]
def canonical(p):
    assert p==p[::-1]
    d=[0]*len(p)
    for i in range(len(p)//2):
        d[i]=max(p[i]-9,0)
        d[-1-i]=p[i]-d[i]
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]>0
    return sum(z*10**i for i,z in enumerate(d))
def check(q,k,ui,C):
    p=templ(q,k,ui,C);n=canonical(p);overflows=[]
    for t in range(120):
        s=str(n);m=n+int(s[::-1])
        overflows.append(int(len(str(m))>len(s)))
        n=m
    digits=list(map(int,str(n)[::-1]))
    p2=[a+b for a,b in zip(digits,digits[::-1])]
    target=templ(q,k+5,ui,C)
    first=next((i for i,(a,b) in enumerate(zip(p2,target)) if a!=b),None)
    return {"gamma":''.join(map(str,overflows)),"return":p2==target,"first":first,"size":len(p2),"expected":len(target)}
if __name__=='__main__':
    for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:
        for ui,C in [(0,[0]*8),(1,[18,2,14,16,14,2,18]),(2,[4,14,4])]:
            print(q,k,ui,C,check(q,k,ui,C))