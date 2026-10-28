#!/usr/bin/env python3
"""Exact 434-relation certificate for decimal F1 power-closure and necklace divisor formula.
Only the position-zero necessary filter is studied, not actual exterior B-cycles.
Run: python3 calculation/decimal_frontier/exterior_census/py/f1_power_closure.py 60
"""
from collections import Counter
from math import gcd
import sys
b=10;n=2*b-2
edges=[]
for g in (0,1):
    row=[]
    for x in range(1,n+1):
        mask=0
        for h in (0,1):
            if (x+h)//b!=g:continue
            y=x%b+(1 if g else (x+h)%b)
            if 1<=y<=n:mask|=1<<(y-1)
        row.append(mask)
    edges.append(tuple(row))
def compose(r,s):
    out=[]
    for m in r:
        z=0
        while m:
            t=m&-m;m-=t;z|=s[t.bit_length()-1]
        out.append(z)
    return tuple(out)
def closed(r):
    return any((m>>i)&1 for i,m in enumerate(r))
I=tuple(1<<i for i in range(n));Z=(0,)*n
ids={I:0};states=[I]
for r in states:
    for g in (0,1):
        s=compose(r,edges[g])
        if s not in ids:ids[s]=len(states);states.append(s)
assert len(states)==434
nexts=[(ids[compose(r,edges[0])],ids[compose(r,edges[1])]) for r in states]
hist=Counter();good=0
for r in states:
    if closed(r):good+=1;continue
    s=r
    for k in range(1,6):
        if s==Z:hist[k]+=1;break
        s=compose(s,r)
    else:raise AssertionError("Non-nilpotent diagonal-free relation")
assert good==176 and sum(hist.values())==258
assert dict(hist)=={1:1,2:251,3:4,4:1,5:1}
# A[p,G] is the number of rooted F1-accepted binary words of length p with G ones.
def root_counts(limit):
    dp={(0,0):1};out=[Counter({0:1})]
    for p in range(1,limit+1):
        nxt={}
        for (j,w),v in dp.items():
            for g,k in enumerate(nexts[j]):
                key=(k,w+g);nxt[key]=nxt.get(key,0)+v
        dp=nxt;C=Counter()
        for (j,w),v in dp.items():
            if closed(states[j]):C[w]+=v
        out.append(C)
    return out
def divisors(m):return [k for k in range(1,m+1) if m%k==0]
def phi(m):return sum(gcd(m,j)==1 for j in range(1,m+1))
def mu(m):
    v=1;f=2
    while f*f<=m:
        if m%f==0:
            m//=f;v=-v
            if m%f==0:return 0
            while m%f==0:m//=f
        f+=1
    return -v if m>1 else v
def counts(limit):
    A=root_counts(limit);out=[]
    for p in range(1,limit+1):
        necklaces=Counter();primitive=Counter()
        for k in divisors(p):
            for w,c in A[p//k].items():
                necklaces[w*k]+=phi(k)*c
                primitive[w*k]+=mu(k)*c
        assert all(v%p==0 for v in necklaces.values())
        assert all(v%p==0 for v in primitive.values())
        N={str(w):v//p for w,v in sorted(necklaces.items()) if v}
        P={str(w):v//p for w,v in sorted(primitive.items()) if v}
        assert all(v>=0 for v in P.values())
        out.append((p,sum(N.values()),sum(P.values()),N,P))
    return out
if __name__=="__main__":
    limit=int(sys.argv[1]) if len(sys.argv)>1 else 60
    out=counts(limit)
    print("states",len(states),"self-loop",good,"nilpotent",sum(hist.values()),
          "nilpotency-index",sorted(hist.items()))
    if limit>=60:
        assert out[35][1:3]==(351150,350924)
        assert out[39][1:3]==(1943815,1943363)
        assert out[59][1:3]==(11425283484,11425255386)
    # Independent earlier Burnside program keeps the power condition explicit.
    from f1_semigroup_count import count
    other=count(10,limit)
    for (p,N,P,byG,primitiveByG),row in zip(out,other):
        assert N==row["f1_necklaces"] and P==row["f1_primitive_necklaces"]
        assert byG==row["byG"] and primitiveByG==row["primitiveByG"]
    print("all p<=%s weights and primitive counts equal independent Burnside results"%limit)
