#!/usr/bin/env python3
"""Independent ordinary-integer replay of six N21 trajectories (not a proof)."""
import sys
sys.set_int_max_str_digits(1000000)
from packet_train import N,ANCHORS,background,insert,pair_step
def realize(q):
    m=len(q);d=[0]*m
    for i in range(m//2):
        x=q[i]
        if i==0:
            a=max(1,x-9);z=x-a
            if z==0:a-=1;z+=1
        else:
            a=min(x,9);z=x-a
        assert 0<=a<=9 and 0<=z<=9
        d[i],d[m-1-i]=a,z
    assert d[-1]>0
    num=int(''.join(map(str,d[::-1])))
    assert from_integer(num)==q
    return num
def from_integer(x):
    s=str(x)
    return [int(a)+int(b) for a,b in zip(reversed(s),s)]
def run():
    root=background()
    q=[root]+[insert(root,(a,)) for a in ANCHORS]+[insert(root,ANCHORS)]
    ints=[realize(p) for p in q]
    first_bad=None
    for t in range(821):
        canonical=[from_integer(v) for v in ints]
        assert canonical==q,('arithmetic mismatch',t)
        assert all(str(v)!=str(v)[::-1] for v in ints),('palindrome',t)
        lower=len(q[0])//2
        fails=[i for i in range(lower) if canonical[0][i]+sum(s[i]-canonical[0][i] for s in canonical[1:-1])!=canonical[-1][i]]
        if fails and first_bad is None:first_bad=t
        if t==820:
            assert fails==[648,649,650,1152,1153,1154,1656,1657,1658]
            break
        ints=[v+int(str(v)[::-1]) for v in ints]
        q=[pair_step(p) for p in q]
    assert first_bad==820
    print('BIGINT_PASS 6 canonical decimal seeds, 821 states (0..820), no palindromes, exact full pairwords, first nonlinear step 820')
if __name__=='__main__':run()
