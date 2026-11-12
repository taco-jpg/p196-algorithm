from lat10 import *
import time,sys
order,edges,live,comps,cyc,comp_of=load()
small=[k for k in range(len(comps)) if cyc[k] and len(comps[k])==20]
for k in small:
    walk=cycle_walk(edges,comp_of,comps[k][0])
    cn=[order[v] for v in walk]
    for P in (80,):
        for which in (0,1):
            t0=time.time()
            o2,e2,ok,cands,starts=centre_scan(cn,P,which,maxnodes=20000)
            lv,cp,cy=live_nodes(len(o2),[e or [] for e in e2])
            print('comp',k,'P',P,'which',which,'closure',len(o2),'complete',ok,'live',sum(lv),'cyclic comps',sorted([len(c) for i,c in enumerate(cp) if cy[i]]),'cands',cands,'time %.1f'%(time.time()-t0)); sys.stdout.flush()
