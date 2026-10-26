"""CP-SAT model for C-survival/cycle under a given driver stream.  usage:
 python3 ccp.py b e g m0 v [timelimit]    e.g. python3 ccp.py 11 101101 100100 42 000001
 e,g: driver bits per step (full joint period), v: trim pattern per step (v_t each side); m_{t+1}=m_t+g_t-2v_t must close to m0."""
import sys
from ortools.sat.python import cp_model
def solve_c(b,e,g,m0,v,tl=60,workers=1):
    P=len(e); ms=[m0]
    for t in range(P): ms.append(ms[-1]+int(g[t])-2*int(v[t]))
    if ms[-1]!=m0 or min(ms)<1: return 'badlen',None
    M=cp_model.CpModel()
    C=[[M.NewIntVar(0,2*b-2,f"C{t}_{i}") for i in range(ms[t])] for t in range(P)]
    for t in range(P):
        m=ms[t]
        for i in range(m//2): M.Add(C[t][i]==C[t][m-1-i])
        et=int(e[t]); gt=int(g[t]); vt=int(v[t])
        l=[M.NewBoolVar(f"l{t}_{i}") for i in range(m+1)]
        M.Add(l[0]==et); M.Add(l[m]==1-et)
        DC=[M.NewIntVar(0,b-1,f"D{t}_{i}") for i in range(m)]
        for i in range(m): M.Add(C[t][i]+l[i]==DC[i]+b*l[i+1])
        yd=(b-1)*et
        nm=m+gt; tgt=C[(t+1)%P]
        for k in range(nm):
            if gt==0: val=DC[k]+DC[m-1-k]
            else:
                f=DC[k] if k<m else yd
                s=yd if k==0 else DC[m-k]
                val=f+s
            if vt<=k<nm-vt: M.Add(tgt[k-vt]==val)
            else: M.Add(val==b-1)
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_workers=workers
    r=s.Solve(M); name=s.StatusName(r)
    if r in (cp_model.OPTIMAL,cp_model.FEASIBLE): return name,[[s.Value(x) for x in C[t]] for t in range(P)]
    return name,None
if __name__=="__main__":
    b=int(sys.argv[1]);e=sys.argv[2];g=sys.argv[3];m0=int(sys.argv[4]);v=sys.argv[5];tl=float(sys.argv[6]) if len(sys.argv)>6 else 60
    print(solve_c(b,e,g,m0,v,tl))
