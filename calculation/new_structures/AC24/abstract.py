#!/usr/bin/env python3
"""Carry-universal outer-prefix propagation for any palindromic pairword completion.
P coefficients 0..18, symmetric. All possible carry-in values at high-side cut {0,1}
are considered, then only their longest common output prefix is retained.
"""
from phase3 import B,W

def norm(p,carry=0):
 d=[]
 for a in p:
  z=a+carry
  d.append(z%10)
  carry=z//10
 return d,carry

def abstract_step(prefix):
 lo,_=norm(prefix,0)
 cand=[]
 gam=[]
 for c in (0,1):
  hi,top=norm(prefix[::-1],c)
  hi=hi[::-1]
  g=top
  gam.append(g)
  x=[]
  for i in range(len(lo)):
   upper=hi[i] if g==0 else (1 if i==0 else hi[i-1])
   x.append(lo[i]+upper)
  cand.append(x)
 length=0
 for a,b in zip(*cand):
  if a!=b:break
  length+=1
 return cand[0][:length],tuple(gam),length,(cand[0][length] if length<len(prefix) else None,cand[1][length] if length<len(prefix) else None)

def run(phase,q=14,k=100,verbose=True):
 prefix=B[phase]+W[phase]*q
 target=prefix
 first_mismatch=None
 gamma=[];lens=[len(prefix)];amb=[]
 for t in range(1,121):
  prefix,gs,L,bd=abstract_step(prefix)
  gamma.append(gs)
  lens.append(L)
  if gs[0]!=gs[1]:amb.append(('clock',t,gs))
  if not prefix:break
  if verbose and (t%10==0 or t<=12 or t==120):print(t,L,gs,bd,prefix[:10])
 if prefix:
  idx=next((i for i,(a,b) in enumerate(zip(prefix,target)) if a!=b),None)
 else:idx=None
 print('FINAL phase',phase,'q',q,'forced length',len(prefix),'first mismatch',idx,'clock ambiguous',amb[:3], 'clock', ''.join(str(x[0]) for x in gamma[:12]))
 if idx is not None:print('proof witness',idx,prefix[idx],target[idx])
 return prefix,gamma,lens,idx
if __name__=='__main__':
 for phase in (0,1,2,3):run(phase,verbose=False)
 run(3)
