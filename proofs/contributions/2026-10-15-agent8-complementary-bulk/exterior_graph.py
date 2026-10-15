"""Exact necessary leading-pair graph and independently checkable potentials."""
from collections import defaultdict


def edges():
    out=[]
    for p in range(1,19):
        for e in (0,1):
            gamma=int(p+e>=10)
            q=p%10+1 if gamma else 2*p+e
            out.append((p,q,gamma,e))
    return out


def potential(weight):
    # H[p] >= H[q]+w(p,q); synchronous longest-path relaxation.
    h=[0]*19
    for _ in range(19):
        h1=h[:]
        for p,q,g,e in edges(): h1[p]=max(h1[p],h[q]+weight(g))
        if h1==h:
            assert all(h[p]>=h[q]+weight(g) for p,q,g,e in edges())
            return h
        h=h1
    return None


if __name__=='__main__':
    up=potential(lambda g:2*g-1)
    low=potential(lambda g:1-4*g)
    print('upper',up)
    print('lower',low)
    for period in range(1,37):
        counts=set()
        for p0 in range(1,19):
            states={(p0,0)}
            for _ in range(period):
                states={(q,k+g) for p,k in states for p1,q,g,e in edges() if p==p1}
            counts|={k for p,k in states if p==p0}
        if period<=12: print(period,sorted(counts))
