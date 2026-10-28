#!/usr/bin/env python3
"""Independent explicit strongly-connected-component lift for rec0 fixed-first-defect.
Uses standard-library Kosaraju SCCs and tuple states; no C++ encodings or degree peel.
This is a local verification script, not the production executable.
"""
from agent2_boundary_data import rows

raw=rows()
W=list(zip(*raw[:20]))
B=list(zip(*raw[20:]))
g=(1,0,1,0,1,0,1,0)
def lat(t,x):
    return B[t%8][x] if x<39 else W[t%8][(x-39)%20]
def asc(t,x):
    for y in range(x-1,x-61,-1):
        if lat(t,y)!=9:return int(lat(t,y)>=10)
    raise AssertionError('ambiguous asc carry')
def desc(t,x):
    for y in range(x+1,x+61):
        if lat(t,y)!=9:return int(lat(t,y)>=10)
    raise AssertionError('ambiguous desc carry')

def scc_cycle_nodes(adj):
    pred={v:[] for v in adj}
    for u,vs in adj.items():
        for v in vs:pred[v].append(u)
    seen=set();done=[]
    for start in adj:
        if start in seen:continue
        seen.add(start);stack=[(start,iter(adj[start]))]
        while stack:
            u,it=stack[-1]
            v=next(it,None)
            if v is None:
                done.append(u);stack.pop();continue
            if v not in seen:
                seen.add(v);stack.append((v,iter(adj[v])))
    visited=set();cyc=set()
    for start in reversed(done):
        if start in visited:continue
        comp=[];queue=[start];visited.add(start)
        while queue:
            u=queue.pop();comp.append(u)
            for v in pred[u]:
                if v not in visited:visited.add(v);queue.append(v)
        if len(comp)>1 or start in adj[start]:cyc.update(comp)
    return cyc


def succ(state, x):
    t,vs=state; k=len(vs)
    u=[0]*k; ai=asc(t,x)
    for i,v in enumerate(vs):
        u[i]=(v+ai)%10
        ai=int(v+ai>=10)
    left=lat(t,x-1)
    out=set()
    for upper in (0,1):
        ds=[0]*(k+1);ds[-1]=upper
        digit=[0]*k
        for i in range(k-1,-1,-1):
            digit[i]=(vs[i]+ds[i+1])%10
            ds[i]=int(vs[i]+ds[i+1]>=10)
        if (g[t]==0 or left==9) and ds[0]!=desc(t,x-1):
            continue
        vnext=[]
        for i in range(k):
            high = digit[i] if not g[t] else ((left+ds[0])%10 if i==0 else digit[i-1])
            vnext.append(u[i]+high)
        if vnext[0]!=lat(t+1,x):
            out.add(((t+1)%8,tuple(vnext)))
    return out

def run(j=4,maxk=30):
    x=119+j
    living={(t,(a,b)) for t in range(8) for a in range(19) if a!=lat(t,x) for b in range(19)}
    for k in range(2,maxk+1):
        adj={n:succ(n,x)&living for n in living}
        cyc=scc_cycle_nodes(adj)
        print('k',k,'candidates',len(living),'edges',sum(map(len,adj.values())),'cyclic_scc_nodes',len(cyc),flush=True)
        if not cyc:
            return k
        living={(t,tuple(v)+(h,)) for t,v in cyc for h in range(19)}
    return None

if __name__=='__main__':
    import sys
    for j in (0,1,2,3,4,9,14,19):
        expected=(2,3,3,2,18,18,18,18)[(0,1,2,3,4,9,14,19).index(j)]
        got=run(j,18)
        assert got==expected,(j,got,expected)
        print('j',j,'first_unviable_k',got)
    print('ALL INDEPENDENT SCC CHECKS PASSED')