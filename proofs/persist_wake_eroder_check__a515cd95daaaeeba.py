"""Independent Python replay of the filtered finite-time center automaton."""
from persist_wake_neutral_spacetime import setup,center_head
from collections import deque
import json,time


def transitions_filtered(state,stage,hs,index,first=False,target_value=None,first_value=None):
 lm,rm,prev=state;T=len(hs)
 def visit(t,q,nlm,nrm,digits,j):
  if t==11 and stage<max(3,index+1):
   if stage<index and q!=9:return
   if stage==index and q==9:return
   if stage==index and target_value is not None and q!=target_value:return
  if t==T:
   yield (nlm,nrm,tuple(digits));return
  l=(lm>>t)&1;r=(rm>>t)&1
  z=q+l;lo=z%10;lc=z//10
  for b in (0,1):
   z=q+b
   if z//10!=r:continue
   hi=z%10
   if hs[t]:yield from visit(t+1,lo+prev[j],nlm|(lc<<t),nrm|(b<<t),digits+[hi],j+1)
   else:yield from visit(t+1,lo+hi,nlm|(lc<<t),nrm|(b<<t),digits,j)
 for initial in range(19):
  if first and initial==9:continue
  if first and first_value is not None and initial!=first_value:continue
  yield from visit(0,initial,0,0,[],0)


def verify(index,maxstates=500000,target_value=None,first_value=None):
 hs,pos,start=setup(2);start=(start,0)
 seen={start};queue=deque([start]);edges=0;heads=0;t0=time.monotonic()
 while queue:
  if len(seen)>maxstates:break
  state,stage=queue.popleft()
  if center_head(state,hs)is not None:heads+=1
  for ns in transitions_filtered(state,stage,hs,index,stage==0,target_value,first_value):
   edges+=1;node=(ns,min(max(3,index+1),stage+1))
   if node not in seen:seen.add(node);queue.append(node)
 return dict(index=index,target_value=target_value,first_value=first_value,states=len(seen),edges=edges,heads=heads,
             complete=not queue,seconds=time.monotonic()-t0)

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--all',action='store_true');args=ap.parse_args()
 results=[]
 for index in (0,2):
  row=verify(index);results.append(row);print(json.dumps(row),flush=True)
 assert[(r['states'],r['edges'],r['heads'],r['complete'])for r in results]==[(6273,6272,0,True),(228061,312252,0,True)]
 open('persist_wake_eroder_partial_certificate.json','w').write(json.dumps(results,indent=2))
 if args.all:
  compensation=[]
  for value in (10,11,12,13,15,16,17,18):
   row=verify(1,target_value=value);compensation.append(row);print(json.dumps(row),flush=True)
  row=verify(1,first_value=14);compensation.append(row);print(json.dumps(row),flush=True)
  assert[(r['states'],r['edges'],r['heads'],r['complete'])for r in compensation]==[(45,44,0,True)]*4+[(172077,248108,0,True),(589,588,0,True),(461,460,0,True),(45,44,0,True),(5,4,0,True)]
  open('persist_wake_eroder_compensation_certificate.json','w').write(json.dumps(compensation,indent=2))
  row=verify(3,first_value=14);print(json.dumps(row),flush=True)
  assert(row['states'],row['edges'],row['heads'],row['complete'])==(4843,4846,0,True)
  open('persist_wake_eroder_strict_certificate.json','w').write(json.dumps(row,indent=2))
