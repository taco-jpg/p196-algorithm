#!/usr/bin/env python3
"""Exact coefficient-band normalization and rational-polynomial reverse/add checking."""
from fractions import Fraction
from collections import defaultdict
import sys
sys.set_int_max_str_digits(0)

B=(17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13)
W=(17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13)
V=(4,4,14,1,5,11,7,1,15,12,7,9,9,12,14,4,0,6,5,17,13,9,7,3,13,10,4,13,5,1,9,4,11,6,16,3,7,7,12,4,2,13,2,15,10,10,9,3)

def source(k):
    h=B+W*k+(9,)+V*k
    return h+(9,)+h[::-1]

def nblock(xs, cin):
    out=[]
    for x in xs:
        y=x+cin
        out.append(y%10)
        cin=y//10
        assert 0<=cin<=1
    return tuple(out),cin

def normalize_affine(segs, coefficient_repeat_offset=0):
    # Output digit blocks in least-significant-first order: (word, a, c) means word^(a*q+c).
    out=[]; c=0
    for word,a in segs:
        if a==0:
            d,c=nblock(word,c)
            out.append((d,0,1))
        else:
            first,nc=nblock(word,c)
            later,st=nblock(word,nc)
            assert st==nc,('band carry is not stationary after first copy',word,c,nc,st)
            out.append((first,0,1))
            out.append((later,a,coefficient_repeat_offset-1))
            c=nc
    if c:out.append(((c,),0,1))
    return out

def expand(segs,k):
    z=()
    for w,a,c in segs:
        count=a*k+c
        assert count>=0
        z+=w*count
    return z

def eval_digit_word(w):
    n=0
    for v in reversed(w):n=n*10+v
    return n

def poly_add(A,B):
    z=defaultdict(Fraction,A)
    for j,v in B.items():z[j]+=v
    return {j:v for j,v in z.items() if v}

def poly_word_ls(segments):
    # Exact expansion in X=10^q. Coefficients may be rational.
    p={}; offset=Fraction(1); exponent=0
    for w,a,c in segments:
        assert c>=0 or a>0
        m=len(w);val=eval_digit_word(w)
        scale=Fraction(10)**(m*c)
        r=Fraction(val,10**m-1)
        p=poly_add(poly_add(p,{exponent+m*a:r*offset*scale}),{exponent:-r*offset})
        offset*=scale
        exponent+=m*a
    return p

def reverse_segments(segs):
    return [(w[::-1],a,c) for w,a,c in reversed(segs)]

def poly_value_at(P,k):
    X=10**k
    q=sum((v*X**j for j,v in P.items()),Fraction())
    assert q.denominator==1
    return q.numerator

def derive_template(p0,p1,p2,kmin,blen,vshift):
    # Infer one step's candidate affine templates from three ordinary-digit trajectories.
    def parse(p,k):
        h=p[:len(p)//2]
        middle=p[len(p)//2:len(p)//2+(len(p)%2)]
        vi=20*k+vshift
        a=h[:blen]
        w=h[blen:blen+20*(k-kmin)]
        j=h[blen+20*(k-kmin):vi]
        v=h[vi:vi+48*(k-kmin)]
        c=h[vi+48*(k-kmin):]
        return a,w,j,v,c,middle
    a0,w0,j0,v0,c0,z0=parse(p0,kmin)
    a1,w1,j1,v1,c1,z1=parse(p1,kmin+1)
    a2,w2,j2,v2,c2,z2=parse(p2,kmin+2)
    if not (a0==a1==a2 and j0==j1==j2 and c0==c1==c2
            and z0==z1==z2 and w1*2==w2 and v1*2==v2):
        return None
    return (a0,w1,j0,v1,c0,z0)

def symbolic_from_template(tpl):
    a,w,j,v,c,center=tpl
    p=[(a,0),(w,1),(j,0),(v,1),(c,0)]
    if center:p.append((center,0))
    p += [(c[::-1],0),(v[::-1],1),(j[::-1],0),(w[::-1],1),(a[::-1],0)]
    # q=0 corresponds to k=kmin+1. Every variable block appears q+1 times.
    return normalize_affine(p,coefficient_repeat_offset=1)

def original_source_poly(kmin):
    base=kmin+1
    seg=[(B,0,1),(W,1,base),((9,),0,1),(V,1,base),((9,),0,1),
         (V[::-1],1,base),((9,),0,1),(W[::-1],1,base),(B[::-1],0,1)]
    return poly_word_ls(seg)
