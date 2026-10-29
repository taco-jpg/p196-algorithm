#!/usr/bin/env python3
"""Independent W14 carry-normalization/mask checker (no C++ imports)."""
import random


def normalize_pairs(p, b):
    c = 0
    d = []
    for x in p:
        z = x + c
        d.append(z % b)
        c = z // b
    if c:
        d.append(c)
    return [d[i] + d[-i - 1] for i in range(len(d))]


def safe_sites(a, b):
    n = len(a)
    return [i for i in range(1, n - 1)
            if a[i] not in (0, b - 1, 2*b - 2)
            and a[i-1] != b - 1 and a[i+1] != b - 1]


def make_digits(a, b):
    h = len(a)
    d = [0] * (2*h)
    for i, x in enumerate(a):
        d[i] = max(0, x - b + 1)
        d[-i-1] = min(b-1, x)
    assert d[-1]
    return d


def add_reverse(d, b):
    n = len(d)
    carry = 0
    out = []
    for i in range(n):
        v = d[i] + d[n-1-i] + carry
        out.append(v % b)
        carry = v // b
    if carry:
        out.append(carry)
    return out


def folded(d):
    return [d[i]+d[-i-1] for i in range(len(d))]


def one(b, a, mask):
    assert a[0] >= b
    p = a + a[::-1]
    s = safe_sites(a,b)
    q = a[:]
    for k,i in enumerate(s):
        if (mask >> k) & 1:
            q[i] += b-1 if a[i] < b-1 else -(b-1)
    pp = q + q[::-1]
    if normalize_pairs(p,b) != normalize_pairs(pp,b):
        raise AssertionError(('pairword erasure', b, a, q))
    d = make_digits(a,b)
    dd = make_digits(q,b)
    assert folded(d) == p and folded(dd) == pp
    assert folded(add_reverse(d,b)) == folded(add_reverse(dd,b))
    assert add_reverse(add_reverse(d,b),b) == add_reverse(add_reverse(dd,b),b)
    return len(s)


def load_rows():
    raw=[s.strip() for s in open('rows.txt') if s.strip() and not s.startswith('#')]
    assert len(raw)==16
    def cv(s):return [int(ch,19) for ch in s]
    B,W=cv(raw[0]),cv(raw[8]);assert len(B)==39 and len(W)==20
    return B,W


def main():
    random.seed(14002000)
    tested=0
    for b in range(3,32):
        for _ in range(200):
            h=random.randrange(4,81)
            a=[random.randrange(2*b-1) for _ in range(h)]
            a[0]=random.randrange(b,2*b-1)
            s=safe_sites(a,b)
            mask=random.getrandbits(len(s))
            one(b,a,mask)
            tested+=1
    print('PASS',tested,'random independent pairword/ordinary-digit local mask controls for bases 3..31')
    B,W=load_rows()
    for q in (1,2,3,4,10,300,301):
        a=B+W*q
        s=safe_sites(a,10)
        assert len(s)==15*q+18,(q,len(s))
        for _ in range(20):
            one(10,a,random.getrandbits(len(s)))
        print('q',q,'half length',len(a),'safe gauge bits',len(s),'20 masked genuine-digit controls PASS')
    # Probe failure of removing neutral-neighbour restriction (strict checker control).
    a=[17,1,9,3,1,8]
    p=a+a[::-1]
    q=a[:];q[1]+=9
    assert normalize_pairs(p,10)!=normalize_pairs(q+q[::-1],10)
    print('PASS corrupted near-9 mask rejected')


if __name__=='__main__': main()
