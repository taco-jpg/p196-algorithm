"""Generalize the exterior carry graph to any number of growth events.

Each segment ends in one new leading digit and has no earlier length increase.
State = segment-start left digits, known outgoing-left/incoming-right carry masks.
After reading one inward digit pair, the new left digits are the cyclic rotation
of segment outputs. For two segments this is exactly lychrel842's exterior graph.
A neutral-band accepting state repeats itself spatially with digit pair (0,b-1)
or (b-1,0), and complementary carry streams, for all time phases.
"""
from continuation_theory_graph import half
from collections import deque
import time,json,argparse

def transitions(base,periods,state,deadline=float('inf')):
    ls,lcs,rcs=state;q=len(periods)
    def visit(j,dr,lsout,lcnew,rcnew,rfirst):
        if time.monotonic()>deadline: raise TimeoutError
        if j==q:
            if dr==rfirst:
                ns=(tuple(lsout[-1:]+lsout[:-1]),tuple(lcnew),tuple(rcnew))
                yield ns,(ls[0],rfirst)
            return
        for dl1,dr1,lc1,rc1 in half(base,'E',ls[j],dr,lcs[j],rcs[j],periods[j]):
            yield from visit(j+1,dr1,lsout+[dl1],lcnew+[lc1],rcnew+[rc1],rfirst)
    for dr in range(base):yield from visit(0,dr,[],[],[],dr)

def neutral(base,periods,state):
    ls,lcs,rcs=state
    if ls[0] not in (0,base-1):return False
    if any(lc^rc != (1<<p)-1 for lc,rc,p in zip(lcs,rcs,periods)):return False
    dl,dr=ls[0],base-1-ls[0]
    for j,p in enumerate(periods):
        if dl!=ls[j]:return False
        for i in range(p):
            s=dl+dr
            dl=(s+((lcs[j]>>i)&1))%base
            dr=(s+((rcs[j]>>i)&1))%base
    return dl==ls[0] and dr==base-1-ls[0]

def predecessors(base,periods,state,deadline=float('inf')):
    """Exact inverse of one spatial transition, not inverse numeric iteration."""
    ls,lcs,rcs=state;q=len(periods)
    def visit(j,dr,lin,lold,rold,rfirst):
        if time.monotonic()>deadline:raise TimeoutError
        if j==q:
            if dr==rfirst:
                yield (tuple(lin),tuple(lold),tuple(rold)),(lin[0],rfirst)
            return
        desired=ls[(j+1)%q]
        for dl in range(base):
            for dl1,dr1,lc1,rc1 in half(base,'I',dl,dr,lcs[j],rcs[j],periods[j]):
                if dl1==desired:
                    yield from visit(j+1,dr1,lin+[dl],lold+[lc1],rold+[rc1],rfirst)
    for dr in range(base):yield from visit(0,dr,[],[],[],dr)

def backwards(base,periods,target,maxstates=20000,seconds=30):
    t=time.monotonic();deadline=t+seconds;q=len(periods)
    start=((1,)*q,tuple(1<<(p-1) for p in periods),(0,)*q)
    parent={target:None};queue=deque([target]);edges=0;complete=True;found=None
    try:
        while queue:
            if len(parent)>maxstates or time.monotonic()>deadline:
                complete=False;break
            st=queue.popleft()
            if st==start:
                found=[]
                while parent[st] is not None:
                    st,dp=parent[st];found.append(dp)
                break
            for prev,dp in predecessors(base,periods,st,deadline):
                edges+=1
                if prev not in parent:
                    parent[prev]=(st,dp);queue.append(prev)
    except TimeoutError:complete=False
    return dict(base=base,periods=periods,states=len(parent),edges=edges,
                complete=complete,seconds=round(time.monotonic()-t,3),path=found)

def path(parent,st,dp):
    result=[dp]
    while parent[st] is not None:
        st,dp=parent[st];result.append(dp)
    return list(reversed(result))

def search(base,periods,maxstates=100000,seconds=60):
    t=time.monotonic();deadline=t+seconds;q=len(periods)
    start=((1,)*q,tuple(1<<(p-1) for p in periods),(0,)*q)
    parent={start:None};queue=deque([start]);accept={};edges=0;complete=True
    try:
        while queue:
            if len(parent)>maxstates or time.monotonic()>deadline:
                complete=False;break
            st=queue.popleft()
            for ns,dp in transitions(base,periods,st,deadline):
                edges+=1
                if neutral(base,periods,ns) and ns not in accept:
                    accept[ns]=path(parent,st,dp)
                if ns not in parent:
                    parent[ns]=(st,dp);queue.append(ns)
    except TimeoutError:complete=False
    return dict(base=base,periods=periods,states=len(parent),edges=edges,
                complete=complete,seconds=round(time.monotonic()-t,3),
                accepted=[dict(state=k,path=v) for k,v in accept.items()])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=int,default=10)
    ap.add_argument('--periods',type=int,nargs='+',default=[2]*12)
    ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--states',type=int,default=100000)
    a=ap.parse_args();print(json.dumps(search(a.base,a.periods,a.states,a.seconds)),flush=True)
