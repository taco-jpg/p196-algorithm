import os
import sys, random, time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import p196cp as P, sched
random.seed(1)
tl=float(sys.argv[1]); 
for (p,NM,MM,lo_n,lo_m) in [(4,6,8,4,7),(6,8,10,5,7),(6,12,14,8,10),(8,10,12,6,8),(12,10,12,6,8)]:
    L=[S for S in sched.schedules(p,2,NM,MM,lo_n,lo_m)]
    if not L: print(p,"none"); continue
    ss=random.sample(L,min(4,len(L)))
    for S in ss:
        r=P.solve(10,S,time_limit=tl)
        print(f"p={p} n~{S[0][0]} m~{S[0][1]} -> {r['status']} {r['time']}s vars={r['nvars']} cons={r['ncons']}",flush=True)
