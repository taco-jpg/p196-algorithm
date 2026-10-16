"""Finite prefix graph for the maximal outer clock; interior carry arbitrary."""
from itertools import product
from collections import deque,Counter
import json

def evolve(q,ci):
    k=len(q);c=0;lo=[]
    for s in q:lo.append((s+c)%10);c=(s+c)//10
    hi=[0]*k;c=ci
    for i in range(k-1,-1,-1):hi[i]=(q[i]+c)%10;c=(q[i]+c)//10
    if c:
        return tuple([lo[0]+1]+[lo[i]+hi[i-1] for i in range(1,k)])
    return tuple(a+b for a,b in zip(lo,hi))

def graph(k):
    states=[(a,)+q for a in (8,17) for q in product(range(19),repeat=k-1)]
    adj={q:set(evolve(q,c) for c in (0,1)) for q in states}
    adj={q:{p for p in outs if p[0]==25-q[0]} for q,outs in adj.items()}
    reverse={q:set() for q in adj}
    for q,outs in adj.items():
        for p in outs:reverse[p].add(q)
    degree={q:len(outs) for q,outs in adj.items()};queue=deque(q for q,d in degree.items() if not d)
    dead=set(queue)
    while queue:
        q=queue.popleft()
        for p in reverse[q]:
            degree[p]-=1
            if not degree[p] and p not in dead:dead.add(p);queue.append(p)
    live={q:adj[q]-dead for q in adj if q not in dead}
    # SCCs by iterative Kosaraju.
    order=[];seen=set()
    for root in live:
        if root in seen:continue
        seen.add(root);stack=[(root,iter(live[root]))]
        while stack:
            node,it=stack[-1]
            try:
                v=next(it)
                if v not in seen:seen.add(v);stack.append((v,iter(live[v])))
            except StopIteration:order.append(node);stack.pop()
    seen=set();sccs=[]
    for root in reversed(order):
        if root in seen:continue
        seen.add(root);stack=[root];component=[]
        while stack:
            node=stack.pop();component.append(node)
            for v in reverse[node]:
                if v in live and v not in seen:seen.add(v);stack.append(v)
        if len(component)>1 or root in live[root]:sccs.append(component)
    result={'width':k,'states':len(states),'live_states':len(live),
            'cyclic_scc_sizes':sorted(len(s) for s in sccs)}
    if sum(map(len,sccs))<=200:result['cyclic_sccs']=sccs
    return result,live

if __name__=='__main__':
    result,live=graph(3)
    from functools import lru_cache
    core=set(map(tuple,result['cyclic_sccs'][0]))
    @lru_cache(None)
    def age(q):return 0 if q in core else 1+max(age(p)for p in live[q])
    result['max_transient_before_forced_cycle']=max(age(q)for q in live)
    print(json.dumps(result));open('novel_encoding_critical_clock3.json','w').write(json.dumps(result,indent=2))
