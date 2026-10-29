#!/usr/bin/env python3
"""Carry-difference excursion counts for phase-shifted W/U 120-step clocks."""
from verify import B,W,GAM,U

def T(x,c):return int(x+c>=10)
def F(w,g):
 m=len(w)
 z=0
 for t in range(2):
  for x in w:z=T(x,z)
 lo=[0]*m;lo[0]=z
 for i in range(1,m):lo[i]=T(w[i-1],lo[i-1])
 z=0
 for _ in range(2):
  for x in w[::-1]:z=T(x,z)
 hi=[0]*m;hi[0]=z
 for i in range(m-1,0,-1):hi[i]=T(w[i],hi[(i+1)%m])
 assert all(T(w[i],lo[i])==lo[(i+1)%m] and T(w[i],hi[(i+1)%m])==hi[i] for i in range(m))
 return tuple((w[i]+lo[i])%10+((w[i]+hi[(i+1)%m])%10 if g==0 else (w[(i-1)%m]+hi[i])%10) for i in range(m))

def cones(start,phase):
 w=tuple(start);l=r=0
 for t in range(120):
  g=GAM[(phase+t)%12]
  l+=1+int(w[l%len(w)]==9)
  r+=1+int(w[(-r-1)%len(w)]==9)-g
  w=F(w,g)
 return (l,r,w)
if __name__=='__main__':
 from collections import Counter
 print('U3 phase2 cone counts',Counter(cones(u,2)[:2] for u in U))
 print('W9 phase2 cones',cones(W[2],2))
 print('max U sum',max(sum(cones(u,2)[:2]) for u in U),'protected U gap at k100',300-max(sum(cones(u,2)[:2])for u in U))
 assert all(cones(u,2)[2]==u for u in U)
