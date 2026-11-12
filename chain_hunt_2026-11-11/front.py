from lat10 import *
import random, time, sys
from collections import Counter
order,edges,live,comps,cyc,comp_of=load()
roots=[i for i,H in enumerate(order) if all(x==0 for x in H[2])]
def setup(k):
    walk=cycle_walk(edges,comp_of,comps[k][0])
    path=find_path(edges,roots,walk[0])
    left=path[:-1]
    return left,walk
def number_at(left,walk,n,cut,t0,mid=None):
    """columns at time t0: left end, n lattice periods, then 'cut' more lattice columns; mirrored. mid: middle digit or None."""
    cols=[(order[i][0][t0],order[i][1][t0]) for i in left]
    lat=[(order[v][0][t0],order[v][1][t0]) for v in walk]
    cols+=lat*n+lat[:cut]
    low=[c[0] for c in cols]; high=[c[1] for c in cols][::-1]
    return low+([mid] if mid is not None else [])+high, len(cols)
def front_run(left,walk,n,cut,t0,mid,steps):
    digs,ncols=number_at(left,walk,n,cut,t0,mid)
    K0=len(left); m=len(walk)
    res=[]
    for t in range(steps+1):
        L=len(digs)
        tt=(t0+t)%8
        # first column (outer->inner) where (a,b) differs from prediction
        bad=None
        half=L//2
        for i in range(half):
            if i<K0: H=order[left[i]]
            else: H=order[walk[(i-K0)%m]]
            if digs[i]!=H[0][tt] or digs[L-1-i]!=H[1][tt]:
                bad=i; break
        res.append((bad if bad is not None else half, half))
        if is_pal(digs): return res,'PAL at %d'%t
        digs=ra_step(digs,10)
    return res,'ok'
if __name__=='__main__':
    random.seed(1)
    small=[k for k in range(len(comps)) if cyc[k] and len(comps[k])==20]
    for k in small:
        left,walk=setup(k)
        print('20-cycle comp',k,'left end width',len(left))
        n=14; steps=260
        stats=[]
        t1=time.time()
        for cut in range(20):
            for t0 in range(8):
                for mid in (None,random.randrange(10),random.randrange(10)):
                    res,msg=front_run(left,walk,n,cut,t0,mid,steps)
                    # defect width in columns from the fold: half - front
                    f0=res[0][0]; 
                    # time when front reaches the left end (K0) or end of run
                    K0=len(left)
                    tend=next((t for t,(f,h) in enumerate(res) if f<=K0+2),steps)
                    fend=res[tend][0]
                    speed=(f0-fend)/max(tend,1)
                    stats.append((speed,cut,t0,mid,f0,fend,tend,msg))
        stats.sort(key=lambda s:s[0])
        sp=[s[0] for s in stats]
        print('  runs',len(stats),'front speed outward (cols/step): min %.3f median %.3f max %.3f'%(sp[0],sp[len(sp)//2],sp[-1]),'time %.0fs'%(time.time()-t1))
        print('  slowest 5:',[(round(s[0],3),s[1],s[2],s[3],s[4],s[5],s[6]) for s in stats[:5]])
        print('  exterior+lattice intact at t=0 in all runs:',all(s[4]>=len(left)+20*n-1 for s in stats))
        sys.stdout.flush()
