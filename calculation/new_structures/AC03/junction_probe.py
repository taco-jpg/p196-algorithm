#!/usr/bin/env python3
"""Independent genuine big-integer controls across arbitrary junction contents."""
import random
from oracle import B,W,U,centre,realize
def check(u,length,cid,junction):
    c=centre(cid,length)
    def template(k):
        h=B+W*14+junction+U[u]*k
        return h+c+h[::-1]
    n=realize(template(100));gam=[]
    for t in range(120):
        s=str(n);nn=n+int(s[::-1])
        gam.append(len(str(nn))-len(s));n=nn
    assert gam==[1,0,0,0]*30
    d=list(map(int,str(n)[::-1]))
    got=[a+b for a,b in zip(d,d[::-1])]
    tar=template(105)
    assert len(got)==len(tar)
    cut=len(B)+14*len(W)+len(junction)+119+120
    first=next((i-cut for i in range(cut,len(got)-cut) if got[i]!=tar[i]),None)
    assert first is not None
    return first
if __name__=="__main__":
    rng=random.Random(20261029);n=0
    for length in (7,8,9,10):
        cap=19**(length//2)*(10 if length%2 else 1)
        for u in range(3):
            for cid in (0,cap-1,rng.randrange(cap)):
                base=check(u,length,cid,[5]);n+=1
                for jlen in (0,1,2,17,24,40,50):
                    for kind in range(3):
                        j=[0]*jlen if kind==0 else [18]*jlen if kind==1 else [rng.randrange(19) for _ in range(jlen)]
                        assert check(u,length,cid,j)==base,(u,length,cid,jlen,kind)
                        n+=1
            print("BIGINT_J_CONTROLS",u,length,n,flush=True)
    print("BIGINT_J_PASS",n)
