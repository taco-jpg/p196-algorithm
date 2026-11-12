from cx import *
from lat10 import load, cycle_walk, fold_frame
import time, sys, pickle
B=10
order,edges,live,comps,cyc,comp_of=load()
def centre_run(cn, P, which=0, maxnodes=3000000, dump=False, timeout=None):
    g,F,phi=fold_frame(P,which)
    m=len(cn)
    assert phi[P]%m==0
    cells=lattice_cells(B,cn)
    starts=[sheared_node(B,F,phi,cells,j) for j in range(m)]
    starts=list(dict.fromkeys(starts))
    pars=[]
    for cas,name in ((1,'i'),(2,'ii')):
        par=parity_seq(g,F.alpha,name)
        if par is not None: pars.append((cas,par))
    r=run_closure(F,starts,pars=pars,maxnodes=maxnodes,dump=dump,timeout=timeout)
    r['nstart']=len(starts); r['F']=F; r['phi']=phi; r['starts']=starts
    return r
if __name__=='__main__':
    small=[k for k in range(len(comps)) if cyc[k] and len(comps[k])==20]
    for k in small:
        cn=[order[v] for v in cycle_walk(edges,comp_of,comps[k][0])]
        for P in map(int,sys.argv[1:]):
            t0=time.time()
            r=centre_run(cn,P)
            print('20-cycle comp',k,'P',P,'nstart',r['nstart'],'nodes',r.get('nodes'),'complete',r.get('complete'),'live',r.get('live'),
                  'cyc',[(c['size'],c['hasstart']) for c in r['cyc']],'cands',len(r['cands']),'dfs',r.get('dfs'),'time %.1f'%(time.time()-t0)); sys.stdout.flush()
