#!/usr/bin/env python3
"""Independent ordinary-decimal controls for Y13 first-exit rigidity.

PAPER PROOF (not dependent on this code):
Let 1<=h<k, H=10^h, g=gcd(h,k), M_j=10^j-1.
gcd(M_h,M_k)=M_g. If M_k divides M_h*q, then
D=M_k/M_g = 1+10^g+...+10^(k-g) divides q.
Since g divides k-h, g<=k-h, hence D>10^(k-g)>=H.
Therefore 0<q<H cannot carry any larger M_k factor.
If H<=q<2H, the only possible positive multiple of D is q=D.
Then M_h*q=M_k, which is the all-nines palindrome.

X07's exact scalar step on q=2 mod 9 and 0<q<H has
F(q)=q+1+reverse_m(10^m-q), 0<F(q)<2H.
Thus immediate higher-exponent reentry after the first failed guard
necessarily reaches a palindrome, and an infinite safe h-ladder
must use at least one genuinely unguarded intermediate integer.
"""
from math import gcd


def next_integer(n):
    """Whole-integer decimal reversal, independent of scalar arithmetic."""
    return n + int(str(n)[::-1])


def next_scalar(q):
    m = len(str(q))
    a = str(10**m - q).zfill(m)
    return q + 1 + int(a[::-1])


def test():
    total = exits = larger = 0
    for h in range(1, 5):
        H = 10**h
        M = H - 1
        for q in range(2, H, 9):
            total += 1
            n = M*q
            assert str(n) != str(n)[::-1]
            actual = next_integer(n)
            f = next_scalar(q)
            assert actual == M*f, (h,q,actual,M*f)
            assert 0 < f < 2*H
            exits += (f >= H)
            for k in range(h+1,2*h+4):
                K = 10**k - 1
                g = gcd(h,k)
                D = K//(10**g-1)
                assert D > H
                assert n%K != 0
                if actual%K == 0:
                    larger += 1
                    assert f >= H and actual == K
                    assert str(actual) == '9'*k
    assert total == 1234
    assert (exits, larger) == (622,22)
    print('PASS: 1234 guarded ordinary-integer steps; 622 first-edge exits;')
    print('22 larger-factor hits, all all-nines palindromes; h=1..4.')
    for h,q in [(1,2),(2,56),(3,758),(4,1442)]:
        n=(10**h-1)*q
        result=next_integer(n)
        assert result == 10**(2*h)-1
        print(f'h={h}, q={q}: {n} -> {result} (palindrome)')


if __name__ == '__main__':
    test()
