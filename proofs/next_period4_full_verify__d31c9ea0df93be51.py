"""Independent literal-integer replay of the complete period-four connector graph.

This builds the necessary recurrent product independently at widths1 and2,
then checks three core lengths using only ordinary integer reversal/addition.
It imports no C++ transition, connector, SCC, or rank implementation.
"""
import itertools
import json
from pathlib import Path
from exist_geom_periodic_bulk_graph import enumerate_states, nextq, scc


def realize(q):
    assert q == q[::-1]
    ds=[0]*len(q)
    for i in range(len(q)//2):
        ds[-1-i]=min(9,q[i]);ds[i]=q[i]-ds[-1-i]
    if len(q)%2:
        assert q[len(q)//2]%2==0
        ds[len(q)//2]=q[len(q)//2]//2
    assert ds[-1]>0
    return int(''.join(map(str,ds[::-1])))


def image(q):
    n=realize(q);word=str(n+int(str(n)[::-1]))
    return ([int(word[i])+int(word[-1-i]) for i in range(len(word))],
            len(word)-len(q),word!=word[::-1])


def run(k):
    bulk=enumerate_states(4);bid={x:i for i,x in enumerate(bulk)}
    bg=[[] for _ in bulk]
    for u,(q,s) in enumerate(bulk):
        for h in (0,1):
            nxt=(nextq(q,h),(s+h)%8)
            if nxt in bid:bg[u].append((bid[nxt],h))
    bc,groups=scc(bg)
    keep=[u for ci,mem in enumerate(groups)
          if any(h and bc[v]==ci for x in mem for v,h in bg[x]) for u in mem]
    outers=[(a,)+tail for a in range(1,19)
            for tail in itertools.product(range(19),repeat=k-1)]
    oi={p:i for i,p in enumerate(outers)}
    oe=[]
    for p in outers:
        edges=set()
        for b in (0,1):
            dest,h,_=image(list(p)+[18*b]+list(p[::-1]))
            edges.add((oi[tuple(dest[:k])],h))
        oe.append(edges)
    nodes=[(u,o) for u in keep for o in range(len(outers))]
    ids={x:i for i,x in enumerate(nodes)};graph=[[] for _ in nodes]
    for x,(u,o) in enumerate(nodes):
        for v,h in bg[u]:
            if bc[v]!=bc[u]:continue
            for oo,hh in oe[o]:
                if hh==h:graph[x].append((ids[v,oo],h))
    pc,groups=scc(graph)
    active=[x for ci,mem in enumerate(groups)
            if any(h and pc[v]==ci for u in mem for v,h in graph[u]) for x in mem]
    active_set=set(active);full={};shape=unsafe=valid=0;additions=0
    for x in active:
        u,o=nodes[x];q,s=bulk[u];p=list(outers[o]);reports=[]
        for length in (16+s,24+s,32+s):
            columns=p+[q[j%4] for j in range(length)]+p[::-1]
            target,h,safe=image(columns);additions+=1
            nb=(nextq(q,h),(s+h)%8);np=target[:k]
            expected=np+[nb[0][j%4] for j in range(length+h)]+np[::-1]
            shaped=(nb in bid and target==expected)
            reports.append((shaped,safe,nb,tuple(np),h))
        assert reports[0]==reports[1]==reports[2],(k,q,s,p,reports)
        shaped,safe,nb,np,h=reports[0]
        shape+=shaped;unsafe+=not safe
        if not shaped or not safe:continue
        target=ids.get((bid[nb],oi[np]))
        if target in active_set and pc[target]==pc[x]:
            full[x]=target;valid+=1
    # Independently rank the functional graph. A live return would be an error.
    rank={};maxchain=0
    for root in active:
        if root in rank:continue
        path=[];here=set();u=root
        while u in full and u not in rank:
            assert u not in here,'A complete safe cycle was found'
            here.add(u);path.append(u);u=full[u]
        depth=rank.get(u,0);rank.setdefault(u,depth)
        for v in reversed(path):depth+=1;rank[v]=depth
        maxchain=max(maxchain,depth)
    result={'outer_width':k,'necessary_recurrent_states':len(active),
            'shape_preserving_states':shape,'unsafe_states':unsafe,
            'safe_edges_within_necessary_components':valid,
            'positive_components':0,'cycle_states':0,
            'integer_additions_checked':additions,
            'maximum_retained_safe_path':maxchain}
    old=json.loads(Path(f'next_period4_full_width{k}.json').read_text())
    for field in ('outer_width','necessary_recurrent_states','shape_preserving_states',
                  'unsafe_states','safe_edges_within_necessary_components',
                  'positive_components','cycle_states'):
        assert result[field]==old[field],(field,result[field],old[field])
    return result


if __name__=='__main__':
    out=[]
    for k in (1,2):
        row=run(k);out.append(row)
        Path('next_period4_full_verified.json').write_text(json.dumps(out,indent=2)+'\n')
        print(json.dumps(row),flush=True)
