#!/usr/bin/env python3
"""Independent acceptance, mutation, domain, and optimized-runtime controls."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import integer_divisibility_check as check


def fixture(base=10):
    system = {"format": "p196-center-affine-v1", "variables": ["x", "base"],
              "target_base": base, "itinerary": {}, "inequalities": [],
              "equalities": [
                  {"label": "trim", "coefficients": [64, -93], "rhs": -68, "origin": {}},
                  {"label": "base", "coefficients": [0, 1], "rhs": base, "origin": {}}]}
    proof = {"format": "p196-integer-row-divisibility-v1", "multipliers": [1, 93],
             "combined_coefficients": [64, 0], "combined_rhs": 93 * base - 68,
             "coefficient_gcd": 64}
    return system, proof


class DivisibilityCheck(unittest.TestCase):
    def test_rationally_consistent_integer_obstruction(self):
        system, proof = fixture()
        self.assertEqual(proof["combined_rhs"], 862)
        self.assertTrue(check.verify(system, proof))
        # x=431/32 solves the two equations over Q, but no integer x does.
        self.assertEqual(64 * 431, 862 * 32)
        system, proof = fixture(20)
        self.assertEqual(proof["combined_rhs"], 64 * 28)
        self.assertFalse(check.verify(system, proof))

    def test_negative_combination(self):
        system, proof = fixture()
        proof.update(multipliers=[-1, -93], combined_coefficients=[-64, 0], combined_rhs=-862)
        self.assertTrue(check.verify(system, proof))

    def test_every_variable_enters_gcd(self):
        system, proof = fixture()
        system["equalities"][1]["coefficients"] = [0, 2]
        proof.update(combined_coefficients=[64, 93], coefficient_gcd=1)
        self.assertFalse(check.verify(system, proof))

    def test_mutated_claims_fail(self):
        mutations = [lambda p: p.update(combined_rhs=863),
                     lambda p: p.update(combined_coefficients=[32, 0]),
                     lambda p: p.update(coefficient_gcd=32),
                     lambda p: p.update(multipliers=[1, 92]),
                     lambda p: p.update(multipliers=[0, 0], combined_coefficients=[0, 0],
                                        combined_rhs=0, coefficient_gcd=0)]
        for mutate in mutations:
            system, proof = fixture()
            mutate(proof)
            self.assertFalse(check.verify(system, proof))

    def test_zero_gcd_rational_case_is_separate(self):
        system, proof = fixture()
        system["equalities"] = [{"label": "impossible", "coefficients": [0, 0], "rhs": 1, "origin": {}}]
        proof.update(multipliers=[1], combined_coefficients=[0, 0], combined_rhs=1, coefficient_gcd=0)
        self.assertFalse(check.verify(system, proof))

    def test_strict_schema(self):
        mutations = [lambda p: p.update(multipliers=[True, 93]),
                     lambda p: p.update(multipliers=[1.0, 93]),
                     lambda p: p.update(multipliers=[[1, 1], 93]),
                     lambda p: p.update(multipliers=[1]),
                     lambda p: p.update(combined_coefficients=[64]),
                     lambda p: p.update(combined_coefficients=[64, False]),
                     lambda p: p.update(combined_rhs=862.0),
                     lambda p: p.update(coefficient_gcd=-64),
                     lambda p: p.update(coefficient_gcd=True)]
        for mutate in mutations:
            system, proof = fixture()
            mutate(proof)
            with self.assertRaises(check.InvalidInput):
                check.verify(system, proof)

    def test_limits(self):
        system, proof = fixture()
        proof["multipliers"][0] = 1 << check.MAX_PROOF_BITS
        with self.assertRaises(check.UnsupportedInput):
            check.verify(system, proof)
        system, proof = fixture()
        with patch.object(check, "MAX_ADDITIONS", 1), self.assertRaises(check.UnsupportedInput):
            check.verify(system, proof)
        with patch.object(check, "MAX_ACCUMULATOR_BITS", 1), self.assertRaises(check.UnsupportedInput):
            check.verify(system, proof)

    def test_normal_and_optimized_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            system_path, proof_path = [Path(directory) / name for name in ("system.json", "proof.json")]
            for flags in ([], ["-O"]):
                for base, expected in ((10, 0), (20, 1)):
                    system, proof = fixture(base)
                    system_path.write_text(json.dumps(system))
                    proof_path.write_text(json.dumps(proof))
                    run = subprocess.run([sys.executable, *flags, str(Path(check.__file__)),
                                          str(system_path), str(proof_path)], capture_output=True, text=True)
                    self.assertEqual(run.returncode, expected, run.stdout + run.stderr)
                    self.assertIn("status", json.loads(run.stdout))


if __name__ == "__main__":
    unittest.main()
