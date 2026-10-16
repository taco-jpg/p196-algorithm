"""Direct universal Horn encoding of DFA closure, with no sampling of words."""
import creative_regular_boolean as b
import creative_regular_invariant as r
import z3,time,json,sys

def fst_graph():
 states=[(0,0,0,-1,False),(1,0,1,1,False)];index={x:i for i,x in enumerate(states)};edges=[]
 pos=0
 while pos<len(states):
  e,a,c,t,started=states[pos]
  for q in range(0 if started else 1,19):
   for cn in (0,1):
    if r.C(q,cn)!=c:continue
    lo=r.D(q,a);hi=r.D(q,cn);out=lo+t if e else lo+hi
    st=(e,r.C(q,a),cn,hi if e else -1,True)
    if st not in index:index[st]=len(states);states.append(st)
    edges.append((pos,q,out,index[st]))
  pos+=1
 return states,edges

def solve(N,seconds=60,seed=None):
 start=time.time();L=b.Learner(N,seed);states,edges=fst_graph()
 R=[[[z3.Bool('closed_%d_%d_%d'%(x,a,c)) for c in range(N)] for a in range(N)] for x in range(len(states))]
 L.s.add(R[0][0][0],R[1][0][0])
 count=0
 for x,q,out,y in edges:
  for a in range(N):
   for c in range(N):
    source=z3.Not(R[x][a][c])
    for aa in range(N):
     first=z3.Not(L.d[a][q][aa])
     for cc in range(N):
      L.s.add(z3.Or(source,first,z3.Not(L.d[c][out][cc]),R[y][aa][cc]));count+=1
 for x,(e,a,c,t,started) in enumerate(states):
  for center in [None]+list(range(0,19,2)):
   if not started and (center is None or center==0):continue
   extra=None
   if center is None:
    if a!=c:continue
    oc=2*t if e else None
   else:
    if r.C(center,a)!=c:continue
    if e:extra=r.D(center,a)+t;oc=None
    else:oc=2*r.D(center,a)
   for ia in range(N):
    for oa in range(N):
     antecedent=[z3.Not(R[x][ia][oa]),z3.Not(L.f[ia][r.terminal_index(center)])]
     if extra is None:L.s.add(z3.Or(antecedent+[L.f[oa][r.terminal_index(oc)]]))
     else:
      for ob in range(N):L.s.add(z3.Or(antecedent+[z3.Not(L.d[oa][extra][ob]),L.f[ob][0]]))
 build=time.time()-start;L.s.set(timeout=int(seconds*1000));status=L.s.check();res={'states':N,'status':str(status),'fst_states':len(states),'fst_edges':len(edges),'closure_clauses':count,'build_seconds':build,'total_seconds':time.time()-start}
 if status==z3.sat:
  dfa=L.model();assert r.safety_counterexample(dfa) is None;assert r.closure_counterexample(dfa) is None
  res['status']='CERTIFICATE';res['dfa']=dfa
 return res

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description='Encode the entire invariant closure product in finite SAT/SMT.')
 parser.add_argument('--min-states',type=int,default=2)
 parser.add_argument('--max-states',type=int,default=4)
 parser.add_argument('--seconds',type=float,default=60)
 parser.add_argument('--objective',choices=['any','196'],default='any')
 parser.add_argument('--output',default='creative_regular_direct_results.json')
 args=parser.parse_args()
 if args.min_states<1 or args.max_states<args.min_states:parser.error('invalid state bounds')
 results=[]
 for n in range(args.min_states,args.max_states+1):
  res=solve(n,args.seconds,seed=None if args.objective=='any' else ((7,),18));results.append(res);print(json.dumps(res),flush=True)
  with open(args.output,'w') as f:json.dump(results,f,indent=2)
  if res['status']=='CERTIFICATE':break
