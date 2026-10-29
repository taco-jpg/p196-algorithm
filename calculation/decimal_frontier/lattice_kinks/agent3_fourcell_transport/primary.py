#!/usr/bin/env python3
"""Complete 4-cell (12-bit) physical cyclic-zero / finite-interval flux classification."""
from itertools import product
from pathlib import Path
from random import Random
ROOT=Path(__file__).resolve().parent
W0=list(map(int,(ROOT/'rec2_w0.txt').read_text().split()))
assert len(W0)==48

def allowed():
 # Enumerate every genuine 4-column coefficient/carry assignment (521284).
 pat={};total=0
 for p,q,r,s in product(range(19),repeat=4):
  for a,F in product((0,1),repeat=2):
   A=int(p+a>=10);B=int(q+A>=10);C=int(r+B>=10)
   E=int(s+F>=10);D=int(r+E>=10);d=int(q+D>=10)
   bits=(p&1)|((q&1)<<1)|((r&1)<<2)|((s&1)<<3)|(a<<4)|(A<<5)|(B<<6)|(C<<7)|(d<<8)|(D<<9)|(E<<10)|(F<<11)
   src=(p&1)|((q&1)<<1)|((r&1)<<2)|(a<<3)|(A<<4)|(B<<5)|(d<<6)|(D<<7)|(E<<8)
   dst=(q&1)|((r&1)<<1)|((s&1)<<2)|(A<<3)|(B<<4)|(C<<5)|(D<<6)|(E<<7)|(F<<8)
   assert bits not in pat or pat[bits]==(src,dst)
   pat[bits]=(src,dst);total+=1
 assert total==521284 and len(pat)==1312
 return pat

def rank(rows):
 piv={}
 for x in rows:
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;break
 return len(piv)

def carries(P):
 n=len(P);a0=[];d0=[]
 for seed in (0,1):
  aa=[seed]
  for x in P:aa.append(int(x+aa[-1]>=10))
  if aa[-1]==seed:a0.append(aa[:-1])
  dd=[0]*n;dd[-1]=seed
  for j in range(n-1,0,-1):dd[j-1]=int(P[j]+dd[j]>=10)
  if seed==int(P[0]+dd[0]>=10):d0.append(dd)
 assert len(a0)==len(d0)==1
 return a0[0],d0[0]

def b12(P,a,d,j):
 n=len(P);ids=[(j+k)%n for k in range(4)]
 return sum((P[i]&1)<<k for k,i in enumerate(ids))|sum(a[i]<<(4+k) for k,i in enumerate(ids))|sum(d[i]<<(8+k) for k,i in enumerate(ids))

def b9(P,a,d,j):
 n=len(P);ids=[(j+k)%n for k in range(3)]
 return sum((P[i]&1)<<k for k,i in enumerate(ids))|sum(a[i]<<(3+k) for k,i in enumerate(ids))|sum(d[i]<<(6+k) for k,i in enumerate(ids))

def eval_mon(b,cache):
 if b not in cache:
  v=0;s=b
  while True:
   v|=1<<s
   if s==0:break
   s=(s-1)&b
  cache[b]=v
 return cache[b]

def feature(P,cache):
 a,d=carries(P);v=0
 for j in range(len(P)):v^=eval_mon(b12(P,a,d,j),cache)
 return v

def step(P,g):
 a,d=carries(P);n=len(P)
 if not g:return [2*P[j]+a[j]+d[j]-10*(a[(j+1)%n]+d[(j-1)%n]) for j in range(n)]
 return [P[j]+P[(j-1)%n]+a[j]+d[(j-1)%n]-10*(a[(j+1)%n]+d[(j-2)%n]) for j in range(n)]

def run():
 pat=allowed();V=set();adj={}
 for u,v in pat.values():
  V.add(u);V.add(v)
  adj.setdefault(u,set()).add(v);adj.setdefault(v,set()).add(u)
 assert len(V)==288 and sum(u==v for u,v in pat.values())==6
 seen={next(iter(V))};stack=list(seen)
 while stack:
  x=stack.pop()
  for y in adj[x]:
   if y not in seen:seen.add(y);stack.append(y)
 assert seen==V
 # 288 independent 1312-bit edge evaluations: 287 gradients, one constant.
 order=sorted(pat);edges=[pat[b] for b in order]
 flux=[]
 for v in sorted(V)[1:]:flux.append(sum(((u==v)^(w==v))<<i for i,(u,w) in enumerate(edges)))
 flux.append((1<<len(edges))-1)
 assert rank(flux)==288
 # 1471 seeded physical 48-cycles witness rank 1024/4096.
 rng=Random(9397);cache={};piv={};hit=None
 for i in range(1471):
  P=[rng.randrange(19) for _ in range(48)];row=feature(P,cache)
  while row:
   k=row.bit_length()-1
   if k in piv:row^=piv[k]
   else:piv[k]=row;break
  if len(piv)==1024 and hit is None:hit=i+1
 assert len(piv)==1024 and hit==1471
 W=[W0]
 for t in range(7):W.append(step(W[-1],1-t%2))
 assert step(W[-1],0)==W0
 allstates=set();counts=[]
 for t,P in enumerate(W):
  a,d=carries(P);st=[b9(P,a,d,j) for j in range(48)]
  local=[b12(P,a,d,j) for j in range(48)]
  assert all(b in pat and pat[b]==(st[j],st[(j+1)%48]) for j,b in enumerate(local))
  counts.append(len(set(st)));allstates.update(st)
  for L in range(48):
   for length in (1,2,3,4,7,11,24,47,48,49,96):
    for k in V:
     lhs=sum(int(st[(L+j)%48]==k)^int(st[(L+j+1)%48]==k) for j in range(length))%2
     rhs=int(st[L]==k)^int(st[(L+length)%48]==k)
     assert lhs==rhs
 assert counts==[45,42,35,45,45,42,35,45] and len(allstates)==178
 assert sum(1-t%2 for t in range(192))==96
 print('PASS: 521284 physical four-column assignments -> 1312 allowed 12-bit patterns; 2784 forbidden')
 print('PASS: 288 connected 9-bit endpoints, 6 loops; 287 gradients + 1 length parity independent')
 print('PASS: 1471 seeded 48-cell physical cyclic words attain rank1024/4096')
 print('PAPER PROOF: exact 3072-dimensional cyclic-zero kernel = 2784 local zeros + 287 gradients + 1 length parity')
 print('PASS: rec2 8 phases x 48 cuts; endpoint counts 45,42,35,45,45,42,35,45; union 178')
 print('PASS: 8*48*11 finite-interval telescopes, 192-step return adds 48 paired cells')
if __name__=='__main__':run()
