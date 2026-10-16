from explore import step,z
from itertools import product
from collections import defaultdict,deque
import json

def run(cap,phases):
 edges=defaultdict(dict)
 for c in phases:
  for b in range(cap+1):
   for B in product(range(19),repeat=b):
    if B and (not B[0] or B[-1]==c):continue
    d,C,g=step(c,B)
    edges[c,z(c,B)].setdefault((d,z(d,C)),(B,C,g))
 # iterated DFS, return a projected closed walk, keep exact edge witnesses
 status={};parent={}
 for root in list(edges):
  if root in status:continue
  stack=[(root,iter(edges[root]))];status[root]=1
  while stack:
   u,it=stack[-1]
   try:v=next(it)
   except StopIteration:status[u]=2;stack.pop();continue
   if status.get(v)==1:
    path=[(u,v)];q=u
    while q!=v:
     r=parent[q];path.append((r,q));q=r
    path.reverse()
    return [dict(source=a,target=b,B=edges[a][b][0],C=edges[a][b][1],overflow=edges[a][b][2]) for a,b in path]
   if v not in status:
    status[v]=1;parent[v]=u;stack.append((v,iter(edges.get(v,{}))))
 return None
if __name__=='__main__':
 for cap in range(1,5):
  r=run(cap,[6,12]);print(cap,json.dumps(r))
  if r:break
