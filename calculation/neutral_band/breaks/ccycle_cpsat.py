import os
"""C-system periodic-orbit finder (CP-SAT) given the bit streams from the B-cycle: e1[t], gam[t].
C^(t) is a symmetric array of explicit length c_t; c_{t+1}=c_t+gam_t-2 v_t; trimmed cells must be n.
Condition: C emits e2 = 1-e1 at every step (pol of C's top-most non-neutral = rho_{-1} = 1-e1), carry-in/defaults = e1.
usage: ccycle_cpsat.solve_C(b, e1, gam, c0, vsched, tl) -> sol or None"""
import sys, itertools
from ortools.sat.python import cp_model
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))

def solve_C(b,e1s,gams,c0,vs,tl=20,workers=1):
    n=b-1; p=len(e1s)
    cl=[c0]
    for t in range(p): cl.append(cl[-1]+gams[t]-2*vs[t])
    if cl[p]!=c0 or min(cl)<0: return 'BADLEN',None
    mdl=cp_model.CpModel()
    C=[[mdl.NewIntVar(0,2*n,f"C{t}_{j}") for j in range(cl[t])] for t in range(p+1)]
    for j in range(c0): mdl.Add(C[p][j]==C[0][j])
    for t in range(p+1):
        c=cl[t]
        for j in range(c): mdl.Add(C[t][j]==C[t][c-1-j])
    for t in range(p):
        c=cl[t]; e1=e1s[t]; g=gams[t]; v=vs[t]
        if c==0:
            return 'EMPTY',None   # empty centre: handled separately (not supported)
        isH=[mdl.NewBoolVar("") for j in range(c)]; isN=[mdl.NewBoolVar("") for j in range(c)]
        for j in range(c):
            x=C[t][j]
            mdl.Add(x>=b).OnlyEnforceIf(isH[j]); mdl.Add(x<=n).OnlyEnforceIf(isH[j].Not())
            mdl.Add(x==n).OnlyEnforceIf(isN[j]); mdl.Add(x!=n).OnlyEnforceIf(isN[j].Not())
            mdl.AddImplication(isN[j],isH[j].Not())
        lam=[mdl.NewBoolVar("") for j in range(c+1)]; mdl.Add(lam[0]==e1)
        for j in range(c):
            z=mdl.NewBoolVar(""); mdl.AddMultiplicationEquality(z,[isN[j],lam[j]]); mdl.Add(lam[j+1]==isH[j]+z)
        R=[mdl.NewBoolVar("") for k in range(c+1)]      # R[k]=rho_{k-1}; rho_{c-1}=R[c]
        mdl.Add(R[c]==e1)                                # default above the top = e1
        for j in range(c-1,-1,-1):
            z=mdl.NewBoolVar(""); mdl.AddMultiplicationEquality(z,[isN[j],R[j+1]]); mdl.Add(R[j]==isH[j]+z)
        mdl.Add(R[0]==1-e1)                              # e2 = rho_{-1} = 1 - e1
        rho=lambda j: R[j+1]
        # next array before trimming
        cn=c+g
        Cn=[]
        for j in range(cn):
            if not g:
                expr=2*C[t][j]+lam[j]+rho(j)-b*(lam[j+1]+rho(j-1))
            else:
                y_term=n*(1-rho(-1)) if False else None
                if j==0 or j==c:
                    # y + DC_0 ;  y = n(1-e2) = n*(1-(1-e1)) = n*e1
                    expr=C[t][0]+lam[0]-b*lam[1]+n*e1
                else:
                    expr=C[t][j]+lam[j]-b*lam[j+1]+C[t][j-1]+rho(j-1)-b*rho(j-2)
            Cn.append(expr)
        # trim v cells each side must be n ; remaining must equal C[t+1]
        for j in range(v): 
            mdl.Add(Cn[j]==n); mdl.Add(Cn[cn-1-j]==n)
        for j in range(cn-2*v): mdl.Add(C[t+1][j]==Cn[j+v])
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_workers=workers
    st=s.Solve(mdl); nm=s.StatusName(st)
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        return nm,[[s.Value(x) for x in C[t]] for t in range(p)]
    return nm,None

def vschedules(p,total):
    for combo in itertools.combinations_with_replacement(range(p),total):
        v=[0]*p
        for i in combo: v[i]+=1
        yield tuple(v)

def search_C(b,e1s,gams,c_range,tl=10,verbose=False,vmax=None):
    p=len(e1s); k=sum(gams)
    if k%2: return None
    for vs in vschedules(p,k//2):
        for c0 in c_range:
            nm,sol=solve_C(b,e1s,gams,c0,vs,tl)
            if sol: return (c0,vs,sol)
    return None

if __name__=="__main__":
    pass
