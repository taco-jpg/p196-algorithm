#!/usr/bin/env python3
"""K-head time-domain graph: states = (x_t[0..K-1]) with x_0>=1, edges labelled g (overflow) with free bit h = H_t[K].  Exactly the first K layers of the
position automaton of bx (a necessary condition for any B-cycle of width >= K; narrower widths are NOT covered, see EXTERIOR.md).
usage: khead.py K [b]   -> prints edge count, min/max cycle mean of g, and for label patterns (01)^k, (0001)^k the periods of the labelled SCCs"""
import sys, itertools
from fractions import Fraction
K=int(sys.argv[1]); b=int(sys.argv[2]) if len(sys.argv)>2 else 10
NX=2*b-1
def edges():
    E=[]
    for x in itertools.product(range(NX),repeat=K):
        if x[0]==0: continue
        for h in (0,1):
            H=[0]*(K+1); H[K]=h
            for i in range(K-1,-1,-1): H[i]=(x[i]+H[i+1])//b
            g=H[0]
            L=[0]*(K+1)
            for i in range(K): L[i+1]=(x[i]+L[i])//b
            y=[]
            for i in range(K):
                if g: part = 1 if i==0 else (x[i-1]+H[i])%b
                else: part = (x[i]+H[i+1])%b
                y.append((x[i]+L[i])%b+part)
            E.append((x,tuple(y),g))
    return E
E=edges()
print('K',K,'edges',len(E))
if K==1:
    print('K=1 edges (expect 36 for b=10):',len(E))
# --- labelled-pattern graphs: state (x, phase) ---
def pattern_graph(pat):
    P=len(pat); out={}
    for (x,y,g) in E:
        for ph in range(P):
            if pat[ph]==g: out.setdefault((x,ph),[]).append((y,(ph+1)%P))
    return out
import math
def scc_periods(out):
    # Tarjan iterative
    idx={}; low={}; st=[]; on=set(); comps=[]; counter=[0]
    nodes=set(out)|{n for v in out.values() for n in v}
    sys.setrecursionlimit(1000000)
    def strong(v):
        stack=[(v,iter(out.get(v,())))]; idx[v]=low[v]=counter[0]; counter[0]+=1; st.append(v); on.add(v)
        while stack:
            u,it=stack[-1]; adv=False
            for w in it:
                if w not in idx:
                    idx[w]=low[w]=counter[0]; counter[0]+=1; st.append(w); on.add(w); stack.append((w,iter(out.get(w,())))); adv=True; break
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
    for v in nodes:
        if v not in idx: strong(v)
    res=[]
    for comp in comps:
        cs=set(comp)
        if len(comp)==1 and comp[0] not in out.get(comp[0],()): continue
        # period = gcd of (dist[u]+1-dist[v]) over edges inside comp
        root=comp[0]; dist={root:0}; q=[root]; gg=0
        for u in q:
            for w in out.get(u,()):
                if w not in cs: continue
                if w not in dist: dist[w]=dist[u]+1; q.append(w)
                else: gg=math.gcd(gg,dist[u]+1-dist[w])
        res.append((len(comp),gg))
    return res
for pat in ([0,1],[0,0,0,1]):
    out=pattern_graph(pat)
    # restrict to nodes that lie in a cycle (SCC with a cycle)
    r=scc_periods(out)
    print('pattern',''.join(map(str,pat)),'cyclic SCCs (size, period of labelled walk length incl. phase):',sorted(r,reverse=True)[:12])
