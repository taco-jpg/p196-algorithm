#!/usr/bin/env python3
"""W06 symbolic four-impulse carry synchronizer checks. The theorem proof is in report."""
from itertools import product
from random import Random
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
def carr(w,c):
 for p in w:c=(p+c)//10
 return c
for x in (0,1):
 assert carr(B,x)==1 and carr(W,x)==1
 assert carr(B[::-1],x)==1 and carr(W[::-1],x)==1
assert B[-1]==W[-1]==13 and W[0]==17
def normalize(p):
 d=[];c=0
 for x in p:
  s=x+c;d.append(s%10);c=s//10
 if c:d.append(c)
 return d
def pair(d):
 n=len(d)
 return [d[i]+d[n-1-i] for i in range(n)]
def build(k,j,L,C,u):
 a=B+W*k
 mid=W*j+[C]+(W[::-1])*j
 p=a+[u]*L+mid+[u]*L+a[::-1]
 assert p==p[::-1] and len(p)%2==1
 return p,len(a),len(mid)
def verify(k,j,L,C,independent=False):
 p0,a,t=build(k,j,L,C,0)
 p9,_,_=build(k,j,L,C,9)
 d0=normalize(p0);d9=normalize(p9)
 n=len(p0)
 assert len(d0)==len(d9)==n+1
 if j>=1 or C>=10:
  expected={a:1,a+L:-1,a+L+t:1,a+2*L+t:-1}
  differences={i:v-w for i,(v,w) in enumerate(zip(d0,d9)) if v!=w}
  assert differences==expected,(k,j,L,C,differences,expected)
  assert pair(d0)==pair(d9)
  assert normalize(pair(d0))==normalize(pair(d9))
 else:
  assert pair(d0)!=pair(d9)
  assert pair(d0)[a]-pair(d9)[a]==1
 if independent:
  from sys import set_int_max_str_digits
  set_int_max_str_digits(1000000)
  def split(P):
   n=len(P);D=[0]*n
   for i in range(n//2):D[i]=min(P[i],9);D[n-1-i]=P[i]-D[i]
   D[n//2]=P[n//2]//2
   return int(''.join(str(x) for x in D[::-1]))
  def R(x):return x+int(str(x)[::-1])
  x,y=split(p0),split(p9)
  assert list(map(int,str(R(x))[::-1]))==d0
  assert list(map(int,str(R(y))[::-1]))==d9
  assert (R(R(x))==R(R(y)))==(j>=1 or C>=10)
if __name__=='__main__':
 count=0
 for k,j,L,C in product(range(11),range(4),range(1,51),range(0,19,2)):
  verify(k,j,L,C);count+=1
 r=Random(474006)
 for i in range(300):
  k=r.randrange(0,201);j=r.randrange(0,51);L=r.randrange(1,501)
  C=r.randrange(0,10)*2
  verify(k,j,L,C,independent=(i<30))
 print('COMPUTED: 22000 exact bounded cases, 300 large random cases, 30 independent bigint pairs; all all-length-theorem regressions passed')
