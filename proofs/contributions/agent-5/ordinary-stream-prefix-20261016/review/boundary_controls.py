#!/usr/bin/env python3
"""Exact-integer boundary controls for the one-step ordinary raw-prefix claim.

The universal proof is in Lean. These finite checks compare literal word
operations, coordinate recurrences, and ordinary integer reversal separately.
"""

from pathlib import Path
from itertools import product
import hashlib
import json

HERE = Path(__file__).resolve().parent
CONTRIBUTION = HERE.parent
PHASES = [2, 4, 6, 8, 10, 12, 14, 16]


def numeral(word):
    return sum(x * 10**i for i, x in enumerate(word))


def high_value(word):
    return numeral(word[::-1])


def norm(word, carry=0):
    digits = []
    for x in word:
        carry, digit = divmod(x + carry, 10)
        digits.append(digit)
    return digits, carry


def normalized(word):
    digits, carry = norm(word)
    return digits + ([carry] if carry else [])


def paired(word):
    return [x + y for x, y in zip(word, word[::-1])]


def surrounded(B, c, gap, W):
    return B + [c] * (gap + 2) + W + [c] * (gap + 2) + B[::-1]


def streams(B, c, count):
    n = len(B)
    a = 9 * numeral(B) - c * 10**n
    r = 9 * high_value(B) + c
    base = 9 * 10**n
    selector = int(base <= r)
    denominator = base * 10**selector
    low, high = [], []
    for _ in range(count):
        d = (-a) % 10
        assert (a - 9 * d) % 10 == 0
        a = (a - 9 * d) // 10
        low.append(d)
        d, r = divmod(10 * r, denominator)
        high.append(d)
    return low, high, [x + y for x, y in zip(low, high)]


def canonical_digits(n):
    if n == 0:
        return [0]
    digits = []
    while n:
        n, d = divmod(n, 10)
        digits.append(d)
    return digits


def ordinary_integer_step(n):
    return n + int(str(n)[::-1])


def positive_last(word):
    return bool(word) and word[-1] > 0


def decimal_digits(word):
    return all(0 <= x < 10 for x in word)


def realize_symmetric_coefficients(coefficients):
    assert coefficients == coefficients[::-1]
    assert all(0 <= x <= 18 for x in coefficients)
    result = [0] * len(coefficients)
    for i in range((len(coefficients) + 1) // 2):
        j = len(coefficients) - 1 - i
        coefficient = coefficients[i]
        if i == j:
            assert coefficient % 2 == 0
            result[i] = coefficient // 2
        else:
            result[i] = coefficient // 2
            result[j] = coefficient - result[i]
    assert decimal_digits(result)
    assert paired(result) == coefficients
    return result


def trace(D, B, c, gap, W, count=None):
    if count is None:
        count = len(B) + 1
    output = normalized(paired(D))
    low, high, expected = streams(B, c, count)
    value = numeral(D)
    return {'D_low_first': D, 'B': B, 'c': c, 'gap_parameter': gap,
            'actual_band_length': gap + 2, 'W': W,
            'shape_holds': paired(D) == surrounded(B, c, gap, W),
            'input_decimal_digits': decimal_digits(D),
            'input_positive_last': positive_last(D),
            'numeral_D': value, 'literal_reversed_word_numeral': numeral(D[::-1]),
            'ordinary_numeric_step': ordinary_integer_step(value),
            'reverseAddDigits_D': output, 'output_numeral': numeral(output),
            'requested_prefix_length': count,
            'actual_raw_pair_prefix': paired(output)[:count],
            'low_stream': low, 'high_stream': high, 'stream_sum': expected}


def main():
    stats = {'bounded_coefficient_word_cases': 0,
             'canonical_ordinary_realization_cases': 0,
             'zero_head_structural_cases': 0,
             'empty_B_cases': 0, 'empty_W_cases': 0,
             'negative_adic_numerator_cases': 0,
             'long_pattern_cases': 0}
    middle_patterns = [[], [0], [18], [1, 1], [18, 0, 18], [0, 18, 18, 0], [9, 18, 1]]
    for n in range(3):
        for coefficients in product(range(19), repeat=n):
            B = list(coefficients)
            for c in PHASES:
                for gap in [0, 1, 4]:
                    for W in middle_patterns:
                        q = surrounded(B, c, gap, W)
                        output = normalized(q)
                        count = len(B) + 1
                        _, _, expected = streams(B, c, count)
                        assert paired(output)[:count] == expected
                        assert len(paired(output)[:count]) == count
                        stats['bounded_coefficient_word_cases'] += 1
                        stats['zero_head_structural_cases'] += bool(B) and B[0] == 0
                        stats['empty_B_cases'] += not B
                        stats['empty_W_cases'] += not W
                        stats['negative_adic_numerator_cases'] += 9 * numeral(B) - c * 10**n < 0
                        if W == W[::-1] and (not W or len(W) % 2 == 0 or W[len(W)//2] % 2 == 0):
                            D = realize_symmetric_coefficients(q)
                            if positive_last(D):
                                integer_step = ordinary_integer_step(numeral(D))
                                assert output == canonical_digits(integer_step)
                                assert decimal_digits(output) and positive_last(output)
                                assert numeral(output) == numeral(D) + numeral(D[::-1])
                                assert paired(output)[:count] == expected
                                stats['canonical_ordinary_realization_cases'] += 1
                            else:
                                assert B and B[0] == 0
    for n in [7, 40]:
        for c in PHASES:
            for B in [[0]*n, [18]*n, [c]*n, [18 if i % 2 else 0 for i in range(n)]]:
                for W in [[], [18]*30, [0, 18]*15]:
                    for gap in [0, 9]:
                        output = normalized(surrounded(B, c, gap, W))
                        assert paired(output)[:n+1] == streams(B, c, n+1)[2]
                        stats['long_pattern_cases'] += 1

    short_band_D = [1, 9, 1]
    short_band_q = [2, 18, 2]
    assert paired(short_band_D) == short_band_q
    short_band_output = normalized(short_band_q)
    assert short_band_output == [2, 8, 3]
    assert paired(short_band_output)[:1] == [5]
    assert streams([], 2, 1)[2] == [4]
    assert short_band_q != surrounded([], 2, 0, [18])

    leading_zero = trace([0, 1, 1, 1, 1, 0], [0], 2, 0, [])
    assert leading_zero['shape_holds'] and leading_zero['input_decimal_digits']
    assert not leading_zero['input_positive_last']
    assert leading_zero['output_numeral'] == 22220
    assert leading_zero['ordinary_numeric_step'] == 12221
    assert leading_zero['actual_raw_pair_prefix'] == leading_zero['stream_sum']

    nondecimal = trace([10, 6, 6, 2], [], 12, 0, [])
    assert nondecimal['shape_holds'] and nondecimal['input_positive_last']
    assert not nondecimal['input_decimal_digits']
    assert nondecimal['output_numeral'] == 13332
    assert nondecimal['ordinary_numeric_step'] == 3432
    assert nondecimal['actual_raw_pair_prefix'] == nondecimal['stream_sum']

    excess_prefix = trace([1, 1, 9, 1, 1], [], 2, 0, [18], count=2)
    assert excess_prefix['shape_holds'] and excess_prefix['input_decimal_digits'] and excess_prefix['input_positive_last']
    assert excess_prefix['actual_raw_pair_prefix'] == [4, 5]
    assert excess_prefix['stream_sum'] == [4, 4]
    exact_prefix = trace([1, 1, 9, 1, 1], [], 2, 0, [18], count=1)
    assert exact_prefix['actual_raw_pair_prefix'] == exact_prefix['stream_sum'] == [4]

    unbounded_middle = trace([1, 1, 1500, 1, 1], [], 2, 0, [3000])
    assert unbounded_middle['shape_holds']
    assert unbounded_middle['actual_raw_pair_prefix'] == [5]
    assert unbounded_middle['stream_sum'] == [4]

    neutral = trace([4, 4, 5, 5], [], 9, 0, [])
    assert neutral['shape_holds'] and neutral['input_decimal_digits'] and neutral['input_positive_last']
    assert neutral['actual_raw_pair_prefix'] == [18]
    assert neutral['stream_sum'] == [10]

    empty_cases = []
    for c in PHASES:
        D = [c//2]*4
        item = trace(D, [], c, 0, [])
        assert item['shape_holds'] and item['input_positive_last'] and item['input_decimal_digits']
        assert item['actual_raw_pair_prefix'] == item['stream_sum']
        empty_cases.append(item)
    zero_boundaries = []
    for D in [[], [0], [0, 0, 0, 0]]:
        assert decimal_digits(D) and not positive_last(D)
        for c in PHASES:
            assert paired(D) != surrounded([], c, 0, [])
        zero_boundaries.append({'D': D, 'DecimalDigits': True, 'PositiveLast': False,
                                'numeral': numeral(D), 'literal_output': normalized(paired(D))})
    allowed_trailing_zero = trace([0, 1, 1, 2], [], 2, 0, [])
    assert allowed_trailing_zero['shape_holds'] and allowed_trailing_zero['input_decimal_digits']
    assert allowed_trailing_zero['input_positive_last']
    assert allowed_trailing_zero['numeral_D'] == 2110
    assert allowed_trailing_zero['ordinary_numeric_step'] == allowed_trailing_zero['output_numeral'] == 2222
    assert allowed_trailing_zero['actual_raw_pair_prefix'] == allowed_trailing_zero['stream_sum']
    records = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(CONTRIBUTION.glob('*.lean'))}
    assert records['RawPrefixStreams.lean'] == '348bd1acf180a35b4cc60a805d417f7ee07a949fcf91761232f682aa5f5ddee6'
    assert records['OrdinaryStreamStep.lean'] == 'ef186b6f9f631231cbd7fcb7d074f2ad6461783f25bb11672577eb3b29c38177'
    report = {'status': 'PASS_ORDINARY_RAW_PREFIX_BOUNDARY_CONTROLS',
              'reviewer': 'Agent #5 /root/semantic_review',
              'proof_status': 'Finite exact-integer controls; no Lean compiler invoked by this script.',
              'source_sha256': records, 'counts': stats,
              'parameters': {'phases': PHASES, 'exhaustive_B_max_length': 2, 'B_coefficients': [0,18],
                             'gap_parameters': [0,1,4], 'middle_patterns': middle_patterns},
              'short_band_counterexample': {'D': short_band_D, 'integer': 191, 'actual_band_length': 1,
                                           'coefficient_word': short_band_q, 'output_digits': short_band_output,
                                           'actual_prefix': [5], 'invalid_stream_prefix': [4]},
              'positive_last_counterexample': leading_zero,
              'decimal_digits_counterexample': nondecimal,
              'valid_exact_prefix': exact_prefix,
              'invalid_longer_prefix': excess_prefix,
              'middle_bound_counterexample': unbounded_middle,
              'neutral_phase_counterexample': neutral,
              'empty_B_and_W_nonvacuity': empty_cases,
              'allowed_zero_least_significant_digit': allowed_trailing_zero,
              'empty_and_zero_digit_boundaries': zero_boundaries}
    (HERE/'boundary-controls.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': report['status'], 'counts': stats}, indent=2))


if __name__ == '__main__':
    main()
