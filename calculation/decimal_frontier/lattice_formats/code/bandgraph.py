import sys, itertools, collections
sys.path.insert(0,'/home/claude/research/w3_formats/code')
from gt import norm, primitive
b = int(sys.argv[1]) if len(sys.argv)>1 else 10
mmax = int(sys.argv[2]) if len(sys.argv)>2 else 3
def fixedcarry(w):
    f0 = norm(b,w,0)[1]; f1 = norm(b,w,1)[1]
    return f0,f1
def succ(w, gam):
    m=len(w)
    f0,f1 = fixedcarry(w)
    if f0==0 and f1==1: return None   # neutral (transparent) band: depends on carries
    cs = f0 if f0==f1 else None
    # lower band steady carry: const map -> value
    cs = f0
    wr = w[::-1]
    g0,g1 = fixedcarry(wr)
    if g0==0 and g1==1: return None
    cs2 = g0
    # steady carry-in to a copy is the fixed point c*: const map f: c*=f(.)=f0 (since const)
    dl,_ = norm(b,w,cs)
    du,_ = norm(b,wr,cs2)
    if gam==0: nw = tuple(dl[i]+du[m-1-i] for i in range(m))
    else: nw = tuple(dl[i]+du[(m-i)%m] for i in range(m))
    u,r = primitive(nw)
    return u
nodes=set(); edges={}
for m in range(1,mmax+1):
    for w in itertools.product(range(2*b-1), repeat=m):
        u,r = primitive(w)
        if u!=w: continue
        nodes.add(w)
for w in list(nodes):
    es=[]
    for gam in (0,1):
        s = succ(w,gam)
        if s is not None: es.append((gam,s))
    edges[w]=es
# find cycles: SCC via tarjan on reachable graph (successors may have length < m but still nodes)
import sys
sys.setrecursionlimit(100000)
idx={};low={};st=[];on=set();sccs=[];c=[0]
allnodes=set(edges)
for w in list(edges):
    for g,s in edges[w]:
        if s not in edges:
            e=[]
            for gam in (0,1):
                t=succ(s,gam)
                if t is not None: e.append((gam,t))
            edges[s]=e
def dfs(v):
    idx[v]=low[v]=c[0];c[0]+=1;st.append(v);on.add(v)
    for g,s in edges.get(v,[]):
        if s not in idx:
            dfs(s);low[v]=min(low[v],low[s])
        elif s in on: low[v]=min(low[v],idx[s])
    if low[v]==idx[v]:
        comp=[]
        while True:
            x=st.pop();on.discard(x);comp.append(x)
            if x==v:break
        sccs.append(comp)
for v in list(edges):
    if v not in idx: dfs(v)
print("base",b,"max period",mmax,"nodes",len(edges))
for comp in sccs:
    if len(comp)>1 or any(s==comp[0] for g,s in edges[comp[0]]):
        print("SCC size",len(comp),sorted(comp)[:12], [ (g,s) for w in comp[:3] for g,s in edges[w]][:6])

print("--- SCCs closed under both gam=0 and gam=1 (every successor stays inside):")
for comp in sccs:
    cs=set(comp)
    if len(comp)==1 and not any(s==comp[0] for g,s in edges[comp[0]]): continue
    closed = all(len(edges[w])==2 and all(s in cs for g,s in edges[w]) for w in comp)
    if closed: print("  CLOSED SCC", sorted(comp))
