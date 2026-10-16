#!/usr/bin/env python3
"""Exact finite controls for the all-length written erasure theorem.

This test does not establish absence of cycles or any claim about P196.
Run with Python 3.10+; only the standard library is used.
"""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path
import random
from complementary_bulk import PHASES, State, audit_instance, normalize, outer_step


def reduced_suffix(B: tuple[int, ...], t: int) -> int:
    r = 0
    for x in reversed(B):
        if x not in (t,t+9):
            break
        r += 1
    return r


def check_erasure(c: int, B: tuple[int, ...]) -> tuple[int,int]:
    kc = int(c >= 10)
    t = c-9*kc
    cp,Bp,uB,gamma = outer_step(c,B)
    if gamma:
        assert uB == reduced_suffix(B,t), (c,B,cp,Bp,uB,gamma)
        assert len(Bp) >= 1
        if uB == len(B):
            assert Bp == (t,)
    elif not B or B[-1] != c:
        alpha = normalize(B,0)[1]
        assert uB == int(alpha == kc), (c,B,cp,Bp,uB,gamma)
        assert len(Bp) >= len(B)
    return gamma,uB


def run(max_b: int=4, random_controls: int=10000) -> dict:
    if not 0 <= max_b <= 6 or random_controls < 0:
        raise ValueError('require 0 <= max_b <= 6 and nonnegative controls')
    hist = Counter()
    all_b_count = 0
    for c in PHASES:
        for b in range(max_b+1):
            Bs = [()] if b == 0 else ((x,)+y for x in range(1,19)
                    for y in product(range(19),repeat=b-1))
            for B in Bs:
                hist[check_erasure(c,B)] += 1
                all_b_count += 1
    # A separate literal-integer route checks the full quotient, not just B.
    rng = random.Random(196009)
    for _ in range(random_controls):
        c = rng.choice(PHASES)
        b,a,m = rng.randrange(31),rng.randrange(21),rng.randrange(11)
        B = () if b == 0 else (rng.randrange(1,19),)+tuple(rng.randrange(19) for _ in range(b-1))
        A = tuple(rng.randrange(19) for _ in range(a))
        H = tuple(rng.randrange(19) for _ in range(m))
        C = H + (() if rng.randrange(2)==0 else (2*rng.randrange(10),)) + H[::-1]
        audit_instance(State(c,B,A,C),rng.randrange(2,10),rng.randrange(2,10))
        check_erasure(c,B)
    # All binary-tail patterns through length 12, every reduced digit and bulk side.
    binary_count = 0
    for t in range(1,9):
        for k in (0,1):
            c = t+9*k
            for b in range(1,13):
                for rest in product((t,t+9),repeat=b-1):
                    B = (t+9,)+rest
                    cp,Bp,uB,gamma = outer_step(c,B)
                    assert (Bp,uB,gamma) == ((t,),b,1)
                    binary_count += 1
    # The no-overflow trimmedness and overflow premises are essential.
    cp,Bp,uB,gamma = outer_step(1,(1,1))
    assert (cp,Bp,uB,gamma) == (2,(),3,0)
    return {
        'status':'PASS',
        'scope':{'phases':PHASES,'all_canonical_B_max_length':max_b,
                 'all_canonical_B_controls':all_b_count,
                 'random_literal_full_quotient_controls':random_controls,
                 'random_seed':196009,'binary_full_erasure_max_length':12,
                 'binary_full_erasure_controls':binary_count},
        'overflow_strip_histogram':{f'{ga},{u}':n for (ga,u),n in sorted(hist.items())},
        'hypothesis_counterexample':{'c':1,'B':[1,1],'gamma':0,'B_next':[],
                                    'stripped':3,'B_length':2,
                                    'note':'B is not trimmed; no overflow. Neither hypothesis may be omitted.'},
        'conclusion':'Finite verification of formulas and edge cases, not a cycle exclusion or a P196 proof.'
    }


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-b',type=int,default=4)
    parser.add_argument('--random-controls',type=int,default=10000)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('erasure_audit.json'))
    args=parser.parse_args()
    result=run(args.max_b,args.random_controls)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
