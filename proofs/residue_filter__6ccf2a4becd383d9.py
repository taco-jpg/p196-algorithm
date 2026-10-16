#!/usr/bin/env python3
"""Cycle-candidate prefilter proved in GeneralMomentAbsorption/ResidueFilter.

This generates exactly the canonical trimmed decimal exteriors whose absorbing
alternating moment is zero modulo 22. It is NOT an acyclicity certificate.
The prefilter concerns closed cycles with an overflow, not pre-overflow states.
"""
from __future__ import annotations
from itertools import product
import json
from audit_exterior import exteriors
from complementary_quotient import exterior_transition

PHASES = (2,4,6,8,10,12,14,16)


def moment(c: int, B: tuple[int,...]) -> int:
    return 2*sum((-1)**i*x for i,x in enumerate(B))+(-1)**len(B)*c


def candidates(cap: int):
    """Enumerate by prefixes; solve the final column modulo 11 directly."""
    if cap < 0:
        raise ValueError('cap must be nonnegative')
    for c in PHASES:
        r=c//2
        for length in range(1,cap+1):
            sign=1 if length%2 else -1
            for P in product(range(19),repeat=length-1):
                if P and P[0]==0:
                    continue
                alt=sum((-1)**i*x for i,x in enumerate(P))
                residue=(r-sign*alt)%11
                for x in range(residue,19,11):
                    if x==c or (not P and x==0):
                        continue
                    yield c,P+(x,)


def count_exact_length(length: int) -> int:
    """Exact integer dynamic programming, no exponential enumeration."""
    if length<1:
        return 0
    residues=[0]*11
    residues[0]=1
    for pos in range(length-1):
        out=[0]*11
        sign=1 if pos%2==0 else -1
        for r,n in enumerate(residues):
            for x in range(1 if pos==0 else 0,19):
                out[(r+sign*x)%11]+=n
        residues=out
    sign=1 if length%2 else -1
    total=0
    for c in PHASES:
        for a,n in enumerate(residues):
            residue=(c//2-sign*a)%11
            for x in range(residue,19,11):
                if x!=c and (length>1 or x>0):
                    total+=n
    return total


def verify(cap: int = 4) -> dict:
    exhaustive={(c,B) for c,B in exteriors(cap,PHASES) if moment(c,B)%22==0}
    generated=list(candidates(cap))
    assert len(generated)==len(set(generated))
    assert set(generated)==exhaustive
    assert len(generated)==sum(count_exact_length(i) for i in range(1,cap+1))
    for c,B in generated:
        cp,Bp,g,u=exterior_transition(c,B)
        assert moment(cp,Bp)%22==0
        assert Bp and Bp[0]>0 and Bp[-1]!=cp
    cumulative=0; counts=[]
    for length in range(1,13):
        n=count_exact_length(length); cumulative+=n
        counts.append({'exterior_cap':length,'exact_length_candidates':n,
                       'cumulative_candidates':cumulative,
                       'unfiltered_states':144*19**(length-1)})
    return {'verified_cap':cap,'complete_generator_comparison':len(generated),
            'counts':counts,'singleton_states':[[c,list(B)] for c,B in candidates(1)],
            'status':'exact residue-universe counts; no larger-cap cycle search performed'}


if __name__=='__main__':
    print(json.dumps(verify(),sort_keys=True))
