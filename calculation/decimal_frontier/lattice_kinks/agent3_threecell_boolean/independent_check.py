#!/usr/bin/env python3
"""Independent schoolbook normalization and de Bruijn parity checker, no model import."""
import random,itertools,collections,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
z=list(map(int,(ROOT/'lat2.txt').read_text().split()))
assert z[:12]==[8,11,48,10,1,0,1,0,1,0,1,0]
W=[z[12+48*t:12+48*(t+1)] for t in range(8)]
E=[sum(1<<m for m in range(512) if (m&b)==m) for b in range(512)]

def normalize(P):
 n=len(P);up=[];down=[]
 for seed in (0,1):
  carry=seed;aa=[]
  for x in P:aa.append(carry);carry=(x+carry)//10
  if carry==seed:up.append(aa)
  carry=seed;dd=[0]*n
  for j in range(n-1,-1,-1):dd[j]=carry;carry=(P[j]+carry)//10
  if carry==seed:down.append(dd)
 assert len(up)==len(down)==1
 a,d=up[0],down[0]
 lo=[(P[j]+a[j])%10 for j in range(n)]
 hi=[(P[j]+d[j])%10 for j in range(n)]
 return lo,hi,a,d

def feat(P):
 _,_,a,d=normalize(P);n=len(P);out=0
 for j in range(n):
  k=(j+1)%n;h=(j+2)%n
  b=(P[j]%2)|((P[k]%2)<<1)|((P[h]%2)<<2)|(a[j]<<3)|(a[k]<<4)|(a[h]<<5)|(d[j]<<6)|(d[k]<<7)|(d[h]<<8)
  out^=E[b]
 return out

def cov(t,P):
 lo,hi,_,_=normalize(P);g=1-t%2;n=len(P)
 N=[lo[j]+hi[(j-g)%n] for j in range(n)]
 v=feat(N)<<(512*((t+1)%8))
 if g:v^=feat(P)<<(512*t)
 return v

def rank(rows):
 piv={}
 for v in rows:
  while v:
   j=(v&-v).bit_length()-1
   if j not in piv:piv[j]=v;break
   v^=piv[j]
 return len(piv)

def nullbasis(piv,n):
 keys=set(piv)
 for j in range(n):
  if j in keys:continue
  v=1<<j
  for k in sorted(keys,reverse=True):
   if (v&piv[k]).bit_count()%2:v^=1<<k
  assert all((v&row).bit_count()%2==0 for row in piv.values())
  yield v

def run():
 rows=[]
 for t in range(8):
  rows.append(cov(t,W[t]))
  for j in range(48):
   for s in (-1,1):
    P=W[t].copy();P[j]+=s
    if 0<=P[j]<=18:rows.append(cov(t,P))
  for j in range(48):
   for s,u in itertools.product((-1,1),repeat=2):
    P=W[t].copy();P[j]+=s;P[(j+1)%48]+=u
    if 0<=P[j]<=18 and 0<=P[(j+1)%48]<=18:rows.append(cov(t,P))
 assert len(rows)==2252 and rank(rows)==814
 rng=random.Random(9396);fp={};gp={}
 for i in range(229):
  P=[rng.randrange(19) for _ in range(48)]
  f=feat(P)
  while f:
   k=(f&-f).bit_length()-1
   if k not in fp:fp[k]=f;break
   f^=fp[k]
  for t in range(8):
   v=cov(t,P)
   while v:
    k=(v&-v).bit_length()-1
    if k not in gp:gp[k]=v;break
    v^=gp[k]
 assert len(fp)==224 and len(gp)==1792
 masks=list(nullbasis(fp,512));assert len(masks)==288 and rank(masks)==288
 # Build a second-order carry graph directly from allowed consecutive triples.
 V=[(p,a,d) for p in range(19) for a in (0,1) for d in (0,1)]
 index={v:i for i,v in enumerate(V)}
 e=[];incoming=[[] for _ in V];outgoing=[[] for _ in V]
 for u,(p,a,d) in enumerate(V):
  for q in range(19):
   for A,D in itertools.product((0,1),repeat=2):
    if A!=(p+a)//10 or d!=(q+D)//10:continue
    v=index[q,A,D];k=len(e);e.append((u,v));outgoing[u].append(k);incoming[v].append(k)
 assert len(e)==1444
 H=[[] for _ in e];total=0
 for v in range(len(V)):
  for i in incoming[v]:
   for j in outgoing[v]:
    u,_=e[i];_,w=e[j]
    p,a,d=V[u];q,A,D=V[v];r,B,F=V[w]
    bits=(p%2)|((q%2)<<1)|((r%2)<<2)|(a<<3)|(A<<4)|(B<<5)|(d<<6)|(D<<7)|(F<<8)
    H[i].append((j,E[bits]));H[j].append((i,E[bits]));total+=1
 assert total==27436
 for mask in masks:
  found=False
  for kap in (0,1):
   potential=[None]*len(e);good=True
   for root in range(len(e)):
    if potential[root] is not None:continue
    potential[root]=0;stack=[root]
    while stack and good:
     u=stack.pop()
     for v,featval in H[u]:
      required=potential[u]^kap^((featval&mask).bit_count()%2)
      if potential[v] is None:potential[v]=required;stack.append(v)
      elif potential[v]!=required:good=False;break
    if not good:break
   if good:found=True;break
  assert found
 counter=json.loads((ROOT/'counterexample.json').read_text())
 k=512*counter['coefficient_phase']+counter['monomial_mask']
 assert all(not((r>>k)&1) for r in rows)
 assert (cov(counter['test_phase'],counter['P'])>>k)&1
 print('INDEPENDENT PASS: digit-normalized 2252 reference rank814 and 229-word global rank1792')
 print('INDEPENDENT PASS: 288 universal masks on 27436 lifted carry edges; explicit physical false positive')
if __name__=='__main__':run()
