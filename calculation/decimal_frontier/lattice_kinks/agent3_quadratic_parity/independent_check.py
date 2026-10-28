#!/usr/bin/env python3
"""Independent cyclic digit-normalization and Boolean rank checker, no model import."""
from pathlib import Path
import json,random
HERE=Path(__file__).resolve().parent
x=[int(v) for v in (HERE/'lat2.txt').read_text().split()]
assert x[:4]==[8,11,48,10] and x[4:12]==[1,0]*4
z=x[12:];rows=[z[48*t:48*(t+1)] for t in range(8)]
ident=[1,6,40,80,16640,33280,2162688,9240,1179672]
def cyclic_digits(P):
 n=len(P);up=[];down=[]
 for seed in (0,1):
  a=seed;vals=[]
  for v in P:vals.append(a);a=(v+a)//10
  if a==seed:up.append(vals)
  d=seed;vals=[0]*n
  for j in range(n-1,-1,-1):vals[j]=d;d=(P[j]+d)//10
  if d==seed:down.append(vals)
 assert len(up)==len(down)==1
 a=up[0];d=down[0]
 lo=[(P[j]+a[j])%10 for j in range(n)]
 hi=[(P[j]+d[j])%10 for j in range(n)]
 return lo,hi,a,d
def local_feature(P):
 _,_,a,d=cyclic_digits(P);n=len(P);acc=[0]*22
 for j in range(n):
  k=(j+1)%n
  bits=[P[j]&1,P[k]&1,a[j],d[j],a[k],d[k]]
  vals=[1]+bits+[bits[u]&bits[v] for u in range(6) for v in range(u+1,6)]
  for k,v in enumerate(vals):acc[k]^=v
 return sum(v<<k for k,v in enumerate(acc))
def cov(t,P):
 l,h,_,_=cyclic_digits(P);g=1-t%2
 after=[l[j]+h[(j-g)%48] for j in range(48)]
 out=local_feature(after)<<(22*((t+1)%8))
 if g:out^=local_feature(P)<<(22*t)
 return out
def row(tag):
 t,j,s,u=tag;P=rows[t].copy()
 if j>=0:
  P[j]+=s
  if u:P[(j+1)%48]+=u
 return cov(t,P)
def gf2rank(vectors):
 piv={}
 for n in vectors:
  while n:
   b=(n&-n).bit_length()-1
   if b not in piv:piv[b]=n;break
   n^=piv[b]
 return len(piv)
def run():
 tags=[tuple(t) for t in json.loads((HERE/'rank_witness.json').read_text())]
 assert len(tags)==104 and gf2rank(row(t) for t in tags)==104
 assert gf2rank(ident)==9
 identity_m=[v<<(22*t) for t in range(8) for v in ident]
 assert gf2rank(identity_m)==72
 for tag in tags:
  r=row(tag)
  assert all((r&v).bit_count()%2==0 for v in identity_m)
 all_tags=[]
 for t in range(8):
  all_tags.append((t,-1,0,0))
  for j in range(48):
   all_tags.extend((t,j,s,0) for s in (-1,1) if 0<=rows[t][j]+s<=18)
  for j in range(48):
   all_tags.extend((t,j,s,u) for s in (-1,1) for u in (-1,1) if 0<=rows[t][j]+s<=18 and 0<=rows[t][(j+1)%48]+u<=18)
 assert len(all_tags)==2252 and gf2rank(row(t) for t in all_tags)==104
 rng=random.Random(483196)
 for trial in range(10000):
  P=[rng.randrange(19) for _ in range(48)]
  _,_,a,d=cyclic_digits(P)
  assert all(not((1-(P[j]&1))*(a[(j+1)%48]^d[(j-1)%48])) for j in range(48))
  assert sum(a[j]*(1-a[(j+1)%48]) for j in range(48))==sum(d[j]*(1-d[(j+1)%48]) for j in range(48))
  f=local_feature(P)
  assert all((f&e).bit_count()%2==0 for e in ident)
 print('INDEPENDENT PASS: digit-normalized rec2 covariance rank=104 on 104 witnesses and all 2252 tests')
 print('INDEPENDENT PASS: 9 independent identity masks, 72-dimensional zero-function kernel')
 print('CONTROLS: 10,000 cyclic rows satisfy even-site carry equality and exact ascending/descending carry-run counts')
if __name__=='__main__':run()
