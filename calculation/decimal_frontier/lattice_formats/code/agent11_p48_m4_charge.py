#!/usr/bin/env python3
"""Exact finite target check for the all-width mod-9 PAPER PROOF.
Base10 p=48 (01)^24, spatial primitive m4 selfmirror absorbing 3-cycles.
Depends on already committed agent11_p16_m4.phi, no external packages.
"""
from agent11_p16_m4 import phi
from collections import Counter
P=48; M=4; N=19**M
G=[t%2 for t in range(P)]
lam=[pow(2,-t,9) for t in range(P)]
assert all(lam[(t-1)%P] == (2*lam[t])%9 for t in range(P))

def dec(s):
 r=[]
 for _ in range(M):r.append(s%19);s//=19
 return tuple(r)
def enc(r):
 s=0
 for x in reversed(r):s=s*19+x
 return s

def symmetric(r):
 return any(all(r[i]==r[(a-i)%M] for i in range(M)) for a in range(M))
def primitive(r):
 return all(any(r[i]!=r[(i+d)%M] for i in range(M)) for d in (1,2))

def cuts(rows,k):
 L=[];H=[];Y=[]
 for t,row in enumerate(rows):
  _,A,D=phi(row,G[t]);L.append(A[k]);H.append((row[k]+D[k])//10)
  if G[t]:Y.append((row[(k-1)%M]+D[(k-1)%M])%10)
 return L,H,Y

def charge(S):
 L,H,Y=S
 return (sum(lam[t]*(L[t]-H[t]) for t in range(P))+sum(lam[2*i+1]*Y[i] for i in range(P//2)))%9

def check_cut_edge(rows,k):
 L,H,Y=cuts(rows,k); Lp,Hp,Yp=cuts(rows,(k+1)%M)
 left=right=0
 for t in range(P):
  x=rows[t][k];xn=rows[(t+1)%P][k]
  if G[t]==0:
   E=xn-2*x-L[t]-Hp[t]+10*(Lp[t]+H[t])
  else:
   i=t//2
   E=xn-x-L[t]-Y[i]+10*Lp[t]
   F=Yp[i]-x-Hp[t]+10*H[t]
   assert F==0
   E+=F
  assert E==0
  left+=lam[t]*E
 right=(charge((Lp,Hp,Yp))-charge((L,H,Y)))%9
 assert left%9==right==0
 return 48

nexts=[-1]*N
for s in range(N):
 r=dec(s)
 for g in G[:16]:
  out=phi(r,g)
  if out is None:break
  r=out[0]
 else:nexts[s]=enc(r)
seen=[False]*N; cycles=[]
for s in range(N):
 if seen[s]:continue
 path=[];seenLocal={};cur=s
 while cur>=0 and not seen[cur] and cur not in seenLocal:
  seenLocal[cur]=len(path);path.append(cur);cur=nexts[cur]
 if cur in seenLocal:
  cy=path[seenLocal[cur]:]
  if len(cy)==3 and any(primitive(dec(x)) and symmetric(dec(x)) for x in cy):cycles.append(cy)
 for x in path:seen[x]=True
assert len(cycles)==16
physQ=[];checks=0;rowsDone=0
for cy in cycles:
 for st in cy:
  r=dec(st);rows=[]
  for t in range(P):
   rows.append(r)
   out=phi(r,G[t]);assert out is not None
   r=out[0]
  assert r==dec(st)
  assert all(symmetric(row) and primitive(row) for row in rows)
  for k in range(M):
   q=charge(cuts(rows,k));physQ.append(q)
   checks+=check_cut_edge(rows,k)
   assert q in (3,6)
  rowsDone+=1
assert len(physQ)==192 and checks==9216
assert Counter(physQ)==Counter({3:96,6:96})
rootL=[0]*P;rootH=G[:];rootY=[1]*(P//2)
assert charge((rootL,rootH,rootY))==0
print(f'PAPER_CHECK_OK base10 temporal=48 overflow=(01)^24 spatial=4 cycles={len(cycles)} rows={rowsDone} cut_states={len(physQ)} charged_3={physQ.count(3)} charged_6={physQ.count(6)} root_charge=0 column_equalities={checks}',flush=True)
