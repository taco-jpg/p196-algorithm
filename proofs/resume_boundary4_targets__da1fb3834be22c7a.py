"""Lift periodic q bulk to exact segment/digit/carry states; verify spatial SCC."""
import json
from resume_renewal_bulk import transform
from continuation_theory_multigrowth import transitions

def carry(q):
 n=len(q);j=next(i for i,a in enumerate(q) if a!=9)
 a=[0]*n;b=[0]*n;a[j]=b[j]=int(q[j]>=10)
 for k in range(1,n):i=(j+k)%n;a[i]=(q[i]+a[(i-1)%n])//10
 for k in range(1,n):i=(j-k)%n;b[i]=(q[i]+b[(i+1)%n])//10
 return a,b

def targets(W,period=16):
 qs=[tuple(W)]
 for t in range(period):qs.append(transform(qs[-1],bool(t%2)))
 assert qs[-1]==qs[0]
 L=[];R=[];car=[]
 for t in range(period):
  qprev=qs[(t-1)%period];a,b=carry(qprev);h=(t-1)%2
  lo=[(qprev[i]+a[(i-1)%4])%10 for i in range(4)]
  hi=[(qprev[(i-h)%4]+b[(i-h+1)%4])%10 for i in range(4)]
  assert tuple(x+y for x,y in zip(lo,hi))==qs[t]
  L.append(hi);R.append(lo);car.append(carry(qs[t]))
 states=[]
 for i in range(4):
  ls=tuple(L[t][i] for t in range(0,period,2))
  lc=tuple(sum(car[t+k][1][i]<<k for k in range(2)) for t in range(0,period,2))
  rc=tuple(sum(car[t+k][0][(i-1)%4]<<k for k in range(2)) for t in range(0,period,2))
  states.append((ls,lc,rc))
 for i,st in enumerate(states):
  ns=[(x,pair) for x,pair in transitions(10,[2]*(period//2),st)]
  assert (states[(i+1)%4],(L[0][i],R[0][i])) in ns,(i,st,ns)
 def pack(s):
  ls,lc,rc=s
  return sum((d|(a<<4)|(b<<6))<<(8*j) for j,(d,a,b) in enumerate(zip(ls,lc,rc)))
 return {'word':W,'states':states,'packed':[pack(s) for s in states], 'L':L,'R':R,'q':qs}
if __name__=='__main__':
 words=[(3,10,15,8),(15,10,3,8),(9,2,9,16)]
 out=[targets(w) for w in words]
 json.dump(out,open('resume_boundary4_targets.json','w'),indent=2)
 for d in out:
  print(d['word'], d['packed'])
