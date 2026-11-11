#!/usr/bin/env python3
# Independent check (python): chain graph of d-periodic interfaces from the root interface (phases Z/d, clock g periodic), longest chain / cycle detection.
# D(root) = longest chain from the root; closed d-walks at level K exist iff K <= D(root); K-head graph dies at level D(root)+1 (if no cycle).
import sys
sys.setrecursionlimit(1000000)
b=10; NV=19
def succs(I, g, d):
    c,xb,A,root=I
    # columns: closed d-walks above interface I; A[t] set bitmask of allowed H
    def step(t,v):
        res={}
        for h in (0,1):
            H=(v+h)//b
            if not (A[t]>>H)&1: continue
            part = (1 if root else (xb[t]+H)%b) if g[t%len(g)] else (v+h)%b
            y=(v+c[t])%b+part
            if root and y<1: continue
            res.setdefault(y,0); res[y]|=1<<h
        return res
    out=[]
    # enumerate closed walks by DFS with reachability pruning
    # backward reach masks
    R=[[0]*NV for _ in range(d+1)]
    for v in range(NV): R[d][v]=1<<v
    for t in range(d-1,-1,-1):
        for v in range(NV):
            if root and v<1: continue
            m=0
            for y in step(t,v): m|=R[t+1][y]
            R[t][v]=m
    for v0 in range(NV):
        if root and v0<1: continue
        if not (R[0][v0]>>v0)&1: continue
        col=[v0]; hs=[]
        def dfs(t):
            if t==d:
                if col[d]==v0:
                    c2=tuple((col[i]+c[i])//b for i in range(d))
                    xb2=tuple(col[i]%b if g[i%len(g)] else 0 for i in range(d))
                    out.append((c2,xb2,tuple(hs)))
                return
            for y,m in step(t,col[t]).items():
                if (R[t+1][y]>>v0)&1:
                    col.append(y); hs.append(m); dfs(t+1); col.pop(); hs.pop()
        dfs(0)
    return out
def run(gw, d):
    g=[int(ch) for ch in gw]
    root=(tuple([0]*d), tuple([-1]*d), tuple(1<<g[t%len(g)] for t in range(d)), True)
    D={}; onstack=set(); cyc=False
    def val(I):
        nonlocal cyc
        if I in D: return D[I]
        if I in onstack: cyc=True; return 10**9
        onstack.add(I); best=0; 
        for J in succs(I,g,d):
            r=val(J+(False,))
            best=max(best, min(10**9, r+1))
        onstack.discard(I); D[I]=best; return best
    r=val(root)
    print(gw, 'd=',d,'interfaces visited',len(D),'cycle:',cyc,'D(root)=',r,'-> K-head dies at',r+1 if not cyc else None)
if __name__=='__main__':
    for arg in sys.argv[1:]:
        gw,dd=arg.split(':'); run(gw,int(dd))
