#!/usr/bin/env python3
"""Finite independent four-step controls; no all-r theorem is claimed here."""
from pathlib import Path
import hashlib
import json

OUT = Path(__file__).resolve().parent


def normalize(q):
    c, d, carries = 0, [], [0]
    for x in q:
        c, digit = divmod(x+c, 10)
        d.append(digit)
        carries.append(c)
    while c:
        c, digit = divmod(c, 10)
        d.append(digit)
    assert d[-1] > 0
    return d, carries


def pair(d):
    return [x+y for x,y in zip(d,d[::-1])]


def g(q):
    return pair(normalize(q)[0])


def phi(q):
    return [x+y for x,y in zip(q+[0],[0]+q)]


def six(r,p,a,b,c):
    return [p]+[0]*(r-1)+[a,b,c,c,b,a]+[0]*(r-1)+[p]


def realize(q,choice):
    d=[0]*len(q)
    for i in range((len(q)+1)//2):
        j=len(q)-1-i
        if i==j:
            assert q[i]%2==0
            d[i]=q[i]//2
        else:
            lo,hi=max(0,q[i]-9),min(9,q[i])
            if i==0:
                hi=min(hi,q[i]-1)
            d[i]=(lo,hi,(lo+hi)//2)[choice]
            d[j]=q[i]-d[i]
    assert all(0<=x<=9 for x in d) and d[-1]>0 and pair(d)==q
    return sum(x*10**i for i,x in enumerate(d))


def main():
    rs=list(range(1,33))+[64,128]
    checks=0
    boundary=None
    for r in rs:
        a=[1]+[0]*r+[10,6,6,10]+[0]*r+[1]
        q=phi(a)
        aa,qq=[a],[q]
        for _ in range(4):
            aa.append(g(aa[-1]))
            qq.append(g(qq[-1]))
        d=six(r,4,2,1,7)
        e=six(r,16,8,5,9)
        assert aa[2]==d and qq[2]==phi(d)
        assert aa[3]==six(r,8,4,2,14) and aa[4]==e
        assert all(len(x)==2*r+6 for x in aa)
        assert all(len(x)==2*r+7 for x in qq)
        assert qq[1]!=phi(aa[1]) and qq[3]!=phi(aa[3])
        assert (qq[4]==phi(e))==(r>=2)
        nd,cc=normalize(aa[3])
        assert nd[r:r+6]==[4,2,4,5,3,4]
        assert [i for i,c in enumerate(normalize(aa[2])[1]) if c]==[]
        assert [i for i,c in enumerate(normalize(qq[2])[1]) if c]==[r+4]
        assert [i for i,c in enumerate(cc) if c]==[r+3,r+4]
        if r>=2:
            assert [i for i,c in enumerate(normalize(qq[3])[1]) if c]==[r+3,r+5]
            expected=[0]*(2*r+7)
            expected[r+2],expected[r+4]=1,-1
            defect=[x-y for x,y in zip(normalize(qq[3])[0],normalize(phi(aa[3]))[0])]
            assert defect==expected
            assert normalize(phi(aa[3]))[0]==phi(nd)
        else:
            defect=[x-y for x,y in zip(qq[4],phi(e))]
            assert defect==[1,-20,1,0,0,0,1,-20,1]
            boundary={'component_states':aa,'whole_states':qq,'overlap_of_actual_component_time4':phi(e),
                      'signed_time4_defect':defect,'wholeThree_incoming_carry_indices':[i for i,c in enumerate(normalize(qq[3])[1]) if c]}
        for choice in range(3):
            n=realize(q,choice)
            n0=n
            for t in range(1,5):
                n+=int(str(n)[::-1])
                assert str(n)!=str(n)[::-1]
                digits=[int(x) for x in str(n)[::-1]]
                assert pair(digits)==qq[t] and len(digits)==2*r+7
            assert n0>0
            checks+=1
    result={'status':'PASS_FINITE_DIAGNOSTICS_ONLY','not_an_all_parameter_theorem':True,
            'fixed_parameters':{'p':1,'u':10,'v':6},'r_values':rs,
            'spacers_checked':len(rs),'canonical_realization_checks':checks,
            'realization_choices_not_asserted_distinct':True,'r1_boundary':boundary,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'finite-controls-result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='r1_boundary'}))
    print('r=1 time-four component:',boundary['component_states'][4])
    print('r=1 time-four whole:',boundary['whole_states'][4])
    print('r=1 signed defect:',boundary['signed_time4_defect'])


if __name__=='__main__':
    main()
