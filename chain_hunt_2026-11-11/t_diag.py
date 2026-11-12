from scan_centre import *
k=[k for k in range(len(comps)) if cyc[k] and len(comps[k])==20][0]
cn=[order[v] for v in cycle_walk(edges,comp_of,comps[k][0])]
for mx in (20,100,400,1600):
    t0=time.time()
    r=centre_run(cn,80,maxnodes=mx)
    print('maxnodes',mx,'nodes',r.get('nodes'),'expanded',r.get('expanded'),'complete',r.get('complete'),'dfs',r.get('dfs'),'time %.1f'%(time.time()-t0)); sys.stdout.flush()
