#!/usr/bin/env python3
"""Finite ordinary-integer controls for safety, double-gate composition and signed defects."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
PINS = {
    'Agent100GroupIIDynamics': '07b8c8d8c0c6fa4aefa1034272464531e27353586066651fd5dda55408d3091c',
    'Agent100GroupIISafety': 'c41ca271d9749e90c4490e676cecfb9e1de5d52164ecd9ec2d3e136e0925ec9f',
    'Agent100DoubleGate': '192b21fc4335c69850c4609084ca8c8c2482241204e9c71f4006c1bf87ab8ebb',
    'Agent100GroupIIDefect': '7dce1b0a08a5c0d86cfaf4cbb3584a9a3c7a0f294602170e7b44c11111eadb0f',
}

def digits(n):
    return [int(c) for c in str(n)][::-1]

def value(q):
    return sum(c * 10 ** i for i, c in enumerate(q))

def normalized(q):
    return digits(value(q))

def pair_of(n):
    ds = digits(n)
    return [a + b for a, b in zip(ds, reversed(ds))]

def next_columns(q):
    return pair_of(value(q))

def step(n):
    return n + int(str(n)[::-1])

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

def initial(r, p, u, v):
    return five_word(r, p, u, u + v, 2 * v)

def middle(r, p, u, v):
    return five_word(r, 2 * p, 2 * u + 1, 2 * (u + v) - 19, 4 * v - 18)

def returned_component(r, p, u, v):
    q = [0] * (2 * r + 6)
    q[0] = q[-1] = 4 * p
    q[r:r + 6] = [1, 4 * u - 19, 4 * v - 18, 4 * v - 18, 4 * u - 19, 1]
    return q

def shifted(q):
    out = [0] * (len(q) + 1)
    for i, x in enumerate(q):
        out[i] += x
        out[i + 1] += x
    return out

def realize(q, choose_high):
    assert q == q[::-1] and q[0] > 0 and all(0 <= x <= 18 for x in q)
    ds = [0] * len(q)
    for i in range(len(q) // 2):
        j = len(q) - 1 - i
        lower = max(1 if i == 0 else 0, q[i] - 9)
        ds[j] = min(9, q[i]) if choose_high else lower
        ds[i] = q[i] - ds[j]
    center = len(q) // 2
    assert q[center] % 2 == 0
    ds[center] = q[center] // 2
    assert ds[-1] > 0 and all(0 <= x <= 9 for x in ds)
    n = value(ds)
    assert pair_of(n) == q and len(digits(n)) == len(q)
    return n

def main():
    root = next(p for p in HERE.parents if (p / 'proofs/Agent100GroupIIDynamics.lean').is_file())
    for module, h in PINS.items():
        assert hashlib.sha256((root / ('proofs/' + module + '.lean')).read_bytes()).hexdigest() == h
    spacers = [1, 2, 3, 5, 10, 20]
    cores = [(u, v) for u in range(5, 9) for v in range(5, 7) if u + v <= 13]
    safety, defects, doubles = [], [], []
    for r in spacers:
        for p in range(1, 5):
            for u, v in cores:
                q = initial(r, p, u, v)
                mid = middle(r, p, u, v)
                ret = shifted(returned_component(r, p, u, v))
                for choose_high in [False, True]:
                    n = realize(q, choose_high)
                    n1, n2 = step(n), step(step(n))
                    checks = {
                        'ordinary_first_pair': pair_of(n1) == mid,
                        'ordinary_second_pair': pair_of(n2) == ret,
                        'positive_time_one_nonpalindrome': str(n1) != str(n1)[::-1],
                        'positive_time_two_nonpalindrome': str(n2) != str(n2)[::-1],
                        'width_preserved': len(str(n1)) == len(q) == len(str(n2)),
                    }
                    assert all(checks.values()), (r, p, u, v, choose_high, checks)
                    safety.append({'r': r, 'p': p, 'u': u, 'v': v, 'high_digit_split': choose_high,
                                   'n': str(n), 'n1': str(n1), 'n2': str(n2), 'checks': checks})
                redundant = [2 * x for x in q]
                cd = [0] * len(q)
                cd[r + 1:r + 6] = [1, -19, -18, -19, 1]
                dd = [0] * len(q)
                dd[r + 1:r + 6] = [1, 1, 0, -1, -1]
                checks = {
                    'coefficient_defect': [a - b for a, b in zip(mid, redundant)] == cd,
                    'digit_defect': [a - b for a, b in zip(normalized(mid), normalized(redundant))] == dd,
                    'antisymmetry': dd == [-x for x in dd[::-1]],
                    'seam_cancels': next_columns(mid) == next_columns(redundant),
                    'no_overflow_both': len(normalized(mid)) == len(q) == len(normalized(redundant)),
                    'redundant_exceeds_admissible_cap': redundant[r + 3] > 18,
                    'new_shape_witness': returned_component(r, p, u, v)[r] == 1 and component(r, p, u, v)[r] == 0,
                }
                assert all(checks.values()), (r, p, u, v, checks)
                defects.append({'r': r, 'p': p, 'u': u, 'v': v, 'checks': checks})
        q0 = initial(r, 1, 1, 6)
        q2 = next_columns(next_columns(q0))
        q3 = next_columns(q2)
        q4 = next_columns(q3)
        c = component(r, 1, 1, 6)
        for _ in range(4):
            c = next_columns(c)
        for choose_high in [False, True]:
            n = realize(q0, choose_high)
            orbit = [n]
            for _ in range(4):
                orbit.append(step(orbit[-1]))
            checks = {
                'first_handoff': q2 == initial(r, 4, 5, 5),
                'time_three_pair': q3 == middle(r, 4, 5, 5),
                'time_four_pair': q4 == shifted(returned_component(r, 4, 5, 5)),
                'component_four_return': c == returned_component(r, 4, 5, 5),
                'time_three_overlap_fails': q3 != shifted(component(r, 8, 10, 10)),
                'time_three_seam_plus_one': q3[r + 1] == shifted(component(r, 8, 10, 10))[r + 1] + 1,
                'ordinary_handoff': pair_of(orbit[2]) == q2,
                'ordinary_four_return': pair_of(orbit[4]) == q4,
                'all_four_positive_outputs_nonpalindrome': all(str(x) != str(x)[::-1] for x in orbit[1:]),
                'all_widths_preserved': all(len(str(x)) == len(q0) for x in orbit),
            }
            assert all(checks.values()), (r, choose_high, checks)
            doubles.append({'r': r, 'high_digit_split': choose_high, 'ordinary_orbit': [str(x) for x in orbit], 'checks': checks})
    report = {'status': 'PASS', 'kind': 'FINITE_INDEPENDENT_ORDINARY_INTEGER_AND_DEFECT_CONTROLS',
              'source_pins': PINS, 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'safety_cases': len(safety), 'defect_cases': len(defects), 'double_gate_cases': len(doubles),
              'named_assertions': len(safety) * 5 + len(defects) * 7 + len(doubles) * 10,
              'method': 'Exact Python integers, ordinary decimal reverse-and-add, two explicit canonical digit splits, coefficient normalization and reflected digit sums. No Lean evaluation or cached outputs.',
              'scope': 'Finite controls only; the arbitrary-positive-r statements and universal realization results are established by Lean, not by these samples.',
              'safety': safety, 'defects': defects, 'double_gate': doubles}
    output = HERE / 'independent_decimal_controls.json'
    assert not output.exists()
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['status', 'safety_cases', 'defect_cases', 'double_gate_cases', 'named_assertions']}))

if __name__ == '__main__':
    main()
