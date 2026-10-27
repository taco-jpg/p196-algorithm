#!/usr/bin/env python3
"""Exact bounded base-10 signed two-neutral-band transfer graph.

Scope: |A|=|E|=|M|=1, B=D=empty; all (x,u) in 0..9 squared;
one signed move in {-1,0,1} at each of eight boundaries, fixed order.
All other phase sizes / longer or multiple moves are OUTSIDE scope.
"""
from itertools import product
from collections import defaultdict,deque,Counter
from two_band import Phase,image_blocks,valid_phase,word,val
from signed_rewrite import Move,apply_moves,signed_edge,signed_cycleOK
import sys
BASE=10
SHIFT=(-1,0,1)
side=defaultdict(list)
for l,r in product(SHIFT,repeat=2):side[l+r].append((l,r))
PAIRS=[(l1,r1,l2,r2,k) for k in sorted(side)
       for l1,r1 in side[k] for l2,r2 in side[k]]
assert len(PAIRS)==19

def mk(triple,x=0,u=0):
    a,e,B,D,M=triple
    return Phase((a,),(B,),M,(D,),(e,),x,9-x,u,9-u)

def active_triples():
    out=[]
    for a,e,B,D in product(range(10),repeat=4):
        if not a:continue
        for mm in (1,2):
            for M in product(range(10),repeat=mm):
                _,r,_=image_blocks(BASE,mk((a,e,B,D,M)))
                if r[0]+r[3]==9 and r[1]+r[2]==9:
                    out.append((a,e,B,D,M))
    return out

def graph():
    triples=active_triples();lookup={z:i for i,z in enumerate(triples)}
    links=[[] for _ in triples]
    rejections=Counter();ntraces=0
    cache={}
    for k,tr in enumerate(triples):
        fixed,runs,_=image_blocks(BASE,mk(tr))
        signature=(fixed,runs)
        if signature not in cache:
            outcomes=[];reject=Counter()
            for l0,r0,l3,r3,dg in PAIRS:
              for l1,r1,l2,r2,dh in PAIRS:
                moves=(Move(0,'L',l0),Move(0,'R',r0),Move(1,'L',l1),Move(1,'R',r1),
                       Move(2,'L',l2),Move(2,'R',r2),Move(3,'L',l3),Move(3,'R',r3))
                result=apply_moves(fixed,runs,moves)
                if result is None:
                    reject['bad_move']+=1;continue
                blocks,shifts,needs=result
                assert shifts==(dg,dh,dh,dg)
                if [len(z) for z in blocks] not in ([1,1,1,1,1],[1,1,2,1,1]):
                    reject['bad_width']+=1;continue
                nt=(blocks[0][0],blocks[4][0],blocks[1][0],blocks[3][0],blocks[2])
                nxt=lookup.get(nt)
                if nxt is None:
                    reject['target_not_active']+=1;continue
                if signed_edge(BASE,mk(tr),mk(nt,runs[0],runs[1]),moves)!=(dg,dh,*needs):
                    raise AssertionError('independent edge check failed')
                outcomes.append((nxt,dg,dh,needs,moves,runs))
            cache[signature]=(outcomes,reject)
        outcomes,reject=cache[signature]
        links[k]=outcomes
        rejections.update(reject)
        ntraces+=len(outcomes)
    print('unique_output_signatures',len(cache),'source_triples',len(triples),flush=True)
    # Integer arithmetic independently checks every retained trace for
    # three genuinely different source band characters and two length pairs.
    checked=0
    for i,row in enumerate(links):
        for nxt,dg,dh,needs,moves,runs in row:
            for xx,uu in ((0,0),(5,7),(9,9)):
                p=mk(triples[i],xx,uu)
                qphase=mk(triples[nxt],runs[0],runs[1])
                for g,h in ((3,4),(6,5)):
                    inp=word(p,g,h)
                    lhs=val(10,inp)+val(10,inp[::-1])
                    rhs=val(10,word(qphase,g+dg,h+dh))
                    assert lhs==rhs
                    checked+=1
    print('independent_integer_crosschecks',checked,'PASS')
    indeg=[0]*len(triples)
    for row in links:
        for j,*_ in row:indeg[j]+=1
    q=deque(i for i,x in enumerate(indeg) if x==0)
    rem=0;dist=[0]*len(triples)
    while q:
        i=q.popleft();rem+=1
        for j,*_ in links[i]:
            if dist[j]<dist[i]+1:dist[j]=dist[i]+1
            indeg[j]-=1
            if indeg[j]==0:q.append(j)
    # Independent iterative DFS, separate from Kahn indegree peeling.
    color=bytearray(len(triples));dfs_done=0
    for root in range(len(triples)):
        if color[root]:continue
        color[root]=1;stack=[(root,0)]
        while stack:
            v,pos=stack[-1]
            if pos==len(links[v]):
                color[v]=2;dfs_done+=1;stack.pop();continue
            stack[-1]=(v,pos+1)
            w=links[v][pos][0]
            if color[w]==1:raise AssertionError('Directed cycle!')
            if color[w]==0:
                color[w]=1;stack.append((w,0))
    assert dfs_done==len(triples)
    print('independent_iterative_DFS_acyclic',True,'visited',dfs_done)
    print('active_fixed_states_A1B1M1_M2',len(triples),'implicit_phases',len(triples)*100,'ordered_boundary_move_pairs',len(PAIRS)**2)
    print('actual_accepted_traces',ntraces,'triple_graph_edges',sum(map(len,links)),
          'kahn_removed',rem,'cyclic_core',len(triples)-rem,'max_path_edges',max(dist),'rejections',dict(rejections))
    return triples,links,indeg

if __name__=='__main__':graph()