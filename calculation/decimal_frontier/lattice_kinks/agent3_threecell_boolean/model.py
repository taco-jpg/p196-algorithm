#!/usr/bin/env python3
"""Exact rec2 3-cell 512-Boolean-feature cyclic pairword model."""
from pathlib import Path
from itertools import product
ROOT=Path(__file__).resolve().parent
raw=list(map(int,(ROOT/'lat2.txt').read_text().split()))
assert raw[:12]==[8,11,48,10,1,0,1,0,1,0,1,0]
W=[raw[12+48*t:12+48*(t+1)] for t in range(8)]
EVAL=[sum(1<<m for m in range(512) if (m&bits)==m) for bits in range(512)]

def carries(P):
 n=len(P);asc=[];desc=[]
 assert n==48 and all(0<=x<=18 for x in P) and any(x!=9 for x in P)
 for seed in (0,1):
  a=[seed]
  for x in P:a.append(int(x+a[-1]>=10))
  if a[-1]==seed:asc.append(a[:-1])
  d=[0]*n;d[-1]=seed
  for j in range(n-1,0,-1):d[j-1]=int(P[j]+d[j]>=10)
  if seed==int(P[0]+d[0]>=10):desc.append(d)
 assert len(asc)==len(desc)==1
 return asc[0],desc[0]

def step(P,g):
 a,d=carries(P);n=len(P)
 if g==0:return [2*P[j]+a[j]+d[j]-10*(a[(j+1)%n]+d[(j-1)%n]) for j in range(n)]
 return [P[j]+P[(j-1)%n]+a[j]+d[(j-1)%n]-10*(a[(j+1)%n]+d[(j-2)%n]) for j in range(n)]

def feature(P):
 a,d=carries(P);n=len(P);v=0
 for j in range(n):
  k=(j+1)%n;h=(j+2)%n
  bits=(P[j]&1)|((P[k]&1)<<1)|((P[h]&1)<<2)|(a[j]<<3)|(a[k]<<4)|(a[h]<<5)|(d[j]<<6)|(d[k]<<7)|(d[h]<<8)
  v^=EVAL[bits]
 return v

def covariance(t,P):
 v=feature(step(P,1-t%2))<<(512*((t+1)%8))
 if t%2==0:v^=feature(P)<<(512*t)
 return v

def tags():
 for t in range(8):
  yield (t,-1,0,0)
  for j in range(48):
   for s in (-1,1):
    if 0<=W[t][j]+s<=18:yield (t,j,s,0)
  for j in range(48):
   for s,u in product((-1,1),repeat=2):
    if 0<=W[t][j]+s<=18 and 0<=W[t][(j+1)%48]+u<=18:yield (t,j,s,u)

def tagged(tag):
 t,j,s,u=tag;P=W[t].copy()
 if j>=0:
  P[j]+=s
  if u:P[(j+1)%48]+=u
 return covariance(t,P)

def add(piv,v):
 while v:
  k=v.bit_length()-1
  if k in piv:v^=piv[k]
  else:piv[k]=v;return True
 return False

def rank(vs):
 piv={}
 for v in vs:add(piv,v)
 return len(piv)

def kernel(piv,n):
 keys=set(piv)
 for free in range(n):
  if free in keys:continue
  v=1<<free
  for k in sorted(keys):
   if (v&piv[k]).bit_count()%2:v^=1<<k
  assert all((v&row).bit_count()%2==0 for row in piv.values())
  yield v
