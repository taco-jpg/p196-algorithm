#!/usr/bin/env python3
"""Exact complete base-10 p=21 spatial-3 row-map census (including superperiods).
This enumerates bulk cycles, NOT exterior-root reachability or a Lychrel seed.
"""
from itertools import product
from collections import Counter
B, M, G = 10, 3, '001001010101001010101'

def phi(row, bit):
    try: z = next(i for i,x in enumerate(row) if x != B-1)
    except StopIteration: return None
    a,d=[0]*M,[0]*M
    a[(z+1)%M]=d[(z-1)%M]=int(row[z]>=B)
    for j in range(1,M):
        i=(z+j)%M; a[(i+1)%M]=(row[i]+a[i])//B
        i=(z-j)%M; d[(i-1)%M]=(row[i]+d[i])//B
    e=[(row[i]+a[i])%B for i in range(M)]
    f=[(row[i]+d[i])%B for i in range(M)]
    return tuple(e[i]+f[(i-bit)%M] for i in range(M))

def independent(row, bit):
    if all(x==B-1 for x in row): return None
    carries=[]
    for backward in (False,True):
        good=[]
        for initial in (0,1):
            c=initial;v=[0]*M
            for j in range(M):
                i=(-j)%M if backward else j
                v[i]=c;c=(row[i]+c)//B
            if c==initial:good.append(v)
        assert len(good)==1
        carries.append(good[0])
    a,d=carries
    e=[(row[i]+a[i])%B for i in range(M)]
    f=[(row[i]+d[i])%B for i in range(M)]
    return tuple(e[i]+f[(i-bit)%M] for i in range(M))

def axis(row):
    return [a for a in range(M) if all(row[i]==row[(a-i)%M] for i in range(M))]

def F(row):
    for c in G:
        row=phi(row,int(c))
        if row is None:break
    return row

def canon(c):
    n=len(c)
    return min(tuple(tuple(c[(t+s)%n][(i+r)%M] for i in range(M))
                     for t in range(n)) for s in range(n) for r in range(M))

nodes=list(product(range(2*B-1),repeat=M))
for row in nodes:
    for bit in (0,1): assert phi(row,bit)==independent(row,bit)
idx={v:i for i,v in enumerate(nodes)}
nxt=[idx[F(row)] if F(row) is not None else -1 for row in nodes]
seen=set();cycles=[]
for i in range(len(nodes)):
    if i in seen:continue
    path=[];pos={};v=i
    while v>=0 and v not in pos and v not in seen:
        pos[v]=len(path);path.append(v);v=nxt[v]
    if v in pos:cycles.append(tuple(nodes[j] for j in path[pos[v]:]))
    seen.update(path)

hits=[c for c in cycles if len(set(c[0]))>1 and axis(c[0])]
for c in hits:
    for start in c:
        for a in axis(start):
            row=start;at=a
            for t in range(len(c)*len(G)):
                bit=int(G[t%len(G)])
                assert at in axis(row)
                assert phi(row,bit)==independent(row,bit)
                row=phi(row,bit);at=(at+bit)%M
            assert row==start and at==a
hist=dict(sorted(Counter(map(len,cycles)).items()))
hithist=dict(sorted(Counter(map(len,hits)).items()))
phasecount=sum(len(axis(row)) for c in hits for row in c)
families={canon(c) for c in hits}
print('all',len(nodes),'defined',sum(x>=0 for x in nxt),'cycles',len(cycles),'hist',hist)
print('primitive-reflective',len(hits),'hist',hithist,'anchored',phasecount,'translation-classes',len(families))
print('independent carry comparisons',2*len(nodes))
assert (len(cycles),hist)==(52,{1:2,2:37,5:6,6:4,8:3})
assert (len(hits),hithist,phasecount,len(families))==(18,{2:15,8:3},54,6)
for c in sorted(families,key=lambda c:(len(c),c)):
    print('family temporal period',len(c)*len(G),'representative row',c[0])
