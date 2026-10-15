#!/usr/bin/env python3
"""General-base controls for the complementary-band exterior and quotient.

Nonneutral source phases are required. In odd bases, a target phase can become
neutral; this is a domain exit, not permission to reuse the reset formula.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from collections import Counter
import hashlib
import json
import random
from complementary_quotient import add, pair, strip_suffix, strip_prefix, strip_center

Word = tuple[int, ...]


def normalize(base: int, w: Word, e: int = 0) -> tuple[Word, int, int]:
    assert base >= 2 and e in (0, 1)
    out = []; total = 0
    for x in w:
        assert 0 <= x <= 2*(base-1)
        e, d = divmod(x+e, base)
        out.append(d); total += e
    return tuple(out), e, total


def phases(base: int) -> tuple[int, ...]:
    return tuple(c for c in range(1, 2*(base-1)) if c != base-1)


def exterior(base: int, c: int, B: Word) -> tuple[int, Word, int, int, int]:
    m = base-1; k = int(c >= base); t = c-m*k
    D, e, L = normalize(base, B)
    E, gamma, H = normalize(base, B[::-1], k)
    u = c+e-base*k
    raw = add(D+(u,), ((1,)+E[::-1]) if gamma else (E[::-1]+(t,)))
    Bp, strips = strip_suffix(raw, 2*t)
    correction = 2*k*len(B)+gamma*k-L-H
    return 2*t, Bp, gamma, correction, strips


def digits(base: int, n: int) -> Word:
    assert n > 0
    out = []
    while n:
        n,d = divmod(n,base); out.append(d)
    return tuple(out)


def value(base: int, w: Word) -> int:
    n=0
    for x in reversed(w): n=base*n+x
    return n


def reverse_add(base: int, n: int) -> int:
    return n+value(base,digits(base,n)[::-1])


def realize(base: int, q: Word) -> int:
    assert q and q[0] > 0 and q == q[::-1]
    m=base-1; d=[0]*len(q)
    for i in range(len(q)//2):
        d[-1-i]=min(m,q[i]); d[i]=q[i]-d[-1-i]
    if len(q)%2:
        assert q[len(q)//2]%2==0
        d[len(q)//2]=q[len(q)//2]//2
    assert all(0<=x<base for x in d) and d[-1]>0
    return value(base,tuple(d))


@dataclass(frozen=True)
class State:
    base: int
    c: int
    B: Word
    A: Word
    C: Word

    def word(self,g:int,h:int)->Word:
        assert g>=0 and h>=0
        d=2*(self.base-1)-self.c
        return self.B+(self.c,)*g+self.A+(d,)*h+self.C+(d,)*h+self.A[::-1]+(self.c,)*g+self.B[::-1]

    def weight(self)->int:
        return 2*len(self.B)+2*len(self.A)+len(self.C)


def transition(s:State)->tuple[State,int,int,int]:
    b,c,B,A,C=s.base,s.c,s.B,s.A,s.C
    assert c in phases(b)
    m=b-1; d=2*m-c; kc,kd=int(c>=b),int(d>=b)
    tc,td=c-m*kc,d-m*kd
    DB,e0,_=normalize(b,B,0); DA,e1,_=normalize(b,A,kc)
    DC,e2,_=normalize(b,C,kd); DRA,e3,_=normalize(b,A[::-1],kd)
    DRB,gamma,_=normalize(b,B[::-1],kc)
    u0,u1=c+e0-b*kc,d+e1-b*kd
    u2,u3=d+e2-b*kd,c+e3-b*kc
    if gamma:
        Br=add(DB+(u0,),(1,)+DRB[::-1])
        Ar=add(DA+(u1,),(u3,)+DRA[::-1]); Cr=pair(DC+(u2,))
    else:
        Br=add(DB+(u0,),DRB[::-1]+(tc,))
        Ar=add((tc,)+DA+(u1,),(u3,)+DRA[::-1]+(td,))
        Cr=pair((td,)+DC+(u2,))
    Bp,uB=strip_suffix(Br,2*tc); Ap,vA=strip_prefix(Ar,2*tc)
    Ap,uA=strip_suffix(Ap,2*td); Cp,vC=strip_center(Cr,2*td)
    target=State(b,2*tc,Bp,Ap,Cp)
    dg,dh=uB+vA-2+gamma,uA+vC-2+gamma
    assert target.weight()+2*dg+2*dh==s.weight()+gamma
    assert exterior(b,c,B)[:3]==(target.c,target.B,gamma)
    return target,dg,dh,gamma


def controls()->dict:
    rng=random.Random(196)
    records=[]
    for base in range(3,17):
        m=base-1; count=0; clock_paths=0; literal=0; neutral=0
        for c in phases(base):
            for size in range(3):
                for B in product(range(2*m+1),repeat=size):
                    if B and (B[0]==0 or B[-1]==c): continue
                    cp,Bp,g,K,_=exterior(base,c,B)
                    M,Mp=sum(B)-c*len(B),sum(Bp)-cp*len(Bp)
                    assert Mp==2*M-g*c+m*K
                    alt = lambda w: sum((-1)**i*x for i,x in enumerate(w))
                    J = 2*alt(B)+(-1)**len(B)*c
                    Jp = 2*alt(Bp)+(-1)**len(Bp)*cp
                    assert (Jp-(2*J if g==0 else 0))%(2*(base+1))==0
                    k=int(c>=base)
                    assert (-2*len(B)<=K<=0) if k==0 else (g<=K<=2*len(B)+g)
                    count+=1
                    if size<=1:
                        cc,BB,G=c,B,0
                        for t in range(24):
                            assert (2*(sum(BB)-cc*len(BB))+cc*G-2**(t+1)*M)%m==0
                            clock_paths+=1
                            if cc not in phases(base): break
                            cc,BB,g,_,_=exterior(base,cc,BB); G+=g
        for _ in range(500):
            c=rng.choice(phases(base))
            B=tuple(rng.randrange(2*m+1) for _ in range(rng.randrange(6)))
            if B and B[0]==0: B=(rng.randrange(1,2*m+1),)+B[1:]
            A=tuple(rng.randrange(2*m+1) for _ in range(rng.randrange(6)))
            half=tuple(rng.randrange(2*m+1) for _ in range(rng.randrange(4)))
            center=(2*rng.randrange(m+1),) if rng.randrange(2) else ()
            C=half+center+half[::-1]
            s=State(base,c,B,A,C); target,dg,dh,gamma=transition(s)
            neutral+=int(target.c==m)
            for g,h in ((2,2),(2,3),(3,2),(5,7)):
                q=s.word(g,h); n=realize(base,q)
                assert pair(digits(base,n))==q
                n1=reverse_add(base,n)
                assert pair(digits(base,n1))==target.word(g+dg,h+dh)
                ds=digits(base,n1); assert ds!=ds[::-1]
                literal+=1
        records.append({'base':base,'exterior_exact_controls':count,'alternating_controls':count,
                        'scaled_moment_path_checks':clock_paths,
                        'literal_quotient_checks':literal,'neutral_target_states':neutral})
    return {'seed':196,'bases':records,'status':'finite controls, not persistent-orbit evidence'}


def states(base:int,cap:int):
    m=base-1
    for c in phases(base):
        if c%2: continue
        d=2*m-c
        for blen in range(cap//2+1):
            Bs=[B for B in product(range(2*m+1),repeat=blen)
                if not B or (B[0]>0 and B[-1]!=c)]
            for alen in range((cap-2*blen)//2+1):
                As=[A for A in product(range(2*m+1),repeat=alen)
                    if not A or (A[0]!=c and A[-1]!=d)]
                for clen in range(cap-2*blen-2*alen+1):
                    Cs=[]
                    for half in product(range(2*m+1),repeat=clen//2):
                        if half and half[0]==d: continue
                        for middle in ([(2*x,) for x in range(m+1)] if clen%2 else [()]):
                            Cs.append(half+middle+half[::-1])
                    for B in Bs:
                        for A in As:
                            for C in Cs: yield State(base,c,B,A,C)


def bounded_full_graph(base:int,cap:int)->dict:
    assert base%2==0 and base>=4
    vertices=list(states(base,cap)); index={s:i for i,s in enumerate(vertices)}
    succ=[]; labels=[]
    for s in vertices:
        q,dg,dh,g=transition(s)
        j=index.get(q,-1)
        if j<0: assert q.weight()>cap
        succ.append(j); labels.append((dg,dh,g))
    done=set(); cycles=[]
    for root in range(len(vertices)):
        if root in done: continue
        path=[]; at={}; j=root
        while j>=0 and j not in done and j not in at:
            at[j]=len(path); path.append(j); j=succ[j]
        if j in at:
            cycle=path[at[j]:]
            Dg=sum(labels[i][0] for i in cycle); Dh=sum(labels[i][1] for i in cycle)
            G=sum(labels[i][2] for i in cycle)
            assert 2*(Dg+Dh)==G
            cycles.append({'period':len(cycle),'dg':Dg,'dh':Dh,'overflows':G,
                           'states':[[vertices[i].c,vertices[i].B,vertices[i].A,vertices[i].C] for i in cycle],
                           'labels':[labels[i] for i in cycle]})
        done.update(path)
    return {'base':base,'weight_cap':cap,'states':len(vertices),'internal_edges':sum(j>=0 for j in succ),
            'escape_edges':sum(j<0 for j in succ),'cycles':cycles,
            'status':'complete bounded graph; escaping paths unresolved'}


if __name__=='__main__':
    import sys
    result=controls() if len(sys.argv)==1 else bounded_full_graph(int(sys.argv[1]),int(sys.argv[2]))
    print(json.dumps(result,sort_keys=True))
