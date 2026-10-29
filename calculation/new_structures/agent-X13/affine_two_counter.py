#!/usr/bin/env python3
"""Exact quadrant-uniform affine-run oracle for base-b reverse-and-add PAIRWORDS.

Coefficients P are least-significant-first, P=pair(N), so the next pairword is
pair(normalize_b(P)). A symbolic run v^(a*k+b*l+c) has an affine length.
For k>=K,l>=L, the checker accepts only if every segment is nonnegative and
all run-length comparisons are proved on the whole quadrant by coefficient
signs. It does not sample k/l to justify a symbolic equality.

The scope is deliberately smaller than a general Presburger verifier: for
undecidable comparisons it raises Nonuniform, never silently selects a side.
No Lean result and no infinite base-10 certificate are claimed.
"""
from dataclasses import dataclass
from itertools import product
import json
import random

@dataclass(frozen=True)
class Aff:
    k:int=0
    l:int=0
    c:int=0
    def __add__(self,x):
        if isinstance(x,int):x=Aff(c=x)
        return Aff(self.k+x.k,self.l+x.l,self.c+x.c)
    def __sub__(self,x):
        if isinstance(x,int):x=Aff(c=x)
        return Aff(self.k-x.k,self.l-x.l,self.c-x.c)
    def value(self,k,l):return self.k*k+self.l*l+self.c
    def __str__(self):return f"{self.k}*k+{self.l}*l+{self.c}"

@dataclass(frozen=True)
class Run:
    value:int
    length:Aff

class Nonuniform(Exception):pass

class Quadrant:
    def __init__(self,kmin=6,lmin=6):self.kmin=kmin;self.lmin=lmin;self.comparisons=0
    def nonneg(self,e):return e.k>=0 and e.l>=0 and e.value(self.kmin,self.lmin)>=0
    def pos(self,e):return e.k>=0 and e.l>=0 and e.value(self.kmin,self.lmin)>=1
    def le(self,a,b):
        self.comparisons+=1
        d=b-a
        if self.nonneg(d):return True
        if self.nonneg(a-b):return False
        raise Nonuniform(f"Cannot order {a} and {b} throughout k>={self.kmin}, l>={self.lmin}")

Z=Aff()
ONE=Aff(c=1)

def rle(seq):
    out=[]
    for run in seq:
        if run.length==Z:continue
        if out and out[-1].value==run.value:
            out[-1]=Run(run.value,out[-1].length+run.length)
        else:out.append(run)
    return out

def literal(seq):return [Run(x,ONE) for x in seq]

def expand(rs,k,l):
    a=[]
    for run in rs:
        n=run.length.value(k,l)
        assert n>=0
        a.extend([run.value]*n)
    return a

def total(rs):
    s=Z
    for r in rs:s=s+r.length
    return s

def norm_symbolic(base,src,guard):
    c=0;ds=[]
    for r in src:
        assert 0<=r.value<=2*(base-1) and guard.pos(r.length)
        head=r.value+c
        ds.append(Run(head%base,ONE))
        c=head//base
        # A constant coefficient block fixes its carry after one cell,
        # including neutral x=b-1 where the carry was already fixed.
        assert (r.value+c)//base == c
        ds.append(Run((r.value+c)%base,r.length-ONE))
    if c:ds.append(Run(c,ONE))
    return rle(ds),c

def zip_runs(xs,ys,guard,combine):
    assert total(xs)==total(ys),(total(xs),total(ys))
    xs=list(xs);ys=list(ys);i=j=0;out=[]
    if xs:rx=xs[0].length
    if ys:ry=ys[0].length
    while i<len(xs) and j<len(ys):
        if guard.le(rx,ry):
            n=rx; out.append(Run(combine(xs[i].value,ys[j].value),n))
            ry=ry-rx;i+=1
            if i<len(xs):rx=xs[i].length
            if ry==Z:
                j+=1
                if j<len(ys):ry=ys[j].length
        else:
            n=ry; out.append(Run(combine(xs[i].value,ys[j].value),n))
            rx=rx-ry;j+=1
            if j<len(ys):ry=ys[j].length
        # Nonzero lengths of source runs assured; difference may be zero on
        # quadrant boundary, which is legal, since this is affine equality.
        assert guard.nonneg(n) and guard.nonneg(rx) and guard.nonneg(ry)
    assert i==len(xs) and j==len(ys)
    return rle(out)

def step_symbolic(base,src,guard):
    ds,gamma=norm_symbolic(base,src,guard)
    new=zip_runs(ds,list(reversed(ds)),guard,lambda x,y:x+y)
    return new,gamma

ROWS=[
    ([10],8,0,[5,11],16,0,[8]),
    ([1,9],16,1,[13,7,9],14,1,[15,16]),
    ([3,9,13],14,2,[7,16,9,9],10,2,[12,14]),
    ([7,9,7],10,3,[9,16,13,0,0],2,2,[6,10]),
    ([14,18,15,1],2,4,[0,14,7,1,0],4,2,[13,0]),
    ([5,14,15,7,3],4,5,[2,5,12,8,1,4],8,2,[4]),
    ([11,9,11,15,6],8,5,[4,11,4,17,2,8],16,2,[8])]
# First phase even length; intermediate parity found directly from overflow.
PHASE_ODD=[False,True,True,True,True,False,False]

def half(t):
    left,u,a,middle,v,b,right=ROWS[t]
    return rle(literal(left)+[Run(u,Aff(k=1,c=-a))]+literal(middle)+
               [Run(v,Aff(l=1,c=-b))]+literal(right))

def full(t):
    h=half(t)
    if PHASE_ODD[t]:
        assert h[-1].length==ONE
        # Don't remove an arbitrary trailing run; last coefficient is always
        # a literal of length one (verify rle coalescing did not change this).
        assert h[-1].length==ONE,(t,h[-1]);second=h[:-1]
    else:second=h
    return rle(h+list(reversed(second)))

def check_rows(kmin=6,lmin=6):
    q=Quadrant(kmin,lmin);checks=[]
    for t in range(6):
        inp=full(t);goal=full(t+1)
        s,g=step_symbolic(10,inp,q)
        # Normalize the list of run boundaries without relying on the syntactic
        # shapes to match; comparator proves every matching interval.
        for run in goal:assert q.nonneg(run.length)
        mismatches=[]
        def eq(a,b):
            if a!=b:mismatches.append((a,b))
            return a
        zip_runs(s,goal,q,eq)
        assert not mismatches,(t,mismatches)
        assert g==[1,0,0,0,1,0][t],(t,g)
        checks.append({'edge':t,'gamma':g,'input_length':str(total(inp)),
                       'output_length':str(total(s)),'segments':len(s)})
    return {'status':'PAPER PROOF implemented by exact affine operations',
            'quadrant':{'k_min':kmin,'l_min':lmin},'edges':checks,
            'uniform_length_comparisons':q.comparisons}

def step_explicit(base,p):
    out=[];carry=0
    for v in p:
        a=v+carry;out.append(a%base);carry=a//base
    if carry:out.append(carry)
    return [out[i]+out[-1-i] for i in range(len(out))]

def seed_from_pairs(p,base):
    # Build genuine integer N with P_i=d_i+d_(n-1-i).
    assert p==p[::-1]
    out=[0]*len(p)
    for i in range(len(p)//2):
        a=p[i]
        out[i]=max(0,a-(base-1));out[-1-i]=min(base-1,a)
    if len(p)%2:
        assert p[len(p)//2]%2==0
        out[len(p)//2]=p[len(p)//2]//2
    assert out[-1]!=0
    return out

def next_digits(base,ds):
    x=[];carry=0
    for a,b in zip(ds,ds[::-1]):
        z=a+b+carry;x.append(z%base);carry=z//base
    if carry:x.append(carry)
    return x

def pair_digits(ds):return [ds[i]+ds[-1-i] for i in range(len(ds))]

def independent_replay(k,l):
    p=expand(full(0),k,l)
    ds=seed_from_pairs(p,10)
    assert pair_digits(ds)==p
    rows=[]
    for t in range(7):
        assert p==expand(full(t),k,l),(k,l,t)
        assert p==pair_digits(ds),(k,l,t,'ordinary integers')
        assert any(v%2 for v in p)
        rows.append({'time':t,'digits':len(ds),'first_pair':p[0],'central_pair':p[len(p)//2]})
        if t<6:
            nxt=next_digits(10,ds)
            assert pair_digits(nxt)==step_explicit(10,p)
            ds=nxt;p=pair_digits(ds)
    return rows

def main():
    cert=check_rows()
    trials=[(6,6),(6,100),(100,6),(27,101),(1000,537)]
    cert['independent_bigint_seed_checks']={f'{k},{l}':independent_replay(k,l) for k,l in trials}
    # Two mutually independent checks: next_digits uses actual digits,
    # step_explicit normalizes pair-coefficient values.
    print(json.dumps(cert,indent=2))

if __name__=='__main__':main()
