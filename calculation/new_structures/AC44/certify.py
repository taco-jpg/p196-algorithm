#!/usr/bin/env python3
"""Sound set-valued carry enclosure: ALL decimal J words, endpoint-only.
No intermediate W9-preservation assumption and no finite-sample inference.
"""
import json, argparse, time
from lab import B,W,template
FULL=(1<<19)-1
def bits(mask):
    while mask:
        lb=mask&-mask
        yield lb.bit_length()-1
        mask-=lb
TR={}
for m in [1<<i for i in range(19)]+[FULL]:
    for c in (1,2,3):
        dm=cm=0
        for b in bits(m):
            for ci in (0,1):
                if c&(1<<ci):
                    z=b+ci
                    dm|=1<<(z%10)
                    cm|=1<<(z//10)
        TR[(m,c)]=(dm,cm)
def advance(P):
    digits=[];carry=1
    for p in P:
        r=TR.get((p,carry))
        if r is None:
            dm=cm=0
            for b in bits(p):
                for ci in (0,1):
                    if carry&(1<<ci):
                        z=b+ci
                        dm|=1<<(z%10)
                        cm|=1<<(z//10)
            r=dm,cm
        d,carry=r
        digits.append(d)
    if carry==3:
        raise ValueError("Ambiguous overflow; no sound certification possible")
    gamma=int(carry==2)
    if gamma:digits.append(1<<1)
    reverse=digits[::-1];cached={};out=[]
    for a,b in zip(digits,reverse):
        key=(a,b);v=cached.get(key)
        if v is None:
            v=0
            for x in bits(a):
                for y in bits(b):v|=1<<(x+y)
            cached[key]=v
        out.append(v)
    return out,gamma
def Uwords():
    return sorted({tuple(([9,a,18-a][i:]+[9,a,18-a][:i]))
                   for a in range(0,19,2) for i in range(3)})
def certify(U,C,q=14,k=100,steps=120,jlen=6,j0=None):
    J=[0]*jlen
    if j0 is not None:
        if not 0<=j0<=18:raise ValueError("J0 outside 0..18")
        J[0]=j0
    P=[1<<x for x in template(J,U,C,q,k)]
    cut=len(B)+len(W)*q
    for i in range(jlen):
        if i==0 and j0 is not None:continue
        P[cut+i]=P[-1-cut-i]=FULL
    gamma=[]
    for _ in range(steps):
        P,g=advance(P)
        gamma.append(g)
    target=template(J,U,C,q,k+5)
    forbidden=set(range(cut,cut+jlen))|set(range(len(target)-cut-jlen,len(target)-cut))
    if len(P)!=len(target):
        return dict(U=U,C=C,jlen=jlen,q=q,k=k,return_possible=False,
                    reason="different length",gamma="".join(map(str,gamma)))
    witness=next(((i,x,m.bit_count()) for i,(m,x) in enumerate(zip(P,target))
                  if i not in forbidden and not (m&(1<<x))),None)
    return dict(U=U,C=C,jlen=jlen,q=q,k=k,J0=j0,
                return_possible=witness is None,first_forced_mismatch=witness,
                gamma="".join(map(str,gamma)),sum_gamma=sum(gamma),
                undetermined_sites=sum(v.bit_count()>1 for v in P))
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--q",type=int,default=14);p.add_argument("--k",type=int,default=100)
    p.add_argument("--jlen",type=int,default=6);p.add_argument("--j0",type=int)
    p.add_argument("--out",default="census.json")
    a=p.parse_args()
    start=time.monotonic()
    data=[certify(u,c,a.q,a.k,120,a.jlen,a.j0) for u in Uwords()
          for c in ([4,4],[4,14,4])]
    with open(a.out,"w") as f:json.dump({"results":data},f,indent=2)
    excluded=sum(not x["return_possible"] for x in data)
    print("RESULTS",len(data),"obstructions",excluded,"elapsed",round(time.monotonic()-start,2))
    if excluded!=60:raise SystemExit("INCONCLUSIVE: not all pairs excluded")
    print("WITNESSES",[(x["U"],len(x["C"]),x.get("first_forced_mismatch")) for x in data])
if __name__=="__main__":main()
