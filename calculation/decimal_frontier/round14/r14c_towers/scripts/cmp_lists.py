#!/usr/bin/env python3
# compare two tower lists (iface= tokens) by rotation class (rotation by multiples of P, xb mod 10)
import sys
def classes(fname, P):
    res=[]
    for line in open(fname):
        if 'iface=' not in line: continue
        spec=line.split('iface=')[1].split()[0]
        cs,xs,As=spec.split('|'); xb=[int(x)%10 for x in xs.rstrip(',').split(',')]; L=len(cs)
        sym=[(cs[t], xb[t], As[t]) for t in range(L)]
        res.append(min(tuple(sym[(t+r*P)%L] for t in range(L)) for r in range(L//P)))
    return res
a=classes(sys.argv[1],int(sys.argv[3])); b=classes(sys.argv[2],int(sys.argv[3]))
sa,sb=set(a),set(b)
print(f'A={len(a)} (classes {len(sa)}), B={len(b)} (classes {len(sb)}), intersection={len(sa&sb)}, A-B={len(sa-sb)}, B-A={len(sb-sa)}')
