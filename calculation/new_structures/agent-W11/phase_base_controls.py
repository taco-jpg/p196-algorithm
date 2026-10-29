#!/usr/bin/env python3
"""Independent b-ary controls for synchronized middle packets. Standard library."""
import sys
sys.set_int_max_str_digits(1000000)
def digits(x,b):
 assert x>0
 ds=[]
 while x:
  x,r=divmod(x,b);ds.append(r)
 return ds
def rev(x,b):
 z=0
 for c in digits(x,b):z=z*b+c
 return z
def nlen(x,b):return len(digits(x,b))
def step(p,s,b):
 E=s[3]+nlen(p[3],b)
 P,S=[0]*4,[0]*4
 for k in range(4):
  j=3-k;terms=[]
  if p[k]:terms.append((p[k],s[k]))
  if p[j]:terms.append((rev(p[j],b),E-s[j]-nlen(p[j],b)))
  a=min(z for _,z in terms)
  P[k]=sum(v*b**(z-a) for v,z in terms);S[k]=a
 return P,S
def pack(p,s,b,q2,delta):
 x=0
 exp=(0,q2,q2+delta,2*q2+delta)
 for k in range(4):
  if p[k]:
   e=exp[k]+s[k]
   assert e>=0
   x+=p[k]*b**e
 for j in range(3):
  if p[j] and p[j+1]:
   assert exp[j]+s[j]+nlen(p[j],b)<=exp[j+1]+s[j+1]
 return x
def run_base(b,steps=90):
 p=[b*7+5,1,0,(b-1)*b+(b-2)];s=[0,2,0,3]
 assert nlen(p[3],b)==2
 q2=450;delta=450
 n=pack(p,s,b,q2,delta)
 phases={-1:0,0:0,1:0};trailing=0
 for t in range(steps+1):
  assert pack(p,s,b,q2,delta)==n,('replay',b,t)
  if t>=1:
   assert p[1]==p[2] and s[1]==s[2],('twins',b,t)
   th=s[3]+nlen(p[3],b)-2*s[1]-nlen(p[1],b)
   assert th in (-1,0,1),('phase',b,t,th)
   assert th!=1 or p[1]%b!=0,('guard',b,t)
   phases[th]+=1;trailing+=int(p[1]%b==0)
  if t==steps:break
  np,ns=step(p,s,b)
  n=n+rev(n,b)
  p,s=np,ns
 return phases,trailing,nlen(n,b)
if __name__=='__main__':
 for b in (2,3,4,9,10,13,16,26):
  hist,trail,L=run_base(b)
  print('PASS base',b,'steps',90,'phases',hist,'trailing_middle_states',trail,'endpoint_digits',L)
 print('ALL MULTIBASE CHECKS PASSED')
