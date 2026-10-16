"""Universal finite-window moving-front synthesis.

Unlike a fixed prefix, the omitted wake is arbitrary and the front moves.
Every incoming carry is retained. A bounded front requires no positive
cycle for weight 2*displacement-overflow, not a fitted trajectory slope.
Historical search: INDEPENDENT_CRITERION_AUDIT.txt now excludes the exact
finite-window potential criterion for every K and p whenever finite closure
forces an overflow cycle (including both-bit or alternating closure). The
code and raw outcomes are preserved for replay;
increasing its state cap or retained suffix cannot repair that criterion.
"""
from collections import deque
from itertools import product
from pathlib import Path
import json, argparse, time, random
from moving_front import bulk_step, periodic_carries, finite_step, realization

HERE=Path(__file__).resolve().parent


def suffix_step(suffix,bulk,cut,h,incoming,K):
    """Return known suffix, next bulk, new cut residue, and displacement."""
    p=len(bulk);start=cut-len(suffix);end=cut+2*p+2
    at=lambda i:suffix[i-start] if i<cut else bulk[i%p]
    a,b=periodic_carries(bulk);c=incoming;lo=[]
    for i in range(start,end):
        v=at(i)+c;lo.append(v%10);c=v//10
    assert c==a[end%p]
    c=b[end%p];hi=[]
    for i in range(end-1,start-1,-1):
        v=at(i)+c;hi.append(v%10);c=v//10
    hi.reverse();nb=bulk_step(bulk,h)
    ns=start+h
    out=[lo[i-start]+hi[i-h-start] for i in range(ns,end)]
    assert all(out[-j]==nb[(end-j)%p] for j in (1,2))
    while out and out[-1]==nb[(ns+len(out)-1)%p]:out.pop()
    # If m=len(out) after tail trimming, this cutoff discards
    # D=max(0,m-K) columns from the known left edge. Consequently
    # newcut-len(retained) = start+h+D, the all-K obstruction.
    newcut=ns+len(out);out=out[-K:]
    return tuple(out),nb,newcut%p,newcut-cut


def cycle(bulk,clock,limit=10000):
    rows=[];b=bulk;t=0;seen={}
    while (b,t%len(clock)) not in seen:
        if all(x==9 for x in b):return None
        if len(rows)>=limit:return None
        seen[b,t%len(clock)]=len(rows);rows.append(b)
        b=bulk_step(b,clock[t%len(clock)]);t+=1
    a=seen[b,t%len(clock)]
    return rows[a:],tuple(clock[(a+i)%len(clock)] for i in range(len(rows)-a))


def scc(adj):
    rev=[[] for _ in adj]
    for u,es in enumerate(adj):
        for v,*_ in es:rev[v].append(u)
    seen=set();order=[]
    for root in range(len(adj)):
        if root in seen:continue
        seen.add(root);stack=[(root,0)]
        while stack:
            u,k=stack[-1]
            if k<len(adj[u]):
                stack[-1]=(u,k+1);v=adj[u][k][0]
                if v not in seen:seen.add(v);stack.append((v,0))
            else:order.append(u);stack.pop()
    comp=[-1]*len(adj);groups=[]
    for root in reversed(order):
        if comp[root]>=0:continue
        cid=len(groups);comp[root]=cid;group=[];stack=[root]
        while stack:
            u=stack.pop();group.append(u)
            for v in rev[u]:
                if comp[v]<0:comp[v]=cid;stack.append(v)
        groups.append(group)
    return comp,groups


def potential(adj,weight=lambda h,d:2*d-h):
    """Exact Bellman-Ford feasibility with early checked cycle extraction."""
    n=len(adj);dist=[0]*n;parent=[None]*n
    def witness(v):
        seen=set()
        while v not in seen and parent[v] is not None:
            seen.add(v);v=parent[v][0]
        if parent[v] is None:return None
        anchor=v;rev=[]
        while True:
            u,h,d,c=parent[v];rev.append((u,v,h,d,c));v=u
            if v==anchor:break
        edges=rev[::-1];w=sum(weight(e[2],e[3]) for e in edges)
        if w<=0:return None
        assert all(e[1]==edges[(i+1)%len(edges)][0] for i,e in enumerate(edges))
        return dict(bounded=False,positive_cycle=edges,weight=w,
                    displacement=sum(e[3] for e in edges),overflows=sum(e[2] for e in edges))
    for turn in range(n):
        changed=None
        for u,es in enumerate(adj):
            for v,h,d,c in es:
                cand=dist[u]+weight(h,d)
                if cand>dist[v]:dist[v]=cand;parent[v]=(u,h,d,c);changed=v
        if changed is None:
            assert all(dist[v]>=dist[u]+weight(h,d) for u,es in enumerate(adj) for v,h,d,c in es)
            return dict(bounded=True,potential=dist)
        proof=witness(changed)
        if proof:return proof
    raise AssertionError('Bellman-Ford cycle extraction failed')


def fixed_graph(bulk,clock,profile,cut,K=2,cap=5000):
    cy=cycle(tuple(bulk),tuple(clock))
    if cy is None:return dict(status='neutral_or_nonrecurrent_bulk')
    bs,hs=cy
    # The selected profile must refer to the supplied initial bulk.
    if bs[0]!=tuple(bulk):return dict(status='bulk_has_transient')
    keys=[(0,cut%len(bulk),tuple(profile))];ids={keys[0]:0};adj=[]
    for t,c,suff in keys:
        es=[]
        for a in (0,1):
            ns,nb,nc,d=suffix_step(suff,bs[t],c,hs[t],a,K)
            nt=(t+1)%len(bs);assert nb==bs[nt]
            key=(nt,nc,ns)
            if key not in ids:
                if len(keys)>=cap:return dict(status='UNKNOWN_state_cap',states=len(keys),bulk_period=len(bs),K=K)
                ids[key]=len(keys);keys.append(key)
            es.append((ids[key],hs[t],d,a))
        adj.append(es)
    bound=potential(adj)
    summary=dict(status='COMPLETE_LOCAL_GRAPH',states=len(keys),edges=sum(map(len,adj)),
                 bulk=list(bulk),clock=list(clock),profile=list(profile),cut=cut,K=K,
                 temporal_period=len(bs),initial_state=0,**bound)
    if bound['bounded']:
        summary.update(keys=keys,adj=adj,bulk_trace=bs,clock_trace=hs)
    else:
        summary['positive_cycle_states']=[keys[e[0]] for e in bound['positive_cycle']]
    return summary


def control():
    rng=random.Random(18703);checks=0
    for _ in range(1000):
        p=rng.randrange(1,8);b=tuple(rng.randrange(19) for _ in range(p))
        if all(x==9 for x in b):continue
        K=rng.randrange(1,9);s=tuple(rng.randrange(19) for _ in range(rng.randrange(K+1)))
        cut=20+len(s);prefix=(rng.randrange(1,19),)+tuple(rng.randrange(19) for _ in range(cut-len(s)-1))
        whole=prefix+s+tuple(b[i%p] for i in range(cut,cut+4*p+5))
        q=whole+(2*rng.randrange(10),)+whole[::-1]
        image,h=finite_step(q);c=0
        for v in prefix:c=(v+c)//10
        ns,nb,nc,d=suffix_step(s,b,cut,h,c,K);newcut=cut+d
        assert nc==newcut%p
        assert image[newcut-len(ns):newcut]==ns
        assert image[newcut:newcut+2*p]==tuple(nb[i%p] for i in range(newcut,newcut+2*p))
        n=realization(q);out=str(n+int(str(n)[::-1]))[::-1]
        assert image==tuple(int(out[i])+int(out[-1-i]) for i in range(len(out)))
        checks+=1
    return checks


def search():
    records=[]
    # Old and new period-five reflection-compatible motifs; this searches
    # arbitrary-wake moving fronts, not exterior widths for old936.
    motifs=[(9,3,6),(5,2,5),(3,10,15,8)]
    rng=random.Random(701)
    for _ in range(80):
        a,b,c=(rng.randrange(19) for _ in range(3))
        motif=(a,b,c,c,b)
        cy=cycle(motif,(0,1))
        if cy and len(cy[0])<=60:
            motifs.append(cy[0][0])
    motifs=list(dict.fromkeys(motifs))
    for K in (1,2,3):
        for bi,b in enumerate(motifs):
            for profile,cut in [((x,),1) for x in (0,7,8,9,10,11,17,18)]:
                if profile[0]==b[0]:continue
                row=fixed_graph(b,(0,1),profile,cut,K=K,cap=6000)
                records.append(row)
                if row.get('bounded'):
                    print(json.dumps({k:v for k,v in row.items() if k not in ('keys','adj','bulk_trace','clock_trace','potential')}),flush=True)
            if bi%10==0:print(json.dumps(dict(K=K,motifs_done=bi+1,queries=len(records))),flush=True)
    result=dict(status='universal_moving_front_synthesis',integer_controls=control(),
                motifs=motifs,records=records,finite_lychrel_witness=False)
    (HERE/'front_language_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(controls=result['integer_controls'],queries=len(records),
                         bounded=sum(bool(r.get('bounded')) for r in records),
                         unknown=sum(r['status'].startswith('UNKNOWN') for r in records))))

if __name__=='__main__':search()
