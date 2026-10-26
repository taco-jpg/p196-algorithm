import sys
from bcycle_cpsat import solve_B
bases=[int(x) for x in sys.argv[1].split(',')]; ps=[int(x) for x in sys.argv[2].split(',')]; M=int(sys.argv[3]); tl=float(sys.argv[4])
for b in bases:
    row=[]
    for p in ps:
        name,sol,gs,wt=solve_B(b,p,M,tl,1,free_e2=True)
        tag={'OPTIMAL':'SAT','FEASIBLE':'SAT','INFEASIBLE':'no','UNKNOWN':'??'}[name]
        if sol: tag+=f"[gam={sum(gs)}]"
        row.append(f"p{p}:{tag}({wt:.0f}s)")
    print(f"base {b:3d} FREE-e2 M={M}: "+"  ".join(row),flush=True)
