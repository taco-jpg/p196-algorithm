"""Necessary exact outer-pair compatibility for the periodic interior graph.

This remains an overapproximation: the bulk and outer pair have not been
connected through finite canonical interfaces and a matched center.
"""
from collections import deque,Counter,defaultdict
from pathlib import Path
import gzip,hashlib,json
from bulk_phases import outputs,INITIAL

ROOT=Path(__file__).parent


def outer(q,h):
    result=set()
    for inner in (0,1):
        if (q+inner)//10!=h:continue
        low=q%10;high=(q+inner)%10
        result.add(low+(1 if h else high))
    return sorted(result)


def scc(graph):
    reverse=defaultdict(list)
    for p,es in graph.items():
        for e in es:reverse[e['target']].append(p)
    visited=set();order=[]
    for root in graph:
        if root in visited:continue
        stack=[(root,False)]
        while stack:
            x,done=stack.pop()
            if done:order.append(x);continue
            if x in visited:continue
            visited.add(x);stack.append((x,True))
            for e in graph[x]:
                y=e['target']
                if y not in visited:stack.append((y,False))
    ids={};components=[]
    for root in reversed(order):
        if root in ids:continue
        i=len(components);todo=[root];ids[root]=i;nodes=[]
        while todo:
            x=todo.pop();nodes.append(x)
            for y in reverse[x]:
                if y not in ids:ids[y]=i;todo.append(y)
        components.append(sorted(nodes))
    return components,ids


def main():
    initial=[(INITIAL,q) for q in range(1,19)]
    todo=deque(initial);seen=set(initial);graph={}
    while todo:
        st=todo.popleft();p,q=st;edges=[]
        for e in outputs(p):
            for oq in outer(q,e['clock']):
                target=(e['target'],oq)
                edges.append(dict(clock=e['clock'],target=target,
                                  **{k:v for k,v in e.items() if k not in ('clock','target')}))
                if target not in seen:seen.add(target);todo.append(target)
        graph[st]=edges
    components,ids=scc(graph)
    candidates=[]
    for i,nodes in enumerate(components):
        if not any(len(set(p))>1 for p,q in nodes):continue
        allowed=set(nodes)
        for start in nodes:
            for first in graph[start]:
                if not first['clock'] or first['target'] not in allowed:continue
                target=first['target'];todo=deque([target]);back={target:None}
                while todo:
                    x=todo.popleft()
                    if x==start:
                        path=[]
                        while back[x] is not None:
                            prev,e=back[x];path.append(dict(source=prev,**e));x=prev
                        loop=[dict(source=start,**first)]+path[::-1]
                        candidates.append(dict(component=i,component_size=len(nodes),loop=loop,
                                               overflow_count=sum(e['clock'] for e in loop)))
                        break
                    for e in graph[x]:
                        y=e['target']
                        if y in allowed and y not in back:back[y]=(x,e);todo.append(y)
    candidates.sort(key=lambda x:(len(x['loop']),-x['overflow_count'],x['loop'][0]['source']))
    # At most three consecutive overflows, exactly (18,9,10,1) at length3.
    overflow_paths=[(q,) for q in range(1,19)]
    layer=[]
    for k in range(1,5):
        overflow_paths=[path+(r,) for path in overflow_paths for r in outer(path[-1],1)]
        layer.append(list(overflow_paths))
    assert layer[2]==[(18,9,10,1)] and layer[3]==[]
    # The earlier bulk-only witness1000111 repeats with four boundary ones.
    clock=(1,0,0,0,1,1,1)
    initial_pairs=list(range(1,19))
    compatible=[(q,) for q in initial_pairs]
    for h in clock*2:compatible=[p+(r,) for p in compatible for r in outer(p[-1],h)]
    assert compatible==[]
    payload=json.dumps(dict(initial=initial,graph=[dict(source=s,edges=graph[s]) for s in sorted(graph)],
                            components=components,shortest_cycle_candidates=candidates[:16],
                            successive_overflow_paths=layer),separators=(',',':'),sort_keys=True).encode()
    (ROOT/'outer_filtered_graph.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    out=dict(reachable_states=len(graph),edges=sum(map(len,graph.values())),strong_components=len(components),
             component_size_distribution=dict(sorted(Counter(map(len,components)).items())),
             candidate_nonconstant_overflow_cycles=len(candidates),
             shortest_recorded_cycle=candidates[0] if candidates else None,
             bulk_only_1000111_cycle_lift='IMPOSSIBLE: repeated clock forces four consecutive overflows',
             longest_possible_consecutive_overflow_path=layer[2],
             payload_sha256=hashlib.sha256(payload).hexdigest(),
             actual_finite_interface_lift='NOT_INSTANTIATED',
             infinite_existence_proved=False,
             scope='Necessary exact bulk and outer-pair compatibility only; local product cycles do not imply actual whole-word orbits')
    (ROOT/'outer_filtered_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
