#!/usr/bin/env python3
"""Independent canonical-root obstruction and finite controls for bauto3/bauto5.

For the time-rooted start state L=0, H=g, Y=1 at overflow positions,
each first-column candidate satisfies 1<=x0<=2b-2 and, for h_t in {0,1},
  floor((x_t+h_t)/b) = g_t
  x_(t+1) = (x_t % b) + (1 if g_t else ((x_t+h_t) % b)).
A root edge also requires the time orbit x_p=x_0.

For g starting 11 0^r 1 with r>=1, the first two 1s yield
(x0,x1,x2)=(b-1,b,1) or (2b-2,b-1,b). The third bit 0 rules out x2=b.
Starting at x2=1, each zero doubles x and optionally adds one,
so x_(r+2)<=2^(r+1)-1. The following 1 requires
b<=x_(r+2)+h_(r+2)<=2^(r+1), impossible if b>2^(r+1).
This is a root obstruction, not a no-cycle theorem for arbitrary phases.
"""
from __future__ import annotations
import argparse


def canonical_root_trajectories(b: int, g: str):
    assert b >= 2 and g and set(g) <= {'0','1'}
    p = len(g)

    def visit(t, x0, x, xs, hs):
        if t == p:
            if x == x0:
                yield tuple(xs), tuple(hs)
            return
        for h in (0,1):
            if (x+h)//b != (g[t] == '1'):
                continue
            nx = x%b + (1 if g[t]=='1' else (x+h)%b)
            yield from visit(t+1,x0,nx,xs+[x],hs+[h])

    for x0 in range(1,2*b-1):
        yield from visit(0,x0,x0,[],[])


def assert_zero_early(b: int, g: str):
    assert g.startswith('11')
    r=0
    for bit in g[2:]:
        if bit=='0': r+=1
        else: break
    assert r>=1 and len(g)>r+2 and g[r+2]=='1'
    assert b>2**(r+1)
    states={(x0,x0) for x0 in range(1,2*b-1)}
    for t in range(r+3):
        nxt=set()
        for x0,x in states:
            for h in (0,1):
                if (x+h)//b!=(g[t]=='1'): continue
                y=x%b+(1 if g[t]=='1' else (x+h)%b)
                nxt.add((x0,y))
        states=nxt
        if t==1:
            assert all(x0 in (b-1,2*b-2) and y in (1,b) for x0,y in states)
        if t==2:
            assert all(x0==b-1 and y in (2,3) for x0,y in states)
        if t==r+1:
            assert all(y<=2**(r+1)-1 for _,y in states)
    assert not states,(b,g,states)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-base',type=int,default=100)
    a=parser.parse_args()
    w9='1100011000'; w13='1010010000'
    for b in range(2,a.max_base+1):
        v=list(canonical_root_trajectories(b,w9))
        if b>=17:
            assert not v,(b,v)
            assert_zero_early(b,w9)
        if b in (9,13,16,17,32,49,100):
            print('base',b,'word',w9,'closed_root_trajectories',len(v))
            if b==16:
                assert any(xs==(15,16,1,3,7,15,16,1,3,7) for xs,_ in v)
                print('base-16 sharpness witness', (15,16,1,3,7,15,16,1,3,7))
    v13=list(canonical_root_trajectories(13,w13))
    assert len(v13)==8,len(v13)
    print('base 13 word',w13,'closed_root_trajectories',len(v13))
    print('PASS: exhaustive first-column checks (not a full SCC census)')


if __name__ == '__main__':
    main()
