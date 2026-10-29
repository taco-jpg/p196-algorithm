#!/usr/bin/env python3
"""Ordinary Python arbitrary-precision integer verification, independent of coefficient dynamics."""
import sys
sys.set_int_max_str_digits(0)
data=[list(map(int,s.split())) for s in open('lattice.txt') if s.strip()]
assert len(data)==47
cols=data[:39];B=[z[0] for z in cols];W=data[39]
U=[1]*40;U[13]=7;U[20]=7;U[30]=6
C=[8,0,0]+U+[16]+U[::-1]+[0,0,8]
def numeric_seed(P):
 assert P==P[::-1]
 d=[0]*len(P)
 for i in range(len(P)//2):
  d[i]=min(9,P[i]);d[-1-i]=P[i]-d[i]
 d[len(P)//2]=P[len(P)//2]//2
 assert d[-1]==8
 return int(''.join(map(str,d[::-1])))
record=None
for q in range(1,5):
 a=B+W*q;N=numeric_seed(a+C+a[::-1]);start=len(str(N))
 assert start==165+40*q
 cores=[]
 for t in range(353):
  s=str(N);assert s!=s[::-1],(q,t,'palindrome')
  d=list(map(int,s[::-1]))
  P=[d[i]+d[len(d)-1-i] for i in range(len(d))]
  assert P[:39]==[z[t%8] for z in cols],(q,t,'exterior')
  if t in (0,88,176,264):
   assert P[:len(a)]==a and P[-len(a):]==a[::-1],(q,t,'renewal')
   cores.append(P[len(a):-len(a)])
  if t==352:
   b=B+W*(q-1)
   assert P[:len(b)]==b and P[-len(b):]==b[::-1]
   r=P[len(b):-len(b)]
   match=0
   while match<20 and r[match]==W[match]:match+=1
   assert match==2 and len(r)==303,(q,match)
  if t<352:N+=int(s[::-1])
 assert [len(c) for c in cores]==[87,131,175,219]
 if record is None:record=cores
 else:assert cores==record,(q,'different core')
 print(f'q={q}: PASS 352 genuine integer steps, {start}->{len(str(N))} digits, 0 palindromes, 3 full band renewals')
print('PASS four independently replayed seeds, every 39-column exterior and all complete pairword templates')
