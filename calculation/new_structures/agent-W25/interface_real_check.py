#!/usr/bin/env python3
"""W25 independent real decimal digit-list reverse/add vs conditional interface.
Run: python3 calculation/new_structures/agent-W25/interface_real_check.py
"""
from heteroclinic import W,U,one_step
from band_first import advance
B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
def check(k=200,r=1000,steps=704,L=-700,R=1000):
    half=B+list(W)*k+list(U)*r
    d=[0]*(2*len(half))
    for i,x in enumerate(half):d[i]=min(x,9);d[-1-i]=x-min(x,9)
    cut=len(B)+k*20
    w=W;u=U
    p=[w[j%20] if j<0 else u[j%4] for j in range(L,R+1)]
    for t in range(steps+1):
        for j in range(L,R+1):
            x=cut+j
            actual=d[x]+d[-1-x]
            assert actual==p[j-L],(t,j,actual,p[j-L])
        if t==steps:break
        g=1 if t%2==0 else 0
        p=one_step(p,w,u,L,g)
        w=next(advance(w,10,g));u=next(advance(u,10,g))
        carry=0;new=[]
        for i in range(len(d)):
            z=d[i]+d[-1-i]+carry
            new.append(z%10);carry=z//10
        if carry:new.append(carry)
        assert carry==g
        d=new
    print("PASS",steps+1,"real decimal states,",(R-L+1)*(steps+1),
          "exact coefficient equalities; final digits",len(d))
    assert len(d)==16430
if __name__=='__main__':check()
