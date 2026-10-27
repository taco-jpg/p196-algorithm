#!/usr/bin/env python3
"""Independent validation of the neutral exterior state's dense index.

    python3 -O calculation/agent-107/test_charge_index.py

Small domains are independently enumerated in fixed-width lexicographic
order. Larger rank queries use cyclic-polynomial exponentiation to count
completions, rather than importing the C++ count table or another new PR.
Base2 has a separate closed-form ternary oracle at the uint64 boundary.
"""

from functools import lru_cache
import itertools
import json
import os
from pathlib import Path
import random
import subprocess
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "charge_index.cpp"
U64_MAX = (1 << 64) - 1


def residue(base, word):
    return (sum(x if i % 2 == 0 else -x for i, x in enumerate(word))
            - (-1) ** len(word)) % (base + 1)


def decode(word):
    position = 0
    while position < len(word) and word[position] == 0:
        position += 1
    return list(word[position:])


def brute_domain(base, width):
    return [decode(word) for word in itertools.product(range(2 * base - 1), repeat=width)
            if residue(base, word) == 0]


def cyclic_product(left, right):
    modulus = len(left)
    out = [0] * modulus
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[(i + j) % modulus] += a * b
    return tuple(out)


def cyclic_power(poly, exponent):
    result = (1,) + (0,) * (len(poly) - 1)
    while exponent:
        if exponent & 1:
            result = cyclic_product(result, poly)
        poly = cyclic_product(poly, poly)
        exponent //= 2
    return result


@lru_cache(maxsize=None)
def polynomial_counts(base, length):
    """Coefficients of F(X)^ceil(n/2)*F(X^-1)^floor(n/2) mod X^(b+1)-1."""
    plus = [0] * (base + 1)
    minus = [0] * (base + 1)
    for digit in range(2 * base - 1):
        plus[digit % (base + 1)] += 1
        minus[-digit % (base + 1)] += 1
    return cyclic_product(cyclic_power(tuple(plus), (length + 1) // 2),
                          cyclic_power(tuple(minus), length // 2))


def polynomial_rank(base, width, word):
    padded = [0] * (width - len(word)) + list(word)
    rank = prefix = 0
    for position, digit in enumerate(padded):
        factor = (-1) ** position
        tail = width - position - 1
        suffix_factor = -factor
        counts = polynomial_counts(base, tail)
        for earlier in range(digit):
            wanted = ((-1) ** width - prefix - factor * earlier) * suffix_factor
            rank += counts[wanted % (base + 1)]
        prefix += factor * digit
    if residue(base, padded):
        raise ValueError("polynomial rank requires an accepted word")
    return rank


def ternary_unrank(width, rank):
    """Base2: first width-1 coefficients are rank's padded ternary digits."""
    prefix = [0] * (width - 1)
    for position in range(width - 2, -1, -1):
        rank, prefix[position] = divmod(rank, 3)
    if rank:
        raise ValueError("rank exceeds ternary prefix space")
    moment = sum(x if i % 2 == 0 else -x for i, x in enumerate(prefix))
    last = (((-1) ** width - moment) * (-1) ** (width - 1)) % 3
    return decode(prefix + [last])


def command_word(name, word):
    return name + " " + json.dumps(list(word), separators=(",", ":"))


class ChargeIndexIndependentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="agent107-index-tests-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.binary = Path(cls.temp.name) / "charge_index"
        build = subprocess.run(
            [os.environ.get("CXX", "g++"), "-O2", "-std=c++17", str(SOURCE), "-o", str(cls.binary)],
            text=True, capture_output=True, timeout=90, check=False,
        )
        if build.returncode:
            raise AssertionError(f"index compilation failed: {build.stderr}")

    def batch(self, base, width, commands, code=0):
        run = subprocess.run(
            [str(self.binary), str(base), str(width)], input="\n".join(commands) + "\n",
            text=True, capture_output=True, timeout=30, check=False,
        )
        self.assertEqual(run.returncode, code, run.stdout + run.stderr)
        records = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
        self.assertEqual(len(records), len(commands), run.stdout + run.stderr)
        if code == 0:
            for record in records:
                self.assertIs(record.get("ok"), True, record)
        return records

    def test_complete_small_domains_and_every_rank(self):
        domains = [(2, width) for width in range(7)]
        domains += [(3, width) for width in range(1, 5)]
        domains += [(4, width) for width in range(1, 4)]
        domains += [(10, width) for width in range(1, 4)]
        checked = 0
        for base, width in domains:
            with self.subTest(base=base, width=width):
                expected = brute_domain(base, width)
                commands = ["count", f"enumerate 0 {len(expected) + 2}"]
                for rank, word in enumerate(expected):
                    commands.extend((command_word("contains", word), command_word("rank", word), f"unrank {rank}"))
                records = self.batch(base, width, commands)
                self.assertEqual(records[0]["count"], len(expected))
                items = records[1]["items"]
                self.assertEqual(items, [{"rank": rank, "B": word} for rank, word in enumerate(expected)])
                self.assertEqual(records[1]["emitted"], len(expected))
                self.assertEqual(records[1]["total"], len(expected))
                self.assertEqual(records[1]["start"], 0)
                self.assertEqual(records[1]["requested_limit"], len(expected) + 2)
                for rank, word in enumerate(expected):
                    contains, ranked, unranked = records[2 + 3 * rank:5 + 3 * rank]
                    self.assertTrue(contains["contains"])
                    self.assertEqual(ranked["rank"], rank)
                    self.assertEqual(unranked["B"], word)
                    self.assertEqual(polynomial_rank(base, width, word), rank)
                checked += len(expected)
        print(f"independent_small_domains={len(domains)} ranked_words={checked}", flush=True)

    def test_large_decimal_random_ranks_and_iterator_windows(self):
        rng = random.Random(107)
        checked = 0
        for width, expected_count in ((8, 1543960696), (12, 201210447209175)):
            count = polynomial_counts(10, width)[(-1) ** width % 11]
            self.assertEqual(count, expected_count)
            ranks = [0, 1, count // 2, count - 2, count - 1] + [rng.randrange(count) for _ in range(25)]
            commands = ["count"] + [f"unrank {rank}" for rank in ranks]
            records = self.batch(10, width, commands)
            self.assertEqual(records[0]["count"], count)
            words = [record["B"] for record in records[1:]]
            for rank, word in zip(ranks, words):
                self.assertTrue(word and word[0] != 0)
                self.assertLessEqual(len(word), width)
                self.assertEqual(residue(10, word), 0)
                self.assertEqual(polynomial_rank(10, width, word), rank)
            ranked = self.batch(10, width, [command_word("rank", word) for word in words])
            self.assertEqual([row["rank"] for row in ranked], ranks)
            starts = [0, count // 2, count - 1, count]
            enumerated = self.batch(10, width, [f"enumerate {start} 17" for start in starts])
            for start, row in zip(starts, enumerated):
                expected_ranks = list(range(start, min(start + 17, count)))
                self.assertEqual(row["emitted"], len(expected_ranks))
                self.assertEqual(row["total"], count)
                self.assertEqual(row["start"], start)
                self.assertEqual([item["rank"] for item in row["items"]], expected_ranks)
                for item in row["items"]:
                    self.assertEqual(polynomial_rank(10, width, item["B"]), item["rank"])
            checked += len(ranks)
        print(f"independent_large_decimal_ranks={checked}", flush=True)

    def test_ids_are_stable_when_width_cap_increases(self):
        for base, smaller, larger in ((2, 5, 12), (3, 3, 8), (10, 3, 8)):
            words = brute_domain(base, smaller)
            records = self.batch(base, larger, [command_word("rank", word) for word in words])
            self.assertEqual([row["rank"] for row in records], list(range(len(words))))
            initial = self.batch(base, larger, [f"enumerate 0 {len(words)}"])[0]
            self.assertEqual([item["B"] for item in initial["items"]], words)
        rng = random.Random(10712)
        count = 1543960696
        ranks = [0, count - 1] + [rng.randrange(count) for _ in range(30)]
        rows = self.batch(10, 8, [f"unrank {rank}" for rank in ranks])
        commands = [command_word("rank", row["B"]) for row in rows] + [f"unrank {rank}" for rank in ranks]
        wider = self.batch(10, 12, commands)
        self.assertEqual([row["rank"] for row in wider[:len(ranks)]], ranks)
        self.assertEqual([row["B"] for row in wider[len(ranks):]], [row["B"] for row in rows])

    def test_base_two_uint64_boundary_has_closed_form_oracle(self):
        count = 3 ** 40
        self.assertLess(count, U64_MAX)
        self.assertGreater(3 ** 41, U64_MAX)
        ranks = [0, 1, 2, count // 2, count - 1, 1 << 63, (1 << 63) + 107]
        commands = ["count"] + [f"unrank {rank}" for rank in ranks]
        rows = self.batch(2, 41, commands)
        self.assertEqual(rows[0]["count"], count)
        expected = [ternary_unrank(41, rank) for rank in ranks]
        self.assertEqual([row["B"] for row in rows[1:]], expected)
        ranked = self.batch(2, 41, [command_word("rank", word) for word in expected])
        self.assertEqual([row["rank"] for row in ranked], ranks)

    def test_enumeration_range_arithmetic_does_not_wrap(self):
        count = len(brute_domain(10, 2))
        rows = self.batch(10, 2, [f"enumerate {count - 1} {U64_MAX}", f"enumerate {count} 0", "enumerate 0 0"])
        self.assertEqual(rows[0]["emitted"], 1)
        self.assertEqual(rows[0]["items"][0]["rank"], count - 1)
        self.assertEqual(rows[1]["items"], [])
        self.assertEqual(rows[2]["items"], [])

    def test_membership_rejects_words_outside_the_declared_domain(self):
        rejected = [[], [0], [0, 10], [1], [19], [10, 0, 0]]
        rows = self.batch(10, 2, [command_word("contains", word) for word in rejected])
        self.assertEqual([row["contains"] for row in rows], [False] * len(rejected))

    def test_invalid_commands_fail_and_batch_continues(self):
        commands = [
            "rank []", "rank [0,10]", "rank [1]", "rank [19]", "rank [-1]",
            "rank [10,0,0]", "rank [1.5]", "rank [true]", "rank [1,]",
            "unrank -1", "unrank 34", f"unrank {U64_MAX + 1}",
            "enumerate 35 0", "enumerate 0 -1", "unknown", "count",
        ]
        rows = self.batch(10, 2, commands, code=2)
        for row in rows[:-1]:
            self.assertFalse(row["ok"], row)
            self.assertTrue(row["error"])
        self.assertEqual(rows[-1]["count"], 34)

    def test_unsupported_or_overflowing_constructor_arguments(self):
        cases = [[], [10], [1, 2], [63, 2], [10, -1], [10, 65],
                 [2, 42], [10, 16], [10, "1.5"], [10, str(U64_MAX + 1)]]
        for args in cases:
            with self.subTest(args=args):
                run = subprocess.run([str(self.binary), *map(str, args)], input="count\n",
                                     text=True, capture_output=True, timeout=5, check=False)
                self.assertEqual(run.returncode, 2, run.stdout + run.stderr)

    def test_cursor_rejects_a_temporary_owner_at_compile_time(self):
        directory = Path(self.temp.name)
        compiler = os.environ.get("CXX", "g++")
        supported = directory / "cursor_lifetime_supported.cpp"
        supported.write_text('''#include "charge_index.hpp"
int main() {
  using Index = p196::agent107::ChargeIndex;
  const Index owner(10, 2);
  auto cursor = owner.stream(0, 1);
  if (cursor.done() || cursor.id() != 0 || owner.rank(cursor.word()) != 0) return 1;
  cursor.advance();
  if (!cursor.done()) return 2;
  unsigned visited = 0;
  bool correct = true;
  Index(10, 2).for_each(0, 2, [&](Index::Count id, const Index::Word &word) {
    ++visited;
    if (id == 0 && word != Index::Word{10}) correct = false;
    if (id == 1 && word != Index::Word{1, 0}) correct = false;
  });
  return visited == 2 && correct ? 0 : 3;
}
''')
        executable = directory / "cursor_lifetime_supported"
        built = subprocess.run([compiler, "-std=c++17", "-I", str(HERE), str(supported),
                                "-o", str(executable)], capture_output=True, text=True,
                               timeout=30, check=False)
        self.assertEqual(built.returncode, 0, built.stderr)
        ran = subprocess.run([str(executable)], capture_output=True, text=True,
                             timeout=5, check=False)
        self.assertEqual(ran.returncode, 0, ran.stdout + ran.stderr)
        rejected = directory / "cursor_lifetime_rejected.cpp"
        rejected.write_text('''#include "charge_index.hpp"
int main() {
  auto cursor = p196::agent107::ChargeIndex(10, 2).stream(0, 1);
  return cursor.done();
}
''')
        built = subprocess.run([compiler, "-std=c++17", "-I", str(HERE), "-c", str(rejected),
                                "-o", str(directory / "rejected.o")],
                               capture_output=True, text=True, timeout=30, check=False)
        self.assertNotEqual(built.returncode, 0)
        self.assertIn("deleted", built.stderr.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
