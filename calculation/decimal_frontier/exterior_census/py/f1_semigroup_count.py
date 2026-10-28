#!/usr/bin/env python3
"""Exact first-coordinate F1 cyclic overflow necklace counts.
Boolean-relation semigroup + Burnside for necklaces; Moebius for primitive words.
A necessary filter only: counts do NOT assert existence of an exterior B-cycle.
"""
from collections import Counter, deque
from functools import lru_cache
from math import gcd
import json, sys

def divisors(n):
    return [d for d in range(1,n+1) if n%d==0]
def phi(n):
    return sum(gcd(n,j)==1 for j in range(1,n+1))
def mu(n):
    if n==1:return 1
    r=1;f=2
    while f*f<=n:
        if n%f==0:
            n//=f;r=-r
            if n%f==0:return 0
            while n%f==0:n//=f
        f+=1
    return -r if n>1 else r

def count(b,pmax):
    ns=2*b-2
    edges=[]
    for g in (0,1):
        row=[]
        for x in range(1,ns+1):
            mask=0
            for c in (0,1):
                if (x+c)//b!=g:continue
                y=x%b+(1 if g else (x+c)%b)
                if 1<=y<=ns:mask|=1<<(y-1)
            row.append(mask)
        edges.append(tuple(row))
    def compose(row,other):
        out=[]
        for mask in row:
            q=0
            while mask:
                bit=mask&-mask;mask-=bit
                q|=other[bit.bit_length()-1]
            out.append(q)
        return tuple(out)
    def closed(row):
        return any((mask>>i)&1 for i,mask in enumerate(row))
    ident=tuple(1<<i for i in range(ns))
    seen={ident:0};queue=deque([ident])
    while queue:
        r=queue.popleft()
        for g in (0,1):
            q=compose(r,edges[g])
            if q not in seen:seen[q]=seen[r]+1;queue.append(q)
    if b==10:assert len(seen)==434 and max(seen.values())==17
    print('relation states',len(seen),'max shortest depth',max(seen.values()),file=sys.stderr)
    @lru_cache(None)
    def power_closed(row,k):
        acc=ident;x=row
        while k:
            if k&1:acc=compose(acc,x)
            k//=2
            if k:x=compose(x,x)
        return closed(acc)
    dp={ident:{0:1}}
    hist={0:dp}
    for p in range(1,pmax+1):
        nxt={}
        for row,weights in dp.items():
            for g in (0,1):
                t=compose(row,edges[g]);dest=nxt.setdefault(t,{})
                for w,c in weights.items():dest[w+g]=dest.get(w+g,0)+c
        dp=nxt;hist[p]=dp
    @lru_cache(None)
    def fixed(d,k):
        c=Counter()
        for row,byw in hist[d].items():
            if power_closed(row,k):c.update(byw)
        return c
    out=[]
    for p in range(1,pmax+1):
        burn=Counter();primitive=Counter()
        for k in divisors(p):
            for w,c in fixed(p//k,k).items():
                burn[k*w]+=phi(k)*c
                primitive[k*w]+=mu(k)*c
        assert all(v%p==0 for v in burn.values())
        assert all(v%p==0 for v in primitive.values())
        weights={str(k):v//p for k,v in sorted(burn.items()) if v}
        primweights={str(k):v//p for k,v in sorted(primitive.items()) if v}
        assert all(v>=0 for v in primweights.values())
        out.append({'p':p,'b':b,'f1_necklaces':sum(weights.values()),
                    'f1_primitive_necklaces':sum(primweights.values()),
                    'byG':weights,'primitiveByG':primweights,
                    'relation_states':len(hist[p])})
    return out

if __name__=='__main__':
    base=int(sys.argv[1]) if len(sys.argv)>1 else 10
    last=int(sys.argv[2]) if len(sys.argv)>2 else 60
    dest=sys.argv[3] if len(sys.argv)>3 else 'f1_b10_p1_60.json'
    rows=count(base,last)
    with open(dest,'w') as f:json.dump(rows,f,indent=2)
    for z in rows:print(z['p'],z['f1_necklaces'],z['f1_primitive_necklaces'])
    print('saved',dest)
