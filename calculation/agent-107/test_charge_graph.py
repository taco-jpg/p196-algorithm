#!/usr/bin/env python3
"""Independent bounded controls for the fixed-width exterior graph.

    python3 -O calculation/agent-107/test_charge_graph.py

The reference builds the original variable-width graph on EVERY valid word,
including the empty word and words rejected by the residue filter. It uses
whole-integer normalization and every legal neutral suffix trim. Kahn's
algorithm checks cycle existence independently of the C++ functional walk.
No full decimal width8 graph is explored by this suite.
"""

from collections import Counter, deque
from functools import lru_cache
import importlib.util
import itertools
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "charge_graph.cpp"
ROOT = HERE.parents[1]


def residue(base, word):
    return (sum(x if position % 2 == 0 else -x
                for position, x in enumerate(word)) - (-1) ** len(word)) % (base + 1)


def fixed_digits(base, coefficients, entry):
    integer = entry + sum(x * base ** position for position, x in enumerate(coefficients))
    digits = []
    for _ in coefficients:
        integer, digit = divmod(integer, base)
        digits.append(digit)
    return tuple(digits), integer


def raw_exterior(base, word):
    left, entry = fixed_digits(base, word, 0)
    right, overflow = fixed_digits(base, word[::-1], 1 - entry)
    if overflow:
        left += ((base - 1) * (1 - entry),)
        right = (1,) + right[::-1]
    else:
        right = right[::-1]
    if len(left) != len(right):
        raise ArithmeticError("inconsistent exterior arm lengths")
    return tuple(a + b for a, b in zip(left, right)), entry, overflow


def legal_words(base, width):
    words = [()]
    for size in range(1, width + 1):
        for first in range(1, 2 * base - 1):
            words.extend((first,) + suffix for suffix in itertools.product(range(2 * base - 1), repeat=size - 1))
    return words


def has_cycle(words, adjacency):
    indegree = {word: 0 for word in words}
    for successors in adjacency.values():
        for successor in successors:
            indegree[successor] += 1
    queue = deque(word for word in words if indegree[word] == 0)
    removed = 0
    while queue:
        word = queue.popleft()
        removed += 1
        for successor in adjacency[word]:
            indegree[successor] -= 1
            if indegree[successor] == 0:
                queue.append(successor)
    return removed != len(words)


@lru_cache(maxsize=None)
def variable_graph(base, width):
    words = legal_words(base, width)
    domain = set(words)
    adjacency = {}
    for word in words:
        raw, _, _ = raw_exterior(base, word)
        successors = []
        trimmed = raw
        while True:
            if trimmed in domain:
                successors.append(trimmed)
            if not trimmed or trimmed[-1] != base - 1:
                break
            trimmed = trimmed[:-1]
        adjacency[word] = successors
    return words, adjacency, has_cycle(words, adjacency)


@lru_cache(maxsize=None)
def fixed_graph(base, width):
    words = [word for word in legal_words(base, width) if len(word) == width and word and residue(base, word) == 0]
    domain = set(words)
    adjacency = {}
    for word in words:
        raw, _, overflow = raw_exterior(base, word)
        if overflow:
            successors = [raw[:-1]] if raw[-1] == base - 1 else []
        else:
            successors = [raw]
        if any(successor not in domain for successor in successors):
            raise ArithmeticError("fixed-width residue domain is not closed on an internal edge")
        adjacency[word] = successors
    return words, adjacency, has_cycle(words, adjacency)


@lru_cache(maxsize=None)
def moment_histogram(base, length):
    counts = Counter()
    for word in itertools.product(range(2 * base - 1), repeat=length):
        counts[sum(x if i % 2 == 0 else -x for i, x in enumerate(word))] += 1
    return counts


def width_count(base, width):
    left = width // 2
    return sum(a_count * b_count
               for a, a_count in moment_histogram(base, left).items()
               for b, b_count in moment_histogram(base, width - left).items()
               if (a + (-1) ** left * b - (-1) ** width) % (base + 1) == 0)


class ChargeGraphIndependentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="agent107-graph-tests-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.binary = Path(cls.temp.name) / "charge_graph"
        build = subprocess.run([os.environ.get("CXX", "g++"), "-O2", "-std=c++17", str(SOURCE),
                                "-o", str(cls.binary)], capture_output=True, text=True,
                               timeout=90, check=False)
        if build.returncode:
            raise AssertionError(f"graph compilation failed: {build.stderr}")

    def invoke(self, base, width, *arguments, code=0):
        run = subprocess.run([str(self.binary), str(base), str(width), *map(str, arguments)],
                             capture_output=True, text=True, timeout=30, check=False)
        self.assertEqual(run.returncode, code, run.stdout + run.stderr)
        records = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
        self.assertEqual(len(records), 1, run.stdout + run.stderr)
        return records[0]

    def check_witness(self, base, width, record):
        witness = record["witness"]
        self.assertTrue(witness)
        for phase, edge in enumerate(witness):
            word, successor = tuple(edge["B"]), tuple(edge["B2"])
            self.assertEqual(len(word), width)
            self.assertTrue(word and word[0] > 0)
            self.assertTrue(all(0 <= coefficient <= 2 * (base - 1) for coefficient in word))
            self.assertEqual(residue(base, word), 0)
            raw, entry, overflow = raw_exterior(base, word)
            self.assertEqual((edge["e"], edge["g"], edge["u"]), (entry, overflow, overflow))
            self.assertEqual(raw, successor + (base - 1,) * overflow)
            self.assertEqual(successor, tuple(witness[(phase + 1) % len(witness)]["B"]))

    def test_all_small_adjacencies_and_original_all_trim_cycle_decisions(self):
        cases = [(2, width) for width in range(7)]
        cases += [(3, width) for width in range(1, 5)]
        cases += [(4, width) for width in range(1, 4)]
        cases += [(10, width) for width in range(1, 4)]
        adjacency_checks = variable_states = variable_edges = 0
        for base, width in cases:
            with self.subTest(base=base, width=width):
                original_words, original_adjacency, original_cyclic = variable_graph(base, width)
                words, adjacency, cyclic = fixed_graph(base, width)
                self.assertEqual(cyclic, original_cyclic)
                ids = {word: index for index, word in enumerate(words)}
                offset = sum(residue(base, word) == 0 for word in original_words if len(word) < width)
                counted = self.invoke(base, width, "count")
                self.assertEqual(counted["status"], "COUNT")
                self.assertEqual(counted["total"], len(words))
                self.assertEqual(counted["offset"], offset)
                self.assertEqual(counted["upper_count"], offset + len(words))
                self.assertEqual(counted["color_bytes"], (len(words) + 3) // 4)
                for word in words:
                    edge = self.invoke(base, width, "edge", json.dumps(word, separators=(",", ":")))
                    raw, entry, overflow = raw_exterior(base, word)
                    expected_exit = not adjacency[word]
                    self.assertEqual(edge["status"], "EDGE")
                    self.assertEqual(edge["B"], list(word))
                    self.assertEqual(edge["raw"], list(raw))
                    self.assertEqual((edge["e"], edge["g"]), (entry, overflow))
                    self.assertIs(edge["exit"], expected_exit)
                    if expected_exit:
                        self.assertIsNone(edge["u"])
                        self.assertIsNone(edge["B2"])
                        self.assertIsNone(edge["target"])
                    else:
                        successor = adjacency[word][0]
                        self.assertEqual(edge["u"], overflow)
                        self.assertEqual(edge["B2"], list(successor))
                        self.assertEqual(edge["target"], ids[successor])
                    adjacency_checks += 1
                census = self.invoke(base, width, "census")
                self.assertEqual(census["status"], "CYCLIC" if cyclic else "ACYCLIC")
                self.assertEqual(census["total"], len(words))
                self.assertEqual(census["offset"], offset)
                if cyclic:
                    self.check_witness(base, width, census)
                else:
                    expected_edges = sum(map(len, adjacency.values()))
                    self.assertEqual(census["visited"], len(words))
                    self.assertEqual(census["finished"], len(words))
                    self.assertEqual(census["edges"], expected_edges)
                    self.assertEqual(census["exited"], len(words) - expected_edges)
                variable_states += len(original_words)
                variable_edges += sum(map(len, original_adjacency.values()))
        print(f"independent_graph_cases={len(cases)} fixed_adjacencies={adjacency_checks} "
              f"original_states={variable_states} original_all_trim_edges={variable_edges}", flush=True)

    def test_nondecimal_positive_control_is_only_an_exterior_witness(self):
        row = self.invoke(2, 2, "census")
        self.assertEqual(row["status"], "CYCLIC")
        self.check_witness(2, 2, row)
        self.assertEqual({tuple(edge["B"]) for edge in row["witness"]}, {(1, 0), (2, 1)})
        self.assertTrue(all("C" not in edge and "C2" not in edge for edge in row["witness"]))

    def test_all_known_exterior_cycles_lift_to_common_width(self):
        # Main's parser supplies fixtures only; all arithmetic below uses this
        # suite's whole-integer normalizer, not the mirror's transition code.
        path = ROOT / "calculation/neutral_band_search.py"
        spec = importlib.util.spec_from_file_location("a107_graph_fixtures", path)
        if spec is None or spec.loader is None:
            raise RuntimeError("main certificate fixture loader unavailable")
        mirror = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mirror)
        fixtures = mirror._lean_certs()
        self.assertEqual(sorted(base for base, _ in fixtures), [2, 4, 8, 11, 16, 17, 26, 32])
        self.assertEqual(sum(len(rows) for _, rows in fixtures), 56)
        independent_edges = native_edges = 0
        skipped_domains = []
        for base, rows in fixtures:
            maximum_width = max(len(edge[0]) for edge in rows)
            for width in (maximum_width, maximum_width + 1):
                with self.subTest(base=base, width=width):
                    padded = [tuple(edge[0]) + (base - 1,) * (width - len(edge[0]))
                              for edge in rows]
                    expected = []
                    for phase, edge in enumerate(rows):
                        source = tuple(edge[0])
                        successor = tuple(edge[2])
                        self.assertEqual(successor, tuple(rows[(phase + 1) % len(rows)][0]))
                        raw, entry, overflow = raw_exterior(base, source)
                        self.assertEqual(raw, successor + (base - 1,) * edge[4])
                        lifted_raw, lifted_entry, lifted_overflow = raw_exterior(base, padded[phase])
                        self.assertEqual((lifted_entry, lifted_overflow), (entry, overflow))
                        self.assertEqual(lifted_raw, raw + (base - 1,) * (width - len(source)))
                        self.assertEqual(lifted_raw,
                                         padded[(phase + 1) % len(rows)] + (base - 1,) * overflow)
                        self.assertEqual(residue(base, padded[phase]), 0)
                        self.assertGreater(padded[phase][0], 0)
                        expected.append((lifted_raw, entry, overflow))
                        independent_edges += 1

                    # Large known fixtures can exceed the C++ index's uint64
                    # representation. Such a domain is explicitly labelled as
                    # unsupported, never interpreted as an acyclic result.
                    count_run = subprocess.run([str(self.binary), str(base), str(width), "count"],
                                               capture_output=True, text=True, timeout=30, check=False)
                    count = json.loads(count_run.stdout)
                    if count_run.returncode == 2:
                        self.assertEqual(count["status"], "ERROR")
                        self.assertEqual(count["error"], "per-residue count exceeds uint64 capacity")
                        skipped_domains.append(f"base{base}/width{width}:uint64_index_unsupported")
                        continue
                    self.assertEqual(count_run.returncode, 0, count_run.stdout + count_run.stderr)
                    self.assertEqual(count["status"], "COUNT")
                    self.assertGreater(count["total"], 0)
                    for phase, word in enumerate(padded):
                        row = self.invoke(base, width, "edge", json.dumps(word, separators=(",", ":")))
                        raw, entry, overflow = expected[phase]
                        self.assertEqual(row["status"], "EDGE")
                        self.assertEqual(row["B"], list(word))
                        self.assertEqual(row["raw"], list(raw))
                        self.assertEqual((row["e"], row["g"], row["u"]), (entry, overflow, overflow))
                        self.assertIs(row["exit"], False)
                        self.assertEqual(row["B2"], list(padded[(phase + 1) % len(rows)]))
                        self.assertGreaterEqual(row["target"], 0)
                        self.assertLess(row["target"], count["total"])
                        native_edges += 1
        self.assertEqual(independent_edges, 112)
        self.assertGreater(native_edges, 0)
        print(f"known_fixture_cycles={len(fixtures)} padded_cycles={2 * len(fixtures)} "
              f"independent_padded_edges={independent_edges} cpp_edges={native_edges} "
              f"cpp_skipped_domains={','.join(skipped_domains) or 'none'}", flush=True)

    def test_zero_path_buffer_uses_exact_fallback(self):
        for base, width in ((3, 2), (2, 2), (10, 3)):
            baseline = self.invoke(base, width, "census")
            fallback = self.invoke(base, width, "census", "--path-cap", 0)
            self.assertEqual(fallback["status"], baseline["status"])
            self.assertEqual(fallback["total"], baseline["total"])
            self.assertGreater(fallback["fallback_paths"], 0)
            if baseline["status"] == "ACYCLIC":
                for field in ("visited", "finished", "edges", "exited"):
                    self.assertEqual(fallback[field], baseline[field])
            else:
                self.check_witness(base, width, fallback)

    def test_incomplete_budgets_never_claim_acyclic(self):
        for option, value in (("--seconds", 0), ("--memory-mib", 0), ("--state-cap", 0), ("--state-cap", 1)):
            with self.subTest(option=option, value=value):
                row = self.invoke(3, 2, "census", option, value, code=3)
                self.assertEqual(row["status"], "UNDECIDED")
                self.assertTrue(row["reason"])
                self.assertLess(row["finished"], row["total"])
        complete = self.invoke(3, 2, "census", "--state-cap", 5)
        self.assertEqual(complete["status"], "ACYCLIC")
        self.assertEqual(complete["visited"], 5)

    def test_width8_count_and_memory_guard_without_graph_traversal(self):
        lower, upper = width_count(10, 7), width_count(10, 8)
        self.assertEqual((lower, upper), (81260909, 1543960696))
        row = self.invoke(10, 8, "count")
        self.assertEqual(row["total"], upper - lower)
        self.assertEqual(row["total"], 1462699787)
        self.assertEqual(row["offset"], lower)
        self.assertEqual(row["color_bytes"], 365674947)
        bounded = self.invoke(10, 8, "census", "--memory-mib", 1, code=3)
        self.assertEqual(bounded["status"], "UNDECIDED")
        self.assertEqual(bounded["visited"], 0)
        print(f"independent_width8_exact_domain={upper - lower} color_bytes=365674947", flush=True)

    def test_edge_queries_require_actual_exact_width_words(self):
        rejected = ([], [10], [0, 10], [1, 1], [19, 7], [-1, 0])
        for word in rejected:
            with self.subTest(word=word):
                row = self.invoke(10, 2, "edge", json.dumps(word, separators=(",", ":")), code=2)
                self.assertEqual(row["status"], "ERROR")

    def test_invalid_resource_options_are_rejected(self):
        cases = [("--seconds", -1), ("--seconds", "nan"), ("--seconds", "inf"),
                 ("--seconds", 1701), ("--memory-mib", -1), ("--memory-mib", 4097),
                 ("--state-cap", -1), ("--path-cap", -1), ("--path-cap", 65537),
                 ("--unknown", 1)]
        for arguments in cases:
            with self.subTest(arguments=arguments):
                row = self.invoke(3, 2, "census", *arguments, code=2)
                self.assertEqual(row["status"], "ERROR")


if __name__ == "__main__":
    unittest.main(verbosity=2)
