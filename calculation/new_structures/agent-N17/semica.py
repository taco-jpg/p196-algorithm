#!/usr/bin/env python3
"""Independent folded carry-rule checker; constructs the 8 time rows from 8 literal steps."""
PRE=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
CYC=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
def seed(h):
 lo=[max(0,(PRE[i] if i<39 else CYC[(i-39)%20])-9) for i in range(h)]
 hi=[(PRE[i] if i<39 else CYC[(i-39)%20])-lo[i] for i in range(h)]
 return lo+hi[::-1]
def step(d):
 n=len(d);carry=0;out=[]
 for i in range(n):
  s=d[i]+d[n-1-i]+carry;out.append(s%10);carry=s//10
 if carry:out.append(carry)
 return out,carry
def pair(d):return [d[i]+d[-i-1] for i in range(len(d))]
def rows():
 d=seed(400);a=[];gam=[]
 for t in range(8):
  p=pair(d);a.append(p[:99]);d,g=step(d);gam.append(g)
 assert gam==[1,0,1,0,1,0,1,0]
 for r in a:assert all(r[i]==r[i+20] for i in range(39,79))
 return [r[:59] for r in a],gam
def run():
 arr,gam=rows()
 cell=lambda t,i:arr[t][i if i<59 else 39+(i-39)%20]
 for t in range(8):
  a=[cell(t,i) for i in range(900)]
  L=[0]
  for x in a:L.append((x+L[-1])//10)
  R=[0]*(len(a)+1)
  for i in range(len(a)-1,-1,-1):R[i]=(a[i]+R[i+1])//10
  assert R[0]==gam[t]
  b=[cell((t+1)%8,i) for i in range(700)]
  if gam[t]:
   out=[a[0]-10*L[1]+1]
   out.extend(a[i]+a[i-1]+L[i]+R[i]-10*(L[i+1]+R[i-1]) for i in range(1,700))
  else:out=[2*a[i]+L[i]+R[i+1]-10*(L[i+1]+R[i]) for i in range(700)]
  assert b==out,(t,[(i,out[i],b[i]) for i in range(700) if b[i]!=out[i]][:3])
  assert all(a[i]!=9 or a[i+1]!=9 for i in range(39,700))
  assert any(arr[t][i]&1 for i in range(39))
  print("phase",t,"overflow",gam[t],"first_odd",next(i for i,x in enumerate(arr[t][:39]) if x&1))
 print("PASS: exact two-sided recurrence, eight phases, preperiod 39, bulk period 20.")
if __name__=="__main__":run()
