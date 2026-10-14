#!/usr/bin/env python3
"""Finite independent-integer controls for the new uniform-escape proof."""
from __future__ import annotations

import itertools
import json
import random
from collections import Counter
from pathlib import Path


def trim(q):
    q = list(q)
    while q and q[-1] == 0:
        q.pop()
    return q


def digits(n, base):
    out = []
    while n:
        n, d = divmod(n, base)
        out.append(d)
    return out


def normalize(q, base):
    """Use two literal integers rather than the proof's carry recursions."""
    L = len(q)
    low = sum(x * base**i for i, x in enumerate(q))
    high = sum(x * base ** (L - 1 - i) for i, x in enumerate(q))
    r = digits(low, base)
    reverse_digits = digits(high, base) + [0] * (L + 1)
    u = [reverse_digits[L - 1 - i] for i in range(L)]
    return r, u, reverse_digits[L]


def at(q, i):
    return q[i] if 0 <= i < len(q) else 0


def phi(q, base):
    r, u, h = normalize(q, base)
    out = [at(r, i) + at(u, i - h) for i in range(len(q) + 2)]
    if h:
        out[0] += 1
    return trim(out), h


def bulk(v, h, base):
    r, u, own_h = normalize(v, base)
    assert own_h == 0  # a separated right component is zero at index zero
    return trim([at(r, i) + at(u, i - h) for i in range(len(v) + 2)])


def add(p, v):
    return trim([at(p, i) + at(v, i) for i in range(max(len(p), len(v)))])


def words(base, maxlen):
    for L in range(1, maxlen + 1):
        for q in itertools.product(range(2 * base - 1), repeat=L):
            if q[0] and q[-1]:
                yield list(q)


def check_pair(p, v, gap, base, counts):
    v = [0] * (len(p) + gap) + list(v)
    q = add(p, v)
    image, h = phi(q, base)
    left, left_h = phi(p, base)
    right = bulk(v, h, base)
    assert h == left_h
    assert image == add(left, right)
    assert right and sum(right) >= 1
    assert sum(image) == sum(left) + sum(right)
    assert len(left) <= len(p) + 1
    first_right = next(i for i, x in enumerate(right) if x)
    new_gap = first_right - len(left)
    assert new_gap >= gap - 2
    counts[f"coupling_base_{base}"] += 1
    counts[f"coupling_branch_{h}"] += 1


def main():
    counts = Counter()
    for base in (2, 3):
        profiles = list(words(base, 3))
        for p in profiles:
            for v in profiles:
                for gap in (2, 3, 4):
                    check_pair(p, v, gap, base, counts)

    rng = random.Random(20261015)
    for _ in range(20000):
        base = rng.choice((2, 3, 10))
        p = [rng.randrange(2 * base - 1) for _ in range(rng.randrange(1, 12))]
        v = [rng.randrange(2 * base - 1) for _ in range(rng.randrange(1, 12))]
        p[0] = rng.randrange(1, 2 * base - 1)
        p[-1] = rng.randrange(1, 2 * base - 1)
        v[0] = rng.randrange(1, 2 * base - 1)
        v[-1] = rng.randrange(1, 2 * base - 1)
        gap = rng.randrange(2, 18)
        check_pair(p, v, gap, base, counts)

    # Multi-step separation is the premise used by the mass induction.
    for _ in range(3000):
        base = rng.choice((2, 3, 10))
        T = rng.randrange(1, 21)
        p = [rng.randrange(2 * base - 1) for _ in range(rng.randrange(1, 8))]
        v = [rng.randrange(2 * base - 1) for _ in range(rng.randrange(1, 8))]
        p[0] = p[-1] = rng.randrange(1, 2 * base - 1)
        v[0] = v[-1] = rng.randrange(1, 2 * base - 1)
        initial_gap = 2 * T + 2
        v = [0] * (len(p) + initial_gap) + v
        q = add(p, v)
        for s in range(T + 1):
            assert q == add(p, v)
            assert sum(q) == sum(p) + sum(v)
            assert p[0] > 0 and sum(v) >= 1
            first_v = next(i for i, x in enumerate(v) if x)
            assert first_v - len(p) >= initial_gap - 2 * s
            if s < T:
                q, h = phi(q, base)
                p, hp = phi(p, base)
                assert h == hp
                v = bulk(v, h, base)
                counts["multi_step_coupling_steps"] += 1

    # Exact nonsymmetric support law, including asymmetric carry endpoints.
    for base in (2, 3, 10):
        trials = list(words(base, 3)) if base != 10 else [
            [rng.randrange(1, 19)] + [rng.randrange(19) for _ in range(rng.randrange(0, 30))] + [rng.randrange(1, 19)]
            for _ in range(5000)
        ]
        for q in trials:
            nxt, h = phi(q, base)
            r, u, _ = normalize(q, base)
            last_forward_carry = at(r, len(q))
            expected_length = len(q) + (1 if h else last_forward_carry)
            assert len(nxt) == expected_length
            assert nxt[0] > 0 and all(0 <= x <= 2 * base - 2 for x in nxt)
            counts["support_law"] += 1

    result = {"status": "all finite controls passed; not a replacement for the proof", "counts": dict(sorted(counts.items()))}
    Path(__file__).with_name("strength_uniform_check_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
