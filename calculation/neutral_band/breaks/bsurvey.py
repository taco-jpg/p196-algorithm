import sys, time, collections
from btransfer import decide, patterns
lo,hi,pmax,ms,tl=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5])
for b in range(lo,hi+1):
    t0=time.time(); found={}
    for p in range(1,pmax+1):
        if time.time()-t0>tl: found[p]='T'; continue
        ex=0; lim=0
        for O in patterns(p):
            r,ns,_=decide(b,p,O,ms)
            if r=='EXISTS': ex+=1
            elif r=='LIMIT': lim+=1
        found[p]=(ex if not lim else f"{ex}+{lim}lim")
    print(f"base {b:3d}: #B-cycle overflow-patterns by period p: "+" ".join(f"p{p}:{found[p]}" for p in found)+f"  ({time.time()-t0:.0f}s)",flush=True)
