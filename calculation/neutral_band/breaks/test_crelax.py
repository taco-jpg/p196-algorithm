import os
import sys, time, collections
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import neutral_band_search as N
from neutral_band_search import *
from c_relax import *
# sanity: true streams of known certificates must be FEASIBLE with the true v-schedule
for b,es in N._lean_certs():
    if b not in (26,16,4,17): continue
    e1s=[e1(b,E[0]) for E in es]; gs=[gam(b,E[0],E[1]) for E in es]; vs=tuple(E[5] for E in es)
    print("base",b,"true schedule, K=6:",c_window_feasible(b,e1s,gs,vs,6,4,20))
# the base-10 p=11 B-cycle streams
e1s=[0,0,1,1,1,0,1,0,0,1,1]; gs=[0,0,0,0,1,1,1,0,0,0,1]
K=int(sys.argv[1]); t0=time.time(); st=collections.Counter()
for vs in vschedules(11,2):
    r=c_window_feasible(10,e1s,gs,vs,K,4,10); st[r]+=1
    if r not in('INFEASIBLE',): print("   schedule",vs,r)
print("base 10, p=11 B-cycle streams, K=%d window, all 66 v-schedules:"%K,dict(st),"(%.0fs)"%(time.time()-t0))
