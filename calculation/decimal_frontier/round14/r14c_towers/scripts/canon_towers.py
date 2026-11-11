#!/usr/bin/env python3
# group a TSURV list by canonical rotation (multiples of clock period P), xb mod 10
import sys
P=int(sys.argv[2]); seen={}
for line in open(sys.argv[1]):
    if 'iface=' not in line: continue
    spec=line.split('iface=')[1].split()[0]
    cs,xs,As=spec.split('|'); xb=[int(x)%10 for x in xs.rstrip(',').split(',')]; L=len(cs)
    sym=[(cs[t], xb[t], As[t]) for t in range(L)]
    best=min(tuple(sym[(t+r*P)%L] for t in range(L)) for r in range(L//P))
    key=best
    ifid=line.split('if=')[1].split()[0] if 'if=' in line else '?'
    seen.setdefault(key,[]).append(ifid)
for k,v in seen.items(): print(len(v), v)
print('distinct classes:',len(seen))
