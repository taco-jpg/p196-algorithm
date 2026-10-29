#!/usr/bin/env python3
"""Phase-8 protected-insertion carry kernel: shifted T12 equations and controls."""
from pathlib import Path
import sys
if hasattr(sys,"set_int_max_str_digits"):sys.set_int_max_str_digits(0)
T=lambda x,c:int(x+c>=10)
def F(w,g):
 m=len(w);lo=[0]*m;hi=[0]*m;z=0
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
 return [(w[i]+lo[i])%10+((w[i]+hi[(i+1)%m])%10 if not g else (w[(i-1)%m]+hi[i])%10) for i in range(m)],hi
def root_next(p,g,upper):
 m=len(p);low=[];c=0
 for x in p:low.append((x+c)%10);c=T(x,c)
 b=[0]*(m+1);b[m]=upper
 for i in range(m-1,-1,-1):b[i]=T(p[i],b[i+1])
 high=[(p[i]+b[i+1])%10 for i in range(m)]
 return [low[i]+(high[i] if not g else (1 if i==0 else high[i-1])) for i in range(m)]
def realize(P):
 d=[0]*len(P)
 for i in range(len(P)//2):
  hi=min(9,P[i]);d[i]=P[i]-hi;d[-1-i]=hi
 if len(P)%2:d[len(P)//2]=P[len(P)//2]//2
 assert d[-1]>0
 return int(''.join(map(str,d[::-1])))
def make(B,W,J,U,C,q,k):
 H=B+W*q+J+U*k
 return realize(H+C+H[::-1])
def pair(n):
 s=str(n);return [int(x)+int(y) for x,y in zip(s[::-1],s)]
def ins(P,w,c):
 L=len(P);return P[:c]+w+P[c:L-c]+w[::-1]+P[L-c:]
def insertion_control(B,W,Urows,J,C):
 q,k=14,100;base=make(B[8],W[8],J,Urows[0],C,q,k)
 for typ in ("W","U"):
  x=base;y=make(B[8],W[8],J,Urows[0],C,q+(typ=="W"),k+(typ=="U"))
  cut=52 if typ=="W" else 34+9*q+len(J)+165
  for t in range(121):
   row=W[(8+t)%12] if typ=="W" else Urows[t]
   assert pair(y)==ins(pair(x),row,cut),(typ,t)
   if t==120:break
   x=x+int(str(x)[::-1]);y=y+int(str(y)[::-1])
def main():
 path=Path(__file__).resolve().parents[2]/"decimal_frontier/lattice_kinks/data/lat_p12m9.txt"
 a=[list(map(int,s.split())) for s in path.read_text().splitlines()]
 assert a[0]==[12,34,9,10]
 W=a[2:14];B=a[26:38];G=lambda t:int(t%4==0)
 assert B[8][0]==10 and W[8]==[4,0,5,5,18,4,8,1,15]
 for t in range(120):
  i=(8+t)%12;n,hi=F(W[i],G(t))
  assert n==W[(i+1)%12] and root_next(B[i],G(t),hi[0])==B[(i+1)%12]
 m=34+9*14
 for t in range(120):
  w=W[(8+t)%12];r=0
  while w[(m-35-r)%9]==9:r+=1
  m-=1+r-G(t)
 assert m==68 # Phase-8 W loss=92, insertion at cut52 is protected.
 controls=0;Lmax=Rmax=0
 for aa in range(0,19,2):
  for rot in range(3):
   v=[9,aa,18-aa];v=v[rot:]+v[:rot];rows=[v]
   for t in range(120):rows.append(F(rows[-1],G(t))[0])
   assert rows[-1]==v and all(w.count(9)==1 for w in rows)
   l=r=0
   for t in range(120):
    w=rows[t];l+=1+int(w[l%3]==9);r+=1+int(w[(-r-1)%3]==9)-G(t)
   assert (l,r)==((152,151,150)[rot],(121,122,120)[rot])
   Lmax=max(l,Lmax);Rmax=max(r,Rmax)
   for C in ([4,14,4],[4,4]):
    insertion_control(B,W,rows,[2,16,0,8,12],C);controls+=2
 assert Lmax<165 and Rmax<135
 print("PASS phase8: W92, U",Lmax,Rmax,"clock (1000)^30, insertion controls",controls)
if __name__=="__main__":main()
