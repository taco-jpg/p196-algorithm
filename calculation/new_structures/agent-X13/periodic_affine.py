#!/usr/bin/env python3
"""Exact symbolic normalization + pairing for affine-length PERIODIC runs.

The domain is the orthant k>=k0,l>=l0 (or any subset). Each run is
`pat[(offset+j) mod len(pat)]` of an affine integer length.
The program proves a comparison uniformly when its difference has
nonnegative coefficients and nonnegative intercept on the orthant.
Otherwise it rejects (never guesses a branch). Each residual finite pattern
comparison checks every residue which can occur inside that interval.
"""
from dataclasses import dataclass
from math import lcm
from affine_two_counter import Aff,Quadrant,Nonuniform,Z,ONE

@dataclass(frozen=True)
class Piece:
    pat:tuple
    length:Aff
    offset:Aff=Z
    def __init__(self,pat,length,offset=Z):
        if isinstance(pat,int):pat=(pat,)
        object.__setattr__(self,'pat',tuple(pat))
        object.__setattr__(self,'length',length)
        object.__setattr__(self,'offset',offset)
        assert self.pat

def literal(vals):return [Piece((x,),ONE) for x in vals]
def revpieces(ps):
    # Reverse a word whose each piece is pat[(offset+j) mod m].
    return [Piece(p.pat[::-1],p.length,Z-p.offset-p.length) for p in ps[::-1]]
def value(p,j,k,l):return p.pat[(p.offset.value(k,l)+j)%len(p.pat)]
def expand(ps,k,l):return [value(p,j,k,l) for p in ps for j in range(p.length.value(k,l))]
def total(ps):
    a=Z
    for p in ps:a=a+p.length
    return a

def effective_pat(p):
    m=len(p.pat)
    if p.offset.k%m or p.offset.l%m:
        raise Nonuniform(f'Piece offset {p.offset} phase depends on counters modulo {m}')
    return tuple(p.pat[(p.offset.c+i)%m] for i in range(m))

def compress(ps):
    out=[]
    for p in ps:
        if p.length==Z:continue
        if out and out[-1].pat==p.pat and out[-1].offset==Z and p.offset==Z and len(p.pat)==1:
            prev=out.pop();out.append(Piece(p.pat,prev.length+p.length))
        else:out.append(p)
    return out

def norm_symbolic(b,ps,G):
    c=0;out=[]
    for p in ps:
        m=len(p.pat)
        if p.length.k%m or p.length.l%m:
            raise Nonuniform(f'Run length {p.length} changes its final phase modulo {m}')
        rem=p.length.c%m
        bulk=p.length-Aff(c=rem)
        assert G.nonneg(bulk-Aff(c=m)),(p,G.kmin,G.lmin)
        w=effective_pat(p)
        first=[]
        for a in w:
            assert 0<=a<=2*(b-1)
            a+=c;first.append(a%b);c=a//b
        out+=literal(first)
        # Carry after one complete period is a fixed point; the final
        # incomplete period must still be handled with the proper carry.
        stabilized=[];cc=c
        for a in w:
            x=a+cc;stabilized.append(x%b);cc=x//b
        assert cc==c
        out.append(Piece(tuple(stabilized),bulk-Aff(c=m)))
        if rem:
            tail=[]
            for a in w[:rem]:
                x=a+c;tail.append(x%b);c=x//b
            out+=literal(tail)
    if c:out.append(Piece(c,ONE))
    return compress(out),c

def derive_pair(b,ps,G):
    ds,overflow=norm_symbolic(b,ps,G)
    out=zip_periodic(ds,revpieces(ds),G,lambda x,y:x+y)
    return out,overflow

def span_pat(p1,p2, n, G, combine):
    p=effective_pat(p1);q=effective_pat(p2);m=lcm(len(p),len(q))
    if n.k==n.l==0:count=min(m,n.c)
    elif G.nonneg(n-Aff(c=m)):count=m
    else:
        raise Nonuniform(f'Interval {n} may expose only partial periodic residues')
    vals=tuple(combine(p[i%len(p)],q[i%len(q)]) for i in range(count))
    return vals, count, m

def zip_periodic(xs,ys,G,combine):
    assert total(xs)==total(ys),(total(xs),total(ys))
    xs=list(xs);ys=list(ys);i=j=0;out=[]
    if xs: rx=xs[0].length; ox=xs[0].offset
    if ys: ry=ys[0].length; oy=ys[0].offset
    while i<len(xs) and j<len(ys):
        # The offset of the residual of each currently consumed piece.
        x=Piece(xs[i].pat,rx,ox);y=Piece(ys[j].pat,ry,oy)
        if G.le(rx,ry):
            n=rx; nxt=ry-rx;first='x'
        else:
            n=ry; nxt=rx-ry;first='y'
        if not G.nonneg(n):raise AssertionError(n)
        if n!=Z:
            vals,c,m=span_pat(x,y,n,G,combine)
            # A fixed short intersection is a literal; periodic interval
            # >= m is represented by an m-periodic block.
            if n.k==n.l==0 and n.c<m:
                out+=literal(vals)
            else:out.append(Piece(vals,n))
        if first=='x':
            i+=1;ry=nxt;oy=oy+n
            if i<len(xs):rx=xs[i].length;ox=xs[i].offset
            if ry==Z:
                j+=1
                if j<len(ys):ry=ys[j].length;oy=ys[j].offset
        else:
            j+=1;rx=nxt;ox=ox+n
            if j<len(ys):ry=ys[j].length;oy=ys[j].offset
        assert G.nonneg(rx) and G.nonneg(ry)
    assert i==len(xs) and j==len(ys)
    return compress(out)

def equal_symbolic(a,b,G):
    bad=[]
    def check(x,y):
        if x!=y:bad.append((x,y))
        return x
    zip_periodic(a,b,G,check)
    return not bad,bad[:4]

if __name__=='__main__':
    import random
    G=Quadrant(3,3)
    for _ in range(300):
        a=[random.randint(0,18) for i in range(random.randint(1,6))]
        b=[random.randint(0,18) for i in range(random.randint(1,6))]
        ps=literal(a)+[Piece(tuple(b),Aff(k=len(b),c=0))]+literal(a[::-1])
        try:ns,g=derive_pair(10,ps,G)
        except Nonuniform:continue
        for k in range(3,20):
            p=expand(ps,k,k);d=[];carry=0
            for v in p:
                x=v+carry;d.append(x%10);carry=x//10
            if carry:d.append(carry)
            t=[d[i]+d[-1-i] for i in range(len(d))]
            assert t==expand(ns,k,k),(k,p,t,expand(ns,k,k))
    print('random periodic symbolic tests PASS')
