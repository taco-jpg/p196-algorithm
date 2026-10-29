#!/usr/bin/env python3
"""Independent arbitrary-precision integer replay of every X07 renewal witness.

No use of the C++ digit engine or its complement-front detector.
Reproduction: python3 independent_renewal.py renewal_events.json
"""
import collections
import json
import sys

sys.set_int_max_str_digits(100000)


def seed(width, A):
    low = [int(c) for c in f'{A:0{width}d}'[::-1]]
    digits = low + [9 - c for c in low]
    return int(''.join(map(str, digits[::-1])))


def protected_length(N):
    # Directly inspect the most-significant-first decimal representation.
    s = str(N)
    n = len(s)
    possible = range(n % 2, n - 1, 2)
    for L in possible:
        m = (n - L) // 2
        if m < 1 or any(x != '9' for x in s[m:m + L]):
            continue
        A = s[-m:][::-1]
        H = s[:m][::-1]
        if int(A[-1]) > 8 or sum(map(int, A)) % 9 != 8:
            continue
        if all(int(a) + int(h) == 9 for a, h in zip(A, H)):
            return L
    return -1


def replay(event, horizon=200):
    A, width = event['A'], event['m']
    target = [(r['t'], r['L']) for r in event['entries']]
    N = seed(width, A)
    mode = 0
    lost = None
    got = []
    for t in range(horizon + 1):
        s = str(N)
        assert s != s[::-1], (A, t, 'unexpected palindrome')
        L = protected_length(N)
        if mode == 0 and L < 0:
            mode = 1
            lost = t
        elif mode == 1 and L >= 1:
            mode = 2
            got.append((t, L))
        elif mode == 2 and L < 0:
            mode = 1
        if t != horizon:
            # Real integer arithmetic, not a paired-digit normalizer.
            N += int(s[::-1])
    assert lost == event['first_lost'], (A, lost, event['first_lost'])
    assert got == target, (A, got, target)
    return N


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'renewal_events.json'
    data = json.load(open(path))
    events = data['events']
    totals = collections.Counter((e['m'], r['L']) for e in events for r in e['entries'])
    assert len(events) == 136
    assert totals == {(4, 1): 26, (6, 1): 73, (6, 2): 37}, totals
    for e in events:
        replay(e)
    print('Independent Python big integers: 136/136 witnesses, t=0..200, zero palindromes, all returns confirmed')
    print('Restorations by (boundary width, central nine-run length):', sorted(totals.items()))
    for A,m in ((521,4),(3491,6)):
        e = next(e for e in events if e['A']==A and e['m']==m)
        N = replay(e, 200)
        # One long post-regeneration test of each selected control.
        N = seed(m,A)
        for t in range(4001):
            s = str(N)
            assert s != s[::-1], (A,t,'palindrome in long control')
            if t < 4000: N += int(s[::-1])
        print(f'A={A} m={m}: independent 4000-step integer replay PASS')


if __name__ == '__main__': main()
