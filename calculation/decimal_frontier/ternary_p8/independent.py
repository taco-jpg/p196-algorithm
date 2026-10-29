#!/usr/bin/env python3
"""Independent Python 3 arithmetic/light-cone checker for Agent13TernaryP8.
No dependencies on p8_nfa.cpp, no SAT solver; runs all exceptional
endpoint factor cases and random real-integer reverse-add controls.
"""
from functools import lru_cache
from itertools import product
import random
MU={'0':'01','1':'02','2':'00'}
G=(1,0,1,0,1,0,1,0)
TABLES=((0,8,17),(0,17,8),(18,1,10),(18,10,1))

@lru_cache(None)
def factors(n):
    if n==1:return frozenset('012')
    if n==2:return frozenset(('00','01','02','10','20'))
    k=(n+2)//2
    return frozenset(z[j:j+n] for w in factors(k)
        for z in [''.join(MU[c] for c in w)] for j in (0,1) if j+n<=len(z))

def pat(seq):
    seen={};out=[]
    for x in seq:
        if x not in seen:seen[x]=len(seen)
        out.append(seen[x])
    return tuple(out)

def digits_with_carry(seq,c):
    out=[]
    for a in seq:
        c,v=divmod(a+c,10)
        out.append(v)
    return out

@lru_cache(maxsize=200000)
def next_words(seq,overflow):
    out=set()
    for left in (0,1):
        l=digits_with_carry(seq,left)
        for right in (0,1):
            r=digits_with_carry(seq[::-1],right)[::-1]
            if overflow:
                v=tuple(l[i]+r[i-1] for i in range(1,len(seq)))
            else:
                v=tuple(l[i]+r[i] for i in range(len(seq)))
            out.add(v)
    return tuple(out)

def evolve(seq,gammas=G):
    pool={seq};max_states=1
    for gamma in gammas:
        pool={v for old in pool for v in next_words(old,gamma)}
        max_states=max(max_states,len(pool))
    return pool,max_states

def exceptions():
    expected={pat(t) for t in factors(28)}
    assert len(factors(32))==80 and len(factors(28))==72
    counts=[]
    for A in TABLES:
        hits=0;maxstates=0
        for source in factors(32):
            seq=tuple(A[ord(s)-48] for s in source)
            states,m=evolve(seq)
            hits+=sum(pat(v) in expected for v in states)
            maxstates=max(maxstates,m)
        assert hits==0,(A,hits)
        counts.append((A,maxstates))
    print('INDEPENDENT EXCEPTION PASS: 4 tables x 80 exact L32 factors, 0 endpoint L28 survivors:',counts)
    next_words.cache_clear()

def corpus_cross_check():
    word='0'
    for _ in range(16):
        word=''.join(MU[c] for c in word)
    assert len(word)==65536
    for n in (16,20,24,28,32):
        direct={word[i:i+n] for i in range(len(word)-n+1)}
        exact=set(factors(n))
        assert direct==exact,(n,len(direct),len(exact))
    assert len(factors(24))==64 and len(factors(28))==72 and len(factors(32))==80
    print('COMPLETE FACTOR-LANGUAGE CONTROLS PASS: L24=64, L28=72, L32=80')

def to_int(a):
    n=0
    for x in a[::-1]:n=10*n+x
    return n

def to_digits(n):
    d=[]
    while n:
        n,r=divmod(n,10);d.append(r)
    return d

def random_arithmetic(steps=3000):
    rng=random.Random(1304748)
    for k in range(steps):
        B=[rng.randrange(1,19)]+[rng.randrange(19) for _ in range(rng.randrange(1,7))]
        W=[rng.randrange(19) for _ in range(rng.randrange(5,30))]
        coeff=B+W+W[::-1]+B[::-1]
        D=to_digits(to_int(coeff))
        gamma=len(D)-len(coeff)
        assert gamma in (0,1)
        pair=tuple(D[i]+D[-1-i] for i in range(len(D)))
        actual=pair[len(B)+gamma:len(B)+len(W)]
        assert actual in next_words(tuple(W),gamma),(k,gamma)
        assert to_int(pair)==to_int(D)+to_int(D[::-1])
    print('INDEPENDENT INTEGER CONTROLS PASS:',steps)
    next_words.cache_clear()

def crop_controls(trials=5000):
    rng=random.Random(13)
    for _ in range(trials):
        longer=tuple(rng.randrange(19) for _ in range(rng.randrange(9,31)))
        cut=rng.randrange(6,len(longer))
        g=rng.randrange(2)
        full=next_words(longer,g)
        short=set(next_words(longer[:cut],g))
        for z in full:
            assert z[:cut-g] in short,('cropping fails',longer,cut,g)
    print('PREFIX CROPPING CONTROL PASS:',trials)

if __name__=='__main__':
    corpus_cross_check();exceptions();random_arithmetic();crop_controls()
