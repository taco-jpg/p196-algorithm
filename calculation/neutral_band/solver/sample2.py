import os
import sys, random, time, collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import p196cp as P, sched
random.seed(int(sys.argv[2]))
tl=float(sys.argv[1]); t00=time.time()
for (p,NM,MM) in [(5,20,20),(8,20,20),(10,20,20),(12,20,20)]:
    L=[S for S in sched.schedules(p,2,NM,MM,4,7)] if p<=8 else None
    if L is None:
        # sample shapes randomly instead of full enumeration
        sh=list(sched.shapes(p,2)); L=[]
        for s in random.sample(sh,200):
            L+=list(sched.realize(s,NM,MM,4,7))[::37]
    ss=random.sample(L,min(150,len(L)))
    ts=[];st=collections.Counter()
    for S in ss:
        if sched.covered(S): continue
        r=P.solve(10,S,time_limit=tl); ts.append(r['time']); st[r['status']]+=1
    ts.sort()
    print(f"p={p} sampled {len(ts)} of {len(L)}: {dict(st)} median {ts[len(ts)//2]}s p90 {ts[int(.9*len(ts))]}s max {ts[-1]}s",flush=True)
    if time.time()-t00>90: break
