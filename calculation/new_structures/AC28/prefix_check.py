#!/usr/bin/env python3
"""Independent two-carry prefix vs ordinary BigInt, every step."""
from bigint_verify import B,W,make,realize
import random,sys
sys.set_int_max_str_digits(0)
def abstract_step(x):
 n=len(x);lo=[];c=0
 for z in x:
  s=z+c;lo.append(s%10);c=s//10
 hs=[];outs=[]
 for entry in (0,1):
  arr=[None]*n;c=entry
  for i in range(n-1,-1,-1):
   s=x[i]+c;arr[i]=s%10;c=s//10
  hs.append(arr);outs.append(c)
 assert outs[0]==outs[1]
 gam=outs[0];new=[]
 for j in range(n):
  a=gam if gam and j==0 else hs[0][j-1] if gam else hs[0][j]
  b=gam if gam and j==0 else hs[1][j-1] if gam else hs[1][j]
  if a!=b:break
  new.append(lo[j]+a)
 return new,gam
def check(J,U,C,k):
 known=B+W*14+list(J)+list(U)*50
 p=make(J,U,C,14,k);N=realize(p)
 assert known==p[:len(known)]
 gamma=0
 for t in range(120):
  old=str(N);N+=int(old[::-1]);after=str(N)
  gam=len(after)-len(old)
  actual=[int(after[-1-i])+int(after[i]) for i in range(len(after))]
  known,g=abstract_step(known);gamma+=g
  assert g==gam and known==actual[:len(known)],(t,g,gam)
 cut=34+9*14
 first=next(i for i in range(cut) if known[i]!=(B+W*14)[i])
 return len(known),first,gamma
if __name__=="__main__":
 rg=random.Random(71828)
 for t in range(12):
  J=[rg.randrange(19) for _ in range(5)]
  a=2*rg.randrange(10);U=[9,a,18-a]
  r=rg.randrange(3);U=U[r:]+U[:r]
  C=[4,4] if t%4==0 else [4,14,4] if t%4==1 else [6,2,8,2,6] if t%4==2 else [4,12,12,4]
  for k in (50,100):check(J,U,C,k)
 print("PASS 2880 independent stepwise BigInt-prefix comparisons")
