"""Relaxed B-system: only the bottom K cells must be periodic (top cells free, no vacuum padding).
Shows how much of B can be periodic before the top edge forces failure."""
import sys
from ortools.sat.python import cp_model
def solve_relaxed(b,p,M,K,tl=20,min_gam=1,fix_gam=None,top=False):
    n=b-1; mdl=cp_model.CpModel()
    V=[[mdl.NewIntVar(0,2*n,f"V{t}_{i}") for i in range(M)] for t in range(p+1)]
    gamv=[mdl.NewBoolVar(f"g{t}") for t in range(p)]
    if not top:
        for i in range(K): mdl.Add(V[p][i]==V[0][i])
    else:
        for i in range(M-K,M): mdl.Add(V[p][i]==V[0][i])
        for t in range(p+1): mdl.Add(V[t][M-1]==n); mdl.Add(V[t][M-2]==n)
    mdl.Add(V[0][0]>=1)
    for t in range(p):
        isH=[mdl.NewBoolVar("") for i in range(M)]; isN=[mdl.NewBoolVar("") for i in range(M)]
        for i in range(M):
            v=V[t][i]
            mdl.Add(v>=b).OnlyEnforceIf(isH[i]); mdl.Add(v<=n).OnlyEnforceIf(isH[i].Not())
            mdl.Add(v==n).OnlyEnforceIf(isN[i]); mdl.Add(v!=n).OnlyEnforceIf(isN[i].Not())
            mdl.AddImplication(isN[i],isH[i].Not())
        lam=[mdl.NewBoolVar("") for i in range(M+1)]; mdl.Add(lam[0]==0)
        for i in range(M):
            z=mdl.NewBoolVar(""); mdl.AddMultiplicationEquality(z,[isN[i],lam[i]]); mdl.Add(lam[i+1]==isH[i]+z)
        R=[mdl.NewBoolVar("") for k in range(M+1)]
        mdl.Add(R[M]==1-lam[M])
        for i in range(M-1,-1,-1):
            z=mdl.NewBoolVar(""); mdl.AddMultiplicationEquality(z,[isN[i],R[i+1]]); mdl.Add(R[i]==isH[i]+z)
        mdl.Add(R[0]==gamv[t]); rho=lambda i: R[i+1]
        for i in range(M-1 if not top else M):   # top cell M-1 of next row left free (truncation) unless top-window mode
            non=2*V[t][i]+lam[i]+rho(i)-b*(lam[i+1]+rho(i-1))
            ovf=(V[t][0]-b*lam[1]+1) if i==0 else (V[t][i]+lam[i]-b*lam[i+1]+V[t][i-1]+rho(i-1)-b*rho(i-2))
            mdl.Add(V[t+1][i]==non).OnlyEnforceIf(gamv[t].Not()); mdl.Add(V[t+1][i]==ovf).OnlyEnforceIf(gamv[t])
    mdl.Add(sum(gamv)>=min_gam)
    if fix_gam: 
        for t,g in enumerate(fix_gam): mdl.Add(gamv[t]==g)
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_workers=1
    st=s.Solve(mdl); nm=s.StatusName(st)
    return nm, ([s.Value(g) for g in gamv] if st in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None)
if __name__=="__main__":
    b=int(sys.argv[1]); p=int(sys.argv[2]); M=int(sys.argv[3])
    for K in range(1,M):
        nm,g=solve_relaxed(b,p,M,K,15)
        print(f"base {b} p={p} M={M} K={K}: {nm} gam={g}",flush=True)
        if nm=='INFEASIBLE': break
