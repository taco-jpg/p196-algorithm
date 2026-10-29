#!/usr/bin/env python3
import sys,random
sys.set_int_max_str_digits(0)
L=(7,12,16,10,7,4,12,8,15,13,17,1,17,18,16,3,5,0,2,12,18,10,1)
PH=(8,16,14,10,2,4)
F={8:16,16:14,14:10,10:2,2:4,4:8}
def seed(k,left=L):
 return ''.join(str(x-x//2) for x in left)+'4'*(2*k)+''.join(str(x//2) for x in left[::-1])
def pair(s):return [int(a)+int(b) for a,b in zip(s[::-1],s)]
def shape(p,x):
 l=(len(p)-1)//2;r=len(p)//2
 while l>=0 and r<len(p) and p[l]==x and p[r]==x:l-=1;r+=1
 w=r-l-1;return tuple(p[:(len(p)-w)//2]),w
def step(p):
 d=[];c=0
 for x in p:d0=(x+c)%10;c=(x+c)//10;d.append(d0)
 if c:d.append(c)
 return [d[i]+d[-1-i] for i in range(len(d))]
def insert(p,x):
 m=len(p)//2
 return p[:m]+([x,p[m],x] if len(p)%2 else [x,x])+p[m+1 if len(p)%2 else m:]
def main():
 rng=random.Random(2026102809);n=0
 for x in PH:
  for parity in (0,1):
   for size in range(8):
    for _ in range(200):
     cap=[rng.randrange(19) for i in range(size)]
     if cap and cap[0]==0:cap[0]=rng.randrange(1,19)
     p=cap+[x]*(6+parity)+cap[::-1]
     assert step(insert(p,x))==insert(step(p),F[x])
     n+=1
 print('central-pump identity random exact checks:',n)
 ref={}
 for k in (28,29,35,80):
  s=seed(k)
  for t in range(37):
   cap,w=shape(pair(s),PH[t%6])
   assert w>6,(k,t,w)
   if t<=24:
    assert any(a%2 for a in cap),(k,t,'missing odd')
    sig=(cap,w-2*k)
    if t not in ref:ref[t]=sig
    else:assert ref[t]==sig,(k,t,'counter-dependent cap')
   if t<36:s=str(int(s)+int(s[::-1]))
 for t,b in {0:0,1:0,2:-1,3:-1,4:8,5:8,6:8,12:5,18:2,24:1}.items():
  assert ref[t][1]==b,(t,b,ref[t][1])
 print('t,beta,cap-width:',[(t,ref[t][1],len(ref[t][0])) for t in (0,4,6,12,18,24)])
 badcap=(7,12,14,0,6);s=seed(28,badcap)
 for _ in range(5):s=str(int(s)+int(s[::-1]))
 assert s==s[::-1]
 print('negative palindrome safety-control at t=5: PASS')
if __name__=='__main__':main()
