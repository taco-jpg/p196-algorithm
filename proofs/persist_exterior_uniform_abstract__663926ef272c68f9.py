from persist_exterior_uniform_language import *

def abstract(A,k):
 outs=[[] for _ in A.phase]
 for u,v,a in A.edges:outs[u].append((a,v))
 blocks=A.phase[:]
 for _ in range(k):
  ids={};new=[]
  for u in range(len(A.phase)):
   key=(A.phase[u],frozenset((a,blocks[v]) for a,v in outs[u]))
   if key not in ids:ids[key]=len(ids)
   new.append(ids[key])
  blocks=new
 n=len(set(blocks));phases=[0]*n
 for u,b in enumerate(blocks):phases[b]=A.phase[u]
 return Automaton(phases,[(blocks[u],blocks[v],a) for u,v,a in A.edges])

def scan(k,steps=20,cap=200000):
 A=start();out=[]
 for depth in range(steps+1):
  hv,he=head(A);row={'lookahead':k,'depth':depth,'vertices':len(A.phase),'edges':len(A.edges),'head_vertices':hv,'head_edges':he};out.append(row)
  print(json.dumps(row),flush=True)
  if hv:row['possible_exterior']=True;break
  try:B=abstract(inverse(A,cap),k)
  except RuntimeError as e:row['incomplete']=str(e);break
  if subsumed_by_bisim(B,A):
   row['fixed_point']=True
   json.dump({'phase':A.phase,'edges':sorted(A.edges)},open(f'persist_exterior_uniform_abstract_invariant_{k}.json','w'),indent=2)
   break
  A=B
 return out
if __name__=='__main__':
 out=[]
 for k in (0,1,2,3):
  out.extend(scan(k));json.dump(out,open('persist_exterior_uniform_abstract_results.json','w'),indent=2)
