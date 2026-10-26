import os
import sys, random, time, collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import p196cp as P, sched
random.seed(3)
t=time.time(); c=collections.Counter()
for S in [((1,2),(2,3),(2,3),(1,3),(2,4),(2,4))]:
    c['base4 known '+P.solve(4,S,backend='z3',time_limit=20)['status']]+=1
L=list(sched.schedules(4,2,9,10,4,7)); ss=random.sample(L,40)
for S in ss: c['b10 '+P.solve(10,S,backend='z3',time_limit=20)['status']]+=1
print(dict(c), f"{time.time()-t:.1f}s")
