#!/usr/bin/env python3
"""Exact symbolic folded-pairword verifier for two independent affine band counts.
Refuses any interval ordering or period phase not provable uniformly.
No finite number of samples constitutes a proof. Coefficients are LSD-first.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import lcm
from typing import Tuple
import argparse, json, pathlib

@dataclass(frozen=True)
class E:
    q:int=0; k:int=0; c:int=0
    def __add__(self,o):
        if isinstance(o,int):o=E(c=o)
        return E(self.q+o.q,self.k+o.k,self.c+o.c)
    __radd__=__add__
    def __neg__(self):return E(-self.q,-self.k,-self.c)
    def __sub__(self,o):return self+(-o if isinstance(o,E) else -o)
    def __mul__(self,n):return E(self.q*n,self.k*n,self.c*n)
    __rmul__=__mul__
    def val(self,q,k):return self.q*q+self.k*k+self.c
    def __str__(self):return f'{self.q}q+{self.k}k+{self.c}'

Q=E(q=1); K=E(k=1)
@dataclass(frozen=True)
class R:
    word:Tuple[int,...]; n:E
    def length(self):return self.n*len(self.word)
class CannotProve(Exception):pass

def nonnegative(e,qmin,kmin):
    if e.q<0 or e.k<0 or e.val(qmin,kmin)<0:
        raise CannotProve('count not uniformly >=0: '+str(e))

def run(w,n=1):
    return R(tuple(w),E(c=n) if isinstance(n,int) else n)

def clean(seq):
    out=[]
    for r in seq:
        if not r.word or r.n==E():continue
        if out and out[-1].word==r.word:
            out[-1]=R(r.word,out[-1].n+r.n)
        elif out and out[-1].n.q==out[-1].n.k==r.n.q==r.n.k==0 and len(out[-1].word)*out[-1].n.c+len(r.word)*r.n.c<=8192:
            old=out.pop()
            out.append(run(old.word*old.n.c+r.word*r.n.c))
        else:out.append(r)
    return out

def choose(a,b,qmin,kmin):
    d=a-b
    if d.q>=0 and d.k>=0 and d.val(qmin,kmin)>=0:return b
    if d.q<=0 and d.k<=0 and d.val(qmin,kmin)<=0:return a
    raise CannotProve('ambiguous symbolic boundary comparison '+str(a)+' vs '+str(b))

def eat(r:R,amt:E,qmin,kmin):
    """Remove amt letters of word**n using parameter-independent phase."""
    m=len(r.word)
    if amt.q%m or amt.k%m:
        raise CannotProve('parameter-dependent cut phase '+str(amt)+' mod '+str(m))
    t=E(amt.q//m,amt.k//m,amt.c//m)
    rem=amt.c%m
    if rem:
        n=r.n-t-E(c=1)
        nonnegative(n,qmin,kmin)
        return clean([R(r.word[rem:]+r.word[:rem],n),run(r.word[rem:])])
    n=r.n-t
    nonnegative(n,qmin,kmin)
    return clean([R(r.word,n)])

def add_runs(a:R,b:R,amt:E,qmin,kmin):
    if amt.q==0 and amt.k==0:
        return [run([a.word[i%len(a.word)]+b.word[i%len(b.word)] for i in range(amt.c)])]
    m=lcm(len(a.word),len(b.word))
    if amt.q%m or amt.k%m:
        raise CannotProve('parameter-dependent paired phase '+str(amt)+' mod '+str(m))
    w=tuple(a.word[i%len(a.word)]+b.word[i%len(b.word)] for i in range(m))
    copies=E(amt.q//m,amt.k//m,amt.c//m)
    nonnegative(copies,qmin,kmin)
    rem=amt.c%m
    return clean([R(w,copies),run(w[:rem])])

def zip_pair(left,right,qmin,kmin,compare=False,limit=25000):
    aa=clean(left);bb=clean(right);out=[];pos=E();iterations=0
    while aa and bb:
        iterations+=1
        if iterations>limit:raise CannotProve('symbolic fragment limit')
        a,b=aa[0],bb[0]
        amt=choose(a.length(),b.length(),qmin,kmin)
        if amt.val(qmin,kmin)<=0:raise CannotProve('zero-width interval at bound')
        if compare:
            period=lcm(len(a.word),len(b.word)) if amt.q or amt.k else amt.c
            cap=min(amt.val(qmin,kmin),period)
            for h in range(cap):
                if a.word[h%len(a.word)]!=b.word[h%len(b.word)]:
                    return {'return':False,'first_mismatch':str(pos+E(c=h)),
                            'observed':a.word[h%len(a.word)],
                            'expected':b.word[h%len(b.word)]}
            if cap<period and (amt.q!=0 or amt.k!=0):
                raise CannotProve('too short for universal period equality')
        else:out+=add_runs(a,b,amt,qmin,kmin)
        pos+=amt
        aa=eat(a,amt,qmin,kmin)+aa[1:]
        bb=eat(b,amt,qmin,kmin)+bb[1:]
    if aa or bb:raise CannotProve('symbolic unequal total lengths')
    return {'return':True,'length':str(pos)} if compare else clean(out)

def reverse(s):return [R(r.word[::-1],r.n) for r in reversed(s)]

def normalized(s,qmin,kmin):
    carry=0;out=[]
    for r in s:
        if r.n==E():continue
        nonnegative(r.n-E(c=1),qmin,kmin)
        d=[];c=carry
        for a in r.word:
            if not 0<=a<=18:raise CannotProve('invalid pairword coefficient')
            z=a+c;d.append(z%10);c=z//10
        out.append(run(d))
        stable=[];cc=c
        for a in r.word:
            z=a+cc;stable.append(z%10);cc=z//10
        if cc!=c:raise CannotProve('block carry transducer not idempotent')
        out.append(R(tuple(stable),r.n-E(c=1)))
        carry=c
    if carry:out.append(run([carry]))
    return clean(out),carry

def step(s,qmin,kmin):
    d,g=normalized(s,qmin,kmin)
    return zip_pair(d,reverse(d),qmin,kmin),g

def tpl(B,W,J,U,C):
    H=[run(B),R(tuple(W),Q),run(J),R(tuple(U),K)]
    return clean(H+[run(C)]+reverse(H))

def replay_symbolic(B,W,J,U,C,qmin=512,kmin=512,nsteps=120):
    current=tpl(B,W,J,U,C)
    gam=[];odd=[]
    for t in range(nsteps):
        offset=E();witness=None
        for r in current:
            for h,x in enumerate(r.word):
                if x&1 and r.n.val(qmin,kmin)>=1:
                    witness=str(offset+E(c=h));break
            if witness is not None:break
            offset+=r.length()
        odd.append(witness)
        try:current,g=step(current,qmin,kmin)
        except CannotProve as e:
            raise CannotProve(f'at temporal step {t}: {e}; input atoms {len(current)}')
        gam.append(g)
        if len(current)>10000:raise CannotProve('atom explosion')
    expected=tpl(B,W,J,U,C)
    expected=[R(a.word,a.n+E(c=5)) if a.n.k else a for a in expected]
    ans=zip_pair(current,expected,qmin,kmin,compare=True)
    clock=gam==[1,0,0,0]*30
    complete=all(x is not None for x in odd)
    ans.update({'gamma':''.join(map(str,gam)),'sum_gamma':sum(gam),
                'fragment_count':len(current),'q_min':qmin,'k_min':kmin,
                'clock_exact':clock,'certificate_ready':ans['return'] and clock and complete,
                'odd_witnesses_complete':complete,
                'first_missing_odd_witness':next((i for i,x in enumerate(odd) if x is None),None)})
    return ans

def digits(n):
    a=[]
    while n:a.append(n%10);n//=10
    return a

def value(w):
    n=0
    for a in reversed(w):n=n*10+a
    return n

def actual_pair(n):
    d=digits(n)
    return [a+b for a,b in zip(d,reversed(d))]

def realize(p):
    assert p==p[::-1]
    d=[0]*len(p)
    for i in range(len(d)//2):
        hi=min(9,p[i]);lo=p[i]-hi
        assert 0<=lo<=9
        d[i]=lo;d[-1-i]=hi
    if len(d)%2:
        assert p[len(d)//2]%2==0
        d[len(d)//2]=p[len(d)//2]//2
    assert d[-1]
    return value(d)

def actual(B,W,J,U,C,q,k,nsteps=120):
    h=list(B)+list(W)*q+list(J)+list(U)*k
    source=h+list(C)+h[::-1]
    target_h=list(B)+list(W)*q+list(J)+list(U)*(k+5)
    target=target_h+list(C)+target_h[::-1]
    n=realize(source);gam=[]
    for t in range(nsteps):
        d=digits(n);rv=value(d[::-1]);n2=n+rv
        gam.append(len(digits(n2))-len(d));n=n2
    p=actual_pair(n)
    first=next((i for i,(x,y) in enumerate(zip(p,target)) if x!=y),None)
    if first is None and len(p)!=len(target):first=min(len(p),len(target))
    return {'return':p==target,'gamma':''.join(map(str,gam)),
            'sum_gamma':sum(gam),'first_mismatch':first,'digits':len(digits(n)),
            'expected_digits':len(target)}

def load_lattice(path):
    lines=pathlib.Path(path).read_text().strip().splitlines()
    p,nb,m,b=map(int,lines[0].split());assert (p,nb,m,b)==(12,34,9,10)
    gamma=list(map(int,lines[1].split()))
    W=[list(map(int,lines[2+i].split())) for i in range(p)]
    B=[list(map(int,lines[2+2*p+i].split())) for i in range(p)]
    return B[0],W[0],gamma

def main():
    a=argparse.ArgumentParser()
    a.add_argument('--lattice',required=True)
    a.add_argument('--J',default='5');a.add_argument('--C',default='10')
    a.add_argument('--U',default='9,14,4');a.add_argument('--qmin',type=int,default=512)
    a.add_argument('--kmin',type=int,default=512)
    a.add_argument('--steps',type=int,default=120)
    a.add_argument('--only-symbolic',action='store_true')
    args=a.parse_args()
    B,W,gamma=load_lattice(args.lattice)
    J=[int(x) for x in args.J.split(',') if x]
    C=[int(x) for x in args.C.split(',') if x]
    U=[int(x) for x in args.U.split(',') if x]
    assert C==C[::-1] and all(0<=x<=18 for x in B+W+J+U+C)
    assert B[0]>0 and (len(C)%2==0 or C[len(C)//2]%2==0), 'not a realizable pairword'
    assert len(U)==3 and U[0]==9 and U[1]+U[2]==18 and U[1]%2==0
    assert args.qmin>=1 and args.kmin>=1
    if not args.only_symbolic:
        for q,k in [(20,20),(40,40),(80,80),(160,160)]:
            print(json.dumps({'q':q,'k':k,**actual(B,W,J,U,C,q,k,args.steps)}),flush=True)
    try:
        print('SYMBOLIC',json.dumps(replay_symbolic(B,W,J,U,C,args.qmin,args.kmin,args.steps)),flush=True)
    except CannotProve as e:print('SYMBOLIC_UNDECIDED',str(e),flush=True)

if __name__=='__main__':main()
