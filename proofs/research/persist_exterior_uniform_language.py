"""All-repetition temporal automata for uniform decimal 8->5->2 exterior."""
from persist_exterior_temporal_language import Automaton,subsumed_by_bisim
from continuation_theory_graph import half
import json,time

def start():
 return Automaton([0,1,2],[(j,(j+1)%3,(d,c,c)) for j,(d,c) in enumerate(zip((8,5,2),(3,1,0)))])

def inverse(A,cap=1000000):
 ids={};phases=[];edges=set();available=[set() for _ in A.phase]
 for u,v,(d,l,r) in A.edges:available[u].add(d)
 def node(u,d,carry_digit):
  key=(u,d,carry_digit)
  if key not in ids:ids[key]=len(ids);phases.append(A.phase[u])
  return ids[key]
 for u,v,(d,l,r) in A.edges:
  for dr in range(10):
   src=node(u,d,dr)
   for dl in range(10):
    for dl1,dr1,lo,ri in half(10,'I',dl,dr,l,r,2):
     if dl1 not in available[v]:continue
     dst=node(v,dl1,dr1);edges.add((src,dst,(dl,lo,ri)))
     if len(edges)>cap:raise RuntimeError('edge cap')
 return Automaton(phases,edges).prune()

def head(A):
 H=Automaton(A.phase,[(u,v,s) for u,v,s in A.edges if s==(1,2,0)]).prune()
 return len(H.phase),len(H.edges)

def run(depthcap=16):
 A=start();out=[]
 for depth in range(depthcap+1):
  hv,he=head(A);row={'depth':depth,'vertices':len(A.phase),'edges':len(A.edges),'head_vertices':hv,'head_edges':he};out.append(row);print(json.dumps(row),flush=True)
  if hv:row['possible_exterior']=True;break
  then=time.monotonic()
  try:B=inverse(A).reduce()
  except RuntimeError as e:row['incomplete']=str(e);break
  row['inverse_seconds']=time.monotonic()-then
  if subsumed_by_bisim(B,A):
   row['bisimulation_fixed_point']=True
   json.dump({'phase':A.phase,'edges':sorted(A.edges)},open('persist_exterior_uniform_invariant.json','w'),indent=2)
   break
  A=B
 json.dump(out,open('persist_exterior_uniform_language_results.json','w'),indent=2)
 return out
if __name__=='__main__':run()
