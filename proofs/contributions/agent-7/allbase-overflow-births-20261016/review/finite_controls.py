#!/usr/bin/env python3
"""Finite discovery controls; these computations are not a universal proof."""
import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import sys

PACKAGE = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(b, a, z, u, v):
    zero = [
        a == 0 and z == 0,
        a == b - 1 and z == b - 1 and u == 1 and v == 1,
        a == b - 1 and z == b and u == 0,
        a == b and z == b - 1 and v == 0,
    ]
    maximum = [
        a == 2 * b - 2 and z == 2 * b - 2,
        a == b - 1 and z == b - 1 and u == 0 and v == 0,
        a == b - 1 and z == b - 2 and u == 1,
        a == b - 2 and z == b - 1 and v == 1,
    ]
    return zero, maximum


def scan(b, coefficients):
    carries, digits = [0], []
    for q in coefficients:
        digits.append((q + carries[-1]) % b)
        carries.append((q + carries[-1]) // b)
    actual = digits + ([carries[-1]] if carries[-1] else [])
    return carries, actual


def placed_with_resets(b, coefficients, resets):
    carry, digits = 0, []
    for q, reset in zip(coefficients, resets):
        active = 0 if reset else carry
        digits.append((q + active) % b + (carry if reset else 0))
        carry = (q + active) // b
    return digits + [carry]


def pairs(digits):
    return [x + y for x, y in zip(digits, reversed(digits))]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    report = {
        'reviewer': 'Agent #7 /root/runtime',
        'kind': 'finite discovery controls; no inference of universal validity',
        'started_at': datetime.now(timezone.utc).isoformat(),
        'status': 'RUNNING',
        'python_version': sys.version,
        'script_sha256': sha(Path(__file__)),
        'semantic_correspondence': [
            'Python // and % on the tested nonnegative integers and positive bases agree with Int Euclidean division and remainder.',
            'scan is an independent diagnostic transcription of original ordinaryTags, terminal and body, with initial carry zero and final zero omitted.',
            'No tagged reset carry is substituted for the actual ordinary carry.',
            'The symmetric coefficient-word sweep is broader than actual input digit-pair encodings; canonical input controls are identified separately.',
        ],
        'source_sha256': {},
    }
    for source in sorted((PACKAGE / 'dependencies').glob('*.lean')):
        report['source_sha256']['dependencies/' + source.name] = sha(source)
    for name in ('AdjacentBirths.lean', 'OverflowDigits.lean'):
        report['source_sha256'][name] = sha(PACKAGE / name)
    try:
        local = []
        for b in [*range(2, 41), 64, 97]:
            summary = {'base': b, 'tuples': 0, 'zero_row_hits': [0] * 4,
                       'maximum_row_hits': [0] * 4, 'new_extreme_tuples': 0}
            for a, z, l, h in itertools.product(range(2 * b - 1), range(2 * b - 1), (0, 1), (0, 1)):
                u, v = (a + l) // b, (z + h) // b
                Q = (z + u) % b + (a + v) % b
                zero, maximum = rows(b, a, z, u, v)
                assert u in (0, 1) and v in (0, 1)
                assert (Q == 0) == any(zero), (b, a, z, l, h, 'zero')
                assert (Q == 2 * b - 2) == any(maximum), (b, a, z, l, h, 'maximum')
                assert sum(zero) <= 1 and sum(maximum) <= 1
                is_new = (Q == 0 and not (a == 0 and z == 0)) or (Q == 2 * b - 2 and not (a == 2 * b - 2 and z == 2 * b - 2))
                if is_new:
                    assert a == b - 1 or z == b - 1
                    summary['new_extreme_tuples'] += 1
                summary['tuples'] += 1
                for row in range(4):
                    summary['zero_row_hits'][row] += int(zero[row])
                    summary['maximum_row_hits'][row] += int(maximum[row])
            assert summary['zero_row_hits'] == [4, 1, 2, 2]
            assert summary['maximum_row_hits'] == [4, 1, 2, 2]
            local.append(summary)
        report['local_sweep'] = {'bases': [s['base'] for s in local],
                                 'tuples': sum(s['tuples'] for s in local),
                                 'results': local}

        whole = []
        wrong_mirror_witness = None
        endpoint_max_witness = None
        for b in range(2, 8):
            summary = {'base': b, 'coefficient_words': 0, 'overflow_words': 0,
                       'interior_positions': 0, 'endpoint_maximum_words': 0,
                       'zero_row_hits': [0] * 4, 'maximum_row_hits': [0] * 4}
            for L in range(1, 7):
                for half in itertools.product(range(2 * b - 1), repeat=(L + 1) // 2):
                    q = list(half) + list(reversed(half[:L // 2]))
                    assert len(q) == L and q == q[::-1]
                    summary['coefficient_words'] += 1
                    c, digits = scan(b, q)
                    assert all(x in (0, 1) for x in c)
                    if c[-1] != 1:
                        continue
                    summary['overflow_words'] += 1
                    assert len(digits) == L + 1 and digits[-1] == 1
                    Q = pairs(digits)
                    endpoint = 1 + q[0] % b
                    assert Q[0] == Q[L] == endpoint and endpoint != 0
                    assert (endpoint == 2 * b - 2) == (b == 2 and q[0] == 1)
                    if endpoint == 2 * b - 2:
                        summary['endpoint_maximum_words'] += 1
                        if endpoint_max_witness is None:
                            endpoint_max_witness = {'base': b, 'coefficients': q, 'carries': c, 'actual_digits': digits, 'pairs': Q}
                    for i in range(1, L):
                        a, z, u, v = q[i - 1], q[i], c[i], c[L - i]
                        assert u == (a + c[i - 1]) // b
                        assert v == (z + c[L - i - 1]) // b
                        assert Q[i] == (z + u) % b + (a + v) % b
                        zero, maximum = rows(b, a, z, u, v)
                        assert (Q[i] == 0) == any(zero)
                        assert (Q[i] == 2 * b - 2) == any(maximum)
                        assert sum(zero) <= 1 and sum(maximum) <= 1
                        if ((Q[i] == 0 and not (a == 0 and z == 0)) or
                            (Q[i] == 2 * b - 2 and not (a == 2 * b - 2 and z == 2 * b - 2))):
                            assert a == b - 1 or z == b - 1
                        wrong = (z + u) % b + (z + c[L - 1 - i]) % b
                        if wrong != Q[i] and wrong_mirror_witness is None:
                            wrong_mirror_witness = {'base': b, 'coefficients': q, 'actual_digits': digits,
                                                    'pairs': Q, 'index': i, 'actual_mirror_index': L - i,
                                                    'wrong_old_width_mirror_index': L - 1 - i,
                                                    'actual_pair': Q[i], 'wrong_pair': wrong}
                        summary['interior_positions'] += 1
                        for row in range(4):
                            summary['zero_row_hits'][row] += int(zero[row])
                            summary['maximum_row_hits'][row] += int(maximum[row])
            whole.append(summary)
        assert wrong_mirror_witness is not None and endpoint_max_witness is not None
        report['symmetric_coefficient_word_sweep'] = {
            'bases': list(range(2, 8)), 'old_widths': list(range(1, 7)),
            'coefficient_words': sum(s['coefficient_words'] for s in whole),
            'overflow_words': sum(s['overflow_words'] for s in whole),
            'interior_positions': sum(s['interior_positions'] for s in whole),
            'results': whole,
        }

        b, a, z, u, v = 2, 0, 2, 0, 0
        assert (z + u) % b + (a + v) % b == 0
        assert not any(rows(b, a, z, u, v)[0])
        assert all((z + h) // b != v for h in (0, 1))
        controls = {
            'uncoupled_carries_negative_control': {
                'base': b, 'a': a, 'z': z, 'u': u, 'v': v,
                'zero_residue_pair': True, 'matches_any_zero_row': False,
                'violates_v_equation_for_both_exterior_carries': True,
                'interpretation': 'The classifier requires actual coupled carries; arbitrary guessed carry bits would falsify completeness.',
            },
            'old_width_mirror_negative_control': wrong_mirror_witness,
            'binary_endpoint_maximum_witness': endpoint_max_witness,
        }
        digits_in = [0, 1, 1]
        q = pairs(digits_in)
        c, ds = scan(2, q)
        assert q == [1, 2, 1] and ds == [1, 0, 0, 1] and pairs(ds) == [2, 0, 0, 2]
        controls['existing_binary_110_control'] = {
            'base': 2, 'least_significant_first_input': digits_in,
            'coefficients': q, 'carries': c, 'actual_digits': ds, 'next_pairs': pairs(ds),
            'interpretation': 'Existing binary 110 example, a diagnostic control and not a novelty claim.',
        }
        q = pairs([2, 1, 2])
        c, ds = scan(3, q)
        reset_ds = placed_with_resets(3, q, [False, True, False])
        assert q == [4, 2, 4] and ds == [1, 0, 2, 1] and reset_ds == [1, 3, 1, 1]
        controls['tag_erasure_control'] = {
            'base': 3, 'canonical_input': [2, 1, 2], 'coefficients': q,
            'tags': [False, True, False], 'actual_digits': ds, 'reset_placed': reset_ds,
            'interpretation': 'Actual digits erase tags; reset-placed output is a different list and even contains a non-digit.',
        }
        width_one = []
        for b in range(2, 8):
            c, ds = scan(b, [2 * b - 2])
            assert ds == [b - 2, 1] and pairs(ds) == [b - 1, b - 1]
            width_one.append({'base': b, 'canonical_input': [b - 1],
                              'coefficients': [2 * b - 2], 'actual_digits': ds, 'pairs': pairs(ds)})
        controls['canonical_width_one_controls'] = width_one
        report['controls'] = controls
        for name, digest in report['source_sha256'].items():
            assert sha(PACKAGE / name) == digest
        report['status'] = 'PASS'
    except Exception as exc:
        report['status'] = 'FAIL'
        report['error'] = repr(exc)
        raise
    finally:
        report['finished_at'] = datetime.now(timezone.utc).isoformat()
        (output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({key: report.get(key) for key in ('status', 'error')}, sort_keys=True))


if __name__ == '__main__':
    main()
