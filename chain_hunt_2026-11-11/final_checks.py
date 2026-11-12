from pipeline import *
from lat10 import load, cycle_walk
import numpy as np, time
B=10
# (1) completeness of rooted closures for all clocks with time period <= 12
t0=time.time(); tot=0; capped=[]; liveclocks=[]
for P in range(1,13):
    for g in necklaces_all(P):
        tot+=1
        F0=Frame(B,(0,)*P,g)
        starts=expand(F0,root_node(B,g))
        if not starts: continue
        r=run_closure(F0,starts,maxnodes=2000000)
        if not r['complete']: capped.append((P,g,r['nodes']))
        if r['live']>0: liveclocks.append((P,''.join(map(str,g)),r['nodes'],r['live'],sorted(c['size'] for c in r['cyc'])))
print('clock words tested (necklaces, period<=12):',tot,'capped:',capped,'time %.0fs'%(time.time()-t0))
for x in liveclocks: print('  live:',x)
# (2) clock 10 SCC growth rate, 9-runs, witnesses
order,edges,live,comps,cyc,comp_of=load()
big=max((k for k in range(len(comps)) if cyc[k]),key=lambda k:len(comps[k]))
idx={v:i for i,v in enumerate(comps[big])}
n=len(idx); A=np.zeros((n,n))
for v in comps[big]:
    for w in edges[v]:
        if w in idx: A[idx[v],idx[w]]+=1
ev=np.linalg.eigvals(A)
print('big SCC size',n,'spectral radius %.5f'%max(abs(ev)))
roots=[i for i,H in enumerate(order) if all(x==0 for x in H[2])]
for k in [k for k in range(len(comps)) if cyc[k] and len(comps[k])==20]:
    walk=cycle_walk(edges,comp_of,comps[k][0])
    left=find_path(edges,roots,walk[0])[:-1]
    cols=left+walk*3
    rmax=0
    for t in range(8):
        run=0
        for v in cols:
            if order[v][0][t]+order[v][1][t]==9: run+=1; rmax=max(rmax,run)
            else: run=0
    wit=[next((i for i,v in enumerate(left) if order[v][0][t]!=order[v][1][t]),None) for t in range(8)]
    print('20-cycle comp',k,'left width',len(left),'max run of pair-sum 9 in a row:',rmax,'first asymmetric column at each phase:',wit)
    top=''.join(str(order[v][1][0]) for v in left); bot=''.join(str(order[v][0][0]) for v in left)
    print('   t=0 left end high digits (MSB first):',top); print('   t=0 left end low digits (LSB first): ',bot)
    print('   lattice period pair sums t=0:',[order[v][0][0]+order[v][1][0] for v in walk])
