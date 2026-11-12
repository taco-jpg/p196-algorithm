from pipeline import *
import time,sys
B=10
t0=time.time()
for P in map(int,sys.argv[1:]):
    tot=0; capped=0; live=[]; maxn=0
    for g in necklaces_all(P):
        tot+=1
        F0=Frame(B,(0,)*P,g)
        starts=expand(F0,root_node(B,g))
        if not starts: continue
        r=run_closure(F0,starts,maxnodes=1000000)
        maxn=max(maxn,r['nodes'])
        if not r['complete']: capped+=1
        if r['live']>0: live.append((''.join(map(str,g)),r['nodes'],r['live'],sorted(c['size'] for c in r['cyc'])))
    print('P=%d clocks=%d capped=%d maxclosure=%d live=%s  (%.0fs)'%(P,tot,capped,maxn,live,time.time()-t0)); sys.stdout.flush()
