import sys
from bcycle_cpsat import solve_B
lo,hi,pmax,M,tl=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5])
free = len(sys.argv)>6 and sys.argv[6]=='free'
for b in range(lo,hi+1):
    sat=[];unk=[]
    for p in range(1,pmax+1):
        name,sol,gs,wt=solve_B(b,p,M,tl,1,free_e2=free)
        if sol: sat.append(p)
        elif name!='INFEASIBLE': unk.append(p)
    print(f"base {b:3d}: B-cycle periods p<={pmax} (|B|<={M-3}) {'FREE' if free else 'feedback'}: {sat}   unknown: {unk}",flush=True)
