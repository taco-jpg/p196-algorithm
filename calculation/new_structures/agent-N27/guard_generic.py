#!/usr/bin/env python3
"""Exhaustive control for the arbitrary-base moving saturated centre local lemma."""
from itertools import product
def norm(seq,c,b):
 out=[]
 for x in seq:
  v=x+c
  out.append(v%b)
  c=v//b
 return out,c
def central_run(word,digit):
 n=len(word)
 l=(n-1)//2
 r=n//2
 if word[l]!=digit or word[r]!=digit:return 0
 while l>0 and word[l-1]==digit:l-=1
 while r+1<n and word[r+1]==digit:r+=1
 return r-l+1
def check():
 count=0
 hist={(0,0):0,(0,1):0,(1,0):0,(1,1):0}
 for b in range(2,21):
  maximal=2*(b-1)
  for q in range(3,9):
   for n in range(0,3):
    for L in product(range(maximal+1),repeat=n):
     if L and L[-1]==maximal:continue
     C=list(L)+[maximal]*q+list(L[::-1])
     for e1,gamma in product((0,1),repeat=2):
      D,e2=norm(C,e1,b)
      c=norm(L,e1,b)[1]
      if gamma:
       y=(b-1)*(1-e2)
       nxt=[a+z for a,z in zip(D+[y],[y]+D[::-1])]
      else:
       nxt=[a+z for a,z in zip(D,D[::-1])]
      expected=q-gamma-2*(1-gamma)*(1-c)
      got=central_run(nxt,maximal)
      assert got==expected,(b,q,L,e1,gamma,c,got,expected)
      hist[(c,gamma)]+=1
      count+=1
 assert count==255816
 print("GENERIC PASS",count,"cases bases 2..20",hist)
if __name__=="__main__":check()
