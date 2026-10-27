#!/usr/bin/env python3
"""Independent necessary prefix model for decimal g=(1000)^G exterior cycles.

This implementation derives each transition directly from positional carries.
It does not import another B automaton.  The optional mirror comparison imports
the repository mirror only as a differential oracle for one-step arithmetic.

View a finite exterior B as B followed by infinitely many neutral 9s.  Forward
carries enter at zero.  A reverse carry at the right end of a finite prefix is
either zero or one; both are retained.  Complementary carries on the neutral
tail make its output neutral, so finite trimming cannot change this prefix
representation.  This also covers B shorter than the observed prefix.

One return block contains the four overflow bits 1000.  The one-coefficient
return graph independently forces the recurrent phase-zero coefficient 10,
whose intervening coefficients are 1, 2, 5.  A genuine exterior cycle with G
return blocks must project to a closed walk of length G in every prefix graph.

These are OVERAPPROXIMATIONS: a cyclic prefix need not reach a finite neutral
tail and is not an accepted B cycle, much less a B/C certificate.  In particular
the first four prefix graphs retain period-one SCCs; this computation alone
cannot establish that G must be divisible by three.

Usage, from the repository root:
  python3 calculation/agent-108/independent_saturation.py
  python3 calculation/agent-108/independent_saturation.py --max-width 9
  python3 calculation/agent-108/independent_saturation.py --mirror-width 4
"""

import argparse
from itertools import product
from math import gcd
from pathlib import Path
import sys


def prefix_transition(prefix, boundary_carry):
    """Return (overflow, output prefix) for one chosen reverse boundary carry."""
    reverse_digits = [0] * len(prefix)
    carry = boundary_carry
    for index in range(len(prefix) - 1, -1, -1):
        carry, reverse_digits[index] = divmod(prefix[index] + carry, 10)
    overflow = carry
    forward_digits = []
    carry = 0
    for coefficient in prefix:
        carry, digit = divmod(coefficient + carry, 10)
        forward_digits.append(digit)
    if overflow:
        partner = [1] + reverse_digits[:-1]
    else:
        partner = reverse_digits
    return overflow, tuple(a + b for a, b in zip(forward_digits, partner))


def one_step(prefix, overflow):
    result = set()
    for boundary_carry in (0, 1):
        actual_overflow, successor = prefix_transition(prefix, boundary_carry)
        if actual_overflow == overflow and successor[0] != 0:
            result.add(successor)
    return result


def return_block(prefix, restrict_heads=True):
    frontier = {prefix}
    for overflow, expected_head in zip((1, 0, 0, 0), (1, 2, 5, 10)):
        frontier = {
            target
            for source in frontier
            for target in one_step(source, overflow)
            if not restrict_heads or target[0] == expected_head
        }
    return frontier


def cyclic_components(adjacency):
    """Iterative Kosaraju, returning only components containing a cycle."""
    reverse = {vertex: [] for vertex in adjacency}
    for source, targets in adjacency.items():
        for target in targets:
            reverse[target].append(source)
    seen = set()
    finish = []
    for start in adjacency:
        if start in seen:
            continue
        seen.add(start)
        stack = [(start, iter(adjacency[start]))]
        while stack:
            vertex, iterator = stack[-1]
            target = next(iterator, None)
            if target is None:
                finish.append(vertex)
                stack.pop()
            elif target not in seen:
                seen.add(target)
                stack.append((target, iter(adjacency[target])))
    seen = set()
    result = []
    for start in reversed(finish):
        if start in seen:
            continue
        component = set()
        stack = [start]
        seen.add(start)
        while stack:
            vertex = stack.pop()
            component.add(vertex)
            for target in reverse[vertex]:
                if target not in seen:
                    seen.add(target)
                    stack.append(target)
        if len(component) > 1 or start in adjacency[start]:
            result.append(component)
    return result


def component_period(adjacency, component):
    """GCD of directed cycle lengths in a strongly connected component."""
    start = min(component)
    depth = {start: 0}
    stack = [start]
    while stack:
        source = stack.pop()
        for target in adjacency[source] & component:
            if target not in depth:
                depth[target] = depth[source] + 1
                stack.append(target)
    period = 0
    for source in component:
        for target in adjacency[source] & component:
            period = gcd(period, depth[source] + 1 - depth[target])
    return period


def check_first_coefficient():
    vertices = {(coefficient,) for coefficient in range(1, 19)}
    adjacency = {
        source: return_block(source, restrict_heads=False) & vertices
        for source in vertices
    }
    components = cyclic_components(adjacency)
    if components != [{(10,)}]:
        raise RuntimeError(f"Unexpected first-coordinate components: {components}")
    phase_paths = {((10,),)}
    for overflow in (1, 0, 0, 0):
        phase_paths = {
            path + (target,)
            for path in phase_paths
            for target in one_step(path[-1], overflow)
        }
    closed = {path for path in phase_paths if path[-1] == path[0]}
    if closed != {((10,), (1,), (2,), (5,), (10,))}:
        raise RuntimeError(f"Unexpected scalar return paths: {closed}")
    edges = sum(map(len, adjacency.values()))
    if edges != 11:
        raise RuntimeError(f"Unexpected first-coordinate edge count: {edges}")
    print(f"FIRST_COORDINATE vertices=18 edges={edges} recurrent=10 phases=10,1,2,5")


def mirror_crosscheck(max_width):
    """Exhaust both realizable boundary carries and short-B neutral padding."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror

    boundary_checks = 0
    for width in range(1, max_width + 1):
        for head in range(1, 19):
            for rest in product(range(19), repeat=width - 1):
                prefix = (head,) + rest
                for boundary_carry in (0, 1):
                    # The terminal coefficient 0 or 18 forces the prescribed
                    # reverse carry regardless of the complementary input.
                    exterior = list(prefix) + [18 * boundary_carry]
                    first_carry = mirror.e1(10, exterior)
                    center = [18 if first_carry == 0 else 0]
                    overflow, predicted = prefix_transition(prefix, boundary_carry)
                    actual = tuple(mirror.nextB(10, exterior, center)[:width])
                    if not mirror.hyp(10, exterior, center):
                        raise RuntimeError("Differential test built an invalid source")
                    if overflow != mirror.gam(10, exterior, center) or predicted != actual:
                        raise RuntimeError((prefix, boundary_carry, predicted, actual))
                    boundary_checks += 1

    padding_checks = 0
    observe_width = max_width + 1
    exteriors = [()]
    for width in range(1, max_width + 1):
        exteriors.extend(
            (head,) + rest
            for head in range(1, 19)
            for rest in product(range(19), repeat=width - 1)
        )
    for finite in exteriors:
        exterior = list(finite)
        first_carry = mirror.e1(10, exterior)
        center = [18 if first_carry == 0 else 0]
        prefix = finite + (9,) * (observe_width - len(finite))
        overflow, predicted = prefix_transition(prefix, 1 - first_carry)
        raw = mirror.nextB(10, exterior, center)
        actual = tuple((raw + [9] * observe_width)[:observe_width])
        if overflow != mirror.gam(10, exterior, center) or predicted != actual:
            raise RuntimeError((finite, predicted, actual))
        padding_checks += 1
    print(f"MIRROR_CROSSCHECK boundary={boundary_checks} neutral_padding={padding_checks} PASS")


def prefix_graphs(max_width, vertex_cap):
    recurrent = {(10,)}
    expected = {
        2: (19, 40, [(4, 1)]),
        3: (76, 234, [(25, 1)]),
        4: (475, 1475, [(68, 1)]),
    }
    for width in range(2, max_width + 1):
        # Every closed walk projects to a closed walk of the shorter prefix.
        # Hence extending only recurrent shorter prefixes is a sound pruning.
        required_vertices = 19 * len(recurrent)
        if required_vertices > vertex_cap:
            print(f"UNDECIDED width={width} required_vertices={required_vertices} cap={vertex_cap}")
            return
        vertices = {prefix + (digit,) for prefix in recurrent for digit in range(19)}
        adjacency = {source: return_block(source) & vertices for source in vertices}
        components = cyclic_components(adjacency)
        recurrent = set().union(*components) if components else set()
        details = sorted((len(c), component_period(adjacency, c)) for c in components)
        edges = sum(map(len, adjacency.values()))
        if width in expected and (len(vertices), edges, details) != expected[width]:
            raise RuntimeError(f"Unexpected graph counts at width {width}")
        self_loops = sum(source in adjacency[source] for source in recurrent)
        print(
            f"PREFIX width={width} vertices={len(vertices)} edges={edges} "
            f"recurrent={len(recurrent)} SCC_size_period={details} self_loops={self_loops}",
            flush=True,
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-width", type=int, default=4)
    parser.add_argument("--mirror-width", type=int, default=3)
    parser.add_argument("--vertex-cap", type=int, default=250000)
    args = parser.parse_args()
    if not 2 <= args.max_width <= 20 or not 1 <= args.mirror_width <= 4:
        parser.error("max-width must be 2..20; mirror-width must be 1..4")
    if args.vertex_cap < 1:
        parser.error("vertex-cap must be positive")
    check_first_coefficient()
    mirror_crosscheck(args.mirror_width)
    prefix_graphs(args.max_width, args.vertex_cap)
    print("COMPUTED necessary prefix graph only; no finite-tail or certificate claim")


if __name__ == "__main__":
    main()
