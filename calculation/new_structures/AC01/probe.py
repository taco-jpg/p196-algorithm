#!/usr/bin/env python3
import sys,itertools
sys.set_int_max_str_digits(100000)
B=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W=[5,18,4,8,1,15,4,0,5]
US=[(9,0,18),(0,18,9),(18,9,0)]
def templ(q,k,J,U,C):
 h=B+W*q+J+list(U)*k;return h+C+h[::-1]
def realize(p):
 n=len(p);d=[0]*n
 for i in range(n//2):
  hi=min(9,p[i]);d[i]=p[i]-hi;d[n-1-i]=hi
 if n%2:
  assert p[n//2]%2==0;d[n//2]=p[n//2]//2
 assert d[-1]!=0
 return d
def step(d):
 n=len(d);o=[];carry=0
 for i in range(n):
  s=d[i]+d[-1-i]+carry;carry=s//10;o.append(s%10)
 if carry:o.append(carry)
 return o
def pair(d):return [d[i]+d[-1-i] for i in range(len(d))]
def run(q,k,J,U,C,steps=120,check=False):
 p=templ(q,k,J,U,C);d=realize(p);g=[]
 for i in range(steps):
  if check:assert pair(d)==pair(d)[::-1]
  nd=step(d);g.append(len(nd)-len(d));d=nd
 want=templ(q,k+5,J,U,C);got=pair(d);same=got==want
 diff=next((i for i,(a,b) in enumerate(zip(got,want)) if a!=b),min(len(got),len(want)))
 return dict(same=same,length=len(got),wantlength=len(want),first=diff,center=got[len(got)//2-12:len(got)//2+12],wanted=want[len(want)//2-12:len(want)//2+12],gamma=''.join(map(str,g)),sumgamma=sum(g))
if __name__=='__main__':
 for U in US:
  for C in [[4,0,2,10,2,0,4],[2]*8,[0,2,4,6,8,8,6,4,2,0]]:
   x=run(14,100,[5],U,C)
   print('U',U,'C',C,'first',x['first'],'center',x['center'],'wanted',x['wanted'],'clock',x['sumgamma'])
