#!/usr/bin/env python3
"""Randomized exact-integer soundness tests for interval/taint exterior."""
import random

def step(lo, hi):
    k = len(lo)
    pair = [{a+b for a in lo[i] for b in hi[i]} for i in range(k)]
    carry = {0}
    low_new = []
    for p in pair:
        sums = {x+c for x in p for c in carry}
        low_new.append({x % 10 for x in sums})
        carry = {x//10 for x in sums}
    carry = {0, 1}
    upper = [set() for _ in range(k)]
    for i in range(k-1, -1, -1):
        sums = {x+c for x in pair[i] for c in carry}
        upper[i] = {x % 10 for x in sums}
        carry = {x//10 for x in sums}
    high_new = [set() for _ in range(k)]
    if 0 in carry:
        for i in range(k): high_new[i] |= upper[i]
    if 1 in carry:
        high_new[0].add(1)
        for i in range(1, k): high_new[i] |= upper[i-1]
    return low_new, high_new

def run():
    rng = random.Random(30112026)
    tested = 0
    for z in range(4500):
        k = rng.randrange(1, 33)
        low = [rng.randrange(10) for _ in range(k)]
        high = [rng.randrange(10) for _ in range(k)]
        high[0] = rng.randrange(1, 10)
        a = [set([x]) for x in low]
        b = [set([x]) for x in high]
        seeds = []
        for _ in range(2):
            core = ''.join(str(rng.randrange(10)) for _ in range(rng.randrange(1, 51)))
            s = ''.join(map(str, high)) + core + ''.join(map(str, low[::-1]))
            seeds.append(int(s))
        for t in range(22):
            guarded = any(a[j].isdisjoint(b[j]) for j in range(k))
            for idx, number in enumerate(seeds):
                word = str(number)
                assert len(word) >= 2*k+1
                for j in range(k):
                    assert int(word[-1-j]) in a[j]
                    assert int(word[j]) in b[j]
                if guarded:
                    assert word != word[::-1], (z,t,idx)
                tested += 1
                seeds[idx] = number + int(word[::-1])
            a,b = step(a,b)
    print(f'PASS {tested} symbolic memberships and guarded palindrome claims, 4500 seeds x 2 centres')

if __name__ == '__main__':
    run()
