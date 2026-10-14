"""Exact interior-frame spatial graph. Eight growths move the interface four columns."""
import json
from continuation_theory_graph import half
from resume_boundary4_targets import targets,carry

def transitions_I(st):
 ds,lc,rc=st; Q=len(ds);K=Q//2
 def visit(k,al,dsnew,lnew,rnew,first):
  if k==K:
   if al==first:
    yield (tuple(dsnew),tuple(lnew),tuple(rnew)),(first,ds[0])
   return
  j=2*k
  for al1,ar1,acl,acr in half(10,'I',al,ds[j],lc[j],rc[j],2):
   if al1!=ds[j+1]:continue
   for bl in range(10):
    for bl1,br1,bcl,bcr in half(10,'I',bl,ar1,lc[j+1],rc[j+1],2):
     dd=dsnew.copy();dd[j+1]=bl;dd[(j+2)%Q]=br1
     yield from visit(k+1,bl1,dd,lnew+[acl,bcl],rnew+[acr,bcr],first)
 for al0 in range(10):yield from visit(0,al0,[0]*Q,[],[],al0)

def internal_targets(W):
 ext=targets(W); L=ext['L'];R=ext['R'];car=[carry(q) for q in ext['q'][:-1]]
 states=[]
 for i in range(4):
  ds=[]
  for k in range(4):
   ds.extend([R[4*k][(k-i)%4],L[4*k+2][(k-i+1)%4]])
  lc=[];rc=[]
  for j in range(8):
   u=(j//2-i)%4
   lc.append(sum(car[2*j+t][1][(u+1)%4]<<t for t in range(2)))
   rc.append(sum(car[2*j+t][0][u]<<t for t in range(2)))
  states.append((tuple(ds),tuple(lc),tuple(rc)))
 for i,st in enumerate(states):
  poss=list(transitions_I(st))
  assert any(ns==states[(i+1)%4] for ns,p in poss),(W,i,st,states[(i+1)%4],poss)
 def pack(st):return sum((d|(a<<4)|(b<<6))<<(8*j) for j,(d,a,b) in enumerate(zip(*st)))
 return {'word':W,'states':states,'packed':[pack(st) for st in states]}

if __name__=='__main__':
 from continuation_theory_graph import transitions as old
 import random
 random.seed(1492)
 for _ in range(100):
  x,y=random.randrange(10),random.randrange(10)
  a,b,c,d=[random.randrange(4) for _ in range(4)]
  st=((x,y),(a,c),(b,d))
  new=set(transitions_I(st))
  want=set()
  for ns,dp,con in old(10,2,2,'I',(x,y,a,b,c,d)):
   xx,yy,aa,bb,cc,dd=ns;want.add((((xx,yy),(aa,cc),(bb,dd)),dp))
  assert new==want
 out=[internal_targets(w) for w in ((3,10,15,8),(15,10,3,8),(9,2,9,16))]
 json.dump(out,open('resume_boundary4_interior_targets.json','w'),indent=2)
 for r in out:print(r['word'],r['packed'])

def predecessors_I(st):
 ds,lc,rc=st;Q=len(ds);K=Q//2
 def visit(k,al,dsold,lold,rold,first):
  if k==K:
   if al==first:yield (tuple(dsold),tuple(lold),tuple(rold)),(first,dsold[0])
   return
  j=2*k
  for ar in range(10):
   for al1,ar1,acl,acr in half(10,'E',al,ar,lc[j],rc[j],2):
    for bl1,br1,bcl,bcr in half(10,'E',ds[j+1],ar1,lc[j+1],rc[j+1],2):
     if br1!=ds[(j+2)%Q]:continue
     yield from visit(k+1,bl1,dsold+[ar,al1],lold+[acl,bcl],rold+[acr,bcr],first)
 for al0 in range(10):yield from visit(0,al0,[],[],[],al0)

def is_head(st):
 ds,lc,rc=st;Q=len(ds)
 for j in range(0,Q,2):
  if lc[j]!=rc[j]:return False
  x=ds[j+1];co=0
  for t in range(2):
   x,c=(2*x+((rc[j+1]>>t)&1))%10,(2*x+((rc[j+1]>>t)&1))//10
   co|=c<<t
  if lc[j+1]!=co or ds[(j+2)%Q]!=x:return False
 return True
