#!/usr/bin/env python3
"""W24 independent radix-b complementary-pair carry kink checks."""
import itertools
import json
import random

def digits(value, base, minimum=0):
    out = []
    while value:
        out.append(value % base)
        value //= base
    while len(out) < minimum:
        out.append(0)
    return out

def val(P, base):
    return sum(x * base ** i for i, x in enumerate(P))

def physical_seed(P, base):
    n = len(P)
    assert n % 2 == 0
    out = [0] * n
    for i in range(n // 2):
        out[n - i - 1] = min(base - 1, P[i])
        out[i] = P[i] - out[n - i - 1]
    assert out[-1] > 0 and all(0 <= x < base for x in out)
    return val(out, base)

def reverse_int(n, base):
    d = digits(n, base)
    return val(d[::-1], base)

def check(base, P):
    n = len(P)
    Q = [2 * (base - 1) - x for x in P]
    assert P == P[::-1] and Q == Q[::-1]
    k = next((i for i, x in enumerate(P) if x != base - 1), None)
    assert k is not None
    A, B = physical_seed(P, base), physical_seed(Q, base)
    S, T = A + reverse_int(A, base), B + reverse_int(B, base)
    assert S == val(P, base) and T == val(Q, base)
    assert S + T == 2 * (base ** n - 1)
    sd, td = digits(S, base, n + 1), digits(T, base, n + 1)
    expected = ([2 * (base - 1)] * k + [base - 2] +
                [base - 1] * (n - 1 - k) + [1])
    assert [x + y for x, y in zip(sd, td)] == expected
    assert sum(v > 0 for v in (sd[-1], td[-1])) == 1
    return k

def main():
    total = 0
    for base in range(3, 22):
        for a in range(1, 2 * base - 2):
            for b in range(2 * base - 1):
                for c in range(2 * base - 1):
                    half = [a, b, c]
                    if all(x == base - 1 for x in half):
                        continue
                    check(base, half + half[::-1])
                    total += 1
    rng = random.Random(2400474)
    for _ in range(10000):
        base = rng.randint(3, 97)
        half = ([rng.randrange(1, 2 * base - 2)] +
                [rng.randrange(2 * base - 1) for _ in range(rng.randrange(3, 80))])
        if all(x == base - 1 for x in half):
            half[1] = 0
        check(base, half + half[::-1])
        total += 1
    print(json.dumps({"checks": total, "exhaustive_base_range": [3, 21],
        "exhaustive_palindromic_pair_length": 6, "random_checks": 10000,
        "random_base_range": [3, 97], "status": "PASS"}, sort_keys=True))

if __name__ == "__main__":
    main()
