#!/usr/bin/env python3
"""Reproducible BOUNDED base-2 discovery check, not a complete all-width proof."""
from itertools import product
from collections import defaultdict, deque, Counter
from two_band import Phase, image_blocks
from signed_rewrite import Move, apply_moves, signed_edge, signed_cycleOK

BASE=2
MAX_A, MAX_B, MAX_M = 2, 2, 4
SHIFT=(-1,0,1)

def bits(n):
    return product(range(BASE), repeat=n)

def phases():
    for a in range(1,MAX_A+1):
        for A in bits(a):
            if A[0]==0:continue
            for E in bits(a):
                for d in range(MAX_B+1):
                    for B in bits(d):
                        for D in bits(d):
                            for m in range(MAX_M+1):
                                for M in bits(m):
                                    for x,u in product(range(BASE),repeat=2):
                                        yield Phase(A,B,M,D,E,x,BASE-1-x,u,BASE-1-u)

side_pairs=defaultdict(list)
for l,r in product(SHIFT,repeat=2):
    side_pairs[l+r].append((l,r))
PAIRS=[(l1,r1,l2,r2,k) for k in sorted(side_pairs)
       for l1,r1 in side_pairs[k] for l2,r2 in side_pairs[k]]
assert len(PAIRS)==19

def build():
    states=list(phases())
    index={p:i for i,p in enumerate(states)}
    edges=[[] for _ in states]
    counts=Counter()
    active=0
    for i,p in enumerate(states):
        blocks,runs,_=image_blocks(BASE,p)
        if runs[0]+runs[3]!=BASE-1 or runs[1]+runs[2]!=BASE-1:continue
        active+=1
        for l0,r0,l3,r3,dg in PAIRS:
            for l1,r1,l2,r2,dh in PAIRS:
                trace=(Move(0,'L',l0),Move(0,'R',r0),
                       Move(1,'L',l1),Move(1,'R',r1),
                       Move(2,'L',l2),Move(2,'R',r2),
                       Move(3,'L',l3),Move(3,'R',r3))
                result=apply_moves(blocks,runs,trace)
                if result is None:continue
                newblocks,offs,_=result
                assert offs==(dg,dh,dh,dg)
                q=Phase(*newblocks,runs[0],runs[3],runs[1],runs[2])
                j=index.get(q)
                if j is not None:
                    edges[i].append((j,dg,dh))
                    counts[(dg,dh)]+=1
    indeg=[0]*len(states)
    for row in edges:
        for j,dg,dh in row:indeg[j]+=1
    q=deque(i for i,d in enumerate(indeg) if d==0)
    removed=0
    while q:
        i=q.popleft()
        removed+=1
        for j,dg,dh in edges[i]:
            indeg[j]-=1
            if indeg[j]==0:q.append(j)
    print('states',len(states),'active',active,'edges',sum(map(len,edges)),
          'kahn_removed',removed,'cyclic_core',len(states)-removed)
    assert (len(states),active,sum(map(len,edges)),removed)==(26040,6720,12088,26028)
    return states,index,edges

def positive_control(states,index,edges):
    ps=[
        Phase((1,0),(1,1),(1,1,0,1),(0,0),(0,0),1,0,1,0),
        Phase((1,1),(0,0),(1,0,0,0),(1,1),(0,1),0,1,0,1),
        Phase((1,0),(1,1),(1,0,1),(0,0),(0,0),1,0,1,0),
        Phase((1,1),(0,0),(0,1,0),(1,1),(0,1),0,1,0,1),
    ]
    traces=[
        (),
        (Move(0,'L',1),Move(0,'R',-1),Move(1,'L',1),Move(2,'L',1)),
        (),
        (Move(0,'L',1),Move(0,'R',-1),Move(1,'L',1),Move(1,'R',-1)),
    ]
    for i in range(4):
        e=signed_edge(BASE,ps[i],ps[(i+1)%4],traces[i])
        assert e is not None
        assert (index[ps[(i+1)%4]],*e[:2]) in edges[index[ps[i]]]
    seed=signed_cycleOK(BASE,ps,traces)
    assert seed==(0,0)
    print('accepted_four_phase_gain_g0_h1',True,'minimum_seed',seed)

if __name__=='__main__':
    positive_control(*build())
