#!/usr/bin/env python3
"""Abstract checks of Brent recurrence and pinned-DAG witness recomputation.

This is a finite-state model, not a test of the production exterior engine.
Python's explicit sets are the independent frontier oracle.
"""
from itertools import product
from math import ceil, log2
import random


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def check_brent():
    cases = 0
    for size in range(1, 6):
        for mapping in product(range(size), repeat=size):
            for start in range(size):
                current = anchor = start
                depth = anchor_depth = power = 1
                distance = 0
                history = [None, start]
                while True:
                    if distance == power:
                        anchor, anchor_depth = current, depth
                        power *= 2
                        distance = 0
                    current = mapping[current]
                    depth += 1
                    distance += 1
                    history.append(current)
                    if current == anchor:
                        require(1 <= anchor_depth < depth, "invalid repeated indices")
                        require(history[anchor_depth] == history[depth], "false repeat")
                        visited = set(history[1:])
                        state = current
                        for _ in range(4 * size):
                            state = mapping[state]
                            require(state in visited, "unseen future terminal could occur")
                        break
                    require(depth <= 8 * size + 8, "Brent did not detect a finite cycle")
                cases += 1
    print(f"PASS abstract Brent: {cases} complete finite-function/start cases")


class Dag:
    """Canonical binary-word sets with immutable, never-reused node IDs."""
    def __init__(self, width):
        self.width = width
        self.nodes = {0: (-1, ()), 1: (width, ())}
        self.unique = {}
        self.next_id = 2
        self.swept = 0

    def live(self, node):
        require(node in self.nodes, f"stale node {node}")

    def build(self, words):
        words = frozenset(words)
        def visit(level, suffixes):
            if not suffixes:
                return 0
            if level == self.width:
                return 1
            bit = self.width - level - 1
            arcs = tuple((label, visit(level + 1,
                         frozenset(w for w in suffixes if ((w >> bit) & 1) == label)))
                         for label in (0, 1))
            arcs = tuple((label, child) for label, child in arcs if child)
            key = level, arcs
            if key not in self.unique:
                node = self.next_id
                self.next_id += 1
                self.nodes[node] = key
                self.unique[key] = node
            return self.unique[key]
        return visit(0, words)

    def words(self, root):
        self.live(root)
        def visit(node, prefix):
            self.live(node)
            if node == 0:
                return set()
            if node == 1:
                return {prefix}
            level, arcs = self.nodes[node]
            out = set()
            for label, child in arcs:
                out.update(visit(child, prefix | (label << (self.width - level - 1))))
            return out
        return visit(root, 0)

    def collect(self, pins):
        marked = {0, 1}
        todo = list(pins)
        while todo:
            node = todo.pop()
            self.live(node)
            if node in marked:
                continue
            marked.add(node)
            todo.extend(child for _, child in self.nodes[node][1])
        dead = set(self.nodes) - marked
        for node in dead:
            key = self.nodes.pop(node)
            require(self.unique.pop(key) == node, "unique-table corruption")
        self.swept += len(dead)


def relation_image(words, relation):
    return set().union(*(relation[word] for word in words)) if words else set()


def check_gc_brent(rng):
    cases, swept = 0, 0
    for _ in range(512):
        dag = Dag(3)
        relation = [set(rng.sample(range(8), rng.randrange(4))) for _ in range(8)]
        initial = {rng.randrange(8)}
        physical = dag.build(initial)
        truth = {rng.randrange(8)}
        current = anchor = dag.build(truth)
        anchor_truth = truth.copy()
        depth = anchor_depth = power = 1
        distance = 0
        dag.collect([physical, current, anchor])
        for _step in range(1024):
            if not truth:
                break
            if distance == power:
                anchor, anchor_depth = current, depth
                anchor_truth = truth.copy()
                power *= 2
                distance = 0
            # Simulate unrelated intermediate union nodes, to force real sweeps.
            dag.build(set(rng.sample(range(8), rng.randrange(9))))
            truth = relation_image(truth, relation)
            current = dag.build(truth)
            depth += 1
            distance += 1
            dag.collect([physical, current, anchor])
            require(dag.words(current) == truth, "GC changed current language")
            require(dag.words(anchor) == anchor_truth, "GC changed anchor language")
            require((current == anchor) == (truth == anchor_truth),
                    "retained canonical equality failed")
            if current == anchor:
                require(anchor_depth < depth, "trivial anchor comparison")
                break
        else:
            raise RuntimeError("no repeat in a 256-element frontier space")
        swept += dag.swept
        cases += 1
    # Explicit stale-ID and retained-equality controls.
    dag = Dag(3)
    old = dag.build({1, 6})
    dag.collect([])
    try:
        dag.words(old)
    except RuntimeError:
        pass
    else:
        raise RuntimeError("a swept ID behaved like an empty graph")
    fresh = dag.build({1, 6})
    require(fresh != old, "dead IDs were reused")
    dag.collect([fresh, fresh])
    require(dag.build({1, 6}) == fresh, "retained language lost canonical ID")
    print(f"PASS abstract boundary GC + Brent: {cases} cases; swept_nodes={swept}")


def recomputation_count(length):
    if length <= 1:
        return 0
    left = length // 2
    return left + recomputation_count(left) + recomputation_count(length - left)


def check_witness(rng):
    cases = images = swept = 0
    for depth in range(1, 65):
        for _ in range(4):
            dag = Dag(3)
            first = [set(rng.sample(range(8), rng.randrange(1, 4))) for _ in range(8)]
            generic = [set(rng.sample(range(8), rng.randrange(1, 4))) for _ in range(8)]
            initial = {rng.randrange(8)}
            frontier = initial.copy()
            for step in range(depth):
                frontier = relation_image(frontier, first if step == 0 else generic)
            target = rng.choice(sorted(frontier))
            physical = dag.build(initial)
            pins, columns = [], [None] * depth
            image_count = 0
            peak_pins = 0

            def collect(extra=()):
                nonlocal peak_pins
                handles = [physical, *pins, *extra]
                peak_pins = max(peak_pins, len(handles))
                dag.collect(handles)

            def recover(a, root_a, b, word_b):
                nonlocal image_count
                pins.append(root_a)
                try:
                    if b == a + 1:
                        relation = first if a == 0 else generic
                        for source in sorted(dag.words(root_a)):
                            if word_b in relation[source]:
                                columns[a] = source, word_b
                                return source
                        raise RuntimeError("valid witness lost its predecessor")
                    middle = (a + b) // 2
                    current = root_a
                    for step in range(a, middle):
                        relation = first if step == 0 else generic
                        current = dag.build(relation_image(dag.words(current), relation))
                        image_count += 1
                        collect([current])
                    word_middle = recover(middle, current, b, word_b)
                    collect()
                    return recover(a, root_a, middle, word_middle)
                finally:
                    require(pins.pop() == root_a, "pin stack mismatch")

            source = recover(0, physical, depth, target)
            require(source in initial, "wrong reconstructed physical source")
            current = source
            for step, edge in enumerate(columns):
                require(edge is not None and edge[0] == current, "disconnected witness")
                relation = first if step == 0 else generic
                require(edge[1] in relation[current], "incorrect phase transition")
                current = edge[1]
            require(current == target, "wrong reconstructed terminal")
            require(image_count == recomputation_count(depth), "wrong image complexity")
            require(peak_pins <= ceil(log2(depth)) + 3, "too many pinned roots")
            cases += 1
            images += image_count
            swept += dag.swept
    print(f"PASS abstract bounded-root witnesses: {cases} cases; images={images}; "
          f"swept_nodes={swept}")


if __name__ == "__main__":
    random_source = random.Random(108_289)
    check_brent()
    check_gc_brent(random_source)
    check_witness(random_source)
    print("ALL ABSTRACT LIVE-MEMORY CHECKS PASSED")
