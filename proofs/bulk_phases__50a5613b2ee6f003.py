"""Exact interior period-four phase graph, NOT a whole-word orbit graph.

Both global alignment clocks are retained as possibilities. All-nine bulk
requires explicit two-sided boundary carry choices. Cycles are necessary
bulk data only: finite canonical interfaces and their actual clock remain
an unsatisfied lifting obligation.
"""
from collections import deque,Counter,defaultdict
from pathlib import Path
import gzip,hashlib,json,itertools

ROOT=Path(__file__).parent
INITIAL=(14,14,4,4)


def outputs(p):
    size=len(p)
    if all(q==9 for q in p):
        return [dict(clock=h,left_carry=a,right_carry=b,target=(18-9*(a+b),)*size)
                for h,a,b in itertools.product((0,1),repeat=3)]
    low=[];high=[];carry_records=[]
    for i,q in enumerate(p):
        j=(i-1)%size
        while p[j]==9:j=(j-1)%size
        a=int(p[j]>=10)
        j=(i+1)%size
        while p[j]==9:j=(j+1)%size
        b=int(p[j]>=10)
        low.append((q+a)%10);high.append((q+b)%10);carry_records.append((a,b))
    return [dict(clock=h,target=tuple(low[i]+high[(i-h)%size] for i in range(size))) for h in (0,1)]


def strongly_connected(graph):
    forward={p:[tuple(e['target']) for e in es] for p,es in graph.items()}
    reverse=defaultdict(list)
    for p,ns in forward.items():
        for q in ns:reverse[q].append(p)
    visited=set();order=[]
    for root in graph:
        if root in visited:continue
        stack=[(root,False)]
        while stack:
            p,done=stack.pop()
            if done:order.append(p);continue
            if p in visited:continue
            visited.add(p);stack.append((p,True))
            for q in forward[p]:
                if q not in visited:stack.append((q,False))
    comp={};components=[]
    for root in reversed(order):
        if root in comp:continue
        ix=len(components);nodes=[];todo=[root];comp[root]=ix
        while todo:
            p=todo.pop();nodes.append(p)
            for q in reverse[p]:
                if q not in comp:comp[q]=ix;todo.append(q)
        components.append(sorted(nodes))
    return components,comp


def return_path(graph,start,target,allowed):
    todo=deque([start]);seen={start:None}
    while todo:
        p=todo.popleft()
        if p==target:
            path=[]
            while seen[p] is not None:
                previous,edge=seen[p];path.append(dict(source=previous,**edge));p=previous
            return path[::-1]
        for edge in graph[p]:
            q=tuple(edge['target'])
            if q in allowed and q not in seen:seen[q]=(p,edge);todo.append(q)
    raise AssertionError('SCC return path absent')


def main():
    graph={};todo=deque([INITIAL]);reached={INITIAL}
    while todo:
        p=todo.popleft();edges=outputs(p);graph[p]=edges
        for edge in edges:
            q=edge['target']
            assert len(q)==4 and all(0<=x<=18 for x in q)
            if q not in reached:reached.add(q);todo.append(q)
        assert len(reached)<=19**4
    components,comp=strongly_connected(graph)
    cycles=[];nonconstant_overflow=[]
    for i,nodes in enumerate(components):
        node_set=set(nodes)
        internal=[(p,e) for p in nodes for e in graph[p] if tuple(e['target']) in node_set]
        candidates=[(p,e) for p,e in internal if e['clock']==1]
        if candidates:
            p,e=min(candidates,key=lambda pe:(len(set(pe[0]))==1,pe[0],pe[1]['target']))
            loop=[dict(source=p,**e)]+return_path(graph,tuple(e['target']),p,node_set)
            entry=dict(component=i,component_size=len(nodes),loop=loop,
                       overflow_count=sum(x['clock'] for x in loop),
                       nonconstant_phase=any(len(set(x['source']))>1 for x in loop))
            cycles.append(entry)
            if entry['nonconstant_phase']:nonconstant_overflow.append(entry)
    # Preserve the explicitly derived ten-step nonoverflow cycle.
    p=(9,10,9,8);ten=[]
    for t in range(10):
        edge=next(e for e in outputs(p) if e['clock']==0);ten.append(dict(source=p,**edge));p=edge['target']
    assert p==(9,10,9,8)
    payload=json.dumps(dict(initial=INITIAL,graph=[dict(source=p,edges=graph[p]) for p in sorted(graph)],
                            components=components,overflow_cycle_witnesses=cycles,ten_step_nooverflow_cycle=ten),
                       separators=(',',':'),sort_keys=True).encode()
    (ROOT/'bulk_phase_graph.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    out=dict(initial=INITIAL,period=4,reachable_indexed_phases=len(graph),edges=sum(map(len,graph.values())),
             finite_universe_bound=19**4,strong_components=len(components),
             component_size_distribution=dict(sorted(Counter(map(len,components)).items())),
             components_with_overflow_cycles=len(cycles),nonconstant_overflow_cycle_components=len(nonconstant_overflow),
             shortest_recorded_nonconstant_overflow_cycle=min(nonconstant_overflow,key=lambda x:len(x['loop'])) if nonconstant_overflow else None,
             constants_reachable=sorted(set(p[0] for p in graph if len(set(p))==1)),
             payload_sha256=hashlib.sha256(payload).hexdigest(),
             scope='Exact periodic interiors with free alignment clock; NOT realizable whole-word orbit graph',
             finite_center_and_exterior_lift='NOT_INSTANTIATED',infinite_existence_proved=False)
    (ROOT/'bulk_phase_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
