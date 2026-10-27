#!/usr/bin/env python3
"""Independent controls for the period-four mod101 quotient obstruction.

    python3 -O calculation/agent-107/test_period4_quotient.py

Witness transitions are computed by normalizing whole Python integers. The
unchanged main mirror is a separate comparison. Rational elimination checks
the determinant and adjugate cofactors construct the modular inverse.
"""

import copy
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

import period4_quotient as target


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MODULUS = 101


def integer_norm(base, word, entry):
    value = entry + sum(coefficient * base ** i for i, coefficient in enumerate(word))
    digits = []
    for _ in word:
        value, digit = divmod(value, base)
        digits.append(digit)
    return tuple(digits), value


def integer_edge(base, word, center):
    left, entry = integer_norm(base, word, 0)
    middle, second_entry = integer_norm(base, center, entry)
    right, overflow = integer_norm(base, word[::-1], second_entry)
    if overflow:
        left += ((base - 1) * (1 - entry),)
        right = (1,) + right[::-1]
        y = (base - 1) * (1 - second_entry)
        center_left, center_right = middle + (y,), (y,) + middle[::-1]
    else:
        right = right[::-1]
        center_left, center_right = middle, middle[::-1]
    if len(left) != len(right) or len(center_left) != len(center_right):
        raise ArithmeticError("inconsistent raw arm lengths")
    return (tuple(a + b for a, b in zip(left, right)),
            tuple(a + b for a, b in zip(center_left, center_right)),
            entry, second_entry, overflow)


def class_moments(word):
    return tuple(sum(coefficient - 9 for i, coefficient in enumerate(word) if i % 4 == j)
                 for j in range(4))


def alternating_residual(word):
    return sum(coefficient if i % 2 == 0 else -coefficient
               for i, coefficient in enumerate(word)) - (-1) ** len(word)


def determinant(matrix):
    size = len(matrix)
    rows = [[Fraction(value) for value in row] for row in matrix]
    result = Fraction(1)
    for column in range(size):
        pivot = next((i for i in range(column, size) if rows[i][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            result = -result
        diagonal = rows[column][column]
        result *= diagonal
        for i in range(column + 1, size):
            scale = rows[i][column] / diagonal
            rows[i] = [a - scale * b for a, b in zip(rows[i], rows[column])]
    if result.denominator != 1:
        raise ArithmeticError("an integer matrix has a noninteger determinant")
    return result.numerator


def cofactor_inverse(matrix, modulus):
    scale = pow(determinant(matrix) % modulus, -1, modulus)
    size = len(matrix)
    return [[scale * (-1) ** (row + column) * determinant(
                [[matrix[i][j] for j in range(size) if j != row]
                 for i in range(size) if i != column]) % modulus
             for column in range(size)] for row in range(size)]


def modular_rank(matrix, modulus):
    rows = [[value % modulus for value in row] for row in matrix]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = pow(rows[rank][column], -1, modulus)
        rows[rank] = [value * scale % modulus for value in rows[rank]]
        for i in range(len(rows)):
            if i != rank:
                multiple = rows[i][column]
                rows[i] = [(a - multiple * b) % modulus for a, b in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def multiply(left, right, modulus):
    return [[sum(a * b for a, b in zip(row, column)) % modulus
             for column in zip(*right)] for row in left]


class PeriodFourIndependentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = target.build_certificate()
        path = ROOT / "calculation/neutral_band_search.py"
        spec = importlib.util.spec_from_file_location("a107_period4_main_mirror", path)
        if spec is None or spec.loader is None:
            raise RuntimeError("unchanged main mirror unavailable")
        cls.mirror = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mirror)

    def test_all_eight_edges_agree_with_integer_arithmetic_and_main_mirror(self):
        certificate = self.certificate
        self.assertEqual((certificate["base"], certificate["modulus"], certificate["width"],
                          certificate["period"]), (10, 101, 16, 4))
        self.assertEqual([pair["j"] for pair in certificate["pairs"]], [2, 3, 4, 5])
        checked = 0
        for pair in certificate["pairs"]:
            left, right = target.make_pair(pair["j"])
            expected_left = [1] * 16
            expected_left[0] = 2
            for index, value in zip((pair["j"], pair["j"] + 4, pair["j"] + 8), (5, 5, 4)):
                expected_left[index] = value
            expected_right = expected_left.copy()
            expected_right[pair["j"]], expected_right[pair["j"] + 4] = 10, 0
            self.assertEqual((tuple(left), tuple(right)), (tuple(expected_left), tuple(expected_right)))
            self.assertEqual(class_moments(left), class_moments(right))
            self.assertEqual(pair["input_moments"], list(class_moments(left)))
            for side, word in (("left", tuple(left)), ("right", tuple(right))):
                with self.subTest(j=pair["j"], side=side):
                    edge = pair[side]
                    self.assertEqual(edge["B"], list(word))
                    self.assertEqual(edge["C"], [18])
                    self.assertEqual((edge["u"], edge["v"]), (0, 0))
                    self.assertEqual(len(word), 16)
                    self.assertGreater(word[0], 0)
                    self.assertTrue(all(type(value) is int and 0 <= value <= 18 for value in word))
                    self.assertNotEqual(word[-1], 9)
                    raw, raw_center, entry, second_entry, overflow = integer_edge(10, word, (18,))
                    self.assertEqual((entry, second_entry, overflow), (0, 1, 0))
                    self.assertEqual(edge["B2"], list(raw))
                    self.assertEqual(edge["C2"], list(raw_center))
                    self.assertEqual(raw_center, (16,))
                    self.assertEqual((edge["e"], edge["e2"], edge["g"]), (entry, second_entry, overflow))
                    self.assertGreater(raw[0], 0)
                    self.assertTrue(all(0 <= value <= 18 for value in raw))
                    self.assertNotEqual(raw[-1], 9)
                    target_entry = integer_norm(10, raw, 0)[1]
                    target_center_exit = integer_norm(10, raw_center, target_entry)[1]
                    self.assertNotEqual(target_entry, target_center_exit)
                    self.assertEqual(alternating_residual(word) % 11, 0)
                    self.assertEqual(alternating_residual(raw) % 11, 0)
                    self.assertEqual((edge["source_R11"], edge["target_R11"]), (0, 0))
                    self.assertEqual(edge["source_moments"], list(class_moments(word)))
                    self.assertEqual(edge["target_moments"], list(class_moments(raw)))
                    mirror_edge = (list(word), [18], list(raw), list(raw_center), 0, 0)
                    self.assertTrue(self.mirror.hyp(10, list(word), [18]))
                    self.assertTrue(self.mirror.hyp(10, list(raw), list(raw_center)))
                    self.assertTrue(self.mirror.edgeOK(10, mirror_edge))
                    self.assertEqual(tuple(self.mirror.nextB(10, list(word), [18])), raw)
                    self.assertEqual(tuple(self.mirror.nextC(10, list(word), [18])), raw_center)
                    self.assertEqual((self.mirror.e1(10, list(word)),
                                      self.mirror.e2(10, list(word), [18]),
                                      self.mirror.gam(10, list(word), [18])), (0, 1, 0))
                    self.assertIs(edge["mirror_edge_ok"], True)
                    self.assertEqual(target.raw_exterior(word), edge)
                    checked += 1
        print(f"independent_collision_pairs=4 exact_integer_and_mirror_edges={checked}", flush=True)

    def test_collision_matrix_exact_determinant_rank_and_two_sided_inverse(self):
        rows = []
        for pair in self.certificate["pairs"]:
            left_raw, *_ = integer_edge(10, tuple(pair["left"]["B"]), (18,))
            right_raw, *_ = integer_edge(10, tuple(pair["right"]["B"]), (18,))
            difference = [right - left for left, right in zip(class_moments(left_raw), class_moments(right_raw))]
            expected = [0] * 4
            expected[(pair["j"] - 1) % 4] += 1
            expected[pair["j"] % 4] -= 20
            expected[(pair["j"] + 1) % 4] += 1
            self.assertEqual(difference, expected)
            self.assertEqual(pair["difference"], difference)
            rows.append(difference)
        self.assertEqual(rows, [[0, 1, -20, 1], [1, 0, 1, -20],
                                [-20, 1, 0, 1], [1, -20, 1, 0]])
        self.assertEqual(self.certificate["matrix"], rows)
        self.assertEqual(determinant(rows), 158400)
        self.assertEqual(determinant(rows) % MODULUS, 32)
        self.assertEqual((self.certificate["determinant"], self.certificate["determinant_mod"]), (158400, 32))
        self.assertEqual(modular_rank(rows, MODULUS), 4)
        self.assertEqual(self.certificate["rank"], 4)
        inverse = cofactor_inverse(rows, MODULUS)
        self.assertEqual(self.certificate["inverse_mod"], inverse)
        identity = [[int(row == column) for column in range(4)] for row in range(4)]
        self.assertEqual(multiply(rows, inverse, MODULUS), identity)
        self.assertEqual(multiply(inverse, rows, MODULUS), identity)

    def test_natural_decimal_period_four_weight_collides(self):
        weights = tuple(pow(10, position, MODULUS) for position in range(4))
        self.assertEqual(weights, (1, 10, 100, 91))
        differences = []
        for pair in self.certificate["pairs"]:
            source_charges = []
            target_charges = []
            for side in ("left", "right"):
                word = tuple(pair[side]["B"])
                raw, *_ = integer_edge(10, word, (18,))
                source_charge = sum(a * b for a, b in zip(class_moments(word), weights)) % MODULUS
                target_charge = sum(a * b for a, b in zip(class_moments(raw), weights)) % MODULUS
                self.assertEqual(target.charge(word, weights), source_charge)
                self.assertEqual(target.charge(raw, weights), target_charge)
                source_charges.append(source_charge)
                target_charges.append(target_charge)
            self.assertEqual(source_charges[0], source_charges[1])
            self.assertNotEqual(target_charges[0], target_charges[1])
            differences.append((target_charges[1] - target_charges[0]) % MODULUS)
        self.assertEqual(differences, [20, 99, 81, 2])

    def test_mod11_alternating_control_is_preserved(self):
        alternating = (1, -1, 1, -1)
        for pair in self.certificate["pairs"]:
            difference = pair["difference"]
            self.assertEqual(sum(a * b for a, b in zip(difference, alternating)) % 11, 0)
            for side in ("left", "right"):
                word = tuple(pair[side]["B"])
                raw, *_ = integer_edge(10, word, (18,))
                self.assertEqual(alternating_residual(raw) % 11,
                                 2 * alternating_residual(word) % 11)
                self.assertEqual(alternating_residual(word) % 11, 0)
        self.assertEqual(modular_rank(self.certificate["matrix"], 11), 3)

    def test_supplied_witness_and_linear_algebra_corruption_is_rejected(self):
        mutations = {
            "source_digit": lambda c: c["pairs"][0]["left"]["B"].__setitem__(2, 6),
            "output_digit": lambda c: c["pairs"][0]["right"]["B2"].__setitem__(0, 5),
            "input_moment": lambda c: c["pairs"][0]["input_moments"].__setitem__(0, 999),
            "difference_row": lambda c: c["pairs"][0]["difference"].__setitem__(0, 1),
            "matrix_entry": lambda c: c["matrix"][0].__setitem__(0, 1),
            "exact_determinant": lambda c: c.__setitem__("determinant", 158501),
            "inverse_entry": lambda c: c["inverse_mod"][0].__setitem__(0, (c["inverse_mod"][0][0] + 1) % 101),
            "rank": lambda c: c.__setitem__("rank", 3),
            "stream_bit": lambda c: c["pairs"][0]["left"].__setitem__("g", 1),
            "mirror_result": lambda c: c["pairs"][0]["left"].__setitem__("mirror_edge_ok", False),
        }
        self.assertIsInstance(target.validate_certificate(copy.deepcopy(self.certificate)), dict)
        for name, mutate in mutations.items():
            with self.subTest(corruption=name):
                corrupted = copy.deepcopy(self.certificate)
                mutate(corrupted)
                with self.assertRaises((ValueError, TypeError)):
                    target.validate_certificate(corrupted)

    def test_cli_evidence_is_checked_under_optimized_python(self):
        for command in ("check", "witnesses"):
            run = subprocess.run([sys.executable, "-O", str(HERE / "period4_quotient.py"), command],
                                 text=True, capture_output=True, timeout=30, check=False)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            row = json.loads(run.stdout)
            self.assertEqual(row["status"], "PASS")
            if command == "witnesses":
                self.assertEqual(row["certificate"], self.certificate)
                self.assertIsInstance(target.validate_certificate(row["certificate"]), dict)


if __name__ == "__main__":
    unittest.main(verbosity=2)
