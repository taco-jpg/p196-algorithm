#!/usr/bin/env python3
"""Independent positive full-integer controls for Q09.
This does not establish any infinite base-10 orbit.
Run: python3 calculation/new_structures/Q09/check.py
"""
B9=[8,9,10,13,14,12,3,14,10,0,11,7,10,9,7,8,8,14,15,2,9,7,0,5,8,3,8,11,8,6,8,7,5,14,11,3,9,3,8,14,7,12,8,2,0,12,1,5,13,8,1,16,15,9,1,7,6,2,1,15,15]
W9=[1,1,15,15]
B50=[48,52,43,61,26,44,60,28,40,67,63,70,57,33,31,36,26,45,58,32,33,32,34,30,37,73,52,42,62,73,51,44,59,30,37,24]
C50=[62,15,22,32,32,22,15,62]
def digits(n,b):
    a=[]
    while n:a.append(n%b);n//=b
    return a or [0]
def value(ds,b):
    n=0
    for d in reversed(ds):n=b*n+d
    return n
def reverse(n,b):return value(digits(n,b)[::-1],b)
def step(n,b):return n+reverse(n,b)
def pair(n,b):
    a=digits(n,b)
    return [a[i]+a[-1-i] for i in range(len(a))]
def seed(P,b):
    assert P==P[::-1] and len(P)%2==0
    d=[0]*len(P)
    for i in range(len(P)//2):
        d[i]=max(0,P[i]-b+1)
        d[-1-i]=P[i]-d[i]
    assert d[-1]>0
    return value(d,b)
def p9(l):return B9+[W9[i%4] for i in range(l)]+B9[::-1]
def p50(h):return B50+[49]*h+C50+[49]*h+B50[::-1]
def control(b,tmpl,period,gain):
    for m in (20,40,80,160):
        h=4*m+2 if b==9 else m
        n=seed(tmpl(h),b)
        for t in range(81):
            if t%period==0:
                assert pair(n,b)==tmpl(h+gain*(t//period)),(b,m,t)
            assert digits(n,b)!=digits(n,b)[::-1]
            if t<80:n=step(n,b)
        print("BIGINT CONTROL",b,m,period,gain,"PASS")
control(9,p9,10,4)
control(50,p50,4,1)
for m in (20,40,80,160):
    n=int("93"+"525"*m+"28")
    for t in range(16):
        if n%10: assert step(reverse(n,10),10)==step(n,10)
        n=step(n,10)
    print("DECIMAL SIZE",m,"PASS")
assert step(4,10)==8 and 99-step(5,10)==89
assert step(10,10)!=10*step(1,10)
print("EXCLUSION WITNESSES PASS")
