import sys
from bcycle_cpsat import solve_B, verify
def sign(b,v): return 'H' if v>=b else ('N' if v==b-1 else 'L')
for b,p in ((4,3),(6,2),(7,3),(8,2),(11,3),(14,2),(3,5),(16,5)):
    # minimise |B|: smallest M with a solution
    for M in range(5,20):
        name,sol,gs,wt=solve_B(b,p,M,10,1)
        if sol: break
    ok1,ok2,out=verify(b,sol,gs)
    print(f"=== base {b} p={p}  (M={M}) replay ok={ok1 and ok2}  sum gam={sum(gs)}")
    for o in out:
        B=list(o[0]); print("   ",B," ".join(sign(b,v) for v in B)," e1,gam,u=",o[1:])
