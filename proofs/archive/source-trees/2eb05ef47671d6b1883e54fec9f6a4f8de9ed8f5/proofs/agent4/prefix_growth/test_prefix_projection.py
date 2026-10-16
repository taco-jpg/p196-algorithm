"""Independent ordinary-integer controls for the three-column projection."""
from __future__ import annotations
import json
from pathlib import Path
import random
from generate_certificate import step


def direct_formula(s, e):
    a,b,c=s
    l1=a//10; l2=(b+l1)//10
    d0=a%10; d1=(b+l1)%10; d2=(c+l2)%10
    r2=(c+e)//10; r1=(b+r2)//10
    gamma=(a+r1)//10
    h0=(a+r1)%10; h1=(b+r2)%10; h2=(c+e)%10
    return ((d0+h0,d1+h1,d2+h2) if gamma==0 else (d0+1,d1+h0,d2+h1)),gamma


def pair_of(n):
    ds=tuple(map(int,str(n)[::-1]))
    return tuple(a+b for a,b in zip(ds,ds[::-1]))


def realize(q):
    ds=[0]*len(q)
    for i in range(len(q)//2):
        ds[i]=min(9,q[i]); ds[-1-i]=q[i]-ds[i]
    if ds[-1]==0:
        ds[0]-=1; ds[-1]=1
    if len(q)%2:
        ds[len(q)//2]=q[len(q)//2]//2
    n=int(''.join(map(str,ds[::-1])))
    assert pair_of(n)==q
    return n


def control(n, prescribed_e=None):
    q=pair_of(n)
    assert len(q)>=6
    carry=0
    for a in q[:-3]:
        carry=(a+carry)//10
    if prescribed_e is not None:
        assert carry==prescribed_e
    expected,gamma=direct_formula(q[:3],carry)
    assert (expected,gamma)==step(q[:3],carry)
    nxt=n+int(str(n)[::-1])
    assert pair_of(nxt)[:3]==expected
    assert len(str(nxt))-len(str(n))==gamma


def main():
    count=0
    for a in range(1,19):
        for b in range(19):
            for c in range(19):
                for e in (0,1):
                    # A central reset realizes either inner carry, and the even
                    # central coefficient is valid for a canonical pair word.
                    q=(a,b,c,18*e,c,b,a)
                    control(realize(q),e)
                    count+=1
    random_count=10000
    r=random.Random(19640042)
    for _ in range(random_count):
        width=r.randrange(6,101)
        n=int(str(r.randrange(1,10))+''.join(str(r.randrange(10)) for _ in range(width-1)))
        control(n)
    result={'status':'PASS','all_prefix_control_pairs':count,
            'random_ordinary_integers':random_count,'seed':19640042,
            'scope':'Independent implementation controls, not the all-width proof or a Lychrel witness.'}
    Path('prefix-projection-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
