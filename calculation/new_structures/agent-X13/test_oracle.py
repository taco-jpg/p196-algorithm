#!/usr/bin/env python3
"""Reproduce exact symbolic obligations, independent decimal integers and mutations."""
import json, hashlib, random
from affine_two_counter import (
    Aff, Quadrant, Nonuniform, Run, ROWS, check_rows, independent_replay,
    full, expand, seed_from_pairs, next_digits, pair_digits,
)
from periodic_affine import Piece, literal, expand as expand_periodic, derive_pair, equal_symbolic
from controls import b9,b50


def convert(ds,b):
    n=0
    for d in reversed(ds):n=n*b+d
    return n

def digits(n,b):
    out=[]
    while n:out.append(n%b);n//=b
    return out or [0]

def integer_replay(b,seed_digits,steps=6):
    n=convert(seed_digits,b)
    states=[]
    for t in range(steps+1):
        ds=digits(n,b)
        assert ds==seed_digits,(b,t,'full bigint mismatch')
        assert ds!=ds[::-1]
        states.append((t,len(ds),ds[0],ds[-1]))
        if t!=steps:
            r=convert(ds[::-1],b)
            n+=r
            seed_digits=next_digits(b,seed_digits)
    return states


def fuzz_periodic(trials=125):
    rng=random.Random(1313007)
    tested=0;rejected=0
    for _ in range(trials):
        b=rng.choice([7,9,10,13,50]);m=rng.randint(1,5)
        w=tuple(rng.randint(0,2*(b-1)) for _ in range(m))
        B=[rng.randint(0,2*(b-1)) for _ in range(rng.randrange(2,7))]
        residual=rng.randrange(m)
        src=literal(B)+[Piece(w,Aff(k=m,c=residual))]+literal(B[::-1])
        G=Quadrant(3,3)
        try:
            out,gamma=derive_pair(b,src,G)
        except Nonuniform:
            rejected+=1;continue
        for k in (3,4,6,11,40):
            coeff=expand_periodic(src,k,3)
            x=[];carry=0
            for v in coeff:
                s=v+carry;x.append(s%b);carry=s//b
            if carry:x.append(carry)
            assert expand_periodic(out,k,3)==[x[i]+x[-1-i] for i in range(len(x))]
            assert gamma==int(carry!=0)
        tested+=1
    return {'trials':trials,'accepted_correct':tested,'safely_rejected':rejected}


def main():
    f=check_rows()
    control=[b9(),b50()]
    # Crucial tests with different (k,l); synchronized k=l alone is not enough.
    trial_pairs=[(6,6),(6,90),(97,6),(27,101),(1000,537)]
    r={}
    for k,l in trial_pairs:
        rowcheck=independent_replay(k,l)
        seed=seed_from_pairs(expand(full(0),k,l),10)
        states=integer_replay(10,seed,steps=6)
        assert [(t,z) for t,z,_,_ in states]==[(x['time'],x['digits']) for x in rowcheck]
        r[f'{k},{l}']={'initial_digits':states[0][1], 'after_six':states[-1][1],
                        'full_bigint_checks':7,'not_palindromes':7}
    # A one-unit mutation in an expected phase MUST be caught by the oracle.
    inp=literal([10,8,5,11,16,8,8,16,11,5,8,10])
    out,g=derive_pair(10,inp,Quadrant(6,6))
    q=list(out);q[0]=Piece((q[0].pat[0]+1,),q[0].length)
    ok,_=equal_symbolic(out,q,Quadrant(6,6))
    assert not ok
    # Unsupported mixed-direction constraints are not silently certified.
    try:Quadrant(6,6).le(Aff(k=1),Aff(l=1))
    except Nonuniform:pass
    else:raise AssertionError('unsafe comparison accepted')
    summary={'label':'PAPER PROOF (affine exactness) / COMPUTED (controls)',
             'decimal_two_counter':f,'control_cycles':[{
             'base':x['base'],'period':x['period'],'cycle_return':x['cycle_return'],
             'proved_orthant_kmin':x['k_min'],'symbolic_compares':x['comparisons'],
             'counter_gain':x['counter_gain']} for x in control],
             'decimal_independent_bigints':r,
             'random_periodic':fuzz_periodic(),
             'mutation_rejected':True,'undecidable_guard_rejected':True}
    blob=json.dumps(summary,indent=2,sort_keys=True)
    print(blob)

if __name__=='__main__':main()
