#!/usr/bin/env python3
"""Check the 'two carry sweeps' formulation of the autonomous B-step against the exact mirror:
   F_i = (B_i + c_{i-1}) mod b  (forward carries, c_{-1}=0, e1 = c_{n-1}),
   R_i = (B_i + d_{i+1}) mod b  (backward carries, d_n = 1-e1, d_i = floor((B_i + d_{i+1})/b), gam = d_0),
   gam=0: B'_i = F_i + R_i ;  gam=1: B'_0 = F_0 + 1, B'_i = F_i + R_{i-1} (1<=i<n), B'_n = xd + R_{n-1}, xd=(b-1)*(1-e1)."""
import sys, random
sys.path.insert(0,'/home/claude/research/w2_theory')
import mirror as m, lib
random.seed(5)
cnt=0
for b in (2,3,5,10,11,17):
    for trial in range(20000):
        n=random.randint(1,9)
        B=[random.randint(0,2*b-2) for _ in range(n)]
        if B[0]==0: B[0]=1
        c=0; F=[]; carries=[]
        for i in range(n):
            v=B[i]+c; F.append(v%b); c=v//b; carries.append(c)
        e1=c; d=1-e1; R=[0]*n
        for i in range(n-1,-1,-1):
            v=B[i]+d; R[i]=v%b; d=v//b
        gam=d
        if gam==0: nb=[F[i]+R[i] for i in range(n)]
        else:
            nb=[F[0]+1]+[F[i]+R[i-1] for i in range(1,n)]+[(b-1)*(1-e1)+R[n-1]]
        # mirror: nextB with a C chosen s.t. e2=1-e1 is implicit in lib.Bstep (untrimmed version)
        e1m=m.e1(b,B); assert e1m==e1
        DB=m.DB(b,B); DR,gm=m.norm(b,B[::-1],1-e1)
        assert gm==gam
        ref=m._zw(DB,DR[::-1]) if gm==0 else m._zw(DB+[(b-1)*(1-e1)],[1]+DR[::-1])
        assert ref==nb,(b,B,ref,nb)
        cnt+=1
print("F/R formulation agrees with mirror nextB on",cnt,"random words")
