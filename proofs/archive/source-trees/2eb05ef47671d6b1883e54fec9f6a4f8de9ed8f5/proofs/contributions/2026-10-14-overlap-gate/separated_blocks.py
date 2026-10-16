"""Controls for exact block separation and its finite exhaustion bound.

The all-input argument is in SEPARATION_EXHAUSTION.md.  This checker checks
the finite outer-column potential inequalities exhaustively and tests the
block formula using ordinary integer arithmetic, including gap=1.
"""
from __future__ import annotations

import json
from pathlib import Path
import random
import sys

from exact_gate_lifetimes import initial_word, realize


def normal(word):
    value = sum(coefficient*10**i for i, coefficient in enumerate(word))
    digits = tuple(map(int, str(value)[::-1]))
    return digits, len(digits)-len(word)


def pair(digits):
    return tuple(a+b for a, b in zip(digits, digits[::-1]))


def symmetric(word):
    return (bool(word) and word == word[::-1]
            and 1 <= word[0] <= 18 and all(0 <= c <= 18 for c in word)
            and (len(word) % 2 == 0 or word[len(word)//2] % 2 == 0))


def separated_step(b, h, gap):
    assert symmetric(b) and symmetric(h) and gap >= 1
    bd, exterior_overflow = normal(b)
    hd, core_overflow = normal(h)
    assert exterior_overflow in (0, 1) and core_overflow in (0, 1)
    delta = max(exterior_overflow, core_overflow)
    new_b = pair(bd)
    new_h = [0]*(len(h)+2*delta-exterior_overflow)
    for i, digit in enumerate(hd):
        new_h[delta-exterior_overflow+i] += digit
        new_h[len(h)+delta-1-i] += digit
    new_h = tuple(new_h)
    assert symmetric(new_b) and symmetric(new_h)
    return new_b, new_h, gap-delta


def whole(b, h, gap):
    return b+(0,)*gap+h+(0,)*gap+b[::-1]


def actual_step(q):
    seed = realize(q)
    successor = seed+int(str(seed)[::-1])
    return pair(tuple(map(int, str(successor)[::-1])))


def potential(a):
    if a == 1:
        return 4
    if a == 2:
        return 3
    if a in (3, 4, 5):
        return 2
    if a in (6, 7, 8, 9, 10):
        return 1
    return 0


def check_potential():
    cases = 0
    for a in range(1, 19):
        for incoming in (0, 1):
            overflow = (a+incoming)//10
            assert overflow in (0, 1)
            new_a = (2*a+incoming if not overflow else a+1-10*(a//10))
            assert 1 <= new_a <= 18
            assert potential(new_a)+1 <= potential(a)+4*overflow
            cases += 1
    return cases


def random_word(rng, length):
    left = [rng.randrange(19) for _ in range(length//2)]
    middle = [2*rng.randrange(10)] if length % 2 else []
    if left:
        left[0] = rng.randrange(1, 19)
    elif middle:
        middle[0] = 2*rng.randrange(1, 10)
    return tuple(left+middle+left[::-1])


def check_blocks():
    rng = random.Random(1961714)
    checks = 0
    for _ in range(3000):
        b = random_word(rng, rng.randrange(1, 9))
        h = random_word(rng, rng.randrange(1, 11))
        gap = rng.choice((1, 1, 1, 2, 3, 5))
        new_b, new_h, new_gap = separated_step(b, h, gap)
        assert actual_step(whole(b, h, gap)) == whole(new_b, new_h, new_gap)
        bd, e = normal(b)
        hd, f = normal(h)
        wd, _ = normal(whole(b, h, gap))
        assert (wd == wd[::-1]) == (e == f and bd == bd[::-1] and hd == hd[::-1])
        checks += 1
    return checks


def check_gate_separation():
    cases = []
    for r in tuple(range(2, 17))+(31, 64, 127):
        b, h, gap = (1, 1), (1, 8, 14, 8, 1), r-1
        q = initial_word(r, 1, 7)
        assert q == whole(b, h, gap)
        bound = 4*gap+potential(b[0])-3
        t = 0
        while gap:
            q = actual_step(q)
            b, h, gap = separated_step(b, h, gap)
            t += 1
            assert q == whole(b, h, gap)
            assert t <= bound
        cases.append({'r': r, 'first_zero_gap_time': t, 'upper_bound': bound})
    return cases


def record_initial_discovery():
    """Archive the finite scans that motivated the exact proofs.

    None means only 'no hit in this finite 300-step scan'.  These records
    are deliberately separate from the universal statements.
    """
    samples = (1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 16, 20, 30, 50, 100, 200)
    cores = ((1, 5), (1, 6), (1, 7), (2, 5), (2, 6), (3, 5))
    records = []
    for u, v in cores:
        for r in samples:
            n = realize(initial_word(r, u, v))
            hit = None
            for t in range(1, 301):
                n += int(str(n)[::-1])
                if str(n) == str(n)[::-1]:
                    hit = t
                    break
            records.append({'core': [u, v], 'r': r,
                            'first_hit_through_300': hit})
    b, h, gap = (1, 1), (1, 8, 14, 8, 1), 59
    separated_trace = []
    for t in range(31):
        _, exterior_overflow = normal(b)
        separated_trace.append({'t': t, 'exterior': b, 'gap': gap,
                                'core': h, 'next_exterior_overflow': exterior_overflow})
        b, h, gap = separated_step(b, h, gap)
    orbit_samples = []
    for u, v in ((2, 5), (2, 6), (3, 5), (1, 6)):
        q = initial_word(7, u, v)
        states = []
        for t in range(12):
            digits, _ = normal(q)
            states.append({'t': t, 'pair_word': q,
                           'next_ordinary_iterate_palindromic': digits == digits[::-1]})
            q = pair(digits)
        orbit_samples.append({'r': 7, 'core': [u, v], 'states': states})
    result = {
        'status': 'finite exploration records; null is not an all-time conclusion',
        'initial_300_step_scan': records,
        'initial_separated_trace_r_60_core_1_7': separated_trace,
        'initial_r_7_orbit_samples_including_post_hit_states': orbit_samples,
        'discarded_inference': 'No inference of infinite safety was made from these scans.',
    }
    path = Path(__file__).with_name('EXPLORATION_RECORDS.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    return len(records)


def main():
    result = {
        'finite_potential_cases': check_potential(),
        'independent_block_controls': check_blocks(),
        'core_1_7_separation_controls': check_gate_separation(),
        'claim': 'exact separation formula; every finite gap exhausted within 4*g+P(a)-3 steps',
        'all_time_core_1_7_safety': 'UNKNOWN',
        'new_Lean_verification': False,
    }
    if '--record-exploration' in sys.argv:
        result['archived_finite_scan_cases'] = record_initial_discovery()
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
