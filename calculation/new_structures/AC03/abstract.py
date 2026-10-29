#!/usr/bin/env python3
"""Independent, sound coefficient-mask overapproximation of genuine decimal carry.
Every real palindromic centre is included despite deliberate loss of correlations.
The 120 overflow bits and carry ports are proved singleton for all centre choices.
"""
from functools import lru_cache
from oracle import tmpl
ALL19=(1<<19)-1
MID=sum(1<<i for i in range(0,19,2))
@lru_cache(None)
def normalize(mask,carry):
    dm=cm=0
    for a in range(19):
        if mask>>a&1:
            for c in (0,1):
                if carry>>c&1:
                    z=a+c
                    dm|=1<<(z%10)
                    cm|=1<<(z//10)
    return dm,cm
@lru_cache(None)
def pair(dm0,dm1):
    out=0
    for a in range(10):
        if dm0>>a&1:
            for b in range(10):
                if dm1>>b&1:out|=1<<(a+b)
    return out
def certify_ports(u,length,cut=280,steps=120):
    C=[0]*length
    source=tmpl(14,100,u,C)
    half=(len(source)-length)//2
    masks=[1<<v for v in source]
    for j in range(length):
        masks[half+j]=MID if length%2 and j==length//2 else ALL19
    ports=[]
    gamma=[]
    for t in range(steps):
        digits=[]
        carry=1   # bitmask of possible incoming carries, initially {0}
        inlet=None
        for j,mask in enumerate(masks):
            if j==cut+t:inlet=carry
            digitmask,carry=normalize(mask,carry)
            digits.append(digitmask)
        # Singletons are the REQUIRED certificate, not an empirical assumption.
        assert inlet in (1,2),(u,length,t,"ambiguous port",inlet)
        assert carry in (1,2),(u,length,t,"ambiguous overflow",carry)
        ports.append(inlet.bit_length()-1)
        overflow=carry.bit_length()-1
        gamma.append(overflow)
        if overflow:digits.append(1<<1)
        masks=[pair(digits[j],digits[-1-j]) for j in range(len(digits))]
    assert gamma==[1,0,0,0]*30
    return ''.join(map(str,ports)),''.join(map(str,gamma))
if __name__=="__main__":
    seen={0:set(),1:set(),2:set()}
    for length in range(7,15):
        for u in range(3):
            p,g=certify_ports(u,length)
            seen[u].add(p)
            print("PORT_CERT",u,length,"ports",p,"clock",g)
    assert all(len(v)==1 for v in seen.values())
    print("PORTS_AND_OVERFLOW_UNIVERSALLY_FORCED_24_CELLS")
