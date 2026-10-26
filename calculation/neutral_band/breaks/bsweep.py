import sys, time
from bcycle_cpsat import solve_B, verify
bases=[int(x) for x in sys.argv[1].split(',')]; ps=[int(x) for x in sys.argv[2].split(',')]; M=int(sys.argv[3]); tl=float(sys.argv[4])
for b in bases:
    row=[]
    for p in ps:
        name,sol,gs,wt=solve_B(b,p,M,tl,1)
        tag={'OPTIMAL':'SAT','FEASIBLE':'SAT','INFEASIBLE':'no','UNKNOWN':'??'}[name]
        if sol:
            ok1,ok2,out=verify(b,sol,gs); tag+=("" if ok1 and ok2 else "(BAD)")+f"[m={max(len(o[0]) for o in out)}]"
        row.append(f"p{p}:{tag}({wt:.0f}s)")
    print(f"base {b:3d} M={M}: "+"  ".join(row),flush=True)
