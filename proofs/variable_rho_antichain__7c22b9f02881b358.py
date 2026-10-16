"""Exact universal-block analysis for three non-overflow inverse layers.
An antichain stores the minimal possible NFA subsets under all binary choices.
"""
import sys,json,time,argparse
from pathlib import Path
from functools import lru_cache
from itertools import product
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from astra_counting_nooverflow_depth import layers

p=argparse.ArgumentParser();p.add_argument('--cap',type=int,default=500000);p.add_argument('--depth',type=int,default=3);a=p.parse_args()
D=a.depth
joint=list(product(tuple(product((0,1),repeat=2)),repeat=D));ix={s:i for i,s in enumerate(joint)}
table=[[sum(1<<ix[ns] for ns in set(ns for ns,_ in layers(st,x))) for x in range(19)] for st in joint]
@lru_cache(None)
def move(v,x):
 out=0
 while v:
  b=v&-v;v-=b;out|=table[b.bit_length()-1][x]
 return out

def minimal(xs):
 xs=sorted(set(xs),key=lambda x:(x.bit_count(),x));out=[]
 for v in xs:
  if not any(v&w==w for w in out):out.append(v)
 return tuple(sorted(out))

def step(st,y):
 out=minimal(move(v,x) for v in st for x in (y,y+9))
 return None if out==(0,) else out

states=[((1<<len(joint))-1,)];si={states[0]:0};edges=[];todo=0;t0=time.time();capped=False
while todo<len(states):
 st=states[todo];row=[]
 for y in range(1,9):
  ns=step(st,y)
  if ns is None:row.append(-1);continue
  if ns not in si:
   si[ns]=len(states);states.append(ns)
  row.append(si[ns])
 edges.append(row);todo+=1
 if todo%10000==0:print('progress',todo,len(states),'maxcollection',max(map(len,states)),'seconds',round(time.time()-t0,2),flush=True)
 if len(states)>a.cap:capped=True;break
if not capped:
 alive=set(range(len(states)));rank=[None]*len(states);r=0
 while True:
  new={i for i in alive if any(j in alive for j in edges[i])}
  for i in alive-new:rank[i]=r
  if new==alive:break
  alive=new;r+=1
 summary=dict(depth=D,states=len(states),alive=len(alive),maxrank=max((x for x in rank if x is not None),default=-1),rootrank=rank[0],maxcollection=max(map(len,states)),seconds=time.time()-t0)
 if alive:
  v=0;seen={};walk=[]
  while v not in seen:
   seen[v]=len(walk);y,nxt=next((y,w) for y,w in enumerate(edges[v],1) if w in alive);walk.append((v,y));v=nxt
  summary['prefix']=walk[:seen[v]];summary['cycle']=walk[seen[v]:]
 json.dump(dict(summary=summary,joint=joint,states=states,edges=edges,rank=rank),open(Path(__file__).with_name('variable_rho_antichain_d'+str(D)+'.json'),'w'))
else:summary=dict(depth=D,capped=len(states),processed=todo,seconds=time.time()-t0,maxcollection=max(map(len,states)))
print(json.dumps(summary,indent=2),flush=True)
