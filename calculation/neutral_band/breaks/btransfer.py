import os
"""Exact spatial transfer-automaton decision procedure for B-cycles (autonomous B-system, feedback e2=1-e1).
For a fixed period p and overflow pattern O (gam^(t)), cells of B are added one at a time from the bottom.
State after cell i: (column of cell i over time, lam_{i+1}^(t), rho_i^(t), rho_{i-1}^(t)).  Finite => exact for ALL lengths |B|.
usage: python3 btransfer.py base p [maxstates]   ; reports for every overflow pattern: B-cycle exists / provably none."""
import sys, itertools, collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))

def decide(b,p,O,maxstates=3_000_000,want_path=False):
    n=b-1
    isH=lambda v: 1 if v>=b else 0
    # state tuples
    start=((0,)*p,(0,)*p,tuple(O),(0,)*p)      # pseudo cell -1: V=0, lam_0=0, rho_{-1}=O, rho_{-2}=0
    seen={start:None}; frontier=[start]; first=True; steps=0
    def terminal(st):
        V,lam,rho,rhom1=st
        # last real cell i=m-1: lam=lam_m, rho=rho_{m-1}, rhom1=rho_{m-2}
        for t in range(p):
            if rho[t]!=1-lam[t]: return False
            if O[t] and V[t]+rho[t]-b*rhom1[t]!=n*lam[t]: return False
        return True
    while frontier:
        nxt=[]
        for st in frontier:
            V,lam,rho,rhom1=st
            first_cell=(st is start)
            for v0 in range(1 if first_cell else 0,2*n+1):
                # DFS over time with branching on rho_new bits
                stack=[(0,(v0,),(),())]   # t, vcol, lam_next_col, rho_new_col
                while stack:
                    t,vc,lc,rc=stack.pop()
                    v=vc[-1]
                    if t==p:
                        if vc[-1]!=vc[0]: continue
                        vcol=vc[:p]
                        ns=(vcol,lc,rc,rho)
                        if ns not in seen:
                            seen[ns]=st; nxt.append(ns)
                        continue
                    # consistency: rho_i^(t) must equal polarity seen from this cell
                    if v==n: opts=(rho[t],)
                    else:
                        if isH(v)!=rho[t]: continue
                        opts=(0,1)
                    lam_nx = lam[t] if v==n else isH(v)
                    for rn in opts:
                        if O[t]: nv=v+lam[t]-b*lam_nx+V[t]+rho[t]-b*rhom1[t]
                        else:    nv=2*v+lam[t]+rn-b*(lam_nx+rho[t])
                        if nv<0 or nv>2*n: continue
                        if first_cell and nv<1 : continue
                        stack.append((t+1,vc+(nv,),lc+(lam_nx,),rc+(rn,)))
        if len(seen)>maxstates: return 'LIMIT',len(seen),None
        for ns in nxt:
            if terminal(ns):
                if want_path:
                    path=[]; s=ns
                    while s is not start: path.append(s); s=seen[s]
                    return 'EXISTS',len(seen),path[::-1]
                return 'EXISTS',len(seen),None
        frontier=nxt; steps+=1
    return 'NONE',len(seen),None

def patterns(p,maxo=None):
    seen=set()
    for O in itertools.product((0,1),repeat=p):
        if sum(O)==0: continue
        if maxo and sum(O)>maxo: continue
        key=min(O[i:]+O[:i] for i in range(p))
        if key in seen: continue
        seen.add(key); yield key

def from_path(b,p,path):
    """B at time 0 from the column values"""
    n=b-1
    B=[st[0][0] for st in path]
    while B and B[-1]==n: B.pop()
    return B

if __name__=="__main__":
    b=int(sys.argv[1]); p=int(sys.argv[2]); ms=int(sys.argv[3]) if len(sys.argv)>3 else 2_000_000
    res=collections.Counter(); ex=[]
    for O in patterns(p):
        r,ns,path=decide(b,p,O,ms,want_path=True)
        res[r]+=1
        if r=='EXISTS': ex.append((O,ns,path))
    print(f"base {b} p={p}: overflow patterns (mod rotation) -> {dict(res)}")
    for O,ns,path in ex[:5]:
        B=from_path(b,p,path)
        from decouple import phiB
        cur=list(B); good=True; gs=[]
        for t in range(p):
            nb,u,E1,g=phiB(b,cur); gs.append(g); cur=nb
        print("   pattern",O,"states",ns,"len(B)=",len(B),"B=",B,"library replay returns:",cur==B,"gam matches:",tuple(gs)==O)
