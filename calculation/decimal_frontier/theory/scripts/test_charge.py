#!/usr/bin/env python3
"""Mod-(b+1) charge lemma test.  W(B)=val(rev B)+1 = sum_i B_i b^(n-1-i) + 1 ; claim: for the autonomous B-step (untrimmed, with e2:=1-e1)
   gam=1  =>  W(B') = 0 mod (b+1);   gam=0  =>  W(B') = +-2 W(B) mod (b+1)  (sign = (-1)^(n-1)... to be determined) ;  trimmed (b-1)'s at the top: B'=B'' ++ (b-1)^u changes W by ... test untrimmed AND trimmed."""
import sys, random
sys.path.insert(0,'/home/claude/research/w2_theory')
import mirror as m, lib
random.seed(7)
def W(b,B): return sum(v*b**(len(B)-1-i) for i,v in enumerate(B))+1
def step_untrimmed(b,B):
    e1=m.e1(b,B); DB=m.DB(b,B); DR,gm=m.norm(b,B[::-1],1-e1)
    nb=m._zw(DB,DR[::-1]) if gm==0 else m._zw(DB+[(b-1)*(1-e1)],[1]+DR[::-1])
    return nb,gm
res={}
for b in (3,4,5,10,11,16):
    M=b+1; bad0=bad1=0; n0=n1=0; signs=set()
    for trial in range(30000):
        n=random.randint(1,10)
        B=[random.randint(0,2*b-2) for _ in range(n)]
        nb,gm=step_untrimmed(b,B)
        w=W(b,B); w2=W(b,nb)
        if gm==1:
            n1+=1
            if w2%M!=0: bad1+=1
        else:
            n0+=1
            ok=[s for s in (1,-1) if (w2-s*2*w)%M==0]
            signs.add((n%2,tuple(ok)))
            if not ok: bad0+=1
    print(f"b={b}: gam=1 cases {n1} violations {bad1};  gam=0 cases {n0} violations {bad0}; (n parity, admissible signs) seen: {sorted(signs)}")
