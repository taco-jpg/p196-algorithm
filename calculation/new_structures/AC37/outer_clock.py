#!/usr/bin/env python3
"""Two-inlet root PREFIX cone: determine real overflow despite unknown middle."""
from verify import B,W

def norm(w,carry):
    out=[]
    for x in w:
        z=x+carry
        out.append(z%10)
        carry=z//10
    return out,carry

def step(prefix):
    L=len(prefix)
    assert L>=1
    low,_=norm(prefix,0)
    high0,g0=norm(prefix[::-1],0)
    high1,g1=norm(prefix[::-1],1)
    if g0!=g1:
        raise AssertionError(('overflow not independent of inner carry',g0,g1))
    g=g0
    alternatives=[]
    for high in (high0,high1):
        if g==0:
            word=[low[i]+high[L-1-i] for i in range(L)]
        else:
            word=[low[0]+1]+[low[i]+high[L-i] for i in range(1,L)]
        alternatives.append(word)
    common=0
    while common<L and alternatives[0][common]==alternatives[1][common]:
        common+=1
    return alternatives[0][:common],g,{'oldlen':L,'newlen':common}

def run():
    # Any q>=14 has this exact mirrored exterior prefix and suffix.
    prefix=B+W*14
    clock=[]
    minsize=len(prefix)
    for t in range(120):
        prefix,g,_=step(prefix)
        assert prefix
        minsize=min(minsize,len(prefix))
        clock.append(g)
    assert clock==[1,0,0,0]*30
    assert minsize==70 and len(prefix)==70
    print('PASS gamma',''.join(map(str,clock)),'30 overflows; guaranteed prefix 160 ->',len(prefix))
    return clock

if __name__=='__main__':
    run()
