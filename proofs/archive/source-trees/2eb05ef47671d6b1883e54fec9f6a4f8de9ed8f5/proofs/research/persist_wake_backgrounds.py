from persist_wake_clock_search import step
import json

def search(background,maxdepth):
 found=[]
 for x in range(19):
  if x==background:continue
  frontier=[('',{((x,),background,0)})]
  for t in range(maxdepth):
   nxt=[]
   for clock,states in frontier:
    for h in (0,1):
     key=clock+str(h)
     if '1111' in key:continue
     new=step(states,h)
     if new is None:continue
     nxt.append((key,new))
     if '0' in key and all(q[-1]==x and u==background for q,u,d in new):
      ds={d for q,u,d in new};growth=key.count('1')
      if max(ds)<=growth:
       row=dict(background=background,x=x,clock=key,shift=sorted(ds),growth=growth,states=len(new))
       found.append(row)
   frontier=nxt
  print('background',background,'terminal',x,'candidates',len(found),flush=True)
 return found

if __name__=='__main__':
 results=[]
 for b in (0,2,18):results.extend(search(b,8))
 print('RESULT',json.dumps(results,indent=2))
 open('persist_wake_backgrounds_results.json','w').write(json.dumps(results,indent=2))
