#!/usr/bin/env python3
"""Independent finite diagnostics for Agent100 Group II overlap formulas.

The primary trajectory uses ordinary Python integers and decimal string reversal.
Coefficient normalization is a separate cross-check. Nothing here is a Lean proof,
an all-spacer verification, or an all-time palindrome-avoidance statement.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def integer_step(n: int) -> int:
    assert n > 0
    return n + int(str(n)[::-1])


def integer_digits(n: int) -> list[int]:
    assert n > 0
    return [int(c) for c in str(n)[::-1]]


def pair_digits(digits: list[int]) -> list[int]:
    return [a + b for a, b in zip(digits, reversed(digits))]


def integer_pairs(n: int) -> list[int]:
    return pair_digits(integer_digits(n))


def palindromic(n: int) -> bool:
    return str(n) == str(n)[::-1]


def realize(q: list[int]) -> int:
    """Construct one canonical positive numeral with exactly these pair sums."""
    assert q and q == q[::-1] and 0 < q[0] <= 18
    assert all(0 <= x <= 18 for x in q)
    d = [0] * len(q)
    for i in range(len(q) // 2):
        j = len(q) - 1 - i
        # Put a positive digit at the most significant end, including q[0]<10.
        if i == 0:
            d[j] = min(9, q[i])
            d[i] = q[i] - d[j]
        else:
            d[i] = min(9, q[i])
            d[j] = q[i] - d[i]
    if len(q) % 2:
        i = len(q) // 2
        assert q[i] % 2 == 0
        d[i] = q[i] // 2
    assert d[-1] > 0 and all(0 <= x < 10 for x in d)
    n = int(''.join(map(str, reversed(d))))
    assert integer_digits(n) == d and integer_pairs(n) == q
    return n


def normalize(q: list[int]) -> tuple[list[int], list[int]]:
    """Separate grade-school carry computation; retain all boundary carries."""
    d: list[int] = []
    carries = [0]
    for x in q:
        c, digit = divmod(x + carries[-1], 10)
        d.append(digit)
        carries.append(c)
    if carries[-1]:
        assert carries[-1] < 10
        d.append(carries[-1])
    return d, carries


def coefficient_step(q: list[int]) -> list[int]:
    return pair_digits(normalize(q)[0])


def phi(q: list[int]) -> list[int]:
    return [a + b for a, b in zip(q + [0], [0] + q)]


def component(r: int, p: int, u: int, v: int) -> list[int]:
    assert r >= 0
    return [p] + [0] * r + [u, v, v, u] + [0] * r + [p]


def expected_return(r: int, p: int, u: int, v: int) -> list[int]:
    assert r >= 1
    return ([4 * p] + [0] * (r - 1)
            + [1, 4 * u - 19, 4 * v - 18, 4 * v - 18, 4 * u - 19, 1]
            + [0] * (r - 1) + [4 * p])


def difference(a: list[int], b: list[int]) -> list[int]:
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)
            for i in range(n)]


def sparse_difference(a: list[int], b: list[int]) -> list[list[int]]:
    return [[i, x] for i, x in enumerate(difference(a, b)) if x]


def integer_trajectory(q: list[int], length: int) -> tuple[list[int], list[list[int]]]:
    n = realize(q)
    nums = [n]
    pairs = [q]
    for _ in range(length):
        nums.append(integer_step(nums[-1]))
        pairs.append(integer_pairs(nums[-1]))
        assert pairs[-1] == coefficient_step(pairs[-2])
        assert integer_digits(nums[-1]) == normalize(pairs[-2])[0]
    return nums, pairs


def groupII_case(r: int, p: int, u: int, v: int) -> dict:
    a = component(r, p, u, v)
    q = phi(a)
    ns_a, ps_a = integer_trajectory(a, 2)
    ns_q, ps_q = integer_trajectory(q, 2)
    ar = expected_return(r, p, u, v)
    assert len(a) == 2 * r + 6 and len(q) == 2 * r + 7
    assert all(len(w) == len(a) for w in ps_a)
    assert all(len(w) == len(q) for w in ps_q)
    assert ps_a[1] == [2 * x for x in a]
    assert ps_a[2] == ar
    assert ps_q[1] != phi(ps_a[1])
    assert ps_q[2] == phi(ar) == phi(ps_a[2])
    assert not palindromic(ns_q[1]) and not palindromic(ns_q[2])
    j = r + 1
    delta = [0] * len(q)
    delta[j:j + 5] = [1, -19, -18, -19, 1]
    assert difference(ps_q[1], phi(ps_a[1])) == delta
    redundant = phi(ps_a[1])
    actual_digits, actual_carries = normalize(ps_q[1])
    reference_digits, reference_carries = normalize(redundant)
    digit_defect = [0] * len(q)
    digit_defect[j:j + 5] = [1, 1, 0, -1, -1]
    assert actual_carries[-1] == reference_carries[-1] == 0
    assert difference(actual_digits, reference_digits) == digit_defect
    assert digit_defect == [-x for x in digit_defect[::-1]]
    return {
        'parameters': {'r': r, 'p': p, 'u': u, 'v': v},
        'integer_component_orbit': [str(n) for n in ns_a],
        'integer_whole_orbit': [str(n) for n in ns_q],
        'component_pair_orbit': ps_a,
        'whole_pair_orbit': ps_q,
        'coefficient_defect': sparse_difference(ps_q[1], phi(ps_a[1])),
        'normalized_digit_defect': sparse_difference(actual_digits, reference_digits),
        'component_carries': [normalize(w)[1] for w in ps_a[:2]],
        'whole_carries': [normalize(w)[1] for w in ps_q[:2]],
        'ordinary_output_palindrome_flags': [palindromic(n) for n in ns_q[1:]],
        'all_assertions_pass': True,
    }


def double_gate_case(r: int) -> dict:
    # Previously proved Group I (p,u,v)=(1,1,6); its returned (4,5,5) is Group II.
    a = component(r, 1, 1, 6)
    q = phi(a)
    ns_a, ps_a = integer_trajectory(a, 4)
    ns_q, ps_q = integer_trajectory(q, 4)
    assert ps_a[2] == component(r, 4, 5, 5)
    assert ps_q[2] == phi(ps_a[2])
    ar = expected_return(r, 4, 5, 5)
    assert ps_a[4] == ar and ps_q[4] == phi(ar)
    assert [ps_q[t] == phi(ps_a[t]) for t in range(5)] == [True, False, True, False, True]
    assert all(not palindromic(n) for n in ns_q[1:])
    return {
        'r': r,
        'integer_component_orbit': [str(n) for n in ns_a],
        'integer_whole_orbit': [str(n) for n in ns_q],
        'component_pair_orbit': ps_a,
        'whole_pair_orbit': ps_q,
        'overlap_equalities_by_time_0_to_4': [True, False, True, False, True],
        'ordinary_output_palindrome_flags': [False, False, False, False],
        'all_assertions_pass': True,
    }


def boundary_diagnostics() -> dict:
    # These finite mismatches diagnose invalid implementation shortcuts only.
    r, p, u, v = 1, 1, 5, 5
    _, a = integer_trajectory(component(r, p, u, v), 2)
    _, q = integer_trajectory(phi(component(r, p, u, v)), 2)
    assert a[2] == [4, 1, 1, 2, 2, 1, 1, 4]
    assert q[2] == [4, 5, 2, 3, 4, 3, 2, 5, 4]
    dropped_r = []
    for p in range(1, 5):
        for u, v in CORES:
            _, aa = integer_trajectory(component(0, p, u, v), 2)
            _, qq = integer_trajectory(phi(component(0, p, u, v)), 2)
            if qq[2] != phi(aa[2]):
                dropped_r.append({'r': 0, 'p': p, 'u': u, 'v': v,
                                  'component_pair_orbit': aa, 'whole_pair_orbit': qq,
                                  'second_difference': sparse_difference(qq[2], phi(aa[2]))})
    assert dropped_r
    # First outside point of the p bound, at a nonminimal spacer.
    _, aa = integer_trajectory(component(2, 5, 5, 5), 2)
    _, qq = integer_trajectory(phi(component(2, 5, 5, 5)), 2)
    assert qq[2] != phi(aa[2])
    return {
        'r1_adjacent_exterior': {
            'parameters': {'r': 1, 'p': 1, 'u': 5, 'v': 5},
            'component_two_step': a[2],
            'whole_two_step': q[2],
            'second_whole_coefficient': q[2][1],
            'incorrect_constant_exterior_prediction': 4,
            'message': 'At r=1, shiftOne adds the newborn central 1 to exterior 4p; second coefficient is 4p+1.'},
        'r0_first_failure': dropped_r[0],
        'r0_failure_count_among_28_diagnostics': len(dropped_r),
        'p5_failure': {'r': 2, 'p': 5, 'u': 5, 'v': 5,
                       'component_pair_orbit': aa, 'whole_pair_orbit': qq,
                       'second_difference': sparse_difference(qq[2], phi(aa[2]))},
    }


CORES = [(u, v) for u in range(5, 9) for v in (5, 6) if u + v <= 13]
SPACERS = list(range(1, 31)) + [100]


def main() -> None:
    assert len(CORES) == 7
    group = [groupII_case(r, p, u, v) for r in SPACERS for p in range(1, 5) for u, v in CORES]
    double = [double_gate_case(r) for r in SPACERS]
    output = {
        'schema_version': 1,
        'status': 'FINITE_DIAGNOSTICS_PASS_NOT_A_LEAN_PROOF',
        'claim_commit': '11dcdec8a54b9afd2dd0824507045e21c8e2dd4d',
        'source_main': '4b4edf976b2c7a9ba1dad80636c0e21c66350325',
        'written_formula_blob': 'd684dc1865a3e59e1c699ad1ec28a4dbec0a74e2',
        'method': 'Independent canonical digit realization, ordinary integer n + decimal_reverse(n), exact comparison to separate grade-school coefficient normalization and written closed forms.',
        'limits': 'Only the explicitly listed finite spacers are computed. No all-r theorem, no initial-seed safety assertion, no all-time avoidance, and no result for196 is inferred.',
        'cores': CORES,
        'spacers': SPACERS,
        'groupII_count': len(group),
        'double_gate_count': len(double),
        'primary_integer_additions': len(group) * 4 + len(double) * 8,
        'groupII': group,
        'double_gate': double,
        'boundary_diagnostics': boundary_diagnostics(),
    }
    target = Path(__file__).with_name('groupII_controls.json')
    data = (json.dumps(output, ensure_ascii=False, indent=2) + '\n').encode()
    target.write_bytes(data)
    summary = {
        k: output[k] for k in ('status', 'cores', 'spacers', 'groupII_count', 'double_gate_count',
                               'primary_integer_additions', 'boundary_diagnostics', 'limits')}
    summary['result_file_sha256'] = hashlib.sha256(data).hexdigest()
    summary['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    summary['result_bytes'] = len(data)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
