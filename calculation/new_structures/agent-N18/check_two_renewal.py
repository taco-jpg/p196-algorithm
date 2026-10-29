#!/usr/bin/env python3
"""Independent Python ordinary-bigint reverse/add; no coefficient-normalization engine."""
import sys
sys.set_int_max_str_digits(0)
data=[list(map(int,s.split())) for s in open("lattice.txt") if s.strip()]
assert len(data)==47
columns=data[:39];B=[x[0] for x in columns];W=data[39]
U=[1]*20;U[13]=7;C=[8,0,0]+U+[16]+U[::-1]+[0,0,8]
def digits_seed(P):
 assert P==P[::-1]
 n=len(P);d=[0]*n
 for i in range(n//2):
  d[i]=min(9,P[i]);d[-i-1]=P[i]-d[i]
 d[n//2]=P[n//2]//2
 assert d[-1]==8
 return int(''.join(map(str,d[::-1])))
expected=None
for q in range(1,5):
 a=B+W*q
 N=digits_seed(a+C+a[::-1]);start=len(str(N))
 assert start==125+40*q
 core=[]
 for t in range(265):
  s=str(N)
  assert s!=s[::-1],(q,t,'palindrome')
  digs=list(map(int,s[::-1]))
  P=[digs[i]+digs[len(digs)-1-i] for i in range(len(digs))]
  assert P[:39]==[col[t%8] for col in columns],(q,t,'exterior')
  if t in (0,88,176):
   assert P[:len(a)]==a and P[-len(a):]==a[::-1],(q,t,'renewal')
   core.append(P[len(a):-len(a)])
  if t==264:
   a3=B+W*(q-1)
   assert P[:len(a3)]==a3 and P[-len(a3):]==a3[::-1]
   R=P[len(a3):-len(a3)]
   k=0
   while k<20 and R[k]==W[k]:k+=1
   assert k==8
  if t<264:N+=int(s[::-1])
 assert [len(x) for x in core]==[47,91,135]
 if expected is None:expected=core
 else:assert core==expected,(q,'q-independent cores')
 print(f'q={q} PASS independent 264-step ordinary integer replay; digits {start}->{len(str(N))}, two 88-step renewals')
print('PASS all 4 q values; 0 palindromes; exact 39-column exterior every step')
