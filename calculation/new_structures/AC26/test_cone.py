#!/usr/bin/env python3
"""Independent decimal integer regression and cone property checks (AC26)."""
import random,sys
sys.set_int_max_str_digits(0)
from cone import B5,W5,step_cone,prove_reference,template,realize,step_schoolbook,pairword

def words():
    for a in range(0,19,2):
        v=[9,a,18-a]
        for r in range(3):yield v[r:]+v[:r]

def independent(j,u,c,q,k):
    n=int(''.join(map(str,realize(template(j,u,c,q,k))[::-1])))
    growth=0
    for _ in range(120):
        s=str(n)
        nxt=n+int(s[::-1])
        growth+=len(str(nxt))-len(s)
        n=nxt
    d=list(map(int,str(n)[::-1]))
    actual=pairword(d)
    expected=template(j,u,c,q,k+5)
    first=next((i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b),None)
    assert growth==30
    return first

def check():
    r=random.Random(262626)
    # One-step universal overapproximation: any central coefficients.
    checked=0
    for _ in range(2000):
        L=r.randrange(1,40)
        P=[r.randrange(19) for _ in range(L)]
        P[0]=r.randrange(1,19)
        mid=[r.randrange(19) for _ in range(r.randrange(2,40))]
        full=P+mid+P[::-1]
        if len(full)%2 and full[len(full)//2]%2:continue
        result=step_cone(P)
        if result is None:continue
        prefix,gamma=result
        d=step_schoolbook(realize(full))
        assert pairword(d)[:len(prefix)]==prefix
        assert len(d)==len(full)+gamma
        checked+=1
    assert checked>=1000
    # Every U rotation, both centre parities, all requested widths;
    # actual digit-array states at all 120 steps vs universal cone.
    count=0
    for q,k in ((14,100),(20,80),(40,160),(80,320),(160,640)):
        forced_len,clock=prove_reference(q)
        assert forced_len==70+9*(q-14)
        for idx,u in enumerate(words()):
            j=[r.randrange(19) for _ in range(5)]
            c=[4,4] if idx%2 else [4,14,4]
            d=realize(template(j,u,c,q,k))
            protected=B5+W5*q
            for bit in clock:
                out=step_cone(protected)
                assert out is not None
                protected,gamma=out
                dd=step_schoolbook(d)
                assert len(dd)-len(d)==gamma==int(bit)
                assert pairword(dd)[:len(protected)]==protected
                d=dd
            first=independent(j,u,c,q,k)
            assert first is None or first>=forced_len
            if q==14: assert first is None or first>=70
            count+=1
    print("PASS",checked,"one-step checks;",count,"true bigint controls;",
          count*120,"schoolbook/cone step validations")

if __name__=="__main__":check()
