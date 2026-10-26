import os
import sys, random, time, resource, collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import p196cp as P, sweep
random.seed(7)
us=list(sweep.units(10,[12],[2])); random.shuffle(us)
ts=[]; c=collections.Counter(); t0=time.time()
for (b,p,G,gam,u) in us[:60]:
    for v in sweep.wcomp(1,p)[:0] if False else list(sweep.wcomp(1,p))[:3]:
        sh=tuple(zip(gam,u,v))
        if not sweep.canonical_primitive(sh): continue
        pn=[0];pm=[0]
        for (g,uu,vv) in sh[:-1]: pn.append(pn[-1]+g-uu); pm.append(pm[-1]+g-2*vv)
        n0=random.randint(max(12-x for x in pn),min(30-x for x in pn)); m0=random.randint(max(15-x for x in pm),min(45-x for x in pm))
        S=tuple((n0+pn[k],m0+pm[k]) for k in range(p))
        r=P.solve(10,S,time_limit=60); ts.append(r['time']); c[r['status']]+=1
        if time.time()-t0>80: break
    if time.time()-t0>80: break
ts.sort(); print(dict(c),"n=",len(ts),"mean %.4f median %.4f max %.3f"%(sum(ts)/len(ts),ts[len(ts)//2],ts[-1]))
print("peak RSS MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
