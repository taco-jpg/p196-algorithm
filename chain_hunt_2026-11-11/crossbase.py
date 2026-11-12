from pipeline import *
import sys
maxP=int(sys.argv[1]); maxQ=int(sys.argv[2])
summary={}
for B in map(int,sys.argv[3:]):
    t0=time.time(); nroot=0; ncert=0; kinds=[]; best=None
    for P in range(1,maxP+1):
        for g in necklaces_all(P):
            r=rooted(B,g,maxnodes=200000)
            if r is None: continue
            for c,walk in cycles_of(r):
                H=r['order'][walk[0]]
                if min_period(list(zip(*H)))!=P: continue
                ps=psums(H)
                kind='wire' if all(s==B-1 for s in ps) else ('uni' if len(walk)==1 else 'm%d'%len(walk))
                nroot+=1
                status,good=find_centres(B,g,r,walk,maxQ=maxQ,maxnodes=150000)
                kinds.append('%s@%s%s'%(kind,''.join(map(str,g)),'*' if good else ''))
                if good:
                    ncert+=len(good)
                    sm=min(good,key=lambda x:len(x[0]))
                    if best is None or len(sm[0])<len(best[0]): best=sm
    print('base %2d: rooted bands %2d, verified certs %3d  %s  [%s] %.1fs'%(B,nroot,ncert,('smallest cert length %d digits (N(1))'%len(best[0])) if best else '', ' '.join(kinds)[:150], time.time()-t0)); sys.stdout.flush()
