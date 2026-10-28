#!/usr/bin/env python3
"""Exterior B-cycle as a time-periodic CSP (CP-SAT, 1 worker).  Unknown array B_t[k], t in Z_p, k=0..K-1 (digits 0..2b-2), forward carries c, backward carries d.
Band: B_t[k]=b-1 for k>=K-margin.  Rule (Lemma 1): F=(B+c_{k-1}) mod b, R=(B+d_{k+1}) mod b, gam_t=d_t[0]=g_t given,
  gam=0: B_{t+1}[k]=F[k]+R[k] ; gam=1: B_{t+1}[0]=F[0]+1, B_{t+1}[k]=F[k]+R[k-1].  Top: d[K]=1-c[K-1] (so e1=c[K-1]).  B_t[0]>=1.
usage: ext_sat.py b gstring K tlim [--prim d]   (--prim d : forbid B_{t+d}=B_t for all t, i.e. solution not d-periodic; d | p)"""
import sys, time
from ortools.sat.python import cp_model
b=int(sys.argv[1]); g=[int(c) for c in sys.argv[2]]; K=int(sys.argv[3]); tlim=float(sys.argv[4]); p=len(g)
prim=None
if '--prim' in sys.argv: prim=int(sys.argv[sys.argv.index('--prim')+1])
margin=2
m=cp_model.CpModel()
B=[[m.NewIntVar(0,2*b-2,f"B{t}_{k}") for k in range(K)] for t in range(p)]
c=[[m.NewIntVar(0,1,f"c{t}_{k}") for k in range(K)] for t in range(p)]       # carry out of position k (forward)
d=[[m.NewIntVar(0,1,f"d{t}_{k}") for k in range(K+1)] for t in range(p)]     # d[k] = backward carry out of position k (into k-1); d[K] = carry into top
F=[[m.NewIntVar(0,b-1,f"F{t}_{k}") for k in range(K)] for t in range(p)]
R=[[m.NewIntVar(0,b-1,f"R{t}_{k}") for k in range(K)] for t in range(p)]
for t in range(p):
    for k in range(K):
        cin = c[t][k-1] if k>0 else 0
        m.Add(B[t][k]+cin==b*c[t][k]+F[t][k])
        m.Add(B[t][k]+d[t][k+1]==b*d[t][k]+R[t][k])
        if k>=K-margin: m.Add(B[t][k]==b-1)
    m.Add(d[t][K]==1-c[t][K-1])
    m.Add(d[t][0]==g[t])
    m.Add(B[t][0]>=1)
    t2=(t+1)%p
    for k in range(K):
        if g[t]==0: m.Add(B[t2][k]==F[t][k]+R[t][k])
        else:
            if k==0: m.Add(B[t2][0]==F[t][0]+1)
            else: m.Add(B[t2][k]==F[t][k]+R[t][k-1])
if prim:
    diffs=[]
    for t in range(p):
        for k in range(K-margin):
            z=m.NewBoolVar(f"z{t}_{k}")
            # z => B[t][k] != B[(t+prim)%p][k]
            m.Add(B[t][k]!=B[(t+prim)%p][k]).OnlyEnforceIf(z)
            diffs.append(z)
    m.AddBoolOr(diffs)
s=cp_model.CpSolver(); s.parameters.num_workers=1; s.parameters.max_time_in_seconds=tlim; s.parameters.random_seed=1
t0=time.time(); st=s.Solve(m)
name=s.StatusName(st)
print(f"b={b} g={sys.argv[2]} K={K} prim={prim}: {name} in {time.time()-t0:.1f}s")
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    e=''.join(str(s.Value(c[t][K-1])) for t in range(p)); print("e1 stream:",e)
    for t in range(p):
        row=[s.Value(B[t][k]) for k in range(K)]
        while row and row[-1]==b-1: row.pop()
        print(t,len(row),row)
