"""Adversarial interior-carry trap under the known eight-phase boundary clock.
A nonempty universal trap would be a sufficient finite-prefix invariant.
"""
from novel_stack_spatial_lift import BASE,scc
from novel_encoding_critical_clock import evolve
from itertools import product
from collections import deque
import json,time

def game(k):
 ts=time.monotonic()
 states={b+x for b in BASE for x in product(range(19),repeat=k-3)}
 phase={b:i for i,b in enumerate(BASE)}
 rev={s:set() for s in states};adj={};bad=[]
 for s in states:
  expected=BASE[(phase[s[:3]]+1)%8]
  outs={evolve(s,c) for c in (0,1)}
  adj[s]=outs&states
  if any(q[:3]!=expected for q in outs):bad.append(s)
  for out in adj[s]:rev[out].add(s)
 queue=deque(bad);dead=set(bad)
 while queue:
  x=queue.popleft()
  for parent in rev[x]:
   if parent not in dead:dead.add(parent);queue.append(parent)
 trap=states-dead
 cyclic=scc(adj)
 result={'width':k,'states':len(states),'universal_trap_states':len(trap),'cyclic_scc_sizes':sorted(len(c) for c in cyclic),'seconds':time.monotonic()-ts}
 return result

if __name__=='__main__':
 results=[]
 for k in range(4,7):
  r=game(k);print(json.dumps(r),flush=True);results.append(r)
 open('novel_stack_spatial_game_results.json','w').write(json.dumps(results,indent=2))
