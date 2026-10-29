#!/usr/bin/env python3
"""Independent Python unbounded-integer phase-7 reverse-and-add controls."""
import sys,random,json
sys.set_int_max_str_digits(0)
B=[5,2,7,12,0,3,14,15,5,9,0,9,3,4,18,11,9,15,9,10,14,10,5,12,0,17,9,16,1,14,1,14,4,17]
W=[11,9,12,2,9,2,4,0,17]
def make(J,U,C,q,k):
 h=B+W*q+list(J)+list(U)*k
 return h+list(C)+h[::-1]
def realize(p):
 n=len(p);d=[0]*n
 for i in range(n//2):
  hi=min(9,p[i]);d[i]=p[i]-hi;d[-i-1]=hi
 if n%2:d[n//2]=p[n//2]//2
 assert d[-1]>0
 z=0
 for x in reversed(d):z=10*z+x
 return z
def check(J,U,C,q=14,k=100):
 p=make(J,U,C,q,k);n=realize(p)
 ds=list(map(int,str(n)[::-1]))
 assert [a+b for a,b in zip(ds,ds[::-1])]==p
 gam=0
 for t in range(120):
  s=str(n);n+=int(s[::-1]);gam+=len(str(n))-len(s)
 ds=list(map(int,str(n)[::-1]))
 out=[a+b for a,b in zip(ds,ds[::-1])]
 target=make(J,U,C,q,k+5)
 assert len(out)==len(target)
 first=next((i for i,(a,b) in enumerate(zip(out,target)) if a!=b),None)
 return dict(q=q,k=k,first=first,gamma=gam,exact=out==target)
if __name__=="__main__":
 rng=random.Random(2807)
 Js=[[0]*5,[18]*5,[1,2,3,4,5],[5,10,0,18,9],[rng.randrange(19) for _ in range(5)]]
 Us=[[9,0,18],[18,0,9],[9,8,10],[16,9,2],[9,18,0]]
 for J,U in zip(Js,Us):
  for C in ([4,4],[4,14,4]):
   rows=[check(J,U,C,q,k) for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]]
   assert all(x["gamma"]==30 and x["first"] is not None for x in rows)
   assert all(x["first"]-rows[0]["first"]==9*(x["q"]-14) for x in rows)
 print("PASS 50 independent BigInt trajectories")
