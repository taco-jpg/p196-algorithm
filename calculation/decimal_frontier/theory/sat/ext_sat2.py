#!/usr/bin/env python3
"""Exterior B-cycle CSP, variables F,R in [0,b-1], carries c,d in {0,1} only (B eliminated):
   B_t[k] = b*c_t[k] + F_t[k] - c_t[k-1]  = b*d_t[k] + R_t[k] - d_t[k+1];  next B_{t+1}[k] = F_t[k]+R_t[k] (gam=0) | F_t[k]+R_t[k-1] (gam=1,k>=1), F_t[0]+1 (k=0).
usage: ext_sat2.py b g K tlim [--prim d] [--e estring]"""
import sys, time
from ortools.sat.python import cp_model
b=int(sys.argv[1]); g=[int(ch) for ch in sys.argv[2]]; K=int(sys.argv[3]); tlim=float(sys.argv[4]); p=len(g)
prim=int(sys.argv[sys.argv.index('--prim')+1]) if '--prim' in sys.argv else None
estr=sys.argv[sys.argv.index('--e')+1] if '--e' in sys.argv else None
margin=2
m=cp_model.CpModel()
F=[[m.NewIntVar(0,b-1,f"F{t}_{k}") for k in range(K)] for t in range(p)]
R=[[m.NewIntVar(0,b-1,f"R{t}_{k}") for k in range(K)] for t in range(p)]
c=[[m.NewBoolVar(f"c{t}_{k}") for k in range(K)] for t in range(p)]
d=[[m.NewBoolVar(f"d{t}_{k}") for k in range(K+1)] for t in range(p)]
def Bexpr(t,k): return b*c[t][k]+F[t][k]-(c[t][k-1] if k>0 else 0)
for t in range(p):
    for k in range(K):
        m.Add(Bexpr(t,k)==b*d[t][k]+R[t][k]-d[t][k+1])
        m.Add(Bexpr(t,k)>=0); m.Add(Bexpr(t,k)<=2*b-2)
        if k>=K-margin: m.Add(Bexpr(t,k)==b-1)
    m.Add(d[t][K]==1-c[t][K-1]); m.Add(d[t][0]==g[t]); m.Add(Bexpr(t,0)>=1)
    if estr: m.Add(c[t][K-1]==int(estr[t]))
    t2=(t+1)%p
    for k in range(K):
        if g[t]==0: m.Add(Bexpr(t2,k)==F[t][k]+R[t][k])
        else: m.Add(Bexpr(t2,k)==(F[t][0]+1 if k==0 else F[t][k]+R[t][k-1]))
if prim:
    diffs=[]
    for t in range(p):
        for k in range(K-margin):
            z=m.NewBoolVar(f"z{t}_{k}")
            m.Add(Bexpr(t,k)!=Bexpr((t+prim)%p,k)).OnlyEnforceIf(z); diffs.append(z)
    m.AddBoolOr(diffs)
s=cp_model.CpSolver(); s.parameters.num_workers=1; s.parameters.max_time_in_seconds=tlim; s.parameters.random_seed=1
t0=time.time(); st=s.Solve(m); name=s.StatusName(st)
print(f"b={b} g={sys.argv[2]} K={K} prim={prim}: {name} in {time.time()-t0:.1f}s",flush=True)
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    print("e1:",''.join(str(s.Value(c[t][K-1])) for t in range(p)))
    for t in range(p):
        row=[s.Value(b*c[t][k]+F[t][k]-(c[t][k-1] if k>0 else 0)) for k in range(K)]
        while row and row[-1]==b-1: row.pop()
        print(t,len(row),row)
