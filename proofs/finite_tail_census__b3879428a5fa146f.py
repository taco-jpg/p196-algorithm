"""Literal decimal census of the six original delayed-repair families.

This is finite evidence only. Every requested case is retained, including
nontermination within the stated horizon. No discovery routine is imported.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

sys.set_int_max_str_digits(100000)
HERE = Path(__file__).resolve().parent
DOMAIN = ((1, 5), (1, 6), (1, 7), (2, 5), (2, 6), (3, 5))


def pair_word(r: int, u: int, v: int) -> tuple[int, ...]:
    a = (1,) + (0,) * r + (u, v, v, u) + (0,) * r + (1,)
    q = tuple(x + y for x, y in zip(a + (0,), (0,) + a))
    assert q == q[::-1] and q[0] > 0 and max(q) <= 18
    assert q[len(q) // 2] % 2 == 0
    return q


def realize(q: tuple[int, ...]) -> int:
    d = [0] * len(q)
    for i in range(len(q) // 2):
        d[i] = max(0, q[i] - 9)
        d[-1 - i] = q[i] - d[i]
    d[len(q) // 2] = q[len(q) // 2] // 2
    assert all(0 <= x <= 9 for x in d) and d[-1] != 0
    return int(''.join(map(str, reversed(d))))


def census_case(r: int, u: int, v: int, horizon: int) -> dict:
    n = realize(pair_word(r, u, v))
    seed = n
    digest = hashlib.sha256()
    first_hit = None
    for t in range(1, horizon + 1):
        n += int(str(n)[::-1])
        digits = str(n)
        digest.update((digits + '\n').encode())
        if digits == digits[::-1]:
            first_hit = t
            break
    return {
        'r': r, 'u': u, 'v': v, 'seed': str(seed),
        'status': 'TERMINATES' if first_hit is not None else 'UNKNOWN',
        'first_positive_palindrome_time': first_hit,
        'steps_checked': t, 'last_digits': len(str(n)),
        'last_value': str(n), 'trajectory_sha256': digest.hexdigest(),
    }


def main() -> None:
    spacers = list(range(1, 33)) + [64, 127, 256, 512]
    horizon = 512
    cases = [census_case(r, u, v, horizon) for u, v in DOMAIN for r in spacers]
    result = {
        'scope': 'finite literal-integer census; no all-r or all-time conclusion',
        'domain': DOMAIN, 'spacers': spacers, 'horizon': horizon,
        'case_count': len(cases), 'cases': cases,
        'main_existence_proved': False,
    }
    (HERE / 'finite_tail_census.json').write_text(json.dumps(result, indent=2) + '\n')
    summary = []
    for u, v in DOMAIN:
        selected = [c for c in cases if (c['u'], c['v']) == (u, v)]
        summary.append({'u': u, 'v': v,
                        'terminated': sum(c['status'] == 'TERMINATES' for c in selected),
                        'first_hits': sorted({c['first_positive_palindrome_time']
                                             for c in selected
                                             if c['first_positive_palindrome_time'] is not None}),
                        'unknown_spacers': [c['r'] for c in selected if c['status'] == 'UNKNOWN']})
    print(json.dumps({'cases': len(cases), 'horizon': horizon, 'summary': summary}, indent=2))


if __name__ == '__main__':
    main()
