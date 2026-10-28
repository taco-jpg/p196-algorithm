#!/usr/bin/env python3
"""Independent constructive F1+F2 root path replay for b=2**(r+1)."""
from itertools import product


def gword(r):
    return '1'+'0'*r+'11'+'0'*(r+1)


def first_x(r):
    b=1<<(r+1)
    return [b]+[(1<<t)-1 for t in range(1,r+2)]+[b]+[(1<<k) for k in range(r+1)]


def first_c(r,mode):
    return [mode]+[1]*(r+1)+[mode]+[0]*(r+1)


def second_x(r,mode):
    b=1<<(r+1)
    if mode==0:
        return [b-2]+[b-1]*(r+2)+[0]+[(1<<k)-1 for k in range(1,r+1)]
    return [2*b-3]+[b-1]*(r+2)+[(1<<(k+1))-1 for k in range(r)]+[b-2]


def second_c(r,mode,free):
    if mode==0:
        return [free]+[1]*(r+1)+[0]+[1]*r+[0]
    return [free]+[1]*(2*r+1)+[0,1]


def replay(r,mode,free):
    b=1<<(r+1)
    g=[int(v) for v in gword(r)]
    p=len(g)
    x=first_x(r);c=first_c(r,mode)
    assert len(x)==len(c)==p
    assert all(1<=v<=2*b-2 for v in x)
    assert all((x[t]+c[t])//b==g[t] for t in range(p))
    for t in range(p):
        nxt=x[t]%b + (1 if g[t] else (x[t]+c[t])%b)
        assert nxt==x[(t+1)%p], ('first',r,mode,t)
    L=[v//b for v in x]
    H=c[:]
    Y={t:(x[t]+c[t])%b for t in range(p) if g[t]}
    xx=second_x(r,mode)
    cc=second_c(r,mode,free)
    assert len(xx)==len(cc)==p
    assert all(0<=v<=2*b-2 for v in xx)
    assert all((xx[t]+cc[t])//b==H[t] for t in range(p))
    for t in range(p):
        nxt=(xx[t]+L[t])%b+(Y[t] if g[t] else (xx[t]+cc[t])%b)
        assert nxt==xx[(t+1)%p], ('second',r,mode,free,t)
    return True


if __name__=='__main__':
    for r in range(1,101):
        for mode,free in product((0,1),repeat=2):replay(r,mode,free)
    print('PASS: all four explicit two-column paths, every r=1..100')
