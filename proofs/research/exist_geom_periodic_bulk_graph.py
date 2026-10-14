"""Enumerate exact center-compatible periodic q bulks, with free N/O control.

This graph does NOT supply an exterior. Its positive cycles are local bulk
components only, and cannot be mistaken for finite integer Lychrel witnesses.
"""
import argparse,itertools,json
from pathlib import Path


def carries(q):
    r=len(q);a=[0]*r;b=[0]*r
    # Nonuniform q has a nonneutral coefficient, so each circular carry
    # direction has a unique fixed stream after at most two circuits.
    c=0
    for _ in range(2):
        for j in range(r):
            a[j]=c;c=(q[j]+c)//10
    c=0
    for _ in range(2):
        for j in reversed(range(r)):
            c=(q[j]+c)//10;b[j]=c
    assert all(a[(j+1)%r]==(q[j]+a[j])//10 for j in range(r))
    assert all(b[j]==(q[j]+b[(j+1)%r])//10 for j in range(r))
    return a,b


def valid(q,s):
    r=len(q)
    if len(set(q))==1:return False
    if any(q[j]!=q[(s-1-j)%r] for j in range(r)):return False
    a,b=carries(q)
    if s%2==0:return a[(s//2)%r]==b[(s//2)%r]
    j=((s-1)//2)%r
    return q[j]%2==0 and a[j]==b[(j+1)%r]


def nextq(q,h):
    r=len(q);a,b=carries(q)
    lo=[(q[j]+a[j])%10 for j in range(r)]
    hi=[(q[j]+b[(j+1)%r])%10 for j in range(r)]
    return tuple(lo[j]+hi[(j-h)%r] for j in range(r))


def outer_next(q,h):
    if h:
        return [10] if q==9 else [q-9] if q>=10 else []
    return [2*q,2*q+1] if q<=8 else [18] if q==9 else []


def scc(adj):
    rev=[[] for _ in adj]
    for u,edges in enumerate(adj):
        for v,h in edges:rev[v].append(u)
    seen=set();order=[]
    for root in range(len(adj)):
        if root in seen:continue
        seen.add(root);stack=[(root,0)]
        while stack:
            u,idx=stack[-1]
            if idx<len(adj[u]):
                stack[-1]=(u,idx+1);v=adj[u][idx][0]
                if v not in seen:seen.add(v);stack.append((v,0))
            else:order.append(u);stack.pop()
    comp=[-1]*len(adj);components=[]
    for root in reversed(order):
        if comp[root]>=0:continue
        ci=len(components);comp[root]=ci;stack=[root];members=[]
        while stack:
            u=stack.pop();members.append(u)
            for v in rev[u]:
                if comp[v]<0:comp[v]=ci;stack.append(v)
        components.append(members)
    return comp,components


def enumerate_states(r):
    result=[]
    for s in range(2*r):
        used=set();orbits=[]
        for j in range(r):
            if j not in used:
                orb={j,(s-1-j)%r};used|=orb;orbits.append(orb)
        for values in itertools.product(range(19),repeat=len(orbits)):
            q=[0]*r
            for orb,v in zip(orbits,values):
                for j in orb:q[j]=v
            if valid(q,s):result.append((tuple(q),s))
    return result


def run(r):
    nodes=enumerate_states(r);ids={x:i for i,x in enumerate(nodes)}
    adj=[[] for _ in nodes];rev=[[] for _ in nodes];exits=0
    for i,(q,s) in enumerate(nodes):
        for h in [0,1]:
            target=(nextq(q,h),(s+h)%(2*r))
            if target in ids:
                j=ids[target];adj[i].append((j,h));rev[j].append(i)
            else:
                assert len(set(target[0]))==1,target
                exits+=1
    seen=set();order=[]
    for root in range(len(nodes)):
        if root in seen:continue
        seen.add(root);stack=[(root,0)]
        while stack:
            u,idx=stack[-1]
            if idx<len(adj[u]):
                stack[-1]=(u,idx+1);v=adj[u][idx][0]
                if v not in seen:seen.add(v);stack.append((v,0))
            else:order.append(u);stack.pop()
    comp=[-1]*len(nodes);components=[]
    for root in reversed(order):
        if comp[root]>=0:continue
        ci=len(components);comp[root]=ci;stack=[root];members=[]
        while stack:
            u=stack.pop();members.append(u)
            for v in rev[u]:
                if comp[v]<0:comp[v]=ci;stack.append(v)
        components.append(members)
    positive=[]
    for ci,members in enumerate(components):
        grow=sum(h for u in members for v,h in adj[u] if comp[v]==ci)
        if grow:
            positive.append({'vertices':len(members),'internal_growth_edges':grow,
                             'internal_edges':sum(1 for u in members for v,h in adj[u] if comp[v]==ci),
                             'example_state':nodes[members[0]]})
            start=next((u for u in members if nodes[u][1]==0),members[0])
            for period in [20,24,28]:
                target_growth=2*r
                stages=[{(start,0):None}]
                for t in range(period):
                    stage={}
                    for (u,g) in stages[-1]:
                        for v,h in adj[u]:
                            if comp[v]==ci and g+h<=target_growth:
                                stage.setdefault((v,g+h),(u,g,h))
                    stages.append(stage)
                if (start,target_growth) in stages[-1]:
                    path=[];state=(start,target_growth)
                    for t in reversed(range(1,period+1)):
                        u,g,h=stages[t][state];path.append((u,h));state=(u,g)
                    path.reverse()
                    positive[-1].setdefault('cycle_examples',[]).append({
                        'period':period,'growth':target_growth,
                        'bulk':[nodes[u][0] for u,h in path],
                        'clock':[h for u,h in path]})
    # Intersect all positive-growth bulk SCCs with the necessary exact
    # scalar outer-pair transition graph. This removes artificial clocks
    # with five consecutive N steps or impossible digit-growth rates.
    active=set(u for ci,mem in enumerate(components) for u in mem
               if any(h and comp[v]==ci for x in mem for v,h in adj[x]))
    pn=[(u,o) for u in active for o in range(1,19)];pi={x:i for i,x in enumerate(pn)}
    pa=[[] for _ in pn]
    for i,(u,o) in enumerate(pn):
        for v,h in adj[u]:
            if comp[u]==comp[v]:
                for oo in outer_next(o,h):pa[i].append((pi[(v,oo)],h))
    pc,pcom=scc(pa);products=[]
    for ci,mem in enumerate(pcom):
        grow=sum(h for u in mem for v,h in pa[u] if pc[v]==ci)
        if not grow:continue
        choices=[u for u in mem if nodes[pn[u][0]][1]==0]
        if not choices:continue
        start=choices[0];entry={'vertices':len(mem),'growth_edges':grow,'cycles':[]}
        for period in [20,24,28]:
            target_growth=2*r;stages=[{(start,0):None}]
            for t in range(period):
                stage={}
                for u,g in stages[-1]:
                    for v,h in pa[u]:
                        if pc[v]==ci and g+h<=target_growth:
                            stage.setdefault((v,g+h),(u,g,h))
                stages.append(stage)
            if (start,target_growth) in stages[-1]:
                path=[];state=(start,target_growth)
                for t in reversed(range(1,period+1)):
                    u,g,h=stages[t][state];path.append((u,h));state=(u,g)
                path.reverse()
                entry['cycles'].append({'period':period,'growth':target_growth,
                    'bulk':[nodes[pn[u][0]][0] for u,h in path],
                    'clock':[h for u,h in path],
                    'outer_sums':[pn[u][1] for u,h in path]})
        products.append(entry)
    return {'spatial_period':r,'states':len(nodes),'edges':sum(map(len,adj)),
            'exits_to_uniform':exits,'strong_components':len(components),
            'components_with_internal_growth':positive,
            'outer_control_product':{'states':len(pn),'edges':sum(map(len,pa)),
                                     'positive_components':products}}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--period',type=int,default=4)
    ap.add_argument('--output',default='exist_geom_periodic_bulk_graph_results.json')
    args=ap.parse_args();res=run(args.period)
    Path(args.output).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
