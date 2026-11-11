#!/usr/bin/env python3
# bandind.py: independent check (different code path: CA c,d,R form with explicit 9-transparency, explicit graph, explicit SCC via networkx-free Kosaraju)
# of the band-anchored closure for window size K <= 3: states = all 19^K windows over every phase; prints per phase-orbit: number of states on cycles through accepting states.
import sys, itertools
sys.setrecursionlimit(100000)
BASE=10
clk=[1,0,1,0,1,0,1,0]
def row_step(row,g):
    # cyclic row exact update using c,d form with 9-transparency: compute a via c chain
    m=len(row)
    def carry_up(x):  # carry into x from below: follow 9s downward
        y=x-1
        for _ in range(m):
            p=row[y%m]
            if p!=9: return 1 if p>=10 else 0
            y-=1
        return None
    def carry_dn(x):  # carry into x from above
        y=x+1
        for _ in range(m):
            p=row[y%m]
            if p!=9: return 1 if p>=10 else 0
            y+=1
        return None
    a=[carry_up(x) for x in range(m)]; b=[carry_dn(x) for x in range(m)]
    if None in a or None in b: return None
    e=[(row[x]+a[x])%10 for x in range(m)]
    r=[(row[x]+b[x])%10 for x in range(m)]
    return tuple(e[x]+r[(x-g)%m] for x in range(m)), a, b
def table(row0):
    r=tuple(row0); rows=[]; UP=[]; DN=[]
    for t in range(8):
        nxt,a,b=row_step(r,clk[t]); rows.append(r); UP.append(a); DN.append(b); r=nxt
    assert r==tuple(row0)
    return rows,UP,DN
def succ_states(ph,w,K,m,B,UP,DN):
    # w: bottom-based tuple of K cells; returns set of new windows (bottom-based) under free a_in, r_in; respects band staying on-band.
    t,je,par=ph; g=clk[t]; dh=(g==1 and par==0); tn=(t+1)%8
    kB=B[t][je]; kBn=B[tn][je]
    Din=DN[t][(je-1)%m]   # carry coming down out of band cell je into window top: equals b_{je-1} of the band
    res=set()
    for a_in in (0,1):
        # ascending chain with 9-transparency: a[i+1] = c(w[i]) unless w[i]==9
        a=[a_in]
        for i in range(K):
            if w[i]!=9: a.append(1 if w[i]>=10 else 0)
            else: a.append(a[-1])
        # descending chain from top: b[K-1]=Din; b[i-1] = c(w[i]) unless w[i]==9
        b=[0]*K; b[K-1]=Din
        for i in range(K-1,0,-1):
            b[i-1]=(1 if w[i]>=10 else 0) if w[i]!=9 else b[i]
        e=[(w[i]+a[i])%10 for i in range(K)]
        r=[(w[i]+b[i])%10 for i in range(K)]
        aK=a[K]
        EB=(kB+aK)%10
        rB=(kB+ (DN[t][je]))%10
        if kB==9 and aK!=UP[t][je]: continue
        if g==0:
            if EB+rB!=kBn: continue
            new=tuple(e[i]+r[i] for i in range(K))
            res.add(new)
        elif not dh:
            if EB+r[K-1]!=kBn: continue
            for rin in range(10):
                new=[0]*K
                new[0]=e[0]+rin
                for i in range(1,K): new[i]=e[i]+r[i-1]
                res.add(tuple(new))
        else:
            new=[0]*K
            for i in range(K-1): new[i]=e[i+1]+r[i]
            new[K-1]=EB+r[K-1]
            res.add(tuple(new))
    return res
def orbits(m):
    seen=set(); orbs=[]
    for t in range(8):
        for j in range(m):
            for p in (0,1):
                if (t,j,p) in seen: continue
                o=[]; cur=(t,j,p)
                while cur not in seen:
                    seen.add(cur); o.append(cur)
                    tt,jj,pp=cur; g=clk[tt]; dh=1 if (g==1 and pp==0) else 0
                    cur=((tt+1)%8,(jj+dh)%m,(pp+g)%2)
                orbs.append(o)
    return orbs
def run(row0,K):
    rows,UP,DN=table(row0); m=len(row0)
    outs={}
    for oi,orb in enumerate(orbits(m)):
        T=len(orb); idx={p:i for i,p in enumerate(orb)}
        # nodes: (l, window); edges via succ
        adj={}
        rev={}
        allw=list(itertools.product(range(19),repeat=K))
        for l,ph in enumerate(orb):
            l2=(l+1)%T
            for w in allw:
                u=(l,w)
                pass
        # (edges computed lazily below)
        # compute SCC via iterative Kosaraju using dictionaries
        # build adjacency first
        allw_set=set(allw)
        adj={}
        for l,ph in enumerate(orb):
            l2=(l+1)%T
            for w in allw:
                adj[(l,w)]=[(l2,nw) for nw in succ_states(ph,w,K,m,rows,UP,DN) if nw in allw_set]
        # iterative trimming then Tarjan: simple approach: repeatedly remove nodes with no in/out edges (core), then SCC via Kosaraju
        nodes=list(adj.keys())
        indeg={n:0 for n in nodes}
        for n in nodes:
            for v in adj[n]:
                indeg[v]+=1
        # Tarjan iterative
        index={}; low={}; on={}; st=[]; comps=[]; cnt=[0]
        for s in nodes:
            if s in index: continue
            work=[(s,iter(adj[s]))]
            index[s]=low[s]=cnt[0]; cnt[0]+=1; st.append(s); on[s]=True
            while work:
                v,it=work[-1]
                for w in it:
                    if w not in index:
                        index[w]=low[w]=cnt[0]; cnt[0]+=1; st.append(w); on[w]=True
                        work.append((w,iter(adj[w]))); break
                    elif on.get(w):
                        low[v]=min(low[v],index[w])
                else:
                    work.pop()
                    if work:
                        p=work[-1][0]; low[p]=min(low[p],low[v])
                    if low[v]==index[v]:
                        comp=[]
                        while True:
                            x=st.pop(); on[x]=False; comp.append(x)
                            if x==v: break
                        comps.append(comp)
        def accepting(l,w):
            t,je,par=orb[l]
            return w[K-1]!=rows[t][(je-1)%m]   # top cell (bottom-based index K-1) off-band
        total=0
        for comp in comps:
            if len(comp)==1:
                v=comp[0]
                if v not in adj[v]: continue
            if any(accepting(l,w) for l,w in comp):
                total+=len(comp)
        outs[oi]=(T,total)
    return outs
if __name__=="__main__":
    row=[int(x) for x in sys.argv[1].split(",")]
    for K in range(1,int(sys.argv[2])+1):
        print("K",K,run(row,K),flush=True)
