"""Small validation survey: lifetime of canonical runs from random (B,C) starts, per base.
usage: python3 lifetimes.py <samples> <maxB> <maxC> base1 base2 ...   (single thread)"""
import sys, collections, random
from lib import *
def lifetime_info(b,B,C,maxsteps=200,maxlen=300):
    """returns (kind, steps, deathinfo)"""
    r=run(b,B,C,maxsteps=maxsteps,maxlen=maxlen)
    return r
def death_type(b,B,C):
    """replay run; at death return (steps, gam at last transition, previous kind)"""
    seen=set(); cur=(tuple(B),tuple(C)); t=0; lastg=None
    while True:
        if cur in seen: return ('cycle',t,None)
        seen.add(cur)
        E=step(b,list(cur[0]),list(cur[1]))
        if E is None: return ('break',t,lastg)
        lastg=gam(b,E[0],E[1]); cur=(tuple(E[2]),tuple(E[3])); t+=1
        if t>200 or len(cur[0])+len(cur[1])>300: return ('long',t,None)
if __name__=="__main__":
    S=int(sys.argv[1]); mB=int(sys.argv[2]); mC=int(sys.argv[3]); bases=[int(x) for x in sys.argv[4:]]
    print("base samples  mean_life  P(>=3) P(>=5) P(>=8) P(>=12) max  cyc  long | deaths after overflow step / total")
    for b in bases:
        rng=random.Random(b*7919+1); L=collections.Counter(); kinds=collections.Counter(); after=collections.Counter(); mx=0; tot=0
        valid=0
        for _ in range(S):
            B,C=rand_state(b,rng,(1,mB),(0,mC))
            if not hyp(b,B,C): continue   # start must have e1!=e2
            valid+=1
            k,t,lg=death_type(b,B,C)
            kinds[k]+=1; L[t]+=1; mx=max(mx,t); tot+=t
            if k=='break' and t>0: after[lg]+=1
        ge=lambda s: sum(v for t,v in L.items() if t>=s)/valid
        print(f"{b:4d} {valid:7d} {tot/valid:8.3f}  {ge(3):.4f} {ge(5):.5f} {ge(8):.6f} {ge(12):.7f} {mx:4d} {kinds['cycle']:4d} {kinds['long']:4d} | deaths with prev step gam=1: {after[1]}, gam=0: {after[0]}")
