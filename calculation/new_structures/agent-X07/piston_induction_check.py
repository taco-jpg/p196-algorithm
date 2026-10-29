#!/usr/bin/env python3
"""Independent exhaustive small-state tests for the complement-nine piston theorem.

The primary proof is arithmetic; this script uses actual ordinary decimal integers
and no X07 C++ frontier implementation. Its tests do NOT establish induction.
"""
from itertools import product
from collections import Counter


def ordinary_step(d):
    value = int(''.join(map(str, reversed(d))))
    rev = int(str(value)[::-1])
    value2 = value + rev
    nxt = [int(x) for x in str(value2)[::-1]]
    # Separate schoolbook engine, not using the integer sum formula.
    out, carry = [], 0
    for i, x in enumerate(d):
        s = x + d[-1-i] + carry
        out.append(s % 10)
        carry = s // 10
    if carry:
        out.append(carry)
    assert nxt == out
    return nxt, carry


def check_one(A, L):
    m = len(A)
    H = [9 - x for x in A]
    d = A + [9]*L + H
    assert d[-1] > 0 and sum(A) % 9 == 8 and A[-1] <= 8 and L >= 1
    nd, gamma = ordinary_step(d)
    mnext, Lnext = m + gamma, L - gamma
    assert len(nd) == 2*mnext+Lnext
    left, middle, high = nd[:mnext], nd[mnext:mnext+Lnext], nd[mnext+Lnext:]
    assert middle == [9]*Lnext, (A, L, 'bulk')
    assert all(x + y == 9 for x, y in zip(left, high)), (A, L, 'complement')
    assert left[-1] <= 8, (A, L, 'inner guard')
    assert sum(left) % 9 == 8, (A, L, 'charge')
    assert nd != nd[::-1], (A, L, 'palindrome')
    return left, Lnext, gamma


def main():
    counts = Counter()
    total = 0
    for m in range(1, 5):
        for tup in product(range(10), repeat=m):
            A = list(tup)
            if A[-1] == 9 or sum(A) % 9 != 8:
                continue
            for L in (1,2,5):
                B, L1, gamma = check_one(A, L)
                counts[(m, L, gamma)] += 1
                total += 1
                if L1 >= 1:
                    check_one(B, L1)  # separate two-step induction control
    print(f'PAPER-PROOF CONTROL PASS initial_states={total} one_step_and_conditional_two_step; m=1..4, L=1/2/5')
    print('counts_by_m:', {m:sum(v for (q,L,g),v in counts.items() if q==m) for m in range(1,5)})
    print('overflow_counts:', {g:sum(v for (m,L,q),v in counts.items() if q==g) for g in (0,1)})

if __name__=='__main__':main()
