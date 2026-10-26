import os
import sys, random, time, collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import p196cp as P, sched
random.seed(11)
L=list(sched.schedules(6,2,14,16,4,7)); ss=random.sample(L,300)
res={}
for be in ('cpsat','z3'):
    t=time.time(); c=collections.Counter()
    for S in ss: c[P.solve(10,S,backend=be,time_limit=20)['status']]+=1
    print(be,dict(c),f"{time.time()-t:.1f}s",flush=True)
