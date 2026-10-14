"""Existential inner-carry relaxation for 22-step neutral-exterior preservation.
UNSAT is a sound all-interior obstruction at the chosen prefix depth;
SAT is not a realizable finite-center witness.
"""
from persist_wake_neutral_center import P,CLOCK
import z3,time,json,argparse

def solve(k,steps=22,seconds=20,m=2):
    w=len(P)+m+k;fixed=P+(9,)*m;s=z3.Solver();s.set(timeout=int(1000*seconds))
    q=[z3.IntVal(x)for x in fixed]+[z3.Int('initial_'+str(i))for i in range(k)]
    initial=q[len(fixed):]
    for x in initial:s.add(x>=0,x<=18)
    if initial:s.add(initial[0]!=9)
    boundaries=[]
    for t in range(steps):
        h=CLOCK[t%11]
        lc=[z3.IntVal(0)]+[z3.Int(f'lc_{t}_{i}')for i in range(1,w+1)]
        rc=[z3.IntVal(h)]+[z3.Int(f'rc_{t}_{i}')for i in range(1,w+1)]
        boundaries.append(rc[-1])
        for c in lc[1:]+rc[1:]:s.add(c>=0,c<=1)
        lo=[q[i]+lc[i]-10*lc[i+1]for i in range(w)]
        hi=[q[i]+rc[i+1]-10*rc[i]for i in range(w)]
        for d in lo+hi:s.add(d>=0,d<=9)
        expr=[lo[i]+hi[i]for i in range(w)] if not h else [lo[0]+1]+[lo[i]+hi[i-1]for i in range(1,w)]
        q=[z3.Int(f'q_{t+1}_{i}')for i in range(w)]
        s.add(*[x==y for x,y in zip(q,expr)])
        if (t+1)%11==0:s.add(*[q[i]==v for i,v in enumerate(fixed)])
    start=time.monotonic();r=s.check();row=dict(k=k,steps=steps,seconds=time.monotonic()-start,status=str(r),m=m)
    if r==z3.sat:
        model=s.model();row['initial_prefix']=[model.eval(v).as_long()for v in initial]
        row['inner_carries']=[model.eval(v).as_long()for v in boundaries]
    elif r==z3.unknown:row['reason']=s.reason_unknown()
    return row

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--depth',type=int,default=12);ap.add_argument('--seconds',type=float,default=10);args=ap.parse_args()
 rows=[]
 for k in range(1,args.depth+1):
    row=solve(k,seconds=args.seconds);rows.append(row);print(json.dumps(row),flush=True)
    if row['status']=='unsat':break
 open('persist_wake_neutral_prefix22_results.json','w').write(json.dumps(rows,indent=2))
