"""Finite-center probes: duration of exact maximal-speed outer clock.
Finite delays do not establish an infinite clock.
"""
from creative_regular_invariant import qstep
from novel_stack_spatial_lift import BASE
from itertools import product
import json,time,argparse

def duration(w,limit=512):
 for t in range(limit):
  a=w[0][0] if w[0] else w[1]
  nxt=qstep(w)
  an=nxt[0][0] if nxt[0] else nxt[1]
  if an!=25-a:return t
  w=nxt
 return limit

def decimal(w):
 p,c=w;low=[];high=[]
 for q in p:
  a=min(q,9);b=q-a
  if not high and b==0:b=1;a=q-1
  low.append(a);high.append(b)
 digits=high+([] if c is None else [c//2])+low[::-1]
 return int(''.join(map(str,digits)))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--maxpairs',type=int,default=5);args=ap.parse_args()
 results=[]
 for k in range(3,args.maxpairs+1):
  best=-1;records=[];count=0;t0=time.monotonic()
  for b in BASE:
   for suf in product(range(19),repeat=k-3):
    for c in [None]+list(range(0,19,2)):
     w=(b+suf,c);v=duration(w);count+=1
     if v>best:best=v;records=[w]
     elif v==best and len(records)<20:records.append(w)
  r={'pairs':k,'count':count,'max_clock_steps':best,'records':records,'decimal_representatives':[decimal(w) for w in records],'seconds':time.monotonic()-t0}
  print(json.dumps(r),flush=True);results.append(r)
 open('novel_stack_finite_center_results.json','w').write(json.dumps(results,indent=2))
