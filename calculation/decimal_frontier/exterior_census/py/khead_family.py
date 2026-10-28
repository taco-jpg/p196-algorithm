#!/usr/bin/env python3
"""Family analysis for a repeating label pattern (e.g. 01 or 0001): K-head graph restricted to the pattern, grown one coordinate at a time.
S_K = nodes (x_0..x_{K-1}, phase) lying on cycles of the K-head pattern graph.  Closed walks of length n exist in the K-head graph only inside cyclic SCCs;
all their lengths are multiples of the SCC's period.  If S_K becomes empty at K0, NO word pattern^k has a B-cycle of width >= K0 (any k).
usage: khead_family.py PATTERN [Kmax] [b]"""
import sys, math
pat=[int(c) for c in sys.argv[1]]; P=len(pat); Kmax=int(sys.argv[2]) if len(sys.argv)>2 else 30; b=int(sys.argv[3]) if len(sys.argv)>3 else 10
NX=2*b-1
def trans(x,h):
    K=len(x)
    H=[0]*(K+1); H[K]=h
    for i in range(K-1,-1,-1): H[i]=(x[i]+H[i+1])//b
    g=H[0]; L=[0]*(K+1)
    for i in range(K): L[i+1]=(x[i]+L[i])//b
    y=[]
    for i in range(K):
        part = (1 if i==0 else (x[i-1]+H[i])%b) if g else (x[i]+H[i+1])%b
        y.append((x[i]+L[i])%b+part)
    return tuple(y),g
def cyc_core(out):
    # nodes on cycles + SCC info (iterative Tarjan)
    idx={}; low={}; st=[]; on=set(); comps=[]; cnt=0
    for v0 in list(out):
        if v0 in idx: continue
        stack=[(v0,iter(out.get(v0,())))]; idx[v0]=low[v0]=cnt; cnt+=1; st.append(v0); on.add(v0)
        while stack:
            u,it=stack[-1]; adv=False
            for w in it:
                if w not in idx:
                    idx[w]=low[w]=cnt; cnt+=1; st.append(w); on.add(w); stack.append((w,iter(out.get(w,())))); adv=True; break
                elif w in on: low[u]=min(low[u],idx[w])
            if adv: continue
            stack.pop()
            if stack: low[stack[-1][0]]=min(low[stack[-1][0]],low[u])
            if low[u]==idx[u]:
                comp=[]
                while True:
                    w=st.pop(); on.discard(w); comp.append(w)
                    if w==u: break
                comps.append(comp)
    res=[]
    for comp in comps:
        cs=set(comp)
        if len(comp)==1 and comp[0] not in out.get(comp[0],()): continue
        root=comp[0]; dist={root:0}; q=[root]; gg=0
        for u in q:
            for w in out.get(u,()):
                if w not in cs: continue
                if w not in dist: dist[w]=dist[u]+1; q.append(w)
                else: gg=math.gcd(gg,dist[u]+1-dist[w])
        res.append((comp,gg))
    return res
# K=1 nodes
cands=[((x,),ph) for x in range(1,NX) for ph in range(P)]
S=None
for K in range(1,Kmax+1):
    if K==1: nodes=cands
    else: nodes=[(pre+(xk,),ph) for (pre,ph) in S for xk in range(NX)]
    out={}
    nodeset=set(nodes)
    for (x,ph) in nodes:
        for h in (0,1):
            y,g=trans(x,h)
            if g==pat[ph]:
                nxt=(y,(ph+1)%P)
                out.setdefault((x,ph),[]).append(nxt)
    # keep only edges to existing nodes
    for k in list(out): out[k]=[n for n in out[k] if n in nodeset]
    comps=cyc_core(out)
    S=[n for c,gp in comps for n in c]
    info=sorted([(len(c),gp) for c,gp in comps],reverse=True)
    print(f'K={K}: nodes on cycles {len(S)}, cyclic SCCs (size,period) {info[:8]}{" ..." if len(info)>8 else ""}',flush=True)
    if not S: print('=> family dies at K=%d: no word %s^k has a B-cycle of width >= %d'%(K,sys.argv[1],K)); break
