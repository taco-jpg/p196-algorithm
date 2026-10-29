#!/usr/bin/env python3
"""Independent arithmetic witness: Python ints, not the C++ digit engine."""
from collections import deque
import sys
sys.set_int_max_str_digits(1000000)
PATH=(17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13)
CYC=(17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13)

def seed(half, patch):
    d=[0]*(half*2)
    for j in range(half):
        p=PATH[j] if j<len(PATH) else CYC[(j-len(PATH))%len(CYC)]
        if patch and j>=half-patch: p=(7*j+11)%19
        d[j]=min(p,9)
        d[2*half-1-j]=p-d[j]
    return int(''.join(map(str,reversed(d))))

def dig(n): return str(n)
def lo(s,j):return int(s[-j-1])
def hi(s,j):return int(s[j])
def front(s,t):
    for j in range(min(len(s),len(t))//2):
        if lo(s,j)+hi(s,j)!=lo(t,j)+hi(t,j):return j
    raise AssertionError('missing front')

def main():
    a=seed(5200,0); b=seed(5200,100)
    old=deque(maxlen=88)
    comparisons=0; seen75=[]; before=0
    for t in range(2001):
        sa,sb=dig(a),dig(b)
        f=front(sa,sb) if t>=912 else None
        if t>=1000:
            oa,ob,of=old[0]
            assert of is not None and f==of-20,(t,f,of)
            assert len(sa)==len(oa)+44 and len(sb)==len(ob)+44
            for r in range(-100,75):
                j,k=f+r,of+r
                for now,past in ((sa,oa),(sb,ob)):
                    assert lo(now,j)==lo(past,k),('low',t,r)
                    assert hi(now,j)==hi(past,k),('high',t,r)
                    comparisons+=2
            j,k=f+75,of+75
            if any(lo(now,j)!=lo(past,k) or hi(now,j)!=hi(past,k)
                   for now,past in ((sa,oa),(sb,ob))):seen75.append(t)
            before+=1
        old.append((sa,sb,f))
        if t<2000:
            a+=int(sa[::-1]);b+=int(sb[::-1]);
    assert comparisons==1001*175*4,comparisons
    assert seen75==[1000,1001],seen75
    print('INDEPENDENT_PYTHON_BIGINT_GLIDER_PASS', 'steps=0..2000',
          'verified_window_t=1000..2000', 'comparisons=',comparisons,
          'first_outer_r75_failures=',seen75)

if __name__=='__main__':main()
