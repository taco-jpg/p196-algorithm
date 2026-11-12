from pipeline import *
B=10
for P,cap in ((16,1000000),(24,1000000)):
    for g in necklaces_all(P):
        F0=Frame(B,(0,)*P,g)
        starts=expand(F0,root_node(B,g))
        if not starts: continue
        r=run_closure(F0,starts,maxnodes=cap)
        if not r['complete']: print('P',P,'capped clock',''.join(map(str,g)),'nodes',r['nodes'],'live in partial graph',r['live'])
