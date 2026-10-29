#!/usr/bin/env python3
"""All-width exact golden Beatty two-phase one-edge identity; not a cycle."""
from math import isqrt
from rotation_bulk import ordinary_step
import argparse,json

def fl(k,num,den):
    t=k*den
    return (isqrt(5*t*t)-t+2*num)//(2*den)
def beatty(k,num,den):
    return fl(k+1,num,den)-fl(k,num,den)
def check(q,num,den):
    s=[beatty(i,num,den) for i in range(q)]
    assert all(v in (0,1) for v in s)
    d0=[2]+[8+v for v in s]+[8]
    d1=[0]+[7+s[i]+s[q-1-i] for i in range(q)]+[1,1]
    observed,g=ordinary_step(d0)
    assert g==1 and observed==d1
    assert d0[0]!=d0[-1] and d1[0]!=d1[-1]
    if q>5:
        mutated=d1[:]
        mutated[1+q//2]=(mutated[1+q//2]+1)%10
        assert mutated!=observed
def main():
    p=argparse.ArgumentParser();p.add_argument('--max-width',type=int,default=2000)
    a=p.parse_args();n=0
    for num,den in [(0,1),(1,7),(2,7),(3,11)]:
        for q in range(2,a.max_width+1):
            check(q,num,den);n+=1
    print(json.dumps({'exact_tests':n,'result':'PASS','all_width_identity':'PAPER PROOF only'}))
if __name__=='__main__':main()
