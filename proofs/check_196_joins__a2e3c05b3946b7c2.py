"""Exact finite orbit-join check for the unresolved original gate cases.

An exact join transfers the all-time question but does not solve it. No join
within these explicit horizons is also not an infinite separation result.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from finite_tail_census import pair_word, realize

HERE = Path(__file__).resolve().parent


def main():
    horizon = 1500
    n = 196
    reference = {n: 0}
    reference_digest = hashlib.sha256((str(n) + '\n').encode())
    for t in range(1, horizon + 1):
        n += int(str(n)[::-1])
        reference[n] = t
        reference_digest.update((str(n) + '\n').encode())
    cases = [(r, 1, 6) for r in range(1, 5)]
    cases += [(r, 1, 7) for r in list(range(1, 17)) + [32, 64, 127] if r != 3]
    results = []
    for r, u, v in cases:
        n = seed = realize(pair_word(r, u, v))
        joined = None
        first_hit = None
        trace_digest = hashlib.sha256((str(n) + '\n').encode())
        for t in range(horizon + 1):
            if n in reference:
                joined = {'gate_index': t, 'index_from_196': reference[n], 'shared_value': str(n)}
                break
            if t and str(n) == str(n)[::-1]:
                first_hit = t
                break
            if t == horizon:
                break
            n += int(str(n)[::-1])
            trace_digest.update((str(n) + '\n').encode())
        results.append({'r': r, 'u': u, 'v': v, 'seed': str(seed),
                        'join': joined, 'first_positive_palindrome_time': first_hit,
                        'steps_checked': t, 'trajectory_sha256': trace_digest.hexdigest(),
                        'last_value': str(n)})
    out = {'scope': 'finite exact integer joins; no all-time assertion',
           'reference_seed': 196, 'reference_horizon': horizon, 'candidate_horizon': horizon,
           'reference_trajectory_sha256': reference_digest.hexdigest(),
           'cases': results, 'joins_found': sum(c['join'] is not None for c in results),
           'main_existence_proved': False}
    (HERE / 'joins_196.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
