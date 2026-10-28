#!/usr/bin/env python3
"""Exact 384-variable rec2 time-dependent carry-correction witness; PAPER PROOF."""
from pathlib import Path
from math import gcd
import sys
def read(path):
 z=list(map(int,Path(path).read_text().split()))
 assert z[:4]==[8,11,48,10] and z[4:12]==[1,0]*4
 data=z[12:];assert len(data)==8*(48+48+11)
 return [data[t*48:(t+1)*48] for t in range(8)],[data[8*48+t*48:8*48+(t+1)*48] for t in range(8)]
def carries(row):
 n=len(row);up=[];dn=[]
 for x in (0,1):
  u=[x]
  for v in row:u.append(int(v+u[-1]>=10))
  if u[-1]==x:up.append(u[:-1])
  d=[0]*n;d[-1]=x
  for i in range(n-1,0,-1):d[i-1]=int(row[i]+d[i]>=10)
  if x==int(row[0]+d[0]>=10):dn.append(d)
 assert len(up)==len(dn)==1
 return up[0],dn[0]
def rowstep(row,g):
 a,d=carries(row);n=len(row)
 if not g:return [2*row[j]+a[j]+d[j]-10*(a[(j+1)%n]+d[(j-1)%n]) for j in range(n)]
 return [row[j]+row[(j-1)%n]+a[j]+d[(j-1)%n]-10*(a[(j+1)%n]+d[(j-2)%n]) for j in range(n)]
def equation(t,P):
 g=1-t%2;A=11 if g else 2;new=rowstep(P,g)
 _,d=carries(P);_,dnext=carries(new);coeff={}
 for j in range(48):
  if d[j]:coeff[t*48+j]=-A*10**j*d[j]
  if dnext[j]:coeff[((t+1)%8)*48+j]=10**j*dnext[j]
 bare=sum(10**j*(new[j]-A*P[j]) for j in range(48))
 return bare,coeff
def change(W,t,j):
 b,c=equation(t,W[t]);P=W[t].copy();P[j]+=1;assert 0<=P[j]<=18
 B,C=equation(t,P)
 return B-b,{k:C.get(k,0)-c.get(k,0) for k in set(C)|set(c) if C.get(k,0)-c.get(k,0)}
def run(data):
 W,cup=read(data)
 for t in range(8):
  assert rowstep(W[t],1-t%2)==W[(t+1)%8]
  assert carries(W[t])[0]==cup[t]
 x,vx=change(W,0,47);y,vy=change(W,2,5);z,vz=change(W,3,5)
 assert x==1-10**48 and vx=={}
 assert y==0 and vy=={148:10**4}
 assert z==-99*10**4 and vz=={148:-2*10**4}
 assert all(2*vy.get(j,0)+vz.get(j,0)==0 for j in set(vy)|set(vz))
 assert gcd(abs(x),abs(2*y+z))==99
 print("PASS: 8 rec2 phases; time-varying 384-variable witness (0,47),(2,5),(3,5)")
 print("WITNESS 1: phase0 position47+1 has bare=1-10^48, coeff=0")
 print("WITNESS 2: 2*(phase2 position5+1)+(phase3 position5+1) has bare=-99*10^4, coeff=0")
 print("gcd(10^48-1,99*10^4)=99; hence M|99")
if __name__=="__main__":
 run(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).with_name("lat2.txt")))
