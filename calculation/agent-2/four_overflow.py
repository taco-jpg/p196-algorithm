#!/usr/bin/env python3
# Exact first-coordinate graph overapproximation and period bound check.
from collections import defaultdict
def step(x,g):
    return {(x%10+1) if g else (2*x+h)
            for h in (0,1) if ((x+h>=10) if g else (x+h<10))}
edges=defaultdict(set)
for x in range(1,11):
    curr={x};z=0
    while curr:
        for a in curr:
            for y in step(a,1):edges[x].add((y,z+1))
        curr={y for a in curr for y in step(a,0)}
        z+=1
potential=lambda x:int(x==1)
assert all(n<=4+potential(x)-potential(y)
           for x in range(1,11) for y,n in edges[x])
tight={x:{y for y,n in edges[x] if n==4+potential(x)-potential(y)}
       for x in range(1,11)}
alive=set(range(1,11))
while True:
    nxt={x for x in alive if any(y in alive for y in tight[x])
         and any(x in tight[y] for y in alive)}
    if nxt==alive:break
    alive=nxt
assert alive=={1}
paths=[]
for x0 in range(1,11):
    frontier=[(x0,(),0)]
    for _ in range(4):
        frontier=[(y,seq+(w,),s+w) for x,seq,s in frontier for y,w in edges[x]]
    paths += [(seq,s) for x,seq,s in frontier if x==x0]
M=max(n for seq,n in paths)
assert M==16
assert set(seq for seq,n in paths if n==M)=={(4,4,4,4)}
print("MAX_PERIOD",M,"UNIQUE_GAP_TUPLE",(4,4,4,4))

