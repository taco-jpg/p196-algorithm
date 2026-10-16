#!/usr/bin/env python3
"""Exact exploratory carry calculations. Outputs are not Lean proofs."""
import argparse
from functools import lru_cache
from itertools import product
import json
from pathlib import Path


def step(q):
    c = 0
    carries = [0]
    digits = []
    for a in q:
        s = a + c
        digits.append(s % 10)
        c = s // 10
        carries.append(c)
    if c:
        digits.append(c)
    assert digits[-1] > 0 and all(0 <= x < 10 for x in digits)
    return tuple(x + y for x, y in zip(digits, reversed(digits))), tuple(carries)


def seed(q):
    ds = [0] * len(q)
    for i in range(len(q) // 2):
        ds[i] = max(0, q[i] - 9)
        ds[-1-i] = min(9, q[i])
    if len(q) % 2:
        assert q[len(q)//2] % 2 == 0
        ds[len(q)//2] = q[len(q)//2] // 2
    assert ds[-1] > 0
    return sum(d * 10**i for i, d in enumerate(ds))


def pair_words(width):
    if width == 1:
        for a in range(2, 19, 2):
            yield (a,)
        return
    for a in range(1, 19):
        for tail in product(range(19), repeat=width//2-1):
            half = (a,) + tail
            if width % 2:
                for center in range(0, 19, 2):
                    yield half + (center,) + half[::-1]
            else:
                yield half + half[::-1]


def outside_step(state, e):
    single, a, b = state
    if single:
        if a < 10:
            return (1, 2*a, 0), 1
        v = a % 10 + 1
        return (0, v, v), 0
    lo = a // 10
    hi = (b + e) // 10
    overflow = (a + hi) // 10
    if overflow == 0:
        return (0, 2*a + hi, (b + lo) % 10 + (b + e) % 10), 1
    return (0, a % 10 + 1, (b + lo) % 10 + (a + hi) % 10), 0


@lru_cache(None)
def budget(k, state):
    if k == 0:
        return 0
    return min(cost + budget(k-1, nxt)
               for nxt, cost in (outside_step(state, e) for e in (0, 1)))


def minimizing_path(k, state):
    rows = []
    while k:
        e = min((0, 1), key=lambda x: outside_step(state, x)[1]
                + budget(k-1, outside_step(state, x)[0]))
        nxt, cost = outside_step(state, e)
        rows.append({'state': state, 'control': e, 'cost': cost, 'next': nxt})
        state = nxt
        k -= 1
    return rows


def explore(max_width):
    states = [(1, a, 0) for a in range(2, 19, 2)]
    states += [(0, a, b) for a in range(1, 19) for b in range(19)]
    bounds = []
    for k in range(13):
        v = min(budget(k, s) for s in states)
        witness = min(states, key=lambda s: budget(k, s))
        row = {'horizon': k, 'min_nonoverflows': v,
               'start': witness, 'path': minimizing_path(k, witness)}
        bounds.append(row)
        print('OUTSIDE_BUDGET', k, v, witness, flush=True)
    results = []
    for width in range(1, max_width+1):
        seen = [dict() for _ in range(11)]
        collisions = [None] * 11
        count = 0
        for q in pair_words(width):
            count += 1
            current = q
            history = []
            for k in range(11):
                current, cs = step(current)
                history.append(cs)
                key = tuple(history)
                other = seen[k].get(key)
                if other is None:
                    seen[k][key] = q
                elif collisions[k] is None:
                    collisions[k] = {'left': other, 'right': q,
                        'left_seed': seed(other), 'right_seed': seed(q),
                        'history': key}
        assert collisions[10] is None, 'violates the existing eleven-word theorem'
        row = {'width': width, 'pair_word_count': count,
               'distinct_histories': [len(s) for s in seen],
               'first_collisions': collisions}
        results.append(row)
        longest = max((k+1 for k, c in enumerate(collisions) if c), default=0)
        print('PAIR_SEARCH', width, count, 'longest_shared_prefix', longest,
              'distinct', row['distinct_histories'], flush=True)
        if longest:
            print('WITNESS', json.dumps(collisions[longest-1]), flush=True)
    return {'status': 'EXPLORATORY_NOT_PROOF', 'max_width': max_width,
            'outside_budgets': bounds, 'finite_history_search': results}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-width', type=int, default=7)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.max_width <= 9:
        raise SystemExit('max-width must lie between 1 and 9')
    data = explore(args.max_width)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, indent=2) + '\n')
