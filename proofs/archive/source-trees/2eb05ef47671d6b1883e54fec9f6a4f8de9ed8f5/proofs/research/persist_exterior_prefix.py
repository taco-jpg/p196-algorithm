"""Exact existential carry-prefix refinement; no finite decimal existence conclusion."""
from collections import deque
from novel_projective_clock import prefix_step
import time,json,argparse

def refine(previous,k):
 cand=[p+(x,) for p in previous for x in range(19)]
 lookup={s:i for i,s in enumerate(cand)}
 outs=[];incoming=[[] for s in cand]
 for i,s in enumerate(cand):
  nxt=set()
  for u in (0,1):
   t,h=prefix_step(s,u)
   if t[0]!=25-s[0]:continue
   j=lookup.get(t)
   if j is not None:nxt.add(j)
  outs.append(len(nxt))
  for j in nxt:incoming[j].append(i)
 queue=deque(i for i,d in enumerate(outs) if d==0)
 while queue:
  i=queue.popleft()
  for j in incoming[i]:
   outs[j]-=1
   if outs[j]==0:queue.append(j)
 return [s for s,d in zip(cand,outs) if d]

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--width',type=int,default=10);ap.add_argument('--states',type=int,default=1000000);args=ap.parse_args()
 alive=[(8,),(17,)];data=[]
 for k in range(2,args.width+1):
  if 19*len(alive)>args.states:break
  t=time.monotonic();count=19*len(alive);alive=refine(alive,k)
  r={'width':k,'candidate_states':count,'live_states':len(alive),'seconds':time.monotonic()-t,'exact':True}
  data.append(r);print(json.dumps(r),flush=True)
  json.dump(data,open('persist_exterior_prefix_results.json','w'),indent=2)
  if not alive:break
 if len(alive)<100000:json.dump(alive,open('persist_exterior_prefix_live.json','w'))
