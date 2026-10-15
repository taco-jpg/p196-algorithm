#!/usr/bin/env python3
"""Bounded adversarial diagnostics; NOT a Lean/kernel proof.

Independent side: integer remainder arithmetic, canonical numeral construction,
and two actual even-length completions of every abstract prefix. Never call the
subject's normalize/F/forward methods when constructing expected edges.
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import resource
import time

resource.setrlimit(resource.RLIMIT_CPU, (100, 110))
resource.setrlimit(resource.RLIMIT_AS, (700 * 1024**2, 700 * 1024**2))
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = ROOT / 'proofs/contributions/2026-10-15-seven-column-prefix'


def decimal_digits(n):
    assert n >= 0
    if n == 0:
        return (0,)
    result = []
    while n:
        result.append(n % 10)
        n //= 10
    return tuple(result)


def from_digits(ds):
    out = 0
    for d in reversed(ds):
        assert 0 <= d <= 9
        out = 10 * out + d
    return out


def reverse_integer(n):
    r = 0
    while n:
        r = 10 * r + n % 10
        n //= 10
    return r


def step(n):
    return n + reverse_integer(n)


def raw(n):
    ds = decimal_digits(n)
    return tuple(ds[i] + ds[-1-i] for i in range(len(ds)))


def realize(s):
    """One canonical positive integer with exactly this symmetric raw word."""
    assert s and s[0] > 0 and s == s[::-1]
    assert all(0 <= x <= 18 for x in s)
    ds = [0] * len(s)
    for i in range(len(s)//2):
        ds[-1-i] = min(s[i], 9)
        ds[i] = s[i] - ds[-1-i]
    if len(s) % 2:
        assert s[len(s)//2] % 2 == 0
        ds[len(s)//2] = s[len(s)//2]//2
    n = from_digits(ds)
    assert n > 0 and len(decimal_digits(n)) == len(s) and raw(n) == s
    return n


def actual_prefix_outputs(s):
    # Center 00 resets the carry to 0; center 99+99 forces it to 1.
    # Both are genuine even-length canonical integer realizations.
    return {raw(step(realize(s + (middle, middle) + s[::-1])))[:len(s)]
            for middle in (0, 18)}


def words(n):
    # Generate by independent outer half and central digit, rather than using
    # the subject's generator. The n=1 positive/canonical case is explicit.
    if n == 1:
        for center_digit in range(1, 10):
            yield (2 * center_digit,)
        return
    for half in itertools.product(range(19), repeat=n//2):
        if half[0] == 0:
            continue
        centers = [(2*d,) for d in range(10)] if n % 2 else [()]
        for center in centers:
            yield half + center + half[::-1]


def subject_module():
    spec = importlib.util.spec_from_file_location('subject_verifier', SOURCE/'verify_certificates.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    started = time.monotonic()
    subject = subject_module()
    counts = {}

    # Exhaust ALL legal prefixes/targets for widths 1..3, comparing inverse
    # sets against edges of actual integer completions (not carry equations).
    exhaustive = []
    for width in range(1, 4):
        expected = {}
        source_count = 0
        for s in itertools.product(range(19), repeat=width):
            if s[0] == 0:
                continue
            source_count += 1
            for p in actual_prefix_outputs(s):
                expected.setdefault(p, set()).add(s)
        target_count = 0
        for p in itertools.product(range(19), repeat=width):
            if p[0] == 0:
                continue
            target_count += 1
            got = subject.prefix_predecessors(p)
            assert got == expected.get(p, set()), ('inverse mismatch', width, p, got, expected.get(p))
        exhaustive.append({'width': width, 'sources': source_count,
                           'legal_targets': target_count,
                           'edges': sum(map(len, expected.values()))})
    counts['exhaustive_small_width_inverse_equivalence'] = exhaustive

    # Deliberately probe the excluded zero-leading domain.
    zero_target = (0,)
    invalid_extra = subject.prefix_predecessors(zero_target)
    assert (9,) in invalid_extra and zero_target not in actual_prefix_outputs((9,))
    counts['excluded_domain_counterexample'] = {
        'target': zero_target, 'inverse_returns': sorted(invalid_extra),
        'actual_outputs_of_source_9': sorted(actual_prefix_outputs((9,))),
        'meaning': 'Equivalence requires target[0] > 0; all certificate nodes satisfy it.'}

    # Seven-column completeness controls biased towards carry threshold 9.
    seven_sources = 0
    seven_edges = 0
    for first in (1, 9, 10, 18):
        for tail in itertools.product((0, 9, 18), repeat=6):
            s = (first,) + tail
            seven_sources += 1
            expected = actual_prefix_outputs(s)
            assert expected == subject.forward_prefixes(s), ('forward mismatch', s)
            for p in expected:
                assert s in subject.prefix_predecessors(p), ('omitted inverse edge', s, p)
                seven_edges += 1
    counts['seven_threshold_sources'] = seven_sources
    counts['seven_threshold_edges'] = seven_edges

    short = {}; boundary = []
    for width in range(1, 7):
        total = growth = 0
        for s in words(width):
            n = realize(s)
            actual = raw(step(n))
            assert actual == subject.F(s), ('short normalization mismatch', s, n, actual)
            assert len(actual) in (width, width+1)
            assert len(decimal_digits(step(n))) >= len(decimal_digits(n))
            if len(actual) > width:
                growth += 1
                if width == 6 and len(boundary) < 8:
                    boundary.append({'raw_source': s, 'integer': n, 'next_integer': step(n), 'raw_target': actual})
            total += 1
        short[str(width)] = {'total': total, 'grew_by_one': growth}
    assert sum(v['total'] for v in short.values()) == 10467
    counts['short_all_realizable_words'] = short
    counts['six_to_seven_examples'] = boundary

    # Cross-check last-step assertion over independent positive integers.
    last_step = {'range': [1, 50000], 'palindromic_outputs': 0, 'no_growth_cases': 0,
                 'leading_digit_over_1_cases': 0}
    for n in range(1, 50001):
        p = step(n)
        assert p > n
        if p != reverse_integer(p):
            continue
        last_step['palindromic_outputs'] += 1
        ds = decimal_digits(p)
        if len(ds) == len(decimal_digits(n)):
            assert raw(n) == ds, ('no-growth palindrome lemma violated', n, p)
            last_step['no_growth_cases'] += 1
        if ds[-1] > 1:
            assert raw(n) == ds
            last_step['leading_digit_over_1_cases'] += 1
    counts['last_step_integer_controls'] = last_step
    counts['missing_hypotheses_witnesses'] = {
        'allow_zero_breaks_strict_growth': {'n': 0, 'Tn': step(0)},
        'drop_no_growth_breaks_raw_equals_target': {'n': 29, 'Tn': step(29), 'raw_n': raw(29), 'target_digits': decimal_digits(step(29))},
        'allow_noncanonical_zero_high_digit_breaks_quotient_semantics': {
            'noncanonical_low_first_digits': [1,0], 'value': 1,
            'padded_reverse_sum': 11, 'actual_integer_reverse_sum': step(1)},
        'odd_center_73937': {'palindrome': 73937, 'center': 9,
                            'fails_realizable_raw_center_even_condition': True}}

    cert = json.loads((SOURCE/'certificate_739.json').read_text())
    rank = {tuple(row['word']): row['rank'] for row in cert['nodes']}
    # Only selected targets, to avoid repeating the authors' full certificate run.
    selected = set(tuple(p) for p in cert['initial'] if rank[tuple(p)] == 38)
    selected.update(sorted(rank)[::293])
    selected.update(p for p in rank if p[:3] == (1,9,6))
    selected.update(p for p in rank if len(p) < 7)
    sampled_edges = 0
    for p in sorted(selected):
        if len(p) != 7:
            continue
        for s in subject.prefix_predecessors(p):
            assert p in actual_prefix_outputs(s), ('unsound inverse edge', s, p)
            assert s in rank and rank[s] < rank[p], ('sampled certificate rank failure', s, p)
            sampled_edges += 1
    counts['sampled_certificate'] = {'targets_selected': len(selected), 'long_edges_checked': sampled_edges,
        'complete_certificate_rechecked': False}

    orbit = [196]
    for _ in range(39):
        orbit.append(step(orbit[-1]))
    assert all(n > 0 and n != reverse_integer(n) for n in orbit)
    assert orbit[39] == 7197630720180367016
    counts['orbit_196_through_39'] = orbit
    manifest = {}
    for path in [SOURCE/'P196_739_Proof.md', SOURCE/'verify_certificates.py', SOURCE/'certificate_739.json', Path(__file__)]:
        manifest[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    result = {'status': 'PASS_DIAGNOSTIC_ONLY', 'role': 'independent adversarial reviewer',
              'elapsed_seconds': round(time.monotonic()-started, 3),
              'limits': {'cpu_seconds_soft': 100, 'address_space_bytes': 700*1024**2},
              'source_sha256': manifest, 'checks': counts,
              'acceptance': 'No Lean claim: bounded Python probes do not establish unbounded projection or full certificate acceptance.'}
    (HERE/'probe-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'elapsed_seconds': result['elapsed_seconds'],
                      'exhaustive': exhaustive, 'seven_sources': seven_sources,
                      'short_words': 10467, 'sampled_targets': len(selected), 'sampled_edges': sampled_edges,
                      'result': str(HERE/'probe-results.json')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
