from collections import deque
from itertools import product
from functools import lru_cache
from decimal_counting_return_mixed import layers
import json,sys,time

def run(clock,cap=30000):
 joint=[];ji={}
 def jindex(st):
  if st not in ji:ji[st]=len(joint);joint.append(st)
  return ji[st]
 @lru_cache(None)
 def local(i,x):
  return sum(1<<jindex(ns) for ns in set(ns for ns,_ in layers(joint[i],x,clock)))
 @lru_cache(None)
 def move(st,x):
  out=0
  while st:
   bit=st&-st;i=bit.bit_length()-1;st-=bit
   out |= local(i,x)
  return out
 root=tuple((0,h,1 if h else -1) for h in clock)
 roots=[]
 for y in range(1,9):
  v=sum(1<<jindex(ns) for ns in set(ns for ns,labs in layers(root,y+9,clock) if all(labs)))
  if v:roots.append(frozenset((v,)))
 if not roots:return dict(clock=clock,empty=True)
 seen={s:i for i,s in enumerate(set(roots))};states=list(seen);todo=deque(states);edges=[]
 while todo:
  st=todo.popleft();row=[]
  for y in range(1,9):
   nxt=frozenset(move(i,x) for i in st for x in (y,y+9))
   if 0 in nxt:row.append(-1);continue
   if nxt not in seen:
    seen[nxt]=len(states);states.append(nxt);todo.append(nxt)
   row.append(seen[nxt])
  edges.append(row)
  if len(states)>cap:return dict(clock=clock,capped=len(states),processed=len(edges),maxcollection=max(map(len,states)),joint_states=len(joint))
 alive=set(range(len(states)));rounds=0
 while True:
  new={i for i in alive if any(j in alive for j in edges[i])}
  rounds+=1
  if new==alive:break
  alive=new
 r=dict(clock=clock,states=len(states),winning=len(alive),elimination_rounds=rounds,maxcollection=max(map(len,states)),joint_states=len(joint))
 if alive:
  pos={};v=next(iter(alive));walk=[]
  while v not in pos:
   pos[v]=len(walk)
   y,nxt=next((y,w) for y,w in enumerate(edges[v],1) if w in alive)
   walk.append((v,y));v=nxt
  r['cycle']=walk[pos[v]:]
 json.dump(dict(summary=r,joint_states=joint,states=[sorted(st) for st in states],transitions=edges,winning=sorted(alive)),open('main_existence_attempt/decimal_counting_return_variable_mixed_'+''.join(map(str,clock))+'.json','w'))
 return r

out=[]
for c in product((0,1),repeat=3):
 r=run(c);out.append(r);print(r,flush=True)
json.dump(out,open('main_existence_attempt/decimal_counting_return_variable_mixed_results.json','w'),indent=2)
