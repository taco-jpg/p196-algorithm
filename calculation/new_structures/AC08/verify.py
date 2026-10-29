#!/usr/bin/env python3
"""Independent decimal-bigint controls for AC08 centre-only scans."""
import random
import sys
sys.set_int_max_str_digits(0)
B=(10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5)
W=(5,18,4,8,1,15,4,0,5)
US=((9,14,4),(14,4,9),(4,9,14))
def template(u,c,q,k):
 h=(*B,*(W*q),5,*(u*k))
 return (*h,*c,*h[::-1])
def realize(p):
 n=len(p);digits=[0]*n
 for i in range(n//2):
  digits[i]=max(0,p[i]-9)
  digits[n-1-i]=min(9,p[i])
 if n%2:
  assert p[n//2]%2==0
  digits[n//2]=p[n//2]//2
 assert digits[-1]
 return int("".join(map(str,digits[::-1])))
def control(uid,c,q=14,k=100):
 p=template(US[uid],c,q,k)
 n=realize(p);gamma=[]
 for _ in range(120):
  s=str(n)
  nxt=n+int(s[::-1])
  gamma.append(len(str(nxt))-len(s))
  n=nxt
 s=str(n);digits=[int(x) for x in s[::-1]]
 got=[digits[i]+digits[-1-i] for i in range(len(digits))]
 expected=template(US[uid],c,q,k+5)
 middle=len(expected)//2; radius=122+len(c)+30
 first=next((i-middle for i in range(middle-radius,middle+radius+1)
             if got[i]!=expected[i]),None)
 return first, ''.join(map(str,gamma)),got==expected
if __name__=="__main__":
 random.seed(271828)
 for uid in range(3):
  for length in range(7,15):
   half=[random.randrange(19) for _ in range(length//2)]
   c=tuple(half+([2*random.randrange(10)] if length%2 else [])+half[::-1])
   baseline=control(uid,c)
   assert baseline[1]=="1000"*30
   for q,k in ((20,80),(40,160),(80,320),(160,640)):
    check=control(uid,c,q,k)
    assert check[0]==baseline[0] and check[1]==baseline[1]
 print("PASS 24 controls across five widths")
