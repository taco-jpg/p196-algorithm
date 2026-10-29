#!/usr/bin/env python3
"""AC06 independent Python bigint checks; not an independent exhaustive census."""
import random,sys
if hasattr(sys,"set_int_max_str_digits"):sys.set_int_max_str_digits(0)
B=(10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5)
W=(5,18,4,8,1,15,4,0,5)
U=((9,10,8),(10,8,9),(8,9,10))
def make(ui,C,q,k,J=(5,)):
 h=B+W*q+J+U[ui]*k
 return h+tuple(C)+h[::-1]
def realize(P):
 assert P==P[::-1]
 d=[0]*len(P)
 for i in range(len(P)//2):
  a=min(9,P[i]);b=P[i]-a;assert 0<=b<=9
  d[i]=b;d[-1-i]=a
 if len(P)%2:
  assert P[len(P)//2]%2==0
  d[len(P)//2]=P[len(P)//2]//2
 assert d[-1]>0
 return int(''.join(map(str,reversed(d))))
def pair(n):
 s=str(n);return tuple(int(x)+int(y) for x,y in zip(s,s[::-1]))
def replay(ui,C,q,k,J=(5,)):
 n=realize(make(ui,C,q,k,J))
 clock=[]
 for t in range(120):
  old=str(n);n+=int(old[::-1]);clock.append(len(str(n))-len(old))
 assert clock==[int(t%4==0) for t in range(120)]
 p=pair(n);desired=make(ui,C,q,k+5,J)
 assert len(p)==len(desired)
 m=len(p)//2;v=len(p)%2
 return p[m-5:m+5+v],desired[m-5:m+5+v]
if __name__=="__main__":
 rng=random.Random(47606);count=0
 for ui in range(3):
  for L in (7,8,9,10,13,14):
   C=[0]*L
   for j in range((L+1)//2):
    d=2*rng.randrange(10) if L%2 and j==L//2 else rng.randrange(19)
    C[j]=C[L-j-1]=d
   for q,k in ((14,100),(20,80),(40,160),(80,320),(160,640)):
    a,b=replay(ui,C,q,k);assert a!=b
    count+=1
 print("PASS",count,"independent bigint width controls")
