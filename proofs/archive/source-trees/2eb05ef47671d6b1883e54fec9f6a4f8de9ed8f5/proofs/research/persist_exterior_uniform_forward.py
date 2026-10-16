from persist_exterior_uniform_language import Automaton,half,subsumed_by_bisim
import json,time

def start():return Automaton([0,1,2],[(j,(j+1)%3,(1,2,0)) for j in range(3)])

def step(A,cap=200000):
 ids={};phase=[];edges=set()
 def node(u,dr,dl):
  key=u,dr,dl
  if key not in ids:ids[key]=len(ids);phase.append(A.phase[u])
  return ids[key]
 desc=[];incoming={}
 for u,v,(d,l,r) in A.edges:
  for dr in range(10):
   for dl1,dr1,li,ro in half(10,'E',d,dr,l,r,2):
    desc.append((u,v,dr,dl1,dr1,li,ro))
    incoming.setdefault((v,dr1),set()).add(dl1)
 for u,v,dr,dl1,dr1,li,ro in desc:
  dst=node(v,dr1,dl1)
  for oldleft in incoming.get((u,dr),()):
   src=node(u,dr,oldleft);edges.add((src,dst,(oldleft,li,ro)))
   if len(edges)>cap:raise RuntimeError('edge cap')
 return Automaton(phase,edges).prune()

def accepting(A):
 target=((8,3,3),(5,1,1),(2,0,0))
 B=Automaton(A.phase,[(u,v,a) for u,v,a in A.edges if a==target[A.phase[u]]]).prune()
 return len(B.phase),len(B.edges)

def run(depthcap=16):
 A=start();out=[]
 for d in range(depthcap+1):
  av,ae=accepting(A);row={'depth':d,'vertices':len(A.phase),'edges':len(A.edges),'target_vertices':av,'target_edges':ae};out.append(row);print(json.dumps(row),flush=True)
  if av:row['possible_uniform_core']=True;break
  try:B=step(A).reduce()
  except RuntimeError as e:row['incomplete']=str(e);break
  if subsumed_by_bisim(B,A):
   row['fixed_point']=True
   json.dump({'phase':A.phase,'edges':sorted(A.edges)},open('persist_exterior_uniform_forward_invariant.json','w'),indent=2)
   break
  A=B
 json.dump(out,open('persist_exterior_uniform_forward_results.json','w'),indent=2)
 return out
if __name__=='__main__':run()
