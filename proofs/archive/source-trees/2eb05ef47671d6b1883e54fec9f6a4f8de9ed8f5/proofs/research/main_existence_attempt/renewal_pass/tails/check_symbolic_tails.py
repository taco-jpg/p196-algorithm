"""Independent sparse-polynomial replay of finite all-parameter first hits.

This checker imports neither the run generator nor its normalizer/alignment.
Affine exponents are formal pairs (coefficient of k, constant). It verifies
every carry/digit/pair/difference identity over the entire orthant k>=0.
"""
from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def clean(p):
    return {e: c for e, c in p.items() if c}


def add(*polys):
    result = defaultdict(int)
    for poly in polys:
        for e, c in poly.items():
            result[e] += c
    return clean(result)


def scale(poly, factor):
    return {e: c * factor for e, c in poly.items() if c * factor}


def plus(a, b):
    return (a[0] + b[0], a[1] + b[1])


def numerator(runs, carry=False):
    """Return (x-1) times the polynomial, width, outgoing carry.

    The input domain of a carry word is checked separately. A column x<=8
    kills carry, x=9 transmits it, and x>=10 sets it, so the carry after the
    first position of a constant run persists throughout that run.
    """
    p, position, outgoing = defaultdict(int), (0, 0), 0
    for value, coefficients, constant in runs:
        assert len(coefficients) == 1 and coefficients[0] >= 0 and constant >= 1
        end = plus(position, (coefficients[0], constant))
        if carry:
            outgoing = (value + outgoing) // 10
            assert outgoing in (0, 1) and (value + outgoing) // 10 == outgoing
            coefficient = outgoing
        else:
            coefficient = value
        p[end] += coefficient
        p[position] -= coefficient
        position = end
    return clean(p), position, outgoing


def reflection(poly, width):
    return {(width[0] - e[0], width[1] - e[1]): -c for e, c in poly.items()}


def expand(runs, k):
    return tuple(value for value, coefficients, constant in runs
                 for _ in range(coefficients[0] * k + constant))


def literal_seed(r, u, v):
    a = (1,) + (0,) * r + (u, v, v, u) + (0,) * r + (1,)
    q = tuple(x + y for x, y in zip(a + (0,), (0,) + a))
    d = [0] * len(q)
    for j in range(len(q) // 2):
        d[j] = max(q[j] - 9, 0)
        d[-1-j] = q[j] - d[j]
    d[len(q) // 2] = q[len(q) // 2] // 2
    return int(''.join(map(str, d[::-1])))


def check_certificate(record):
    u, v, lower, hit = [record[k] for k in ('u', 'v', 'r_min', 'first_positive_palindrome_time')]
    states, ds, diffs, flags = [record[k] for k in
        ('states', 'output_digit_words', 'digit_reflection_differences', 'overflow_flags')]
    assert len(states) == hit + 1 and len(ds) == len(diffs) == len(flags) == hit
    expected_start = [[1, [0], 2], [0, [1], lower-1], [u, [0], 1],
                      [u+v, [0], 1], [2*v, [0], 1], [u+v, [0], 1],
                      [u, [0], 1], [0, [1], lower-1], [1, [0], 2]]
    assert numerator(states[0])[:2] == numerator(expected_start)[:2]
    for t in range(hit):
        q, out, digits, delta, flag = states[t], states[t+1], ds[t], diffs[t], flags[t]
        assert all(0 <= x <= 18 for x, _, _ in q + out)
        assert q[0][0] > 0 and out[0][0] > 0
        Q, L, _ = numerator(q)
        assert Q == reflection(Q, L)
        C, _, h = numerator(q, carry=True)
        assert h == flag
        D = add(Q, {plus(e, (0, 1)): c for e, c in C.items()}, scale(C, -10))
        claimed_D, W, _ = numerator(digits)
        assert W == plus(L, (0, flag)) and D == claimed_D
        assert all(0 <= x <= 9 for x, _, _ in digits) and digits[-1][0] > 0
        paired, output_width, _ = numerator(out)
        assert output_width == W and paired == add(D, reflection(D, W))
        diff, diff_width, _ = numerator(delta)
        assert diff_width == W and diff == add(D, scale(reflection(D, W), -1))
        assert all(-9 <= x <= 9 for x, _, _ in delta)
        # Positive run lengths prohibit cancellation between disjoint intervals
        # for every k>=0, even if formal exponents coincide across parameters.
        is_palindrome = all(x == 0 for x, _, _ in delta)
        assert is_palindrome == (t + 1 == hit)
    # Independent ordinary-integer controls, not used for universal inference.
    controls = 0
    for k in (0, 1, 2, 3, 7, 31, 127, 1024):
        n = literal_seed(lower + k, u, v)
        for t in range(hit):
            n += int(str(n)[::-1])
            digit_tuple = tuple(map(int, str(n)[::-1]))
            assert digit_tuple == expand(ds[t], k)
            assert (str(n) == str(n)[::-1]) == (t+1 == hit)
            controls += 1
    return controls


def main():
    certificate_path = HERE / 'symbolic_tail_certificates.json'
    data = json.loads(certificate_path.read_text())
    controls = sum(check_certificate(c) for c in data['certificates'])
    finite_boundaries = []
    for c in data['certificates']:
        lower = 5 if (c['u'], c['v']) == (1, 6) else 1
        for r in range(lower, c['r_min']):
            n = literal_seed(r, c['u'], c['v'])
            seed = n
            for t in range(1, c['first_positive_palindrome_time'] + 1):
                n += int(str(n)[::-1])
                assert (str(n) == str(n)[::-1]) == (t == c['first_positive_palindrome_time'])
            finite_boundaries.append({'u': c['u'], 'v': c['v'], 'r': r,
                                     'seed': str(seed), 'first_hit': t, 'palindrome': str(n)})
    out = {'status': 'PASS', 'scope': 'exact all-parameter polynomial identities plus explicit small boundaries',
           'certificate_sha256': hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
           'symbolic_transition_count': sum(c['first_positive_palindrome_time'] for c in data['certificates']),
           'ordinary_integer_transition_controls': controls, 'finite_boundaries': finite_boundaries,
           'imports_generator_or_run_normalizer': False, 'parameter_sampling_used_as_proof': False,
           'formalized_in_Lean': False, 'main_existence_proved': False}
    (HERE / 'symbolic_tail_audit.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
