#!/usr/bin/env python3
"""Finite independent divmod replay of the 620 depth-12 candidate.

Uses Python's unbounded nonnegative integers. No Z3, author discovery module,
or string reversal is imported or called. This is arithmetic evidence, not a
Lean proof. The input JSON is independently recomputed, not trusted.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import resource
import sys
import time


SOURCE_SHA = '372dd79903a67df46f7402f65f9fd7e0bf5b713fecd07e9a8fc2b37f75d83bdd'
INPUT_SHA = '1fef7118361b91ad70b4ed31a2137ee15e384480bd8b3a1ffafbca4553f56acf'
QUERY_SHA = '305cdd7cd21c30680348ce6b416f499af3fc8ffc52600c145dabdefbfd563201'
SEED = 19014942070
TARGET = 62003033030026
STEPS = 12


def require(test: bool, detail: object) -> None:
    if not test:
        raise AssertionError(detail)


def low_digits(n: int) -> list[int]:
    require(type(n) is int and n > 0, ('positive integer required', n))
    result = []
    while n:
        n, digit = divmod(n, 10)
        result.append(digit)
    return result


def reverse_decimal(n: int) -> int:
    require(type(n) is int and n >= 0, ('natural integer required', n))
    result = 0
    while n:
        n, digit = divmod(n, 10)
        result = 10 * result + digit
    return result


def natural_literal(value: object) -> int:
    require(isinstance(value, str) and re.fullmatch(r'[0-9]+', value) is not None,
            ('expected ASCII decimal literal', value))
    return int(value)


def pack_nibbles(digits: list[int]) -> int:
    require(all(0 <= digit <= 9 for digit in digits), 'non-decimal nibble')
    return sum(digit * 16 ** i for i, digit in enumerate(digits))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--contribution', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    contribution = args.contribution.resolve()
    input_path = contribution / 'search/sweep-001/width11/result.json'
    query_path = input_path.parent / 'query.smt2'
    model_path = input_path.parent / 'model.txt'
    source_path = contribution / 'search_bounded.py'
    payloads = {path: path.read_bytes() for path in [input_path, query_path, model_path, source_path]}
    require(hashlib.sha256(payloads[source_path]).hexdigest() == SOURCE_SHA, 'discovery source changed')
    require(hashlib.sha256(payloads[input_path]).hexdigest() == INPUT_SHA, 'candidate report changed')
    require(hashlib.sha256(payloads[query_path]).hexdigest() == QUERY_SHA, 'query changed')
    author = json.loads(payloads[input_path])
    require((author['width'], author['steps'], author['prefix']) == (11, STEPS, '620'), 'candidate domain')
    require(author['source_sha256'] == SOURCE_SHA and author['query_sha256'] == QUERY_SHA, 'author metadata linkage')
    advertised = [natural_literal(value) for value in author['orbit']]
    require(len(advertised) == STEPS + 1, 'orbit count')

    values = [SEED]
    for _ in range(STEPS):
        values.append(values[-1] + reverse_decimal(values[-1]))
    require(values == advertised, ('independent orbit mismatch', values, advertised))
    widths = [len(low_digits(value)) for value in values]
    require(widths == author['canonical_widths'], ('canonical width mismatch', widths))
    initial_width = widths[0]
    steps = []
    max_column_sum = 0
    for t in range(STEPS):
        n, successor = values[t], values[t + 1]
        rev = reverse_decimal(n)
        actual_digits = low_digits(n)
        width = len(actual_digits)
        capacity = initial_width + t
        require(1 <= initial_width <= width <= capacity < 64, ('width capacity', t))
        source_digits = actual_digits + [0] * (capacity - width)
        next_digits = low_digits(successor) + [0] * (capacity + 1 - widths[t + 1])
        require(len(next_digits) == capacity + 1, ('next capacity', t))
        full_reverse = sum(source_digits[i] * 16 ** (capacity - 1 - i) for i in range(capacity))
        reversal_shift_bits = 4 * (capacity - width)
        encoded_reverse = full_reverse >> reversal_shift_bits
        require(encoded_reverse == pack_nibbles(low_digits(rev)), ('padded reversal mismatch', t))
        carry = 0
        carries = [0]
        column_sums = []
        for i in range(capacity):
            rev_digit = (encoded_reverse >> (4 * i)) & 15
            require(0 <= rev_digit <= 9, ('reverse nibble domain', t, i))
            lhs = source_digits[i] + rev_digit + carry
            outgoing, output_digit = divmod(lhs, 10)
            require(0 <= outgoing <= 1 and 0 <= lhs <= 19, ('carry or five-bit range', t, i))
            rhs = next_digits[i] + 10 * outgoing
            require(lhs == rhs and output_digit == next_digits[i], ('decimal column', t, i))
            require(lhs < 32 and rhs < 32, ('five-bit wrap', t, i))
            carry = outgoing
            carries.append(carry)
            column_sums.append(lhs)
        require(next_digits[capacity] == carry, ('capacity terminal carry', t))
        require(widths[t + 1] in (width, width + 1), ('width change', t))
        require(carries[width] == widths[t + 1] - width, ('actual width overflow carry', t))
        trailing_zeros = next(i for i, digit in enumerate(actual_digits) if digit != 0)
        max_column_sum = max(max_column_sum, *column_sums)
        steps.append({
            'source_time': t, 'source': str(n), 'reverse_divmod': str(rev),
            'successor': str(successor), 'source_width': width,
            'reverse_canonical_width': len(low_digits(rev)),
            'successor_width': widths[t + 1], 'source_trailing_zeros': trailing_zeros,
            'overflow_at_actual_width': bool(carries[width]),
            'allocated_capacity': capacity, 'reversal_shift_bits': reversal_shift_bits,
            'column_sums': column_sums, 'carries': carries,
        })
    target = values[-1]
    require(values[0] > 0 and target == TARGET, 'literal endpoints')
    require(reverse_decimal(target) == target, 'target palindrome')
    require(widths[-1] >= 3, 'target width')
    leading_three, suffix = divmod(target, 10 ** (widths[-1] - 3))
    require(leading_three == 620, 'target high-end prefix')
    for path, data in payloads.items():
        require(path.read_bytes() == data, ('input changed during replay', str(path)))
    result = {
        'schema_version': 1,
        'status': 'PASS_INDEPENDENT_FINITE_INTEGER_REPLAY_ONLY',
        'evidence_level': 'Unbounded ordinary integer recomputation, no solver trust; not Lean acceptance or an optimality proof.',
        'reviewer': '/root/strategy_review',
        'executed_at_utc': datetime.now(timezone.utc).isoformat(),
        'argv': sys.argv,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'seed': str(SEED), 'target': str(TARGET), 'steps': STEPS,
        'orbit': [str(value) for value in values], 'canonical_widths': widths,
        'target_palindrome_divmod': True, 'target_leading_three_divmod': leading_three,
        'target_suffix_after_three_digits': str(suffix),
        'positive_seed': True, 'all_12_step_equalities': True,
        'padded_nibble_reversal_matches_integer_reversal_at_all_source_times': True,
        'all_full_capacity_decimal_column_equations': True,
        'all_columns_no_five_bit_wrap': True,
        'maximum_actual_column_sum': max_column_sum,
        'trailing_zero_source_times': [step['source_time'] for step in steps if step['source_trailing_zeros']],
        'overflow_source_times': [step['source_time'] for step in steps if step['overflow_at_actual_width']],
        'palindromic_times_in_this_13_value_trace': [t for t, value in enumerate(values) if reverse_decimal(value) == value],
        'integer_overflow_prevention': 'Python integers have arbitrary precision; no fixed-width arithmetic is used for decimal values.',
        'bounded_interval_search': 'NOT_STARTED; parent cancelled after discovery of this candidate.',
        'step_details': steps,
        'inputs': {str(path.relative_to(contribution)): {
            'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)} for path, data in payloads.items()},
        'elapsed_seconds': time.monotonic() - started,
        'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in [
        'status', 'seed', 'target', 'steps', 'canonical_widths',
        'trailing_zero_source_times', 'overflow_source_times',
        'maximum_actual_column_sum', 'elapsed_seconds', 'max_rss_kib']}, indent=2))


if __name__ == '__main__':
    main()
