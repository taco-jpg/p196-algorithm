#!/usr/bin/env python3
"""Exact finite table for *all* single-site substitutions in a p12/m9 bulk.
External data file is checked in separately in the upstream repository.
Conservative boundary margin m+2 ensures all carry disturbances resynchronize.
"""
from pathlib import Path
import json,sys

def load(path):
 a=list(map(int,Path(path).read_text().split()))
 p,nB,m,b=a[:4]; i=4;g=a[i:i+p];i+=p
 def rows(cnt,width):
  nonlocal i
  v=[a[i+t*width:i+(t+1)*width] for t in range(cnt)];i+=cnt*width
  return v
 W=rows(p,m);cup=rows(p,m);B=rows(p,nB)
 assert i==len(a) and (p,m,b)==(12,9,10)
 return p,nB,m,b,g,W,cup,B

def step(P):
 c=0;v=[]
 for x in P:
  x+=c;v.append(x%10);c=x//10
 if c:v.append(c)
 return [v[i]+v[-1-i] for i in range(len(v))]

path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'data'/'lat_p12m9.txt'
p,nb,m,b,g,W,cup,B=load(path)
assert g==[1,0,0,0]*3
# Every phase has a non-9 symbol per period: carry deviations cannot travel
# farther than m sites once the modified coefficient itself has passed.
assert all(any(x!=9 for x in row) for row in W)
assert all((B[t][0]>=10)==bool(g[t]) for t in range(p))
expected={0:[14,9,13,17,10,6,13,None,14],
          4:[17,10,6,13,None,14,14,9,13],
          8:[13,None,14,14,9,13,17,10,6]}
# Derive overflow-phase candidates directly from carry equations.
for t in (0,4,8):
 assert g[t]==1 and 9 not in W[t]
 for r,q in enumerate(W[t]):
  lowcarry=cup[t][r]
  highcarry=int(W[t][(r+1)%m]>=10)
  candidates=[]
  for a in range(19):
   if a==q: continue
   dl=int(a+lowcarry>=10)-int(q+lowcarry>=10)
   dh=int(a+highcarry>=10)-int(q+highcarry>=10)
   if dl==dh and a-q==9*dl:candidates.append(a)
  want=[expected[t][r]] if expected[t][r] is not None else []
  assert candidates==want,(t,r,candidates,want)
for t in range(p):
 for odd in (0,1):
  for k in (0,1):
   n=400+18*k+odd;h=(n+1)//2
   low=[B[t][x] if x<nb else W[t][(x-nb)%m] for x in range(h)]
   if odd and low[-1]%2:low[-1]-=1
   P=low+low[-2::-1] if odd else low+low[::-1]
   F=step(P)
   for j in range(nb+2*m,h-(m+2)):
    r=(j-nb)%m; q=low[j]
    found=[]
    for a in range(19):
     if q==a:continue
     low2=low.copy();low2[j]=a
     P2=low2+low2[-2::-1] if odd else low2+low2[::-1]
     if step(P2)==F:found.append(a)
    expect=([expected[t][r]] if (t in expected and expected[t][r] is not None) else [])
    assert found==expect,(t,odd,k,j,r,q,found,expect)
  print('CHECKED t',t,'odd',odd,'gamma',g[t], 'kernel=',expected.get(t,[None]*m),flush=True)
print('COMPLETE all phases, odd/even, two lengths, every safe bulk index, replacements 0..18')
