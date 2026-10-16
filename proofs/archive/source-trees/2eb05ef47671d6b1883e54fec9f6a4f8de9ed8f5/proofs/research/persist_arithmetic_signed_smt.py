"""Find finite cores satisfying prescribed neutral-boundary carry phases.
SAT witness checked by full integer arithmetic. UNSAT is only fixed width.
"""
from persist_arithmetic_signed_core import *
import z3,time,argparse

def solve(c,steps,seconds):
 s=z3.SolverFor('QF_BV');s.set(timeout=int(1000*seconds))
 ds=[z3.BitVec('d_0_'+str(i),4)for i in range(c)];initial=ds[:]
 for d in ds:s.add(z3.ULE(d,9))
 for t in range(steps):
  a=INCOMING[t%11];h=CLOCK[t%11];L=len(ds)
  ns=[z3.BitVec(f'd_{t+1}_{i}',4)for i in range(L)]
  cs=[z3.BoolVal(bool(a))]+[z3.Bool(f'c_{t}_{i}')for i in range(1,L)]+[z3.BoolVal(not a)]
  for i in range(L):
   s.add(z3.ULE(ns[i],9))
   inp=z3.ZeroExt(1,ds[i])+z3.ZeroExt(1,ds[L-1-i])+z3.If(cs[i],z3.BitVecVal(1,5),z3.BitVecVal(0,5))
   out=z3.ZeroExt(1,ns[i])+z3.If(cs[i+1],z3.BitVecVal(10,5),z3.BitVecVal(0,5))
   s.add(inp==out)
  if h:ns.append(z3.BitVecVal(9*a,4))
  ds=ns
 start=time.monotonic();status=s.check();result=dict(width=c,steps=steps,status=str(status),seconds=time.monotonic()-start)
 if status==z3.sat:
  model=s.model();C=sum(model.eval(d).as_long()*10**i for i,d in enumerate(initial));result['center']=str(C).zfill(c)
  assert sum(row[-1]for row in run(c,C,steps))==steps
  assert check_actual(c,C,m=60,steps=steps)==steps
 elif status==z3.unknown:result['reason']=s.reason_unknown()
 return result

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--width',nargs='+',type=int,default=[8,10,12,16,24,32,64]);ap.add_argument('--steps',type=int,default=22);ap.add_argument('--seconds',type=float,default=10);args=ap.parse_args();res=[]
 for c in args.width:
  row=solve(c,args.steps,args.seconds);res.append(row);print(json.dumps(row),flush=True)
  with open('persist_arithmetic_signed_smt_results.json','w')as f:json.dump(res,f,indent=2)
