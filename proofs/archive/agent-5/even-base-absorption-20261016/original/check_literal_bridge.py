#!/usr/bin/env python3
"""Finite ordinary-integer cross-checks. Not a general Lean arithmetic bridge."""
from __future__ import annotations
from itertools import product
from pathlib import Path
import json
from check_model import State, step, overflow, moment

def digits(n: int, base: int) -> list[int]:
    out = []
    while n:
        n, d = divmod(n, base)
        out.append(d)
    return out or [0]

def value(ds: list[int], base: int) -> int:
    out = 0
    for d in reversed(ds):
        out = out * base + d
    return out

def reverse(n: int, base: int) -> int:
    return value(digits(n, base)[::-1], base)

def pair_word(n: int, base: int) -> tuple[int, ...]:
    ds = digits(n, base)
    return tuple(a + b for a, b in zip(ds, ds[::-1]))

def realize(s: State, gap: int, base: int) -> int:
    Q = s.B + (s.c,) * gap + s.B[::-1]
    if len(Q) % 2:
        raise ValueError('This finite control uses even initial gaps.')
    ds = [0] * len(Q)
    for i in range(len(Q) // 2):
        ds[i] = Q[i] // 2
        ds[-1-i] = Q[i] - ds[i]
    assert all(0 <= d < base for d in ds)
    assert ds[-1] > 0
    n = value(ds, base)
    assert pair_word(n, base) == Q
    return n

def main() -> None:
    seeds = 0
    comparisons = 0
    endpoint_checks = 0
    stopped_for_gap = 0
    for m in (3, 5, 9):
        base = m + 1
        for width in range(3):
            for B in product(range(2 * m + 1), repeat=width):
                if B and B[0] == 0:
                    continue
                for c in range(1, 2 * m):
                    if c == m:
                        continue
                    for gap0 in (2, 10, 20):
                        s = State(c, B)
                        gap = gap0
                        n = realize(s, gap, base)
                        seeds += 1
                        for t in range(8):
                            if gap < 2:
                                stopped_for_gap += 1
                                break
                            out = step(m, s)
                            g = overflow(m, s)
                            next_gap = gap + g + 2 * (len(s.B) - len(out.B))
                            assert next_gap >= 0
                            next_n = n + reverse(n, base)
                            expected = out.B + (out.c,) * next_gap + out.B[::-1]
                            actual = pair_word(next_n, base)
                            assert actual == expected, (m, s, gap, out, next_gap, actual, expected)
                            assert len(digits(next_n, base)) - len(digits(n, base)) == g
                            if t + 1 >= m.bit_length() + 1:
                                assert moment(out) % (2 * (m + 2)) == 0
                                endpoint_checks += 1
                            comparisons += 1
                            s, gap, n = out, next_gap, next_n
    report = {
        'status': 'FINITE_LITERAL_CONTROLS_PASS',
        'bases': [4, 6, 10], 'initial_width_cap': 2,
        'initial_gaps': [2, 10, 20], 'transition_cap': 8,
        'realized_start_instances': seeds, 'ordinary_integer_transition_comparisons': comparisons,
        'post_bound_residue_checks': endpoint_checks, 'runs_stopped_at_small_gap': stopped_for_gap,
        'scope': 'All initial coefficients in range at the stated width cap, positive outer head, '
                 'all positive nonneutral interior phases. Each step compared with literal integer '
                 'addition and reversal. Comparison stops when the computed gap is below 2. '
                 'No all-time finite-gap realizability or palindrome-avoidance conclusion.'
    }
    Path(__file__).with_name('literal_controls.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
