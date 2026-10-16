"""Independent finite certificate checker for the neutral exterior's centers.

This file imports none of the search implementations. It verifies a regular
invariant for all periodic temporal words and arbitrary finite spatial depth.
It is a computational certificate, not a Lean proof or a Lychrel theorem.
"""
import json
from collections import defaultdict, deque
from functools import lru_cache

@lru_cache(None)
def digit_column(a,b,left_out,right_in,steps):
    paths={(a,b,0,0)}
    for t in range(steps):
        fresh=set()
        for x,y,left_in,right_out in paths:
            for incoming in range(2):
                high=x+y+incoming
                low=x+y+((right_in>>t)&1)
                if high//10==((left_out>>t)&1):
                    fresh.add((high%10,low%10,left_in+(incoming<<t),right_out+((low//10)<<t)))
        paths=fresh
    return paths

def cyclic_part(phases, edges):
    n=len(phases); outs=[[] for _ in range(n)]
    for u,v,a in edges:outs[u].append(v)
    # Independent transitive reachability: an edge is on a cycle precisely
    # when its destination can reach its source.
    reachable=[]
    for root in range(n):
        seen={root};stack=[root]
        while stack:
            for v in outs[stack.pop()]:
                if v not in seen:seen.add(v);stack.append(v)
        reachable.append(seen)
    kept=[(u,v,a) for u,v,a in edges if u in reachable[v]]
    nodes=sorted({u for u,v,a in kept}|{v for u,v,a in kept})
    ren={u:i for i,u in enumerate(nodes)}
    return [phases[u] for u in nodes],[(ren[u],ren[v],a) for u,v,a in kept]

def predecessor_graph(phases,edges,ps):
    triples=set(); raw=[]
    for u,v,sym in edges:
        x,y,l0,r0,l1,r1=sym
        p0,p1=ps[2*phases[u]:2*phases[u]+2]
        for a in range(10):
            for b in range(10):
                for aa,bb,ll,rr in digit_column(a,b,l0,r0,p0):
                    for cc,dd,ss,tt in digit_column(y,bb,l1,r1,p1):
                        src=(u,x,a);dst=(v,dd,cc)
                        triples.add(src);triples.add(dst)
                        raw.append((src,dst,(b,aa,ll,rr,ss,tt)))
    keys=sorted(triples); ren={s:i for i,s in enumerate(keys)}
    pp=[phases[s[0]] for s in keys]
    ee=sorted(set((ren[u],ren[v],s) for u,v,s in raw))
    return cyclic_part(pp,ee)

def simulation(source_phases,source_edges,target_phases,target_edges):
    so=[defaultdict(set) for _ in source_phases]
    to=[defaultdict(set) for _ in target_phases]
    for u,v,a in source_edges:so[u][a].add(v)
    for u,v,a in target_edges:to[u][a].add(v)
    related=[{v for v,p in enumerate(target_phases) if p==phase} for phase in source_phases]
    rounds=0
    while True:
        rounds+=1; removed=[]
        for u in range(len(source_phases)):
            for v in related[u]:
                if any(not (related[uu]&to[v].get(label,set()))
                       for label,ends in so[u].items() for uu in ends):removed.append((u,v))
        if not removed:break
        for u,v in removed:related[u].remove(v)
    assert all(related),'A source vertex has no forward simulation representative'
    # Recheck local simulation independently of the convergence stopping rule.
    assert all(any(vv in related[uu] for vv in to[v].get(a,()))
               for u,vv_unused,a in source_edges for uu in [vv_unused] for v in related[u])
    return {'pairs':sum(map(len,related)), 'rounds':rounds,
            'relation':[sorted(vs) for vs in related]}

def head_ranking(phases,edges,ps):
    es=[];nodes=set()
    for u,v,s in edges:
        x,y,l0,r0,l1,r1=s
        if l0!=r0:continue
        z=y;out=0
        for t in range(ps[2*phases[u]+1]):
            total=2*z+((r1>>t)&1);z=total%10;out+=(total//10)<<t
        if out==l1:
            a=(u,x);b=(v,z);nodes.add(a);nodes.add(b);es.append((a,b))
    es=set(es);indeg={u:0 for u in nodes};out=defaultdict(set)
    for u,v in es:indeg[v]+=1;out[u].add(v)
    q=deque(u for u in nodes if indeg[u]==0);ranks={u:0 for u in q};processed=0
    while q:
        u=q.popleft();processed+=1
        for v in out[u]:
            ranks[v]=max(ranks.get(v,0),ranks[u]+1);indeg[v]-=1
            if indeg[v]==0:q.append(v)
    assert processed==len(nodes),'Head-intersection graph has a cycle'
    assert all(ranks[u]<ranks[v] for u,v in es)
    return {'vertices':len(nodes),'edges':len(es),'maximum_rank':max(ranks.values(),default=0),
            'ranking':[[list(u),ranks[u]] for u in sorted(nodes)]}

def verify(rotation):
    data=json.load(open(f'persist_exterior_temporal_invariant_{rotation}.json'))
    phases=data['phase'];edges=[(u,v,tuple(a)) for u,v,a in data['edges']];ps=data['periods']
    assert set(phases)=={0,1}
    for u,v,(x,y,l0,r0,l1,r1) in edges:
        assert phases[v]==1-phases[u]
        p0,p1=ps[2*phases[u]:2*phases[u]+2]
        assert 0<=x<10 and 0<=y<10
        assert all(0<=c<(1<<p) for c,p in [(l0,p0),(r0,p0),(l1,p1),(r1,p1)])
    base_d=(9,0,9,9);base_l=(1,0,3,3);base_r=(0,1,12,28)
    d=base_d[rotation:]+base_d[:rotation];l=base_l[rotation:]+base_l[:rotation];r=base_r[rotation:]+base_r[:rotation]
    d=tuple(9-x if j%2==0 else x for j,x in enumerate(d))
    initial=[(j,1-j,(d[2*j],d[2*j+1],l[2*j],r[2*j],l[2*j+1],r[2*j+1])) for j in range(2)]
    init_sim=simulation([0,1],initial,phases,edges)
    pred_phases,pred_edges=predecessor_graph(phases,edges,ps)
    pred_sim=simulation(pred_phases,pred_edges,phases,edges)
    maps=json.load(open(f'persist_exterior_temporal_homomorphism_{rotation}.json'))
    target_edges=set(edges)
    for source_phases,source_edges,mapping in [([0,1],initial,maps['initial_map']),
                                               (pred_phases,pred_edges,maps['map'])]:
        assert len(mapping)==len(source_phases)
        assert all(0<=v<len(phases) and phases[v]==source_phases[u] for u,v in enumerate(mapping))
        assert all((mapping[u],mapping[v],label) in target_edges for u,v,label in source_edges)
    ranks=head_ranking(phases,edges,ps)
    result={'rotation':rotation,'periods':ps,'invariant_vertices':len(phases),'invariant_edges':len(edges),
            'predecessor_vertices':len(pred_phases),'predecessor_edges':len(pred_edges),
            'initial_simulation':init_sim,'predecessor_simulation':pred_sim,'head_dag':ranks,
            'initial_homomorphism':maps['initial_map'],'predecessor_homomorphism':maps['map'],
            'both_homomorphisms_verified':True}
    return result

if __name__=='__main__':
    output=[verify(i) for i in [0,1]]
    json.dump(output,open('persist_exterior_temporal_certificate.json','w'),indent=2)
    for r in output:
        print(json.dumps({k:v if not isinstance(v,dict) else {kk:vv for kk,vv in v.items() if kk not in ['relation','ranking']} for k,v in r.items()}))
