#!/usr/bin/env python3
"""Symbolic all-centre one-step pump checker for the known decimal p8/m20 lattice.

The middle D[0..m-1] is a vector of INDEPENDENT formal output digits.
The normalizer's outgoing carry from D is universally quantified (0 or 1).
The proof in reports/AgentN10UniversalPumpLemma.md uses block factorization
to reduce arbitrary band counts and centre lengths to this finite boundary check.
"""
import json
from pathlib import Path
P=json.loads((Path(__file__).resolve().parent/"phase.json").read_text())
def norm(a,c):
    digits=[]
    for p in a:
        v=p+c;digits.append(v%10);c=v//10
    return digits,c
def word(t,r,u,m):
    b=P["phase_B"][t];w=P["phase_W"][t]
    lo,c=norm(b+w*r,0)
    hi,g=norm((w*r)[::-1]+b[::-1],u)
    # Each formal centre digit is an independent generator; coefficients carry
    # a constant and a tuple of generator identifiers.
    d=[(x,()) for x in lo]+[(0,(i,)) for i in range(m)]+[(x,()) for x in hi]
    if g:d.append((g,()))
    return d,c,g
def pairs(d):
    return [(d[i][0]+d[-1-i][0],tuple(sorted(d[i][1]+d[-1-i][1])))
            for i in range(len(d))]
def check():
    tests=0
    for t in range(8):
        w=P["phase_W"][t];b=P["phase_B"][t]
        cw0=norm(w,0)[1];cw1=norm(w,1)[1]
        cr0=norm(w[::-1],0)[1];cr1=norm(w[::-1],1)[1]
        assert cw0==cw1 and cr0==cr1,("not absorbing",t)
        assert norm(b,0)[1]==cw0,("not in steady lower carry",t)
        for r in (1,2,3):
            for u in (0,1):
                for m in (0,1,2,3,7,17):
                    a,cin,g=word(t,r,u,m)
                    plus,cin1,g1=word(t,r+1,u,m)
                    assert cin==cin1 and g==g1,(t,r,u,m,"carry mismatch")
                    pa,pb=pairs(a),pairs(plus)
                    nxt=[(x,()) for x in P["phase_W"][(t+1)%8]]
                    target=pa[:39]+nxt+pa[39:-39]+nxt[::-1]+pa[-39:]
                    assert pb==target,(t,r,u,m,"symbolic mismatch")
                    tests+=1
    print(f"PASS {tests} symbolic cases; 8 phases, 3 band counts,"
          " 2 centre-output carries, 6 symbolic centre lengths")
if __name__=="__main__":check()
