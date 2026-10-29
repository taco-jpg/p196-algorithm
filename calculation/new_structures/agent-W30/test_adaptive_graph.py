#!/usr/bin/env python3
"""W30: independently check the whole binary 1800-state carry-fibre graph.

Checks every reachable bulk state, both overflow labels forced by opposite caps,
against actual Python arbitrary-precision integer reverse-and-add; no use of
C++ coefficient stepping. An independent 12-period carry iteration must agree
with the cyclic solver and all 3600 finite edges.
"""
from collections import deque,Counter
import json
from pathlib import Path
from fibre_graph import f, reflect, cyclic_carry

def independent_carry(r, reverse):
    c=0; rows=[]
    for j in range(5*12):
        i=(-j if reverse else j)%5
        if j>=5*11: rows.append((i,c))
        c=(r[i]+c)//10
    out=[None]*5
    for i,v in rows:out[i]=v
    assert None not in out
    return tuple(out)

def explicit_number(seed):
    n=len(seed); d=[0]*n
    for i in range(n//2):
        p=seed[i];d[i]=max(0,p-9);d[n-1-i]=p-d[i]
    assert d[-1]!=0 and all(d[i]+d[n-1-i]==seed[i] for i in range(n))
    return int(''.join(map(str,reversed(d))))

def next_pair_by_int(P):
    n=explicit_number(P)
    result=n+int(str(n)[::-1])
    d=[int(x) for x in str(result)[::-1]]
    return tuple(d[i]+d[-1-i] for i in range(len(d)))

def test():
    start=((17,3,14,3,17),4)
    queue=deque([start]);seen={start};graph={};odd=0;nines=0
    for_cap=Counter();checked=0
    while queue:
        st=queue.popleft();r,delta=st
        assert reflect(r,delta)
        odd+=any(a%2 for a in r);nines+=9 in r
        for reverse in (False,True):
            aa=cyclic_carry(r,reverse)
            assert len(aa)==1,(st,reverse,aa)
            bb=independent_carry(r,reverse)
            assert aa[0]==bb,(st,reverse,aa,bb)
        outgoing=[]
        for gamma,cap in ((0,1),(1,17)):
            # Even L with L-1 == delta (mod 5); periodic centre is palindromic.
            L=next(k for k in range(100,112,2) if (k-1)%5==delta)
            P=(cap,)+tuple(r[i%5] for i in range(L))+(cap,)
            assert tuple(reversed(P))==P
            nxt=next_pair_by_int(P)
            observed_gamma=len(nxt)-len(P)
            assert observed_gamma==gamma,(st,gamma,observed_gamma)
            predicted=f(r,gamma)
            assert predicted is not None
            for i in range(11,L-10):
                assert nxt[1+i]==predicted[i%5],(st,gamma,i,nxt[1+i],predicted[i%5])
                checked+=1
            dest=(predicted,(delta+gamma)%5)
            assert reflect(*dest)
            if dest not in seen:seen.add(dest);queue.append(dest)
            outgoing.append(dest)
            for_cap[gamma]+=1
        graph[st]=outgoing
    # Independent Kosaraju SCC, iterative, deterministic.
    rev={x:[] for x in graph}
    for x,ys in graph.items():
        for y in ys:rev[y].append(x)
    visited=set();order=[]
    for x in graph:
        if x in visited:continue
        visited.add(x);stk=[(x,0)]
        while stk:
            a,k=stk[-1]
            if k<len(graph[a]):
                y=graph[a][k];stk[-1]=(a,k+1)
                if y not in visited:visited.add(y);stk.append((y,0))
            else:
                order.append(a);stk.pop()
    unseen=set(graph);scc=[]
    for x in reversed(order):
        if x not in unseen:continue
        unseen.remove(x);comp=[];Q=[x]
        while Q:
            a=Q.pop();comp.append(a)
            for y in rev[a]:
                if y in unseen:unseen.remove(y);Q.append(y)
        scc.append(comp)
    assert len(scc)==1 and len(scc[0])==1800
    assert len(seen)==1800 and nines==190 and odd==1290 and for_cap[0]==for_cap[1]==1800
    out={
        'label':'COMPUTED', 'base':10,'row_period':5, 'seed_row':[17,3,14,3,17], 'seed_mirror_axis':4,
        'reachable_reflection_states':len(seen),'reachable_scc_count':len(scc),'largest_scc_size':max(map(len,scc)),
        'states_with_coefficient_9':nines,'states_with_an_odd_coefficient':odd,'states_all_even':len(seen)-odd,
        'states_ambiguous_cyclic_carries':0,'edges':sum(map(len,graph.values())),
        'cap_forced_gamma_0_edges':for_cap[0],'cap_forced_gamma_1_edges':for_cap[1],
        'independent_integer_interior_equalities':checked,
        'scope':'entire reachable closed 1800-state component under arbitrary gamma, NOT a rooted infinite orbit'
    }
    with open(str(Path(__file__).with_name('adaptive_graph1800.json')),'w') as h:json.dump(out,h,indent=2,sort_keys=True);h.write('\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':test()
