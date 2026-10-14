"""Exact finite-state closure of the public-domain lychrel842 search.

Unlike its depth-bounded Haskell tree, visit each carry/digit state once.
This decides arbitrary WIDTH within the original two-growth neutral-band ansatz,
for fixed base and half-periods. It is not a decision procedure for Lychrel numbers.
Original source preserved in continuation_theory_primary/search.hs.
Fixed source calcConn's second-half use of first-half carry vectors.
"""
from functools import lru_cache
from collections import deque
import argparse, json, time

@lru_cache(None)
def half(base, side, dl, dr, lc, rc, p):
    # E: known left-output, right-input. I: known left-input, right-output.
    paths=[(dl,dr,0,0)]
    for i in range(p):
        nxt=[]; l=(lc>>i)&1; r=(rc>>i)&1
        for a,b,x,y in paths:
            s=a+b
            for u in (0,1):
                li,ri=(u,r) if side=='E' else (l,u)
                al,lo=divmod(s+li,base)[1],(s+li)//base
                ar,ro=divmod(s+ri,base)[1],(s+ri)//base
                if (lo==l if side=='E' else ro==r):
                    xx,yy=(li,ro) if side=='E' else (lo,ri)
                    nxt.append((al,ar,x|(xx<<i),y|(yy<<i)))
        paths=nxt
        if not paths: break
    return tuple(paths)

def connector(base, adl, mdl, ac, ar, bc, br, pa,pb):
    if adl not in (0,base-1): return None
    if ac^ar != (1<<pa)-1 or bc^br != (1<<pb)-1: return None
    x=adl; y=base-1-adl
    for i in range(pa):
        s=x+y; x=(s+((ac>>i)&1))%base; y=(s+((ar>>i)&1))%base
    if x!=mdl: return None
    for i in range(pb):
        s=x+y; x=(s+((bc>>i)&1))%base; y=(s+((br>>i)&1))%base
    if x!=adl: return None
    return (adl,ac,bc)

def transitions(base,pa,pb,side,state):
    x,y,acl,acr,bcl,bcr=state
    if side=='E':
        for ar0 in range(base):
            for al1,ar1,alc,arc in half(base,'E',x,ar0,acl,acr,pa):
                for bl1,br1,blc,brc in half(base,'E',y,ar1,bcl,bcr,pb):
                    if br1!=ar0: continue
                    ns=(bl1,al1,alc,arc,blc,brc)
                    con=connector(base,bl1,al1,alc,arc,blc,brc,pa,pb)
                    yield ns,(x,ar0),con
    else:
        for al0 in range(base):
            for al1,ar1,alc,arc in half(base,'I',al0,x,acl,acr,pa):
                if al1!=y: continue
                for bl0 in range(base):
                    for bl1,br1,blc,brc in half(base,'I',bl0,ar1,bcl,bcr,pb):
                        if bl1!=al0: continue
                        ns=(br1,bl0,alc,arc,blc,brc)
                        con=connector(base,base-1-br1,bl0,alc,arc,blc,brc,pa,pb)
                        yield ns,(al0,x),con

def heads(base,pa,pb,side):
    if side=='E': return [(1,1,1<<(pa-1),0,1<<(pb-1),0)]
    res=[]
    for d in range(base):
        for ac in range(1<<pa):
            for bc in range(1<<pb):
                x=d; cs=0
                for i in range(pb):
                    s=2*x+((bc>>i)&1); x=s%base; cs|=(s//base)<<i
                res.append((x,d,ac,ac,cs,bc))
    return res

def path_to(parent,state,dp):
    path=[dp]
    while parent[state] is not None:
        prev,pair=parent[state];path.append(pair);state=prev
    return list(reversed(path))

def search(base,pa,pb,side,maxstates=1000000,maxtime=120):
    t=time.monotonic(); hs=heads(base,pa,pb,side)
    parent={x:None for x in hs}; queue=deque(hs); accepted={}; edges=0; complete=True
    while queue:
        if len(parent)>maxstates or time.monotonic()-t>maxtime:
            complete=False;break
        st=queue.popleft()
        for ns,dp,con in transitions(base,pa,pb,side,st):
            edges+=1
            if con is not None and con not in accepted:
                accepted[con]=path_to(parent,st,dp)
            if ns not in parent:
                parent[ns]=(st,dp);queue.append(ns)
    return dict(base=base,pa=pa,pb=pb,side=side,states=len(parent),edges=edges,
                complete=complete,seconds=round(time.monotonic()-t,3),
                accepted=[dict(conn=k,path=v) for k,v in accepted.items()])

def numeral(digits):
    abc='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    return ''.join(abc[d] for d in digits)

def construct(base,ext,intl,gap=0):
    e=ext['path'];i=intl['path'];a=ext['conn'][0]
    el=[x for x,y in e];er=[y for x,y in reversed(e)]
    il=[x for x,y in reversed(i)];ir=[y for x,y in i]
    return el+[a]*gap+il+ir+[base-1-a]*gap+er

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--base',type=int,default=10)
    ap.add_argument('--pa',type=int,default=4);ap.add_argument('--pb',type=int,default=4)
    ap.add_argument('--side',choices=['E','I','both'],default='both')
    ap.add_argument('--seconds',type=float,default=120)
    ap.add_argument('--states',type=int,default=1000000)
    args=ap.parse_args()
    for side in ('E','I') if args.side=='both' else (args.side,):
        r=search(args.base,args.pa,args.pb,side,args.states,args.seconds)
        print(json.dumps(r),flush=True)
