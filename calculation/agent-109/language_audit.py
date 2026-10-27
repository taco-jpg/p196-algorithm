#!/usr/bin/env python3
"""Independent bounded audit of neutral_language.py.

Uses exhaustive integer Tile enumeration, a separate Tarjan SCC routine,
tuple-valued raw product states, and no quotient in the reference iteration.
Periodic-word tests allow any hidden-state period multiple, as required by
the all-temporal-period language interpretation. No infinite-depth claim.
"""
from collections import defaultdict
from itertools import product
from random import Random
import argparse
import sys

import neutral_language as candidate

sys.setrecursionlimit(20000)
SLOTS = tuple(product((0, 1), (0, 1), (0, 1), range(-1, 10)))
OUTSIDE = (0, 0, 0, 0)
NEUTRAL = frozenset((a, b, 1-a, 10*b-1) for a, b in product((0, 1), repeat=2))


def independent_tiles():
    """Enumerate both full slot tuples before testing column coefficients."""
    result = set()
    for inner in SLOTS:
        ia, ib, ic, iz = inner
        for outer in SLOTS:
            oa, ob, oc, oz = outer
            for e in (0, 1):
                r = iz + 10*e
                if not 0 <= r <= 18 or not 0 <= oz+e <= 9:
                    continue
                if r < 9 and e != 0 or r > 9 and e != 1:
                    continue
                qn = (r+ob) % 10 + oz + e
                if not 0 <= qn <= 18 or (r+ob)//10 != ib:
                    continue
                for q in range(19):
                    if ((q+oa)//10 == ia and (q+ic)//10 == oc
                            and (q+oa) % 10 + (q+ic) % 10 == r):
                        result.add((outer, inner, q, r, e, qn))
    return result


def tarjan(vertices, edges):
    """Reference SCCs: one-pass Tarjan, unlike candidate Kosaraju."""
    adjacency = defaultdict(list)
    for source, _, target in edges:
        adjacency[source].append(target)
    discovered, low, active, stack, component = {}, {}, set(), [], {}
    next_index = 0
    next_component = 0

    def visit(u):
        nonlocal next_index, next_component
        discovered[u] = low[u] = next_index
        next_index += 1
        active.add(u)
        stack.append(u)
        for v in adjacency[u]:
            if v not in discovered:
                visit(v)
                low[u] = min(low[u], low[v])
            elif v in active:
                low[u] = min(low[u], discovered[v])
        if low[u] == discovered[u]:
            while True:
                v = stack.pop()
                active.remove(v)
                component[v] = next_component
                if v == u:
                    break
            next_component += 1

    for vertex in vertices:
        if vertex not in discovered:
            visit(vertex)
    return component


def prune(edges):
    vertices = {s for s, _, _ in edges} | {t for _, _, t in edges}
    component = tarjan(vertices, edges)
    return {(s, a, t) for s, a, t in edges if component[s] == component[t]}


def reference_predecessor(edges, by_inner):
    raw = set()
    for source, inner, target in edges:
        for outer, q, qn in by_inner[inner]:
            raw.add((source+(q,), outer, target+(qn,)))
    return prune(raw)


def periodic_trace(edges, word):
    """A cycle in the graph times the prescribed label phase."""
    by_letter = defaultdict(list)
    for source, label, target in edges:
        by_letter[label].append((source, target))
    constrained = set()
    for phase, label in enumerate(word):
        for source, target in by_letter[label]:
            constrained.add(((source, phase), label,
                             (target, (phase+1) % len(word))))
    return bool(prune(constrained))


def words_to_check():
    words = {(slot,) for slot in SLOTS}
    for length in range(2, 4):
        words.update(product(sorted(NEUTRAL), repeat=length))
    for length in range(1, 5):
        for a in product((0, 1), repeat=length):
            words.add(tuple((a[j], 1-a[(j+1) % length],
                             1-a[j], 9-10*a[(j+1) % length])
                            for j in range(length)))
    rng = Random(109289)
    for _ in range(96):
        words.add(tuple(rng.choice(SLOTS) for _ in range(rng.randrange(2, 6))))
    return sorted(words)


def candidate_as_tuples(edges):
    return {((s,), candidate.SLOTS[a], (t,)) for s, a, t in edges}


def reference_product_numbered(edges, by_inner):
    raw = reference_predecessor(candidate_as_tuples(edges), by_inner)
    used = sorted({s for s, _, _ in raw} | {t for _, _, t in raw})
    ids = {s: j for j, s in enumerate(used)}
    return len(used), sorted((ids[s], candidate.INDEX[a], ids[t])
                            for s, a, t in raw)


def cyclic_core_controls():
    rng = Random(109)
    for n in range(1, 31):
        for _ in range(4):
            edges = {(rng.randrange(n), rng.randrange(4), rng.randrange(n))
                     for _ in range(2*n)}
            kept = prune(edges)
            used = sorted({s for s, _, _ in kept} | {t for _, _, t in kept})
            ids = {s: j for j, s in enumerate(used)}
            expected = (len(used), sorted((ids[s], a, ids[t]) for s, a, t in kept))
            assert candidate.cyclic_core(n, edges) == expected
    print('CYCLIC_CORE_CONTROLS cases=120 PASS')


def audit(depth):
    table = independent_tiles()
    projected = {(inner, q, outer, qn) for outer, inner, q, _, _, qn in table}
    expected = {(candidate.SLOTS[inner], q, candidate.SLOTS[outer], qn)
                for (inner, q), options in candidate.TILES.items()
                for outer, qn in options}
    assert projected == expected
    print(f'TILE_ENUMERATION full_rows={len(table)} projected_rows={len(projected)} PASS')
    by_inner = defaultdict(set)
    for outer, inner, q, _, _, qn in table:
        by_inner[inner].add((outer, q, qn))
    cyclic_core_controls()
    patterns = words_to_check()
    total_checks = 0
    compact_checks = 0
    for flip in (False, True):
        if flip:
            reference = {((a,), (a, 1-aa, 1-a, 9-10*aa), (aa,))
                         for a, aa in product((0, 1), repeat=2)}
            n = 2
            edges = [(a, candidate.INDEX[label], aa)
                     for (a,), label, (aa,) in reference]
        else:
            reference = {((), slot, ()) for slot in NEUTRAL}
            n = 1
            edges = [(0, candidate.INDEX[slot], 0) for slot in sorted(NEUTRAL)]
        for d in range(depth+1):
            compressed = candidate_as_tuples(edges)
            accepted = 0
            for word in patterns:
                raw_answer = periodic_trace(reference, word)
                quotient_answer = periodic_trace(compressed, word)
                assert raw_answer == quotient_answer, (flip, d, word)
                accepted += int(raw_answer)
                total_checks += 1
            raw_outside = periodic_trace(reference, (OUTSIDE,))
            assert raw_outside == candidate.uniform_cycle(n, edges, candidate.OUTSIDE)
            raw_vertices = {s for s, _, _ in reference} | {t for _, _, t in reference}
            print(f'LANGUAGE mode={"flip" if flip else "free"} depth={d} '
                  f'raw_states={len(raw_vertices)} raw_edges={len(reference)} '
                  f'quotient_states={n} quotient_edges={len(edges)} '
                  f'patterns={len(patterns)} accepted={accepted} outside={raw_outside}', flush=True)
            if d < depth:
                reference = reference_predecessor(reference, by_inner)
                independently_numbered = reference_product_numbered(edges, by_inner)
                ordinary_product = candidate.predecessor(n, edges)
                compact_product = candidate.predecessor_compact(n, edges)
                assert independently_numbered == ordinary_product == compact_product
                compact_checks += 1
                n, edges = ordinary_product
                n, edges = candidate.bisimulation(n, edges)
    print(f'PERIODIC_PATTERN_COMPARISONS checks={total_checks} PASS')
    print(f'INDEPENDENT_PRODUCT_COMPACT_COMPARISONS checks={compact_checks} PASS')
    print('ALL LANGUAGE AUDIT CHECKS PASSED; NO INFINITE-DEPTH CONCLUSION')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--depth', type=int, default=5)
    args = parser.parse_args()
    if not 0 <= args.depth <= 5:
        parser.error('depth must lie in 0..5 for this bounded validation')
    audit(args.depth)


if __name__ == '__main__':
    main()
