import os
"""Relaxed C-system (valid for ALL lengths c_t >= K+margin): only the K cells next to the lower edge of C must be periodic
(in the frame that drifts right by v_t at each trim); top boundary bits free; no symmetry/centre constraint.
Infeasible => no C-cycle with this (e1,gam,v) schedule for any large centre.   usage via function c_window_feasible"""
import sys, itertools
from ortools.sat.python import cp_model
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
def c_window_feasible(b,e1s,gams,vs,K,extra=4,tl=20,workers=1):
    n=b-1; p=len(e1s); s=[0]
    for t in range(p): s.append(s[-1]+vs[t])
    ktot=s[p]; M=K+ktot+extra
    mdl=cp_model.CpModel()
    V=[[mdl.NewIntVar(0,2*n,"") for j in range(M)] for t in range(p+1)]
    for t in range(p+1):
        for j in range(min(s[t],M)): mdl.Add(V[t][j]==n)
    for j in range(K): mdl.Add(V[p][j+ktot]==V[0][j])
    for t in range(p):
        e1=e1s[t]; g=gams[t]
        isH=[mdl.NewBoolVar("") for j in range(M)]; isN=[mdl.NewBoolVar("") for j in range(M)]
        for j in range(M):
            x=V[t][j]
            mdl.Add(x>=b).OnlyEnforceIf(isH[j]); mdl.Add(x<=n).OnlyEnforceIf(isH[j].Not())
            mdl.Add(x==n).OnlyEnforceIf(isN[j]); mdl.Add(x!=n).OnlyEnforceIf(isN[j].Not())
            mdl.AddImplication(isN[j],isH[j].Not())
        lam=[mdl.NewBoolVar("") for j in range(M+1)]; mdl.Add(lam[0]==e1)
        for j in range(M):
            z=mdl.NewBoolVar(""); mdl.AddMultiplicationEquality(z,[isN[j],lam[j]]); mdl.Add(lam[j+1]==isH[j]+z)
        R=[mdl.NewBoolVar("") for k in range(M+1)]           # R[k]=rho_{k-1}; top boundary R[M] free
        for j in range(M-1,-1,-1):
            z=mdl.NewBoolVar(""); mdl.AddMultiplicationEquality(z,[isN[j],R[j+1]]); mdl.Add(R[j]==isH[j]+z)
        mdl.Add(R[0]==1-e1)
        rho=lambda j: R[j+1]
        for j in range(M-1):
            if not g: expr=2*V[t][j]+lam[j]+rho(j)-b*(lam[j+1]+rho(j-1))
            elif j==0: expr=V[t][0]+lam[0]-b*lam[1]+n*e1
            else: expr=V[t][j]+lam[j]-b*lam[j+1]+V[t][j-1]+rho(j-1)-b*rho(j-2)
            mdl.Add(V[t+1][j]==expr)
    sv=cp_model.CpSolver(); sv.parameters.max_time_in_seconds=tl; sv.parameters.num_workers=workers
    st=sv.Solve(mdl); return sv.StatusName(st)

def vschedules(p,total):
    for combo in itertools.combinations_with_replacement(range(p),total):
        v=[0]*p
        for i in combo: v[i]+=1
        yield tuple(v)
