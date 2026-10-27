#!/usr/bin/env python3
"""Independent finite-set audit of the cyclic segment MDD recurrence.

This reference model uses no center arithmetic or production C++ MDD code.
It checks correlated input languages, canonical union, signed inactive symbols,
single-segment cyclic closure, changed transition signatures, and a backward
predecessor extractor against exhaustive finite relational composition.

Run: python3 calculation/agent-111/mdd_audit.py
This is a finite algorithm audit, not a decimal certificate or Lean theorem.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import product
import json
import random


class MDD:
    """Fixed-level canonical finite languages; nodes are immutable Python tuples."""

    def __init__(self, variables: int):
        if variables < 1:
            raise ValueError("require at least one variable")
        self.variables = variables
        self.nodes = [(-1, ()), (variables, ())]
        self.unique = {}
        self.union_cache = {}

    def make(self, level, edges):
        if not 0 <= level < self.variables:
            raise ValueError("invalid nonterminal level")
        merged = {}
        for label, child in edges:
            if child == 0:
                continue
            if self.nodes[child][0] != level + 1:
                raise ValueError("MDD edges must advance exactly one level")
            merged[label] = self.unite(merged.get(label, 0), child)
        if not merged:
            return 0
        key = (level, tuple(sorted(merged.items())))
        if key not in self.unique:
            self.unique[key] = len(self.nodes)
            self.nodes.append(key)
        return self.unique[key]

    def unite(self, left, right):
        if left == right or right == 0:
            return left
        if left == 0:
            return right
        left, right = sorted((left, right))
        key = (left, right)
        if key not in self.union_cache:
            ll, le = self.nodes[left]
            rl, re = self.nodes[right]
            if ll != rl:
                raise ValueError("union requires the same remaining variables")
            self.union_cache[key] = self.make(ll, le + re)
        return self.union_cache[key]

    def from_tuples(self, words):
        root = 0
        for word in words:
            if len(word) != self.variables:
                raise ValueError("tuple arity mismatch")
            node = 1
            for i in range(self.variables - 1, -1, -1):
                node = self.make(i, [(word[i], node)])
            root = self.unite(root, node)
        return root

    def to_set(self, node):
        if node == 0:
            return set()
        if node == 1:
            return {()}
        return {(label,) + suffix
                for label, child in self.nodes[node][1]
                for suffix in self.to_set(child)}

    def image(self, root, relations):
        # This memo belongs to exactly this call/transition signature.
        # It must not persist across different generic or terminal-tail steps.
        @lru_cache(None)
        def delayed(node, previous_y, first_c):
            if node == 0:
                return 0
            i = self.nodes[node][0]
            if node == 1:
                return self.make(self.variables - 1,
                                 [(encode(self.variables - 1, previous_y, first_c), 1)])
            edges = []
            for source, child in self.nodes[node][1]:
                for y, c in relations[i].get(source, ()):
                    edges.append((encode(i - 1, previous_y, c),
                                  delayed(child, y, first_c)))
            return self.make(i - 1, edges)

        if root == 0:
            return 0
        if self.nodes[root][0] != 0 or len(relations) != self.variables:
            raise ValueError("image requires a full-arity input language")
        result = 0
        for source, child in self.nodes[root][1]:
            for y, c in relations[0].get(source, ()):
                result = self.unite(result, delayed(child, y, c))
        return result

    def predecessor(self, root, relations, target):
        """Find an entire input-language path for a fixed output tuple."""
        if len(target) != self.variables:
            raise ValueError("output tuple arity mismatch")
        decoded = [decode(i, x) for i, x in enumerate(target)]

        @lru_cache(None)
        def walk(node):
            if node == 0:
                return None
            if node == 1:
                return ()
            i = self.nodes[node][0]
            required = (decoded[i][0], decoded[(i - 1) % self.variables][1])
            for source, child in self.nodes[node][1]:
                if required in relations[i].get(source, ()):
                    suffix = walk(child)
                    if suffix is not None:
                        return (source,) + suffix
            return None

        return walk(root)


def encode(segment, y, next_c):
    if y not in range(3) or next_c not in range(-1, 3):
        raise ValueError("synthetic symbol outside test alphabet")
    return 100 * segment + 16 * y + next_c + 1


def decode(segment, label):
    value = label - 100 * segment
    y, c = value // 16, value % 16 - 1
    if encode(segment, y, c) != label:
        raise ValueError("invalid synthetic local state label")
    return y, c


def explicit_image(frontier, relations):
    result = set()
    variables = len(relations)
    for word in frontier:
        for choices in product(*(relations[i].get(source, ())
                                 for i, source in enumerate(word))):
            result.add(tuple(encode(i, choices[i][0], choices[(i + 1) % variables][1])
                             for i in range(variables)))
    return result


def audit(cases_per_arity=100):
    if not 1 <= cases_per_arity <= 1000:
        raise ValueError("cases per arity must be in 1..1000")
    rng = random.Random(111)
    cases = output_words = backward_checks = signature_checks = 0
    for variables in range(1, 7):
        universe = list(product(range(2), repeat=variables))
        for _ in range(cases_per_arity):
            frontier = set(rng.sample(universe, rng.randrange(min(len(universe), 16) + 1)))
            relations = [{source: rng.sample(list(product(range(3), range(-1, 3))),
                                             rng.randrange(4))
                          for source in range(2)} for _ in range(variables)]
            expected = explicit_image(frontier, relations)
            mdd = MDD(variables)
            root = mdd.from_tuples(frontier)
            shuffled = list(frontier)
            rng.shuffle(shuffled)
            if mdd.from_tuples(shuffled + shuffled[:1]) != root:
                raise RuntimeError("canonical root depends on insertion order or duplicates")
            symbolic = mdd.image(root, relations)
            if mdd.to_set(symbolic) != expected:
                raise RuntimeError("symbolic image differs from explicit relational image")
            if mdd.from_tuples(expected) != symbolic:
                raise RuntimeError("equal finite languages have different canonical roots")
            # Reusing the same input root under a new tail signature must not
            # reuse stale memoized images from a previous transition relation.
            if mdd.image(root, [{} for _ in range(variables)]) != 0:
                raise RuntimeError("stale image memo survived a changed signature")
            if mdd.image(root, relations) != symbolic:
                raise RuntimeError("stable labels/arena failed on a repeated image")
            signature_checks += 1
            for target in rng.sample(list(expected), min(10, len(expected))):
                predecessor = mdd.predecessor(root, relations, target)
                if predecessor not in frontier:
                    raise RuntimeError("backward witness is outside input frontier")
                decoded = [decode(i, x) for i, x in enumerate(target)]
                if not all((decoded[i][0], decoded[(i - 1) % variables][1])
                           in relations[i][source]
                           for i, source in enumerate(predecessor)):
                    raise RuntimeError("backward local relation mismatch")
                backward_checks += 1
            cases += 1
            output_words += len(expected)
    return {"correlated_cyclic_image_cases": cases,
            "explicit_output_tuples": output_words,
            "backward_predecessor_checks": backward_checks,
            "changed_signature_checks": signature_checks}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases-per-arity", type=int, default=100)
    arguments = parser.parse_args()
    print(json.dumps(audit(arguments.cases_per_arity), sort_keys=True))
