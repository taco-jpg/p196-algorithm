#!/usr/bin/env python3
"""Independent controls for the neutral exterior moment filter.

    python3 -O calculation/agent-107/test_exterior_charge.py

Counts use meet-in-the-middle enumeration of *integer* alternating moments,
not the implementation's residue dynamic program. Transition checks normalize
whole integers with fixed width. Known cycles are read by a separate fixture
parser and retimed to include concentrated, nonbinary exterior trim counts.
"""

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
import importlib.util
import itertools
from pathlib import Path
import unittest

import exterior_charge as target


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ExteriorFixture:
    B: tuple[int, ...]
    u: int


def fixture_cycles():
    """Use main's existing fixture parser, independent of exterior_charge's parser.

    No arithmetic helper from the mirror is used by this test suite.
    """
    path = ROOT / "calculation/neutral_band_search.py"
    spec = importlib.util.spec_from_file_location("a107_fixture_mirror", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("existing fixture loader unavailable")
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    fixtures = {base: tuple(ExteriorFixture(tuple(row[0]), row[4]) for row in rows)
                for base, rows in mirror._lean_certs()}
    if set(fixtures) != {2, 4, 8, 11, 16, 17, 26, 32}:
        raise ValueError("expected eight main-branch certificate fixtures")
    return fixtures


def integer_moment(word):
    return sum(coefficient if i % 2 == 0 else -coefficient
               for i, coefficient in enumerate(word)) - (-1) ** len(word)


def integer_digits(base, word, entry):
    value = entry + sum(coefficient * base ** i for i, coefficient in enumerate(word))
    digits = []
    for _ in word:
        value, digit = divmod(value, base)
        digits.append(digit)
    return tuple(digits), value


def integer_exterior(base, word):
    left, entry = integer_digits(base, word, 0)
    reversed_digits, overflow = integer_digits(base, word[::-1], 1 - entry)
    if overflow:
        left += ((base - 1) * (1 - entry),)
        right = (1,) + reversed_digits[::-1]
    else:
        right = reversed_digits[::-1]
    if len(left) != len(right):
        raise ArithmeticError("inconsistent arm lengths")
    return tuple(a + b for a, b in zip(left, right)), entry, overflow


@lru_cache(maxsize=None)
def enumerated_moments(base, length):
    counts = Counter()
    for word in itertools.product(range(2 * base - 1), repeat=length):
        counts[sum(coefficient if i % 2 == 0 else -coefficient
                   for i, coefficient in enumerate(word))] += 1
    return counts


def meet_in_middle_count(base, maximum_length):
    """Count widths<=M via their bijection to words padded by leading zeros.

    Prepending M-|B| zeros multiplies R(B) by a sign, so zero residue is
    preserved. Every length-M word corresponds to exactly one empty word or
    word with nonzero first coefficient. Empty B is never accepted.
    """
    left_length = maximum_length // 2
    right_length = maximum_length - left_length
    sign = (-1) ** left_length
    wanted = (-1) ** maximum_length
    return sum(left_count * right_count
               for left, left_count in enumerated_moments(base, left_length).items()
               for right, right_count in enumerated_moments(base, right_length).items()
               if (left + sign * right - wanted) % (base + 1) == 0)


class ExteriorChargeIndependentTests(unittest.TestCase):
    def test_full_modulus_law_in_odd_bases_and_every_suffix_trim(self):
        checked = trims = 0
        for base in (3, 5, 7):
            for length in range(4):
                for word in itertools.product(range(2 * base - 1), repeat=length):
                    raw, entry, overflow = integer_exterior(base, word)
                    self.assertEqual(target.raw_exterior(base, word), (raw, entry, overflow))
                    expected = 0 if overflow else 2 * integer_moment(word)
                    self.assertEqual((integer_moment(raw) - expected) % (base + 1), 0)
                    trimmed = raw
                    while True:
                        self.assertEqual((integer_moment(trimmed) - integer_moment(raw)) % (base + 1), 0)
                        self.assertEqual(target.eligible(base, trimmed), integer_moment(trimmed) % (base + 1) == 0)
                        trims += 1
                        if not trimmed or trimmed[-1] != base - 1:
                            break
                        trimmed = trimmed[:-1]
                    checked += 1
        print(f"independent_odd_base_steps={checked} legal_suffix_trims={trims}", flush=True)

    def test_factor_two_filter_is_strictly_weaker_in_base_three(self):
        # Q=2*alt+(b-1)*sign vanishes modulo4, but R=alt-sign does not.
        self.assertEqual(target.charge(3, (1,)) % 4, 0)
        self.assertEqual(integer_moment((1,)) % 4, 2)
        self.assertFalse(target.eligible(3, (1,)))
        self.assertTrue(target.eligible(3, (3,)))

    def test_decimal_width_eight_count_by_integer_moment_meet_in_middle(self):
        result = target.residue_counts(10, 8, include_empty=True)
        for row in result["rows"]:
            width = row["length"]
            self.assertEqual(row["cumulative_total"], 19 ** width)
            self.assertEqual(row["cumulative_zero_charge"], meet_in_middle_count(10, width))
        self.assertEqual(result["total"], 16983563041)
        self.assertEqual(result["zero_charge"], 1543960696)
        print(f"independent_decimal_width8={result['zero_charge']}/{result['total']}", flush=True)

    def test_odd_base_counts_use_the_full_modulus(self):
        for base in (3, 5, 7):
            result = target.residue_counts(base, 6, include_empty=True)
            for row in result["rows"]:
                self.assertEqual(row["cumulative_zero_charge"], meet_in_middle_count(base, row["length"]))
        self.assertEqual(target.residue_counts(3, 1)["zero_charge"], 1)

    def test_known_cycles_with_concentrated_nonbinary_exterior_trims(self):
        fixtures = fixture_cycles()
        checked_cycles = checked_edges = 0
        for base, original in sorted(fixtures.items()):
            source = original * 2
            period = len(source)
            mass = sum(edge.u for edge in source)
            self.assertGreaterEqual(mass, 2)
            for position in range(period):
                new_trims = [mass if phase == position else 0 for phase in range(period)]
                difference = [0]
                for old, new in zip(source, new_trims):
                    difference.append(difference[-1] + old.u - new)
                self.assertEqual(difference[-1], 0)
                offset = [value - min(difference) for value in difference[:-1]]
                words = [edge.B + (base - 1,) * amount for edge, amount in zip(source, offset)]
                for phase, word in enumerate(words):
                    raw, _, _ = integer_exterior(base, word)
                    successor = words[(phase + 1) % period]
                    self.assertEqual(raw, successor + (base - 1,) * new_trims[phase])
                    self.assertEqual(integer_moment(word) % (base + 1), 0)
                    self.assertTrue(target.eligible(base, word))
                    checked_edges += 1
                checked_cycles += 1
        print(f"independent_retimed_B_cycles={checked_cycles} edges={checked_edges}", flush=True)

    def test_nonnatural_inputs_rejected(self):
        invalid = ((10.0, (1,)), (True, (1,)), (10, (1.5,)),
                   (10, (True,)), (10, (-1,)), (10, (19,)))
        for base, word in invalid:
            with self.subTest(base=base, word=word):
                with self.assertRaises((ValueError, TypeError)):
                    target.raw_exterior(base, word)


if __name__ == "__main__":
    unittest.main(verbosity=2)
