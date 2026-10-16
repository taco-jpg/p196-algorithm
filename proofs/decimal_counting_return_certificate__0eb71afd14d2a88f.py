"""Three incoming image layers shrink each constant-rho maximal overflow fiber.
An exact finite prefix certificate; no claim about general fibers or Lychrel existence.
"""
from collections import deque
from itertools import product
from decimal_counting_return_mixed import layers
import json, math

def build(clock,y):
 root=tuple((0,h,1 if h else -1) for h in clock)
 first=frozenset(ns for ns,labs in layers(root,y+9,clock) if all(labs))
 states=[first];ix={first:0};trans=[];todo=deque([first])
 while todo:
  st=todo.popleft();row=[]
  for s in (y,y+9):
   nxt=frozenset(ns for path in st for ns,_ in layers(path,s,clock))
   if nxt not in ix:
    ix[nxt]=len(states);states.append(nxt);todo.append(nxt)
   row.append(ix[nxt])
  trans.append(row)
 assert frozenset() in ix
 z=ix[frozenset()]
 rev=[[] for _ in states]
 for v,row in enumerate(trans):
  for bit,w in enumerate(row):rev[w].append((v,bit))
 dist=[None]*len(states);kill=[None]*len(states);dist[z]=0;todo=deque([z])
 while todo:
  w=todo.popleft()
  for v,bit in rev[w]:
   if dist[v] is None:
    dist[v]=dist[w]+1;kill[v]=bit;todo.append(v)
 assert all(d is not None for d in dist),(clock,y)
 return dict(clock=clock,y=y,states=[[[list(t) for t in path] for path in sorted(st)] for st in states],transitions=trans,empty=z,distance=dist,kill_bit=kill,K=max(dist))

out=[build(c,y) for c in product((0,1),repeat=3) for y in range(1,9)]
K=max(x['K'] for x in out)
for y in range(1,9):
 rows=[r for r in out if r['y']==y]
 print('y',y,'states',sum(len(r['states']) for r in rows),'K',max(r['K'] for r in rows),'nonempty_clocks',[r['clock'] for r in rows if r['K']])
print('global K',K,'rho',2*(1-2**(-K))**(1/K))
json.dump(dict(description=__doc__,K=K,cases=out),open('main_existence_attempt/decimal_counting_return_certificate.json','w'),indent=1)
