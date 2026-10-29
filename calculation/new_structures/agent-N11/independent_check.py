#!/usr/bin/env python3
"""Independent Python bigint and randomized controls for carry-shadow rule."""
from __future__ import annotations
import argparse
import random
MASK=(1<<64)-1
def hash_digits(s):
    h=1469598103934665603
    for c in reversed(s):
        h=((h^int(c))*1099511628211)&MASK
    return format(h,'x')
def pairword(s):
    return [int(s[-1-i])+int(s[i]) for i in range(len(s)//2)]
def rule(p,i,gamma):
    if gamma==0:
        if p[i-1]==9 or p[i+1]==9:return None
        return (p[i]+int(p[i-1]>=10))%10+(p[i]+int(p[i+1]>=10))%10
    if p[i-1]==9 or p[i]==9:return None
    return (p[i]+int(p[i-1]>=10))%10+(p[i-1]+int(p[i]>=10))%10
def test_196(n,sample_file=None):
    checkpoints={}
    if sample_file:
        with open(sample_file) as f:
            next(f)
            for line in f:
                x=line.rstrip().split('\t')
                checkpoints[int(x[0])]=(int(x[1]),x[-1])
    a=196;totals=[0,0];eligible=[0,0];controls=0
    for t in range(n+1):
        s=str(a)
        if t in checkpoints:
            length,h=checkpoints[t]
            assert len(s)==length,(t,len(s),length)
            assert hash_digits(s)==h,(t,hash_digits(s),h)
            controls+=1
        if t==n:break
        p=pairword(s); nxt=a+int(s[::-1]); sn=str(nxt)
        g=int(len(sn)>len(s));q=pairword(sn)
        for i in range(2,min(len(p)-2,len(q))):
            totals[g]+=1
            pred=rule(p,i,g)
            if pred is not None:
                eligible[g]+=1
                assert pred==q[i],(t,i,g,p[i-1:i+2],pred,q[i])
        assert sn!=sn[::-1],('pal',t+1)
        a=nxt
    print('PYTHON independent int replay PASSED',n,'steps, checkpoints',controls,'eligible',eligible,'totals',totals)
def random_controls(n):
    r=random.Random(196);good=0;ambiguous=0
    for _ in range(n):
        length=r.randint(40,200)
        d=[r.randrange(10) for _ in range(length)]
        d[-1]=r.randint(1,9)
        s=''.join(map(str,reversed(d)));a=int(s);p=pairword(s)
        nxt=str(a+int(s[::-1]));g=int(len(nxt)>len(s));q=pairword(nxt)
        for i in range(2,len(p)-2):
            z=rule(p,i,g)
            if z is not None:
                assert z==q[i]
                good+=1
            else:ambiguous+=1
    print('RANDOM seed controls PASSED',n,'eligible',good,'ambiguous',ambiguous)
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--steps',type=int,default=5000)
    ap.add_argument('--sample-file')
    a=ap.parse_args()
    random_controls(1000)
    test_196(a.steps,a.sample_file)
