#!/usr/bin/env python3
"""Pair words of orbit(seed, t). Usage: orbit.py SEED T [K]  -> prints comma list of first K column sums."""
import sys
sys.set_int_max_str_digits(0)
def T(n): return n + int(str(n)[::-1])
def pair_word(n):
    d = [int(c) for c in str(n)][::-1]
    L = len(d)
    return [d[i] + d[L - 1 - i] for i in range(L)]
if __name__ == '__main__':
    seed, t = int(sys.argv[1]), int(sys.argv[2])
    k = int(sys.argv[3]) if len(sys.argv) > 3 else 32
    n = seed
    for _ in range(t): n = T(n)
    print(','.join(map(str, pair_word(n)[:k])))
