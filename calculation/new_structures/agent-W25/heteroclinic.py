#!/usr/bin/env python3
"""Agent W25: exact conditional W20|U4 two-sided carry-interface dynamics.
The infinite periodic boundary conditions are NOT a rooted decimal certificate.
Run: python3 calculation/new_structures/agent-W25/heteroclinic.py
"""
from band_first import advance,carries
W=(17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13)
U=(9,18,9,0)
def one_step(p,w,u,L,g):
    R=L+len(p)-1
    cw,_=next(carries(w,10))
    _,hu=next(carries(u,10))
    c=cw[L%20];lo=[]
    for x in p:
        lo.append((x+c)%10);c=(x+c)//10
    h=hu[(R+1)%4];hi=[0]*len(p)
    for i in range(len(p)-1,-1,-1):
        x=p[i];hi[i]=(x+h)%10;h=(x+h)//10
    hi_before_left=(w[(L-1)%20]+h)%10
    return [lo[i]+(hi[i] if g==0 else (hi[i-1] if i else hi_before_left))
            for i in range(len(p))]
def run(rot=0,cycles=24,L=-1000,R=2100):
    w=W;u=U[rot:]+U[:rot]
    p=[w[j%20] if j<0 else u[j%4] for j in range(L,R+1)]
    trace=[]
    for t in range(88*cycles+1):
        if t%88==0:
            bad=[j for j in range(L,R+1)
                 if p[j-L]!=(w[j%20] if j<0 else u[j%4])]
            lo=min(bad) if bad else None
            hi=max(bad) if bad else None
            trace.append((t,lo,hi,len(bad)))
            n=t//88
            if n:
                assert lo==-20*n+(2 if rot%2 else 0)
                assert hi==66*n+(-1 if rot%2 else -4)
        if t==88*cycles:break
        g=1 if t%2==0 else 0
        p=one_step(p,w,u,L,g)
        w=next(advance(w,10,g));u=next(advance(u,10,g))
        if t%500==0:
            assert all(p[j-L]==w[j%20] for j in range(L,L+20))
            assert all(p[j-L]==u[j%4] for j in range(R-20,R+1))
    return trace
if __name__=='__main__':
    for rot in range(4):
        data=run(rot)
        print("PASS rotation",rot,"checkpoints",len(data)-1,
              "final (step,left,right,count)",data[-1])
