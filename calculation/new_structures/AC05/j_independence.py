#!/usr/bin/env python3
"""Independent physical bigint check: central 10-pairword collar is junction-independent."""
import random,sys
sys.set_int_max_str_digits(0)
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
Us=[[9,8,10],[8,10,9],[10,9,8]]
def state(u,c,J,q,k):
    h=B+W*q+J+Us[u]*k;p=h+c+h[::-1];d=[0]*len(p)
    for i in range(len(p)//2):
        high=min(9,p[i]);d[i]=p[i]-high;d[-1-i]=high
    if len(p)&1:d[len(p)//2]=p[len(p)//2]//2
    n=int(''.join(map(str,d[::-1])))
    for t in range(120):n+=int(str(n)[::-1])
    d=list(map(int,str(n)[::-1]));mid=len(d)//2
    return tuple(d[i]+d[len(d)-1-i] for i in range(mid-10,mid+10))
rng=random.Random(0xAC05);trials=0
for u in range(3):
 for L in range(7,15):
  for trial in range(3):
   c=[0]*L
   for j in range((L+1)//2):
    v=2*rng.randrange(10) if (L&1 and j==L//2) else rng.randrange(19)
    c[j]=c[-1-j]=v
   for q,k in ((14,100),(20,80),(40,160)):
    baseline=state(u,c,[5],q,k)
    for J in ([0],[17,18],[5,4,2,13,0,3],[0]*7):
     assert state(u,c,J,q,k)==baseline
     trials+=1
print('PASS junction-independent 10-pairword collar, independent bigint controls=',trials)
