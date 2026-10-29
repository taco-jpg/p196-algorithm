#!/usr/bin/env python3
"""Physical decimal bigint versus independent folded pairword addition."""
import sys
sys.set_int_max_str_digits(0)
B=[10,4,15,4,1,7,9,11,11,18,0,18,6,9,17,4,0,12,0,2,10,1,12,4,2,15,0,13,4,8,4,8,10,15]
W=[4,0,5,5,18,4,8,1,15]
def source(q,k,j,u,c):
 h=B+W*q+j+u*k
 return h+c+h[::-1]
def realize(p):
 d=[0]*len(p)
 for i in range(len(d)//2):
  h=min(9,p[i]);l=p[i]-h
  assert 0<=l<=9
  d[i],d[-1-i]=l,h
 if len(d)%2:
  assert p[len(d)//2]%2==0
  d[len(d)//2]=p[len(d)//2]//2
 assert d[-1]
 return int(''.join(map(str,d[::-1])))
def pair(n):
 d=list(map(int,str(n)[::-1]))
 return [x+y for x,y in zip(d,d[::-1])]
def folded_step(p):
 d=[];carry=0
 for a in p:
  x=a+carry;d.append(x%10);carry=x//10
 if carry:d.append(carry)
 return [x+y for x,y in zip(d,d[::-1])]
def check(q,k,j,u,c):
 p=source(q,k,j,u,c);n=realize(p);assert pair(n)==p
 gamma=[]
 for t in range(120):
  ds=str(n);n+=int(ds[::-1]);gamma.append(len(str(n))-len(ds))
  p=folded_step(p);assert p==pair(n),(q,k,j,u,c,t)
 goal=source(q,k+5,j,u,c)
 i=next((i for i,(x,y) in enumerate(zip(p,goal)) if x!=y),None)
 assert gamma==[1,0,0,0]*30 and i is not None
 return i
if __name__=="__main__":
 cases=[([0]*6,[9,0,18],[4,4]),([0,1,0,0,0,0],[0,18,9],[4,14,4]),([0,18,12,5,6,9],[9,16,2],[4,4]),([0,4,17,10,18,11],[10,8,9],[4,14,4]),([0,16,2,9,18,14],[18,0,9],[4,4]),([0,18,0,0,6,9],[18,9,0],[4,4]),([0,1,2,3,4,5],[9,2,16],[4,14,4]),([0,16,9,2,18,14],[2,16,9],[4,4]),([0,18,12,4,0,1],[16,9,2],[4,14,4])]
 for q,k in [(14,100),(20,80),(40,160),(80,320),(160,640)]:
  for j,u,c in cases:print(q,k,check(q,k,j,u,c))
 print("PASS 45 full true-decimal bigint controls")
