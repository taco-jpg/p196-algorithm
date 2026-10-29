#!/usr/bin/env python3
"""Finite 4-state folded-carry relation matrices for a dyadic decimal morphic edge."""
from dataclasses import dataclass

B=10
STATES=[(a,z) for a in (0,1) for z in (0,1)]
I=tuple(1<<i for i in range(4))

def step_matrix(p,q,b=10):
    rows=[]
    for a,z in STATES:
        row=0
        for j,(a2,z2) in enumerate(STATES):
            if a2==(p+a)//b and z==(p+z2)//b and q==(p+a)%b+(p+z2)%b:
                row|=1<<j
        rows.append(row)
    return tuple(rows)

def mul(A,B):
    out=[]
    for bits in A:
        row=0
        for i in range(4):
            if bits&(1<<i):row|=B[i]
        out.append(row)
    return tuple(out)

def accept(M,gamma):
    row=M[STATES.index((0,gamma))]
    return any((row>>i)&1 for i,(a,z) in enumerate(STATES) if a==z)

def closure():
    MA=step_matrix(14,10)
    MB=step_matrix(16,14)
    MP=mul(step_matrix(4,9),step_matrix(14,9))
    X,Y,T=MA,MB,I
    seen={};outputs=[]
    while (X,Y,T) not in seen:
        k=len(outputs)
        seen[(X,Y,T)]=k
        M=mul(MP,T)
        outputs.append({'level':k,'matrix':list(M),'accepted':accept(M,0),
                        'X':list(X),'Y':list(Y),'T':list(T)})
        X,Y,T=mul(X,Y),mul(Y,X),mul(T,Y)
        if len(outputs)>1_000_000:raise RuntimeError('cap')
    first=seen[(X,Y,T)];period=len(outputs)-first
    assert all(v['accepted'] for v in outputs[1:])
    # The level 0 (no tail) also works, though the application uses h>=1.
    print('MONOID_PASS', 'reachable_triples',len(outputs),'preperiod',first,'period',period,
          'all_accepted',all(x['accepted'] for x in outputs))
    print('MORPHIC_MATRICES',outputs)
    return first,period,outputs
if __name__=='__main__':closure()
