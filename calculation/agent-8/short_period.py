#!/usr/bin/env python3
"""Independent time-first column transfer for exact periodic B-only cycles.

Computes a necessary all-exterior-width automaton for specified g time-word.
No actual center C is assumed. A returned ACCEPT is B-side only.
"""
import argparse
from collections import deque


def possible_successors(state, g, first=False):
    p=len(g)
    L,H,Y=state
    idx=[];j=0
    for v in g:
        idx.append(j if v else None)
        j+=int(bool(v))
    successors=set()
    for x0 in range(1 if first else 0,19):
        xs=[0]*p; hn=[0]*p
        def rec(t,x):
            if t==p:
                if x==x0:
                    nxtL=tuple((xs[i]+L[i])//10 for i in range(p))
                    nxtY=tuple((xs[i]+hn[i])%10 for i in range(p) if g[i])
                    successors.add((nxtL,tuple(hn),nxtY))
                return
            xs[t]=x
            for c in (0,1):
                if (x+c)//10 != H[t]: continue
                hn[t]=c
                lowdigit=(x+L[t])%10
                partner=Y[idx[t]] if g[t] else (x+c)%10
                nx=lowdigit+partner
                rec(t+1,nx)
        rec(0,x0)
    return successors


def accepting(state,g):
    L,H,Y=state
    return all(l+h==1 for l,h in zip(L,H)) and all(Y[j]==9*L[i] for j,i in enumerate(k for k,v in enumerate(g) if v))


def solve(g, cap=300000):
    p=len(g)
    start=((0,)*p,tuple(g),(1,)*sum(g))
    seen={start};frontier={start}
    depth=0;totalarc=0
    while frontier:
        new=set()
        for state in frontier:
            if accepting(state,g):
                return ('ACCEPT',depth,len(seen),totalarc,state)
            dst=possible_successors(state,g,first=(depth==0))
            totalarc+=len(dst)
            new.update(dst-seen)
        seen.update(new)
        if len(seen)>cap: return ('CAPPED',depth,len(seen),totalarc,None)
        frontier=new;depth+=1
        if depth>450: return ('DEPTH-CAPPED',depth,len(seen),totalarc,None)
    return ('EXHAUSTED',depth,len(seen),totalarc,None)


def main():
    a=argparse.ArgumentParser()
    a.add_argument('--pmin',type=int,default=1)
    a.add_argument('--pmax',type=int,default=5)
    a.add_argument('--necklace',action='store_true')
    a.add_argument('--g',default=None)
    a.add_argument('--cap',type=int,default=300000)
    args=a.parse_args()
    cases=[]
    if args.g:
        cases=[tuple(int(c) for c in args.g)]
    else:
        for p in range(args.pmin,args.pmax+1):
            for w in range(1<<p):
                g=tuple((w>>t)&1 for t in range(p))
                if not args.necklace or g==min(g[j:]+g[:j] for j in range(p)):
                    cases.append(g)
    summaries={};states=0
    for g in cases:
        label=''.join(map(str,g))
        status,depth,num,arc,wit=solve(g,args.cap)
        summaries[status]=summaries.get(status,0)+1
        states+=num
        print(f'p={len(g)} g={label} status={status} depth={depth} states={num} explored_arcs={arc}',flush=True)
        if status=='ACCEPT': print('  accepting interface:',wit)
    print('SUMMARY',summaries,'total_states_by_word',states)

if __name__=='__main__':main()