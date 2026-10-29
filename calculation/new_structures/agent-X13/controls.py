#!/usr/bin/env python3
"""Published base-9 absorbing and base-50 neutral controls, with symbolic all-k checks."""
from affine_two_counter import Aff,Quadrant,Run,expand as expand_uniform,step_explicit,seed_from_pairs,next_digits,pair_digits
from periodic_affine import Piece,literal,revpieces,expand,derive_pair,equal_symbolic,total,Nonuniform

B9=[8,9,10,13,14,12,3,14,10,0,11,7,10,9,7,8,8,14,15,2,9,7,0,5,8,3,8,11,8,6,8,7,5,14,11,3,9,3,8,14,7,12,8,2,0,12,1,5,13,8,1,16,15,9,1,7,6,2,1,15,15]
W9=[1,1,15,15]
GAM9=[1,1,0,0,0,1,1,0,0,0]

def template9(B,W,t):
    l=Aff(k=4,c=2+sum(GAM9[:t]))
    return literal(B)+[Piece(tuple(W),l)]+literal(B[::-1])

def b9():
    G=Quadrant(3,3)
    B=B9;W=W9;check=[]
    for t,g in enumerate(GAM9):
        inp=template9(B,W,t)
        assert expand(inp,3,3)==expand(inp,3,53)[::1]
        assert expand(inp,3,3)==expand(inp,3,3)[::-1]
        new,gamma=derive_pair(9,inp,G)
        assert gamma==g,(t,gamma,g)
        # Infer one next state and *independently* prove it for ALL k>=3.
        sample=expand(new,3,3)
        B2=sample[:61]
        W2=sample[61:65]
        expected=template9(B2,W2,t+1)
        ok,bad=equal_symbolic(new,expected,G)
        assert ok,(t,bad)
        for k in (3,4,9,50):
            p=expand(inp,k,k);n=step_explicit(9,p)
            assert n==expand(expected,k,k)
        check.append({'t':t,'gamma':gamma,'W':W,'next_W':W2,'B_length':len(B)})
        B,W=B2,W2
    assert B==B9 and W==W9
    assert total(template9(B,W,10))==total(template9(B9,W9,0))+Aff(c=4)
    return {'base':9,'period':10,'k_min':3,'band_length':'4*k+2','counter_gain':1,
            'edges':check,'comparisons':G.comparisons,'cycle_return':True}

B50=[48,52,43,61,26,44,60,28,40,67,63,70,57,33,31,36,26,45,58,32,33,32,34,30,37,73,52,42,62,73,51,44,59,30,37,24]
C50=[62,15,22,32,32,22,15,62]
# published trim stream makes left/right neutral-band lengths vary by phases:
OFF50=[0,1,0,2,1]
WIDTH50=[36,35,36,35,36]
CLEN50=[8,8,9,7,8]
GAM50=[0,1,0,1]

def template50(B,C,t):
    l=Aff(k=1,c=OFF50[t]);return literal(B)+[Piece((49,),l)]+literal(C)+[Piece((49,),l)]+literal(B[::-1])

def b50():
    G=Quadrant(12,12);B=B50;C=C50;check=[]
    for t,g in enumerate(GAM50):
        inp=template50(B,C,t)
        assert expand(inp,12,12)==expand(inp,12,12)[::-1]
        new,gamma=derive_pair(50,inp,G)
        assert gamma==g,(t,gamma,g)
        n=expand(new,12,12)
        width=WIDTH50[t+1];centre=CLEN50[t+1];q=12+OFF50[t+1]
        B2=n[:width]
        C2=n[width+q:width+q+centre]
        expected=template50(B2,C2,t+1)
        ok,bad=equal_symbolic(new,expected,G)
        assert ok,(t,bad)
        for k in (12,13,30,100):
            p=expand(inp,k,k)
            assert step_explicit(50,p)==expand(expected,k,k)
        check.append({'t':t,'gamma':gamma,'B_length':len(B),'C_length':len(C),'band_offset':OFF50[t]})
        B,C=B2,C2
    assert B==B50 and C==C50
    return {'base':50,'period':4,'k_min':12,'band_length':'k','counter_gain':1,
            'edges':check,'comparisons':G.comparisons,'cycle_return':True}

if __name__=='__main__':
    import json
    print(json.dumps([b9(),b50()],indent=2))
