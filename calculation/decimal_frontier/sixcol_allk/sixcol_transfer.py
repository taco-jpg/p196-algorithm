#!/usr/bin/env python3
"""Finite all-k no-go at SIX spatial columns for base-10 g=(11000)^k.

Use the prior all-k three-column lemma (repeated coefficients, independent
third outgoing carry choices a,b) and re-enumerate EVERY subsequent column
from original bauto3 position equations. This checker also reconstructs the
full fifth-column graph and its unique cyclic three-state SCC, rather than
assuming its matrix. The subsequent sixth-column graph has no path of length 2.
"""
from collections import Counter
from itertools import product

G=(1,1,0,0,0)
L4=(1,1,0,0,1)
EXPECTED_S={(9,9),(15,0),(15,9)}


def steps(L,H,Y):
    """Every five-step column path; return (start,end,x_history,chosen_carry)."""
    assert len(L)==len(H)==5 and len(Y)==2
    for initial in range(19):
        def recur(t,x,xs,cs):
            if t==5:
                yield initial,x,tuple(xs),tuple(cs)
                return
            for c in (0,1):
                if (x+c)//10 != H[t]:continue
                nextx=(x+L[t])%10+(Y[0 if t==0 else 1] if G[t]
                                        else (x+c)%10)
                assert 0<=nextx<=18
                yield from recur(t+1,nextx,xs+[x],cs+[c])
        yield from recur(0,initial,[],[])


def sccs(nodes,edges):
    out={v:set() for v in nodes}
    back={v:set() for v in nodes}
    for u,v in edges:
        out[u].add(v);back[v].add(u)
    seen=set();order=[]
    def dfs(v):
        seen.add(v)
        for w in out[v]:
            if w not in seen:dfs(w)
        order.append(v)
    for v in nodes:
        if v not in seen:dfs(v)
    seen.clear();cc=[]
    for v in reversed(order):
        if v in seen:continue
        stack=[v];seen.add(v);group=set()
        while stack:
            z=stack.pop();group.add(z)
            for w in back[z]:
                if w not in seen:seen.add(w);stack.append(w)
        cc.append(group)
    return cc


def run():
    fifth=Counter()
    kept=[]
    fourth_count=0
    fifth_count=0
    for a,b in product((0,1),repeat=2):
        for u4,v4,x4,c4 in steps(L4,(a,b,0,1,0),(5+a,b)):
            fourth_count+=1
            L5=tuple((x4[t]+L4[t])//10 for t in range(5))
            Y5=((x4[0]+c4[0])%10,(x4[1]+c4[1])%10)
            for u5,v5,x5,c5 in steps(L5,c4,Y5):
                fifth_count+=1
                u=(u4,u5);v=(v4,v5)
                fifth[(u,v)]+=1
                if u in EXPECTED_S and v in EXPECTED_S:
                    kept.append((u,v,x4,c4,x5,c5,L5))
    assert fourth_count==182
    assert fifth_count==2874
    assert len(fifth)==846
    V5={u for u,v in fifth}|{v for u,v in fifth}
    assert len(V5)==266
    comp5=sccs(V5,fifth)
    recur5=[c for c in comp5 if len(c)>1 or any((v,v) in fifth for v in c)]
    assert len(comp5)==264 and len(recur5)==1 and recur5[0]==EXPECTED_S
    assert len(kept)==8
    assert [fifth[(u,v)] for u,v in [((9,9),(15,0)),((9,9),(15,9)),
        ((15,0),(9,9)),((15,9),(9,9))]]==[1,1,4,2]
    sixth=Counter()
    for u,v,x4,c4,x5,c5,L5 in kept:
        L6=tuple((x5[t]+L5[t])//10 for t in range(5))
        Y6=((x5[0]+c5[0])%10,(x5[1]+c5[1])%10)
        for u6,v6,x6,c6 in steps(L6,c5,Y6):
            sixth[(u+(u6,),v+(v6,))]+=1
    assert len(sixth)==54 and sum(sixth.values())==104
    sources={u for u,v in sixth};targets={v for u,v in sixth}
    assert len(sources)==9 and len(targets)==16
    assert sources.isdisjoint(targets)
    assert all(u[:2] in {(15,0),(15,9)} for u in sources)
    assert all(v[:2]==(9,9) for v in targets)
    V6=sources|targets
    assert len(V6)==25
    assert len(sccs(V6,sixth))==25
    print('Fourth paths:',fourth_count,'fifth paths:',fifth_count)
    print('Full fifth graph:',len(V5),'states,',len(fifth),'weighted ordered edges')
    print('Fifth cyclic SCC:',sorted(EXPECTED_S),'with 8 local path realizations')
    print('Sixth restricted graph:',len(V6),'nodes,',len(sixth),'pairs, 104 paths')
    print('Sixth sources:',len(sources),'targets:',len(targets),'intersection:',len(sources&targets))
    print('PASS: no two consecutive sixth-column edges; no time-closed sixth column for ANY k>=1')

if __name__=='__main__':run()
