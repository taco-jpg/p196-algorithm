#!/usr/bin/env python3
"""T12: exact conditional all-q,k 120-step pumping lemma; NO decimal certificate.
Run: python3 calculation/new_structures/T12/cut.py
"""
from pathlib import Path
from itertools import product
from random import Random

s=(Path(__file__).resolve().parents[2]/'decimal_frontier/lattice_kinks/data/lat_p12m9.txt').read_text().splitlines()
a=[list(map(int,line.split())) for line in s]
assert a[0]==[12,34,9,10] and a[1]==[1,0,0,0]*3
W=a[2:14];B=a[26:38]
G=lambda t:int(t%4==0)
T=lambda x,c:int(x+c>=10)

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

def root_next(p,g,upper_carry):
 m=len(p);low=[];c=0
 for x in p:low.append((x+c)%10);c=T(x,c)
 b=[0]*(m+1);b[m]=upper_carry
 for i in range(m-1,-1,-1):b[i]=T(p[i],b[i+1])
 high=[(p[i]+b[i+1])%10 for i in range(m)]
 return [low[i]+(high[i] if not g else (1 if i==0 else high[i-1])) for i in range(m)]

def phases(u):
 v=[tuple(u)]
 for t in range(120):v.append(F(v[-1],G(t)))
 return v

def cones(v):
 m=len(v[0]);l=r=0
 for t in range(120):
  w=v[t];l+=1+int(w[l%m]==9);r+=1+int(w[(-r-1)%m]==9)-G(t)
 return l,r

def make(q,k,J,U,C):
 h=B[0]+W[0]*q+list(J)+list(U)*k
 p=h+list(C)+h[::-1];n=len(p);d=[0]*n
 assert p==p[::-1] and (n%2==0 or p[n//2]%2==0)
 for i in range(n//2):d[i]=p[i]-min(9,p[i]);d[n-1-i]=min(9,p[i])
 if n%2:d[n//2]=p[n//2]//2
 assert d[-1]>0 and all(0<=x<=9 for x in d)
 return int(''.join(map(str,d[::-1])))

def pair(n):
 s=str(n);return [int(x)+int(y) for x,y in zip(s[::-1],s)]

def step_digits(n):
 d=list(map(int,str(n)[::-1]));c=0;out=[]
 for x,y in zip(d,d[::-1]):
  v=x+y+c;out.append(v%10);c=v//10
 if c:out.append(c)
 return int(''.join(map(str,out[::-1])))

def ins(p,w,c):
 L=len(p);return p[:c]+list(w)+p[c:L-c]+list(w)[::-1]+p[L-c:]

def main():
 assert all(B[t][0]==(10 if G(t) else (1,2,5)[t%4-1]) for t in range(12))
 assert all(tuple(W[(t+1)%12])==F(tuple(W[t]),G(t)) for t in range(12))
 for t in range(12):
  p=B[t]+W[t]*7;target=B[(t+1)%12]+W[(t+1)%12]*7
  for m in range(37,80):
   cut=p[:m];r=0
   while cut[m-r-1]==9:r+=1
   safe=m-1-r+G(t)
   for c in (0,1):assert root_next(cut,G(t),c)[:safe]==target[:safe]
 m=34+9*14;s0=m
 for t in range(120):
  r=0
  while W[t%12][(m-35-r)%9]==9:r+=1
  m-=1+r-G(t)
 assert s0-m==91
 rnd=Random(120475)
 for aa,rot in product(range(0,19,2),range(3)):
  v=(9,aa,18-aa);U=v[rot:]+v[:rot]
  v=phases(U)
  assert v[-1]==tuple(U) and all(row.count(9)==1 for row in v)
  assert cones(v)==((152,151,150)[rot],(121,122,120)[rot])
  for q,k in ((14,100),(20,160)):
   J=tuple(rnd.randrange(19) for _ in range((q+k+U[0])%7))
   C=(10,) if q==14 else (8,8)
   for typ in ('W','U'):
    x=make(q,k,J,U,C);y=make(q+(typ=='W'),k+(typ=='U'),J,U,C)
    c=52 if typ=='W' else 34+9*q+len(J)+165
    rows=[tuple(z) for z in W]*11 if typ=='W' else v
    for t in range(121):
     assert pair(y)==ins(pair(x),rows[t],c),(U,q,k,typ,t)
     if t==120:break
     xx=x+int(str(x)[::-1]);yy=y+int(str(y)[::-1])
     assert xx==step_digits(x) and yy==step_digits(y)
     assert len(str(xx))-len(str(x))==G(t)
     assert len(str(yy))-len(str(y))==G(t)
     x,y=xx,yy
 print('PASS: 12 rooted ports, all 30 U3 120-cycles, exact W/U cones and 120 genuine block-insertion trajectories.')
 print('THEOREM: Return(q,k) iff Return(14,100) for every q>=14,k>=100 and fixed J,C,U; no witness supplied.')

if __name__=='__main__':main()
