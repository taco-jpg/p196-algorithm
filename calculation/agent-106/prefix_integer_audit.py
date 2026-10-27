#!/usr/bin/env python3
"""Independent integer and graph audits of Agent 106's prefix projection.

The numeric transition uses ordinary Python integers and decimal string
digits, not the carry recurrence being audited.  SCCs use recursive Tarjan;
component periods use lengths of actual returns, not a distance-residue gcd.
This checks finite prefix abstractions only, not finite B-cycle existence.

  python3 calculation/agent-106/prefix_integer_audit.py
"""

from collections import Counter
from itertools import product
from math import gcd
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prefix_bridge
import prefix_extension


def pair_coefficients(word):
    value = sum(coefficient * 10 ** i for i, coefficient in enumerate(word))
    digits = tuple(int(character) for character in str(value)[::-1])
    paired = tuple(a + b for a, b in zip(digits, digits[::-1]))
    return paired, len(digits) - len(word)


def direct_integer_bridge_audit():
    rng = random.Random(106109)
    overflows = [0, 0]
    empty = short = 0
    for _ in range(20000):
        width = rng.randrange(65)
        exterior = ([rng.randrange(1, 19)] +
                    [rng.randrange(19) for _ in range(width - 1)]
                    if width else [])
        raw, e, gamma = prefix_bridge.raw_exterior(exterior)
        center = [10] if e == 0 else [0]
        band = 3 + rng.randrange(6)
        template = exterior + [9] * band + center + [9] * band + exterior[::-1]
        actual, actual_gamma = pair_coefficients(template)
        assert actual_gamma == gamma
        assert actual[:len(raw)] == tuple(raw)
        assert actual[:3] == tuple((raw + [9] * 3)[:3])
        overflows[gamma] += 1
        empty += width == 0
        short += width < 3
    assert (overflows, empty, short) == ([9203, 10797], 306, 907)
    print("DIRECT_INTEGER_PREFIX_AUDIT PASSED")
    print(f"samples=20000 overflow_counts={overflows} empty_B={empty} "
          f"B_width_lt_3={short} seed=106109")


def integer_graph(width, profile):
    tails = list(product(range(19), repeat=width - 3))
    words = [prefix + tail for prefix in profile for tail in tails]
    index = {word: i for i, word in enumerate(words)}
    adjacency = [[] for _ in words]
    for i, word in enumerate(words):
        phase = i // len(tails)
        next_prefix = profile[(phase + 1) % 8]
        for inward in (0, 1):
            # A central 0 produces carry 0; a central 18 produces carry 1,
            # irrespective of the lower half's outgoing carry bit.
            whole = word + (18 * inward,) + word[::-1]
            paired, gamma = pair_coefficients(whole)
            target = paired[:width]
            if gamma == phase % 2 and target[:3] == next_prefix:
                successor = index[target]
                if successor not in adjacency[i]:
                    adjacency[i].append(successor)
    return adjacency


def tarjan(adjacency):
    sys.setrecursionlimit(max(10000, 4 * len(adjacency)))
    serial = 0
    discovery = [-1] * len(adjacency)
    low = [0] * len(adjacency)
    active = [False] * len(adjacency)
    stack = []
    components = []

    def visit(vertex):
        nonlocal serial
        discovery[vertex] = low[vertex] = serial
        serial += 1
        active[vertex] = True
        stack.append(vertex)
        for successor in adjacency[vertex]:
            if discovery[successor] == -1:
                visit(successor)
                low[vertex] = min(low[vertex], low[successor])
            elif active[successor]:
                low[vertex] = min(low[vertex], discovery[successor])
        if low[vertex] == discovery[vertex]:
            component = set()
            while True:
                member = stack.pop()
                active[member] = False
                component.add(member)
                if member == vertex:
                    break
            components.append(component)

    for vertex in range(len(adjacency)):
        if discovery[vertex] == -1:
            visit(vertex)
    return components


def return_length_period(component, adjacency):
    """Gcd of explicitly observed returns through length 3*|component|.

    For a simple cycle through v, shortest root->v and v->root paths have
    length at most m-1 each.  Their concatenation and the same walk with the
    cycle inserted have lengths <=3m-2.  The gcd of these return lengths
    divides every simple cycle length.  Conversely each recorded return is
    a closed walk.  Thus this finite return-length gcd is the exact period.
    """
    root = min(component)
    frontier = {root}
    answer = 0
    for length in range(1, 3 * len(component) + 1):
        frontier = {successor for vertex in frontier
                    for successor in adjacency[vertex] if successor in component}
        if root in frontier:
            answer = gcd(answer, length)
    assert answer > 0
    return answer


def audit_graph(width):
    profile = list(prefix_bridge.source_skeleton())
    reference = integer_graph(width, profile)
    _, actual, reverse = prefix_extension.graph(width, profile)
    assert len(reference) == len(actual)
    assert all(set(a) == set(b) for a, b in zip(reference, actual))
    independent_components = tarjan(reference)
    membership, actual_components = prefix_extension.strongly_connected(actual, reverse)
    assert {frozenset(c) for c in independent_components} == {
        frozenset(c) for c in actual_components}
    cyclic = [c for c in independent_components
              if len(c) > 1 or min(c) in reference[min(c)]]
    periods = Counter()
    for component in cyclic:
        exact = return_length_period(component, reference)
        root = min(component)
        observed = prefix_extension.component_period(
            actual_components[membership[root]], membership[root], membership, actual)
        assert exact == observed
        periods[exact] += 1
    print(f"INDEPENDENT_PREFIX_GRAPH_AUDIT width={width} vertices={len(reference)} "
          f"edges={sum(map(len, reference))} cyclic_sccs={len(cyclic)} "
          f"cyclic_vertices={sum(map(len, cyclic))} "
          f"period_gcd_histogram={dict(sorted(periods.items()))} "
          f"scc_size_histogram={dict(sorted(Counter(map(len, cyclic)).items()))} PASS")


def main():
    direct_integer_bridge_audit()
    audit_graph(4)
    audit_graph(5)


if __name__ == "__main__":
    main()
