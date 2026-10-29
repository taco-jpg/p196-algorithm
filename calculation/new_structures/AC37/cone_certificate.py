#!/usr/bin/env python3
"""Sound two-carry CENTRAL cone for the decimal p12/m9 phase-4 macro.

If the symmetric pairword P has a known centred substring S, the carry entering
S during normalization is an arbitrary bit 0/1. Under the specified genuine
overflow g, for j in [0,len(S)-g), the next pairword coefficient is
d[g+j]+d[len(S)-1-j]. Both indices lie in S. Normalize with BOTH inlet bits,
retain the common symmetric centre and discard contaminated ends. Induction
makes the result exact for every unknown exterior, with no finite-radius
assumption and no strict intermediate-W9 pruning.
"""
from collections import Counter

def norm_digits(w,carry):
    out=[]
    for x in w:
        z=x+carry
        out.append(z%10)
        carry=z//10
    return out

def step(core,gamma):
    assert gamma in (0,1) and core==core[::-1]
    M=len(core)
    d0=norm_digits(core,0)
    d1=norm_digits(core,1)
    L=M-gamma
    assert L>0
    p0=[d0[gamma+j]+d0[M-1-j] for j in range(L)]
    p1=[d1[gamma+j]+d1[M-1-j] for j in range(L)]
    assert p0==p0[::-1] and p1==p1[::-1]
    bad=[min(j,L-1-j)+1 for j in range(L) if p0[j]!=p1[j]]
    trim=max(bad,default=0)
    safe=p0[trim:L-trim]
    assert safe==safe[::-1]
    return safe,gamma+trim

def all_u():
    for a in range(0,19,2):
        w=[9,a,18-a]
        for r in range(3):
            yield w[r:]+w[:r]

def propagate(U,C,k=100,steps=120):
    core=U*k+C+(U*k)[::-1]
    shift=0
    for t in range(steps):
        core,increment=step(core,int(t%4==0))
        shift+=increment
        assert core
    assert len(core)+2*shift==6*k+len(C)+30
    return core,shift

def flank_window(core,C):
    start=(len(core)-len(C))//2
    assert start>=1
    return core[start-1:start+len(C)+1]

def certificate():
    words=list(all_u())
    assert len(words)==len({tuple(u) for u in words})==30
    result={}
    for C in ([4,4],[4,14,4]):
        hist=Counter()
        for rank,U in enumerate(words):
            core,shift=propagate(U,C)
            actual=flank_window(core,C)
            wanted=[U[-1]]+C+[U[-1]]
            assert len(core)>=328
            assert actual!=wanted,(rank,U,C,actual,wanted)
            hist[(shift,len(core))]+=1
            print('CELL',rank,'C',','.join(map(str,C)),'U',','.join(map(str,U)),
                  'cut',shift,'got',','.join(map(str,actual)),
                  'want',','.join(map(str,wanted)))
        assert sorted(hist.values())==[10,10,10]
        result[tuple(C)]=hist
        print('PASS centre',C,'30/30 disjoint windows','cuts',dict(sorted(hist.items())))
    return result

if __name__=='__main__':
    certificate()
