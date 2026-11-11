#!/usr/bin/env python3
import os
"""r13b patcmp.py: compare the windows of E_acc(44,80) (K=44 deepest walks) with lattice rows (rec0 at all (t',j'), also reversed rows, rec1).
usage: patcmp.py ORBIT K FILE"""
import sys, struct, collections
exec(open(os.path.expanduser('~/p196_run/r13b/src/ean.py')).read().split("f=open(fn,'rb')")[0].replace("tblf, oi, K, fn = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]","tblf='tbl/lat_rec0.tbl'; oi=int(sys.argv[1]); K=int(sys.argv[2]); fn=sys.argv[3]"))
f=open(fn,'rb'); Lo,W=struct.unpack('ii',f.read(8)); assert Lo==len(Ph)
states=[]
for l in range(Lo):
    n=struct.unpack('Q',f.read(8))[0]; data=f.read(8*W*n)
    for i in range(n):
        words=struct.unpack_from('<%dQ'%W,data,8*W*i); w=[(words[q//12]>>(5*(q%12)))&31 for q in range(K)]
        states.append((l,tuple(w)))
print('states',len(states))
# per layer distinct windows
perlayer=collections.Counter(l for l,w in states); print('states per layer (first 12):',[perlayer[l] for l in range(12)])
distinct=collections.Counter(w for l,w in states); print('distinct windows overall:',len(distinct))
# compare a sample window (lowest layer with accepting state) with lattice rows
def best_match(w):
    best=(0,None)
    for tp in range(P):
        for jp in range(M):
            m=sum(1 for y in range(len(w)) if w[y]==Lt[tp][(jp+y)%M])
            if m>best[0]: best=(m,('direct',tp,jp))
            m2=sum(1 for y in range(len(w)) if w[y]==Lt[tp][(jp-y)%M])
            if m2>best[0]: best=(m2,('reversed',tp,jp))
    return best
sample=[s for s in states if s[0] in (77,78)][:6]+states[:6]
for l,w in sample:
    t,j,par=Ph[l]; lat=[Lt[t][(j+y)%M] for y in range(K)]
    off=sum(1 for y in range(K) if w[y]!=lat[y])
    print('layer',l,(t,j,par),'off-lattice cells',off,'best match against lattice rows: ',best_match(w))
    print('  w:',' '.join('%2d'%x for x in w))
    print('  L:',' '.join('%2d'%x for x in lat))
