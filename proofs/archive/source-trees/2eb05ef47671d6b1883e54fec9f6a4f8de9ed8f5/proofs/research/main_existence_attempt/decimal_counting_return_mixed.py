from collections import deque
from functools import lru_cache
from itertools import product
import json,sys
sys.path.insert(0,'research')
sys.setrecursionlimit(50000)
from astra_counting_nooverflow_depth import sccs

@lru_cache(None)
def local(st,s,h):
 a,b,t=st;out=[]
 for x in range(19):
  for bn in (0,1):
   if (x+bn)//10!=b:continue
   an,lo=divmod(x+a,10);hi=(x+bn)%10
   if (lo+t if h else lo+hi)==s:out.append(((an,bn,hi if h else -1),x))
 return tuple(out)

@lru_cache(None)
def layers(st,s,clock):
 if not st:return (((),()),)
 h=clock[0]
 return tuple(((ns,)+tail,(x,)+labels) for ns,x in local(st[0],s,h) for tail,labels in layers(st[1:],x,clock[1:]))

def graph(clock,y,cap=50000):
 root=tuple((0,h,1 if h else -1) for h in clock)
 first=frozenset(ns for ns,labs in layers(root,y+9,clock) if all(labs))
 if not first:return dict(states=1,empty=True)
 states=[first];ix={first:0};trans=[];todo=deque([first])
 while todo:
  st=todo.popleft();row=[]
  for s in (y,y+9):
   nxt=frozenset(ns for path in st for ns,_ in layers(path,s,clock))
   if nxt not in ix:
    if len(states)>=cap:return dict(capped=cap)
    ix[nxt]=len(states);states.append(nxt);todo.append(nxt)
   row.append(ix[nxt])
  trans.append(row)
 comps=sccs(trans)
 closed=[c for c in comps if states[c[0]] and all(w in c for v in c for w in trans[v])]
 return dict(states=len(states),maxsubset=max(map(len,states)),components=[len(c) for c in comps],closed=[len(c) for c in closed])

if __name__=='__main__':
 out=[]
 for d in (3,4):
  for c in product((0,1),repeat=d):
   for y in range(1,9):
    r=dict(clock=c,y=y,**graph(c,y,10000));print(r,flush=True);out.append(r)
 open('main_existence_attempt/decimal_counting_return_mixed.json','w').write(json.dumps(out,indent=2))
