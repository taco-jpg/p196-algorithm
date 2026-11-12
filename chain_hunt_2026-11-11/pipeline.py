from cx import *
import sys, time, itertools
from math import gcd

def necklaces_all(P):
    seen=set(); out=[]
    for bits in itertools.product((0,1),repeat=P):
        if sum(bits)==0: continue
        mn=min(bits[i:]+bits[:i] for i in range(P))
        if mn in seen: continue
        seen.add(mn); out.append(mn)
    return out

def min_period(seq):
    n=len(seq)
    for p in range(1,n+1):
        if n%p==0 and all(seq[i]==seq[i%p] for i in range(n)): return p

def rooted(B,g,maxnodes=400000):
    P=len(g)
    F0=Frame(B,(0,)*P,g)
    starts=expand(F0,root_node(B,g))
    if not starts: return None
    r=run_closure(F0,starts,maxnodes=maxnodes,dump=True)
    if r.get('live',0)==0: return None
    n=r['nodes']
    r['order']=[node_from_raw(r['raw'],i) for i in range(n)]
    r['el']=edge_lists(n,r['edges'])
    r['nroots']=len(starts)
    return r

def cycles_of(r):
    """yield (list of node ids forming one simple cycle) for each cyclic component (only if the component is a single cycle or self loop; else the shortest cycle through rep)."""
    from collections import deque
    comp=r['comp']; el=r['el']
    for c in r['cyc']:
        v=c['rep']; k=comp[v]
        # shortest cycle through v inside its component
        prev={v:None}; dq=deque([v]); found=None
        while dq and found is None:
            u=dq.popleft()
            for w in el[u]:
                if comp[w]!=k: continue
                if w==v: found=u; break
                if w not in prev: prev[w]=u; dq.append(w)
        walk=[]; u=found
        while u is not None: walk.append(u); u=prev[u]
        yield c, walk[::-1]

def fold_setup(B,g,m):
    """smallest multiple P of len(g) with even overflow count and Q=S/2 divisible by m."""
    d=len(g); S=sum(g)
    k=1
    while True:
        SP=S*k
        if SP%2==0 and (SP//2)%m==0: break
        k+=1
    G=tuple(g)*k
    ov=[t for t in range(len(G)) if G[t]==1]
    adv=set(ov[1::2])
    F,phi=make_frame(B,G,adv)
    return G,F,phi,SP//2

def find_centres(B,g,r,walk,maxnodes=400000,maxQ=3,verbose=False):
    order=r['order']; el=r['el']
    m=len(walk)
    G,F,phi,Q=fold_setup(B,g,m)
    if Q>maxQ: return 'skipQ%d'%Q, []
    P=F.P
    cyc_nodes=[order[v] for v in walk]
    cells=lattice_cells(B,cyc_nodes)
    starts=[sheared_node(B,F,phi,cells,j) for j in range(m)]
    pars=[]
    for cas,name in ((1,'i'),(2,'ii')):
        par=parity_seq(G,F.alpha,name)
        if par is not None: pars.append((cas,par))
    rr=run_closure(F,starts,pars=pars,maxnodes=maxnodes,dump=True,timeout=120)
    if rr.get('timeout'): return 'timeout',[]
    status='closed' if rr['complete'] else 'capped'
    if not rr['cands']: return status+' nodes=%d'%rr['nodes'], []
    raw=rr['raw']
    left=find_path(el,list(range(r['nroots'])),walk[0])[:-1]
    left_cols=[(order[i][0][0],order[i][1][0]) for i in left]
    band_cols=[(H[0][0],H[1][0]) for H in cyc_nodes]
    good=[]
    pard=dict(pars)
    for c in rr['cands']:
        path=c['path']; j0=path[0]   # start index = lattice phase j0 (starts are inserted in order, dedup may shift)
        Hs=[node_from_raw(raw,v) for v in path]
        # identify lattice phase of the start node
        try: ph=starts.index(Hs[0])
        except ValueError: continue
        H=Hs[-1]; Hn=node_from_raw(raw,c['w'])
        par=pard[c['case']]
        pre=band_cols[:ph+1]
        chain=[(X[0][0],X[1][0]) for X in Hs[1:]]
        if c['case']==1:
            if par[0]==0: cc=pre+chain; mid=None
            else: cc=pre+chain; mid=Hn[0][0]
        else:
            if par[0]==1:
                full=pre+chain
                cc=full[:-1]; mid=H[0][0]
            else: cc=pre+chain; mid=None
        mk=lambda n,cc=cc,mid=mid: build_number(left_cols,band_cols,n,cc,mid)
        ok,msg=check_template(B,mk,3,Q//m,P,periods=5,ns=3)
        if ok: good.append((mk(1),P,Q//m,m))
    return status+' nodes=%d cands=%d'%(rr['nodes'],len(rr['cands'])), good

if __name__=='__main__':
    maxP=int(sys.argv[1])
    for B in map(int,sys.argv[2:]):
        t0=time.time(); tot=0
        print('=== base',B)
        for P in range(1,maxP+1):
            for g in necklaces_all(P):
                r=rooted(B,g)
                if r is None: continue
                for c,walk in cycles_of(r):
                    H=r['order'][walk[0]]
                    if min_period(list(zip(*H)))!=P: continue   # count each structure at its true time period
                    ps=psums(H)
                    kind='wire' if all(s==B-1 for s in ps) else ('uniform' if len(walk)==1 else 'lattice m=%d (comp %d)'%(len(walk),c['size']))
                    status,good=find_centres(B,g,r,walk)
                    tot+=len(good)
                    line='  P=%d clock=%s S=%d %-22s centre search: %s'%(P,''.join(map(str,g)),sum(g),kind,status)
                    if good:
                        smallest=min(good,key=lambda x:len(x[0]))
                        line+='  VERIFIED certs=%d  e.g. N(1)=%s (base %d), period %d'%(len(good),digits_to_str(smallest[0]),B,smallest[1])
                    print(line); sys.stdout.flush()
        print('  base',B,'verified certificates:',tot,'time %.1f'%(time.time()-t0)); sys.stdout.flush()
