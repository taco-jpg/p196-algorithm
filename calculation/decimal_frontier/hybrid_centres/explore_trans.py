import sys
from htrans import transfer
from runsat import stream
b=10
cyc=stream('p11'); p=11
gam=[cyc[t][1] for t in range(p)]; e1=[cyc[t][2] for t in range(p)]
A=0; T=11; N=9
start=(tuple(e1),tuple(1-x for x in e1),tuple(N*e1[t] if gam[t] else 0 for t in range(T)),())
print('gam',gam); print('e1 ',e1)
from collections import deque
seen={start:0}; layers={0:[start]}
cur=[start]; L=0
succs={}
while cur:
    nxt=[]
    for s in cur:
        ss=transfer(b,gam,e1,A,s,L)
        succs[s]=ss
        for (ns,v0) in ss:
            if ns not in seen:
                seen[ns]=L+1; nxt.append(ns)
    L+=1; cur=nxt
    print('layer',L,'new states',len(nxt))
print('total',len(seen))
for s,ss in succs.items():
    print('state', 'Aup',''.join(map(str,s[0])),'G',''.join(map(str,s[1])),'dd',s[2], 'n_succ',len(ss), [ (v0, 'same' if ns==s else seen[ns]) for ns,v0 in ss][:8])
