#!/usr/bin/env python3
"""Independent exact-integer controls for the proposed finite digit formula.

This script is regression evidence, not a universal theorem or a Lean build.
Its reference exterior update transcribes P196.Agent7.Finite.outerNext.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
CONTRIBUTION = HERE.parent
REPO = CONTRIBUTION.parents[3]
PHASES = [2, 4, 6, 8, 10, 12, 14, 16]
TAIL_LENGTHS = [0, 1, 4]


def normalize(word, carry):
    digits = []
    for coefficient in word:
        carry, digit = divmod(coefficient + carry, 10)
        digits.append(digit)
    return digits, carry


def strip(phase, word):
    end = len(word)
    while end and word[end - 1] == phase:
        end -= 1
    return word[:end]


def outer_next(phase, word):
    bulk_carry = int(phase >= 10)
    band = max(phase - 9 * bulk_carry, 0)
    low, low_carry = normalize(word, 0)
    high, overflow = normalize(list(reversed(word)), bulk_carry)
    boundary = max(phase + low_carry - 10 * bulk_carry, 0)
    opposite = list(reversed(high)) + [band] if overflow == 0 else [1] + list(reversed(high))
    raw = [x + y for x, y in zip(low + [boundary], opposite)]
    return {'c': 2 * band, 'B': strip(2 * band, raw)}


def low_value(word):
    return sum(coefficient * 10**index for index, coefficient in enumerate(word))


def high_value(word):
    result = 0
    for coefficient in word:
        result = 10 * result + coefficient
    return result


def adic_digits(count, numerator):
    result = []
    for _ in range(count):
        digit = (-numerator) % 10
        assert 0 <= digit < 10
        assert (numerator - 9 * digit) % 10 == 0
        result.append(digit)
        numerator = (numerator - 9 * digit) // 10
    return result


def fraction_digits(count, numerator, denominator):
    assert denominator > 0
    result = []
    for _ in range(count):
        digit, numerator = divmod(10 * numerator, denominator)
        result.append(digit)
    return result


def coordinates(phase, word):
    length = len(word)
    bulk_carry = int(phase >= 10)
    _, overflow = normalize(list(reversed(word)), bulk_carry)
    return {
        'a': 9 * low_value(word) - phase * 10**length,
        'r': 9 * high_value(word) + phase,
        'D': 9 * 10**length,
        'g': overflow,
        't': max(phase - 9 * bulk_carry, 0),
    }


def stream_successor(phase, word, count):
    coord = coordinates(phase, word)
    low = adic_digits(count, coord['a'])
    high = fraction_digits(count, coord['r'], coord['D'] * 10**coord['g'])
    summed = [x + y for x, y in zip(low, high)]
    return {'c': 2 * coord['t'], 'B': strip(2 * coord['t'], summed)}


def inspect_state(phase, word):
    coord = coordinates(phase, word)
    low_scan, low_carry = normalize(word, 0)
    high_scan, overflow = normalize(list(reversed(word)), int(phase >= 10))
    assert overflow in (0, 1)
    assert coord['r'] // coord['D'] == overflow
    assert 0 < coord['r'] < 2 * coord['D']
    scaled_denominator = coord['D'] * 10**overflow
    assert 0 < coord['r'] < scaled_denominator
    assert 1 <= coord['t'] <= 8
    boundary = phase + low_carry - 10 * int(phase >= 10)
    assert 0 <= boundary < 10
    opposite = list(reversed(high_scan)) + [coord['t']] if overflow == 0 else [1] + list(reversed(high_scan))
    reference = outer_next(phase, word)
    for tail in TAIL_LENGTHS:
        count = len(word) + 1 + tail
        low = adic_digits(count, coord['a'])
        high = fraction_digits(count, coord['r'], scaled_denominator)
        assert low == low_scan + [boundary] + [coord['t']] * tail
        assert high == opposite + [coord['t']] * tail
        assert all(0 <= digit < 10 for digit in low + high)
        assert (coord['a'] - 9 * low_value(low)) % 10**count == 0
        assert stream_successor(phase, word, count) == reference
    return coord


stats = {
    'exhaustive_states': 0,
    'negative_adic_numerator_states': 0,
    'empty_word_states': 0,
    'overflow_states': 0,
    'zero_head_states': 0,
    'untrimmed_states': 0,
    'long_pattern_states': 0,
    'generic_normalize_instances': 0,
}

for length in range(4):
    for coefficients in product(range(19), repeat=length):
        word = list(coefficients)
        for phase in PHASES:
            coord = inspect_state(phase, word)
            stats['exhaustive_states'] += 1
            stats['negative_adic_numerator_states'] += int(coord['a'] < 0)
            stats['empty_word_states'] += int(not word)
            stats['overflow_states'] += coord['g']
            stats['zero_head_states'] += int(bool(word) and word[0] == 0)
            stats['untrimmed_states'] += int(bool(word) and word[-1] == phase)

for length in [7, 40]:
    for phase in PHASES:
        patterns = [
            [0] * length, [18] * length, [phase] * length,
            [18 if index % 2 else 0 for index in range(length)],
            [0 if index % 2 else 18 for index in range(length)],
        ]
        for word in patterns:
            inspect_state(phase, word)
            stats['long_pattern_states'] += 1

# The intermediate adic normalization statement has no coefficient or phase
# bound and accepts arbitrary signed phase numerators and natural carries.
for length in range(3):
    for coefficients in product([0, 9, 10, 18, 19, 35, 99], repeat=length):
        word = list(coefficients)
        for carry in [0, 1, 5, 99]:
            digits, final_carry = normalize(word, carry)
            for phase_numerator in [-25, -1, 0, 1, 9, 10, 25]:
                initial = 9 * (low_value(word) + carry) - phase_numerator * 10**length
                for tail in TAIL_LENGTHS:
                    assert adic_digits(length + tail, initial) == digits + adic_digits(tail, 9 * final_carry - phase_numerator)
                    stats['generic_normalize_instances'] += 1


def trace(phase, word, count=7):
    coord = coordinates(phase, word)
    scaled_denominator = coord['D'] * 10**coord['g']
    return {
        'state': {'c': phase, 'B': word},
        'coordinates': coord,
        'rho': str(Fraction(coord['r'], coord['D'])),
        'normalized_rho': str(Fraction(coord['r'], scaled_denominator)),
        'low_stream': adic_digits(count, coord['a']),
        'high_stream': fraction_digits(count, coord['r'], scaled_denominator),
        'exact_successor': outer_next(phase, word),
        'stream_successor': stream_successor(phase, word, count),
    }


empty_high = trace(12, [])
wrong_unscaled_high = fraction_digits(4, empty_high['coordinates']['r'], empty_high['coordinates']['D'])
assert wrong_unscaled_high[0] == 13
short_cutoff_state = {'c': 2, 'B': [10]}
short_cutoff = stream_successor(2, [10], 1)
assert short_cutoff != outer_next(2, [10])
neutral = trace(9, [0], 6)
assert neutral['stream_successor'] != neutral['exact_successor']
unbounded = trace(10, [19], 6)
assert unbounded['coordinates']['g'] == 2
assert unbounded['stream_successor'] != unbounded['exact_successor']
unequal_left = strip(2, [x + y for x, y in zip([0] + [1], [] + [1])])
unequal_right = strip(2, [x + y for x, y in zip([0], [])])
assert unequal_left != unequal_right

module_records = []
for path in sorted(CONTRIBUTION.glob('*.lean')):
    data = path.read_bytes()
    module_records.append({'path': str(path.relative_to(REPO)), 'sha256': sha256(data).hexdigest()})

report = {
    'status': 'PASS_EXACT_FINITE_CONTROLS',
    'proof_status': 'Finite regression evidence only; no Lean compiler was invoked by this review script.',
    'reviewer': 'Agent #5 independent semantic reviewer',
    'claimed_scope': 'Explicit finite coordinate digit streams and cutoff-tail assembly; no new orbit-level conclusion.',
    'parameters': {'phases': PHASES, 'coefficient_range': [0, 18], 'exhaustive_max_width': 3, 'tail_lengths': TAIL_LENGTHS, 'long_pattern_widths': [7, 40]},
    'counts': stats,
    'complete_stream_prefix_checks': (stats['exhaustive_states'] + stats['long_pattern_states']) * len(TAIL_LENGTHS),
    'source_snapshots_at_control_completion': module_records,
    'boundary_traces': [trace(c, []) for c in PHASES] + [trace(2, [0]), trace(2, [10]), trace(2, [18]), trace(16, [0, 0, 0])],
    'rejected_variant_controls': {
        'unscaled_high_rho': {'state': empty_high['state'], 'wrong_high_stream': wrong_unscaled_high, 'correct_high_stream': empty_high['high_stream'][:4]},
        'cutoff_at_word_length_only': {'state': short_cutoff_state, 'insufficient_prefix_successor': short_cutoff, 'exact_successor': outer_next(2, [10])},
        'neutral_phase': neutral,
        'coefficient_bound_dropped': unbounded,
        'unequal_zip_base_lengths': {'a': [0], 'b': [], 't': 1, 'q': 1, 'left': unequal_left, 'right': unequal_right},
        'real_tail_digit_nine': {'actual_fraction_digits': fraction_digits(3, 9, 9), 'invalid_claimed_repeat': [9, 9, 9]},
    },
}
(HERE / 'boundary-controls.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'status': report['status'], 'counts': stats, 'complete_stream_prefix_checks': report['complete_stream_prefix_checks']}, indent=2))
