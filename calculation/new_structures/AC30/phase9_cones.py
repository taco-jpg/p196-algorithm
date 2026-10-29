#!/usr/bin/env python3
"""Phase-9 T12 carry-front recurrences. Numeric loop checks, not infinite-horizon replay."""
from pathlib import Path
LATTICE=(Path(__file__).with_name('lattice.txt') if Path(__file__).with_name('lattice.txt').exists() else Path(__file__).resolve().parents[2]/'decimal_frontier/lattice_kinks/data/lat_p12m9.txt')
l=[list(map(int,x.split())) for x in LATTICE.read_text().splitlines()]
B,W=l[26:38],l[2:14]
g=lambda t:int((9+t)%4==0)
T=lambda x,c:int(x+c>=10)
def F(w,gamma):
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
 return tuple((w[i]+lo[i])%10+((w[i]+hi[(i+1)%m])%10 if not gamma else (w[i-1]+hi[i])%10) for i in range(m))
if __name__ == "__main__":
 assert all(tuple(W[(9+t+1)%12])==F(W[(9+t)%12],g(t)) for t in range(120))
 m=34+9*14;runs=[]
 for t in range(120):
  r=0
  while W[(9+t)%12][(m-35-r)%9]==9:r+=1
  d=1+r-g(t);m-=d;runs.append(d)
 print('W_ROOT_LOSS',34+9*14-m,'histogram',{d:runs.count(d) for d in set(runs)},'post',m,'cut',52)
 assert 34+9*14-m==92
 for rot in range(3):
  for a in range(0,19,2):
   v=[9,a,18-a];u=tuple(v[rot:]+v[:rot]);seq=[u]
   for t in range(120):seq.append(F(seq[-1],g(t)))
   assert seq[-1]==u
   L=R=0
   for t in range(120):
    ww=seq[t]
    L+=1+int(ww[L%3]==9)
    R+=1+int(ww[(-R-1)%3]==9)-g(t)
   assert (L,R)==[(151,120),(150,121),(152,122)][rot]
   print('U_CONES',rot,a,L,R)
