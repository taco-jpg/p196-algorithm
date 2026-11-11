#!/usr/bin/env python3
# lines of file A (with iface=) whose rotation class (mod P, xb mod 10) is not present in file B
import sys
def cls(spec,P):
    cs,xs,As=spec.split('|'); xb=[int(x)%10 for x in xs.rstrip(',').split(',')]; L=len(cs)
    sym=[(cs[t], xb[t], As[t]) for t in range(L)]
    return min(tuple(sym[(t+r*P)%L] for t in range(L)) for r in range(L//P))
P=int(sys.argv[3])
B=set()
for l in open(sys.argv[2]):
    if 'iface=' in l: B.add(cls(l.split('iface=')[1].split()[0],P))
for l in open(sys.argv[1]):
    if 'iface=' in l and cls(l.split('iface=')[1].split()[0],P) not in B: sys.stdout.write(l)
