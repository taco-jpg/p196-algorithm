#!/usr/bin/env python3
"""Sound signature-quotient graph for base10 signed two-neutral bands.

Fix |A|=|E|=|B|=|D|=1; |M|=1..Mmax (default 3).
Trace: one -1/0/+1 move per L/R side of each of four runs, fixed order.
Every source digit option x,u is included implicitly. NOT all signed traces.
"""
import sys
from random import Random
from itertools import product
from collections import defaultdict,Counter,deque
from two_band import Phase,image_blocks,word,val
from signed_rewrite import Move,apply_moves,signed_edge

BASE=10
DELTA=(-1,0,1)
SP=defaultdict(list)
for l,r in product(DELTA,repeat=2):SP[l+r].append((l,r))
PAIRS=[(l,r,l2,r2,k) for k in sorted(SP) for l,r in SP[k] for l2,r2 in SP[k]]
assert len(PAIRS)==19

def pair_reps(m):
    if m==1:
        for v in range(10):yield (v,)
    if m==2:
        for t in range(19):
            a=min(9,t);yield (a,t-a)
    if m==3:
        for t in range(19):
            a=min(9,t)
            for v in range(10):yield (a,v,t-a)

def sums(M):
    return tuple(M[i]+M[-1-i] for i in range(len(M)))

def rep(s0,s1,M):
    a=max(1,s0-9)
    assert 1<=a<=9 and 0<=s0-a<=9
    b=min(9,s1)
    assert 0<=s1-b<=9
    return Phase((a,),(b,),M,(s1-b,),(s0-a,),0,9,0,9)

def signature(p):
    return (p.A[0]+p.E[0],p.B[0]+p.D[0],sums(p.M))

def build(Mmax=3):
    states=[];facts={}
    for s0 in range(1,19):
        for s1 in range(19):
            for m in range(1,Mmax+1):
                for M in pair_reps(m):
                    p=rep(s0,s1,M)
                    O,R,_=image_blocks(BASE,p)
                    if R[0]+R[3]!=9 or R[1]+R[2]!=9:continue
                    sig=(s0,s1,sums(M))
                    assert sig not in facts
                    facts[sig]=(O,R,p)
                    states.append(sig)
    idx={s:i for i,s in enumerate(states)}
    print('active_signatures',len(states),'Mmax',Mmax,flush=True)
    edges=[[] for _ in states]
    rejection=Counter()
    for i,sig in enumerate(states):
        O,R,p=facts[sig]
        for l0,r0,l3,r3,dg in PAIRS:
            for l1,r1,l2,r2,dh in PAIRS:
                moves=(Move(0,'L',l0),Move(0,'R',r0), Move(1,'L',l1),Move(1,'R',r1),
                       Move(2,'L',l2),Move(2,'R',r2),Move(3,'L',l3),Move(3,'R',r3))
                ret=apply_moves(O,R,moves)
                if ret is None:
                    rejection['badmove']+=1;continue
                blocks,off,need=ret
                assert off==(dg,dh,dh,dg)
                if (len(blocks[0]),len(blocks[1]),len(blocks[3]),len(blocks[4]))!=(1,1,1,1):
                    rejection['outwidth']+=1;continue
                mid=blocks[2]
                if not (1<=len(mid)<=Mmax):
                    rejection['midwidth']+=1;continue
                if blocks[0][0]==0:
                    rejection['zerolead']+=1;continue
                qs=(blocks[0][0]+blocks[4][0],blocks[1][0]+blocks[3][0],sums(mid))
                j=idx.get(qs)
                if j is None:
                    rejection['inactive_target']+=1;continue
                q=Phase(*blocks,R[0],R[3],R[1],R[2])
                if signed_edge(BASE,p,q,moves)!=(dg,dh,*need):
                    raise AssertionError((i,qs,moves))
                edges[i].append((j,dg,dh,need,moves,p,q))
    total=sum(map(len,edges))
    indeg=[0]*len(states)
    for row in edges:
        for j,*_ in row:indeg[j]+=1
    q=deque(i for i,k in enumerate(indeg) if k==0)
    dist=[0]*len(states);peeled=0
    while q:
        i=q.popleft();peeled+=1
        for j,*_ in edges[i]:
            if dist[j]<dist[i]+1:dist[j]=dist[i]+1
            indeg[j]-=1
            if indeg[j]==0:q.append(j)
    colors=bytearray(len(states));completed=0
    for root in range(len(states)):
        if colors[root]:continue
        colors[root]=1;stack=[(root,0)]
        while stack:
            v,k=stack[-1]
            if k==len(edges[v]):
                colors[v]=2;completed+=1;stack.pop();continue
            stack[-1]=(v,k+1);nxt=edges[v][k][0]
            if colors[nxt]==1:raise AssertionError('directed cycle found')
            if not colors[nxt]:colors[nxt]=1;stack.append((nxt,0))
    assert completed==len(states)
    cross=0
    for row in edges:
      for j,dg,dh,need,moves,p,qp in row:
        for x,u in ((0,0),(5,7),(9,9)):
            src=Phase(p.A,p.B,p.M,p.D,p.E,x,9-x,u,9-u)
            for g,h in ((3,4),(6,5)):
                w=word(src,g,h)
                assert val(BASE,w)+val(BASE,w[::-1])==val(BASE,word(qp,g+dg,h+dh))
                cross+=1
    print('signature_edges',total,'kahn_removed',peeled,'dfs_acyclic',True,
          'longest_path_edges',max(dist),'bigint_crosschecks',cross,'rejections',dict(rejection))
    return len(states),total,peeled,max(dist)


def equivalence_selftest(n=20000):
    rng=Random(0xA103C0DE)
    for _ in range(n):
        a=rng.randrange(1,10);e=rng.randrange(10)
        b=rng.randrange(10);d=rng.randrange(10)
        m=tuple(rng.randrange(10) for k in range(rng.randrange(1,4)))
        x=rng.randrange(10);u=rng.randrange(10)
        actual=Phase((a,),(b,),m,(d,),(e,),x,9-x,u,9-u)
        if len(m)==1:canonical=m
        elif len(m)==2:
            z=m[0]+m[1];k=min(9,z);canonical=(k,z-k)
        else:
            z=m[0]+m[2];k=min(9,z);canonical=(k,m[1],z-k)
        p=rep(a+e,b+d,canonical)
        assert signature(actual)==signature(p)
        assert image_blocks(BASE,actual)==image_blocks(BASE,p)
    print('random_signature_equivalence',n,'PASS',flush=True)

if __name__=='__main__':
    equivalence_selftest()
    build(int(sys.argv[1]) if len(sys.argv)>1 else 3)