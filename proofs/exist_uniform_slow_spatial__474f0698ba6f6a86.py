"""Exact spatial route for slower uniform-digit pumps, with explicit caps."""
from continuation_theory_multigrowth import backwards,transitions
from continuation_theory_graph import half
import json

def uniform_target(periods,d):
 initial=d;ls=[];mask=[]
 for p in periods:
  ls.append(d);c=0
  for i in range(p):
   h=int(d>=5);c|=h<<i
   d=2*d-9*h
  mask.append(c)
 assert d==initial
 target=(tuple(ls),tuple(mask),tuple(mask))
 # Uniform digit pair is exactly a spatial self-loop.
 for j,p in enumerate(periods):
  after=ls[(j+1)%len(periods)]
  assert (after,after,mask[j],mask[j]) in half(10,'E',ls[j],ls[j],mask[j],mask[j],p)
 return target

if __name__=='__main__':
 out=[]
 for d in (8,7,5,1,2,4):
  ps=(2,4,2)*3;t=uniform_target(ps,d)
  r=backwards(10,ps,t,maxstates=20000,seconds=3)
  r['bulk_digit']=d;r['target']=t;out.append(r);print(json.dumps(r),flush=True)
  json.dump(out,open('exist_uniform_slow_spatial_results.json','w'),indent=2)
