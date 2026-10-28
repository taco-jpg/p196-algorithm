#!/usr/bin/env python3
"""Independent digit-normalization checker of the generated rec2 certificates."""
from pathlib import Path
from math import gcd
from random import Random
import json
HERE=Path(__file__).resolve().parent
CERTS=Path('/tmp/agent3_rec2_spatial_certificates')
nums=[int(v) for v in (HERE/'lat2.txt').read_text().split()]
assert nums[:4]==[8,11,48,10] and nums[4:12]==[1,0]*4
z=nums[12:];W=[z[t*48:(t+1)*48] for t in range(8)]
def digits(P):
 n=len(P);uc=[];dc=[]
 for seed in (0,1):
  u=seed;U=[]
  for v in P:U.append(u);u=(v+u)//10
  if u==seed:uc.append(U)
  d=seed;D=[0]*n
  for j in range(n-1,-1,-1):D[j]=d;d=(P[j]+d)//10
  if d==seed:dc.append(D)
 assert len(uc)==len(dc)==1
 a=uc[0];d=dc[0]
 L=[(P[j]+a[j])%10 for j in range(n)]
 R=[(P[j]+d[j])%10 for j in range(n)]
 return L,R,d
def sig(t,P):
 gam=1-t%2;mul=11 if gam else 2
 low,high,old=digits(P)
 N=[low[j]+high[(j-gam)%48] for j in range(48)]
 _,_,now=digits(N);out={}
 def add(i,v):
  v=out.get(i,0)+v
  if v:out[i]=v
  elif i in out:del out[i]
 for j in range(48):
  add(((t+1)%8)*48+j,N[j]);add(t*48+j,-mul*P[j])
  add(384+((t+1)%8)*48+j,now[j]);add(384+t*48+j,-mul*old[j])
 return out,N
def eq(tag):
 t,j,s1,s2=tag
 base,_=sig(t,W[t]);r=W[t].copy()
 if j>=0:
  r[j]+=s1
  if s2:r[(j+1)%48]+=s2
 B,_=sig(t,r)
 if j>=0:B={i:B.get(i,0)-base.get(i,0) for i in B.keys()|base.keys()}
 B={i:v for i,v in B.items() if v}
 rhs=-B.pop(0,0)
 return B,rhs
def evaluate(cert,mod):
 nonzero={};rhs=0
 for tag,c in cert:
  row,b=eq(tuple(tag));rhs+=c*b
  for j,v in row.items():nonzero[j]=nonzero.get(j,0)+c*v
 if mod:
  assert all(v%mod==0 for v in nonzero.values())
  return rhs%mod
 assert not any(nonzero.values())
 return rhs
def run():
 for t in range(8):assert sig(t,W[t])[1]==W[(t+1)%8]
 proof=json.loads((CERTS/'int_certificates.json').read_text())
 vals=[]
 for c in proof['certs']:
  r=evaluate(c['coefficients'],None);assert r==c['rhs'];vals.append(r)
 assert gcd(*vals)==396
 mod4=json.loads((CERTS/'mod4_certificate.json').read_text())
 assert evaluate(mod4['terms'],4)==2
 ct=0
 for t in range(8):
  tags=[(t,-1,0,0)]
  for j in range(48):
   tags.extend((t,j,s,0) for s in (-1,1) if 0<=W[t][j]+s<=18)
  for j in range(48):
   tags.extend((t,j,s,u) for s in (-1,1) for u in (-1,1)
     if 0<=W[t][j]+s<=18 and 0<=W[t][(j+1)%48]+u<=18)
  for tag in tags:
   co,b=eq(tag)
   assert (co.get(1,0)+co.get(49,0)-b)%2==0
   assert (sum(v*pow(10,j%48,99) for j,v in co.items() if j<384)-b)%99==0
   ct+=1
 assert ct==2252
 rng=Random(4743196)
 for _ in range(1200):
  P=[rng.randrange(19) for _ in range(48)];L,R,_=digits(P)
  for g in (0,1):
   N=[L[j]+R[(j-g)%48] for j in range(48)]
   for mod in (3,9,11,33,99):
    Q=lambda row:sum(pow(10,j,mod)*v for j,v in enumerate(row))%mod
    assert Q(N)==(11 if g else 2)*Q(P)%mod
 print('INDEPENDENT PASS: two-digit-normalization carry solver checks four integer certificates and mod-4 torsion certificate')
 print('INDEPENDENT PASS: explicit mod-2/mod-99 solutions on 2252 tests; 2400 randomized cyclic controls')
 print('INDEPENDENT MODULUS CLASSIFICATION: all and only M dividing 198')
if __name__=='__main__':run()
