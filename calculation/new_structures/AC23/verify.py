#!/usr/bin/env python3
"""Independent literal decimal-bigint controls, no reuse of scan's step equations."""
import sys,collections
from pathlib import Path
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
LAT=Path(__file__).resolve().parents[2]/'decimal_frontier/lattice_kinks/data/lat_p12m9.txt'
if not LAT.exists(): LAT=Path(__file__).with_name('lat_p12m9.txt')
DATA=list(map(lambda line:list(map(int,line.split())),LAT.read_text().splitlines()))
B=DATA[26:38];W=DATA[2:14]; GAM=DATA[1];
U=sorted(set(tuple([9,a,18-a][r:]+[9,a,18-a][:r])for a in range(0,19,2) for r in range(3)))

def decode(v):
 d=[]
 for i in range(5):d.append(v%19);v//=19
 return d[::-1]

def num_from_pair(p):
 assert p==p[::-1]
 d=[0]*len(p)
 for i in range(len(p)//2):
  d[i]=p[i]-min(9,p[i]);d[-1-i]=min(9,p[i])
 if len(p)%2:d[len(p)//2]=p[len(p)//2]//2
 assert 1<=d[-1]<=9
 return int(''.join(map(str,d[::-1])))

def pair_of_number(n):
 s=str(n)
 return [int(a)+int(b)for a,b in zip(s[::-1],s)]

def step(n):
 s=str(n)
 return n+int(s[::-1])

def check(code,ui,centre,q,k,phase=2,steps=120):
 h=B[phase]+W[phase]*q+decode(code)+list(U[ui])*k
 c=[4,4] if centre==2 else [4,14,4]
 p=h+c+h[::-1]
 n=num_from_pair(p)
 gamma=[]; 
 for t in range(steps):
  before=len(str(n)); n=step(n);gamma.append(len(str(n))-before)
 pp=pair_of_number(n)
 cut=34+9*q
 m=next((i for i in range(cut) if pp[i]!=(B[phase]+W[phase]*q)[i]),cut)
 return m, ''.join(map(str,gamma)),len(pp), pp

if __name__=='__main__':
 hist=collections.Counter()
 for ui in (0,2,11,16,29):
  for centre in (2,3):
   for code in (0,1,19,19**2,19**3,19**4,63,127,1024,777777,2476098):
    m,g,l,pp=check(code,ui,centre,14,100)
    assert g==''.join(str(GAM[(2+t)%12])for t in range(120)),(ui,centre,code,g)
    assert l==len(B[2]+W[2]*14+decode(code)+list(U[ui])*105)*2+len([4,4]if centre==2 else [4,14,4]),l
    hist[m]+=1
  print('U',ui+1,'independent 22 controls passed; mismatch histogram',dict(hist));hist.clear()
 for q,k in ((20,80),(40,160),(80,320),(160,640)):
  m,g,l,pp=check(297,11,2,q,k)
  assert g==''.join(str(GAM[(2+t)%12])for t in range(120))
  print('width q,k=',q,k,'first mismatch cut offset=',m-(34+9*q),'length=',l)
 print('PASS: independent genuine Python bigint engine, phase 2, 120 steps each.')
