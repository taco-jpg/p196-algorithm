"""Exact affine carry encoders; these are identities, not a Lychrel proof.

Digits are least significant first. This file checks the identities against
independent ordinary integer arithmetic, including leading overflow digits.
"""
from itertools import product
import json


def digits(n, base):
    out = []
    while n:
        out.append(n % base)
        n //= base
    return out or [0]


def value(ds, base):
    return sum(d * base ** i for i, d in enumerate(ds))


def add_reverse(ds, base):
    carry = [0]
    out = []
    for a, b in zip(ds, reversed(ds)):
        s = a + b + carry[-1]
        out.append(s % base)
        carry.append(s // base)
    if carry[-1]:
        out.append(carry[-1])
    assert value(out, base) == value(ds, base) + value(ds[::-1], base)
    return out, carry


def check_encoder(ds, b, B, a, u):
    assert a >= 1 and u >= 0 and a * (b - 1) + 2 * u == B - 1
    encoded = [a*d + u for d in ds]
    src, c = add_reverse(ds, b)
    dst, cb = add_reverse(encoded, B)
    assert c == cb
    L = len(ds)
    predicted = [a*src[i] + 2*u + (1-a)*c[i] + (a*b-B)*c[i+1]
                 for i in range(L)]
    if c[-1]:
        predicted.append(1)
    assert predicted == dst
    if u == 0:
        cp = c + [0] if c[-1] else c
        delta = [(a-1)*(cp[i+1]-cp[i]) for i in range(len(src))]
        assert dst == [a*x+e for x,e in zip(src,delta)]
        assert all(delta[i]+delta[-1-i] == 0 for i in range(len(delta))) == (
            cp[1:-1] == cp[1:-1][::-1])
    if a == 1:
        expected = [src[i] + 2*u*(1-c[i+1]) for i in range(L)]
        if c[-1]:
            expected.append(1)
        assert dst == expected


def binary_family(m):
    return list(map(int, ('10'+'1'*m+'01'+'0'*m)[::-1]))


def base4_family(m):
    return list(map(int, ('10'+'3'*m+'323'+'0'*m+'00')[::-1]))


def check_families():
    for m in range(3, 35):
        ds = binary_family(m)
        src, c = add_reverse(ds,2)
        delta = [8*(c[i+1]-c[i]) for i in range(len(ds))]
        expected = [0]*len(ds)
        expected[m] = 8
        expected[2*m+2] = -8
        assert delta == expected
        sym = [delta[i]+delta[-1-i] for i in range(len(ds))]
        expect_sym = [0]*len(ds)
        for i,v in [(m,8),(m+3,8),(1,-8),(2*m+2,-8)]:
            expect_sym[i] += v
        assert sym == expect_sym
    for m in range(25):
        ds = base4_family(m)
        start = ds
        for _ in range(6):
            assert ds != ds[::-1]
            ds,_ = add_reverse(ds,4)
        assert ds == base4_family(m+1)
        for a,u in ((1,3),(3,0)):
            check_encoder(start,4,10,a,u)


def main():
    counts={}
    for b in (2,4):
        for a in range(1,10):
            twice_u = 9-a*(b-1)
            if twice_u < 0 or twice_u % 2:
                continue
            u=twice_u//2
            count=0
            for L in range(1,7):
                for ds in product(range(b),repeat=L):
                    if ds[-1] == 0:
                        continue
                    check_encoder(list(ds),b,10,a,u)
                    count+=1
            counts[f'base{b}_a{a}_u{u}']=count
    # Orientation reversing local encoder E(d)=u-d with complemented carry.
    for b in (2,4):
        B=10;u=(B+b-2)//2
        for s in range(2*b-1):
            for ci in (0,1):
                src,co=(s+ci)%b,(s+ci)//b
                actual=2*u-s+(1-ci)
                assert actual//B == 1-co
                assert actual%B == b-1-src+(B-b)*co
    check_families()
    print(json.dumps({'status':'passed','encoder_checks':counts,
                      'binary_family_checked_m':[3,34],
                      'base4_family_checked_m':[0,24],
                      'claim':'Exact carry identities only; no decimal Lychrel certificate.'},indent=2))


if __name__=='__main__':
    main()
