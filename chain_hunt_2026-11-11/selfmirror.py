# a-static self-mirror walks: every column periodic from birth (no centre). Works for any clock.
from pipeline import *
import sys
def birth_ok(H,g,tb):
    """column born at time tb (step tb-1 overflowed): odd phase until next overflow, even phase until the one after."""
    P=len(g); a,b,c,d=H
    assert g[(tb-1)%P]==1
    t=tb; stage=0
    while True:
        tt=t%P; s=a[tt]+b[tt]
        if stage==0:
            if a[tt]!=b[tt] or not (d[tt]==2 or d[tt]==c[tt]): return None
        else:
            cp=1 if s+c[tt]>=10 else 0
            if not (d[tt]==2 or d[tt]==cp): return None
        if g[tt]==1:
            stage+=1
            if stage==2: return (t+1)%P     # birth time of the next column
        t+=1
def analyse(g,maxnodes=3000000):
    r=rooted(10,g,maxnodes)
    if r is None: print('no live structure'); return
    P=len(g); n=r['nodes']; order=r['order']; el=r['el']
    print('clock',''.join(map(str,g)),'nodes',n,'live',r['live'])
    births=[t for t in range(P) if g[(t-1)%P]==1]
    ok={}   # (node,tb) -> next tb
    for i in range(n):
        for tb in births:
            nx=birth_ok(order[i],g,tb)
            if nx is not None: ok[(i,tb)]=nx
    print('birth-compatible (node,phase) pairs:',len(ok),' distinct nodes:',len(set(i for i,_ in ok)))
    # product graph: (i,tb) -> (j,nx) if j in el[i] and (j,nx) in ok
    adj={}
    for (i,tb),nx in ok.items():
        adj[(i,tb)]=[(j,nx) for j in el[i] if (j,nx) in ok]
    # prune nodes without successors repeatedly
    alive=set(adj)
    changed=True
    while changed:
        changed=False
        for v in list(alive):
            if not any(w in alive for w in adj[v]):
                alive.discard(v); changed=True
    print('pairs on an infinite self-mirror walk:',len(alive))
    return r,ok,alive
if __name__=='__main__':
    g=tuple(int(x) for x in sys.argv[1])
    analyse(g, int(sys.argv[2]) if len(sys.argv)>2 else 3000000)
