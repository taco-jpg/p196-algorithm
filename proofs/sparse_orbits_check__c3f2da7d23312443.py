#!/usr/bin/env python3
"""Finite controls for sparse_orbits_theorem.md, not an infinite-time proof.

Enumerate every admissible symmetric decimal pair-sum word of length <= 8;
also test long random words and deliberately sparse/dense controls. Each
transition is checked against ordinary integer reversal and addition after
an independently constructed canonical decimal realization of the word.
"""

from __future__ import annotations

import itertools
import json
import random
from collections import Counter
from pathlib import Path


def digits(n: int) -> list[int]:
    assert n > 0
    return [int(c) for c in str(n)[::-1]]


def pair_sums(n: int) -> list[int]:
    d = digits(n)
    return [a + b for a, b in zip(d, reversed(d))]


def realize(q: list[int]) -> int:
    """Realize q without assuming the units digit is nonzero."""
    assert q and q == q[::-1] and 1 <= q[0] <= 18
    assert all(0 <= x <= 18 for x in q)
    L = len(q)
    d = [0] * L
    for i in range(L // 2):
        # Put the positive share at the high endpoint, ensuring canonicality.
        d[L - 1 - i] = min(q[i], 9)
        d[i] = q[i] - d[L - 1 - i]
    if L % 2:
        assert q[L // 2] % 2 == 0
        d[L // 2] = q[L // 2] // 2
    n = sum(x * 10**i for i, x in enumerate(d))
    assert len(str(n)) == L and pair_sums(n) == q
    return n


def zero_runs(word: list[int]) -> list[tuple[int, int]]:
    runs = []
    start = None
    for i, x in enumerate(word + [1]):
        if x == 0 and start is None:
            start = i
        elif x != 0 and start is not None:
            runs.append((start, i - 1))
            start = None
    return runs


def max_zero_run(word: list[int]) -> int:
    return max((b - a + 1 for a, b in zero_runs(word)), default=0)


def check(q: list[int], counts: Counter[str]) -> None:
    n = realize(q)
    m = n + int(str(n)[::-1])
    qnext = pair_sums(m)
    L = len(q)
    a = [0]
    r = []
    for x in q:
        c, d = divmod(x + a[-1], 10)
        a.append(c)
        r.append(d)
    b = a[::-1]
    u = r[::-1]
    h = a[-1]
    assert h in (0, 1) and len(qnext) == L + h
    assert digits(m) == r + ([1] if h else [])
    assert all(q[i] + b[i + 1] == u[i] + 10 * b[i] for i in range(L))
    if not h:
        expected = [r[i] + u[i] for i in range(L)]
    else:
        expected = [r[0] + 1]
        expected += [r[i] + u[i - 1] for i in range(1, L)]
        expected += [1 + r[0]]
    assert expected == qnext
    assert qnext[0] > 0 and qnext[-1] > 0
    counts["transitions"] += 1
    counts[f"overflow_{h}"] += 1
    if n % 10 == 0:
        counts["canonical_inputs_with_trailing_zero"] += 1

    # Directly check the local lemma on every maximal simultaneous-zero run.
    simultaneous = [int(not (x == y == 0)) for x, y in zip(r, u)]
    for A, B in zero_runs(simultaneous):
        k = B - A + 1
        if k >= 2:
            assert q[A : B + 1] in ([0] * k, [9] * k)
            counts["simultaneous_zero_intervals_ge2"] += 1

    for A, B in zero_runs(qnext):
        k = B - A + 1
        assert 1 <= A <= B < len(qnext) - 1
        if h == 0 and k >= 2:
            if q[A : B + 1] == [0] * k:
                counts["no_overflow_long_zero_inherited"] += 1
            else:
                assert q[A : B + 1] == [9] * k
                assert 9 * k <= sum(q)
                counts["no_overflow_long_zero_from_nines"] += 1
        elif h == 1 and k >= 3:
            if q[A : B] == [0] * (k - 1):
                assert q[A - 1 : B + 1] == [0] * (k + 1)
                assert a[A] == a[B] == b[A] == b[B] == 0
                counts["overflow_long_zero_inherited"] += 1
            else:
                assert q[A : B] == [9] * (k - 1)
                assert 9 * (k - 1) <= sum(q)
                counts["overflow_long_zero_from_nines"] += 1

    Z, Znext, mass = max_zero_run(q), max_zero_run(qnext), sum(q)
    limit = max(Z, 1, mass // 9) if h == 0 else max(max(Z - 1, 0), 2, mass // 9 + 1)
    assert Znext <= limit
    support = sum(x != 0 for x in q)
    assert L <= support + (support - 1) * Z
    counts["gap_and_support_bounds"] += 1


def admissible_words(max_length: int):
    for L in range(1, max_length + 1):
        if L == 1:
            for center in range(2, 19, 2):
                yield [center]
            continue
        for first in range(1, 19):
            for interior in itertools.product(range(19), repeat=L // 2 - 1):
                left = [first, *interior]
                if L % 2:
                    for center in range(0, 19, 2):
                        yield left + [center] + left[::-1]
                else:
                    yield left + left[::-1]


def main() -> None:
    counts: Counter[str] = Counter()
    by_length: Counter[int] = Counter()
    for q in admissible_words(8):
        check(q, counts)
        by_length[len(q)] += 1

    rng = random.Random(20261014)
    random_count = 20_000
    for _ in range(random_count):
        L = rng.randrange(1, 241)
        if L == 1:
            q = [rng.randrange(1, 10) * 2]
        else:
            half = [rng.randrange(1, 19)]
            # Many zeros and nines exercise long inherited and created gaps.
            half += [rng.choice([0, 0, 0, 9, 9, rng.randrange(19)]) for _ in range(L // 2 - 1)]
            q = half + ([rng.randrange(10) * 2] if L % 2 else []) + half[::-1]
        check(q, counts)

    targeted_count = 0
    for gap in range(1, 81):
        # Even center-free lengths admit arbitrary runs of nine.
        for outer in range(1, 19):
            for middle in (0, 9):
                q = [outer] + [middle] * (2 * gap) + [outer]
                check(q, counts)
                targeted_count += 1
        # Simultaneous-zero q=10 can occur only as an isolated site.
        q = [11] + [0] * gap + [9, 10, 9, 9, 10, 9] + [0] * gap + [11]
        check(q, counts)
        targeted_count += 1

    result = {
        "status": "all finite controls passed; mathematical proof is separate",
        "exhaustive_admissible_words_by_length": dict(sorted(by_length.items())),
        "random_words": random_count,
        "targeted_words": targeted_count,
        "counts": dict(sorted(counts.items())),
        "proved_claim_in_companion_note": "Every positive decimal reverse-and-add orbit has unbounded digit sum; this script is not that proof.",
    }
    path = Path(__file__).with_name("sparse_orbits_check_results.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
