#!/usr/bin/env python3
"""Independent Python big-int test of the 0-vs-18 dyadic central perturbation."""
import sys

EXPECTED={4:6,5:84,6:280,7:587,8:1355,9:3160,10:5796,11:11546,12:23223}

def seed(h,central):
    word='A'
    for _ in range(h):word=''.join('AB' if c=='A' else 'BA' for c in word)
    lower=[4]+[14 if c=='A' else 16 for c in word]
    lo=[1]+[c-9 for c in lower[1:]]
    hi=[3]+[9]*(len(lower)-1)
    digits=lo+[central//2]+hi[::-1]
    assert all(digits[i]+digits[-i-1]==lower[i] for i in range(len(lower)))
    assert digits[len(lower)]*2==central
    return int(''.join(str(x) for x in digits[::-1]))

def pairhead(n,k=16):
    x=str(n)
    length=len(x)
    return tuple(int(x[-1-i])+int(x[i]) for i in range(min(k,length)))

def run(h,k=16):
    a,b=seed(h,0),seed(h,18)
    limit=EXPECTED[h]
    for t in range(limit+1):
        ha,hb=pairhead(a,k),pairhead(b,k)
        if t<limit:assert ha==hb,(h,t,ha,hb)
        else:assert ha!=hb,(h,t,ha,hb)
        if t<limit:
            sa,sb=str(a),str(b)
            a+=int(sa[::-1]);b+=int(sb[::-1])
    print('BIGINT_SHIELD_PASS',h,k,limit,len(str(a)),len(str(b)))

if __name__=='__main__':
    sys.set_int_max_str_digits(0)
    levels=[int(x) for x in sys.argv[1:]] if len(sys.argv)>1 else [4,5,6,7,8,9]
    for h in levels:run(h)
