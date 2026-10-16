"""Independent Tarjan/rank certificate replay of the all-period sofic closure.

No temporal word length is bounded here. Graphs encode labels of arbitrary
finite nonempty closed walks. The independent local arithmetic checker is
also reused as a checked finite table constructor.
"""
from pathlib import Path
from collections import deque
import json,time,sys,hashlib
from check_reverse_certificate import build_tables,target,canonical,unpack,encode_letter

HERE=Path(__file__).resolve().parent
sys.setrecursionlimit(100000)

def components(n,edges):
    outgoing=[[]for _ in range(n)]
    for u,v,l in edges:outgoing[u].append(v)
    index=[-1]*n;low=[0]*n;onstack=[False]*n;stack=[];clock=0
    comp=[-1]*n;groups=[]
    def visit(u):
        nonlocal clock
        index[u]=low[u]=clock;clock+=1;stack.append(u);onstack[u]=True
        for v in outgoing[u]:
            if index[v]<0:visit(v);low[u]=min(low[u],low[v])
            elif onstack[v]:low[u]=min(low[u],index[v])
        if low[u]==index[u]:
            group=[]
            while True:
                v=stack.pop();onstack[v]=False;comp[v]=len(groups);group.append(v)
                if v==u:break
            groups.append(group)
    for u in range(n):
        if index[u]<0:visit(u)
    forward=[set()for _ in groups];indegree=[0]*len(groups)
    for u,v,l in edges:
        a,b=comp[u],comp[v]
        if a!=b and b not in forward[a]:forward[a].add(b);indegree[b]+=1
    todo=deque(i for i,d in enumerate(indegree)if d==0);ranks=[None]*len(groups);k=0
    while todo:
        u=todo.popleft();ranks[u]=k;k+=1
        for v in sorted(forward[u]):
            indegree[v]-=1
            if not indegree[v]:todo.append(v)
    assert k==len(groups)
    return comp,groups,[ranks[comp[u]]for u in range(n)]

def inverse_raw(n,edges,fibers,output):
    outgoing=[[]for _ in range(n)]
    for i,(u,v,l)in enumerate(edges):outgoing[u].append(i)
    vertices=[(i,x)for i,(u,v,l)in enumerate(edges)for x in fibers[l]]
    ids={x:i for i,x in enumerate(vertices)}
    raw=[]
    for u,(e,x)in enumerate(vertices):
        for f in outgoing[edges[e][1]]:
            for y in fibers[edges[f][2]]:
                l=output[x][y]
                if l>=0:raw.append((u,ids[f,y],l))
    return vertices,raw

def no_uniform_cycle(n,edges,letter):
    outgoing=[[]for _ in range(n)];indegree=[0]*n
    for u,v,l in edges:
        if l==letter:outgoing[u].append(v);indegree[v]+=1
    todo=deque(i for i,d in enumerate(indegree)if d==0);rank=[None]*n;count=0
    while todo:
        u=todo.popleft();rank[u]=count;count+=1
        for v in outgoing[u]:
            indegree[v]-=1
            if not indegree[v]:todo.append(v)
    assert count==n
    assert all(rank[u]<rank[v]for u,v,l in edges if l==letter)
    return rank

def check():
    start=time.monotonic();fibers,output,_,_=build_tables()
    graphs=[]
    for k in range(9):
        raw=json.loads((HERE/f'sofic_depth_{k}.json').read_text())
        n=raw['vertices'];es=[tuple(e)for e in raw['edges']]
        assert all(0<=u<n and 0<=v<n and 0<=l<88 for u,v,l in es)
        graphs.append((n,es))
    # The initial graph is the two minimal six-slot target cycles.
    expected=[];total=0
    for p in sorted({canonical(target(B))for B in [(9,3,6),(9,6,3)]}):
        w=unpack(*p);assert w[:6]==w[6:]
        for j,l in enumerate(w[:6]):expected.append((total+j,total+(j+1)%6,l))
        total+=6
    assert graphs[0]==(12,expected)
    # All twelve bulk targets are cyclic rotations of powers of these cycles.
    from itertools import permutations
    periods=[unpack(*p)[:6]for p in sorted({canonical(target(B))for B in [(9,3,6),(9,6,3)]})]
    for B in list(permutations((9,3,6)))+list(permutations((9,12,15))):
        w=target(B)
        assert any(w==tuple(p[(i+r)%6]for i in range(12))for p in periods for r in range(6))
    assert graphs[8]==graphs[5]
    transitions=[]
    for k in range(8):
        n,es=graphs[k];vertices,raw=inverse_raw(n,es,fibers,output)
        comp,groups,rank=components(len(vertices),raw)
        kept_edges=[(u,v,l)for u,v,l in raw if comp[u]==comp[v] and (len(groups[comp[u]])>1 or u==v)]
        kept=sorted({u for u,v,l in kept_edges}|{v for u,v,l in kept_edges})
        renumber={u:i for i,u in enumerate(kept)}
        trimmed=(len(kept),[(renumber[u],renumber[v],l)for u,v,l in kept_edges])
        assert trimmed==graphs[k+1],k
        destination=k+1 if k<7 else 5
        next_edges=set(graphs[destination][1])
        mapping=[renumber.get(u,-1)for u in range(len(vertices))]
        # These two local finite assertions are sufficient for cycle-image
        # inclusion; the SCC algorithm itself need not be trusted afterward.
        for u,v,l in raw:
            assert rank[u]<=rank[v]
            if rank[u]==rank[v]:
                assert mapping[u]>=0 and mapping[v]>=0
                assert (mapping[u],mapping[v],l)in next_edges
        transitions.append(dict(source=k,destination=destination,
            raw_vertices=len(vertices),raw_edges=len(raw),rank=rank,mapping=mapping))
    root=encode_letter(0,1,1,7)
    root_ranks=[no_uniform_cycle(n,es,root)for n,es in graphs[:8]]
    certificate=dict(alphabet_size=88,graphs=[dict(vertices=n,edges=es)for n,es in graphs[:8]],
        transitions=transitions,root_letter=root,root_ranks=root_ranks)
    cert_text=json.dumps(certificate,separators=(',',':'))+'\n'
    (HERE/'sofic_rank_certificate.json').write_text(cert_text)
    result=dict(status='all_period_sofic_certificate_verified',
        scope='fixed finite 8/17 exterior with alternating clock and stated periodic 936/12159 tails',
        graph_sizes=[dict(vertices=n,edges=len(es))for n,es in graphs],
        recurrence=dict(first=5,repeat=8,spatial_period=3),
        arbitrary_positive_temporal_length=True,arbitrary_finite_exterior_width=True,
        root_uniform_closed_walk_excluded=True,
        certificate_sha256=hashlib.sha256(cert_text.encode()).hexdigest(),
        seconds=time.monotonic()-start,decimal_lychrel_existence_proved=False,lean_formalized=False)
    (HERE/'sofic_independent_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':check()
