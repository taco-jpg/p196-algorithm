import sys
sys.path.insert(0,'.'); sys.path.insert(0,'lat')
from latcellw import *
fn='lat/lat2.txt'; j0=int(sys.argv[1]); wmax=int(sys.argv[2])
p, m, b, gam, W, a, G, dd = lattice_links(fn, j0)
R=19; allowed=None
for w in range(1,wmax+1):
    cand = [((v,), t) for t in range(p) for v in range(R)] if allowed is None else [(pre+(v,),t) for (pre,t) in allowed for v in range(R)]
    cs=set(cand); edges={}
    for (vs,t) in cand:
        for nv in step_nodes(b,gam[t],a[t],G[t],dd[t],vs,t):
            tgt=(nv,(t+1)%p)
            if tgt in cs: edges.setdefault((vs,t),[]).append(tgt)
    comps=sccs(edges); keep=set(); sccl=[]
    for c in comps:
        if len(c)==1 and c[0] not in edges.get(c[0],[]): continue
        if any(vs[0]!=W[t][j0%m] for (vs,t) in c): keep.update(c); sccl.append(c)
    allowed=keep
# find a cycle in the largest SCC: DFS walk
c=max(sccl,key=len); cs=set(c)
start=min(c,key=lambda x:x[1]); path=[start]; seen={start:0}
cur=start
while True:
    nxts=[x for x in edges.get(cur,[]) if x in cs]
    # prefer an unseen node
    nx=[x for x in nxts if x not in seen]
    cur=nx[0] if nx else nxts[0]
    if cur in seen: cyc=path[seen[cur]:]; break
    seen[cur]=len(path); path.append(cur)
print('SCC sizes',[len(x) for x in sccl],'cycle length',len(cyc))
for (vs,t) in cyc:
    lat=[W[t][(j0+i)%m] for i in range(len(vs))]
    print('t',t,'v',vs,'lattice',lat)
