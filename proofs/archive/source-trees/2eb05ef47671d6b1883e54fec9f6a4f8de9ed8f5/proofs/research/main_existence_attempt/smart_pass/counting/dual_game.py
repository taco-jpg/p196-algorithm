"""Dual universal-bit survival game for arbitrary rho words."""
import json,time
from pathlib import Path
p=Path(__file__).with_name('compact_transitions.txt')
tau=[list(map(int,line.split())) for line in p.read_text().splitlines()]
N=len(tau);states=[(1<<N)-1];idx={states[0]:0};edges=[];todo=0;t0=time.time();cap=1000000
while todo<len(states):
 s=states[todo];row=[]
 for y in range(8):
  out=0
  for v in range(N):
   a,b=tau[v][y],tau[v][y+8]
   if a>=0 and b>=0 and (s>>a&1) and(s>>b&1):out|=1<<v
  if out not in idx:idx[out]=len(states);states.append(out)
  row.append(idx[out])
 edges.append(row);todo+=1
 if todo%1000==0:print('progress',todo,len(states),'sec',time.time()-t0,flush=True)
 if len(states)>cap:print('CAPPED',todo,len(states));break
else:
 # Nonempty-state longest path: directed cycle means an infinite viable rho word.
 import sys;sys.setrecursionlimit(100000)
 color=[0]*len(states);rank=[None]*len(states);trace=[];cycle=[]
 def dfs(v):
  if not states[v]:return -1
  if color[v]==2:return rank[v]
  if color[v]==1:
   cycle.extend(trace[trace.index(v):]+[v]);raise RuntimeError('cycle')
  color[v]=1;trace.append(v);r=0
  for w in edges[v]:r=max(r,1+dfs(w))
  trace.pop();color[v]=2;rank[v]=r;return r
 try:dfs(0)
 except RuntimeError:pass
 summary=dict(states=len(states),cycle=cycle,maxrank=max((x for x in rank if x is not None),default=-1),rootrank=rank[0],seconds=time.time()-t0)
 print(json.dumps(summary,indent=2),flush=True)
 json.dump(dict(summary=summary,states=states,edges=edges,rank=rank),open(Path(__file__).with_name('dual_game.json'),'w'))
