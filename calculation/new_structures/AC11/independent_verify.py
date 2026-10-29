#!/usr/bin/env python3
"""Independent physical big-integer reverse/add and carry-prefix controls.

COMPUTED finite controls only. No decimal all-time Lychrel certificate.
"""
import random
import sys
sys.set_int_max_str_digits(0)
B=[2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11]
W=[1,10,8,5,9,16,0,9,11]
def uwords():
    return [tuple((9,a,18-a)[(i+r)%3] for i in range(3))
            for a in range(0,19,2) for r in range(3)]
def digits(n):
    return [int(ch) for ch in str(n)[::-1]]
def pair(d):
    return [d[i]+d[-1-i] for i in range(len(d))]
def realize(half, centre):
    p=half+centre+half[::-1]
    assert p==p[::-1] and p[0]==2
    d=[0]*len(p)
    for i in range(len(p)//2):
        a=min(9,p[i])
        if i==0:a=0 # keep highest decimal digit nonzero
        b=p[i]-a
        assert 0<=a<=9 and 0<=b<=9
        d[i]=a;d[-1-i]=b
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]!=0 and pair(d)==p
    return int(''.join(map(str,d[::-1])))
def prefix_step(p):
    r=len(p)-1
    while r>=0 and p[r]==9:r-=1
    assert r>=0
    low=[];carry=0
    for x in p:
        z=x+carry;low.append(z%10);carry=z//10
    upper=[0]*r;carry=int(p[r]>=10)
    for i in range(r-1,-1,-1):
        z=p[i]+carry;upper[i]=z%10;carry=z//10
    gamma=carry
    out=([low[0]+1] if gamma else [])
    out.extend(low[i]+upper[i-gamma] for i in range(gamma,r+gamma))
    return out,gamma
def control(J,U,C,q,k):
    half=B+W*q+list(J)+list(U)*k
    n=realize(half,list(C))
    prefix=half[:34+9*q+len(J)+3*48]
    clocks=[]
    for t in range(120):
        d=digits(n);p=pair(d)
        assert p[:len(prefix)]==prefix,('prefix mismatch',t,q,k)
        nxt=n+int(str(n)[::-1]) # true decimal big-integer reverse-and-add
        dd=digits(nxt)
        carry=0;normal=[]
        for x in p:
            z=x+carry;normal.append(z%10);carry=z//10
        if carry:normal.append(carry)
        assert dd==normal,('schoolbook mismatch',t,q,k)
        gamma=len(dd)-len(d)
        assert gamma==int((t+2)%4==0),('wrong clock',t,q,k)
        prefix,pgamma=prefix_step(prefix)
        assert gamma==pgamma
        clocks.append(gamma);n=nxt
    actual=pair(digits(n))
    h=B+W*q+list(J)+list(U)*(k+5)
    expected=h+list(C)+h[::-1]
    difference=next((i for i,(x,y) in enumerate(zip(actual,expected)) if x!=y),-1)
    assert len(actual)==len(expected) and sum(clocks)==30
    assert difference>=0 and difference<34+9*q,('unexpected W9 restoration',q,k,J,U,C)
    assert actual[:len(prefix)]==prefix
    return difference
if __name__=="__main__":
    rng=random.Random(12022026)
    widths=[(14,100),(20,80),(40,160),(80,320),(160,640)]
    report=[]
    for uidx,U in enumerate(uwords()):
        for nj in (3,4):
            J=[rng.randrange(19) for _ in range(nj)]
            for ci,C in enumerate(([4,14,4],[4,4])):
                trials=widths if uidx%5==0 and ci==0 else widths[:1]
                for q,k in trials:report.append((uidx,nj,ci,q,k,control(J,U,C,q,k)))
    print("BIGINT_PASSED",len(report),"reference",sum(x[3]==14 for x in report),
          "min_difference",min(x[5] for x in report),
          "max_difference",max(x[5] for x in report))