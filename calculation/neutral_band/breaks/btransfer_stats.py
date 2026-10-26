import sys, time, collections
from btransfer import decide, patterns
b=int(sys.argv[1]); p=int(sys.argv[2]); ms=int(sys.argv[3]); tl=float(sys.argv[4])
t0=time.time(); res=collections.Counter(); mx=0; npat=0
for O in patterns(p):
    if time.time()-t0>tl: res['timeout-skipped']+=1; continue
    r,ns,_=decide(b,p,O,ms); res[r]+=1; mx=max(mx,ns); npat+=1
print(f"base {b} p={p}: {dict(res)} max reachable states per pattern = {mx}  ({time.time()-t0:.1f}s)",flush=True)
