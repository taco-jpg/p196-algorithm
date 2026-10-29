#!/usr/bin/env python3
"""Independent base-10 GMP control of the N02 travelling centre, in pure Python int.
Reads the p8 lattice directly from the tracked p8_scc.txt, not the C++ arrays.
Checks all 19 short pumped seeds through exact breakpoints 88q+4, using
unbounded Python integers and decimal digit reversal.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path


def original_data(root):
    name=Path(root)/'calculation/decimal_frontier/lattice_formats/p8_scc.txt'
    line=next(x for x in name.read_text().splitlines() if x.startswith('SCC p=8 g=10101010'))
    raw_a=line.split(' path=',1)[1].split(' cyc=',1)
    def parse(part):
        return [[int(v) for v in x.split(',')] for x in re.findall(r'\[([^]]+)\]',part)]
    path,cyc=map(parse,raw_a)
    assert len(path)==39 and len(cyc)==20
    assert all(len(x)==8 and all(0<=v<=18 for v in x) for x in path+cyc)
    return path,cyc


def seed(q,path,cyc):
    half=[x[0] for x in path]+[x[0] for x in cyc]*q
    digits=[0]*(2*len(half))
    for i,v in enumerate(half):
        digits[i]=min(v,9)
        digits[-1-i]=v-digits[i]
    assert digits[-1]>0
    text=''.join(str(i) for i in digits[::-1])
    return int(text)


def frontier(n,t,path,cyc):
    s=str(n)
    digits=tuple(map(int,s))
    h=(len(digits)+1)//2
    for j in range(h):
        pair=digits[-1-j]+digits[j]
        exp=path[j][t%8] if j<39 else cyc[(j-39)%20][t%8]
        if pair!=exp:return j
    return h


def replay(q,path,cyc,stop):
    n=seed(q,path,cyc)
    fronts=[]
    initial_len=len(str(n))
    fail=None
    for t in range(stop):
        s=str(n)
        if s==s[::-1]:raise AssertionError(('palindrome',q,t))
        j=frontier(n,t,path,cyc)
        if j<39:
            fail=(t,j)
            break
        fronts.append(j)
        if t>=98 and j!=fronts[t-88]-20:
            raise AssertionError(('front-shift',q,t,j,fronts[t-88]))
        x=int(s[::-1]);n2=n+x
        gamma=len(str(n2))-len(s)
        if gamma!=int(t%2==0):raise AssertionError(('overflow',q,t,gamma))
        n=n2
    return fail,fronts,initial_len,len(str(n))


def main(root):
    path,cyc=original_data(root)
    # Every shorter q has its own independent arbitrary-precision seed and orbit.
    for q in range(1,20):
        fail,fronts,n0,nlast=replay(q,path,cyc,88*q+5)
        assert fail==(88*q+4,38),(q,fail)
        assert n0==2*(39+20*q)
        assert min(fronts)>=39
    print('N02_INDEPENDENT_INTEGER_SHORT_FAMILY_PASS 19 seeds q=1..19; first_bad=88q+4, index=38')
    # Independent 1,500-step positive long-pumped control, outside the short-q range.
    fail,fronts,n0,nlast=replay(30,path,cyc,1500)
    assert fail is None and n0==1278 and len(fronts)==1500
    print('N02_INDEPENDENT_INTEGER_Q30_PASS 1500 steps, no palindromes, no exterior failure')


if __name__=='__main__':
    if len(sys.argv)>1:root=sys.argv[1]
    else:root=Path(__file__).resolve().parents[3]
    main(root)
