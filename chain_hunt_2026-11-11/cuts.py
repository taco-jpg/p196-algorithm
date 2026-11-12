# Cut every live rooted chain at every node, phase and parity (plus a free middle digit) and measure how long the
# periodic exterior survives when the real fold is put there.  Clock given on the command line.
from pipeline import *
from chain import live_nodes
import sys
g=tuple(int(x) for x in sys.argv[1]); maxsteps=int(sys.argv[2]) if len(sys.argv)>2 else 400
B=10; P=len(g)
r=rooted(B,g,3000000)
n=r['nodes']; order=r['order']; el=r['el']
edges=el
live,comps,cyc=live_nodes(n,edges)
L=[v for v in range(n) if live[v]]
print('clock',sys.argv[1],'nodes',n,'live',len(L))
# BFS tree from roots
from collections import deque
prev={s:None for s in range(r['nroots'])}; dq=deque(range(r['nroots']))
while dq:
    v=dq.popleft()
    for w in el[v]:
        if w not in prev: prev[w]=v; dq.append(w)
def path(v):
    p=[]
    while v is not None: p.append(v); v=prev[v]
    return p[::-1]
best=[]
hist={}
for v in L:
    pth=path(v); K=len(pth)
    Hs=[order[i] for i in pth]
    for t0 in range(P):
        cols=[(H[0][t0],H[1][t0]) for H in Hs]
        low=[c[0] for c in cols]; high=[c[1] for c in cols][::-1]
        for mid in [None]+list(range(10)):
            d=low+([mid] if mid is not None else [])+high
            t=0
            while t<maxsteps:
                Ld=len(d); tt=(t0+t)%P
                ok=True
                for i in range(K):
                    if d[i]!=Hs[i][0][tt] or d[Ld-1-i]!=Hs[i][1][tt]: ok=False; break
                if not ok: break
                d=ra_step(d,B); t+=1
            hist[t]=hist.get(t,0)+1
            if t>=12: best.append((t,v,K,t0,mid))
best.sort(key=lambda z:-z[0])
print('survival histogram (steps: count):',sorted(hist.items()))
for b in best[:25]: print('  survived %d steps: node %d depth %d phase %d mid %s'%b)
