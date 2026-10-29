#!/usr/bin/env python3
"""W13: exact local p8/20 non-gauge erasure and independent ordinary-int controls."""
from itertools import product
from random import Random
import json

B=[17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]
W=[17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]
OPTIONS=[(11,14,3)]+[(6+9*a,6+9*b,7+9*c) for a,b,c in product((0,1),repeat=3)]
def seed(q,choices=()):
    assert q>=2 and (not choices or q>=30+10*len(choices))
    h=B+W*q+[0]
    for m,k in enumerate(choices):
        s=39+20*(30+10*m)+5
        h[s:s+3]=OPTIONS[k]
    return h+h[-2::-1]
def pair(d):
    return [d[i]+d[-1-i] for i in range(len(d))]
def coeff_step(p):
    d=[];c=0
    for x in p:
        z=x+c;d.append(z%10);c=z//10
    if c:d.append(c)
    return pair(d)
def digits(p):
    assert p==p[::-1] and p[len(p)//2]%2==0
    d=[0]*len(p)
    for i in range(len(p)//2):
        d[i]=min(9,p[i]);d[-1-i]=p[i]-d[i]
    d[len(p)//2]=p[len(p)//2]//2
    assert d[-1] and pair(d)==p
    return d
def literal_step(d):
    r=[];c=0
    for i in range(len(d)):
        z=d[i]+d[-1-i]+c;r.append(z%10);c=z//10
    if c:r.append(c)
    return r
def check():
    s=39+3*20+5;base=seed(8)
    assert base[s:s+3]==[11,14,3]
    guards=[];supports=[]
    for v in OPTIONS[1:]:
        a=base[:];b=base[:]
        for i,x in enumerate(v):b[s+i]=b[-s-i-1]=x
        g=[];sp=[]
        for t in range(4):
            diff=[j-s for j in range(len(a)//2) if a[j]!=b[j]]
            sp.append(diff)
            if t<3:
                g.append((a[s-1],a[s+4]))
                assert a[s-1]==b[s-1] and a[s+4]==b[s+4]
                assert a[s-1]!=9 and a[s+4]!=9
            if t<3:a,b=coeff_step(a),coeff_step(b)
        assert sp==[[0,1,2],[0,1,2,3],[0,1,2,3],[]],sp
        assert g==[(17,1),(12,10),(5,1)],g
        guards=g;supports=sp
    q=65;M=3
    baseline=[seed(q)]
    for _ in range(3):baseline.append(coeff_step(baseline[-1]))
    for tup in product(range(9),repeat=M):
        p=seed(q,tup)
        for t in range(3):
            if any(tup):assert p!=baseline[t]
            p=coeff_step(p)
        assert p==baseline[3]
    patterns=[(0,0,0),(1,1,1),(8,8,8),(3,5,7)]
    rng=Random(20261028)
    patterns += [tuple(rng.randrange(9) for _ in range(3)) for _ in range(32)]
    target=None
    for pat in patterns:
        d=digits(seed(65,pat));n=int(''.join(map(str,d[::-1])))
        assert str(n)!=str(n)[::-1]
        for t in range(4):
            d=literal_step(d)
            n+=int(str(n)[::-1])
            assert ''.join(map(str,d[::-1]))==str(n)
            assert str(n)!=str(n)[::-1]
        assert target is None or n==target
        target=n
    p=seed(65);odd=[]
    for t in range(4):
        idx=next(i for i in range(39) if p[i]%2)
        odd.append(idx);p=coeff_step(p)
    assert odd==[0,1,0,4],odd
    return dict(label="COMPUTED",eight_non_gauge_replacements=OPTIONS[1:],
                first_three_overflows="101",difference_supports=supports,
                carry_reset_guards=guards,q65_M3_exhaustive=729,
                independent_bigint_patterns=36,odd_exterior_witnesses_t0_t3=odd,
                universal_statement="9^M seeds coalesce as pairwords at t3 and integers at t4")
if __name__=="__main__":
    print(json.dumps(check(),indent=2))
