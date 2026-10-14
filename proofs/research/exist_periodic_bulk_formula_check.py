"""Independent literal-integer verification of the period-three core formulas."""
import json
import random
from pathlib import Path


def check(trials=100000):
    rng = random.Random(196)
    stats = dict(trials=0, carry_closure_and_interface=0,
                 overflow_absorptions=0, ordinary=0, integer_steps=0)
    witnesses = []
    def rev(n,k):
        return int(str(n).zfill(k)[::-1])
    def integer(A,B,U,M,k):
        return A*10**(k+M)+sum(U[j%3]*10**(k+j) for j in range(M))+B
    for trial in range(trials):
        k=rng.choice([1,2,3,4])
        A=rng.randrange(10**(k-1),10**k)
        B=rng.randrange(10**k)
        U=[rng.randrange(10) for _ in range(3)]
        r=rng.randrange(3)
        low=B+rev(A,k)
        c0=low//10**k
        Bn=low%10**k
        q=[U[j]+U[(r-1-j)%3] for j in range(3)]
        c=c0
        cs=[]
        V=[]
        for x in q:
            cs.append(c)
            x+=c
            V.append(x%10)
            c=x//10
        stats['trials']+=1
        if c!=c0:
            continue
        stats['carry_closure_and_interface']+=1
        H=A+rev(B,k)+cs[r]
        h=int(H>=10**k)
        if h and H%10!=V[r]:
            continue
        An=H//10 if h else H
        stats['overflow_absorptions' if h else 'ordinary']+=1
        for m in [1,2,3,7]:
            M=3*m+r
            n=integer(A,B,U,M,k)
            actual=n+int(str(n)[::-1])
            expected=integer(An,Bn,V,M+h,k)
            assert actual==expected,(A,B,U,r,H,V,actual,expected)
            stats['integer_steps']+=1
        if len(witnesses)<4 or (h and not any(w['overflow'] for w in witnesses)):
            witnesses.append(dict(A=A,B=B,U=U,r=r,width=k,nextA=An,nextB=Bn,
                                  nextU=V,carry=cs,overflow=h))
    return dict(stats=stats,witnesses=witnesses,random_seed=196)


if __name__ == '__main__':
    result = check()
    Path('exist_periodic_bulk_formula_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
