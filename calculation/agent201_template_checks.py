#!/usr/bin/env python3
"""Targeted checks for reports/REPORT_201.md; no seed search or existence claim."""

from itertools import product


def norm(word, carry=0):
    out = []
    for symbol in word:
        total = symbol + carry
        out.append(total % 10)
        carry = total // 10
    return out, carry


def normalize(word):
    out, carry = norm(word)
    return out + ([carry] if carry else [])


def pair(word):
    return [a + b for a, b in zip(word, reversed(word))]


def folded_step(word):
    return pair(normalize(word))


def template(c, B, A, C, G, H):
    assert G >= 0 and H >= 0
    left = B + [c] * G + A + [18 - c] * H
    return left + C + left[::-1]


def raw(c, B, A, C):
    kc, kd = int(c >= 10), int(18 - c >= 10)
    t, v = c - 9 * kc, 18 - c - 9 * kd
    DB, e0 = norm(B, 0)
    DA, e1 = norm(A, kc)
    DC, e2 = norm(C, kd)
    DRA, e3 = norm(A[::-1], kd)
    DRB, gamma = norm(B[::-1], kc)
    u0 = c + e0 - 10 * kc
    u1 = 18 - c + e1 - 10 * kd
    u2 = 18 - c + e2 - 10 * kd
    u3 = c + e3 - 10 * kc
    add = lambda a, b: [x + y for x, y in zip(a, b)]
    if gamma == 0:
        Br = add(DB + [u0], DRB[::-1] + [t])
        Ar = add([t] + DA + [u1], [u3] + DRA[::-1] + [v])
        Cr = pair([v] + DC + [u2])
        blocks = (DB + [u0], [t] + DA + [u1],
                  [v] + DC + [u2], [v] + DRA + [u3], [t] + DRB)
    else:
        assert gamma == 1
        Br = add(DB + [u0], [1] + DRB[::-1])
        Ar = add(DA + [u1], [u3] + DRA[::-1])
        Cr = pair(DC + [u2])
        blocks = (DB + [u0], DA + [u1], DC + [u2],
                  DRA + [u3], DRB + [1])
    X1, X2, X3, X4, X5 = blocks
    step_pal = X1 == X5[::-1] and X2 == X4[::-1] and X3 == X3[::-1]
    return 2 * t, Br, Ar, Cr, gamma, step_pal


def run_lengths(word):
    out = []
    for x in word:
        if out and out[-1][0] == x:
            out[-1] = (x, out[-1][1] + 1)
        else:
            out.append((x, 1))
    return out


def cap(word, threshold):
    return tuple((x, min(n, threshold)) for x, n in run_lengths(word))


def realize(q):
    assert q == q[::-1] and q[0] > 0
    d = [0] * len(q)
    for i in range(len(q) // 2):
        d[i] = q[i] - min(9, q[i])
        d[-1 - i] = min(9, q[i])
    if len(q) % 2:
        assert q[len(q) // 2] % 2 == 0
        d[len(q) // 2] = q[len(q) // 2] // 2
    assert pair(d) == q and d[-1] > 0
    return sum(x * 10**i for i, x in enumerate(d))


def digits(n):
    return [int(x) for x in str(n)[::-1]]


def main():
    count = 0
    for s, incoming, length in product(range(19), range(2), (1, 2, 7)):
        out, terminal = norm([s] * length, incoming)
        if s <= 8:
            expected, last = [s + incoming] + [s] * (length - 1), 0
        elif s == 9:
            expected, last = [9 * (1 - incoming)] * length, incoming
        else:
            expected = [s + incoming - 10] + [s - 9] * (length - 1)
            last = 1
        assert (out, terminal) == (expected, last)
        count += 1
    print(f"carry cases: {count} passed")

    scenarios = (
        ([], [], []),
        ([1], [9], [0]),
        ([10], [9, 10], [18]),
        ([9, 0, 18], [8, 9, 10], [2, 8, 2]),
        ([0], [18], [0, 0]),
        ([18, 9], [0, 9, 18], [10, 4, 10]),
    )
    count = 0
    overflow_counts = {0: 0, 1: 0}
    for c, blocks, G, H in product(
            [x for x in range(1, 18) if x != 9], scenarios, (2, 3, 7), (2, 3, 7)):
        B, A, C = blocks
        nxt, Br, Ar, Cr, gamma, step_pal = raw(c, B, A, C)
        q = template(c, B, A, C, G, H)
        assert folded_step(q) == template(nxt, Br, Ar, Cr, G - 2 + gamma, H - 2 + gamma)
        assert len(Br) == len(B) + 1
        assert len(Ar) == len(A) + 2 - gamma
        assert len(Cr) == len(C) + 2 - gamma
        e = normalize(q)
        assert step_pal == (e == e[::-1])
        count += 1
        overflow_counts[gamma] += 1
    print(f"raw identity, block lengths, palindrome test: {count} passed; "
          f"overflow counts={overflow_counts}")

    for c in [x for x in range(1, 18) if x != 9]:
        nxt, Br, Ar, Cr, gamma, step_pal = raw(c, [], [], [])
        if c <= 8:
            assert gamma == 0 and nxt == 2 * c
            assert Ar == [2 * c + 1, 17 - 2 * c]
            assert all(x % 2 == 1 for x in Ar)
            assert nxt % 2 == 0 and (18 - nxt) % 2 == 0
        else:
            a = c - 9
            assert gamma == 1 and nxt == 2 * a and Br == [a]
            assert Br != [nxt]
    print("empty-block obstruction: all 16 phases passed")

    for K in (2, 3, 7, 20):
        a, b = [10] * K, [10] * (K + 1)
        assert cap(a, K) == cap(b, K)
        assert folded_step(a) == [1] + [2] * (K - 1) + [1]
        assert folded_step(b) == [1] + [2] * K + [1]
        assert cap(folded_step(a), K) != cap(folded_step(b), K)
    print("run-cap obstruction: K=2,3,7,20 passed")
    print("K=3 outputs:", cap(folded_step([10] * 3), 3),
          cap(folded_step([10] * 4), 3))

    # A topological cycle alone cannot certify indefinitely viable counters.
    decrement = 5
    admissible_steps = 0
    while decrement - 1 >= 2:
        decrement -= 1
        admissible_steps += 1
    assert admissible_steps == 3
    print("negative-drift self-loop: starting at 5 with floor 2 allows 3 steps")

    # Neither one-edge cycle is viable forever, but their concatenation grows.
    abstract = [3, 3]
    minimum = abstract[:]
    for _ in range(1000):
        for delta in ((2, -1), (-1, 2)):
            abstract = [a + d for a, d in zip(abstract, delta)]
            minimum = [min(a, b) for a, b in zip(minimum, abstract)]
            assert min(abstract) >= 2
    assert abstract == [1003, 1003]
    print(f"abstract growing closed walk: 1000 laps, 2000 edges; "
          f"final={abstract}; coordinate minima={minimum}")

    # No decimal Lychrel construction is claimed. This is one prescribed
    # canonical realization, used to compare two exact implementations.
    q = [10] * 4
    n = realize(q)
    initial = n
    first_palindrome = None
    for t in range(1001):
        ds = digits(n)
        if t > 0 and ds == ds[::-1] and first_palindrome is None:
            first_palindrome = t
        if t == 1000:
            break
        expected = n + int(str(n)[::-1])
        assert normalize(pair(ds)) == digits(expected)
        assert folded_step(pair(ds)) == pair(digits(expected))
        n = expected
    print(f"decimal implementation check: seed={initial}; 1000 steps passed; "
          f"first positive-time palindrome={first_palindrome}; final digits={len(str(n))}")


if __name__ == "__main__":
    main()
