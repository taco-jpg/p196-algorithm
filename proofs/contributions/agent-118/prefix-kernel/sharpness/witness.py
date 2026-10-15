#!/usr/bin/env python3
"""Extract an explicit integer A with T^H(A) = P for a deepest backward chain (diagnostic)."""
import sys
sys.dont_write_bytecode = True
import exact_depth as ed

def realize(v):
    """An integer whose pair-sum word is v (units first): split each mirror sum."""
    n = len(v); a = [0] * n
    for i in range((n + 1) // 2):
        j = n - 1 - i
        if i == j:
            a[i] = v[i] // 2
        else:
            hi = min(9, v[i]); lo = v[i] - hi   # put the larger digit at the high end
            a[j], a[i] = hi, lo
    assert a[-1] > 0 and all(0 <= x <= 9 for x in a)
    return int(''.join(map(str, reversed(a))))

def T(n): return n + int(str(n)[::-1])

def chain(Pstr):
    w = tuple(map(int, Pstr))                 # palindrome: digit word read either way
    path = [w]
    while True:
        ps = ed.preimages(path[-1])
        if not ps: break
        path.append(max(ps, key=ed.depth))
    A = realize(path[-1])
    t = len(path)                              # number of additions from A to P
    x = A
    for _ in range(t): x = T(x)
    return A, t, x

if __name__ == '__main__':
    P = sys.argv[1]
    A, t, x = chain(P)
    print({'P': P, 'A': A, 't': t, 'orbit_A_t_equals_P': x == int(P), 'palindrome': str(x) == str(x)[::-1]})
