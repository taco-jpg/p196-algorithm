#!/usr/bin/env python3
"""Independent exact checks for Agent 722's top-of-exterior theorem.
No network, third-party packages, or repository imports needed.
All coefficient words are least-significant first, canonical trim B[-1]!=b-1.
"""
from itertools import product
from random import Random


def norm(base, a, carry):
    out = []
    for v in a:
        out.append((v + carry) % base)
        carry = (v + carry) // base
    return out, carry


def step(base, B):
    D, e1 = norm(base, B, 0)
    R, gam = norm(base, B[::-1], 1-e1)
    raw = ([u+v for u,v in zip(D,R[::-1])] if gam == 0 else
           [u+v for u,v in zip(D+[(base-1)*(1-e1)],[1]+R[::-1])])
    trimmed = raw[:]
    while trimmed and trimmed[-1] == base-1:
        trimmed.pop()
    return tuple(trimmed), e1, gam, tuple(raw)


def native_pair_step(base, B, gap=13):
    D, e1 = norm(base, B, 0)
    centre = [2*(base-1)] if e1==0 else [0]
    P = list(B)+[base-1]*gap+centre+[base-1]*gap+list(B[::-1])
    digits = [0]*len(P)
    for j in range(len(P)//2):
        digits[j] = P[j]//2
        digits[-j-1] = P[j]-digits[j]
    digits[len(P)//2] = P[len(P)//2]//2
    assert 1 <= digits[-1] < base and all(0 <= d < base for d in digits)
    number = sum(d*base**j for j,d in enumerate(digits))
    reverse_number = sum(d*base**j for j,d in enumerate(digits[::-1]))
    target = number + reverse_number
    out = []
    while target:
        out.append(target%base)
        target//=base
    newpair = [u+v for u,v in zip(out,out[::-1])]
    newB,e,gam,raw=step(base,B)
    assert e==e1
    assert len(out) == len(digits)+gam, ('gamma',base,B)
    assert newpair[:len(raw)] == list(raw), ('integer pair prefix',base,B,e,gam,raw,newpair[:len(raw)])
    return gam


def check(B, base):
    B1,e,g,raw=step(base,B)
    if g:
        assert len(B1)==len(B)+1, ('width violation',base,B,e,g,raw,B1)
        assert norm(base,B1,0)[1] == 1-e, ('carry-flip violation',base,B,e,g,raw,B1)
        assert raw[-1]!=base-1, ('top neutral',base,B,e,g,raw)
    else:
        assert len(B1)<=len(B), ('nonoverflow width increase',base,B,e,g,raw,B1)
    return g


def main():
    n=0; gcount=0
    for base in range(2,12):
        for width in range(1,5):
            for B in product(range(2*base-1), repeat=width):
                if B[0]==0 or B[-1]==base-1: continue
                gcount+=check(B,base)
                n+=1
        print('PASS exhaustive base',base)
    rand=Random(722)
    intn=intg=0
    for i in range(15000):
        base=rand.randrange(2,27)
        width=rand.randrange(1,31)
        B=[rand.randrange(0,2*base-1) for _ in range(width)]
        B[0]=rand.randrange(1,2*base-1)
        while B[-1]==base-1 or (width==1 and B[-1]==0):
            B[-1]=rand.randrange(0,2*base-1)
        check(B,base)
        intg+=native_pair_step(base,B)
        intn+=1
    print('ALL CHECKS PASSED:',n,'exhaustive canonical exterior words,',gcount,'overflow cases;')
    print('independent ordinary-integer checks:',intn,'random cases,',intg,'overflows')


if __name__=='__main__':main()
