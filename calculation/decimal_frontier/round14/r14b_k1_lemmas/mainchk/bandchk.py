#!/usr/bin/env python3
"""Main-session check of r14b section 5: closure of the band-anchored relaxation R^B_K, written from the definition (full enumeration, K <= 3)."""
import sys, itertools
sys.setrecursionlimit(1000000)
clk = [1, 0, 1, 0, 1, 0, 1, 0]
tp = 8
def row_step(x, g):
    n = len(x)
    al = [0]*n
    for _ in range(n+2):
        for c in range(n): al[(c+1)%n] = 1 if x[c]+al[c] >= 10 else 0
    be = [0]*n
    for _ in range(n+2):
        for c in range(n-1,-1,-1): be[c] = 1 if x[c]+be[(c+1)%n] >= 10 else 0
    lo = [(x[c]+al[c])%10 for c in range(n)]
    hi = [(x[c]+be[(c+1)%n])%10 for c in range(n)]
    return [lo[c]+(hi[(c-1)%n] if g else hi[c]) for c in range(n)], al, be
def analyse(V, Kmax):
    m = len(V)
    B = [list(V)]; UP = []; DN = []
    for t in range(tp):
        y, al, be = row_step(B[t], clk[t]); B.append(y); UP.append(al); DN.append(be)
    assert B[tp] == B[0], 'not 8-periodic'
    res = []
    seen = set(); 
    phases = [(t,j,par) for t in range(tp) for j in range(m) for par in (0,1)]
    orbits = []
    for ph in phases:
        if ph in seen: continue
        o = []; cur = ph
        while cur not in seen:
            seen.add(cur); o.append(cur)
            t,j,par = cur; g = clk[t]; dh = 1 if g==1 and par==0 else 0
            cur = ((t+1)%tp, (j+dh)%m, (par+g)%2)
        orbits.append(o)
    out = []
    for o in orbits:
        K0 = None
        counts = []
        for K in range(1, Kmax+1):
            states = [(l, w) for l in range(len(o)) for w in itertools.product(range(19), repeat=K)]
            adj = {}
            for (l, w) in states:
                t,j,par = o[l]; g = clk[t]; dh = 1 if g==1 and par==0 else 0
                tn = (t+1)%tp
                suc = set()
                bv = B[t][j]; dn = DN[t][(j+1)%m]   # DN[t][c] is the carry OUT of c (row_step); the carry INTO cell j from above is DN[t][j+1]
                Din = 1 if bv + dn >= 10 else 0
                r = [0]*K; b = Din
                for i in range(K-1,-1,-1):
                    s = w[i]+b; r[i] = s%10; b = 1 if s>=10 else 0
                for a_in in (0,1):
                    a = a_in; e = [0]*K
                    for i in range(K):
                        s = w[i]+a; e[i] = s%10; a = 1 if s>=10 else 0
                    EB = (bv + a)%10; RB = (bv + dn)%10
                    if g == 0:
                        if EB + RB != B[tn][j]: continue
                        suc.add(tuple(e[i]+r[i] for i in range(K)))
                    elif dh == 0:
                        if EB + r[K-1] != B[tn][j]: continue
                        for r_in in range(10):
                            suc.add(tuple((e[0]+r_in) if i==0 else e[i]+r[i-1] for i in range(K)))
                    else:
                        if bv == 9 and a != UP[t][j]: continue
                        suc.add(tuple([e[i+1]+r[i] for i in range(K-1)]+[EB+r[K-1]]))
                nl = (l+1)%len(o)
                adj[(l,w)] = [(nl,x) for x in suc]
            # Tarjan on the explicit graph
            index={}; low={}; on=set(); st=[]; cnt=0; comps=[]
            for root in adj:
                if root in index: continue
                work=[(root,iter(adj[root]))]; index[root]=low[root]=cnt; cnt+=1; st.append(root); on.add(root)
                while work:
                    u,it=work[-1]; adv=False
                    for v in it:
                        if v not in index:
                            index[v]=low[v]=cnt; cnt+=1; st.append(v); on.add(v); work.append((v,iter(adj[v]))); adv=True; break
                        elif v in on: low[u]=min(low[u],index[v])
                    if adv: continue
                    work.pop()
                    if work:
                        p=work[-1][0]; low[p]=min(low[p],low[u])
                    if low[u]==index[u]:
                        c=[]
                        while True:
                            x=st.pop(); on.discard(x); c.append(x)
                            if x==u: break
                        comps.append(c)
            total=0
            for c in comps:
                if len(c)==1 and c[0] not in adj[c[0]]: continue
                fl=False
                for (l,w) in c:
                    t,j,par=o[l]
                    if w[K-1]!=B[t][(j-1)%m]: fl=True; break
                if fl: total+=len(c)
            counts.append(total)
            if total==0:
                K0=K; break
        out.append((K0,counts))
    return out
for arg in sys.argv[2:]:
    V=[int(x) for x in arg.split(',')]
    print(arg, analyse(V,int(sys.argv[1])),flush=True)
