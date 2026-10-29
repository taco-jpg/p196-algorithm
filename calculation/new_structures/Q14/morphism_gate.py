#!/usr/bin/env python3
"""Exact graph criterion for bounded increments of a nonerasing morphism."""
from collections import deque
from math import lcm

def gate(sigma, seed):
    alphabet=set(sigma)
    assert seed and all(w and set(w)<=alphabet for w in sigma.values())
    assert set(seed)<=alphabet
    succ={x:list(w) for x,w in sigma.items()}
    rev={x:[] for x in alphabet}
    for x,cs in succ.items():
        for c in cs: rev[c].append(x)
    def reach(starts,edge):
        seen=set(starts); q=deque(starts)
        while q:
            for y in edge[q.popleft()]:
                if y not in seen: seen.add(y); q.append(y)
        return seen
    relevant=reach(seed,succ) & reach([x for x in alphabet if len(sigma[x])>1],rev)
    graph={x:[y for y in succ[x] if y in relevant] for x in relevant}
    ids={}; low={}; stack=[]; on=set(); comps=[]
    def visit(x):
        ids[x]=low[x]=len(ids); stack.append(x); on.add(x)
        for y in graph[x]:
            if y not in ids:
                visit(y); low[x]=min(low[x],low[y])
            elif y in on: low[x]=min(low[x],ids[y])
        if low[x]==ids[x]:
            C=[]
            while True:
                z=stack.pop(); on.remove(z); C.append(z)
                if z==x: break
            comps.append(C)
    for x in relevant:
        if x not in ids: visit(x)
    ix={x:i for i,C in enumerate(comps) for x in C}
    cyclic=[]
    for i,C in enumerate(comps):
        if not (len(C)>1 or any(x in graph[x] for x in C)): continue
        cyclic.append(i)
        for x in C:
            if sum(ix[y]==i for y in graph[x])!=1:
                return False,"branching productive SCC",C
    dag={i:set() for i in range(len(comps))}
    for x,ys in graph.items():
        for y in ys:
            if ix[x]!=ix[y]: dag[ix[x]].add(ix[y])
    for i in cyclic:
        todo=list(dag[i]); seen=set()
        while todo:
            j=todo.pop()
            if j in seen: continue
            seen.add(j)
            if j in cyclic:
                return False,"two productive cycle components in series",(comps[i],comps[j])
            todo.extend(dag[j])
    return True,"bounded increments",comps

def exact_increment_bound(sigma,seed):
    """Return (exact max Delta, checked prefix length, eventual period) or None."""
    ok,_,comps=gate(sigma,seed)
    if not ok: return None
    graph={x:list(w) for x,w in sigma.items()}
    cycles=[len(C) for C in comps if len(C)>1 or any(x in graph[x] for x in C)]
    period=lcm(*cycles) if cycles else 1
    n=len(sigma); horizon=3*n+2*period
    counts={x:seed.count(x) for x in sigma}; deltas=[]
    for _ in range(horizon):
        deltas.append(sum(counts[x]*(len(sigma[x])-1) for x in sigma))
        nxt={x:0 for x in sigma}
        for x,w in sigma.items():
            for y in w: nxt[y]+=counts[x]
        counts=nxt
    assert all(deltas[i]==deltas[i+period] for i in range(3*n,3*n+period))
    checked=3*n+period
    return max(deltas[:checked]),checked,period

def brute_increments(sigma,seed,upto=15):
    word=seed; lengths=[len(word)]
    for _ in range(upto):
        word="".join(sigma[x] for x in word); lengths.append(len(word))
        if len(word)>1_000_000: break
    return [b-a for a,b in zip(lengths,lengths[1:])]

if __name__=="__main__":
    cases=[
      ("rank2",{"A":"AB","B":"B"},"A",True),
      ("rank3",{"A":"AB","B":"BC","C":"C"},"A",False),
      ("fib",{"A":"AB","B":"A"},"A",False),
      ("periodic",{"A":"B","B":"A"},"AB",True),
      ("linear_alternating",{"A":"A01","0":"1","1":"0"},"A",True),
      ("invisible_expander",{"A":"AB","B":"BB","X":"X"},"X",True)]
    for name,sigma,seed,expected in cases:
        ok,why,_=gate(sigma,seed); assert ok==expected,(name,ok,why)
        print(name,ok,why,exact_increment_bound(sigma,seed),brute_increments(sigma,seed,10))
