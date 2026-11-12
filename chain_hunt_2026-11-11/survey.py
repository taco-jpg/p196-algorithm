from cx import *
import sys, time, itertools
def necklaces(d):
    seen=set(); out=[]
    for bits in itertools.product((0,1),repeat=d):
        if sum(bits)==0: continue
        rots=[bits[i:]+bits[:i] for i in range(d)]
        mn=min(rots)
        if mn in seen: continue
        seen.add(mn)
        # primitive only
        prim=all(rots[0]!=rots[i] for i in range(1,d))
        if prim: out.append(mn)
    return out
def survey(B, maxd, maxnodes=300000):
    res=[]
    for d in range(1,maxd+1):
        for g in necklaces(d):
            # no 1-run constraint: overflow top digit is 1, quick filter not needed
            F0=Frame(B,(0,)*d,g)
            starts=expand(F0,root_node(B,g))
            if not starts: continue
            r=run_closure(F0,starts,maxnodes=maxnodes,dump=True)
            if r['live']==0: continue
            raw=r['raw']; comp=r['comp']
            for c in r['cyc']:
                H=node_from_raw(raw,c['rep'])
                ps=psums(H)
                kind='wire' if all(s==B-1 for s in ps) else ('uniform' if c['size']==1 else 'lattice')
                res.append((d,''.join(map(str,g)),sum(g),c['size'],kind,r['nodes'],r['complete']))
    return res
if __name__=='__main__':
    maxd=int(sys.argv[1])
    for B in map(int,sys.argv[2:]):
        t0=time.time()
        res=survey(B,maxd)
        print('base',B,'periods<=',maxd,'time %.1f'%(time.time()-t0))
        for x in res: print('   d=%d clock=%s S=%d  cyc_size=%d %s  (nodes %d complete %s)'%x)
        sys.stdout.flush()
