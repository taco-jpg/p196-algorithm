#!/usr/bin/env python3
"""Independent arbitrary-precision and digit-list controls for the W10 cell."""
import sys
sys.set_int_max_str_digits(0)
B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W = [5,18,4,8,1,15,4,0,5]
U = [4,9,14]

def template(q, k, J, C):
    h = B + W*q + list(J) + U*k
    return h + list(C) + h[::-1]

def realize(p):
    assert p == p[::-1] and len(p) % 2 == 0
    d = [0] * len(p)
    for i in range(len(p)//2):
        d[i] = max(0, p[i]-9)
        d[-1-i] = min(9, p[i])
    assert d[-1] > 0
    return d

def value_lsd(d):
    return int(''.join(map(str, d[::-1])))

def step_list(d):
    out, carry, n = [], 0, len(d)
    for i in range(n):
        z = d[i] + d[n-1-i] + carry
        out.append(z % 10)
        carry = z // 10
    if carry:
        out.append(carry)
    return out

def first_w_mismatch(d, q):
    prefix = B + W*q
    for i, want in enumerate(prefix):
        got = d[i] + d[len(d)-1-i]
        if got != want:
            if i < len(B):
                return ("B", i, got, want)
            return ("W", i-len(B), got, want)
    return None

def run_bigint(q, k, J, C):
    n = value_lsd(realize(template(q,k,J,C)))
    gamma = []
    for _ in range(120):
        s = str(n)
        nxt = n + int(s[::-1])
        gamma.append(len(str(nxt))-len(s))
        n = nxt
    d = list(map(int, str(n)[::-1]))
    return ''.join(map(str,gamma)), first_w_mismatch(d,q)

def run_digits(q, k, J, C):
    d = realize(template(q,k,J,C))
    gamma = []
    for _ in range(120):
        old = len(d)
        d = step_list(d)
        gamma.append(len(d)-old)
    return ''.join(map(str,gamma)), first_w_mismatch(d,q)

def main():
    cases = 0
    for q in (20,40,80,160):
        k = 5*q
        for J in ([0,0,0], [5,9,9], [0,0,0,0], [5,9,9,9]):
            for C in ([0,0], [8,8,8,8], [18]*12):
                a = run_bigint(q,k,J,C)
                b = run_digits(q,k,J,C)
                assert a == b, (q,k,J,len(C),a,b)
                assert a[0] == '1000'*30, (q,k,J,len(C),a[0])
                assert a[1] is not None and a[1][0] == 'W', (q,k,J,len(C),a[1])
                x = len(B) + 9*q
                expected_delta = {(0,0,0):23, (5,9,9):20,
                                  (0,0,0,0):22, (5,9,9,9):20}[tuple(J)]
                assert a[1][1] == x - len(B) - expected_delta, (q,k,J,a[1],x)
                cases += 1
    print(f"BIGINT_DIGITLIST_PASS cases={cases} widths=q20,40,80,160 k=5q centres=2,4,12")
    print("all 48 controls have gamma=1000^30 and a W9 mismatch; sample engines agree exactly")

if __name__ == "__main__":
    main()
