"""All-period intersection: nonuniform centered period4 bulk and two outer pairs.

No finite exterior is supplied by this necessary-condition product. Any
returned cycle must still be completed and checked as an integer family.
"""
import json
from collections import deque
from pathlib import Path
from exist_geom_periodic_bulk_graph import enumerate_states,nextq,scc


def outer_pair_edges(q):
    q0,q1=q;c1=q0//10;c2=(q1+c1)//10
    low0=q0-10*c1;low1=q1+c1-10*c2
    result=set()
    for b2 in [0,1]:
        b1=(q1+b2)//10;h=(q0+b1)//10
        high0=q0+b1-10*h;high1=q1+b2-10*b1
        dest=(low0+1,low1+high0) if h else (low0+high0,low1+high1)
        result.add((dest,h))
    return result


def run():
    r=4;nodes=enumerate_states(r);ids={q:i for i,q in enumerate(nodes)}
    adj=[[] for _ in nodes]
    for i,(q,s) in enumerate(nodes):
        for h in [0,1]:
            nxt=(nextq(q,h),(s+h)%(2*r))
            if nxt in ids:adj[i].append((ids[nxt],h))
    comp,components=scc(adj)
    keep=[]
    for ci,mem in enumerate(components):
        if any(h and comp[v]==ci for u in mem for v,h in adj[u]):keep+=mem
    outer=[(a,b) for a in range(1,19) for b in range(19)]
    oi={q:i for i,q in enumerate(outer)}
    oe=[[ (oi[v],h) for v,h in outer_pair_edges(q)] for q in outer]
    # Exhaustively compare with the independently authored carry arithmetic.
    from exist_uniform_clock_obstruction import transition
    for q in outer:
        assert outer_pair_edges(q)=={transition(*q,b) for b in [0,1]}
    pn=[(u,o) for u in keep for o in range(len(outer))]
    pi={x:i for i,x in enumerate(pn)}
    pa=[[] for _ in pn]
    for i,(u,o) in enumerate(pn):
        for v,h in adj[u]:
            if comp[v]!=comp[u]:continue
            for oo,hh in oe[o]:
                if h==hh:pa[i].append((pi[(v,oo)],h))
    pc,pcs=scc(pa);positive=[]
    for ci,mem in enumerate(pcs):
        growth=sum(h for u in mem for v,h in pa[u] if pc[v]==ci)
        if not growth:continue
        entry={'vertices':len(mem),'internal_growth_edges':growth,'cycles':[]}
        # One shortest return through an overflow edge from center phase0.
        candidate=next(( (u,v,h) for u in mem if nodes[pn[u][0]][1]==0
                         for v,h in pa[u] if h and pc[v]==ci),None)
        assert candidate is not None
        u,v,h=candidate;parent={v:None};queue=deque([v])
        while u not in parent:
            x=queue.popleft()
            for y,flag in pa[x]:
                if pc[y]==ci and y not in parent:
                    parent[y]=(x,flag);queue.append(y)
        path=[];x=u
        while x!=v:
            prev,flag=parent[x];path.append((prev,flag));x=prev
        path.reverse();path=[(u,h)]+path
        qtrace=[nodes[pn[x][0]][0] for x,flag in path]
        htrace=[flag for x,flag in path]
        outertrace=[outer[pn[x][1]] for x,flag in path]
        assert sum(htrace)>0 and sum(htrace)%(2*r)==0
        entry['cycles'].append({'period':len(path),'growth':sum(htrace),
                                'bulk':qtrace,'clock':htrace,'outer_pairs':outertrace})
        positive.append(entry)
    return {'bulk_states':len(nodes),'recurrent_bulk_states':len(keep),
            'outer_states':len(outer),'product_states':len(pn),
            'product_edges':sum(map(len,pa)),'product_components':len(pcs),
            'positive_components':positive,
            'outer_model_crosscheck_cases':684,
            'scope':'Necessary conditions only; a finite exterior is still required.'}


if __name__=='__main__':
    out=run();Path('exist_geom_bulk_two_outer_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='positive_components'}))
    print(json.dumps(out['positive_components']))
