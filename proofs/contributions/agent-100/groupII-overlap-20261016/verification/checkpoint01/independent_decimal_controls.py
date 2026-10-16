#!/usr/bin/env python3
"""Finite statement/index controls via exact base-10 integers, independent of Lean evaluation."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
EXPECTED_SOURCE = '07b8c8d8c0c6fa4aefa1034272464531e27353586066651fd5dda55408d3091c'

def next_pair_columns(coefficients):
    number = sum(c * 10 ** i for i, c in enumerate(coefficients))
    digits = [int(c) for c in str(number)][::-1]
    return [a + b for a, b in zip(digits, reversed(digits))]

def component(r, p, u, v):
    q = [0] * (2 * r + 6)
    q[0] = q[-1] = p
    q[r + 1:r + 5] = [u, v, v, u]
    return q

def five_word(r, p, a, b, c):
    q = [0] * (2 * r + 7)
    q[0] = q[1] = q[-2] = q[-1] = p
    q[r + 1:r + 6] = [a, b, c, b, a]
    return q

def shift_one(q):
    result = [0] * (len(q) + 1)
    for i, coefficient in enumerate(q):
        result[i] += coefficient
        result[i + 1] += coefficient
    return result

def returned_component(r, p, u, v):
    q = [0] * (2 * r + 6)
    q[0] = q[-1] = 4 * p
    q[r:r + 6] = [1, 4 * u - 19, 4 * v - 18, 4 * v - 18, 4 * u - 19, 1]
    return q

def main():
    root = next(p for p in HERE.parents if (p / 'proofs/Agent100GroupIIDynamics.lean').is_file())
    raw = (root / 'proofs/Agent100GroupIIDynamics.lean').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE
    cores = [(u, v) for u in range(5, 9) for v in range(5, 7) if u + v <= 13]
    assert cores == [(5, 5), (5, 6), (6, 5), (6, 6), (7, 5), (7, 6), (8, 5)]
    rows = []
    for r in [1, 2, 3, 5, 10, 20]:
        for p in range(1, 5):
            for u, v in cores:
                comp = component(r, p, u, v)
                start = five_word(r, p, u, u + v, 2 * v)
                middle = five_word(r, 2 * p, 2 * u + 1, 2 * (u + v) - 19, 4 * v - 18)
                returned = returned_component(r, p, u, v)
                checks = {
                    'initial_overlap': start == shift_one(comp),
                    'component_step_one': next_pair_columns(comp) == component(r, 2 * p, 2 * u, 2 * v),
                    'component_step_two': next_pair_columns(next_pair_columns(comp)) == returned,
                    'whole_step_one': next_pair_columns(start) == middle,
                    'whole_step_two': next_pair_columns(middle) == shift_one(returned),
                    'intermediate_seam_plus_one': middle[r + 1] == shift_one(component(r, 2 * p, 2 * u, 2 * v))[r + 1] + 1,
                    'short_spacer_additive_boundary': shift_one(returned)[1] == 4 * p + (1 if r == 1 else 0),
                    'returned_component_symmetric': returned == returned[::-1],
                }
                assert all(checks.values()), (r, p, u, v, checks)
                rows.append({'r': r, 'p': p, 'u': u, 'v': v, 'checks': checks})
    report = {'status': 'PASS', 'kind': 'FINITE_INDEPENDENT_DECIMAL_STATEMENT_CONTROLS',
              'source_sha256': EXPECTED_SOURCE, 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'case_count': len(rows), 'checks_per_case': 8,
              'method': 'Convert pair-column coefficients to exact integer, extract ordinary decimal digits, and add reflected digits. No Lean execution or cached Lean output used.',
              'scope': 'All 28 p/u/v choices for six selected positive spacer lengths. Finite controls only; arbitrary-r theorem proof comes from Lean.',
              'rows': rows}
    path = HERE / 'independent_decimal_controls.json'
    assert not path.exists()
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'cases': len(rows), 'checks': 8 * len(rows), 'output': str(path)}))

if __name__ == '__main__':
    main()
