"""Exact arbitrary-width, finite-time center language at a neutral cut.

A spatial state stores 22 low incoming/high outgoing carries and the
previous outer column's high-side digit at overflow times. No temporal
return or bound on center width is imposed. Exact even/odd center heads
close the finite spacetime strip.
"""
from collections import deque
import time,json,argparse
CLOCK=(1,1,0,0,0,1,0,0,0,0,1)
INCOMING=(0,1,0,0,1,1,0,0,1,1,1)


def bitmask(xs):return sum(v<<i for i,v in enumerate(xs))

def setup(periods=2):
 hs=CLOCK*periods;incoming=INCOMING*periods
 pos=[i for i,h in enumerate(hs) if h]
 start=(bitmask(incoming),bitmask([1-x for x in incoming]),tuple(9*incoming[t]for t in pos))
 return hs,pos,start


def transitions(state,hs,first=False):
 lm,rm,prev=state;T=len(hs)
 def visit(t,q,nlm,nrm,digits,j):
  if t==T:
   yield (nlm,nrm,tuple(digits));return
  l=(lm>>t)&1;r=(rm>>t)&1
  total=q+l;lo=total%10;lc=total//10
  for b in (0,1):
   z=q+b
   if z//10!=r:continue
   hi=z%10
   if hs[t]:
    nq=lo+prev[j]
    yield from visit(t+1,nq,nlm|(lc<<t),nrm|(b<<t),digits+[hi],j+1)
   else:
    yield from visit(t+1,lo+hi,nlm|(lc<<t),nrm|(b<<t),digits,j)
 for initial in range(19):
  if first and initial==9:continue
  for ns in visit(0,initial,0,0,[],0):yield ns,initial


def center_head(state,hs):
 lm,rm,prev=state
 for middle in [()]+[(x,)for x in range(0,19,2)]:
  q=middle;j=0
  for t,h in enumerate(hs):
   c=(lm>>t)&1;digits=[]
   for x in q:
    z=x+c;digits.append(z%10);c=z//10
   if c!=((rm>>t)&1):break
   if h:
    if not q:q=(2*prev[j],)
    else:
     end=digits[0]+prev[j]
     q=(end,)+tuple(digits[i]+digits[len(digits)-i]for i in range(1,len(digits)))+(end,)
    j+=1
   else:q=tuple(a+b for a,b in zip(digits,digits[::-1]))
  else:return middle
 return None


def reconstruct(parent,state,middle):
 half=[]
 while parent[state] is not None:
  state,x=parent[state];half.append(x)
 half.reverse()
 return tuple(half)+middle+tuple(half[::-1])


def search(periods=2,limit=100000,seconds=30):
 hs,pos,start=setup(periods);t0=time.monotonic()
 parent={start:None};queue=deque([start]);edges=0;accepted=[];complete=True;bydepth={};depth={start:0}
 while queue:
  if len(parent)>limit or time.monotonic()-t0>seconds:complete=False;break
  st=queue.popleft();d=depth[st];bydepth[d]=bydepth.get(d,0)+1
  middle=center_head(st,hs)
  if middle is not None:
   q=reconstruct(parent,st,middle);accepted.append(q);print('CENTER',len(q),q,flush=True)
   complete=False
   break
  for ns,x in transitions(st,hs,first=(st==start)):
   edges+=1
   if ns not in parent:
    parent[ns]=(st,x);depth[ns]=d+1;queue.append(ns)
  if len(parent)%10000<10:print('states',len(parent),'edges',edges,'depth',d,'seconds',round(time.monotonic()-t0,2),flush=True)
 result=dict(periods=periods,steps=len(hs),states=len(parent),edges=edges,complete=complete,
             seconds=time.monotonic()-t0,depth_counts=bydepth,accepted=accepted,witness_found=bool(accepted))
 return result

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--periods',type=int,default=2);ap.add_argument('--states',type=int,default=100000);ap.add_argument('--seconds',type=float,default=30);args=ap.parse_args()
 result=search(args.periods,args.states,args.seconds);print(json.dumps(result),flush=True)
 open(f'persist_wake_neutral_spacetime_{args.periods}_results.json','w').write(json.dumps(result,indent=2))
