#!/usr/bin/env python3
"""Independent actual Python bigint plus non-in-place digit-array replay."""
import sys
sys.set_int_max_str_digits(0)
B=[2,11,1,1,11,17,14,3,9,3,0,0,12,13,16,4,9,6,6,4,6,4,8,14,12,16,12,8,17,5,6,5,9,16]
W=[0,9,11,1,10,8,5,9,16]
def source(q,k,J,U,C):
 h=B+W*q+J+U*k
 return h+C+h[::-1]
def digits_from_source(P):
 assert P==P[::-1]
 d=[0]*len(P)
 for i in range(len(P)//2):
  hi=min(9,P[i])
  d[i]=P[i]-hi;d[-1-i]=hi
 if len(P)%2:
  assert P[len(P)//2]%2==0
  d[len(P)//2]=P[len(P)//2]//2
 assert d[-1]>0
 return d
def step(d):
 c=0;out=[]
 for i in range(len(d)):
  z=d[i]+d[-1-i]+c
  out.append(z%10);c=z//10
 if c:out.append(c)
 return out
def pair(d):return [d[i]+d[-1-i] for i in range(len(d))]
def check(q,k,J,U,C):
 P=source(q,k,J,U,C);d=digits_from_source(P)
 n=int(''.join(map(str,d[::-1])))
 gamma=[]
 for t in range(120):
  assert pair(d)==P
  old=len(d);d=step(d)
  n=n+int(str(n)[::-1])
  assert d==list(map(int,str(n)[::-1])),(q,k,t)
  gamma.append(len(d)-old);P=pair(d)
 assert gamma==[0,0,1,0]*30,(q,k,gamma)
 target=source(q,k+5,J,U,C)
 mismatch=next((i for i,(a,b) in enumerate(zip(P,target)) if a!=b),None)
 assert mismatch is not None and 10<=34+9*q-mismatch<=25 and mismatch<34+9*q
 assert P[10]==target[10]==0
 print("BIGINT_PASS",q,k,"J",J,"U",U,"C",C,"first_mismatch",mismatch)
for q,k,J,U,C in [
 (14,100,[1,2,3],[9,0,18],[4,14,4]),
 (14,100,[1,2,3],[9,0,18],[4,4]),
 (20,80,[18,18,18,18],[9,10,8],[4,4]),
 (40,160,[0,0,0],[18,0,9],[4,14,4]),
 (80,320,[17,1,18,0],[9,18,0],[4,4]),
 (160,640,[1,9,10,18],[9,14,4],[4,14,4])
]:check(q,k,J,U,C)
print("AC19_SIX_INDEPENDENT_CONTROLS_PASS")
