#!/usr/bin/env python3
"""W13 phase-shifted four-step, two-preimage repair. Exact arithmetic tests."""
from itertools import product
from random import Random
import json
from three_step_eraser import coeff_seed,next_pair,digits,pair,literal_step

def canonical_digits(p):
    d=[0]*len(p)
    for i in range(len(p)//2):
        d[i]=min(9,p[i]);d[-i-1]=p[i]-d[i]
    if len(p)%2: assert p[len(p)//2]%2==0;d[len(p)//2]=p[len(p)//2]//2
    if d[-1]==0:
        assert d[0]>0
        d[0]-=1;d[-1]+=1
    assert d[-1]>0 and pair(d)==p
    return d
OPTIONS=((3,2,7),(5,16,0),(1,6,5))

def source(q,choices=()):
    assert q>=30+10*len(choices)
    p=next_pair(coeff_seed(q))
    for m,c in enumerate(choices):
        assert c in (0,1,2)
        j=39+20*(30+10*m)+10
        assert p[j:j+3]==list(OPTIONS[0])
        for k,v in enumerate(OPTIONS[c]):
            p[j+k]=p[-j-1-k]=v
    return p

def proof_controls():
    q=65; base=source(q)
    s=39+20*30+10
    single={}; guardref=[(10,8),(1,17),(6,8),(13,17)]
    expected_support=[[0,1,2],[0,1,2],[0,1,2,3],[0,1,2,3],[]]
    for c in (1,2):
        p=source(q,(c,))
        a=base[:];b=p[:];supports=[];guards=[];diff_t1=None
        for t in range(5):
            support=[i-s for i in range(len(a)//2) if a[i]!=b[i]]
            supports.append(support)
            if t<4:
                guards.append((a[s-1],a[s+4]))
                assert a[s-1]==b[s-1] and a[s+4]==b[s+4]
                assert a[s-1]!=9 and a[s+4]!=9
            if t==1:diff_t1=(a[s:s+3],b[s:s+3])
            if t<4:a,b=next_pair(a),next_pair(b)
        assert supports==expected_support,(c,supports)
        assert guards==guardref,(c,guards)
        assert diff_t1==([7,4,15],([12,12,2] if c==1 else [3,12,11]))
        single[c]={'source_replacement':OPTIONS[c],'supports':supports,'guards':guards,'t1':diff_t1}
    expected=base[:]
    for _ in range(4):expected=next_pair(expected)
    for cs in product(range(3),repeat=3):
        p=source(q,cs)
        for _ in range(4):p=next_pair(p)
        assert p==expected,cs
    patterns=[(0,0,0),(1,1,1),(2,2,2),(1,2,1)]
    rng=Random(20261028)
    patterns.extend([tuple(rng.randrange(3) for _ in range(3)) for _ in range(32)])
    common=None
    for cs in patterns:
        d=canonical_digits(source(q,cs));num=int(''.join(map(str,d[::-1])))
        assert str(num)!=str(num)[::-1]
        for t in range(5):
            d=literal_step(d)
            num+=int(str(num)[::-1])
            assert ''.join(map(str,d[::-1]))==str(num)
            assert str(num)!=str(num)[::-1]
        assert common is None or common==num,cs
        common=num
    p=base[:];odd=[]
    for _ in range(5):
        odd.append(next(j for j in range(39) if p[j]&1))
        p=next_pair(p)
    assert odd==[1,0,4,0,7],odd
    return {'label':'COMPUTED','distinct_root_options':list(OPTIONS),
            'local_tables':single,'q65_M3_combinations':27,
            'independent_python_int_controls':len(patterns),
            'odd_exterior_witnesses_t0_to_t4':odd,
            'claim':'Any M, q>=30+10M: 3^M distinct canonical decimal seeds have identical pairword after 4 steps, exact same integer after 5'}

if __name__=='__main__':
    print(json.dumps(proof_controls(),indent=2))
