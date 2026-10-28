#!/usr/bin/env python3
"""Exact joint spatial columns 4/5 transfer for decimal g=(11000)^k.

The first three columns, for EVERY k>=1, are fixed by the published
Agent12ThreeColumnAllK proof. Third outgoing carry bits a,b in each
five-time block are free. Enumerate each fourth/fifth pair transition
from original bauto3 equations, then identify all cyclic SCCs.
"""
from collections import Counter
from itertools import product

G=(1,1,0,0,0)
L4=(1,1,0,0,1)
S=((9,9),(15,0),(15,9))
EXPECT=((0,1,1),(4,0,0),(2,0,0))


def fourth_five_steps(a,b):
    H4=(a,b,0,1,0);Y4=(5+a,b)
    for start in range(19):
        def step(t,x,xs,cs):
            if t==5:
                yield start,x,tuple(xs),tuple(cs)
                return
            for c in (0,1):
                if (x+c)//10!=H4[t]:continue
                nx=(x+L4[t])%10+(Y4[0 if t==0 else 1] if G[t]
                                      else (x+c)%10)
                assert 0<=nx<=18
                yield from step(t+1,nx,xs+[x],cs+[c])
        yield from step(0,start,[],[])


def fifth_five_steps(xs4,cs4):
    L5=tuple((xs4[t]+L4[t])//10 for t in range(5))
    H5=cs4
    Y5=((xs4[0]+cs4[0])%10,(xs4[1]+cs4[1])%10)
    for start in range(19):
        def step(t,x):
            if t==5:
                yield start,x
                return
            for c in (0,1):
                if (x+c)//10!=H5[t]:continue
                nx=(x+L5[t])%10+(Y5[0 if t==0 else 1] if G[t]
                                      else (x+c)%10)
                assert 0<=nx<=18
                yield from step(t+1,nx)
        yield from step(0,start)


def components(nodes,weighted):
    outs={v:set() for v in nodes}
    back={v:set() for v in nodes}
    for (u,v) in weighted:
        outs[u].add(v);back[v].add(u)
    seen=set();order=[]
    def visit(v):
        seen.add(v)
        for w in outs[v]:
            if w not in seen:visit(w)
        order.append(v)
    for v in nodes:
        if v not in seen:visit(v)
    comps=[];seen.clear()
    for v in reversed(order):
        if v in seen:continue
        stack=[v];seen.add(v);group=set()
        while stack:
            z=stack.pop();group.add(z)
            for w in back[z]:
                if w not in seen:seen.add(w);stack.append(w)
        comps.append(group)
    return comps


def product_matrix(A,B):
    return [[sum(A[i][t]*B[t][j] for t in range(len(A)))
        for j in range(len(A))] for i in range(len(A))]


def verify():
    weighted=Counter();four_paths=0
    for a,b in product((0,1),repeat=2):
        for u4,v4,xs4,cs4 in fourth_five_steps(a,b):
            four_paths+=1
            for u5,v5 in fifth_five_steps(xs4,cs4):
                weighted[((u4,u5),(v4,v5))]+=1
    assert four_paths==182
    assert len(weighted)==846
    assert sum(weighted.values())==2874
    nodes={u for u,v in weighted}|{v for u,v in weighted}
    assert len(nodes)==266
    comps=components(nodes,weighted)
    cyclic=[c for c in comps if len(c)>1 or any((v,v) in weighted for v in c)]
    assert len(comps)==264 and cyclic==[set(S)],(len(comps),cyclic)
    M=tuple(tuple(weighted[u,v] for v in S) for u in S)
    assert M==EXPECT,M
    assert M==((0,1,1),(4,0,0),(2,0,0))
    V=[[int(i==j) for j in range(3)] for i in range(3)]
    for k in range(1,21):
        V=product_matrix(V,M)
        got=sum(V[i][i] for i in range(3))
        want=0 if k%2 else 2*6**(k//2)
        assert got==want,(k,got,want)
        print(f'k={k} complete-five-column histories={got}')
    print('PASS full 266-state graph, 846 pairs, 2874 paths, unique 3-state cyclic SCC')
    print('matrix',M,'characteristic polynomial x*(x*x-6)')

if __name__=='__main__':verify()
