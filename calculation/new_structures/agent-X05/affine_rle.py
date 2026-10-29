#!/usr/bin/env python3
"""X05 independent-counter affine run-length carry/pair engine.
A proof-producing *arithmetic* symbolic engine: each RLE run has length c+u*A+v*B.
All branch decisions are certified for the entire orthant A>=MIN_A,B>=MIN_B.
No approximation, random extrapolation or finite sampling is used for symbolic claims.
"""
from dataclasses import dataclass
from collections import Counter
import argparse,json,hashlib,random

@dataclass(frozen=True)
class L:
    c: int=0
    a: int=0
    b: int=0
    def __add__(s,t):
        if isinstance(t,int):return L(s.c+t,s.a,s.b)
        return L(s.c+t.c,s.a+t.a,s.b+t.b)
    def __sub__(s,t):
        if isinstance(t,int):return L(s.c-t,s.a,s.b)
        return L(s.c-t.c,s.a-t.a,s.b-t.b)
    def neg(s):return L(-s.c,-s.a,-s.b)
    def val(s,A,B):return s.c+s.a*A+s.b*B
    def tup(s):return (s.c,s.a,s.b)
ZERO=L()
ONE=L(1)

def positive(x,mina,minb):
    return x.a>=0 and x.b>=0 and x.val(mina,minb)>0

def sign(x,mina,minb):
    if x==ZERO:return 0
    if x.a>=0 and x.b>=0 and x.val(mina,minb)>=0:return 1
    if x.a<=0 and x.b<=0 and x.val(mina,minb)<=0:return -1
    raise ValueError('undecidable length ordering: '+str(x))

def add_word(w,v,k,mina,minb):
    if k==ZERO:return
    assert positive(k,mina,minb),(v,k)
    if w and w[-1][0]==v:w[-1]=(v,w[-1][1]+k)
    else:w.append((v,k))

def cat(parts,mina,minb):
    w=[]
    for v,k in parts:add_word(w,v,k,mina,minb)
    return w

def canon_digit_normalize(word,base,mina,minb):
    """Normalize arbitrary coefficient word, represented by symbolic affine runs.
    For non-neutral coefficients, carry becomes constant after first digit.
    """
    carry=0;dig=[]
    for value,length in word:
        assert 0<=value<=2*base-2
        if length==ONE:
            z=value+carry;add_word(dig,z%base,ONE,mina,minb);carry=z//base
        elif value==base-1:
            add_word(dig,(value+carry)%base,length,mina,minb)
            # carry fixed for base-1
        else:
            z=value+carry;cc=z//base
            add_word(dig,z%base,ONE,mina,minb)
            add_word(dig,(value+cc)%base,length-ONE,mina,minb)
            carry=cc
    if carry:add_word(dig,carry,ONE,mina,minb)
    # Canonical high digits must be nonzero: discard arbitrary trailing zero runs.
    while dig and dig[-1][0]==0:dig.pop()
    assert dig
    return dig

def paired(dig,mina,minb):
    """Zip least-significant-first and high-first digit RLE with symbolic lengths.
    Exact for every A,B in the orthant; unknown comparisons cause a hard failure.
    """
    left=list(dig); right=list(reversed(dig));i=j=0
    lo=left[0][1];hi=right[0][1];out=[];pal=True
    while i<len(left) and j<len(right):
        cmp=sign(lo-hi,mina,minb)
        if cmp<=0:use=lo
        else:use=hi
        assert positive(use,mina,minb)
        dl=left[i][0];dh=right[j][0]
        if dl!=dh:pal=False
        add_word(out,dl+dh,use,mina,minb)
        lo=lo-use;hi=hi-use
        if lo==ZERO:
            i+=1
            if i<len(left):lo=left[i][1]
        if hi==ZERO:
            j+=1
            if j<len(right):hi=right[j][1]
    assert i==len(left) and j==len(right)
    return out, pal

def symbolic_step(word,base,mina,minb):
    d=canon_digit_normalize(word,base,mina,minb)
    return (*paired(d,mina,minb), d)

def seed(mina,minb):
    # P(A,B) = 9^(A+1) 18^2 9^B 00 9^B 18^2 9^(A+1).
    return cat([(9,L(1,1,0)),(18,L(2)),(9,L(0,0,1)),
                (0,L(2)),(9,L(0,0,1)),(18,L(2)),(9,L(1,1,0))],mina,minb)

def expand(w,A,B):
    return [v for value,k in w for v in [value]*k.val(A,B)]

def ordinary_step(p,b=10):
    # Independent full-digit arithmetic, not using symbolic carry zipper.
    n=sum(x*pow(b,i) for i,x in enumerate(p))
    digs=[]
    while n: digs.append(n%b);n//=b
    if not digs:digs=[0]
    return [digs[i]+digs[~i] for i in range(len(digs))],digs

def independent_integer_step(p,b=10):
    n=0
    for x in reversed(p):n=n*b+x
    ss=[];q=n
    while q:ss.append(q%b);q//=b
    if not ss:ss=[0]
    rev=0
    for x in ss:rev=rev*b+x
    y=n+rev
    out=[]
    while y:out.append(y%b);y//=b
    return out

def coeff_digits(p,b=10):
    n=0
    for x in reversed(p):n=n*b+x
    out=[]
    while n:out.append(n%b);n//=b
    return out or [0]

def run(mina=1000,minb=1000,steps=150,checks=25,save=None,period=50):
    w=seed(mina,minb)
    controls=[(mina,minb),(mina+1,minb+4),(mina+17,minb+7),(mina+3,minb+23)]
    rows=[]
    for t in range(steps):
        try:nxt,pal,d=symbolic_step(w,10,mina,minb)
        except ValueError as e:
            print('STOP symbolic unorderable at t=',t,'reason=',str(e));break
        assert not pal,('palindrome possible',t)
        if t<checks or (period and t%period==0):
            for p in controls:
                actual=expand(w,*p)
                digit_out=ordinary_step(actual)[1]
                assert digit_out==expand(d,*p),(t,p,'digit mismatch')
                assert independent_integer_step(actual)==coeff_digits(expand(nxt,*p)),(t,p,'integer mismatch')
        counter=Counter((val,le.a,le.b) for val,le in nxt)
        row={'t':t,'rle_terms':len(nxt),'len_min':sum(le.val(mina,minb) for _,le in nxt),
             'palindrome':pal,'a_terms':sum(1 for v,le in nxt if le.a),
             'b_terms':sum(1 for v,le in nxt if le.b),
             'min_first':nxt[0][0],'min_last':nxt[-1][0]}
        rows.append(row)
        w=nxt
        if t and t%250==0:print("MILESTONE",t,"terms",len(w),"min_length",row["len_min"],"maxparams",max(max(abs(le.a),abs(le.b),abs(le.c)) for _,le in w),flush=True)
    summary={'label':'COMPUTED','scope':'all integers A>=MIN_A, B>=MIN_B independently',
             'MIN_A':mina,'MIN_B':minb,'certified_steps':len(rows),
             'distinct_parameter_counters':2,'integer_control_steps':checks,'controls':controls,
             'final_terms':len(w),'final_length':rows[-1]['len_min'] if rows else 0,
             'end_word':[[v,le.tup()] for v,le in w] if len(w)<200 else 'omitted',
             'rows':rows,'not_infinite':'No closed cycle or base-10 Lychrel certificate claimed'}
    print('CERTIFIED_STEPS',len(rows),'MAX_TERMS',max([r['rle_terms'] for r in rows] or [0]))
    print('FINAL',rows[-1] if rows else None)
    if save:
        with open(save,'w') as f:json.dump(summary,f,indent=2)
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--steps',type=int,default=150)
    p.add_argument('--min',type=int,default=1000);p.add_argument('--checks',type=int,default=25)
    p.add_argument('--save');p.add_argument('--period',type=int,default=50);a=p.parse_args()
    run(a.min,a.min,a.steps,a.checks,a.save,a.period)
