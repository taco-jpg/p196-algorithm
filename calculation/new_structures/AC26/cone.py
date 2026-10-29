#!/usr/bin/env python3
"""Sound two-ended 120-step decimal pairword exterior cone, phase 5.

No strict-per-phase W9 restriction. The *only* unknown at the high
protected suffix is its incoming carry, always 0 or 1.
"""
B5=[1,5,11,12,9,10,8,3,11,6,14,16,10,0,14,12,9,8,7,2,8,12,5,17,14,8,9,13,14,17,14,12,15,13]
W5=[12,9,7,10,4,5,10,14,13]

def norm(coeffs, carry):
    digits=[]
    for a in coeffs:
        s=a+carry
        digits.append(s%10)
        carry=s//10
    return digits,carry

def step_cone(prefix):
    """Return (common next prefix, forced overflow); None if ambiguous."""
    low,_=norm(prefix,0)
    options=[]
    for incoming in (0,1):
        high,overflow=norm(prefix[::-1],incoming)
        high=high[::-1] # highest-significance digit first
        out=[low[i]+(overflow if i==0 else high[i-1])
             if overflow else low[i]+high[i]
             for i in range(len(prefix))]
        options.append((overflow,out))
    if options[0][0]!=options[1][0]:
        return None
    a,b=options[0][1],options[1][1]
    cut=0
    while cut<len(prefix) and a[cut]==b[cut]:
        cut+=1
    return a[:cut],options[0][0]

def prove_reference(q=14):
    """Finite exact calculation supporting universal arbitrary-interior lemma."""
    p=B5+W5*q
    clock=[]
    for t in range(120):
        result=step_cone(p)
        if result is None:
            raise AssertionError(("ambiguous_overflow",t,len(p)))
        p,gamma=result
        clock.append(gamma)
        if not p:
            raise AssertionError(("cone_empty",t))
    expected=B5+W5*q
    assert p==expected[:len(p)]
    assert clock==([0,0,0,1]*30)
    return len(p),''.join(str(x) for x in clock)

def pairword(d):
    return [d[i]+d[-1-i] for i in range(len(d))]

def template(J,U,C,q,k):
    H=B5+W5*q+J+U*k
    return H+C+H[::-1]

def realize(P):
    assert P==P[::-1]
    d=[0]*len(P)
    for i in range(len(P)//2):
        high=min(9,P[i])
        d[i]=P[i]-high
        d[-1-i]=high
    if len(P)%2:
        assert P[len(P)//2]%2==0
        d[len(P)//2]=P[len(P)//2]//2
    assert d[-1]!=0
    return d

def step_schoolbook(d):
    carry=0
    out=[]
    for i in range(len(d)):
        a=d[i]+d[-1-i]+carry
        out.append(a%10)
        carry=a//10
    if carry: out.append(carry)
    return out

if __name__=="__main__":
    for q in (8,14,20,40,80,160):
        print("q",q,"forced_prefix_and_clock",prove_reference(q))
