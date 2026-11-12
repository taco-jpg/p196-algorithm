from pipeline import *
from chain import live_nodes, sccs
import numpy as np
g=(0,1,0,1,0,1,0,1)
r=rooted(10,g,3000000)
n=r['nodes']; el=r['el']; order=r['order']
live,comps,cyc=live_nodes(n,el)
big=max((c for k,c in enumerate(comps) if cyc[k]),key=len)
S=set(big); print('SCC size',len(big))
deg={}
for v in big:
    d=sum(1 for w in el[v] if w in S); deg[d]=deg.get(d,0)+1
print('out-degree inside SCC:',deg)
idx={v:i for i,v in enumerate(big)}
M=np.zeros((len(big),len(big)))
for v in big:
    for w in el[v]:
        if w in S: M[idx[v],idx[w]]+=1
ev=np.linalg.eigvals(M); lam=max(abs(ev)); print('spectral radius',lam)
# number of closed walks of even length m (trace of M^m)
P=np.eye(len(big)); 
for m in range(1,201):
    P=P@M
    if m in (20,40,48,60,61,64,80,96,100,120,160,200): print('closed walks of length',m,':',int(round(np.trace(P))))
# branch nodes
br=[v for v in big if sum(1 for w in el[v] if w in S)>1]
print('branch nodes:',len(br))
# depth of SCC nodes
