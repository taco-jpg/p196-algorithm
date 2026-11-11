#!/usr/bin/env python3
"""r13b ean.py: analyse an E_K file of eset2 (K, WORDS=3): histogram of (front f, top g) of the off-lattice cells, per K.
usage: ean.py lat.tbl orbit K file"""
import sys, struct, numpy as np
tblf, oi, K, fn = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
toks = open(tblf).read().split(); P, M = int(toks[0]), int(toks[1]); p=2
if len(open(tblf).readline().split())>=3: B=int(toks[2]); p=3
else: B=10
G=[int(x) for x in toks[p:p+P]]; p+=P
Lt=[];UP=[];DN=[]
for t in range(P):
    Lt.append([int(x) for x in toks[p:p+M]]); p+=M
    UP.append([int(x) for x in toks[p:p+M]]); p+=M
    DN.append([int(x) for x in toks[p:p+M]]); p+=M
def phases(which):
    NPH=2*P*M; orb=[-1]*NPH; reps=[]; n=0
    def dec(s): return (s//2)//M, (s//2)%M, s%2
    def enc(t,j,pr): return (t*M+j)*2+pr
    for s in range(NPH):
        if orb[s]>=0: continue
        reps.append(s); x=s
        while True:
            orb[x]=n; t,j,pr=dec(x); g=G[t]; dh=(g==1 and pr==0); x=enc((t+1)%P,(j+dh)%M,(pr+g)%2)
            if x==s: break
        n+=1
    s=reps[which]; x=s; res=[]
    while True:
        t,j,pr=dec(x); res.append((t,j,pr)); g=G[t]; dh=(g==1 and pr==0); x=enc((t+1)%P,(j+dh)%M,(pr+g)%2)
        if x==s: break
    return res
Ph=phases(oi)
f=open(fn,'rb'); Lo,W=struct.unpack('ii',f.read(8)); assert Lo==len(Ph)
from collections import Counter
H=Counter(); total=0; lat=0
WIDTHS=Counter(); WID_ACC=Counter()
for l in range(Lo):
    n=struct.unpack('Q',f.read(8))[0]
    a=np.fromfile(f,dtype=np.uint64,count=W*n).reshape(-1,W)
    t,j,pr=Ph[l]
    Ltab=np.array([Lt[t][(j+i)%M] for i in range(K)],dtype=np.int64)
    cells=np.zeros((n,K),dtype=np.int64)
    for i in range(K):
        cells[:,i]=(a[:,i//12]>>np.uint64(5*(i%12)))&np.uint64(31)
    off=(cells!=Ltab)
    anyoff=off.any(axis=1)
    fp=np.where(anyoff,off.argmax(axis=1),K)
    gp=np.where(anyoff,K-1-off[:,::-1].argmax(axis=1),-1)
    # histogram of (front f, g)
    for ff,gg,cnt in zip(*np.unique(np.stack([fp,gp]),axis=1,return_counts=True)) if False else []:
        pass
    pairs,cnts=np.unique(fp*(K+1)+(gp+1),return_counts=True)
    for pv,c in zip(pairs,cnts):
        ff=int(pv)//(K+1); gg=int(pv)%(K+1)-1
        H[(ff,gg)]+=int(c)
    total+=n
print('K=%d total=%d'%(K,total))
print('histogram: row f = lowest off-lattice cell (K = all lattice), col g = highest off-lattice cell')
K2=K
print('f\\g'+''.join('%9d'%g for g in range(K2)))
for ff in range(K2+1):
    row=''.join('%9s'%(H[(ff,g)] if (ff,g) in H else '.') for g in range(K2))
    if ff==K2: row+='   all-lattice: %d'%H[(K2,-1)]
    print('%3d'%ff+row)
# width marginals
wd=Counter(); fm=Counter()
for (ff,gg),c in H.items():
    if ff<K2: wd[gg-ff+1]+=c; fm[ff]+=c
print('defect width g-f+1 histogram (states):', sorted(wd.items()))
print('front f histogram:', sorted(fm.items()))
