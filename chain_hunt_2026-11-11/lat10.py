from tools import *
import pickle
from collections import deque
B=10
G2=(1,0)
def load():
    order,edges=pickle.load(open('clock10_p8.pkl','rb'))
    n=len(order)
    live,comps,cyc=live_nodes(n,edges)
    comp_of=[0]*n
    for k,cm in enumerate(comps):
        for v in cm: comp_of[v]=k
    return order,edges,live,comps,cyc,comp_of
def cycle_walk(edges,comp_of,v):
    k=comp_of[v]; walk=[v]
    while True:
        nx=[w for w in edges[walk[-1]] if comp_of[w]==k]
        assert len(nx)==1
        if nx[0]==v: break
        walk.append(nx[0])
    return walk
def fold_frame(P, which=0):
    """clock 10 repeated; overflow at even t; advance at every other overflow (t%4==2 if which==0 else t%4==0)."""
    g=G2*(P//2)
    adv={t for t in range(P) if t%4==(2 if which==0 else 0)}
    return (g,)+make_frame(B,g,adv)
def centre_scan(cyc_nodes, P, which=0, maxnodes=200000, verbose=False):
    """cyc_nodes: list of outer-frame nodes forming a cycle (length m). Returns (closure size, complete, candidates)."""
    g,F,phi=fold_frame(P,which)
    m=len(cyc_nodes)
    assert phi[P]%m==0, (phi[P],m)
    cells=lattice_cells(B,cyc_nodes)
    starts=[sheared_node(B,F,phi,cells,j) for j in range(m)]
    o2,e2,ok=closure(F,starts,maxnodes=maxnodes,verbose=verbose)
    # sanity: each start must have the next start as successor
    idx={H:i for i,H in enumerate(o2)}
    for j in range(m):
        assert idx[starts[(j+1)%m]] in e2[idx[starts[j]]], 'lattice not a cycle in sheared frame'
    cands=[]
    for case in ('i','ii'):
        par=parity_seq(g,F.alpha,case)
        if par is None: continue
        for i,H in enumerate(o2):
            if e2[i] is None: continue
            for w in e2[i]:
                if mirror_edge(H,o2[w],par,case):
                    cands.append((case,i,w))
    return o2,e2,ok,cands,starts
