#!/usr/bin/env python3
"""Independent generic-base randomized tests for the all-base W06 synchronization lemma."""
from random import Random
r=Random(600474)
def carry(word,c,b):
 for x in word:c=(x+c)//b
 return c
def norm(word,b):
 d=[];c=0
 for x in word:
  x+=c;d.append(x%b);c=x//b
 if c:d.append(c)
 return d
def pair(word):return [word[i]+word[-1-i] for i in range(len(word))]
count=0
for b in range(2,31):
 for _ in range(250):
  n=r.randint(2,30)
  A=[r.randrange(2*b-1) for _ in range(n)]
  A[0]=r.randrange(b,2*b-1)
  A[-1]=r.randrange(b,2*b-1)
  if carry(A,0,b)!=1 or carry(A[::-1],1,b)!=1:continue
  t=r.choice([1,3,5,7,9,11])
  T=[0]*t
  T[0]=T[-1]=r.randrange(b,2*b-1)
  for i in range(1,t//2):T[i]=T[-1-i]=r.randrange(2*b-1)
  T[t//2]=r.randrange(b)*2
  if t==1:T[0]=T[-1]=2*r.randrange((b+1)//2,b)
  assert T==T[::-1] and carry(T,1,b)==1 and T[0]>=b
  L=r.randrange(1,200)
  p0=A+[0]*L+T+[0]*L+A[::-1]
  pq=A+[b-1]*L+T+[b-1]*L+A[::-1]
  assert p0==p0[::-1] and pq==pq[::-1]
  d0=norm(p0,b);dq=norm(pq,b)
  assert len(d0)==len(dq)==len(p0)+1
  a=len(A);m=len(T)
  expected={a:1,a+L:-1,a+L+m:1,a+2*L+m:-1}
  got={i:x-y for i,(x,y) in enumerate(zip(d0,dq)) if x!=y}
  assert got==expected,(b,A,T,L,got,expected)
  assert pair(d0)==pair(dq)
  assert norm(pair(d0),b)==norm(pair(dq),b)
  count+=1
assert count>5000,count
print(f'COMPUTED generic-base controls: {count} cases in bases 2..30, all four impulses cancel')
