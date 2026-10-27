#!/usr/bin/env python3
"""Independent bounded regression checks for the guarded exterior automaton.

Run from the repository root:
    python3 calculation/agent-107/test_bauto_guarded.py

The original transition implementation is compiled independently for differential
positive controls. A separate digit-arithmetic routine replays every returned B
witness; no guarded transition helper is imported. All runs have short timeouts.
Temporary source/binaries disappear when the suite finishes.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WRAPPER = HERE / "bauto_guarded.py"
ORIGINAL = ROOT / "calculation/neutral_band/structure/bauto.cpp"
P11_G = "11100010000"
P12_G = "100010001000"
P16_G4 = "1000100010001000"


def execute(args, timeout=45):
    return subprocess.run(
        [str(arg) for arg in args], capture_output=True, text=True,
        timeout=timeout, check=False,
    )


def read_original_accepts(stdout):
    """Parse original public output without using the new wrapper parser."""
    result = {}
    pattern = re.compile(
        r"^ACCEPT b=(\d+) p=(\d+) g=([01]+) e=([01]+) "
        r"depth=(\d+) states=(\d+)(?: B_t=(.*))?$"
    )
    for line in stdout.splitlines():
        if not line.startswith("ACCEPT"):
            continue
        match = pattern.fullmatch(line)
        if not match:
            raise AssertionError(f"Unrecognized original ACCEPT: {line!r}")
        witness = [
            [int(value) for value in word.split(",") if value]
            for word in re.findall(r"\[([^\]]*)\]", match[7] or "")
        ]
        result[match[4]] = {
            "depth": int(match[5]), "states": int(match[6]), "B_t": witness,
        }
    return result


def arithmetic_step(base, word):
    """Independent autonomous B step: two elementary long-addition passes."""
    forward = []
    carry = 0
    for coefficient in word:
        carry, digit = divmod(coefficient + carry, base)
        forward.append(digit)
    e = carry
    reverse = []
    carry = 1 - e
    for coefficient in reversed(word):
        carry, digit = divmod(coefficient + carry, base)
        reverse.append(digit)
    overflow = carry
    if overflow:
        left = forward + [(base - 1) * (1 - e)]
        right = [1] + list(reversed(reverse))
    else:
        left = forward
        right = list(reversed(reverse))
    if len(left) != len(right):
        raise AssertionError("Mismatched arithmetic-step lengths")
    successor = [x + y for x, y in zip(left, right)]
    while successor and successor[-1] == base - 1:
        successor.pop()
    return e, overflow, successor


class GuardedAutomatonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="agent107-bauto-tests-")
        cls.addClassCleanup(cls.temp.cleanup)
        temp = Path(cls.temp.name)
        cls.binary = temp / "bauto_guarded"
        cls.original = temp / "bauto_original"
        cls.truncated = temp / "bauto_original_depth1"
        build = execute([sys.executable, WRAPPER, "--build", cls.binary], 90)
        if build.returncode:
            raise AssertionError(f"Guarded build failed: {build.stdout}\n{build.stderr}")
        compiler = os.environ.get("CXX", "g++")
        build = execute([compiler, "-O2", "-std=c++17", ORIGINAL, "-o", cls.original], 90)
        if build.returncode:
            raise AssertionError(f"Original build failed: {build.stderr}")
        original_text = ORIGINAL.read_text()
        old = "while(!fr.empty()&&depth<400){"
        if original_text.count(old) != 1:
            raise AssertionError("Original depth guard changed; audit fixture needs review")
        fixture = temp / "bauto_original_depth1.cpp"
        fixture.write_text(original_text.replace(old, "while(!fr.empty()&&depth<1){", 1))
        build = execute([compiler, "-O2", "-std=c++17", fixture, "-o", cls.truncated], 90)
        if build.returncode:
            raise AssertionError(f"Controlled-depth fixture build failed: {build.stderr}")

    def invoke(self, *args, expected_code=0):
        process = execute([self.binary, *args])
        self.assertEqual(process.returncode, expected_code, process.stdout + process.stderr)
        records = [json.loads(line) for line in process.stdout.splitlines() if line.strip()]
        streams = [record for record in records if record.get("type") == "STREAM"]
        summaries = [record for record in records if record.get("type") == "SUMMARY"]
        self.assertEqual(len(summaries), 1, records)
        summary = summaries[0]
        self.assertEqual(summary["streams"], len(streams))
        self.assertEqual(summary["exhausted"], sum(row["status"] == "EXHAUSTED" for row in streams))
        self.assertEqual(summary["undecided"], sum(row["status"] == "UNDECIDED" for row in streams))
        return streams, summary

    def replay_witness(self, record, accepted):
        base, period = record["base"], record["period"]
        witness = accepted["B_t"]
        self.assertEqual(len(witness), period)
        self.assertEqual(len(accepted["e"]), period)
        self.assertEqual(len(record["g"]), period)
        for phase, word in enumerate(witness):
            self.assertTrue(not word or word[0] > 0)
            self.assertTrue(all(0 <= digit <= 2 * (base - 1) for digit in word))
            e, overflow, successor = arithmetic_step(base, word)
            self.assertEqual(e, int(accepted["e"][phase]))
            self.assertEqual(overflow, int(record["g"][phase]))
            self.assertEqual(successor, witness[(phase + 1) % period])

    def test_original_depth_exit_is_silent_but_guarded_is_undecided(self):
        legacy = execute([self.truncated, 10, 11, 11, "-g", P11_G])
        self.assertEqual(legacy.returncode, 0)
        self.assertEqual(read_original_accepts(legacy.stdout), {})
        self.assertIn("p=11 done", legacy.stderr)
        self.assertNotIn("cap", legacy.stderr.lower())
        rows, _ = self.invoke(10, 11, 11, "-g", P11_G, "-depth", 1, expected_code=3)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], "UNDECIDED")
        self.assertEqual(rows[0]["reason"], "depth_cap")
        self.assertEqual(rows[0]["depth"], 1)
        self.assertEqual(rows[0]["accepted"], [])

    def test_zero_depth_is_unexamined_not_exhausted(self):
        rows, _ = self.invoke(10, 11, 11, "-g", P11_G, "-depth", 0, expected_code=3)
        self.assertEqual(rows[0]["reason"], "depth_cap")
        self.assertEqual(rows[0]["states"], 1)
        self.assertEqual(rows[0]["depth"], 0)

    def test_state_cap_is_undecided(self):
        rows, _ = self.invoke(10, 11, 11, "-g", P11_G, "-cap", 1, expected_code=3)
        self.assertEqual(rows[0]["status"], "UNDECIDED")
        self.assertEqual(rows[0]["reason"], "state_cap")

    def test_oversized_key_is_not_silently_skipped(self):
        rows, _ = self.invoke(10, 22, 22, "-g", "1" * 22, expected_code=3)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], "UNDECIDED")
        self.assertEqual(rows[0]["reason"], "unsupported_key")
        self.assertEqual(rows[0]["accepted"], [])

    def test_invalid_arguments_fail_before_search(self):
        invalid = [
            [], [10], [1, 3, 3], [10, 0, 0], [10, 64, 64],
            [10, 12, 11], [10, 11, 11, "-g", "111x0010000"],
            [10, 11, 11, "-g", "1"], [10, 11, 12, "-g", P11_G],
            [10, 11, 11, "-part", 0, 0], [10, 11, 11, "-part", -1, 2],
            [10, 11, 11, "-part", 2, 2], [10, 11, 11, "-cap", 0],
            [10, 11, 11, "-depth", -1], [10, 11, 11, "-g"],
            [10, 11, 11, "-cap", "abc"], [10, 11, 11, "-unknown"],
        ]
        for arguments in invalid:
            with self.subTest(arguments=arguments):
                process = execute([self.binary, *arguments])
                self.assertEqual(process.returncode, 2, process.stdout + process.stderr)
                errors = [json.loads(line) for line in process.stderr.splitlines() if line.strip()]
                self.assertTrue(any(record.get("type") == "ERROR" for record in errors), process.stderr)
                self.assertNotIn('"type":"STREAM"', process.stdout)

    def test_known_positive_streams_match_original_and_replay(self):
        cases = [
            (11, P11_G, {"10100110011"}, 18061),
            (12, P12_G, {"101010010101", "010110101001", "100101011010"}, 136653),
        ]
        for period, pattern, expected_e, expected_states in cases:
            with self.subTest(period=period):
                arguments = [10, period, period, "-g", pattern, "-w"]
                legacy = execute([self.original, *arguments])
                self.assertEqual(legacy.returncode, 0, legacy.stderr)
                original_accepts = read_original_accepts(legacy.stdout)
                self.assertEqual(set(original_accepts), expected_e)
                rows, _ = self.invoke(*arguments)
                self.assertEqual(len(rows), 1)
                row = rows[0]
                self.assertEqual(row["status"], "EXHAUSTED")
                self.assertEqual(row["reason"], "frontier_empty")
                self.assertEqual(row["states"], expected_states)
                self.assertEqual({entry["e"] for entry in row["accepted"]}, expected_e)
                for accepted in row["accepted"]:
                    original = original_accepts[accepted["e"]]
                    self.assertEqual(accepted["depth"], original["depth"])
                    self.assertEqual(accepted["B_t"], original["B_t"])
                    self.replay_witness(row, accepted)

    def test_acceptance_at_depth_limit_remains_a_partial_enumeration(self):
        rows, _ = self.invoke(10, 11, 11, "-g", P11_G, "-depth", 29, "-w", expected_code=3)
        row = rows[0]
        self.assertEqual(row["status"], "UNDECIDED")
        self.assertEqual(row["reason"], "depth_cap")
        self.assertEqual({entry["e"] for entry in row["accepted"]}, {"10100110011"})
        for accepted in row["accepted"]:
            self.replay_witness(row, accepted)

    def test_natural_exhaustion_has_exact_known_state_count(self):
        rows, _ = self.invoke(10, 16, 16, "-g", P16_G4)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], "EXHAUSTED")
        self.assertEqual(rows[0]["reason"], "frontier_empty")
        self.assertEqual(rows[0]["states"], 13170)
        self.assertEqual(rows[0]["accepted"], [])

    def test_state_cap_retains_acceptance_in_partial_next_layer(self):
        rows, _ = self.invoke(10, 11, 11, "-g", P11_G, "-cap", 10736,
                              "-w", expected_code=3)
        row = rows[0]
        self.assertEqual(row["status"], "UNDECIDED")
        self.assertEqual(row["reason"], "state_cap")
        self.assertEqual(row["states"], 10736)
        self.assertEqual(row["depth"], 28)
        self.assertEqual({entry["e"] for entry in row["accepted"]}, {"10100110011"})
        for accepted in row["accepted"]:
            self.assertEqual(accepted["depth"], 29)
            self.replay_witness(row, accepted)

    def test_partition_preserves_every_small_necklace_once(self):
        whole, _ = self.invoke(10, 1, 5)
        first, _ = self.invoke(10, 1, 5, "-part", 0, 2)
        second, _ = self.invoke(10, 1, 5, "-part", 1, 2)
        key = lambda row: (row["period"], row["g"])
        expected = {key(row) for row in whole}
        actual_first = {key(row) for row in first}
        actual_second = {key(row) for row in second}
        self.assertFalse(actual_first & actual_second)
        self.assertEqual(actual_first | actual_second, expected)
        self.assertEqual(len(whole), 23)  # 2 + 3 + 4 + 6 + 8 binary necklaces
        self.assertEqual({key(row): row for row in whole}, {key(row): row for row in first + second})


if __name__ == "__main__":
    unittest.main(verbosity=2)
