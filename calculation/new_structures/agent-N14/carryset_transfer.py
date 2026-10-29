#!/usr/bin/env python3
"""Set-valued carry boundary and exact single-column temporal transfer."""
from pathlib import Path
def read(name='p39_k12.txt'):
    a=dict(s.split('=',1) for s in Path(__file__).with_name(name).read_text().strip().splitlines())
    return a['gamma'],[list(map(int,r.split(','))) for r in a['rows'].split(';')]
def contracts(g,rows):
    p=len(g);K=len(rows[0]);allowed=[];L=[]
    assert len(rows)==p
    for t,x in enumerate(rows):
        lo=[0]*K
        for j in range(1,K):lo[j]=(x[j-1]+lo[j-1])//10
        L.append((x[-1]+lo[-1])//10)
        opts=[]
        for upper in (0,1):
            high=[0]*K;high[-1]=upper
            for j in range(K-1,0,-1):high[j-1]=(x[j]+high[j])//10
            gam=(x[0]+high[0])//10
            if gam!=int(g[t]):continue
            nextrow=[]
            for j in range(K):
                partner=(1 if j==0 else (x[j-1]+high[j-1])%10) if gam else (x[j]+high[j])%10
                nextrow.append((x[j]+lo[j])%10+partner)
            if nextrow==rows[(t+1)%p]:opts.append(upper)
        allowed.append(tuple(opts))
    return allowed,L
def next_states(g,rows,A,L,t,states):
    j=t%len(g);r=set()
    for z in states:
        for v in (0,1):
            u=(z+v)//10
            if u not in A[j]:continue
            part=(rows[j][-1]+u)%10 if g[j]=='1' else (z+v)%10
            r.add((z+L[j])%10+part)
    return r
def horizon(g,rows):
    A,L=contracts(g,rows)
    if not all(A):return 0,False
    states=set(range(19));seen=set()
    for t in range(19*len(g)*524288+1):
        key=(t%len(g),frozenset(states))
        if key in seen:return t,True
        seen.add(key)
        states=next_states(g,rows,A,L,t,states)
        if not states:return t+1,False
    raise RuntimeError('Unexpected transfer bound')
if __name__=='__main__':
    g,rows=read()
    A,L=contracts(g,rows)
    assert all(A)
    assert sum(len(x)==2 for x in A)==14
    t,infinite=horizon(g,rows)
    assert (t,infinite)==(13,False),(t,infinite)
    print('PASS exact all-carry transfer; width-13 extension expires at transition 13')
