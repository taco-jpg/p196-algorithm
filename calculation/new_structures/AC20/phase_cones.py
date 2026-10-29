#!/usr/bin/env python3
"""Phase-11 finite carry-port cones. No claim of a decimal certificate."""
from verify_independent import Us,W,G
def T(x,c): return int(x+c>=10)
def F(w,g):
 m=len(w);z=0
 for _ in range(2):
  for x in w:z=T(x,z)
 lo=[0]*m;lo[0]=z
 for i in range(1,m):lo[i]=T(w[i-1],lo[i-1])
 z=0
 for _ in range(2):
  for x in reversed(w):z=T(x,z)
 hi=[0]*m;hi[0]=z
 for i in range(m-1,0,-1):hi[i]=T(w[i],hi[(i+1)%m])
 assert all(T(w[i],lo[i])==lo[(i+1)%m] and T(w[i],hi[(i+1)%m])==hi[i] for i in range(m))
 return tuple((w[i]+lo[i])%10 + (((w[i]+hi[(i+1)%m])%10) if not g else ((w[(i-1)%m]+hi[i])%10)) for i in range(m))
def audit(u):
 v=tuple(u);l=r=0
 for t in range(120):
  g=G[(11+t)%12]
  l+=1+int(v[l%3]==9)
  r+=1+int(v[(-r-1)%3]==9)-g
  v=F(v,g)
  assert v.count(9)==1
 assert v==tuple(u)
 return l,r
if __name__=='__main__':
 hist={}
 for u in Us():
  x=audit(u);hist[x]=hist.get(x,0)+1
 assert hist=={(150,119):10,(149,120):10,(151,121):10},hist
 m=34+9*14;w=W
 for t in range(120):
  g=G[(11+t)%12]
  r=0
  while w[(m-35-r)%9]==9:r+=1
  m-=1+r-g
  w=F(w,g)
 assert w==W and m==70,(w,m)
 print('PHASE11_CONES_PASS',hist,'W9_retreat',160-m,'U_gap_min',300-max(a+b for a,b in hist))
