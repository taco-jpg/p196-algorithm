# K-tail column graph (prototype). Rows I_0 = 9-wire target (c=e, d=1-e, r=9e at ovf), I_1..I_K outward; node = (x_0..x_{K-1}, phase);
# label = (c, r) of I_K at the slot; deterministic successor. S_K = nodes on cycles (free labels).
import sys
B=10
clock=sys.argv[1]; e=sys.argv[2]; Kmax=int(sys.argv[3])
P=len(clock); Q=len(e)
per=P
while per%Q: per+=P
def step(x,ph,cK,rK):
    t=ph; ov=clock[t%P]=='1'; et=int(e[t%Q]); K=len(x)
    d=[1-et]+[0]*K
    for k in range(K): d[k+1]=(x[k]+d[k])//B
    if ov and (x[0]+d[0])%B!=9*et: return None
    r=[9*et]+[0]*K
    for k in range(1,K): r[k]=(x[k]+d[k])%B
    r[K]=rK
    c=[0]*(K+1); c[K]=cK
    for k in range(K-1,-1,-1): c[k]=(x[k]+c[k+1])//B
    if c[0]!=et: return None
    nx=tuple((x[k]+c[k+1])%B+(r[k+1] if ov else (x[k]+d[k])%B) for k in range(K))
    return nx,d[K]
def labels(ph):
    return [(c,r) for c in (0,1) for r in (range(B) if clock[ph%P]=='1' else (0,))]
def core(nodes):
    nodes=set(nodes)
    out={}
    for (x,ph) in nodes:
        s=set()
        for (c,r) in labels(ph):
            res=step(x,ph,c,r)
            if res and (res[0],(ph+1)%per) in nodes: s.add((res[0],(ph+1)%per))
        out[(x,ph)]=s
    # iterate: remove nodes with no out or no in (trim) -> nodes on cycles superset; then SCC-exact via repeated trim is enough for "on a cycle" approx
    changed=True
    while changed:
        changed=False
        indeg={n:0 for n in out}
        for n,s in out.items():
            for m in s:
                if m in indeg: indeg[m]+=1
        dead=[n for n in out if indeg[n]==0 or not any(m in out for m in out[n])]
        if dead:
            changed=True
            for n in dead: del out[n]
    return out
S=None
for K in range(1,Kmax+1):
    if K==1: cand=[((a,),ph) for a in range(2*B-1) for ph in range(per)]
    else: cand=[(x+(a,),ph) for (x,ph) in S for a in range(2*B-1)]
    out=core(cand); S=list(out)
    # root cycles at width K: labels c=0, r=1, and d_K == ovf, x_{K-1}>=1
    rootnext={}
    for (x,ph) in S:
        if x[-1]<1: continue
        res=step(x,ph,0,1 if clock[ph%P]=='1' else 0)
        if res and res[1]==(1 if clock[ph%P]=='1' else 0) and (res[0],(ph+1)%per) in out: rootnext[(x,ph)]=(res[0],(ph+1)%per)
    cyc=set()
    for v in rootnext:
        seen=[];u=v
        while u in rootnext and u not in seen: seen.append(u);u=rootnext[u]
        if u==v: cyc.add(len(seen))
    print(f"K={K}: core {len(S)} nodes; root cycles lengths {sorted(cyc)}",flush=True)
    if not S: print("core empty"); break
