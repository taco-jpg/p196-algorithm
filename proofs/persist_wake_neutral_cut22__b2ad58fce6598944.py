"""Exact fixed neutral-cut prefix constraints; existential deeper carries."""
import z3,time,json,argparse
CLOCK=(1,1,0,0,0,1,0,0,0,0,1)
INCOMING=(0,1,0,0,1,1,0,0,1,1,1)

def solve(k,steps=22,seconds=5):
 s=z3.Solver();s.set(timeout=int(1000*seconds))
 q=[z3.Int('initial_'+str(i))for i in range(k)];initial=q[:]
 for x in initial:s.add(x>=0,x<=18)
 s.add(initial[0]!=9)
 boundaries=[]
 for t in range(steps):
  h=CLOCK[t%11];r=INCOMING[t%11]
  lc=[z3.IntVal(r)]+[z3.Int(f'lc_{t}_{i}')for i in range(1,k+1)]
  rc=[z3.IntVal(1-r)]+[z3.Int(f'rc_{t}_{i}')for i in range(1,k+1)]
  boundaries.append(rc[-1])
  for c in lc[1:]+rc[1:]:s.add(c>=0,c<=1)
  lo=[q[i]+lc[i]-10*lc[i+1]for i in range(k)]
  hi=[q[i]+rc[i+1]-10*rc[i]for i in range(k)]
  for d in lo+hi:s.add(d>=0,d<=9)
  expr=[lo[i]+hi[i]for i in range(k)] if not h else [lo[0]+9*r]+[lo[i]+hi[i-1]for i in range(1,k)]
  q=[z3.Int(f'q_{t+1}_{i}')for i in range(k)]
  s.add(*[x==y for x,y in zip(q,expr)])
 start=time.monotonic();result=s.check()
 row=dict(k=k,steps=steps,status=str(result),seconds=time.monotonic()-start)
 if result==z3.sat:
  model=s.model();row['initial_prefix']=[model.eval(v).as_long()for v in initial]
  row['inner_carries']=[model.eval(v).as_long()for v in boundaries]
 elif result==z3.unknown:row['reason']=s.reason_unknown()
 return row

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--depth',type=int,default=12);ap.add_argument('--seconds',type=float,default=5);args=ap.parse_args()
 rows=[]
 for k in range(1,args.depth+1):
  print('building',k,flush=True);row=solve(k,seconds=args.seconds);rows.append(row);print(json.dumps(row),flush=True)
  if row['status']=='unsat':break
 open('persist_wake_neutral_cut22_results.json','w').write(json.dumps(rows,indent=2))
