#!/usr/bin/env python3
"""Independent ordinary Python integer reverse-and-add verifier for AC10."""
import random,sys
sys.set_int_max_str_digits(0)
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
US=[[9,18,0],[18,0,9],[0,9,18]]
def templ(U,C,q=14,k=100):
 h=B+W*q+[5]+U*k
 return h+C+h[::-1]
def realize(p):
 n=len(p);d=[0]*n
 for i in range(n//2):
  high=min(9,p[i]);d[i]=p[i]-high;d[n-1-i]=high
 if n%2:d[n//2]=p[n//2]//2
 assert d[-1]>0
 return int(''.join(map(str,d[::-1])))
def pairword(v):
 s=str(v);return [int(s[i])+int(s[-i-1]) for i in range(len(s))]
def folded_step(p):
 c=0;a=[]
 for x in p:
  z=x+c;a.append(z%10);c=z//10
 if c:a.append(c)
 return [a[i]+a[-1-i] for i in range(len(a))]
def audit(U,C,q,k):
 p=templ(U,C,q,k);n=realize(p);clock=[]
 for t in range(120):
  assert pairword(n)==p,(U,C,q,k,t)
  p=folded_step(p)
  s=str(n);n+=int(s[::-1]);clock.append(len(str(n))-len(s))
 assert pairword(n)==p
 assert sum(clock)==30
 return ''.join(map(str,clock))
def main():
 rng=random.Random(20261029);n=0;clocks=set()
 for U in US:
  for sz in (7,8,9,10,11,12,13,14):
   for q,k in ((14,100),(20,80),(40,160),(80,320),(160,640)):
    h=[rng.randrange(19) for _ in range(sz//2)]
    C=h+([2*rng.randrange(10)] if sz&1 else [])+h[::-1]
    clocks.add(audit(U,C,q,k));n+=1
    v=realize(templ(U,C,q,k))
    for t in range(120):v+=int(str(v)[::-1])
    got=pairword(v);want=templ(U,C,q,k+5)
    mid=len(want)//2;r=122+sz+30
    assert len(got)==len(want)
    assert got[mid-r:mid+r+1]!=want[mid-r:mid+r+1]
 print('INDEPENDENT_PYTHON_BIGINT_PASS',n,'controls',len(clocks),'clock(s)')
if __name__=='__main__':main()
