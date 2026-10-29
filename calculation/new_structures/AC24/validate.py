#!/usr/bin/env python3
import sys,random
from phase3 import U,check,tpl,from_coeff,to_coeff,normalize_pair
from abstract import abstract_step
rng=random.Random(24680)
for n in range(25):
 J=[rng.randrange(19) for _ in range(5)]
 u=U[rng.randrange(30)]
 c=[4,4] if n%2==0 else [4,14,4]
 for q,k in ((14,100),(20,80),(40,160),(80,320),(160,640)):
  p=tpl(3,J,u,c,q,k)
  x=from_coeff(p)
  a=p[:34+9*14]
  gamma=[]
  for t in range(120):
   a,g,_,_=abstract_step(a)
   old=str(x);x+=int(old[::-1]);gamma.append(len(str(x))>len(old))
   phys=to_coeff(x)
   assert phys[:len(a)]==a,(n,q,k,t)
   assert g[0]==g[1]==gamma[-1],(n,q,k,t,g)
  assert len(a)==70 and a==tpl(3,J,u,c,q,k+5)[:70]
 print(f'control {n+1}/25 OK: all five widths, 120 physical steps, per-step abstractions')
print('PASS: 125 physical orbits, 15,000 transitions, every phase checked')
