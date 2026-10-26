import sys, time, itertools
from btransfer import decide, patterns, from_path
from decouple import phiB
from ccycle_cpsat import solve_C, vschedules
b=10; p=11
O=(0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1)
r,ns,path=decide(b,p,O,3_000_000,want_path=True)
B=from_path(b,p,path)
cur=list(B); e1s=[]; gs=[]
for t in range(p):
    nb,u,E1,g=phiB(b,cur); e1s.append(E1); gs.append(g); cur=nb
print("e1 stream",e1s,"gam",gs)
t0=time.time(); tried=0; stat={}
lo,hi=int(sys.argv[1]),int(sys.argv[2]); tl=float(sys.argv[3]); budget=float(sys.argv[4])
for c0 in range(lo,hi+1):
    for vs in vschedules(p,sum(gs)//2):
        if time.time()-t0>budget: print("budget exhausted at c0=",c0,"tried",tried); sys.exit()
        nm,sol=solve_C(b,e1s,gs,c0,vs,tl); tried+=1
        stat[nm]=stat.get(nm,0)+1
        if sol: print("FOUND C-cycle! c0=",c0,"v=",vs,"C0=",sol[0]); sys.exit()
    print(f"c0={c0}: {stat}  ({time.time()-t0:.0f}s)",flush=True)
