from pipeline import *
import sys
B=int(sys.argv[1]); maxQ=int(sys.argv[2]); Ps=list(map(int,sys.argv[3:]))
for P in Ps:
    for g in necklaces_all(P):
        r=rooted(B,g)
        if r is None: continue
        for c,walk in cycles_of(r):
            H=r['order'][walk[0]]
            if min_period(list(zip(*H)))!=P: continue
            ps=psums(H)
            kind='wire' if all(s==B-1 for s in ps) else ('uniform' if len(walk)==1 else 'lattice m=%d (comp %d)'%(len(walk),c['size']))
            t0=time.time()
            status,good=find_centres(B,g,r,walk,maxQ=maxQ,maxnodes=300000)
            line='  P=%d clock=%s S=%d %-22s centre search: %s (%.1fs)'%(P,''.join(map(str,g)),sum(g),kind,status,time.time()-t0)
            if good:
                smallest=min(good,key=lambda x:len(x[0]))
                line+='  VERIFIED certs=%d  e.g. N(1)=%s (base %d), period %d, len %d'%(len(good),digits_to_str(smallest[0]),B,smallest[1],len(smallest[0]))
            print(line[:300]); sys.stdout.flush()
