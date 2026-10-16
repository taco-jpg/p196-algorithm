"""Exact signed core between complementary decimal 0/9 annuli.

Research reduction only; no existence claim. Width changes pad the high tail;
low end remains fixed. Neutrality survives precisely while prescribed signs do.
"""
import json,random
CLOCK=(1,1,0,0,0,1,0,0,0,0,1)
INCOMING=(0,1,0,0,1,1,0,0,1,1,1)
record=next(r for r in json.load(open('persist_block_neutral_timechange_results.json')) if r['periods']==[1,1,4,5])['accepted'][0]
A=''.join(str(a) for a,b in record['path'])
B=''.join(str(b) for a,b in reversed(record['path']))

def reverse(c,x):
 assert 0<=x<10**c
 return int(str(x).zfill(c)[::-1]) if c else 0

def signed_reverse(c,s):
 assert 0<abs(s)<=10**c
 return reverse(c,s-1)-10**c if s>0 else reverse(c,s+10**c)+1

def advance(c,s,h):
 z=s+signed_reverse(c,s)
 return c+h,z

def run(c,C,steps=11):
 s=C-10**c;out=[]
 for t in range(steps):
  old=(c,s);c,s=advance(c,s,CLOCK[t%11])
  good=s!=0 and (s>0)==(INCOMING[t%11]==0)
  out.append((old,c,s,good))
  if not good:break
 return out

def check_actual(c,C,m=30,steps=22):
 n=int(A+'9'*m+str(C).zfill(c)+'0'*m+B) if c else int(A+'9'*m+'0'*m+B)
 w=len(B)+m;s=C-10**c;passed=0
 for t in range(steps):
  L=len(str(n));digits=list(map(int,str(n)[::-1]));car=[0]
  for j in range(L):car.append((digits[j]+digits[L-1-j]+car[-1])//10)
  a=car[w];b=car[w+c]
  assert a==INCOMING[t%11],(c,C,t,'a',a)
  assert car[-1]==CLOCK[t%11]
  z=s+signed_reverse(c,s)
  assert (b==1-a)==(z!=0 and (z>0)==(a==0)),(c,C,t,'survival',a,b,z)
  if b!=1-a:return passed
  n+=int(str(n)[::-1]);c+=CLOCK[t%11]
  Cnext=(n//10**w)%10**c
  snext=Cnext+1 if a==0 else Cnext-10**c
  assert snext==z,(c,C,t,'map',snext,z)
  s=z;passed+=1
 return passed

if __name__=='__main__':
 hist={};best=[];record=0
 for c in range(6):
  for C in range(10**c):
   k=check_actual(c,C)
   assert k==sum(row[-1] for row in run(c,C,22))
   hist[k]=hist.get(k,0)+1
   if k>record:record=k;best=[(c,C,k)];print('record',record,c,C,flush=True)
   elif k==record:best.append((c,C,k))
 print('hist',hist,'record',record,'best',best[:20])
 with open('persist_arithmetic_signed_core_results.json','w') as f:json.dump(dict(histogram=hist,record=record,best=best),f,indent=2)
