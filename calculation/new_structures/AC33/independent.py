#!/usr/bin/env python3
"""Independent Python bignum step and exact coefficient return check, AC33."""
import sys,json
sys.set_int_max_str_digits(0)
B=(10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5)
W=(5,18,4,8,1,15,4,0,5)
Us=((9,0,18),(9,8,10),(9,16,2))
Cs=((4,4),(4,14,4))
def pair(q,k,J,U,C):
 h=list(B)+list(W)*q+list(J)+list(U)*k
 return h+list(C)+h[::-1]
def realize(p):
 d=[0]*len(p)
 for i in range(len(p)//2):
  a=min(9,p[i]);d[i]=p[i]-a;d[-1-i]=a
 if len(p)%2:d[len(p)//2]=p[len(p)//2]//2
 assert 0<d[-1]<=9
 return int(''.join(map(str,d[::-1])))
def getpair(n):
 s=str(n)
 return [int(a)+int(b) for a,b in zip(s[::-1],s)]
def test(ui,ci,J,q=14,k=100):
 U=Us[ui];C=Cs[ci];n=realize(pair(q,k,J,U,C))
 gamma=[];pal_time=-1
 for t in range(120):
  s=str(n)
  if s==s[::-1] and pal_time<0:pal_time=t
  n+=int(s[::-1])
  gamma.append(len(str(n))-len(s))
 got=getpair(n);wanted=pair(q,k+5,J,U,C)
 first=next((i for i,(x,y) in enumerate(zip(got,wanted)) if x!=y),None)
 if first is None and len(got)!=len(wanted):first=min(len(got),len(wanted))
 return {"q":q,"k":k,"J":J,"U":ui,"C":ci,"gamma":''.join(map(str,gamma)),
         "growth":sum(gamma),"first_mismatch":first,"returning":got==wanted,
         "palindrome_at":pal_time,"endpoint_length":len(got)}
if __name__=="__main__":
 for ui in range(3):
  for ci in range(2):
   for J in ([0,0,0,0,0,0],[0,0,1,2,3,4],[0,0,18,18,18,18]):
    print(json.dumps(test(ui,ci,J)))
