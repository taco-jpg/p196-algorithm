#!/usr/bin/env python3
"""Independent Python big-integer RAA vs decimal-array controls and abstract sets."""
import random,json,sys
from lab import run,template
from certify import Uwords,FULL,advance
if hasattr(sys,"set_int_max_str_digits"):sys.set_int_max_str_digits(0)
def decimal_source(p):
    assert p==p[::-1]
    n=len(p);d=[0]*n
    for i in range(n//2):
        lo=max(0,p[i]-9)
        d[i]=lo;d[n-1-i]=p[i]-lo
    if n&1:
        if p[n//2]&1:raise ValueError("Odd midpoint")
        d[n//2]=p[n//2]//2
    assert d[-1]!=0
    return int("".join(str(x) for x in reversed(d)))
def pairword(n):
    a=list(map(int,str(n)))[::-1]
    return [x+y for x,y in zip(a,a[::-1])]
def big_replay(J,U,C,q,k,steps=120):
    p=template(J,U,C,q,k);n=decimal_source(p)
    assert pairword(n)==p
    gamma=[]
    for _ in range(steps):
        s=str(n);nn=n+int(s[::-1])
        gamma.append(len(str(nn))-len(s));n=nn
    got=pairword(n);target=template(J,U,C,q,k+5)
    first=next((i for i,(a,b) in enumerate(zip(got,target)) if a!=b),None)
    if first is None and len(got)!=len(target):first=min(len(got),len(target))
    return first,sum(gamma),got
def check_domains(J,U,C):
    p=template(J,U,C);A=[1<<x for x in template([0]*6,U,C)]
    for i in range(6):A[160+i]=A[-161-i]=FULL
    n=decimal_source(p)
    for t in range(121):
        got=pairword(n)
        assert len(got)==len(A) and all((m>>x)&1 for x,m in zip(got,A)),t
        if t<120:
            A,g=advance(A)
            nn=n+int(str(n)[::-1])
            assert g==len(str(nn))-len(str(n)),t
            n=nn
def main():
    rng=random.Random(1964411);uu=Uwords();rows=[];contain=0
    plans=[(14,100,range(30)),(20,80,[0,1,2,3,10]),
           (40,160,[0,5,10,15,20]),(80,320,[0,9,18,27]),
           (160,640,[0,16])]
    for q,k,indices in plans:
        for idx in indices:
            for C in ([4,4],[4,14,4]):
                J=[rng.randrange(19) for _ in range(6)]
                a,b,p,_,_=run(J,uu[idx],C,q,k)
                x,y,got=big_replay(J,uu[idx],C,q,k)
                if (a,b,p)!=(x,y,got) or x is None:
                    raise RuntimeError(("Independent checker disagreement",q,k,idx,J))
                if q==14 and idx%5==0:
                    check_domains(J,uu[idx],C);contain+=1
                rows.append(dict(q=q,k=k,U=uu[idx],C=C,J=J,mismatch=x,gamma=y))
    with open("independent.json","w") as f:
        json.dump(dict(cases=len(rows),domain_containment_cases=contain,controls=rows),f,indent=2)
    print("PASS",len(rows),"independent big-integer controls;",contain,"full domain-containment controls")
if __name__=="__main__":main()
