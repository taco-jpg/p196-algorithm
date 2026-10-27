#!/usr/bin/env python3
"""Adversarial independent controls for the row identity acceptance boundary."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import row_contradiction_check as check


def row(label, coefficients, rhs):
    return {"label": label, "coefficients": coefficients, "rhs": rhs, "origin": {}}


def fixture():
    system = {"format": "p196-center-affine-v1", "variables": ["x", "b"],
              "target_base": 10, "itinerary": {}, "inequalities": [],
              "equalities": [row("first", [1, 2], 3), row("second", [2, 4], 7)]}
    proof = {"format": "p196-rational-row-contradiction-v1", "multipliers": [[2, 1], [-1, 1]]}
    return system, proof


class RowCheck(unittest.TestCase):
    def test_genuine_scaled_contradictions(self):
        system, proof = fixture()
        self.assertTrue(check.verify(system, proof))
        for n, d in ((1, 7), (-11, 23), (10**100, 17)):
            proof["multipliers"] = [[2 * n, d], [-n, d]]
            self.assertTrue(check.verify(system, proof))

    def test_false_or_vacuous_identities(self):
        system, proof = fixture()
        system["equalities"][1]["rhs"] = 6
        self.assertFalse(check.verify(system, proof))
        system, proof = fixture()
        proof["multipliers"] = [[1, 1], [-1, 1]]
        self.assertFalse(check.verify(system, proof))
        proof["multipliers"] = [[0, 1], [0, 1]]
        self.assertFalse(check.verify(system, proof))
        system["equalities"] = []
        proof["multipliers"] = []
        self.assertFalse(check.verify(system, proof))

    def test_inequality_only_conflict_is_not_this_proof(self):
        system, proof = fixture()
        system["equalities"] = []
        system["inequalities"] = [row("x<=0", [1, 0], 0), row("x>=1", [-1, 0], -1)]
        proof["multipliers"] = []
        self.assertFalse(check.verify(system, proof))

    def test_opaque_status_cannot_change_acceptance(self):
        system, proof = fixture()
        proof["status"] = "NO_CONTRADICTION"
        system["status"] = "FEASIBLE"
        self.assertTrue(check.verify(system, proof))
        proof["multipliers"] = [[0, 1], [0, 1]]
        proof["status"] = "PROVED"
        self.assertFalse(check.verify(system, proof))

    def test_malformed_systems(self):
        mutations = [
            lambda s: s.update(format="other"),
            lambda s: s.update(variables=[]),
            lambda s: s.update(variables=["x", "x"]),
            lambda s: s.update(variables=["", "b"]),
            lambda s: s.update(target_base=True),
            lambda s: s.update(target_base=1),
            lambda s: s.update(itinerary=[]),
            lambda s: s.update(inequalities=None),
            lambda s: s["equalities"][0].update(coefficients=[1]),
            lambda s: s["equalities"][0].update(coefficients=[True, 2]),
            lambda s: s["equalities"][0].update(rhs=3.0),
            lambda s: s["equalities"][0].update(origin=[]),
            lambda s: s["equalities"][0].update(label=""),
        ]
        for mutation in mutations:
            system, proof = fixture()
            mutation(system)
            with self.assertRaises(check.InvalidInput):
                check.verify(system, proof)

    def test_malformed_proofs(self):
        for multipliers in ([], [[2, 1]], [[2, 0], [-1, 1]],
                            [[2, -1], [-1, 1]], [[True, 1], [-1, 1]],
                            [[2.0, 1], [-1, 1]], [[2, 1, 0], [-1, 1]]):
            system, proof = fixture()
            proof["multipliers"] = multipliers
            with self.assertRaises(check.InvalidInput):
                check.verify(system, proof)

    def test_budgets_fail_closed(self):
        system, proof = fixture()
        system["equalities"][0]["rhs"] = 1 << check.MAX_ROW_BITS
        with self.assertRaises(check.UnsupportedInput):
            check.verify(system, proof)
        system, proof = fixture()
        proof["multipliers"][0][0] = 1 << check.MAX_PROOF_BITS
        with self.assertRaises(check.UnsupportedInput):
            check.verify(system, proof)
        system, proof = fixture()
        with patch.object(check, "MAX_ADDITIONS", 1), self.assertRaises(check.UnsupportedInput):
            check.verify(system, proof)
        with patch.object(check, "MAX_ACCUMULATOR_BITS", 1), self.assertRaises(check.UnsupportedInput):
            check.verify(system, proof)

    def test_json_parser(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.json"
            for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
                path.write_text(text)
                with self.assertRaises(check.InvalidInput):
                    check.read_json(path)
            path.write_text('{"n":' + "1" * 4_900 + '}')
            self.assertGreater(check.read_json(path)["n"].bit_length(), 16_000)
            path.write_text('{"n":' + "1" * 5_001 + '}')
            with self.assertRaises(check.UnsupportedInput):
                check.read_json(path)
            with patch.object(check, "MAX_FILE_BYTES", 2), self.assertRaises(check.UnsupportedInput):
                check.read_json(path)

    def test_cli_normal_and_optimized(self):
        with tempfile.TemporaryDirectory() as directory:
            system, proof = fixture()
            paths = [Path(directory) / "system.json", Path(directory) / "proof.json"]
            paths[0].write_text(json.dumps(system))
            for optimized in ([], ["-O"]):
                for expected, multipliers in ((0, [[2, 1], [-1, 1]]),
                                              (1, [[0, 1], [0, 1]]),
                                              (2, [[True, 1], [-1, 1]])):
                    proof["multipliers"] = multipliers
                    paths[1].write_text(json.dumps(proof))
                    run = subprocess.run([sys.executable, *optimized, str(Path(check.__file__)),
                                          *map(str, paths)], capture_output=True, text=True)
                    self.assertEqual(run.returncode, expected, run.stdout + run.stderr)
                    self.assertIn("status", json.loads(run.stdout))


if __name__ == "__main__":
    unittest.main()
