#!/usr/bin/env python3
"""Uncapped exact 36-vertex carry graph proof of sharp changed-run bounds
in the decimal p=12, m=9 no-overflow lattice.
Usage: python3 sharp_streak.py lattice_input.txt
"""
from pathlib import Path
from collections import deque,defaultdict
import json,sys

def load(fn):
    ns=iter(map(int,Path(fn).read_text().split()))
    p,k,m,b=[next(ns) for _ in range(4)]
    assert (p,k,m,b)==(12,34,9,10)
    g=[next(ns) for _ in range(p)]
    w=[[next(ns) for _ in range(m)] for _ in range(p)]
    cups=[[next(ns) for _ in range(m)] for _ in range(p)]
    border=[[next(ns) for _ in range(k)] for _ in range(p)]
    assert next(ns,None) is None
    return g,w,border

def baseline_table(t,w,border,n=400):
    p=[0]*n
    for i in range(n//2):
        v=border[t][i] if i<34 else w[t][(i-34)%9]
        p[i]=p[n-1-i]=v
    C=[0];o=[]
    for v in p:
        z=v+C[-1];o.append(z%10);C.append(z//10)
    assert C[-1]==0
    base=34+18
    tab=[]
    for r in range(9):
        i=base+r
        tab.append((p[i],o[i]+o[n-1-i],C[i],C[n-i]))
    for i in range(52,n//2-10):
        assert (p[i],o[i]+o[n-1-i],C[i],C[n-i])==tab[(i-52)%9]
    return tab

def graph(tab):
    adj=defaultdict(list);rev=defaultdict(list)
    for r,(q,s,_,_) in enumerate(tab):
        for a in range(2):
            for b in range(2):
                state=(r,a,b)
                for x in range(19):
                    for u in range(2):
                        if (x+u)//10!=b:continue
                        if (x+a)%10+(x+u)%10 !=s:continue
                        dst=((r+1)%9,(x+a)//10,u)
                        diff=(x!=q)
                        adj[state].append((dst,diff,x))
                        rev[dst].append((state,diff,x))
    return adj,rev

def closure(init,arcs):
    seen=set(init);todo=deque(init)
    while todo:
        s=todo.popleft()
        for v,_,_ in arcs[s]:
            if v not in seen:seen.add(v);todo.append(v)
    return seen

def longest_dag(s,allowed,adj,gray,cache):
    if s in cache:return cache[s]
    assert s not in gray,('change-only cycle',s)
    gray.add(s)
    val=0
    for v,diff,_ in adj[s]:
        if diff and v in allowed:
            val=max(val,1+longest_dag(v,allowed,adj,gray,cache))
    gray.remove(s)
    cache[s]=val
    return val

def decide(tab):
    adj,rev=graph(tab)
    base={(r,*tab[r][2:]) for r in range(9)}
    starts={dst for state in base for dst,diff,_ in adj[state] if diff}
    reachable=closure(starts,adj)
    co=closure(base,rev)
    relevant=reachable & co
    # All relevant paths start after at least one actual source change and
    # can finish with a return to baseline carries. Any finite-support
    # one-step collision's inside path lives in this exact subgraph.
    cache={};maximum=0
    for s in relevant:
        maximum=max(maximum,longest_dag(s,relevant,adj,set(),cache))
    # Include a changed run starting at the very first defect edge, whose
    # source is a baseline cut and need not itself lie in relevant.
    initial_bound=max([0]+[1+longest_dag(dst,relevant,adj,set(),cache)
        for b in base for dst,diff,_ in adj[b] if diff and dst in relevant])
    maximum=max(maximum,initial_bound)
    return [maximum,len(relevant),sum(map(len,adj.values())),len(starts)]

def main(fn):
    g,w,b=load(fn)
    assert g==[1,0,0,0]*3
    entries=[]
    for t in range(12):
        if g[t]:continue
        tab=baseline_table(t,w,b)
        ans=decide(tab)
        entries.append([t]+ans)
        print('PHASE',t,'MAX_CHANGED_RUN',ans[0],'RELEVANT_STATES',ans[1], 'EDGES',ans[2], 'CHANGED_ROOTS',ans[3])
    assert [e[1] for e in entries]==[3,5,0,3,5,0,3,5,0]
    print('SHARP_RUN_BOUND_3_5_ALL_WIDTH_PASS')
    print('SUMMARY_JSON',json.dumps(entries,separators=(',',':')))

if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).with_name('lattice_input.txt')))
