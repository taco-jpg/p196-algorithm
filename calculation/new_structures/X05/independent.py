#!/usr/bin/env python3
"""Independent bigint, digit-array, and U3 reset-cone controls for X05."""
import sys
sys.set_int_max_str_digits(0)

B = [10,4,6,6,7,12,9,16,16,13,0,2,10,17,7,0,18,6,5,18,4,18,14,9,14,8,12,17,10,4,6,4,0,5]
W = [5,18,4,8,1,15,4,0,5]
U = [9,6,12]

def carry(x, c):
    return int(x+c >= 10)

def bulk_step(word, overflow):
    m = len(word)
    z = 0
    for _ in range(2):
        for x in word:
            z = carry(x, z)
    low = [0]*m
    low[0] = z
    for i in range(1, m):
        low[i] = carry(word[i-1], low[i-1])

    z = 0
    for _ in range(2):
        for x in reversed(word):
            z = carry(x, z)
    high = [0]*m
    high[0] = z
    for i in range(m-1, 0, -1):
        high[i] = carry(word[i], high[(i+1) % m])

    return tuple(
        (word[i]+low[i]) % 10
        + ((word[i]+high[(i+1) % m]) % 10 if not overflow
           else (word[i-1]+high[i]) % 10)
        for i in range(m)
    )

def cone_bounds(phases):
    m = len(phases[0])
    left = right = 0
    for t in range(120):
        w = phases[t]
        left += 1 + int(w[left % m] == 9)
        right += 1 + int(w[(-right-1) % m] == 9) - int(t % 4 == 0)
    return left, right

def check_bulk_cones():
    phases = [tuple(U)]
    for t in range(120):
        phases.append(bulk_step(phases[-1], int(t % 4 == 0)))
    assert phases[-1] == tuple(U)
    assert all(row.count(9) == 1 for row in phases)
    cones = cone_bounds(phases)
    assert cones == (152, 121), cones
    assert 3*100 - sum(cones) == 27
    print(f"PASS independent U3 carry-cycle and reset cones: seam={cones[0]} centre={cones[1]} gap={3*100-sum(cones)}")

def template(q, k, J, L):
    C = [0]*L
    C[L//2] = 4
    h = B + W*q + J + U*k
    p = h + C + h[::-1]
    assert p == p[::-1] and p[0] > 0
    assert all(0 <= x <= 18 for x in p) and C == C[::-1]
    assert C[L//2] % 2 == 0
    return p

def integer_from_pairword(p):
    assert p == p[::-1] and p[0] > 0
    assert all(0 <= x <= 18 for x in p)
    d = [0]*len(p)
    for i in range(len(p)//2):
        d[i] = max(0, p[i]-9)
        d[-1-i] = min(9, p[i])
    if len(p) % 2:
        assert p[len(p)//2] % 2 == 0
        d[len(p)//2] = p[len(p)//2]//2
    assert d[-1] > 0
    return int("".join(map(str, d[::-1])))

def schoolbook_reverse_add(n):
    d = list(map(int, str(n)[::-1]))
    out = []
    carry = 0
    for i, x in enumerate(d):
        z = x + d[-1-i] + carry
        out.append(z % 10)
        carry = z//10
    if carry:
        out.append(carry)
    return int("".join(map(str, out[::-1])))

def pairword(n):
    s = str(n)
    return [int(s[-1-i]) + int(s[i]) for i in range(len(s))]

def main():
    check_bulk_cones()
    # The full J domain is exhausted by search.cpp. These controls are
    # independent real-decimal checks across all five claimed centre lengths.
    js = [[0,0,0], [0,0,0,0], [18,18,18,18], [0,18,3,12]]
    checks = 0
    for J in js:
        for L in (15,17,19,21,23):
            for q, k in ((14,100), (20,100), (40,200), (80,400), (160,800)):
                p = template(q, k, J, L)
                n = integer_from_pairword(p)
                assert str(n) != str(n)[::-1], (J,L,q,k,"palindromic source")
                wanted = template(q, k+5, J, L)
                overflows = []
                palindrome = []
                for t in range(120):
                    a = n + int(str(n)[::-1])
                    b = schoolbook_reverse_add(n)
                    assert a == b, (J,L,q,k,t)
                    overflows.append(len(str(a))-len(str(n)))
                    palindrome.append(str(a) == str(a)[::-1])
                    n = a
                assert overflows == [1,0,0,0]*30, (J,L,q,k,overflows)
                got = pairword(n)
                mismatch = next((i for i,(x,y) in enumerate(zip(got,wanted)) if x != y), None)
                if mismatch is None and len(got) != len(wanted):
                    mismatch = min(len(got), len(wanted))
                assert mismatch is not None, (J,L,q,k,"unexpected full return")
                cut = 34 + 9*q
                assert -25 <= mismatch-cut <= -14, (J,L,q,k,mismatch,cut,mismatch-cut)
                assert not any(palindrome), (J,L,q,k,"palindrome in control trajectory")
                checks += 1
                print(f"PASS J={J} C_len={L} q={q} k={k} clock=1000^30 first_mismatch={mismatch} offset={mismatch-cut} palindrome_steps=0")
    print(f"PASS independent Python big-integer and fresh-buffer digit-array agreement: {checks} cases x 120 steps")

if __name__ == "__main__":
    main()
