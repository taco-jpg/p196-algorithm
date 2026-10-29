#!/usr/bin/env python3
"""Independent ordinary Python bigint replay for the exact AC36 root."""
import sys
sys.set_int_max_str_digits(0)
B=[5,2,3,12,16,2,15,10,9,7,18,8,15,9,1,14,0,3,10,0,17,17,9,3,3,15,8,7,9,4,3,3,9,2]
W=[4,0,17,11,9,12,2,9,2]
def template(j,u,odd,q,k):
    h=B+W*q+list(j)+list(u)*k
    return h+([4,14,4] if odd else [4,4])+h[::-1]
def realize(p):
    assert p==p[::-1]
    d=[0]*len(p)
    for i in range(len(p)//2):
        d[-i-1]=min(p[i],9)
        d[i]=p[i]-d[-i-1]
    if len(p)%2:d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]!=0 and all(0<=x<=9 for x in d)
    return int(''.join(map(str,d[::-1])))
def check(j,u,odd,q,k):
    source=template(j,u,odd,q,k)
    target=template(j,u,odd,q,k+5)
    n=realize(source)
    pair=lambda x:[int(a)+int(b) for a,b in zip(str(x)[::-1],str(x))]
    assert pair(n)==source
    gamma=[]
    for t in range(120):
        s=str(n)
        n=n+int(s[::-1])
        gamma.append(len(str(n))-len(s))
    actual=pair(n)
    first=next((i for i,(a,b) in enumerate(zip(actual,target)) if a!=b),None)
    if first is None and len(actual)!=len(target):first=min(len(actual),len(target))
    firstW=next((i for i in range(34,34+9*q) if actual[i]!=target[i]),None)
    return first,firstW,sum(gamma),gamma==[int(t%4==1) for t in range(120)]
if __name__=="__main__":
    for j in [(0,0,0,0,0,0),(0,15,4,7,0,0),(0,10,4,0,0,1)]:
      for u in [(0,9,18),(9,4,14),(14,4,9)]:
       for odd in (False,True):
        for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:
         x=check(j,u,odd,q,k)
         assert x[2:]==(30,True), (j,u,odd,q,k,x)
         if j==(0,0,0,0,0,0) and q==14 and k==100:assert x[0]==135,x
    print("INDEPENDENT_BIGINT_PASS: 90 controls (3 J * 3 U * 2 C * 5 widths)");
