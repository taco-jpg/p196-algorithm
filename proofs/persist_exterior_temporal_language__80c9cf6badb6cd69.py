"""Cyclic temporal-word automata for all repetitions of one exterior clock.

Experimental symbolic graph method. No decimal witness/proof is claimed.
A state word contains pairs of growth segments; one inverse spatial step is
an exact finite transduction. Every accepted word is a closed temporal walk.
"""
from continuation_theory_graph import half
from persist_exterior_neutral_center import BASE_PERIODS,BASE_STATE,internal
import json,time

class Automaton:
 def __init__(self,phase,edges):
  self.phase=phase;self.edges=set(edges)
 def prune(self):
  n=len(self.phase);adj=[[] for _ in range(n)];rev=[[] for _ in range(n)]
  for u,v,a in self.edges:adj[u].append(v);rev[v].append(u)
  visited=set();order=[]
  for root in range(n):
   if root in visited:continue
   visited.add(root);stack=[(root,0)]
   while stack:
    u,i=stack[-1]
    if i<len(adj[u]):
     v=adj[u][i];stack[-1]=(u,i+1)
     if v not in visited:visited.add(v);stack.append((v,0))
    else:order.append(u);stack.pop()
  comp=[-1]*n;cid=0
  for root in reversed(order):
   if comp[root]>=0:continue
   comp[root]=cid;stack=[root]
   while stack:
    u=stack.pop()
    for v in rev[u]:
     if comp[v]<0:comp[v]=cid;stack.append(v)
   cid+=1
  es={(u,v,a) for u,v,a in self.edges if comp[u]==comp[v]}
  keep={u for u,v,a in es}|{v for u,v,a in es};ids={u:i for i,u in enumerate(sorted(keep))}
  return Automaton([self.phase[u] for u in sorted(keep)],[(ids[u],ids[v],a) for u,v,a in es])
 def reduce(self):
  n=len(self.phase);outs=[[] for _ in range(n)]
  for u,v,a in self.edges:outs[u].append((a,v))
  blocks=self.phase[:]
  while True:
   keys=[(self.phase[u],frozenset((a,blocks[v]) for a,v in outs[u])) for u in range(n)]
   ids={};new=[]
   for key in keys:
    if key not in ids:ids[key]=len(ids)
    new.append(ids[key])
   if len(set(new))==len(set(blocks)):break
   blocks=new
  # One final partition can be renumbered but has exactly the same equivalence.
  phases=[0]*len(set(new))
  for u,b in enumerate(new):phases[b]=self.phase[u]
  return Automaton(phases,[(new[u],new[v],a) for u,v,a in self.edges])

def start(rotation):
 ps=BASE_PERIODS[rotation:]+BASE_PERIODS[:rotation]
 ext=tuple(xs[rotation:]+xs[:rotation] for xs in BASE_STATE);ds,l,r=internal(ext)
 es=[]
 for k in range(2):
  j=2*k;es.append((k,1-k,(ds[j],ds[j+1],l[j],r[j],l[j+1],r[j+1])))
 return Automaton([0,1],es),ps

def inverse(A,ps,cap=1000000):
 # New temporal state: (old temporal state, current right digit, old left digit).
 ids={};phase=[];es=set()
 available=[set() for _ in A.phase]
 for u,v,a in A.edges:available[u].add(a[0])
 def node(u,x,al):
  key=u,x,al
  if key not in ids:ids[key]=len(ids);phase.append(A.phase[u])
  return ids[key]
 for u,v,a in A.edges:
  x,y,l0,r0,l1,r1=a;p0,p1=ps[2*A.phase[u]:2*A.phase[u]+2]
  for al in range(10):
   src=node(u,x,al)
   for ar in range(10):
    for aa,bb,ll,rr in half(10,'E',al,ar,l0,r0,p0):
     for cc,dd,ss,tt in half(10,'E',y,bb,l1,r1,p1):
      if dd not in available[v]:continue
      dst=node(v,dd,cc);label=(ar,aa,ll,rr,ss,tt)
      es.add((src,dst,label))
      if len(es)>cap:raise RuntimeError('edge cap reached')
 return Automaton(phase,es).prune()

def heads(A,ps):
 ids={};phase=[];es=set()
 def node(u,x):
  key=u,x
  if key not in ids:ids[key]=len(ids);phase.append(A.phase[u])
  return ids[key]
 for u,v,a in A.edges:
  x,y,l0,r0,l1,r1=a
  if l0!=r0:continue
  z=y;co=0;p=ps[2*A.phase[u]+1]
  for i in range(p):
   s=2*z+((r1>>i)&1);z=s%10;co|=(s//10)<<i
  if co!=l1:continue
  es.add((node(u,x),node(v,z),a))
 H=Automaton(phase,es).prune()
 return {'states':len(H.phase),'edges':len(H.edges)}

def subsumed_by_bisim(A,B):
 # All cyclic traces of A must already have representatives in B.
 n=len(A.phase);C=Automaton(A.phase+B.phase, list(A.edges)+[(u+n,v+n,a) for u,v,a in B.edges])
 outs=[[] for _ in C.phase]
 for u,v,a in C.edges:outs[u].append((a,v))
 blocks=C.phase[:]
 while True:
  ids={};new=[]
  for u in range(len(C.phase)):
   key=(C.phase[u],frozenset((a,blocks[v]) for a,v in outs[u]))
   if key not in ids:ids[key]=len(ids)
   new.append(ids[key])
  if len(set(new))==len(set(blocks)):break
  blocks=new
 return set(new[:n])<=set(new[n:])

def run(rot,maxdepth=8):
 A,ps=start(rot);A=A.prune().reduce();out=[]
 for depth in range(maxdepth+1):
  h=heads(A,ps);r={'rotation':rot,'depth':depth,'states':len(A.phase),'edges':len(A.edges),'head_graph':h};out.append(r);print(json.dumps(r),flush=True)
  if h['states']:r['possible_center']=True;break
  t=time.monotonic()
  try:B=inverse(A,ps).reduce()
  except RuntimeError as e:r['incomplete']=str(e);break
  r['inverse_seconds']=time.monotonic()-t
  if subsumed_by_bisim(B,A):r['bisimulation_fixed_point']=True;break
  A=B
 return out
if __name__=='__main__':
 result=[]
 for rot in (0,1):
  result.extend(run(rot));json.dump(result,open('persist_exterior_temporal_language_results.json','w'),indent=2)
