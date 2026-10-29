#!/usr/bin/env python3
"""AC45: carry-exact adjacent folded-column ROBDD, NOT pi185 emptiness.
Run: python3 calculation/new_structures/AC45/joined_columns.py
"""
from functools import lru_cache
from itertools import product
from random import Random
import sys
sys.set_int_max_str_digits(30000)
B=(10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5)
W=(5,18,4,8,1,15,4,0,5)

class BDD:
 def __init__(self):self.nodes={};self.unique={}
 def mk(self,bit,a,b):
  if a==b:return a
  k=(bit,a,b)
  if k not in self.unique:
   u=len(self.nodes)+2;self.unique[k]=u;self.nodes[u]=k
  return self.unique[k]
 def stats(self,root,n):
  live=set()
  @lru_cache(None)
  def count(u,lo):
   if u==0:return 0
   if u==1:return 1<<(n-lo)
   bit,a,b=self.nodes[u]
   return (count(a,bit+1)+count(b,bit+1))<<(bit-lo)
  def visit(u):
   if u<2 or u in live:return
   live.add(u);_,a,b=self.nodes[u];visit(a);visit(b)
  visit(root);return count(root,0),len(live)

def transition(xs,outer,g,highs,first=0):
 """Exact shared carry/lag across every neighbouring spatial column."""
 lo,hi,lag=outer;ys=[]
 for j,(x,h) in enumerate(zip(xs,highs)):
  if (x+h)//10!=hi:return None
  a=(x+lo)%10;b=(x+h)%10
  y=a+(1 if first+j==0 and g else b if not g else lag)
  if not 0<=y<=18:return None
  ys.append(y);lo=(x+lo)//10;hi=h;lag=b
 return tuple(ys)

def solve(outer,clock,source,target,first=0):
 """ROBDD over time-major high-carry choices, with spatial joins enforced."""
 width=len(source);depth=len(clock)
 assert len(outer)==depth and len(target)==width and width>0
 bdd=BDD();states=set()
 @lru_cache(None)
 def visit(t,xs):
  states.add((t,xs))
  if t==depth:return int(xs==tuple(target))
  @lru_cache(None)
  def within(j,lo,hi,lag,prefix):
   if j==width:return visit(t+1,prefix)
   x=xs[j];branches=[]
   for h in (0,1):
    if (x+h)//10!=hi:branches.append(0);continue
    a=(x+lo)%10;upper=(x+h)%10
    y=a+(1 if first+j==0 and clock[t] else upper if not clock[t] else lag)
    if not 0<=y<=18:branches.append(0);continue
    branches.append(within(j+1,(x+lo)//10,h,upper,prefix+(y,)))
   return bdd.mk(t*width+j,*branches)
  return within(0,*outer[t],())
 root=visit(0,tuple(source));paths,nodes=bdd.stats(root,depth*width)
 return {'columns':width,'paths':paths,'robdd_nodes':nodes,'reachable_dp_states':len(states)}

def brute(outer,clock,source,target,first=0):
 d={tuple(source):1};width=len(source)
 for t,g in enumerate(clock):
  nd={}
  for xs,mul in d.items():
   for hs in product((0,1),repeat=width):
    ys=transition(xs,outer[t],g,hs,first)
    if ys is not None:nd[ys]=nd.get(ys,0)+mul
  d=nd
 return d.get(tuple(target),0)

def trace(q,k,U=(9,0,18),C=(4,4),J=(5,)):
 H=B+W*q+tuple(J)+tuple(U)*k;p=H+tuple(C)+H[::-1]
 assert len(p)%2==len(C)%2 and (len(p)%2==0 or p[len(p)//2]%2==0)
 ds=[0]*len(p)
 for i in range(len(p)//2):ds[i]=max(0,p[i]-9);ds[-1-i]=p[i]-ds[i]
 if len(p)%2:ds[len(p)//2]=p[len(p)//2]//2
 n=int(''.join(map(str,ds[::-1])));pal_count=0
 for t in range(120):
  digits=tuple(map(int,str(n)[::-1]));pal_count+=digits==digits[::-1]
  pw=tuple(x+y for x,y in zip(digits,digits[::-1]));c=[0];nxt=[]
  for x,y in zip(digits,digits[::-1]):
   z=x+y+c[-1];nxt.append(z%10);c.append(z//10)
  if c[-1]:nxt.append(c[-1])
  z=n+int(str(n)[::-1]);actual=tuple(map(int,str(z)[::-1]))
  assert tuple(nxt)==actual
  g=int(t%4==0);assert len(nxt)-len(digits)==g and c[-1]==g
  highs=tuple(c[len(digits)-1-i] for i in range(4))
  nxtpw=tuple(x+y for x,y in zip(actual,actual[::-1]))
  assert transition(pw[:4],(0,g,-1),g,highs)==nxtpw[:4]
  n=z
 assert pal_count==0
 return True

def main():
 r=Random(452);nchecks=0;positive=0
 for width in (1,2,3,4):
  for depth in (1,2,3,4,5,6):
   for _ in range(60):
    clk=[r.randrange(2) for t in range(depth)]
    ports=[(r.randrange(2),r.randrange(2),r.randrange(10)) for t in clk]
    a=tuple(r.randrange(19) for _ in range(width))
    z=tuple(r.randrange(19) for _ in range(width))
    first=r.randrange(2)
    x=solve(ports,clk,a,z,first)['paths']
    y=brute(ports,clk,a,z,first)
    assert x==y,(width,depth,x,y)
    nchecks+=1;positive+=int(x>0)
 # Planted gamma-one input, with one forbidden and one valid joint carry.
 assert transition((10,4),(0,1,-1),1,(1,0)) is None
 assert transition((10,4),(0,1,-1),1,(0,0)) is not None
 for q,k in ((14,100),(20,120),(40,200),(80,400),(160,800)):
  for U in ((9,0,18),(9,8,10),(18,0,9)):
   for C in ((4,4),(4,14,4)):
    trace(q,k,U,C)
 clk=[int(t%4==0) for t in range(120)]
 ports=[(0,g,-1) for g in clk]
 print('COMPUTED brute-controls',nchecks,'nonzero',positive,'physical-step-controls',30*120)
 for n in (1,2,3,4):print('COMPUTED joined-120',solve(ports,clk,B[:n],B[:n]))
 print('UNDECIDED: the free-J/C 120-layer spatial language is NOT computed')
if __name__=='__main__':main()
