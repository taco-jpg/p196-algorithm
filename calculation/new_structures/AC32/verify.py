#!/usr/bin/env python3
"""Unbounded Python integer versus independent schoolbook decimal digit-array oracle."""
import sys,json
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
B=[5,2,3,3,3,16,9,7,18,6,0,1,5,8,13,9,18,12,12,8,12,8,17,9,6,14,5,18,14,11,12,11,9,12]
W=[2,9,2,4,0,17,11,9,12]
def realize(p):
 n=len(p);d=[0]*n
 for i in range(n//2):
  hi=min(9,p[i]);d[i]=p[i]-hi;d[n-1-i]=hi
 if n%2:d[n//2]=p[n//2]//2
 assert d[-1]>0 and all(0<=x<=9 for x in d)
 return d
def digits(n):return [int(x) for x in str(n)[::-1]]
def test(J,U,C,q,k):
 H=B+W*q+list(J)+list(U)*k;p=H+list(C)+H[::-1]
 d=realize(p);n=int(''.join(map(str,d[::-1])))
 assert digits(n)==d
 assert [x+y for x,y in zip(d,d[::-1])]==p
 clock=[]
 for step in range(120):
  oldlen=len(d)
  n=n+int(str(n)[::-1]);v=digits(n)
  c=0;nd=[]
  for x,y in zip(d,reversed(d)):
   z=x+y+c;nd.append(z%10);c=z//10
  if c:nd.append(c)
  assert nd==v,(step,nd[:25],v[:25])
  clock.append(len(nd)-oldlen);d=nd
 targetH=B+W*q+list(J)+list(U)*(k+5)
 target=targetH+list(C)+targetH[::-1]
 pair=[a+b for a,b in zip(d,d[::-1])]
 first=next((i for i,(a,b) in enumerate(zip(pair,target)) if a!=b),None)
 if first is None and len(pair)!=len(target):first=min(len(pair),len(target))
 assert len(d)==len(target)
 return dict(q=q,k=k,first_mismatch=first,overflows=sum(clock),outlen=len(d),
             targetlen=len(target),endpoint_equal=pair==target)
if __name__=='__main__':
 cases=[([2,0,0,0,0],[9,0,18],[4,14,4]),
        ([0,0,2,0,0],[18,0,9],[4,14,4]),
        ([18,18,18,18,18],[9,14,4],[4,4]),
        ([0,1,2,3,4],[9,2,16],[4,4])]
 for J,U,C in cases:
  for q,k in [(14,100),(20,20),(40,40),(80,80),(160,160)]:
   ans=test(J,U,C,q,k)
   print(json.dumps(dict(J=J,U=U,C=C,**ans)))
 print('20_INDEPENDENT_INTEGER_VS_DIGIT_ARRAY_120_STEP_REPLAYS_PASSED')
