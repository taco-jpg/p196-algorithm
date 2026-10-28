#!/usr/bin/env python3
"""Independent pure-Python functional graph of all 19**4 spatial rows."""
from agent11_p16_m4 import phi
from collections import Counter
B=19; M=4;N=B**M

def dec(i):
 a=[]
 for _ in range(M):a.append(i%19);i//=19
 return tuple(a)
def enc(a):
 x=0
 for v in reversed(a):x=x*19+v
 return x

def symmetry(row):
 return any(all(row[i]==row[(k-i)%M] for i in range(M)) for k in range(M))
def primitive(row):
 return all(any(row[i]!=row[(i+d)%M] for i in range(M)) for d in (1,2))
nexts=[-1]*N
for s in range(N):
 r=dec(s)
 for t in range(16):
  res=phi(r,t%2)
  if res is None:break
  r=res[0]
 else:nexts[s]=enc(r)
seen=[0]*N;pos=[-1]*N;cycles=[]
for s in range(N):
 if seen[s]:continue
 path=[];i=s
 while i>=0 and seen[i]==0:
  seen[i]=1;pos[i]=len(path);path.append(i);i=nexts[i]
 if i>=0 and seen[i]==1 and pos[i]>=0:
  cy=path[pos[i]:]
  cycles.append(cy)
 for j in path:seen[j]=2;pos[j]=-1
cnt=Counter(map(len,cycles))
mirrorCy=[c for c in cycles if any(symmetry(dec(x)) for x in c)]
primitiveSym=[c for c in mirrorCy if any(primitive(dec(x)) and symmetry(dec(x)) for x in c)]
print('PYTHON_COMPLETE',N,'valid',sum(v>=0 for v in nexts),'cycles',len(cycles),'length_counts',sorted(cnt.items()),'mirror',len(mirrorCy),'primitive_mirror',len(primitiveSym),'longer',sum(len(c)>1 for c in primitiveSym),'cycle_members',sum(map(len,cycles)),flush=True)
assert N==130321 and sum(v>=0 for v in nexts)==128126
assert cnt==Counter({1:60,3:50})
assert len(mirrorCy)==70 and len(primitiveSym)==64 and sum(len(c)>1 for c in primitiveSym)==16
