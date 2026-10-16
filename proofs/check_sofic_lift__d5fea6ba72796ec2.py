"""Independent local arithmetic, Tarjan, and rank/projection replay.

Every graph accepts labels of finite nonempty closed walks. Certificates
cover all their lengths. The finite root-pattern test is a rank certificate,
not a bounded iteration experiment. No Lean claim is made.
"""
from pathlib import Path
from itertools import product
from collections import deque,Counter
import json,time,hashlib,sys,argparse
HERE=Path(__file__).resolve().parent
CLOCK=(0,0,0,0,1,1,1)
sys.setrecursionlimit(100000)


def letter(t,a,v):return 22*t+11*a+v+CLOCK[t]


def normalization(q,h):
    n=len(q)
    if all(x==9 for x in q):return None
    low=[];high=[];a=[];b=[]
    for i,x in enumerate(q):
        j=(i-1)%n
        while q[j]==9:j=(j-1)%n
        incoming_low=int(q[j]>9)
        j=(i+1)%n
        while q[j]==9:j=(j+1)%n
        incoming_high=int(q[j]>9)
        low.append((x+incoming_low)%10);high.append((x+incoming_high)%10)
        a.append(incoming_low);b.append((x+incoming_high)//10)
    return tuple(low[i]+high[(i-h)%n]for i in range(n)),a,b


def bulk_catalog():
    graph={}
    for q in product(range(19),repeat=3):
        r=q
        for h in CLOCK:
            step=normalization(r,h)
            if step is None:break
            r=step[0]
        else:graph[q]=r
    alive=set(graph)
    while True:
        good={q for q in alive if graph[q]in alive}
        if good==alive:break
        alive=good
    indegree={q:0 for q in alive}
    for q in alive:indegree[graph[q]]+=1
    todo=deque(q for q,d in indegree.items()if not d)
    while todo:
        q=todo.popleft();alive.remove(q);r=graph[q];indegree[r]-=1
        if not indegree[r]:todo.append(r)
    cycles=[]
    while alive:
        q=min(alive);cycle=[];r=q
        while r not in cycle:cycle.append(r);alive.remove(r);r=graph[r]
        assert r==q;cycles.append(cycle)
    assert Counter(map(len,cycles))=={1:8,2:10,3:4,4:3,6:4,18:3,30:2}
    return cycles


def expected_initial(new_only=True,all_recurrent=False,macro_periods=None):
    words=set();motifs=[]
    for cycle in bulk_catalog():
        if macro_periods is not None and len(cycle)not in macro_periods:continue
        if not all_recurrent and (len(cycle)!=4 if new_only else 4%len(cycle)!=0):continue
        motifs+=cycle
        for B in cycle:
            q=B;word=[]
            for t in range(7*len(cycle)):
                step,a,b=normalization(q,CLOCK[t%7])
                v=q[-1]-10*b[-1]if CLOCK[t%7]else b[0]
                word.append(letter(t%7,a[0],v));q=step
            assert q==B
            word=tuple(word)
            p=next(p for p in range(7,len(word)+1,7)if len(word)%p==0 and all(word[j]==word[j%p]for j in range(len(word))))
            word=word[:p]
            words.add(min(word[k:]+word[:k]for k in range(0,p,7)))
    edges=[];n=0
    for w in sorted(words):
        for j,l in enumerate(w):edges.append((n+j,n+(j+1)%len(w),l))
        n+=len(w)
    return (n,edges),words,motifs


def reference_tables():
    """Enumerate actual low/high carries first; derive each new label."""
    fibers={}
    for t,h in enumerate(CLOCK):
        vals=range(-1,10)if h else(0,1)
        for a in (0,1):
            for v in vals:fibers[letter(t,a,v)]=set()
        for q,a,incoming_high in product(range(19),(0,1),(0,1)):
            low=(q+a)%10;alpha=(q+a)//10
            high=(q+incoming_high)%10;outgoing_high=(q+incoming_high)//10
            if h:
                new=letter(t,alpha,q-10*outgoing_high)
                option=(t,q,a,outgoing_high,low)
            else:
                new=letter(t,alpha,incoming_high)
                option=(t,q,a,outgoing_high,low+high)
            fibers[new].add(option)
    return {l:sorted(xs)for l,xs in fibers.items()}


def previous_label(x,y):
    t,q,a,b,last=x
    if y[0]!=(t+1)%7:return None
    if not CLOCK[t]:return letter(t,a,b)if y[1]==last else None
    previous_high_digit=y[1]-last
    if 0<=previous_high_digit<=9:
        z=previous_high_digit-b
        assert -1<=z<=9
        return letter(t,a,z)
    return None


def inverse_raw(n,edges,fibers):
    outgoing=[[]for _ in range(n)]
    for e,(u,v,l)in enumerate(edges):outgoing[u].append(e)
    vertices=[(e,x)for e,(_,_,l)in enumerate(edges)for x in fibers[l]]
    ids={x:i for i,x in enumerate(vertices)};raw=[]
    for i,(e,x)in enumerate(vertices):
        for f in outgoing[edges[e][1]]:
            for y in fibers[edges[f][2]]:
                l=previous_label(x,y)
                if l is not None:raw.append((i,ids[f,y],l))
    return vertices,raw


def components(n,edges):
    outgoing=[[]for _ in range(n)]
    for u,v,l in edges:outgoing[u].append(v)
    index=[-1]*n;low=[0]*n;on=[False]*n;stack=[];clock=0;comp=[-1]*n;groups=[]
    def visit(u):
        nonlocal clock
        index[u]=low[u]=clock;clock+=1;stack.append(u);on[u]=True
        for v in outgoing[u]:
            if index[v]<0:visit(v);low[u]=min(low[u],low[v])
            elif on[v]:low[u]=min(low[u],index[v])
        if low[u]==index[u]:
            group=[]
            while True:
                v=stack.pop();on[v]=False;comp[v]=len(groups);group.append(v)
                if v==u:break
            groups.append(group)
    for u in range(n):
        if index[u]<0:visit(u)
    forward=[set()for _ in groups];degree=[0]*len(groups)
    for u,v,l in edges:
        a,b=comp[u],comp[v]
        if a!=b and b not in forward[a]:forward[a].add(b);degree[b]+=1
    todo=deque(i for i,d in enumerate(degree)if d==0);rank=[-1]*len(groups);count=0
    while todo:
        u=todo.popleft();rank[u]=count;count+=1
        for v in sorted(forward[u]):
            degree[v]-=1
            if not degree[v]:todo.append(v)
    assert count==len(groups)
    return comp,groups,[rank[comp[u]]for u in range(n)]


def root_rank(n,edges):
    allowed={0,22,45,66,108,110,144}
    # Phase encoding makes every accepted closed word a repetition of the
    # required seven-label root, up to a temporal rotation.
    phase={}
    for u,v,l in edges:
        phase.setdefault(u,l//22);assert phase[u]==l//22
    assert all(phase[v]==(phase[u]+1)%7 for u,v,l in edges)
    out=[[]for _ in range(n)];degree=[0]*n
    for u,v,l in edges:
        if l in allowed:out[u].append(v);degree[v]+=1
    todo=deque(i for i,d in enumerate(degree)if d==0);rank=[-1]*n;count=0
    while todo:
        u=todo.popleft();rank[u]=count;count+=1
        for v in out[u]:
            degree[v]-=1
            if not degree[v]:todo.append(v)
    assert count==n,'root-pattern closed walk exists'
    assert all(rank[u]<rank[v]for u,v,l in edges if l in allowed)
    return rank


def check(new_only=True,all_recurrent=False,macro_periods=None):
    began=time.monotonic()
    prefix='sofic7_full'if all_recurrent else('sofic28_new'if new_only else'sofic28_all')
    if macro_periods is not None:prefix='sofic7_periods_'+'_'.join(map(str,macro_periods))
    summary=json.loads((HERE/f'{prefix}_summary.json').read_text())
    recurrence=summary['recurrence'];assert recurrence is not None
    end=recurrence['repeat'];first=recurrence['first'];graphs=[]
    for d in range(end+1):
        g=json.loads((HERE/f'{prefix}_depth{d}.json').read_text())
        graphs.append((g['vertices'],[tuple(e)for e in g['edges']]))
    expected,words,motifs=expected_initial(new_only,all_recurrent,macro_periods)
    assert graphs[0]==expected
    assert graphs[end]==graphs[first]
    fibers=reference_tables()
    # Independent exact table comparison additionally audits the discovered
    # implementation used to build graph vertex numbering.
    from sofic_lift import options,output
    for l,fs in fibers.items():assert set(fs)==set(options(l))
    allopts=set(x for fs in fibers.values()for x in fs)
    comparisons=0
    for x in allopts:
        for y in allopts:
            if y[0]!=(x[0]+1)%7:continue
            ref=previous_label(x,y);assert (-1 if ref is None else ref)==output(x,y);comparisons+=1
    transitions=[]
    for d in range(end):
        n,es=graphs[d]
        # Match the discovery option order only for deterministic numbering;
        # its option sets were independently exhausted above.
        ordered={l:list(options(l))for l in fibers}
        vertices,raw=inverse_raw(n,es,ordered)
        comp,groups,rank=components(len(vertices),raw)
        good=[(u,v,l)for u,v,l in raw if comp[u]==comp[v]and(len(groups[comp[u]])>1 or u==v)]
        kept=sorted({u for u,v,l in good}|{v for u,v,l in good});rename={v:i for i,v in enumerate(kept)}
        trimmed=(len(kept),[(rename[u],rename[v],l)for u,v,l in good])
        assert trimmed==graphs[d+1],d
        dest=d+1 if d+1<end else first;dest_edges=set(graphs[dest][1])
        mapping=[rename.get(u,-1)for u in range(len(vertices))]
        for u,v,l in raw:
            assert rank[u]<=rank[v]
            if rank[u]==rank[v]:
                assert mapping[u]>=0 and mapping[v]>=0
                assert (mapping[u],mapping[v],l)in dest_edges
        transitions.append(dict(source=d,destination=dest,raw_vertices=len(vertices),
                                raw_edges=len(raw),rank=rank,mapping=mapping))
    ranks=[root_rank(n,es)for n,es in graphs[:-1]]
    cert=dict(graphs=[dict(vertices=n,edges=es)for n,es in graphs[:-1]],
              transitions=transitions,root_word=[0,22,45,66,108,110,144],root_ranks=ranks)
    raw=json.dumps(cert,separators=(',',':'))+'\n'
    (HERE/f'{prefix}_rank_certificate.json').write_text(raw)
    result=dict(status='independent_all_period_rank_projection_certificate_verified',
                new_tails_only=new_only and not all_recurrent,
                all_recurrent_non_neutral_period3=all_recurrent and macro_periods is None,
                uses_complete_recurrent_catalog=all_recurrent,
                macro_periods=macro_periods,
                motifs=len(motifs),seed_cycles=len(words),recurrence=recurrence,
                graph_sizes=[dict(vertices=n,edges=len(es))for n,es in graphs],
                local_option_comparisons=comparisons,arbitrary_temporal_multiples=True,
                arbitrary_finite_exterior_width=True,root_closed_walk_excluded=True,
                certificate_sha256=hashlib.sha256(raw.encode()).hexdigest(),
                seconds=time.monotonic()-began,decimal_existence_proved=False,lean_formalized=False)
    (HERE/f'{prefix}_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True);return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--all-tails',action='store_true')
    p.add_argument('--all-recurrent',action='store_true')
    p.add_argument('--macro-periods')
    a=p.parse_args();check(not a.all_tails,a.all_recurrent,
                         None if a.macro_periods is None else list(map(int,a.macro_periods.split(','))))
