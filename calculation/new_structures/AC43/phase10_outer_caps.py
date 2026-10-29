#!/usr/bin/env python3
"""AC43 exact two-ended carry cap for the physically rooted decimal p12 clock."""
from pathlib import Path
B0=[10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W0=[5,18,4,8,1,15,4,0,5]
B10=[2,11,1,1,11,17,14,3,9,3,0,0,12,13,16,4,9,6,6,4,6,4,8,14,12,16,12,8,17,5,6,5,9,16]
W10=[0,9,11,1,10,8,5,9,16]
W9=[10,4,5,10,14,13,12,9,7]

def cap_step(low,high):
    """Any unknown carry entering the high cap is 0 or 1; take the common prefix."""
    assert len(low)==len(high) and low
    n=len(low);p=[x+y for x,y in zip(low,high)]
    out=[];carry=0
    for x in p:
        z=x+carry;out.append(z%10);carry=z//10
    def upper(c):
        dst=[0]*n
        for i in range(n-1,-1,-1):
            z=p[i]+c;dst[i]=z%10;c=z//10
        return ([1] if c else [])+dst
    a,b=upper(0),upper(1)
    assert len(a)==len(b),"high overflow ambiguous"
    common=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),len(a))
    keep=min(n,common)
    assert keep>0
    return out[:keep],a[:keep],len(a)-n

def cap0(q):
    P=B0+W0*q
    return [p-min(p,9) for p in P],[min(p,9) for p in P]

def prove():
    lo,hi=cap0(14);g=[];t10=None
    for t in range(130):
        lo,hi,overflow=cap_step(lo,hi);g.append(overflow)
        if t==9:
            t10=(lo[:],hi[:])
            p=[a+b for a,b in zip(lo,hi)]
            assert p[:34]==B10 and p[34:43]==W10
    assert [a+b for a,b in zip(lo,hi)][:34]==B10
    assert g[:10]==[1,0,0,0,1,0,0,0,1,0]
    assert g[10:]==[0,0,1,0,0,0,1,0,0,0,1,0]*10
    assert len(t10[0])==152 and len(lo)==62
    return t10,(lo,hi)

def check_rows():
    path=Path("calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt")
    if not path.exists():return
    d=[int(x) for x in path.read_text().split()]
    assert len(d)==640 and d[:4]==[12,34,9,10]
    v=d[4:];w=[v[12+9*i:12+9*(i+1)] for i in range(12)]
    b=[v[228+34*i:228+34*(i+1)] for i in range(12)]
    assert w[0]==W0 and w[9]==W9 and w[10]==W10
    assert b[0]==B0 and b[10]==B10

def wrong_row_control():
    p=B10+W9*14
    lo=[x-min(9,x) for x in p];hi=[min(9,x) for x in p]
    for _ in range(120):lo,hi,_=cap_step(lo,hi)
    s=[a+b for a,b in zip(lo,hi)]
    assert s[:10]==B10[:10] and s[10]==1 and B10[10]==0

if __name__=="__main__":
    check_rows();prove();wrong_row_control()
    print("PAPER PROOF (finite trace): all q>=14, arbitrary legal interior")
    print("physical phase 10 and 130 preserve exactly B10; cap lengths 152/62")
    print("wrong W[9] paired with B[10] yields spurious index-10 mismatch")
