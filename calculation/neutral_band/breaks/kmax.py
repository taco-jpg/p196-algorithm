import sys
from bcycle_relax import solve_relaxed
b=int(sys.argv[1]); ps=[int(x) for x in sys.argv[2].split(',')]; Kcap=int(sys.argv[3]); tl=float(sys.argv[4])
for p in ps:
    last=0; status='?'
    for K in range(1,Kcap+1):
        nm,g=solve_relaxed(b,p,K+7,K,tl)
        if nm in('OPTIMAL','FEASIBLE'): last=K
        else: status=nm; break
    print(f"base {b} p={p}: bottom-periodic depth K_max = {last}{'+' if status=='?' else ''} (stopped by {status})",flush=True)
