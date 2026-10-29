#!/usr/bin/env python3
"""Agent X16 exact arithmetic controls. No decimal infinity claim."""
import sys,json,argparse
sys.set_int_max_str_digits(0)
def tm(x):return x.bit_count()&1
def pairs(d):return [d[i]+d[-1-i] for i in range(len(d))]
def direct(d,b=10):
 c=0;out=[]
 for x,y in zip(d,reversed(d)):
  s=x+y+c;out.append(s%b);c=s//b
 if c:out.append(c)
 return out
def norm(p,b=10):
 c=0;out=[];cs=[0]
 for x in p:
  s=x+c;out.append(s%b);c=s//b;cs.append(c)
 if c:out.append(c)
 return out,cs
def split(p,b=10):
 assert p==p[::-1] and p[0]>0
 n=len(p);d=[0]*n
 for i in range(n//2):
  hi=min(b-1,p[i]);d[i]=p[i]-hi;d[n-1-i]=hi
 if n%2:
  assert p[n//2]%2==0
  d[n//2]=p[n//2]//2
 return d
def seed(a,b,k):
 n=2*k+8
 return split([a if tm(min(i,n-1-i))==0 else b for i in range(n)])
def latch(maxk):
 for k in range(maxk+1):
  d=seed(9,10,k);n=len(d);h=n//2
  nxt,c=norm(pairs(d))
  assert nxt==direct(d) and c==[0,0]+[1]*(n-1)
  p=[0]*(n+1);p[0]=10
  for i in range(2,h):p[i]=tm(i)+tm(i-1)
  p[h]=2*tm(h-1)
  for i in range(h+1,n+1):p[i]=p[n-i]
  assert pairs(nxt)==p and p[3]==1
  nxt2,c2=norm(p)
  assert nxt2==direct(nxt) and c2==[0,1]+[0]*(n-1)+[1]
  assert pairs(nxt2)[0]==1
  z=direct(nxt2)
  assert z==z[::-1] # carry dies: fourth state palindrome
 return {'tested_k':[0,maxk],'fourth_state_palindrome':True}
B=[8,9,10,13,14,12,3,14,10,0,11,7,10,9,7,8,8,14,15,2,9,7,0,5,8,3,8,11,8,6,8,7,5,14,11,3,9,3,8,14,7,12,8,2,0,12,1,5,13,8,1,16,15,9,1,7,6,2,1,15,15]
W=[1,1,15,15];G=[1,1,0,0,0,1,1,0,0,0]
def control9():
 def word(l):return B+[W[i%4] for i in range(l)]+B[::-1]
 for k in range(50):
  l=10+4*k;d=split(word(l),9)
  for g in G:
   q=direct(d,9);assert norm(pairs(d),9)[0]==q and len(q)-len(d)==g
   d=q;l+=g
  assert pairs(d)==word(l) and l==14+4*k
 return {'lengths':50,'exact_edges':500,'growth_per_cycle':4}
def orbit(d,steps,integer_check=0,require_odd=False):
 pals=0;odd=0;history=[];maxprefix=0
 for t in range(steps+1):
  p=pairs(d);pals+=d==d[::-1];odd+=any(x&1 for x in p)
  if len(history)==8:
   old=history.pop(0)
   pre=next((j for j,(a,b) in enumerate(zip(old,p)) if a!=b),min(len(old),len(p)))
   maxprefix=max(maxprefix,pre)
  history.append(p)
  if t==steps:break
  nxt,_=norm(p);assert nxt==direct(d)
  if t<integer_check:
   v=int(''.join(map(str,reversed(d))))
   assert v+int(str(v)[::-1])==int(''.join(map(str,reversed(nxt))))
  d=nxt
 if require_odd:assert odd==steps+1
 return {'steps':steps,'palindromes':pals,'odd_pair_states':odd,
         'states':steps+1,'final_digits':len(d),
         'independent_integer_edges':integer_check,
         'max_p8_pair_prefix_match':maxprefix}
def main():
 a=argparse.ArgumentParser();a.add_argument('--quick',action='store_true');a.add_argument('--output',default='x16_observations.json');z=a.parse_args()
 steps=300 if z.quick else 20000
 data={'tm_latch':latch(255 if z.quick else 3000),
 'base9_control':control9(),
 'decimal_tm_17_14_k63':orbit(seed(17,14,63),steps,min(1601,steps),not z.quick),
 'decimal_196_reference':orbit([6,9,1],steps)}
 with open(z.output,'w') as f:json.dump(data,f,indent=2)
 print(json.dumps(data,indent=2))
if __name__=='__main__':main()
