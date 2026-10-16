"""Exact finite-center closure with first nonneutral q=14, one clock."""
from persist_wake_neutral_spacetime import setup,transitions,center_head,reconstruct
from collections import deque
import json,time
hs,pos,start=setup(1);began=time.monotonic()
parent={start:None};queue=deque();edges=0
for ns,x in transitions(start,hs,first=True):
 if x!=14:continue
 edges+=1
 if ns not in parent:parent[ns]=(start,x);queue.append(ns)
complete=True;accepted=None
while queue:
 if len(parent)>1000000 or time.monotonic()-began>45:complete=False;break
 st=queue.popleft();middle=center_head(st,hs)
 if middle is not None:
  accepted=reconstruct(parent,st,middle);break
 for ns,x in transitions(st,hs):
  edges+=1
  if ns not in parent:parent[ns]=(st,x);queue.append(ns)
res=dict(states=len(parent),edges=edges,complete=complete,accepted=accepted,seconds=time.monotonic()-began)
print(json.dumps(res),flush=True)
open('persist_arithmetic_fourteen_closure_results.json','w').write(json.dumps(res,indent=2))
