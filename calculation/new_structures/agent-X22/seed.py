#!/usr/bin/env python3
"""Deterministic 12,800-ary carry-compatible mosaic, not a palindrome-free proof."""
import argparse,random
from sft import B0,W,cycles
def seed(tiles=600,random_seed=20261028):
    opts=[ps for ps,states in cycles(W[1],1) if states[0]==(1,1,4)]
    assert len(opts)==12800 and tuple(W[0]) in opts
    rng=random.Random(random_seed)
    half=B0+[q for _ in range(tiles) for q in rng.choice(opts)]
    lower=[min(9,p) for p in half]
    upper=[p-d for p,d in zip(half,lower)]
    assert upper[0]>0
    return ''.join(map(str,upper+lower[::-1]))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--tiles",type=int,default=600)
    p.add_argument("--random-seed",type=int,default=20261028)
    a=p.parse_args()
    print(seed(a.tiles,a.random_seed))
