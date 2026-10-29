#!/usr/bin/env python3
"""Independent real-decimal controls for the Z45 growing-seam length ledger.

This is a scoped length-law check, not a search for a certificate.
"""
import sys
sys.set_int_max_str_digits(0)

B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W = [5,18,4,8,1,15,4,0,5]
U = [9,6,12]
J = [5]
C = [10]
W1, W2 = [1], [2,3]  # variant 4: |w1|=1, |w2|=2

def pairword_to_int(p):
    assert p == p[::-1]
    assert all(0 <= x <= 18 for x in p)
    assert p[0] > 0
    d = [0] * len(p)
    for i in range(len(p)//2):
        d[i] = max(0, p[i] - 9)
        d[-1-i] = min(9, p[i])
    if len(p) % 2:
        assert p[len(p)//2] % 2 == 0
        d[len(p)//2] = p[len(p)//2] // 2
    assert d[-1] > 0
    return int(''.join(map(str, d[::-1])))

def template(q, k, j=J):
    h = B + W*q + j + U*k
    p = h + C + h[::-1]
    assert p == p[::-1]
    return pairword_to_int(p)

def schoolbook_reverse_add(n):
    ds = list(map(int, str(n)[::-1]))  # LSB-first digits of n
    out, carry = [], 0
    for i, x in enumerate(ds):
        z = x + ds[-1-i] + carry
        out.append(z % 10)
        carry = z // 10
    if carry:
        out.append(carry)
    return int(''.join(map(str, out[::-1])))

def main():
    assert len(B) == 34 and sum(B) == 307
    assert len(W) == 9 and sum(W) == 60
    assert len(U) == 3 and sum(U) == 27
    assert len(W1) + len(W2) == 3
    print('q,k,source_digits,clock_ones,actual_gain,target_fixed_J_gain,target_growing_J_gain,excess')
    for q, k in ((20,100),(40,200),(80,400),(160,800)):
        n0 = template(q,k)
        n = n0
        clock = 0
        clock_bits = []
        for t in range(120):
            a = n + int(str(n)[::-1])
            b = schoolbook_reverse_add(n)
            assert a == b, (q,k,t)
            bit = int(len(str(a)) > len(str(n)))
            clock += bit
            clock_bits.append(bit)
            n = a
        actual_gain = len(str(n)) - len(str(n0))
        fixed_gain = len(str(template(q,k+5))) - len(str(n0))
        growing_gain = len(str(template(q,k+5, W1+J+W2))) - len(str(n0))
        assert clock == 30 and actual_gain == 30
        assert clock_bits == [int(t % 4 == 0) for t in range(120)], (q,k,clock_bits[:16])
        assert fixed_gain == 30
        assert growing_gain == 36
        assert growing_gain - actual_gain == 6
        print(f'{q},{k},{len(str(n0))},{clock},{actual_gain},{fixed_gain},{growing_gain},{growing_gain-actual_gain}')
    print('PASS: four canonical real-decimal starts; bigint and independent digit-array RAA agree for all 480 steps.')
    print('Scope: length-law controls only; no candidate seam return or all-time claim.')

if __name__ == '__main__':
    main()
