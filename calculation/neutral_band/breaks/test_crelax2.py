import sys, time, collections
from c_relax import *
e1s=[0,0,1,1,1,0,1,0,0,1,1]; gs=[0,0,0,0,1,1,1,0,0,0,1]
K=int(sys.argv[1]); lim=float(sys.argv[2]); t0=time.time(); st=collections.Counter(); first={}
for vs in vschedules(11,2):
    if time.time()-t0>lim: st['skipped']+=1; continue
    r=c_window_feasible(10,e1s,gs,vs,K,4,15); st[r]+=1
print("K=%d: %s (%.0fs)"%(K,dict(st),time.time()-t0))
