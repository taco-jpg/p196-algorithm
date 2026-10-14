"""Conditioned spatial extension of a forced outer clock, preserving phases.
No finite prefix certificate is treated as an infinite finite-seed proof.
"""
from novel_encoding_critical_clock import evolve
from collections import deque
import json

BASE=[(17,13,14),(8,12,9),(17,5,0),(8,13,5),(17,6,11),(8,14,8),(17,8,17),(8,16,16)]

def scc(adj):
    reverse={q:set() for q in adj}
    for a,outs in adj.items():
        for b in outs:reverse[b].add(a)
    order=[];seen=set()
    for root in adj:
        if root in seen:continue
        seen.add(root);stack=[(root,iter(adj[root]))]
        while stack:
            node,it=stack[-1]
            try:
                v=next(it)
                if v not in seen:seen.add(v);stack.append((v,iter(adj[v])))
            except StopIteration:order.append(node);stack.pop()
    seen=set();out=[]
    for root in reversed(order):
        if root in seen:continue
        seen.add(root);stack=[root];component=[]
        while stack:
            node=stack.pop();component.append(node)
            for v in reverse[node]:
                if v not in seen:seen.add(v);stack.append(v)
        if len(component)>1 or root in adj[root]:out.append(component)
    return out

def lift(clock):
    p=len(clock)
    adj={(t,x):set() for t in range(p) for x in range(19)}
    labels={}
    for t,x in adj:
        q=clock[t]+(x,)
        for carry in (0,1):
            out=evolve(q,carry)
            if out[:-1]==clock[(t+1)%p]:
                dst=((t+1)%p,out[-1]);adj[t,x].add(dst)
                labels.setdefault(((t,x),dst),[]).append(carry)
    cs=scc(adj)
    result={'width':len(clock[0])+1,'previous_period':p,'states':len(adj),'cyclic_scc_sizes':[len(c) for c in cs]}
    if len(cs)!=1:return result,None
    nodes=set(cs[0]);inner={n:adj[n]&nodes for n in nodes}
    result['branching_nodes']=sum(len(v)!=1 for v in inner.values())
    if result['branching_nodes']:return result,None
    start=min(nodes);cycle=[start];at=next(iter(inner[start]))
    while at!=start:
        cycle.append(at);at=next(iter(inner[at]))
    assert len(cycle)==len(nodes)
    newclock=[clock[t]+(x,) for t,x in cycle]
    result['period']=len(newclock)
    result['new_column']=[q[-1] for q in newclock]
    result['carry_choices']=[labels[(cycle[i],cycle[(i+1)%len(cycle)])] for i in range(len(cycle))]
    return result,newclock

if __name__=='__main__':
    clock=BASE;results=[]
    for width in range(4,25):
        result,newclock=lift(clock)
        results.append(result);print(json.dumps(result),flush=True)
        if newclock is None:break
        clock=newclock
        if len(clock)>100000:break
    open('novel_stack_spatial_lift_results.json','w').write(json.dumps(results,indent=2))
    open('novel_stack_spatial_lift_clock.json','w').write(json.dumps(clock,indent=2))
