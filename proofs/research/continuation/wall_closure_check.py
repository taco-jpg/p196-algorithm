"""Finite controls for wall_closure_notes.md; no infinity extrapolation."""
from __future__ import annotations

import importlib.util
from itertools import product
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'astra_moving_boundary_check.py'
if not SOURCE.exists():
    SOURCE = HERE.parent / 'research' / 'astra_moving_boundary_check.py'
spec = importlib.util.spec_from_file_location('wall_reference', SOURCE)
wall = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(wall)


def T(n):
    return n + int(str(n)[::-1])


def S(n):
    return sum(map(int, str(n)))


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total-first, length-1):
            yield (first,) + tail


def check_sum9(n):
    assert S(n) == 9
    L = len(str(n))
    d = tuple(map(int, str(n)[::-1]))
    center = d[L//2] if L % 2 else None
    current = n
    first_palindrome = None
    consecutive = 0
    for step in range(1, 4):
        current = T(current)
        if S(current) == 9 and consecutive == step-1:
            consecutive += 1
        if str(current) == str(current)[::-1]:
            first_palindrome = step
            break
    assert first_palindrome is not None
    assert consecutive <= 2
    expected = (2 if L == 1 else
                1 if center is None or center <= 4 else
                3 if center == 8 else 2)
    assert first_palindrome == expected, (n, first_palindrome, expected)
    return first_palindrome


def quotient_control(W, C):
    V, h, r = wall.wall_step(W)
    w = len(W)
    A = 2*10**w-sum(x*10**i for i, x in enumerate(W))
    assert A >= 2
    e = tuple(map(int, str(A-1)[::-1]))
    padded = e + (0,)*max(0, len(r)-len(e))
    assert tuple(9-x for x in padded) == r
    monotone = all(e[i] <= e[i-C] for i in range(C, len(e)))
    assert monotone == wall.digit_monotone(r, C)
    q = wall.difference_word(W, C)
    assert sum(x*10**i for i, x in enumerate(q)) == (10**C-1)*A
    if monotone:
        reconstructed = 0
        units = 0
        for j in range(C):
            for m in range(1, (len(e)+C-1)//C+1):
                lo = e[j+(m-1)*C] if j+(m-1)*C < len(e) else 0
                hi = e[j+m*C] if j+m*C < len(e) else 0
                lam = lo-hi
                assert lam >= 0
                units += lam
                reconstructed += 10**j*lam*(10**(C*m)-1)//(10**C-1)
        assert units <= 9*C
        assert reconstructed == A-1


def run():
    rng = random.Random(20261014)
    counts = {'sum9_exhaustive': 0, 'sum9_random': 0,
              'quotient_controls': 0, 'long_C1_walls': 0}
    first_palindrome_counts = {1: 0, 2: 0, 3: 0}
    for width in range(1, 9):
        for d in compositions(9, width):
            if d[-1] == 0:
                continue
            n = sum(x*10**i for i, x in enumerate(d))
            first_palindrome_counts[check_sum9(n)] += 1
            counts['sum9_exhaustive'] += 1
    for _ in range(2000):
        width = rng.randrange(9, 251)
        d = [0]*width
        d[-1] = 1
        for _ in range(8):
            d[rng.randrange(width)] += 1
        n = sum(x*10**i for i, x in enumerate(d))
        check_sum9(n)
        counts['sum9_random'] += 1
    for W in wall.wall_words(2):
        for C in range(1, len(W)+4):
            quotient_control(W, C)
            counts['quotient_controls'] += 1
    for _ in range(2000):
        half_width = rng.randrange(1, 51)
        U = (rng.randrange(1, 19),) + tuple(rng.randrange(19) for _ in range(half_width-1))
        W = U + ((9,) if rng.randrange(2) else ()) + tuple(18-x for x in U[::-1])
        C = rng.randrange(1, len(W)+4)
        quotient_control(W, C)
        counts['quotient_controls'] += 1
    # Arbitrarily widen monotone anti-complement walls, including long
    # constant plateaus. Their validity is checked before following them.
    for k in (1, 2, 5, 20, 100):
        for x in range(1, 10):
            for center_width in (0, 1, 2, 10, 100):
                W = (x,)*k + (9,)*center_width + (18-x,)*k
                assert wall.word_valid(wall.difference_word(W, 1))
                successes = 0
                for _ in range(3):
                    V, h, r = wall.wall_step(W)
                    if not wall.digit_monotone(r, 1):
                        break
                    successes += 1
                    W = V
                assert successes <= 2
                counts['long_C1_walls'] += 1
    sharp = [180]
    for _ in range(3):
        sharp.append(T(sharp[-1]))
    result = dict(status='proved C=1 obstruction; no general fixed-C conclusion',
                  counts=counts, first_palindrome_counts=first_palindrome_counts,
                  sharp_example=sharp)
    HERE.joinpath('wall_closure_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    run()
