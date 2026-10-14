"""Literal-integer controls for the free-clock local arithmetic.

Independent reversal/addition checks audit the implementation; the report's
carry equations supply the all-length reasoning.
"""
from pathlib import Path
import json
import random
from clock_search import bulk_step,random_row,valid
from check_prefix_extension import phase_relation,prefix_image

HERE=Path(__file__).resolve().parent


def realize(q):
    L=len(q)
    assert q==q[::-1] and q[0]>0 and all(0<=v<=18 for v in q)
    d=[0]*L
    for j in range(L//2):
        d[j]=max(q[j]-9,0)
        d[-j-1]=min(q[j],9)
    if L%2:
        assert q[L//2]%2==0
        d[L//2]=q[L//2]//2
    return int(''.join(map(str,d[::-1])))


def numeric_q(n):
    ds=list(map(int,str(n)))
    return [a+b for a,b in zip(ds,ds[::-1])]


def check():
    rng=random.Random(19620261014)
    local=bulk=positions=0
    for K in range(1,9):
        for j in range(1800):
            prefix=[rng.randrange(1,19)]+[rng.randrange(19) for _ in range(K-1)]
            middle=[rng.randrange(19) for _ in range(1+rng.randrange(12))]
            center=[2*rng.randrange(10)] if j%2 else []
            q=prefix+middle+center+middle[::-1]+prefix[::-1]
            n=realize(q); nxt=n+int(str(n)[::-1]); nq=numeric_q(nxt)
            h=len(nq)-len(q)
            assert h in (0,1)
            rel,_=phase_relation(prefix,nq[:K],h)
            assert nq[K] in rel[q[K]]
            assert any(prefix_image(prefix,e)[:2]==(nq[:K],h) for e in (0,1))
            local+=1
    for r in (3,5,7):
        for _ in range(1500):
            residue=rng.randrange(2*r)
            q=random_row(r,residue,rng)
            if not valid(q,residue):
                continue
            K=rng.randrange(1,9)
            E=[rng.randrange(1,19)]+[rng.randrange(19) for _ in range(K-1)]
            length=8*r+residue
            word=E+[q[j%r] for j in range(length)]+E[::-1]
            n=realize(word);nxt=n+int(str(n)[::-1]);nq=numeric_q(nxt)
            h=len(nq)-len(word)
            expected=bulk_step(q,h)
            for j in range(2*r,length-2*r):
                assert nq[K+j]==expected[j%r]
                positions+=1
            bulk+=1
    result=dict(status='PASS',local_prefix_cases=local,periodic_bulk_cases=bulk,
                checked_interior_positions=positions,ordinary_integer_oracle=True,
                scope='Finite implementation controls; arbitrary-length justification is in STATUS.md')
    (HERE/'arithmetic_controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':
    check()
