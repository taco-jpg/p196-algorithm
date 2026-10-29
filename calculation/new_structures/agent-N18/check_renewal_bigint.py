#!/usr/bin/env python3
"""Independent ordinary-Python-big-integer 88-step decimal renormalisation checks."""
import random,sys
sys.set_int_max_str_digits(0)
a=[list(map(int,line.split())) for line in open('lattice.txt') if line.strip()]
assert len(a)==47
B=[x[0] for x in a[:39]];W=a[39]
def seed(P):
 assert P==P[::-1]
 n=len(P);d=[0]*n
 for i in range(n//2):
  d[i]=min(9,P[i]);d[n-1-i]=P[i]-d[i]
 if n%2:
  assert P[n//2]%2==0
  d[n//2]=P[n//2]//2
 assert d[-1]>0
 return int(''.join(map(str,d[::-1])))
def step88(P):
 n=seed(P)
 for _ in range(88):
  s=str(n);n+=int(s[::-1])
 s=str(n);d=list(map(int,s[::-1]))
 return [d[i]+d[len(d)-1-i] for i in range(len(d))]
def randcore(L,r):
 h=[r.randrange(19) for _ in range(L//2)]
 return h+([2*r.randrange(10)] if L%2 else [])+h[::-1]
r=random.Random(180474)
cases=[[],[0],[18],[0,0],[18,18],[0,0,0],[18,18,18],[8,0,0,16,0,0,8]]
for L in range(8):
 for _ in range(30):cases.append(randcore(L,r))
for i,C in enumerate(cases):
 out=[]
 for q in (1,2,3):
  p=B+W*q
  z=step88(p+C+p[::-1]);pad=B+W*(q-1)
  assert z[:len(pad)]==pad and z[-len(pad):]==pad[::-1],(i,q)
  D=z[len(pad):len(z)-len(pad)]
  assert len(D)==len(C)+84
  out.append(D)
 assert out[0]==out[1]==out[2],i
C=[8,0,0,16,0,0,8];p=B+W
R=step88(p+C+p[::-1])[39:-39]
assert len(R)==91 and R[:20]==W and R[-20:]==W[::-1]
D=R[20:-20];assert len(D)==51
assert step88(p+D+p[::-1])[39:59]!=W
print('PASS 248 independent decimal big-integer cases q=1,2,3; W-renewal witness validated')
