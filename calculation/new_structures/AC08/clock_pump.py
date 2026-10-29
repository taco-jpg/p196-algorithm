#!/usr/bin/env python3
"""AC08: universal-C length clock proof for canonical phase-0 q14/k100/J=[5].

Proof: an arbitrary palindrome centre is overapproximated by ALL^L in
the digit-mask word. A centre insertion of ALL commutes with the abstract
reverse-add step when the odd centre mask is ALL, or when the even
two central masks are ALL. T(ALL,ALL,nonempty carry)=(ALL,{0,1}).
The 121 abstract base-width frames check the pumping precondition.
"""
from functools import lru_cache
from verify import B,W
US=[]
for a in range(0,19,2):
 w=(9,a,18-a)
 US.extend((w,w[1:]+w[:1],w[2:]+w[:2]))
US=tuple(US)
ALL=(1<<10)-1
@lru_cache(None)
def transfer(left,right,carry):
 output=0;newcarry=0
 for a in range(10):
  if left&(1<<a):
   for b in range(10):
    if right&(1<<b):
     for c in (0,1):
      if carry&(1<<c):
       s=a+b+c;output|=1<<(s%10);newcarry|=1<<(s//10)
 return output,newcarry

def source(uid,L):
 h=(*B,*(W*14),5,*(US[uid]*100))
 P=(*h,*(0 for _ in range(L)),*h[::-1])
 n=len(P)
 out=[]
 for i,p in enumerate(P):
  if len(h)<=i<len(h)+L:out.append(ALL)
  elif i<n//2:out.append(1<<max(0,p-9))
  else:out.append(1<<min(9,p))
 return out

def transition(d):
 n=len(d);a=[0]*n;carry=1
 for i in range(n):a[i],carry=transfer(d[i],d[n-i-1],carry)
 if carry==2:a.append(1<<1)
 elif carry!=1:raise AssertionError("ambiguous overflow carry %s"%carry)
 return a,carry==2

def central_full(d):
 m=len(d)//2
 return d[m]==ALL and (len(d)%2 or d[m-1]==ALL)

def trace(uid,L):
 d=source(uid,L);clock=[];frames=[]
 for t in range(121):
  assert central_full(d),(uid,L,t)
  frames.append(d)
  if t<120:
   d,g=transition(d);clock.append(int(g))
 return frames,clock

def insert_middle(d):
 m=len(d)//2
 return d[:m]+[ALL]+d[m:]

if __name__=="__main__":
 for c in (1,2,3):
  assert transfer(ALL,ALL,c)==(ALL,3)
 for uid in range(30):
  base,clock=trace(uid,2)
  assert ''.join(map(str,clock))=="1000"*30
  nextwidth,clock2=trace(uid,3)
  assert clock2==clock
  assert all(insert_middle(x)==y for x,y in zip(base,nextwidth))
  for L in (0,1):
   d=source(uid,L);gamma=[]
   for t in range(120):
    d,g=transition(d);gamma.append(int(g))
   assert ''.join(map(str,gamma))=="1000"*30
  print("U rank",uid+1,"PASS")
 print("PAPER PUMP + FINITE MASK CERTIFICATE PASS: 30 U, all C lengths")
