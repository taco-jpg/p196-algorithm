#!/usr/bin/env python3
"""Two-independent-neutral-band pumping format (PAPER soundness; COMPUTED tests).

Not a base-10 certificate and not kernel-verified. For phases with valid nonzero
leading digit, the tested edge checker is SUFFICIENT for all g,h>=0, not merely
for the finite sample g,h used in tests.
"""
from dataclasses import dataclass
from itertools import product
from random import Random

@dataclass(frozen=True)
class Phase:
    A: tuple
    B: tuple
    M: tuple
    D: tuple
    E: tuple
    x: int
    y: int
    u: int
    v: int


def valid_phase(b,p):
    blocks=(p.A,p.B,p.M,p.D,p.E)
    return (b>=2 and bool(p.A) and p.A[0]>0 and len(p.A)==len(p.E)
      and len(p.B)==len(p.D) and p.x+p.y==b-1 and p.u+p.v==b-1
      and all(isinstance(z,int) and 0<=z<b for W in blocks for z in W)
      and all(0<=z<b for z in (p.x,p.y,p.u,p.v)))


def word(p,g,h):
    assert g>=0 and h>=0
    return (p.A+(p.x,)*g+p.B+(p.u,)*h+p.M+
            (p.v,)*h+p.D+(p.y,)*g+p.E)


def val(b,s):
    n=0
    for c in s:n=n*b+c
    return n


def add_fixed(b,S,T,carry):
    assert len(S)==len(T) and carry in (0,1)
    width=len(S)
    n=val(b,S)+val(b,T)+carry
    assert n//(b**width)<=1
    out=[0]*width
    for i in range(width-1,-1,-1):out[i]=n%b;n//=b
    return tuple(out),n


def image_blocks(b,p):
    assert valid_phase(b,p)
    R0,c1=add_fixed(b,p.E,p.A[::-1],0)
    R1,c2=add_fixed(b,p.D,p.B[::-1],c1)
    R2,c3=add_fixed(b,p.M,p.M[::-1],c2)
    R3,c4=add_fixed(b,p.B,p.D[::-1],c3)
    R4,c5=add_fixed(b,p.A,p.E[::-1],c4)
    z=b-1
    fixed=((1,)*c5+R4,R3,R2,R1,R0)
    runs=(z*(1-c4),z*(1-c3),z*(1-c2),z*(1-c1))
    return fixed,runs,(c1,c2,c3,c4,c5)


def image_word(b,p,g,h):
    fixed,runs,_=image_blocks(b,p)
    O0,O1,O2,O3,O4=fixed
    x,u,v,y=runs
    return O0+(x,)*g+O1+(u,)*h+O2+(v,)*h+O3+(y,)*g+O4


def edgeOK(b,p,q,dg,dh):
    """A finite free-monoid cut witness guarantees all-length identity."""
    if not (valid_phase(b,p) and valid_phase(b,q) and
            isinstance(dg,int) and isinstance(dh,int) and 0<=dg<=10 and 0<=dh<=10):
        return False
    F,R,carry=image_blocks(b,p)
    x,u,v,y=R
    if (x,u,v,y)!=(q.x,q.u,q.v,q.y):return False
    O0,O1,O2,O3,O4=F
    for a0 in range(dg+1):
      a1=dg-a0
      for d0 in range(dg+1):
        d1=dg-d0
        if O0 != q.A+(x,)*a0 or O4 != (y,)*d1+q.E:continue
        for b0 in range(dh+1):
          b1=dh-b0
          if not O1==(x,)*a1+q.B+(u,)*b0:continue
          for c0 in range(dh+1):
            c1=dh-c0
            if O2==(u,)*b1+q.M+(v,)*c0 and O3==(v,)*c1+q.D+(y,)*d0:
                return True
    return False


def cycleOK(b,phases,deltas):
    """Paper-sound nonpalindrome pumping format, NOT a Lean-verified theorem."""
    if not phases or len(phases)!=len(deltas):return False
    if not all(valid_phase(b,p) and p.A[0]!=p.E[-1] for p in phases):return False
    if not all(isinstance(dg,int) and isinstance(dh,int) and dg>=0 and dh>=0
               for dg,dh in deltas):return False
    if sum(dg+dh for dg,dh in deltas)==0:return False
    return all(edgeOK(b,phases[i],phases[(i+1)%len(phases)],*deltas[i])
               for i in range(len(phases)))


def rand_phase(rng,b):
    a=rng.randint(1,4);d=rng.randint(0,4);m=rng.randint(0,5)
    rr=lambda n:tuple(rng.randrange(b) for _ in range(n))
    A=(rng.randrange(1,b),)+rr(a-1)
    x=rng.randrange(b);u=rng.randrange(b)
    return Phase(A,rr(d),rr(m),rr(d),rr(a),x,b-1-x,u,b-1-u)


def selftest(trials=12000):
    rng=Random(0x1962BAAD)
    counts={}
    for i in range(trials):
        b=(2,3,4,8,10,11,17,26,32)[i%9]
        p=rand_phase(rng,b)
        g=rng.randrange(0,30);h=rng.randrange(0,30)
        if i%97==0:g+=100;h+=110
        w=word(p,g,h)
        got=val(b,image_word(b,p,g,h))
        expected=val(b,w)+val(b,w[::-1])
        assert got==expected,(i,b,p,g,h,got,expected)
        counts[b]=counts.get(b,0)+1
    print('two_band_bigint_crosschecks',trials,'PASS','by_base',counts)
    positive=0
    for i in range(100000):
        b=10
        p=rand_phase(rng,b)
        O,R,c=image_blocks(b,p)
        if c[-1]!=0:continue
        x,u,v,y=R
        if x+y!=b-1 or u+v!=b-1:continue
        if not O[0] or not O[0][0]:continue
        q=Phase(O[0],O[1],O[2],O[3],O[4],x,y,u,v)
        if not valid_phase(b,q):continue
        assert edgeOK(b,p,q,0,0)
        assert not edgeOK(b,p,q,1,0)
        for g,h in product((0,1,3,17),(0,2,7)):
            assert val(b,word(q,g,h))==val(b,word(p,g,h))+val(b,word(p,g,h)[::-1])
        positive+=1
        if positive==5:break
    assert positive==5
    print('synthetic_valid_phase_transitions',positive,'PASS')
    print('NO BASE-10 CYCLE CLAIMED')

if __name__=='__main__':selftest()
