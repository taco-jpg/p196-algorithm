#!/usr/bin/env python3
"""Independent digit-array cone comparison, a diagnostic not a proof of T12."""
import random
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
U=[[9,8,10],[8,10,9],[10,9,8]]
def run(ui,c):
 h=B+W*14+[5]+U[ui]*100;p=h+c+h[::-1]
 n=len(p);d=[0]*n
 for i in range(n//2):
  high=min(9,p[i]);d[i]=p[i]-high;d[-1-i]=high
 if n%2:d[n//2]=p[n//2]//2
 for t in range(120):
  out=[];carry=0
  for a,b in zip(d,reversed(d)):
   v=a+b+carry;out.append(v%10);carry=v//10
  if carry:out.append(carry)
  d=out
 return [d[i]+d[-i-1] for i in range(len(d))]
rng=random.Random(50);count=0
for ui in range(3):
 for L in range(7,15):
  base=run(ui,[0]*L);mid=len(base)//2;low=mid-170;high=mid+170
  for _ in range(10):
   c=[0]*L
   for j in range(L//2):c[j]=c[-j-1]=rng.randrange(19)
   if L%2:c[L//2]=2*rng.randrange(10)
   got=run(ui,c)
   assert len(got)==len(base)
   assert all(got[i]==base[i] for i in range(len(base)) if not low<=i<high)
   count+=1
print('PASS centre cone diagnostic',count,'physical decimal trajectories')
