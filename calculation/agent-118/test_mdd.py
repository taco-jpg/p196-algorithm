#!/usr/bin/env python3
"""Tiny exact oracles for cyclic segment relations, independent of cauto.

For one input word x, choose (y_s, c_s) from table[s][x_s].  The output
letter at segment s is (y_s, c_{s+1}), with the last link closing at c_0.
Union is taken over whole input words: coordinate marginals are insufficient.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import itertools
from pathlib import Path
import random
import re
import subprocess

from check_center import parse_witness


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def explicit_image(frontier, tables):
    """Definition-level oracle; enumerate choices for each actual input word."""
    segments = len(tables)
    if segments == 0:
        raise ValueError("the no-trim/no-segment relation is unsupported")
    result = set()
    for word in frontier:
        require(len(word) == segments, "input word has incorrect dimension")
        choices = [tables[s].get(word[s], ()) for s in range(segments)]
        for selected in itertools.product(*choices):
            result.add(tuple((selected[s][0], selected[(s + 1) % segments][1])
                             for s in range(segments)))
    return result


class Diagram:
    """Canonical finite-language DAG. Node 0 is empty; node 1 accepts epsilon."""
    def __init__(self):
        self.nodes = [None, None]
        self.unique = {}
        self.union_cache = {}

    def make(self, depth, branches):
        arcs = tuple(sorted((label, child) for label, child in branches.items() if child))
        if not arcs:
            return 0
        key = (depth, arcs)
        if key not in self.unique:
            self.unique[key] = len(self.nodes)
            self.nodes.append(key)
        return self.unique[key]

    def union(self, left, right):
        if not left or left == right:
            return right
        if not right:
            return left
        key = (min(left, right), max(left, right))
        if key in self.union_cache:
            return self.union_cache[key]
        require(left != 1 and right != 1, "union mixes different word lengths")
        depth, arcs = self.nodes[left]
        other_depth, other_arcs = self.nodes[right]
        require(depth == other_depth, "union mixes different variable positions")
        branches = dict(arcs)
        for label, child in other_arcs:
            branches[label] = self.union(branches.get(label, 0), child)
        root = self.make(depth, branches)
        self.union_cache[key] = root
        return root

    def from_words(self, words, depth=0):
        words = set(words)
        if not words:
            return 0
        if () in words:
            require(words == {()}, "language has mixed word lengths")
            return 1
        buckets = {}
        for word in words:
            buckets.setdefault(word[0], set()).add(word[1:])
        return self.make(depth, {label: self.from_words(tails, depth + 1)
                                 for label, tails in buckets.items()})

    def words(self, root):
        if root == 0:
            return set()
        if root == 1:
            return {()}
        return {(label,) + tail for label, child in self.nodes[root][1]
                for tail in self.words(child)}


def diagram_image(frontier, tables):
    """Relational image retaining the original input-DAG path and cyclic c_0."""
    segments = len(tables)
    if not segments:
        raise ValueError("the no-trim/no-segment relation is unsupported")
    inputs, outputs = Diagram(), Diagram()
    input_root = inputs.from_words(frontier)
    guesses = [sorted({c for rows in table.values() for _, c in rows}) for table in tables]

    @lru_cache(None)
    def visit(node, segment, required_guess, first_guess):
        if not node:
            return 0
        require(node != 1 and inputs.nodes[node][0] == segment, "invalid input-DAG depth")
        branches = {}
        for old_letter, child in inputs.nodes[node][1]:
            for y, c in tables[segment].get(old_letter, ()):
                if c != required_guess:
                    continue
                if segment + 1 == segments:
                    require(child == 1, "last input segment does not accept")
                    label, tail = (y, first_guess), 1
                    branches[label] = outputs.union(branches.get(label, 0), tail)
                else:
                    for next_guess in guesses[segment + 1]:
                        tail = visit(child, segment + 1, next_guess, first_guess)
                        label = (y, next_guess)
                        branches[label] = outputs.union(branches.get(label, 0), tail)
        return outputs.make(segment, branches)

    root = 0
    for first_guess in guesses[0]:
        root = outputs.union(root, visit(input_root, 0, first_guess, first_guess))
    return outputs, root


def check_model(frontier, tables):
    expected = explicit_image(frontier, tables)
    output, root = diagram_image(frontier, tables)
    actual = output.words(root)
    require(expected == actual, f"image mismatch: missing={expected - actual}, extra={actual - expected}")
    require(output.from_words(expected) == root, "equal languages have unequal canonical roots")
    return len(expected), len(output.nodes) - 2


def regression_models():
    # Same coordinate marginals do not permit the two missing diagonal corners.
    correlated = {(0, 0), (1, 1)}
    tables = [{0: [(0, 0)], 1: [(1, 0)]} for _ in range(2)]
    exact = explicit_image(correlated, tables)
    relaxed_inputs = set(itertools.product(*[set(word[s] for word in correlated) for s in range(2)]))
    relaxed = explicit_image(relaxed_inputs, tables)
    require(len(exact) == 2 and len(relaxed) == 4 and exact < relaxed,
            "correlation counterexample was not reproduced")
    yield correlated, tables

    # Equal first output labels must merge BOTH suffix languages.
    yield {(0, 0), (1, 1)}, [{0: [(9, 0)], 1: [(9, 0)]},
                             {0: [(4, 1)], 1: [(5, 1)]}]

    # Last output uses the first segment's guess, not its own guess.
    source, tables = {(0, 0)}, [{0: [(5, 2)]}, {0: [(6, 9)]}]
    require(explicit_image(source, tables) == {((5, 9), (6, 2))}, "cyclic link changed")
    yield source, tables

    # One segment closes to its own choice; -1 is a meaningful inactive value.
    yield {(0,)}, [{0: [(7, -1), (8, 3), (7, -1)]}]

    # Dead local choices eliminate the corresponding entire input path only.
    yield {(0, 1), (1, 0)}, [{0: [], 1: [(2, -1)]}, {0: [(3, 4)], 1: []}]
    yield set(), [{0: [(1, 0)]}, {0: [(2, 0)]}]
    yield {(0, 0)}, [{0: []}, {0: [(2, 0)]}]


def abstract_selftest(random_cases=128):
    rng = random.Random(118340)
    totals = Counter()
    models = list(regression_models())
    for _ in range(random_cases):
        segments = rng.randrange(1, 6)
        alphabet = rng.randrange(1, 4)
        words = list(itertools.product(range(alphabet), repeat=segments))
        frontier = set(rng.sample(words, rng.randrange(min(len(words), 12) + 1)))
        tables = [{old: [(rng.randrange(3), rng.choice((-1, 0, 1, 2)))
                         for _ in range(rng.randrange(4))]
                   for old in range(alphabet)} for _ in range(segments)]
        models.append((frontier, tables))
    for frontier, tables in models:
        image_size, node_count = check_model(frontier, tables)
        totals["models"] += 1
        totals["input_words"] += len(frontier)
        totals["output_words"] += image_size
        totals["max_output_words"] = max(totals["max_output_words"], image_size)
        totals["max_nodes"] = max(totals["max_nodes"], node_count)
    for oracle in (explicit_image, diagram_image):
        try:
            oracle({()}, [])
        except ValueError:
            totals["no_segment_rejections"] += 1
        else:
            raise RuntimeError("unsupported no-segment case silently accepted")
    return dict(sorted(totals.items()))


def fields(line):
    return dict(re.findall(r"(\w+)=([^ ]+)", line))


def checked_run(command, completed=True):
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    if completed:
        require(result.returncode == 0, f"unexpected solver exit: {command}\n{result.stderr}")
        require("UNDECIDED" not in result.stdout + result.stderr,
                f"incomplete control: {command}")
    else:
        require(result.returncode == 2 and "UNDECIDED" in result.stdout + result.stderr,
                f"guard did not return explicit UNDECIDED: {command}")
        require("MDD_DONE" not in result.stdout, "guarded search printed a completed decision")
    return result


def feasible_headers(text):
    return {tuple(line.split()[:6]) for line in text.splitlines() if line.startswith("FEASIBLE")}


def production_checks(binary, baseline=None):
    """Seven complete explicit-frontier comparisons plus targeted boundary checks."""
    cases = [
        (2, "1010", "1010", "0001"),
        (2, "1010", "1010", "1000"),
        (2, "0000", "1010", "0001"),
        (4, "100100", "100100", "000001"),
        (10, "101010010101" * 2, "100010001000" * 2, "00001000" * 3),
        (10, "101010010101" * 2, "100010001000" * 2, "10000000" * 3),
        (10, "101010010101" * 2, "100010001000" * 2, "111" + "0" * 21),
    ]
    tally = Counter()
    for base, entering, overflow, trims in cases:
        common = [str(base), entering, overflow, "1", "1", "-v", trims,
                  "-allm", "-cap", "1000000", "-w"]
        command = [str(binary), *common, "--compare", "-quiet",
                   "-nodes", "1000000", "-ops", "100000000"]
        result = checked_run(command)
        done = [line for line in result.stdout.splitlines() if line.startswith("MDD_DONE ")]
        require(len(done) == 1, "missing unique MDD completion")
        info = fields(done[0])
        require(info["scope"] == "allm" and info["status"] in ("none", "hit"),
                "control did not complete its all-length scope")
        require(int(info["classes"]) == 2 * int(info["period"]), "incomplete long-width classes")
        require(int(info["mlo"]) > 2 * len(entering), "invalid all-length threshold")
        tally["allm_controls"] += 1
        tally["exact_frontier_comparisons"] += int(info["comparisons"])
        tally["allm_" + info["status"]] += 1
        for line in result.stdout.splitlines():
            if line.startswith("FEASIBLE"):
                _, period, _ = parse_witness(line)
                tally["witnesses_replayed"] += 1
                tally["witness_edges_replayed"] += period
        if baseline is not None:
            old = checked_run([str(baseline), *common])
            old_done = [line for line in old.stdout.splitlines() if line.startswith("DONE ")]
            require(len(old_done) == 1, "missing baseline completion")
            original = fields(old_done[0])
            for name in ("status", "jstar", "period", "mlo", "classes", "tails"):
                require(original[name] == info[name], f"baseline metadata mismatch: {name}")
            require(feasible_headers(old.stdout) == feasible_headers(result.stdout),
                    "baseline feasible width/classes differ")
            tally["baseline_allm_agreements"] += 1

    # The real P48 target has one million first-layer tuples. Compare them all;
    # stop after that layer and require the honest non-completion result.
    command = [str(binary), "10", "101010010101" * 4, "100010001000" * 4,
               "1", "1", "-v", "00001000" * 6, "-allm", "--compare",
               "-cap", "1000000", "-nodes", "1000000", "-ops", "100000000",
               "-layers", "1"]
    result = checked_run(command, completed=False)
    layers = [fields(line) for line in result.stdout.splitlines() if line.startswith("MDD_LAYER ")]
    require(len(layers) == 1 and layers[0]["j"] == "1"
            and layers[0]["kind"] == "generic" and layers[0]["tuples"] == "1000000"
            and layers[0]["count_exact"] == "1", "P48 first-layer comparison did not finish")
    require("mdd_generic_period_not_detected" in result.stderr,
            "P48 control stopped for an unexpected reason")
    tally["p48_explicit_tuples_compared"] = 1000000
    tally["p48_period_limit_rejected"] = 1

    # Guards must never emit a negative mathematical decision.
    guards = [
        ([str(binary), "2", "0", "0", "1", "1", "-v", "0"],
         "mdd_requires_positive_trim_segments"),
        ([str(binary), "2", "1010", "1010", "1", "1", "-v", "0001",
          "-allm", "-nodes", "3"], "mdd_node_cap"),
        ([str(binary), "2", "1010", "1010", "1", "1", "-v", "0001",
          "-allm", "-ops", "1"], "mdd_operation_cap"),
    ]
    for command, reason in guards:
        result = checked_run(command, completed=False)
        require(reason in result.stderr, "guard stopped for an unexpected reason")
        tally["resource_or_scope_guards"] += 1
    return dict(sorted(tally.items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--random-cases", type=int, default=128)
    parser.add_argument("--binary", type=Path, help="also test the production C++ MDD engine")
    parser.add_argument("--baseline", type=Path, help="compare completed all-length metadata to cauto")
    args = parser.parse_args()
    if args.baseline and not args.binary:
        parser.error("--baseline requires --binary")
    print("abstract_segment_oracle", abstract_selftest(args.random_cases))
    if args.binary:
        print("production_mdd_checks", production_checks(args.binary, args.baseline))
    print("COMPUTED CHECKS PASSED; exact finite set equality only")


if __name__ == "__main__":
    main()
