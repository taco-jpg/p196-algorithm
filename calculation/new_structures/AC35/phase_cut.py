#!/usr/bin/env python3
"""All starting phases of p12/m9 T12 physical insertion and reset-cone proof."""
from pathlib import Path
from random import Random
import sys
sys.set_int_max_str_digits(0)
p=Path(__file__).resolve().parents[2]/"decimal_frontier/lattice_kinks/data/lat_p12m9.txt"
rows=[list(map(int,s.split())) for s in p.read_text().splitlines()]
assert rows[0]==[12,34,9,10] and rows[1]==[1,0,0,0]*3
W,B=rows[2:14],rows[26:38]
T=lambda x,c:int(x+c>=10)
G=lambda t:int(t%4==0)
def F(w,g):
 m=len(w);assert any(x!=9 for x in w)
 lo=[0]*m;hi=[0]*m;z=0
 for _ in range(2):
  for x in w:z=T(x,z)
 lo[0]=z
 for i in range(1,m):lo[i]=T(w[i-1],lo[i-1])
 z=0
 for _ in range(2):
  for x in w[::-1]:z=T(x,z)
 hi[0]=z
 for i in range(m-1,0,-1):hi[i]=T(w[i],hi[(i+1)%m])
 assert all(T(w[i],lo[i])==lo[(i+1)%m] and T(w[i],hi[(i+1)%m])==hi[i] for i in range(m))
 return tuple((w[i]+lo[i])%10+((w[i]+hi[(i+1)%m])%10 if not g else (w[(i-1)%m]+hi[i])%10) for i in range(m))
def candidates():
 for a in range(0,19,2):
  u=(9,a,18-a)
  for rot in range(3):yield u[rot:]+u[:rot]
def radius(p):
 m=160
 for t in range(120):
  r=0
  while W[(p+t)%12][(m-35-r)%9]==9:r+=1
  m-=1+r-G(p+t)
 return 160-m
def uradius(u,p):
 v=u;l=r=0
 for t in range(120):
  l+=1+(v[l%3]==9)
  r+=1+(v[(-r-1)%3]==9)-G(p+t)
  v=F(v,G(p+t))
 assert v==u
 return l,r
def root_next(w,g,upper):
 m=len(w);low=[];c=0
 for x in w:low.append((x+c)%10);c=T(x,c)
 b=[0]*(m+1);b[m]=upper
 for i in range(m-1,-1,-1):b[i]=T(w[i],b[i+1])
 hi=[(w[i]+b[i+1])%10 for i in range(m)]
 return [low[i]+(hi[i] if not g else (1 if i==0 else hi[i-1])) for i in range(m)]
def kernel():
 rad=[]
 for p in range(12):
  g=G(p)
  assert B[p][0]==(10 if g else (1,2,5)[p%4-1])
  assert any(x%2 for x in B[p])
  assert tuple(W[(p+1)%12])==F(tuple(W[p]),g)
  a=B[p]+W[p]*7;b=B[(p+1)%12]+W[(p+1)%12]*7
  for m in range(37,80):
   r=0
   while a[m-1-r]==9:r+=1
   safe=m-1-r+g
   for upper in (0,1):assert root_next(a[:m],g,upper)[:safe]==b[:safe]
  wr=radius(p)
  rr=[uradius(u,p) for u in candidates()]
  assert wr<=93 and max(x for x,y in rr)<=152 and max(y for x,y in rr)<=122
  assert 160-wr>=67>52+9 and 165-152>=13 and 135-122>=13
  rad.append(wr)
 return rad
def source(p,q,k,J,U,C):
 h=B[p]+W[p]*q+list(J)+list(U)*k
 w=h+list(C)+h[::-1];n=len(w);d=[0]*n
 for i in range(n//2):
  a=min(9,w[i]);d[i]=w[i]-a;d[-1-i]=a
 if n%2:
  assert w[n//2]%2==0
  d[n//2]=w[n//2]//2
 assert d[-1]>0
 return int(''.join(map(str,d[::-1])))
def independent(n):
 d=[int(x) for x in str(n)[::-1]];out=[];c=0
 for x,y in zip(d,d[::-1]):
  s=x+y+c;out.append(s%10);c=s//10
 if c:out.append(c)
 return int(''.join(map(str,out[::-1])))
def pair(n):
 s=str(n);return [int(x)+int(y) for x,y in zip(s[::-1],s)]
def insert(p,w,c):
 return p[:c]+list(w)+p[c:len(p)-c]+list(w)[::-1]+p[len(p)-c:]
def controls(p,U,J,C):
 for kind in ("W","U"):
  x=source(p,14,100,J,U,C)
  y=source(p,14+(kind=="W"),100+(kind=="U"),J,U,C)
  cut=52 if kind=="W" else 34+9*14+len(J)+165
  v=U
  for t in range(121):
   w=W[(p+t)%12] if kind=="W" else v
   assert pair(y)==insert(pair(x),w,cut),(p,U,kind,t)
   if t==120:break
   ox,oy=x,y
   x+=int(str(x)[::-1]);y+=int(str(y)[::-1])
   assert x==independent(ox) and y==independent(oy)
   assert len(str(x))-len(str(ox))==G(p+t)
   assert len(str(y))-len(str(oy))==G(p+t)
   v=F(v,G(p+t))
if __name__=="__main__":
 print("W-loss phases 0..11:",kernel())
 rng=Random(1204752)
 for p in range(12):
  for i,u in enumerate(candidates()):
   if i not in (0,14,28):continue
   J=tuple(rng.randrange(19) for _ in range((i+p)%7))
   C=(4,14,4) if (i+p)%2 else (4,4)
   controls(p,u,J,C)
 print("PASS: 12 rooted caps, all 12x30 U return loops, 72 full 120-step physical paired-insertion controls")
