# compare CP-SAT B-cycle existence with brute-force orbit enumeration (autonomous B system), small bases
import itertools, sys
from lib import *
from decouple import phiB
from bcycle_cpsat import solve_B
def brute_periods(b,maxm,maxlen):
    n=b-1; per=set()
    for m in range(0,maxm+1):
        for B in itertools.product(range(2*n+1),repeat=m):
            B=list(B)
            if B and B[0]==0: continue
            seen={}; cur=tuple(B); t=0; gs=[]
            while cur not in seen and t<300 and len(cur)<=maxlen:
                seen[cur]=t; nb,u,E1,g=phiB(b,list(cur)); gs.append(g); cur=tuple(nb); t+=1
                if nb and nb[0]==0: break
            if cur in seen:
                s=seen[cur]; cyc=gs[s:]
                if sum(cyc)>0: per.add((len(cyc),max(len(x) for x in [list(k) for k in list(seen)[s:]] or [[]])))
    return per
for b,maxm in ((3,6),(4,5),(5,4),(6,4),(7,3)):
    per=brute_periods(b,maxm,maxm+6)
    bp=sorted({p for p,_ in per})
    M=maxm+3
    cs=[]
    for p in range(1,13):
        name,sol,gs,wt=solve_B(b,p,M,10,1)
        if sol:
            # minimal period of found cycle can be a divisor; record p
            cs.append(p)
    print(f"base {b}: brute-force minimal periods (|B|<={maxm}) = {bp} | CP-SAT periods p<=12 with SAT (|B|<={maxm}): {cs}",flush=True)
