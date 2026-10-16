from collections import deque
from itertools import product
from functools import lru_cache
from decimal_counting_return_mixed import layers
import json,sys
clock=(0,0,0)
allstates=tuple(product(tuple((a,b,-1) for a,b in product((0,1),repeat=2)),repeat=3))
ix={s:i for i,s in enumerate(allstates)}
local={}
for i,st in enumerate(allstates):
 for x in range(1,18):
  if x==9:continue
  local[i,x]=sum(1<<ix[ns] for ns in set(ns for ns,_ in layers(st,x,clock)))
@lru_cache(None)
def move(st,x):
 out=0
 while st:
  bit=st&-st;i=bit.bit_length()-1;st-=bit
  out|=local[i,x]
 return out
root=tuple((0,0,-1) for _ in clock)
roots=[]
for y in range(1,9):
 v=sum(1<<ix[ns] for ns in set(ns for ns,labs in layers(root,y+9,clock) if all(labs)))
 if v:roots.append(frozenset((v,)))
seen={s:i for i,s in enumerate(set(roots))};states=list(seen);todo=deque(states);edges=[]
cap=int(sys.argv[1]) if len(sys.argv)>1 else 200000
while todo:
 st=todo.popleft();row=[]
 for y in range(1,9):
  nxt=frozenset(move(i,x) for i in st for x in (y,y+9))
  if 0 in nxt:row.append(-1);continue
  if nxt not in seen:
   seen[nxt]=len(states);states.append(nxt);todo.append(nxt)
  row.append(seen[nxt])
 edges.append(row)
 if len(states)>cap:
  print('CAPPED',len(states),'processed',len(edges),'maxcollection',max(map(len,states)),flush=True)
  break
 if len(edges)%10000==0:print('progress',len(edges),len(states),len(st),flush=True)
else:
 alive=set(range(len(states)));rounds=0
 while True:
  new={i for i in alive if any(j in alive for j in edges[i])}
  rounds+=1
  if new==alive:break
  alive=new
 print(dict(states=len(states),winning=len(alive),elimination_rounds=rounds,maxcollection=max(map(len,states)),winning_ids=list(alive)[:20]),flush=True)
 json.dump(dict(states=[sorted(st) for st in states],transitions=edges,winning=sorted(alive)),open('main_existence_attempt/decimal_counting_return_variable_nfa.json','w'))
 if alive:
  pos={};v=next(iter(alive));walk=[]
  while v not in pos:
   pos[v]=len(walk)
   y,nxt=next((y,w) for y,w in enumerate(edges[v],1) if w in alive)
   walk.append((v,y));v=nxt
  print('CYCLE',walk[pos[v]:],flush=True)
