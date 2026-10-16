"""Finite automata for repeated no-overflow inverse layers.

Target pair words are scanned outside in. Each inverse layer is the
exact folded four-carry-state automaton, not an equidistribution model.
"""
from collections import deque, Counter
from itertools import product
from functools import lru_cache
import json


@lru_cache(None)
def local(st, s):
    a,b=st
    out=[]
    for x in range(19):
        for bp in (0,1):
            ap,lo=divmod(x+a,10)
            bh,hi=divmod(x+bp,10)
            if bh==b and lo+hi==s:
                out.append(((ap,bp),x))
    return tuple(out)


@lru_cache(None)
def layers(states,s):
    if not states:
        return (((),()),)
    ans=[]
    for ns,x in local(states[0],s):
        for tail,labels in layers(states[1:],x):
            ans.append(((ns,)+tail,(x,)+labels))
    return tuple(ans)


def graph(depth):
    root=tuple((0,0) for _ in range(depth))
    first=frozenset(ns for ns,labels in layers(root,14) if all(labels))
    states=[first]
    ix={first:0}
    trans=[]
    todo=deque([first])
    while todo:
        st=todo.popleft()
        row=[]
        for s in (5,14):
            target=frozenset(ns for path in st for ns,_ in layers(path,s))
            if target not in ix:
                ix[target]=len(states);states.append(target);todo.append(target)
            row.append(ix[target])
        trans.append(row)
    accepting=[any(all(a==b for a,b in path) for path in st) for st in states]
    return states,trans,accepting


def sccs(trans):
    n=len(trans)
    index=[-1]*n;low=[0]*n;stack=[];active=set();scc=[]
    def visit(v):
        index[v]=low[v]=len([x for x in index if x>=0])
        stack.append(v);active.add(v)
        for w in trans[v]:
            if index[w]<0:
                visit(w);low[v]=min(low[v],low[w])
            elif w in active:low[v]=min(low[v],index[w])
        if low[v]==index[v]:
            comp=[]
            while True:
                w=stack.pop();active.remove(w);comp.append(w)
                if w==v:break
            scc.append(comp)
    for v in range(n):
        if index[v]<0:visit(v)
    return scc


def main():
    out=[]
    for depth in range(1,4):
        states,trans,accept=graph(depth)
        components=sccs(trans)
        useful_closed=[c for c in components if any(accept[v] for v in c) and all(w in c for v in c for w in trans[v])]
        vec=Counter({0:1});counts=[]
        for m in range(41):
            counts.append(sum(n for i,n in vec.items() if accept[i]))
            nv=Counter()
            for i,n in vec.items():
                for j in trans[i]:nv[j]+=n
            vec=nv
        row=dict(depth=depth,states=len(states),nondeterministic_states=sum(len(s)>1 for s in states),components=[len(c) for c in components],useful_closed=[dict(size=len(c),accepted=sum(accept[v] for v in c)) for c in useful_closed],counts=counts)
        print(row,flush=True)
        out.append(dict(**row,state_lists=[[[list(c) for c in path] for path in sorted(st)] for st in states],transitions=trans,accepting=accept))
    with open('astra_counting_nooverflow_depth_results.json','w') as f:json.dump(out,f,indent=2)


if __name__=='__main__':main()
