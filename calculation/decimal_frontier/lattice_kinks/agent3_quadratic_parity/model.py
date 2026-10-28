#!/usr/bin/env python3
"""Exact cyclic rec2 quadratic parity/carry feature model (one 48-cell ring)."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
raw=list(map(int,(ROOT/'lat2.txt').read_text().split()))
assert raw[:4]==[8,11,48,10] and raw[4:12]==[1,0]*4
z=raw[12:];W=[z[t*48:(t+1)*48] for t in range(8)]
PAIRS=[(i,j) for i in range(6) for j in range(i+1,6)]
NUM=22
IDENTITY=[1,6,40,80,16640,33280,2162688,9240,1179672]
def carries(P):
 n=len(P);a=[];d=[]
 for seed in (0,1):
  u=[seed]
  for x in P:u.append(int(x+u[-1]>=10))
  if u[-1]==seed:a.append(u[:-1])
  v=[0]*n;v[-1]=seed
  for j in range(n-1,0,-1):v[j-1]=int(P[j]+v[j]>=10)
  if seed==int(P[0]+v[0]>=10):d.append(v)
 assert len(a)==len(d)==1
 return a[0],d[0]
def step(P,g):
 a,d=carries(P);n=len(P)
 if g==0:return [2*P[j]+a[j]+d[j]-10*(a[(j+1)%n]+d[(j-1)%n]) for j in range(n)]
 return [P[j]+P[(j-1)%n]+a[j]+d[(j-1)%n]-10*(a[(j+1)%n]+d[(j-2)%n]) for j in range(n)]
def features(P):
 a,d=carries(P);n=len(P);out=0
 for j in range(n):
  k=(j+1)%n
  bits=[P[j]&1,P[k]&1,a[j],d[j],a[k],d[k]]
  feat=[1]+bits+[bits[i]&bits[k] for i,k in PAIRS]
  for i,x in enumerate(feat):
   if x:out^=1<<i
 return out
def covariance(t,P):
 N=step(P,1-t%2)
 out=features(N)<<(((t+1)%8)*NUM)
 if t%2==0:out^=features(P)<<(t*NUM)
 return out
def all_tests():
 for t in range(8):
  yield (t,-1,0,0)
  for j in range(48):
   for s in (-1,1):
    if 0<=W[t][j]+s<=18:yield (t,j,s,0)
  for j in range(48):
   for s in (-1,1):
    for u in (-1,1):
     if 0<=W[t][j]+s<=18 and 0<=W[t][(j+1)%48]+u<=18:yield (t,j,s,u)
def test_row(tag):
 t,j,s,u=tag;P=W[t].copy()
 if j>=0:
  P[j]+=s
  if u:P[(j+1)%48]+=u
 return covariance(t,P)
def rank(rows):
 piv={}
 for v in rows:
  while v:
   k=v.bit_length()-1
   if k not in piv:piv[k]=v;break
   v^=piv[k]
 return len(piv)
