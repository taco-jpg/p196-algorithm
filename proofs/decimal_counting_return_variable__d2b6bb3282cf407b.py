from collections import deque
from itertools import product
from decimal_counting_return_mixed import layers
import json

clock=(0,0,0)
root=tuple((0,0,-1) for _ in clock)
allstates=tuple(product(tuple((a,b,-1) for a,b in product((0,1),repeat=2)),repeat=3))
ix={s:i for i,s in enumerate(allstates)}
local={}
for st in allstates:
 for s in range(3,7):
  for x in (s,s+9):
   ans=layers(st,x,clock)
   assert len(ans)<=1
   local[(ix[st],x)]=None if not ans else ix[ans[0][0]]
roots=[]
for y in range(3,7):
 st=frozenset(ix[ns] for ns,labs in layers(root,y+9,clock) if all(labs))
 roots.append(st)
seen={s:i for i,s in enumerate(set(roots))};states=list(seen);todo=deque(states);edges=[]
while todo:
 st=todo.popleft();row=[]
 for y in range(3,7):
  nxt=[]
  for i in st:
   nxt += [local[(i,y)],local[(i,y+9)]]
  if None in nxt:row.append(-1);continue
  nxt=frozenset(nxt)
  if nxt not in seen:
   seen[nxt]=len(states);states.append(nxt);todo.append(nxt)
  row.append(seen[nxt])
 edges.append(row)
 if len(states)>200000:
  print('capped',len(states));break
alive=set(range(len(states)))
while True:
 new={i for i in alive if any(j in alive for j in edges[i])}
 if new==alive:break
 alive=new
print(dict(states=len(states),winning=len(alive),sizes=sorted(set(map(len,states))),winning_states=[sorted(states[i]) for i in alive][:4]))
