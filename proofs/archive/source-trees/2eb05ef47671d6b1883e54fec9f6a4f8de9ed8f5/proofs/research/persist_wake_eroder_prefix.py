"""Negate the proposed three-neutral-symbol eroder using exact prefix dynamics."""
import z3,time,json,argparse
from persist_wake_neutral_cut22 import CLOCK,INCOMING

def solve(k,steps=22,seconds=10,negate=3):
 s=z3.SolverFor('QF_BV');s.set(timeout=int(1000*seconds))
 q=[z3.BitVec('initial_'+str(i),5)for i in range(k)];initial=q[:]
 for x in initial:s.add(z3.ULE(x,18))
 s.add(initial[0]!=9);cut=[];mid=None
 def add(x,c):
  z=x+z3.If(c,z3.BitVecVal(1,5),z3.BitVecVal(0,5));carry=z3.UGE(z,10)
  return z3.If(carry,z-10,z),carry
 for t in range(steps):
  h=CLOCK[t%11];r=INCOMING[t%11]
  c=z3.BoolVal(bool(r));lo=[]
  for x in q:d,c=add(x,c);lo.append(d)
  c=z3.Bool('inner_'+str(t));cut.append(c);hi=[]
  for x in q[::-1]:d,c=add(x,c);hi.append(d)
  s.add(c==bool(1-r));hi.reverse()
  expr=[lo[i]+hi[i]for i in range(k)] if not h else [lo[0]+9*r]+[lo[i]+hi[i-1]for i in range(1,k)]
  q=[z3.BitVec(f'q_{t+1}_{i}',5)for i in range(k)]
  s.add(*[x==y for x,y in zip(q,expr)])
  if t==10:mid=q[:]
 s.add(z3.Or([mid[i]!=9 for i in range(min(negate,k))]))
 start=time.monotonic();result=s.check();row=dict(k=k,steps=steps,status=str(result),seconds=time.monotonic()-start,negated_neutral_count=negate)
 if result==z3.sat:
  model=s.model();row['initial_prefix']=[model.eval(v).as_long()for v in initial]
  row['inner_carries']=[int(z3.is_true(model.eval(v)))for v in cut]
  row['macro_prefix']=[model.eval(v).as_long()for v in mid]
 elif result==z3.unknown:row['reason']=s.reason_unknown()
 return row

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--depth',type=int,default=12);ap.add_argument('--seconds',type=float,default=10);ap.add_argument('--negate',type=int,default=3);args=ap.parse_args()
 rows=[]
 for k in range(max(3,args.negate),args.depth+1):
  row=solve(k,seconds=args.seconds,negate=args.negate);rows.append(row);print(json.dumps(row),flush=True)
  if row['status']=='unsat':break
 open('persist_wake_eroder_prefix_results.json','w').write(json.dumps(rows,indent=2))
