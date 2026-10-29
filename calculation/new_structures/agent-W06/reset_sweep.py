#!/usr/bin/env python3
"""Finite p8/m20 0-vs-9 buffer synchronization sweep and independent bigint controls."""
from itertools import product
from random import Random
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
def seed(k,width,value,centre,inner):
 h=B+W*k+[value]*width+W*inner
 p=h+[centre]+h[::-1]
 assert p==p[::-1]
 d=[0]*len(p)
 for i in range(len(p)//2):
  d[i]=min(9,p[i]);d[-1-i]=p[i]-d[i]
 d[len(p)//2]=centre//2
 assert d[0]!=0 and d[-1]!=0
 return d
def step_digits(d):
 n=len(d);c=0;out=[]
 for i in range(n):
  a=d[i]+d[n-i-1]+c
  out.append(a%10);c=a//10
 if c:out.append(c)
 return out
def pair(d):return tuple(x+y for x,y in zip(d,reversed(d)))
def as_int(d):return int(''.join(str(v) for v in reversed(d)))
def bigint_step(n):return n+int(str(n)[::-1])
def sweep():
 good=bad=rules_bad=0
 for k,L,C,inner in product(range(11),range(1,51),range(0,19,2),(0,1,3)):
  d0=seed(k,L,0,C,inner)
  d9=seed(k,L,9,C,inner)
  n0=step_digits(d0);n9=step_digits(d9)
  reset=(pair(n0)==pair(n9))
  predicts=(C>=10 or inner>=1)
  rules_bad+=(reset!=predicts)
  good+=reset;bad+=not reset
  if reset and step_digits(n0)!=step_digits(n9):
   raise AssertionError('same pairword must give same next integer digits')
 assert (good,bad,rules_bad)==(13750,2750,0),(good,bad,rules_bad)
 print(f'COMPUTED reset exhaustive-box cases={good+bad}, success={good}, failure={bad}, classification_discrepancies={rules_bad}')
 r=Random(47406)
 checked=0
 for _ in range(120):
  k=r.randrange(11);L=r.randrange(1,51)
  C=r.randrange(0,19,2);inner=r.choice((0,1,3))
  d0=seed(k,L,0,C,inner);d9=seed(k,L,9,C,inner)
  n0=as_int(d0);n9=as_int(d9)
  assert tuple(map(int,str(n0)[::-1]))==tuple(d0)
  a,b=bigint_step(n0),bigint_step(n9)
  assert (pair(step_digits(d0))==pair(step_digits(d9))) == (pair(tuple(int(ch) for ch in str(a)[::-1])) == pair(tuple(int(ch) for ch in str(b)[::-1])))
  if (C>=10 or inner>=1):assert bigint_step(a)==bigint_step(b)
  checked+=1
 a,b=seed(4,12,0,0,0),seed(4,12,9,0,0)
 assert pair(step_digits(a))!=pair(step_digits(b))
 assert bigint_step(56)==121 and str(bigint_step(56))==str(bigint_step(56))[::-1]
 print(f'Bigint random controls={checked}, expected non-merger and palindrome controls passed')
if __name__=='__main__':sweep()
