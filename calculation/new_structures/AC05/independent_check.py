#!/usr/bin/env python3
"""Independent Python bigint versus decimal digit-list controls."""
import sys
sys.set_int_max_str_digits(0)
B=(10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5)
W=(5,18,4,8,1,15,4,0,5)
U=((9,8,10),(8,10,9),(10,9,8))
def pair(u,c,q,k):
    half=list(B)+list(W)*q+[5]+list(U[u])*k
    return half+list(c)+half[::-1]
def realize(p):
    d=[0]*len(p)
    for i in range(len(p)//2):
        hi=min(9,p[i]);d[i]=p[i]-hi;d[-i-1]=hi
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1] and all(x<=9 for x in d)
    return d
def digit_step(d):
    carry=0; out=[]
    for a,b in zip(d,reversed(d)):
        v=a+b+carry
        out.append(v%10);carry=v//10
    if carry:out.append(carry)
    return out
def run(u,L,q,k):
    h=L//2;c=[0]*L
    for i in range(h):c[i]=c[-i-1]=(7*i+11+u)%19
    if L%2:c[h]=(6+2*u)%20
    d=realize(pair(u,c,q,k));n=int(''.join(map(str,d[::-1])));clock=[]
    for t in range(120):
        old=d;d=digit_step(d)
        n=n+int(str(n)[::-1])
        assert d==list(map(int,str(n)[::-1])),(u,L,q,k,t)
        clock.append(len(d)-len(old))
    target=pair(u,c,q,k+5)
    got=[d[i]+d[-i-1] for i in range(len(d))]
    assert len(got)==len(target)
    assert clock==[1,0,0,0]*30
    cen=len(d)//2;window=152+L
    diffs=[i-cen for i in range(max(0,cen-window),min(len(got),cen+window)) if got[i]!=target[i]]
    print("INDEPENDENT",u,L,q,k,"gamma",sum(clock),"first-centre-mismatch",diffs[0] if diffs else None)
for u in range(3):
 for L in range(7,15):
  for q,k in ((14,100),(20,80),(40,160),(80,320),(160,640)):
   run(u,L,q,k)
