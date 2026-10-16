from exist_uniform_slow_spatial import uniform_target
from continuation_theory_multigrowth import transitions
from collections import deque
import time,json

def run(periods,cap=50000,seconds=5):
 targets={uniform_target(periods,d):d for d in (8,7,5,1,2,4)}
 start=((1,)*len(periods),tuple(1<<(p-1) for p in periods),(0,)*len(periods))
 par={start:None};queue=deque([start]);edges=0;st=time.monotonic();deadline=st+seconds
 complete=True;found=None;maxdepth=0;depth={start:0}
 try:
  while queue:
   if len(par)>cap or time.monotonic()>deadline:complete=False;break
   s=queue.popleft();maxdepth=max(maxdepth,depth[s])
   if s in targets:
    path=[];found={'bulk_digit':targets[s],'state':s}
    while par[s] is not None:
     s,dp=par[s];path.append(dp)
    found['path']=path[::-1];break
   for ns,dp in transitions(10,periods,s,deadline):
    edges+=1
    if ns not in par:par[ns]=(s,dp);depth[ns]=depth[s]+1;queue.append(ns)
 except TimeoutError:complete=False
 return {'periods':periods,'states':len(par),'edges':edges,'maxdepth':maxdepth,'complete':complete,'seconds':time.monotonic()-st,'found':found}
if __name__=='__main__':
 out=[]
 for ps in ((2,4,2)*3,(4,2,2)*3,(2,2,4)*3):
  r=run(ps);out.append(r);print(json.dumps(r),flush=True);json.dump(out,open('exist_uniform_slow_forward_results.json','w'),indent=2)
