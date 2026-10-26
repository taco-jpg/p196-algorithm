"""B-system periodic-orbit finder (CP-SAT).  Necessary condition for any neutral-band certificate:
the autonomous block B (feedback e2 = 1-e1) must be periodic.  Unknown: B^(t), t<p, vacuum-padded to M cells.
usage: python3 bcycle_cpsat.py base p M [timelimit_s] [workers]   prints SAT/UNSAT/UNKNOWN and the cycle."""
import sys, time
from ortools.sat.python import cp_model
sys.path.insert(0,'.')
from lib import *

def solve_B(b,p,M,tl=60,workers=1,min_gam=1,fix_gam=None,verbose=False,free_e2=False):
    n=b-1; mdl=cp_model.CpModel()
    V=[[mdl.NewIntVar(0,2*n,f"V{t}_{i}") for i in range(M)] for t in range(p)]
    gamv=[mdl.NewBoolVar(f"g{t}") for t in range(p)]
    for t in range(p):
        mdl.Add(V[t][M-1]==n); mdl.Add(V[t][M-2]==n); mdl.Add(V[t][0]>=1)
        isH=[mdl.NewBoolVar(f"H{t}_{i}") for i in range(M)]
        isN=[mdl.NewBoolVar(f"N{t}_{i}") for i in range(M)]
        for i in range(M):
            v=V[t][i]
            mdl.Add(v>=b).OnlyEnforceIf(isH[i]); mdl.Add(v<=n).OnlyEnforceIf(isH[i].Not())
            mdl.Add(v==n).OnlyEnforceIf(isN[i]); mdl.Add(v!=n).OnlyEnforceIf(isN[i].Not())
            mdl.AddImplication(isN[i],isH[i].Not())
        lam=[mdl.NewBoolVar(f"l{t}_{i}") for i in range(M+1)]
        mdl.Add(lam[0]==0)
        for i in range(M):
            z=mdl.NewBoolVar(f"zl{t}_{i}"); mdl.AddMultiplicationEquality(z,[isN[i],lam[i]])
            mdl.Add(lam[i+1]==isH[i]+z)
        # r[i+1] stands for rho_i ; r index shift by 2 so r[0]=rho_{-2}? we need rho_{-1}, rho_{-2}: define array R of size M+2: R[k]=rho_{k-1}, k=0..M+1 ; R[0]=rho_{-1}=gam ; rho_{M-1}=R[M]
        R=[mdl.NewBoolVar(f"r{t}_{k}") for k in range(M+1)]
        if not free_e2: mdl.Add(R[M]==1-lam[M])                  # rho_{M-1} = e2 = 1-e1
        for i in range(M-1,-1,-1):               # rho_{i-1} = isH_i + isN_i*rho_i   -> R[i] = ...R[i+1]
            z=mdl.NewBoolVar(f"zr{t}_{i}"); mdl.AddMultiplicationEquality(z,[isN[i],R[i+1]])
            mdl.Add(R[i]==isH[i]+z)
        mdl.Add(R[0]==gamv[t])
        rho=lambda i: R[i+1]                     # rho_i
        # rho_{-2} needed for overflow i=1:  R[-1] -> use gam (rho_{-1}) per derivation r[i-2] at i=1 is rho_{-1}=gam
        Vn=V[(t+1)%p]
        for i in range(M):
            nonovf=2*V[t][i]+lam[i]+rho(i)-b*(lam[i+1]+rho(i-1))
            if i==0:
                ovf=V[t][0]-b*lam[1]+1
            else:
                r2=rho(i-2) if i-2>=-1 else None
                ovf=V[t][i]+lam[i]-b*lam[i+1]+V[t][i-1]+rho(i-1)-b*rho(i-2)
            mdl.Add(Vn[i]==nonovf).OnlyEnforceIf(gamv[t].Not())
            mdl.Add(Vn[i]==ovf).OnlyEnforceIf(gamv[t])
    mdl.Add(sum(gamv)>=min_gam)
    if fix_gam is not None:
        for t,g in enumerate(fix_gam): mdl.Add(gamv[t]==g)
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_workers=workers
    st=s.Solve(mdl)
    name=s.StatusName(st)
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        sol=[[s.Value(V[t][i]) for i in range(M)] for t in range(p)]
        gs=[s.Value(g) for g in gamv]
        return name,sol,gs,s.WallTime()
    return name,None,None,s.WallTime()

def verify(b,sol,gs):
    """replay with the library: autonomous B-system must reproduce the cycle"""
    from decouple import phiB
    n=b-1; p=len(sol)
    cur=list(sol[0])
    while cur and cur[-1]==n: cur.pop()
    out=[]
    for t in range(p):
        nb,u,E1,g=phiB(b,cur); out.append((tuple(cur),E1,g,u)); cur=nb
    first=list(sol[0])
    while first and first[-1]==n: first.pop()
    return cur==first, [o[2] for o in out]==gs, out

if __name__=="__main__":
    b=int(sys.argv[1]); p=int(sys.argv[2]); M=int(sys.argv[3]); tl=float(sys.argv[4]) if len(sys.argv)>4 else 60
    w=int(sys.argv[5]) if len(sys.argv)>5 else 1
    name,sol,gs,wt=solve_B(b,p,M,tl,w)
    print(f"base {b} p={p} M={M}: {name} ({wt:.1f}s)")
    if sol:
        ok1,ok2,out=verify(b,sol,gs)
        print("  library replay returns to start:",ok1," gam pattern matches:",ok2)
        for o in out: print("   B=",list(o[0]),"e1,gam,u=",o[1:])
