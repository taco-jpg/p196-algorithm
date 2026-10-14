"""Exact SAT encoding of universal binary survival, arbitrary rho blocks.
The 240 DFA bits are propagated in the dual direction, so no 2^K tree is built.
"""
from pathlib import Path
import z3,json,time,argparse
p=argparse.ArgumentParser();p.add_argument('--max-depth',type=int,default=30);p.add_argument('--timeout',type=int,default=60000);a=p.parse_args()
base=Path(__file__).parent;tau=[list(map(int,line.split())) for line in(base/'compact_transitions.txt').read_text().splitlines()];N=len(tau)
solver=z3.Solver();solver.set(timeout=a.timeout)
old=[z3.BoolVal(True)]*N;ys=[];rows=[];started=time.time()
for k in range(1,a.max_depth+1):
 y=z3.BitVec('y_'+str(k),3);ys.append(y);new=[z3.Bool('s_%d_%d'%(k,v)) for v in range(N)]
 for v in range(N):
  cases=[]
  for q in range(8):
   u,w=tau[v][q],tau[v][q+8]
   if u>=0 and w>=0:cases.append(z3.And(y==q,old[u],old[w]))
  solver.add(new[v]==z3.Or(cases))
 query=z3.Or([new[g*15+14] for g in range(16)])
 solver.push();solver.add(query);t0=time.time();result=solver.check();row=dict(depth=k,status=str(result),seconds=time.time()-t0,total_seconds=time.time()-started)
 if result==z3.sat:
  model=solver.model();word=[model.eval(t,model_completion=True).as_long()+1 for t in ys];row['rho_word_read_inside_to_outside']=word
  row['viable_initial_groups']=[g for g in range(16) if z3.is_true(model.eval(new[g*15+14]))]
 elif result==z3.unsat:
  (base/'rho_horizon_unsat.smt2').write_text(solver.to_smt2());row['certificate']='rho_horizon_unsat.smt2'
 else:row['reason']=solver.reason_unknown()
 rows.append(row);print(json.dumps(row),flush=True)
 json.dump(rows,open(base/'rho_horizon_sat.json','w'),indent=2)
 solver.pop()
 if result!=z3.sat:break
 old=new
