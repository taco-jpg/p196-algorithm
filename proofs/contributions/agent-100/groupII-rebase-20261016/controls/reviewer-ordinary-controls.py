#!/usr/bin/env python3
"""Independent finite rebase diagnostics using ordinary integer reverse-add.

No author helper, symbolic nextColumns, or carry implementation is imported.
Finite observations are diagnostic evidence, not all-parameter Lean theorems.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys


def decimal_digits(n: int) -> list[int]:
    assert n > 0
    return [int(c) for c in str(n)[::-1]]


def ordinary_step(n: int) -> int:
    assert n > 0
    return n + int(str(n)[::-1])


def pair_word(n: int) -> list[int]:
    d = decimal_digits(n)
    return [a + b for a, b in zip(d, reversed(d))]


def finite_overlap(word: list[int]) -> list[int]:
    return [word[0]] + [word[i] + word[i - 1] for i in range(1, len(word))] + [word[-1]]


def admissible_checks(word: list[int]) -> dict[str, bool]:
    return {
        'positive_width': len(word) > 0,
        'positive_exterior': word[0] > 0,
        'nonnegative_before_any_nat_projection': all(x >= 0 for x in word),
        'coefficient_bound18': all(x <= 18 for x in word),
        'symmetric': word == word[::-1],
        'odd_center_even': len(word) % 2 == 0 or word[len(word) // 2] % 2 == 0,
    }


def realize(word: list[int], choice: int) -> int:
    """Two extreme canonical digit splits; choice1 includes a zero units digit."""
    assert choice in (0, 1) and all(admissible_checks(word).values())
    width = len(word)
    d = [0] * width
    for i in range(width // 2):
        j = width - 1 - i
        leading_min = max(1 if i == 0 else 0, word[i] - 9)
        leading_max = min(9, word[i])
        assert leading_min <= leading_max
        d[j] = leading_min if choice == 0 else leading_max
        d[i] = word[i] - d[j]
    if width % 2:
        d[width // 2] = word[width // 2] // 2
    assert d[-1] > 0 and all(0 <= x <= 9 for x in d)
    n = sum(x * 10**i for i, x in enumerate(d))
    assert decimal_digits(n) == d and pair_word(n) == word
    return n


def trajectory(n: int) -> list[int]:
    one = ordinary_step(n)
    return [n, one, ordinary_step(one)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('Preserve earlier evidence; select a new output filename.')
    spacers = [1, 2, 7]
    exteriors = [5, 6, 7, 8, 9]
    cores = [(u, v) for u in range(5, 9) for v in range(5, 7) if u + v <= 13]
    rows = []
    for r in spacers:
        for p in exteriors:
            for u, v in cores:
                a0 = [p] + [0] * r + [u, v, v, u] + [0] * r + [p]
                q0 = finite_overlap(a0)
                assert len(a0) == 2 * r + 6 and len(q0) == 2 * r + 7
                variants = []
                for choice in (0, 1):
                    a_nums = trajectory(realize(a0, choice))
                    q_nums = trajectory(realize(q0, choice))
                    a_words = [pair_word(n) for n in a_nums]
                    q_words = [pair_word(n) for n in q_nums]
                    assert [len(w) for w in a_words] == [2*r+6, 2*r+6, 2*r+7]
                    assert [len(w) for w in q_words] == [2*r+7, 2*r+7, 2*r+8]
                    a2, q2 = a_words[2], q_words[2]
                    delta = [0] * len(a2)
                    delta[r+1:r+6] = [1, -1, 0, -1, 1]
                    rebased_int = [a + d for a, d in zip(a2, delta)]
                    checks = admissible_checks(rebased_int)
                    assert all(checks.values()), (r, p, u, v, choice, rebased_int, checks)
                    rebased_nat = [max(0, x) for x in rebased_int]
                    assert rebased_nat == rebased_int
                    assert finite_overlap(rebased_nat) == q2
                    actual_defect = [q - a for q, a in zip(q2, finite_overlap(a2))]
                    assert actual_defect == finite_overlap(delta)
                    difference_support = [[i, c-a] for i, (c, a) in enumerate(zip(rebased_nat, a2)) if c != a]
                    assert difference_support == [[r+1, 1], [r+2, -1], [r+4, -1], [r+5, 1]]
                    assert all(0 <= i < len(a2) for i, _ in difference_support)
                    witnesses = [realize(rebased_nat, k) for k in (0, 1)]
                    assert all(m > 0 and pair_word(m) == rebased_nat for m in witnesses)
                    assert all(m != a_nums[2] for m in witnesses)
                    variants.append({
                        'digit_split_choice': choice,
                        'component_numbers_t0_t1_t2': [str(n) for n in a_nums],
                        'whole_numbers_t0_t1_t2': [str(n) for n in q_nums],
                        'component_digits_t0_t1_t2': [decimal_digits(n) for n in a_nums],
                        'whole_digits_t0_t1_t2': [decimal_digits(n) for n in q_nums],
                        'component_pair_words_t0_t1_t2': a_words,
                        'whole_pair_words_t0_t1_t2': q_words,
                        'signed_delta': delta,
                        'rebased_int_before_toNat': rebased_int,
                        'rebased_nat_after_toNat': rebased_nat,
                        'toNat_changed_no_coefficient': rebased_nat == rebased_int,
                        'admissible_checks': checks,
                        'overlap_of_rebased_word': finite_overlap(rebased_nat),
                        'actual_whole_minus_overlap_actual_component': actual_defect,
                        'rebased_minus_actual_component_nonzero_support': difference_support,
                        'rebased_positive_canonical_realizations': [str(n) for n in witnesses],
                        'rebased_realization_digits': [decimal_digits(n) for n in witnesses],
                    })
                assert variants[0]['component_numbers_t0_t1_t2'][0] != variants[1]['component_numbers_t0_t1_t2'][0]
                assert variants[0]['whole_numbers_t0_t1_t2'][0] != variants[1]['whole_numbers_t0_t1_t2'][0]
                assert variants[0]['component_numbers_t0_t1_t2'][1:] == variants[1]['component_numbers_t0_t1_t2'][1:]
                assert variants[0]['whole_numbers_t0_t1_t2'][1:] == variants[1]['whole_numbers_t0_t1_t2'][1:]
                rows.append({'r': r, 'p': p, 'u': u, 'v': v, 'variants': variants})
    summary = {
        'status': 'PASS_FINITE_DIAGNOSTICS_ONLY',
        'case_count': len(rows),
        'initial_realization_choices_per_component_and_whole': 2,
        'ordinary_reverse_additions': len(rows) * 8,
        'r_values': spacers, 'p_values': exteriors, 'cores': cores,
        'r1_cases': sum(x['r'] == 1 for x in rows),
        'p5_cases': sum(x['p'] == 5 for x in rows),
        'p9_cases': sum(x['p'] == 9 for x in rows),
        'observed_min_rebased_coefficient': min(min(v['rebased_int_before_toNat']) for x in rows for v in x['variants']),
        'observed_max_rebased_coefficient': max(max(v['rebased_int_before_toNat']) for x in rows for v in x['variants']),
        'all_rebased_words_differ_from_actual_component_at_valid_columns': True,
        'all_signed_coefficients_nonnegative_before_toNat': True,
        'all_rebased_finite_overlaps_equal_actual_whole_time2': True,
    }
    document = {
        'scope': 'Independent bounded ordinary arithmetic diagnostics for claimed GroupII rebase; not a Lean theorem or a universal inference.',
        'claim_commit': 'e1bc61f552413f4a1ed6cef86c88265d39fd896d',
        'task_blob': 'a277d7843d3509cf60a581ce06fb8d451975bea3',
        'executor': 'Agent #100 scope_audit independent reviewer, no Lean source authorship',
        'implementation': 'Python arbitrary integers, decimal string reverse-add, direct canonical digit splits; no author helper imported.',
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'python_version': sys.version,
        'summary': summary, 'rows': rows,
    }
    args.output.write_text(json.dumps(document, indent=2) + '\n')
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
