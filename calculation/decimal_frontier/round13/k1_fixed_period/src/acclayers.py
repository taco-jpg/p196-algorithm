#!/usr/bin/env python3
import os
"""r13b acclayers.py: accepting states of an E_acc file per layer (phase), and defect front/top statistics.
usage: acclayers.py lat.tbl orbit K file"""
import sys, struct, numpy as np
exec(open(os.path.expanduser('~/p196_run/r13b/src/ean.py')).read().split("f=open(fn,'rb')")[0])
f=open(fn,'rb'); Lo,W=struct.unpack('ii',f.read(8)); assert Lo==len(Ph)
acc=[]; tot=[]; fronts=np.zeros(K+1,dtype=np.int64)
for l in range(Lo):
    n=struct.unpack('Q',f.read(8))[0]
    a=np.fromfile(f,dtype=np.uint64,count=W*n).reshape(-1,W)
    t,j,pr=Ph[l]
    Ltab=np.array([Lt[t][(j+i)%M] for i in range(K)],dtype=np.int64)
    cells=np.zeros((n,K),dtype=np.int64)
    for i in range(K): cells[:,i]=(a[:,i//12]>>np.uint64(5*(i%12)))&np.uint64(31)
    off=(cells!=Ltab); anyoff=off.any(axis=1)
    fp=np.where(anyoff,off.argmax(axis=1),K)
    acc.append(int((fp==0).sum())); tot.append(n)
    if n: fronts+=np.bincount(fp,minlength=K+1)
print(f'K={K} total={sum(tot)} accepting={sum(acc)}')
print('accepting per layer (layer:count, nonzero):',[(l,acc[l]) for l in range(Lo) if acc[l]][:40])
print('layers with any state:',sum(1 for x in tot if x),'of',Lo,' front histogram f=0..:',list(fronts[:12]))
