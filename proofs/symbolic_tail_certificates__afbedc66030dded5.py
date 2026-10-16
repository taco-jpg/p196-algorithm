"""All-parameter finite first-hit certificates for the original repair cores.

Lengths are c+a*k for an arbitrary integer k>=0. The existing orthant run
normalizer refuses every ordering not proved throughout that domain.
All attempts, including failures to cover a domain, are recorded.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
sys.path.insert(0, str(PROJECT / 'main_existence_attempt/smart_pass/collision'))
from orthant_runs import Length, constant, canon, normal, add_runs, step, as_json


def q_start(r_min: int, u: int, v: int):
    one = constant(1, 1)
    gap = Length((1,), r_min - 1)
    assert gap.positive()
    return canon([(1, constant(2, 1)), (0, gap), (u, one),
                  (u+v, one), (2*v, one), (u+v, one), (u, one),
                  (0, gap), (1, constant(2, 1))])


def trace(r_min: int, u: int, v: int, target: int):
    q = q_start(r_min, u, v)
    states, digits_by_step, flags, differences = [q], [], [], []
    for t in range(1, target + 1):
        digits, h = normal(q)
        if h:
            digits = canon(digits + [(1, constant(1, 1))])
        difference = add_runs(digits, [(-x, n) for x, n in digits[::-1]])
        hits = all(x == 0 for x, n in difference)
        assert hits == (t == target), ('wrong first-hit time', r_min, u, v, t, hits)
        q, h2 = step(q)
        assert h == h2
        states.append(q)
        flags.append(h)
        digits_by_step.append(digits)
        differences.append(difference)
    return {'r_min': r_min, 'r_parameterization': f'r={r_min}+k, k any integer >=0',
            'u': u, 'v': v, 'first_positive_palindrome_time': target,
            'states': [as_json(q) for q in states],
            'output_digit_words': [as_json(d) for d in digits_by_step],
            'digit_reflection_differences': [as_json(d) for d in differences],
            'overflow_flags': flags}


def main():
    targets = [(1, 5, 3), (2, 5, 4), (2, 6, 4), (3, 5, 4), (1, 6, 11)]
    attempts, certificates = [], []
    for u, v, target in targets:
        for lower in range(2, 33):
            try:
                cert = trace(lower, u, v, target)
            except (AssertionError, ValueError) as exc:
                attempts.append({'u': u, 'v': v, 'r_min': lower,
                                 'status': 'DOMAIN_NOT_CERTIFIED',
                                 'exception': type(exc).__name__, 'detail': repr(exc)})
            else:
                attempts.append({'u': u, 'v': v, 'r_min': lower, 'status': 'CERTIFIED'})
                certificates.append(cert)
                break
        else:
            raise RuntimeError(('no affine certificate obtained', u, v))
    result = {'status': 'symbolic first-hit certificates generated; independent replay required',
              'parameter_model': 'one independent nonnegative integer k; exact coefficientwise comparisons',
              'certificates': certificates, 'attempts': attempts,
              'remaining_core': [1, 7], 'main_existence_proved': False}
    (HERE / 'symbolic_tail_certificates.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'certificates': [{k:c[k] for k in ('u','v','r_min','first_positive_palindrome_time')}
                                      for c in certificates],
                      'attempts': len(attempts)}, indent=2))


if __name__ == '__main__':
    main()
