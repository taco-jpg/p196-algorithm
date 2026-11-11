import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r14
sys.setrecursionlimit(1000000)
def build_graph(L, lay):
    T = len(lay)
    idx = [ {w:i for i,w in enumerate(c)} for ph,c in lay ]
    edges = [ [ [] for _ in c ] for ph,c in lay ]
    for l,(ph,c) in enumerate(lay):
        l2 = (l+1) % T
        for i,w in enumerate(c):
            for Din,v,nw in L.succ(ph, w):
                j = idx[l2].get(nw)
                if j is not None:
                    edges[l][i].append((j, Din, v))
    return idx, edges
def nid(off, l, i): return off[l]+i
def sccs(lay, edges):
    T = len(lay)
    off = [0]*(T+1)
    for l,(ph,c) in enumerate(lay): off[l+1] = off[l]+len(c)
    N = off[T]
    adj = [[] for _ in range(N)]
    for l in range(T):
        l2 = (l+1) % T
        for i,es in enumerate(edges[l]):
            u = off[l]+i
            for (j,_,_) in es: adj[u].append(off[l2]+j)
    # iterative Tarjan
    index = [-1]*N; low = [0]*N; on = [False]*N; st=[]; comp=[-1]*N; cnt=0; ncomp=0
    for s in range(N):
        if index[s]!=-1: continue
        work=[(s,0)]
        while work:
            u,pi = work.pop()
            if pi==0:
                index[u]=low[u]=cnt; cnt+=1; st.append(u); on[u]=True
            rec=False
            for k in range(pi,len(adj[u])):
                v=adj[u][k]
                if index[v]==-1:
                    work.append((u,k+1)); work.append((v,0)); rec=True; break
                elif on[v]:
                    low[u]=min(low[u],index[v])
            if rec: continue
            if low[u]==index[u]:
                while True:
                    v=st.pop(); on[v]=False; comp[v]=ncomp
                    if v==u: break
                ncomp+=1
            if work:
                p=work[-1][0]; low[p]=min(low[p],low[u])
    return off, adj, comp, ncomp
