#!/usr/bin/env python3
"""Independent arbitrary-precision decimal oracle, not the C++ pairword engine."""
import sys
sys.set_int_max_str_digits(0)
B=(5,2,3,3,3,16,9,7,18,6,0,1,5,8,13,9,18,12,12,8,12,8,17,9,6,14,5,18,14,11,12,11,9,12)
W=(2,9,2,4,0,17,11,9,12)
G=(1,0,0,0,1,0,0,0,1,0,0,0)
def Us():
 return [tuple(w[r:]+w[:r]) for a in range(0,19,2) for w in [[9,a,18-a]] for r in range(3)]
def tpl(q,k,j,u,c):
 h=B+W*q+tuple(j)+tuple(u)*k
 return h+tuple(c)+h[::-1]
def realize(p):
 d=[0]*len(p)
 for i in range(len(p)//2):
  d[i]=max(0,p[i]-9);d[-i-1]=p[i]-d[i]
 if len(p)%2:
  assert p[len(p)//2]%2==0
  d[len(p)//2]=p[len(p)//2]//2
 assert d[-1]>0 and all(0<=x<=9 for x in d)
 return int(''.join(map(str,d[::-1])))
def pair(n):
 d=tuple(map(int,str(n)[::-1]))
 return tuple(d[i]+d[-i-1] for i in range(len(d)))
def replay(q,k,j,u,c):
 n=realize(tpl(q,k,j,u,c))
 for t in range(120):
  s=str(n);n+=int(s[::-1])
  assert len(str(n))-len(s)==G[(11+t)%12]
 observed=pair(n);expected=tpl(q,k+5,j,u,c)
 assert len(observed)==len(expected)
 return next((i for i,(x,y) in enumerate(zip(observed,expected)) if x!=y),-1)
if __name__=='__main__':
 tests=0
 for q,k in ((14,100),(20,100),(40,160),(80,320),(160,640)):
  for j in ((0,0,0),(18,0,18),(17,12,3,8),(18,18,18,18)):
   for rank in (0,9,18,29):
    for c in ((4,14,4),(4,4)):
     d=replay(q,k,j,Us()[rank],c)
     assert 0<=d<34+9*q,(q,k,j,rank,c,d)
     tests+=1
 print('INDEPENDENT_BIGINT_PASS',tests,'trajectories',tests*120,'decimal steps')
