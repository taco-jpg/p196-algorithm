import os
import sys, random, collections
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import neutral_band_search as N
from neutral_band_search import norm, e1, e2, DB, DC, DR, gam, xd, yd, nextB, nextC, hyp, trim, step, run, is_cert

def pol_top(b, W, default):
    """carry out of block W (incoming carry=default) = polarity of top-most non-neutral entry"""
    n = b-1
    for w in reversed(W):
        if w > n: return 1
        if w < n: return 0
    return default

def tie_depth(b, W):
    n=b-1
    for j,w in enumerate(reversed(W)):
        if w != n: return j
    return len(W)

def rand_state(b, rng, mB=(1,8), mC=(0,8)):
    n=b-1
    m=rng.randint(*mB); B=[rng.randint(1,2*n)]+[rng.randint(0,2*n) for _ in range(m-1)]
    c=rng.randint(*mC); h=[rng.randint(0,2*n) for _ in range((c+1)//2)]
    C=h+h[:c//2][::-1]
    return B,C
