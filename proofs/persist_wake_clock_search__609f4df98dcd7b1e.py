"""Universal front return checks for prescribed, not necessarily alternating clocks."""
from resume_history_search_front import update_suffix
import json


def step(states,h):
    new=set()
    for q,u,d in states:
        for c in (0,1):
            out,nu,move=update_suffix(q,u,h,c)
            if not out:return None
            new.add((out,nu,d+move))
    return new


def explore(depth):
    frontier=[('',{((8,),6,0)})];found=[]
    for t in range(depth):
        nxt=[]
        for clock,states in frontier:
            for h in (0,1):
                new=step(states,h)
                if new is None:continue
                key=clock+str(h);nxt.append((key,new))
                if (t+1)%2==0 and all(q[-1]==8 and u==6 for q,u,d in new):
                    ds={d for q,u,d in new};growth=key.count('1')
                    row=dict(clock=key,shift=sorted(ds),growth=growth,
                             buffer_drift=[growth-d for d in sorted(ds)],states=len(new))
                    found.append(row)
                    if max(ds)<=growth:print('candidate',row,flush=True)
        frontier=nxt
        print('depth',t+1,'clocks',len(frontier),'totalstates',sum(len(s) for _,s in frontier),'renewals',len(found),flush=True)
    return found

if __name__=='__main__':
    result=explore(12)
    open('persist_wake_clock_search_results.json','w').write(json.dumps(result,indent=2))
