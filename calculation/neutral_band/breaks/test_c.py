import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import neutral_band_search as N
from neutral_band_search import *
from ccycle_cpsat import *
# derive streams from the Lean certificates and re-find the C cycle with the solver
for b,es in N._lean_certs():
    if b not in (26,11,16,4,17): continue
    e1s=[e1(b,E[0]) for E in es]; gs=[gam(b,E[0],E[1]) for E in es]
    cs=[len(E[1]) for E in es]; vs=[E[5] for E in es]
    print(f"base {b}: p={len(es)} e1={e1s} gam={gs} c_t={cs} v={vs}")
    for tl in (30,):
        nm,sol=solve_C(b,e1s,gs,cs[0],tuple(vs),tl)
        print("   CP-SAT C with the true schedule:",nm, "match true C0:", (sol is not None and sol[0]==es[0][1]))
        if sol:
            # replay with library: canonical run from (B,C) of the cert and compare C trajectory
            print("   C0 found:",sol[0][:12],"...")
