#!/usr/bin/env python3
"""Independent bounded semantic controls. This is not a Lean proof.

Run with Python 3, no third-party packages. No randomness or concurrency.
Exact decimal integer reversal is independent of column normalization.
"""
import hashlib
import itertools
import json
import pathlib
import platform

HERE = pathlib.Path(__file__).resolve().parent
PIN = '4ffba5a60b6089075f6e3e4ab5952eb6bc46a4d7'

def reverse_add(n):
    return n + int(str(n)[::-1])

def columns(n):
    digits = [int(d) for d in reversed(str(n))]
    return tuple(a + b for a, b in zip(digits, reversed(digits)))

def realize(q):
    """Choose digits from mirrored sums, with a nonzero leading digit."""
    L = len(q)
    d = [0] * L
    for i in range((L + 1) // 2):
        j = L - 1 - i
        if i == j:
            assert q[i] % 2 == 0
            d[i] = q[i] // 2
        else:
            d[j] = min(q[i], 9)
            d[i] = q[i] - d[j]
    n = sum(v * 10**i for i, v in enumerate(d))
    assert len(str(n)) == L and columns(n) == q
    return n

def normalize(q):
    carries = [0]
    out = []
    for a in q:
        v = a + carries[-1]
        out.append(v % 10)
        carries.append(v // 10)
    if carries[-1]:
        out.append(carries[-1])
    return tuple(a + b for a, b in zip(out, reversed(out))), carries, out

def advance(s, e):
    a, b, c = s
    l1 = a // 10
    l2 = (b + l1) // 10
    d0, d1, d2 = a % 10, (b + l1) % 10, (c + l2) % 10
    r2 = (c + e) // 10
    r1 = (b + r2) // 10
    gamma = (a + r1) // 10
    h0, h1, h2 = (a + r1) % 10, (b + r2) % 10, (c + e) % 10
    return ((d0 + h0, d1 + h1, d2 + h2) if gamma == 0 else
            (d0 + 1, d1 + h0, d2 + h1)), gamma

def admissible_words(L):
    ranges = [range(1, 19)] + [range(19)] * ((L + 1) // 2 - 1)
    if L % 2:
        ranges[-1] = range(0, 19, 2)
    for half in itertools.product(*ranges):
        yield tuple(half + (half[-2::-1] if L % 2 else half[::-1]))

def trace(q, horizon):
    n = realize(q)
    out = []
    overflows = 0
    for t in range(horizon + 1):
        nq, carry, digits = normalize(q)
        out.append({'t': t, 'integer': str(n), 'width': len(q), 'q': q,
                    'prefix': q[:3], 'inner_carry': carry[len(q)-3],
                    'outgoing_overflow': carry[-1], 'overflows_so_far': overflows})
        q = nq
        n = reverse_add(n)
        overflows += carry[-1]
    return out

def main():
    result = {'evidence_label': 'bounded exact diagnostic, not formal proof',
              'source_commit': PIN, 'python': platform.python_version(),
              'algorithm': 'all admissible symmetric q words; canonical digit realization; literal decimal reversal',
              'parameters': {'projection_widths': [3, 4, 5, 6, 7, 8],
                             'orbit_initial_widths': [3, 4, 5, 6], 'orbit_horizon': 24},
              'projection': [], 'orbit': []}
    digest = hashlib.sha256()
    witnesses = {}
    for L in range(3, 9):
        count = 0
        branch_counts = [0, 0]
        examples = {}
        for q in admissible_words(L):
            nq, carry, digits = normalize(q)
            n = realize(q)
            out = reverse_add(n)
            projected, gamma = advance(q[:3], carry[L-3])
            assert projected == nq[:3]
            assert gamma == carry[-1]
            assert len(nq) == L + gamma
            assert columns(out) == nq
            assert len(str(out)) == len(nq)
            assert out == sum(d * 10**i for i, d in enumerate(digits))
            count += 1
            branch_counts[gamma] += 1
            examples.setdefault(str(gamma), {'q': q, 'integer': str(n), 'next_integer': str(out),
                                            'inner_carry': carry[L-3], 'next_q': nq})
            digest.update((f'{L}:{q}:{carry}:{nq}:{out}\n').encode())
        result['projection'].append({'L': L, 'words': count, 'branch_counts': branch_counts,
                                     'first_examples_by_overflow': examples, 'mismatches': 0})
    for L in range(3, 7):
        count = steps = closed = saturated_closed = 0
        time_counts = {}
        for initial in admissible_words(L):
            q, n, overflows = initial, realize(initial), 0
            count += 1
            for t in range(1, 25):
                nq, carry, _ = normalize(q)
                p, gamma = advance(q[:3], carry[len(q)-3])
                assert p == nq[:3] and gamma == carry[-1]
                n = reverse_add(n)
                q = nq
                overflows += gamma
                assert columns(n) == q and len(str(n)) == L + overflows == len(q)
                steps += 1
                if q[:3] == initial[:3]:
                    closed += 1
                    assert 2 * overflows <= t
                    assert t <= 10 * overflows
                    if t % 8 and 'nonsaturated_return' not in witnesses:
                        witnesses['nonsaturated_return'] = trace(initial, t)
                    if 2 * len(q) == 2 * L + t:
                        saturated_closed += 1
                        time_counts[t] = time_counts.get(t, 0) + 1
                        assert t % 8 == 0
                        witnesses.setdefault('saturated_return', trace(initial, t))
        result['orbit'].append({'initial_width': L, 'words': count, 'checked_steps': steps,
                                'positive_closed_prefixes': closed,
                                'positive_saturated_closed_prefixes': saturated_closed,
                                'saturated_return_time_counts': time_counts, 'mismatches': 0})
    result['projection_transcript_sha256'] = digest.hexdigest()
    result['witnesses'] = witnesses
    result['limits'] = ['No claim beyond stated finite enumeration bounds.',
                        'No inference that every abstract path has a whole-word lift.',
                        'No palindrome-avoidance or infinite-orbit conclusion.',
                        'This script performs no Lean compilation.']
    target = HERE / 'exact-diagnostics.json'
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'witnesses'}, indent=2))
    print('Witness kinds:', sorted(witnesses))

if __name__ == '__main__':
    main()
