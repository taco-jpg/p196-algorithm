#!/usr/bin/env python3
"""Independent Python reference for the exact base-10 B-graph computation.
Reconstructs the B projection from simple carry arithmetic; integer-orbit
cross-check also compares its raw output against ordinary reverse-add.
"""
from collections import deque
from itertools import product
import random
import re
import subprocess
import sys


def norm(word, carry):
    out = []
    for x in word:
        x += carry
        out.append(x % 10)
        carry = x // 10
    return out, carry


def step_B(word):
    b, e1 = norm(word, 0)
    r, g = norm(word[::-1], 1-e1)
    if g:
        left = b + [9*(1-e1)]
        right = [1] + r[::-1]
    else:
        left = b
        right = r[::-1]
    return tuple(x+y for x, y in zip(left,right)), g


def edges(B, K):
    raw, g = step_B(B)
    t = 0
    while t < len(raw) and raw[len(raw)-1-t] == 9:
        t += 1
    return [(raw[:len(raw)-u],u,g) for u in range(t+1)
            if len(raw)-u <= K and (len(raw)==u or raw[0]!=0)]


def candidates(K):
    yield ()
    for n in range(1,K+1):
        for a in range(1,19):
            for rest in product(range(19),repeat=n-1):
                yield (a,) + rest


def census(K):
    vs = list(candidates(K))
    deg = {b:0 for b in vs}
    outs = {}
    count = 0
    trims = {}
    by_gamma = [0,0]
    for b in vs:
        outs[b] = []
        for bn,u,g in edges(b,K):
            outs[b].append(bn)
            deg[bn]+=1
            count+=1
            trims[u] = trims.get(u,0)+1
            by_gamma[g] +=1
    q=deque(b for b in vs if deg[b]==0)
    removed=0
    while q:
        b=q.popleft()
        removed+=1
        for bn in outs[b]:
            deg[bn]-=1
            if deg[bn]==0:
                q.append(bn)
    return len(vs),count,by_gamma,trims,len(vs)-removed


def digits(n):
    d=[]
    while n:
        d.append(n%10)
        n//=10
    return d


def crosscheck_integer(trials=10000):
    rng=random.Random(1961208)
    found=0
    attempts=0
    while found<trials and attempts<trials*30:
        attempts+=1
        n=rng.randint(1,7)
        B=[rng.randint(1,18)] + [rng.randint(0,18) for _ in range(n-1)]
        half=[rng.randint(0,18) for _ in range(rng.randint(0,4))]
        C=half+half[::-1]
        d1,e1=norm(B,0)
        _,e2=norm(C,e1)
        if e1==e2: continue
        g=5
        q=B+[9]*g+C+[9]*g+B[::-1]
        assert q==q[::-1]
        # Realize q by two complementary decimal digits at each mirrored pair.
        low=[]; high=[]
        for i,v in enumerate(q[:len(q)//2]):
            a=min(9,v-1) if i==0 else min(9,v)
            z=v-a
            assert 0<=a<=9 and 0<=z<=9
            low.append(a); high.append(z)
        xdigits=low+high[::-1]
        assert xdigits[-1]>0
        x=sum(a*10**i for i,a in enumerate(xdigits))
        rd=digits(x)
        rev=sum(a*10**i for i,a in enumerate(rd[::-1]))
        nxt=digits(x+rev)
        newpair=tuple(a+b for a,b in zip(nxt,nxt[::-1]))
        raw, gam=step_B(B)
        assert newpair[:len(raw)]==raw,(B,C,raw,newpair)
        found+=1
    assert found==trials,(found,attempts)
    print(f'INTEGER-ORBIT cross-check PASSED: {found} admissible randomized templates (seed=1961208)')


def main():
    binary=sys.argv[1] if len(sys.argv)>1 else './b_width_graph'
    for K in range(1,5):
        s=subprocess.check_output([binary,str(K)],text=True).strip()
        py=census(K)
        assert f'states={py[0]}' in s
        assert f'edges={py[1]}' in s
        assert f'gamma0={py[2][0]}' in s
        assert f'gamma1={py[2][1]}' in s
        assert f'residual={py[-1]}' in s
        assert 'trimmed='+','.join(f'{j}:{py[3].get(j,0)}' for j in range(K+1)) in s
        print(f'CROSS-LANGUAGE K={K} PASSED: {py[0]} states; {py[1]} edges; residual {py[-1]}')
    crosscheck_integer()
    print('ALL CROSS-CHECKS PASSED')


if __name__=='__main__':main()