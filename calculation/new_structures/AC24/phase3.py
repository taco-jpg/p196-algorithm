#!/usr/bin/env python3
import random,collections,time,sys
sys.set_int_max_str_digits(0)
B=[
[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5],
[1,5,10,12,13,10,3,7,14,11,4,2,3,9,15,7,9,15,11,14,13,13,14,5,5,13,11,11,9,5,10,10,4,5],
[2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11],
[5,2,3,12,16,2,15,10,9,7,18,8,15,9,1,14,0,3,10,0,17,17,9,3,3,15,8,7,9,4,3,3,9,2]
]
W=[
[5,18,4,8,1,15,4,0,5],
[10,14,13,12,9,7,10,4,5],
[1,10,8,5,9,16,0,9,11],
[4,0,17,11,9,12,2,9,2]
]
U=[[9,a,18-a][r:]+[9,a,18-a][:r] for a in range(0,19,2) for r in range(3)]
def tpl(phase,J,U,C,q,k):
 h=B[phase]+W[phase]*q+list(J)+list(U)*k
 return h+list(C)+h[::-1]
def normalize_pair(P):
 d=[];carry=0
 for x in P:
  v=x+carry;d.append(v%10);carry=v//10
 if carry:d.append(carry)
 return [d[i]+d[-1-i] for i in range(len(d))],bool(carry)
def from_coeff(P):
 d=[0]*len(P)
 for i in range(len(P)//2):
  d[i]=max(0,P[i]-9);d[-1-i]=min(9,P[i])
 if len(P)&1:d[len(P)//2]=P[len(P)//2]//2
 assert d[-1]>0
 return int(''.join(map(str,d[::-1])))
def to_coeff(n):
 s=str(n)
 return [int(s[i])+int(s[-1-i]) for i in range(len(s))]
def check(phase,J,U,C,q=14,k=100,bigint=False):
 p=tpl(phase,J,U,C,q,k)
 t=tpl(phase,J,U,C,q,k+5)
 if bigint:
  n=from_coeff(p)
  gs=[]
  for _ in range(120):
   a=str(n);n+=int(a[::-1]);gs.append(int(len(str(n))>len(a)))
  p=to_coeff(n)
 else:
  gs=[]
  for _ in range(120):p,g=normalize_pair(p);gs.append(g)
 idx=next((i for i in range(min(len(p),len(t))) if p[i]!=t[i]),min(len(p),len(t)))
 return idx,idx==len(t) and len(p)==len(t),sum(gs),len(p),gs
if __name__=='__main__':
 J=[0,1,2,3,4]
 for i in [0,1,2,10,29]:
  for C in ([4,4],[4,14,4]):
   a=check(3,J,U[i],C)
   b=check(3,J,U[i],C,bigint=True)
   print(i,U[i],C,a[:4],b[:4],a[4]==b[4]);assert a==b
