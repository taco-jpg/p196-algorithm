from tools import *
import time
B=10
for name,g in (('p11',(1,1,1,0,0,0,1,0,0,0,0)),('p12',(1,0,0,0)*3)):
    P=len(g)
    F0=Frame(B,(0,)*P,g)
    R=root_node(B,g)
    t0=time.time()
    starts=expand(F0,R)
    order,edges,ok=closure(F0,starts,maxnodes=400000)
    live,comps,cyc=live_nodes(len(order),edges)
    print(name,'roots',len(starts),'nodes',len(order),'complete',ok,'live',sum(live),'time %.1f'%(time.time()-t0))
    cs=[(len(cm),k) for k,cm in enumerate(comps) if cyc[k]]
    print('  cyclic comps sizes:',sorted([c[0] for c in cs],reverse=True))
    roots=list(range(len(starts)))
    for sz,k in cs:
        v=comps[k][0]
        path=find_path(edges,roots,v)
        H=order[v]
        print('  comp size',sz,'depth of first node',len(path)-1,'psums',psums(H),'c',H[2],'d',H[3])
