"""Finite-state, arbitrary-width check for overflow carry normalization.
This is an exact graph exhaustion, not a bounded-length input enumeration.
"""
from collections import deque
import json

def norm_edges(st):
 a,b=st
 if b==0:
  yield 0,(0,0);yield 0,(0,1)
 else:
  yield 10,(1,0);yield 10,(1,1)
 if a!=b:yield 9,(a,b)

def edge(st,q,h):
 a,b,t=st
 for bn in (0,1):
  if (q+bn)//10!=b:continue
  an=(q+a)//10;lo=(q+a)%10;hi=(q+bn)%10
  yield (an,bn,hi if h else -1),lo+t if h else lo+hi

def feed(states,q,hs):
 if not states:
  yield (),q;return
 for st,r in edge(states[0],q,hs[0]):
  for tail,s in feed(states[1:],r,hs[1:]):yield (st,)+tail,s

def finish(states,c,hs,bad):
 if not states:
  yield bad or c is not None and c>9;return
 a,b,t=states[0];h=hs[0]
 if c is None:
  if a!=b:return
  yield from finish(states[1:],2*t if h else None,hs[1:],bad)
 elif (c+a)//10==b:
  r=(c+a)%10
  if h:
   for tail,qout in feed(states[1:],r+t,hs[1:]):
    yield from finish(tail,None,hs[1:],bad or qout>9)
  else:yield from finish(states[1:],2*r,hs[1:],bad)

def check(first,hs):
 initial=((0,1),tuple((0,h,1 if h else -1) for h in hs),False)
 seen={};queue=deque()
 for q,ns in norm_edges(initial[0]):
  if q!=first:continue
  for tail,r in feed(initial[1],q,hs):
   st=(ns,tail,r>9);seen[st]=(q,);queue.append(st)
 edges=0;terminals=0;terminal_bad=0
 while queue:
  ns,states,bad=st=queue.popleft()
  a,b=ns
  terminals_c=([None] if a==b else [])+[10*b]
  for c in terminals_c:
   for result in finish(states,c,hs,bad):
    terminals+=1
    if result:
     terminal_bad+=1
     return dict(first=first,schedule=hs,status='counterexample',pairs=seen[st],center=c,states=len(seen))
  for q,nns in norm_edges(ns):
   for tail,r in feed(states,q,hs):
    edges+=1;nxt=(nns,tail,bad or r>9)
    if nxt not in seen:seen[nxt]=seen[st]+(q,);queue.append(nxt)
 return dict(first=first,schedule=hs,status='complete',states=len(seen),edges=edges,terminals=terminals,bad_terminals=terminal_bad)
if __name__=='__main__':
 r=[check(10,(1,0)),check(9,(1,1,0))]
 print(json.dumps(r,indent=2));json.dump(r,open('resume_renewal_normalization_results.json','w'),indent=2)
