import sys, itertools, collections
from bsys import *
b=int(sys.argv[1]); nmax=int(sys.argv[2]); T=int(sys.argv[3]) if len(sys.argv)>3 else 300
res=collections.Counter(); ex={}
for n in range(1,nmax+1):
    for B in itertools.product(range(2*b-1),repeat=n):
        if B[0]==0: continue
        cur=list(B); seen=set(); out=None
        for t in range(T):
            key=tuple(cur)
            if key in seen: out='cycle'; break
            seen.add(key)
            nb,u,e1,gam=bstep(b,cur)
            if not nb or nb[0]==0: out='dead'; break
            cur=nb
            if len(cur)>nmax+6: out='grow'; break
        if out is None: out='long'
        res[out]+=1; ex.setdefault(out,B)
print(b,nmax,dict(res),ex)
