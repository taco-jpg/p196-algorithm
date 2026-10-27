#!/usr/bin/env python3
"""Independent arithmetic checks of the center trim-schedule construction.

    python3 -O calculation/agent-107/test_trim_schedule.py

In particular, the full-cycle controls use ordinary integers and reversed
canonical digits, rather than the coefficient mirror used by the selftest.
These are bounded implementation checks; the universal statement is proved
in reports/agent-107-T3.md.
"""

from dataclasses import replace
import itertools
from pathlib import Path
import unittest

import trim_schedule as target


ROOT = Path(__file__).resolve().parents[2]


def integer_normalize(base, coefficients, entry):
    """Independent fixed-width normalization by evaluating one integer first."""
    value = entry + sum(coefficient * base ** i for i, coefficient in enumerate(coefficients))
    digits = []
    for _ in coefficients:
        value, digit = divmod(value, base)
        digits.append(digit)
    return tuple(digits), value


def integer_center(base, coefficients, entry, overflow):
    digits, final = integer_normalize(base, coefficients, entry)
    if final != 1 - entry:
        raise ValueError("carry does not flip")
    extended = digits + (((base - 1) * entry,) if overflow else ())
    return tuple(left + right for left, right in zip(extended, reversed(extended)))


def template_integer(base, edge, gap):
    coefficients = edge.B + (base - 1,) * gap + edge.C + (base - 1,) * gap + edge.B[::-1]
    return sum(coefficient * base ** i for i, coefficient in enumerate(coefficients))


def reverse_integer(base, value):
    reversed_value = 0
    while value:
        value, digit = divmod(value, base)
        reversed_value = reversed_value * base + digit
    return reversed_value


class TrimScheduleIndependentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = target.fixture_cycles(ROOT)

    def test_small_padding_covariance_including_nonsymmetric_words(self):
        checks = 0
        for base, maximum_length in ((2, 5), (3, 4), (4, 3)):
            for size in range(1, maximum_length + 1):
                for coefficients in itertools.product(range(2 * base - 1), repeat=size):
                    for entry in (0, 1):
                        digits, final = integer_normalize(base, coefficients, entry)
                        self.assertEqual(target.normalize(base, coefficients, entry), (digits, final))
                        if final != 1 - entry:
                            continue
                        for amount in range(4):
                            padded = (base - 1,) * amount + coefficients + (base - 1,) * amount
                            for overflow in (0, 1):
                                raw = integer_center(base, coefficients, entry, overflow)
                                expected = (base - 1,) * amount + raw + (base - 1,) * amount
                                self.assertEqual(integer_center(base, padded, entry, overflow), expected)
                                self.assertEqual(target.raw_center(base, padded, entry, overflow), expected)
                                checks += 1
        print(f"independent_local_covariance={checks}", flush=True)

    def test_retimed_certificates_against_ordinary_reverse_add(self):
        cycles = edges = 0
        for base, original in sorted(self.fixtures.items()):
            source = original * 2
            mass = sum(edge.v for edge in source)
            for position in range(len(source)):
                schedule = tuple(mass if phase == position else 0 for phase in range(len(source)))
                transformed, _ = target.retime_cycle(base, source, schedule)
                _, overflows = target.cycle_streams(base, transformed)
                gap = 2 + sum(overflows)
                value = template_integer(base, transformed[0], gap)
                for phase, edge in enumerate(transformed):
                    self.assertEqual(value, template_integer(base, edge, gap))
                    reversed_value = reverse_integer(base, value)
                    self.assertNotEqual(value, reversed_value)
                    value += reversed_value
                    gap += edge.u + edge.v - overflows[phase]
                    successor = transformed[(phase + 1) % len(transformed)]
                    self.assertEqual(value, template_integer(base, successor, gap))
                    edges += 1
                cycles += 1
        print(f"independent_integer_cycles={cycles} independent_integer_edges={edges}", flush=True)

    def test_width_allowance_can_attain_twice_the_total_trim_mass(self):
        base = 26
        original = self.fixtures[base] * 2
        period = len(original)
        mass = sum(edge.v for edge in original)
        at_last = (0,) * (period - 1) + (mass,)
        source, _ = target.retime_cycle(base, original, at_last)
        at_first = (mass,) + (0,) * (period - 1)
        transformed, offsets = target.retime_cycle(base, source, at_first)
        self.assertEqual(offsets, (mass,) + (0,) * (period - 1))
        self.assertEqual(len(transformed[0].C) - len(source[0].C), 2 * mass)
        self.assertEqual(min(offsets), 0)
        for old, new in zip(source, transformed):
            self.assertEqual((old.B, old.B2, old.u), (new.B, new.B2, new.u))

    def test_non_natural_and_malformed_inputs_are_rejected_under_optimization(self):
        original = self.fixtures[2]
        mutations = (
            replace(original[0], u=True),
            replace(original[0], v=False),
            replace(original[0], u=0.0),
            replace(original[0], v=-1),
            replace(original[0], B=(-1,) + original[0].B[1:]),
            replace(original[0], C=(3,) + original[0].C[1:]),
            replace(original[0], B2=original[0].B2 + (0,)),
            replace(original[0], C2=original[0].C2 + (0,)),
        )
        for mutation in mutations:
            self.assertFalse(target.cycle_ok(2, (mutation,) + original[1:]))
        for base in (True, 2.0, 1, -2):
            self.assertFalse(target.cycle_ok(base, original))
        for source, destination in (([True], [1]), ([1], [1.0]), ([1], [2]), ([0], [-1])):
            with self.assertRaises(ValueError):
                target.padding_offsets(source, destination)
        for entry, overflow in ((True, 0), (1, True), (1.0, 0), (1, 0.0)):
            with self.assertRaises(ValueError):
                target.raw_center(10, (4,), entry, overflow)


if __name__ == "__main__":
    unittest.main(verbosity=2)
