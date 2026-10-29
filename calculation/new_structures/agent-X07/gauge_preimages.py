#!/usr/bin/env python3
"""Independent Python integer controls for the X07 mirror-gauge fibres.

For m=10+18k, set r=m/2; choose palindromic m-digit A with outer
mirror pair 6, other pairs 4, with disjoint paired offsets (+d,-d),
d in {-1,0,1}. All charge-8 words map to exactly q'=10^m+1.
"""
from itertools import product
from collections import Counter
import json
import sys

sys.set_int_max_str_digits(200000)


def make_a(m, choices):
    assert (m-10)%18==0 and m>=10
    r=m//2
    groups=(r-1)//2
    assert len(choices)==groups
    vals=[6]+[4]*(r-1)
    for k,d in enumerate(choices):
        vals[1+2*k]+=d
        vals[2+2*k]-=d
    lo=vals+vals[::-1]
    assert len(lo)==m and all(0<=x<=8 for x in lo)
    a=int(''.join(map(str,lo[::-1])))
    assert str(a)==str(a)[::-1] and len(str(a))==m
    assert sum(lo)%9==8
    return a


def check_config(m,h,choices):
    A=make_a(m,choices)
    M=10**h-1
    q0=10**m-A
    N=M*q0
    assert q0%9==2 and N!=int(str(N)[::-1])
    target=M*(10**m+1)
    assert N+int(str(N)[::-1])==target,(m,h,choices)
    assert target!=int(str(target)[::-1])
    return A,q0


def main():
    report={}
    for m in (10,28,46):
        k=(m//2-1)//2
        h=m+2
        seen=set()
        count=0
        for choices in product((-1,0,1),repeat=k):
            if m==46 and count>=1000: break
            A,q=check_config(m,h,choices)
            assert A not in seen
            seen.add(A);count+=1
        assert count == (3**k if m<46 else 1000)
        report[str(m)]={'gauge_pairs':k,'full_family_cardinality':3**k,
                        'bigint_controls':count,'h':h,'common_q':str(10**m+1),
                        'example_A':str(next(iter(seen)))}
    # Adversarial control: charge-preserving, non-mirrored changes must break
    # the common successor, even though the mutated seed remains protected.
    m,h=10,12
    baseline=make_a(m,(0,0))
    low=[int(z) for z in str(baseline)[::-1]]
    low[1]+=1
    low[2]-=1
    assert sum(low)%9==8 and low[-1]<=8
    broken=int(''.join(map(str,low[::-1])))
    assert broken!=int(str(broken)[::-1])
    M=10**h-1
    Q=10**m-broken
    real=M*Q
    assert real+int(str(real)[::-1])!=M*(10**m+1)
    report['mutation_control']={'m':m,'A':broken,'did_not_merge':True}
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':main()
