"""Exact finite-center reachability for a supplied neutral exterior connector."""
from continuation_theory_graph import half
from collections import deque
import time,json

BASE_STATE=((9,0,9,9),(1,0,3,3),(0,1,12,28))
BASE_PERIODS=(1,1,4,5)

def internal(exterior):
 d,l,r=exterior
 return (tuple(9-x if j%2==0 else x for j,x in enumerate(d)),l,r)

def trans(st,ps,back=False):
 ds,lc,rc=st;Q=len(ds);K=Q//2
 def visit(k,al,dd,ll,rr,first):
  if k==K:
   if al==first:yield(tuple(dd),tuple(ll),tuple(rr)),(first, dd[0] if back else ds[0])
   return
  j=2*k
  if back:
   for ar in range(10):
    for al1,ar1,acl,acr in half(10,'E',al,ar,lc[j],rc[j],ps[j]):
     for bl1,br1,bcl,bcr in half(10,'E',ds[j+1],ar1,lc[j+1],rc[j+1],ps[j+1]):
      if br1!=ds[(j+2)%Q]:continue
      yield from visit(k+1,bl1,dd+[ar,al1],ll+[acl,bcl],rr+[acr,bcr],first)
  else:
   for al1,ar1,acl,acr in half(10,'I',al,ds[j],lc[j],rc[j],ps[j]):
    if al1!=ds[j+1]:continue
    for bl in range(10):
     for bl1,br1,bcl,bcr in half(10,'I',bl,ar1,lc[j+1],rc[j+1],ps[j+1]):
      nn=dd.copy();nn[j+1]=bl;nn[(j+2)%Q]=br1
      yield from visit(k+1,bl1,nn,ll+[acl,bcl],rr+[acr,bcr],first)
 for al in range(10):yield from visit(0,al,[] if back else [0]*Q,[],[],al)

def head(st,ps):
 ds,lc,rc=st;Q=len(ds)
 for j in range(0,Q,2):
  if lc[j]!=rc[j]:return False
  x=ds[j+1];out=0
  for i in range(ps[j+1]):
   z=2*x+((rc[j+1]>>i)&1);x=z%10;out|=(z//10)<<i
  if x!=ds[(j+2)%Q] or out!=lc[j+1]:return False
 return True

def search(rotation=0,maxstates=1000000,seconds=30,repeats=1):
 periods=BASE_PERIODS*repeats
 ps=periods[rotation:]+periods[:rotation]
 ext=tuple((xs*repeats)[rotation:]+(xs*repeats)[:rotation] for xs in BASE_STATE)
 target=internal(ext)
 assert any(ns==target for ns,p in trans(target,ps))
 todo=deque([target]);parent={target:None};start=time.monotonic();edges=0;found=None;complete=True
 while todo:
  if len(parent)>maxstates or time.monotonic()-start>seconds:complete=False;break
  st=todo.popleft()
  if head(st,ps):found=st;complete=False;break
  for ns,p in trans(st,ps,back=True):
   edges+=1
   if ns not in parent:parent[ns]=(st,p);todo.append(ns)
 path=[]
 if found:
  st=found
  while parent[st]:st,p=parent[st];path.append(p)
 return {'rotation':rotation,'repeats':repeats,'periods':ps,'target':target,'states':len(parent),'edges':edges,'complete':complete,'found':found,'path':path,'seconds':time.monotonic()-start}
if __name__=='__main__':
 out=[]
 for rot in range(4):
  r=search(rot);out.append(r);print(json.dumps(r),flush=True)
  json.dump(out,open('persist_exterior_neutral_center_results.json','w'),indent=2)
