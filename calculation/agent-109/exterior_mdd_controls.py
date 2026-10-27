#!/usr/bin/env python3
"""Arithmetic and known-positive controls for exact exterior MDD preimages.

The exhaustive survivor-set oracle is exterior_graph_audit.py.  This file
checks the local transducer, its boundary cases, and all eight known exterior
cycles independently of the MDD's sink-peeling iteration.  It does not claim
an unrestricted-width exclusion or a decimal B/C certificate.

At width W, the terminal carries identify e=L_W and H_W=1-e.  If g=1,
the raw image has one further coefficient h(1-e)+Y_W.  The terminal guard
Y_W=h*e therefore says exactly that this coefficient is the neutral h.
Thus the MDD relation is raw_B(source)=target++[h]*g, with positive source
head.  For W=0, both outside slots fail the terminal guard, agreeing with
raw_B(())=(b), which cannot be neutrally trimmed to the empty word.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import sys

import exterior_mdd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror


def require(condition, context):
    if not condition:
        raise AssertionError(context)


def integer_image(base, word):
    """Normalize each direction by whole integer arithmetic, then add digits."""
    width = len(word)
    place = tuple(base**k for k in range(width))
    total = sum(x*p for x, p in zip(word, place))
    e = total//base**width
    reverse_total = 1-e+sum(x*p for x, p in zip(reversed(word), place))
    g = reverse_total//base**width
    low = tuple(total//p % base for p in place)
    high = tuple(reverse_total//p % base for p in reversed(place))
    if g:
        low += ((base-1)*(1-e),)
        high = (1,)+high
    return tuple(x+y for x, y in zip(low, high)), e, g


def canonical(base, word):
    end = len(word)
    while end and word[end-1] == base-1:
        end -= 1
    return tuple(word[:end])


def pad(base, word, width):
    return tuple(word)+(base-1,)*(width-len(word))


def slots(base):
    return tuple((g, low, high, pending)
                 for g, low, high in product((0, 1), repeat=3)
                 for pending in (range(base) if g else (0,)))


def literal_column(base, outer, x, high_next):
    """Solve the digit/carry equations by bounded subtraction, not division."""
    g, low, high, pending = outer
    right = x+high_next-base*high
    if not 0 <= right < base:
        return None
    low_solutions = [(ln, x+low-base*ln) for ln in (0, 1)
                     if 0 <= x+low-base*ln < base]
    require(len(low_solutions) == 1, ('unique low carry', base, outer, x))
    low_next, left = low_solutions[0]
    return ((g, low_next, high_next, right if g else 0),
            left+(pending if g else right))


def singleton(dd, word):
    """Build one prescribed word without using any MDD preimage code."""
    require(len(word) == dd.width, ('singleton width', word, dd.width))
    root = 1
    for level in reversed(range(dd.width)):
        children = [0]*dd.arity
        children[word[level]] = root
        root = dd.node(level, children)
    return root


def word_set(dd, words, level=0):
    """Construct the exact finite trie without using preimage or MDD union."""
    if not words:
        return 0
    if level == dd.width:
        return 1
    groups = [[] for _ in range(dd.arity)]
    for word in words:
        groups[word[level]].append(word)
    return dd.node(level, [word_set(dd, group, level+1) for group in groups])


def accepted_words(dd, root):
    """Expand all accepting paths independently of contains() and count()."""
    result = set()
    stack = [(root, ())]
    while stack:
        node, prefix = stack.pop()
        if node == 0:
            continue
        if node == 1:
            require(len(prefix) == dd.width, ('early terminal', prefix))
            result.add(prefix)
            continue
        level, children = dd.nodes[node]
        require(level == len(prefix), ('expansion level', level, prefix))
        stack.extend((child, prefix+(digit,)) for digit, child in enumerate(children)
                     if child)
    return result


def collect_checked(dd, root, expected, stats):
    """Discard every old ID; verify the retained language and fresh arena."""
    reachable = dd.reachable_nodes(root)
    started = dd.started
    peaks = dd.peak_nodes, dd.peak_cache
    new_root = dd.collect(root)
    require(dd.started == started and (dd.peak_nodes, dd.peak_cache) == peaks,
            ('collection changed budget history', dd.base, dd.width))
    require(not dd.pre_cache and not dd.union_cache and dd.count_cache == {0: 0, 1: 1},
            ('collection cache reset', dd.base, dd.width))
    require(len(dd.nodes)-2 == reachable == dd.reachable_nodes(new_root),
            ('collection retained unreachable nodes', dd.base, dd.width))
    require(dd.unique == {node: i for i, node in enumerate(dd.nodes) if i >= 2},
            ('collection unique table', dd.base, dd.width))
    for i, (level, children) in enumerate(dd.nodes[2:], start=2):
        require(len(children) == dd.arity and any(children),
                ('collection node shape', dd.base, dd.width, i))
        require(all(0 <= child < i for child in children),
                ('collection topological IDs', dd.base, dd.width, i))
        require(all((child == 0 or (child == 1 and level == dd.width-1)
                     or (child >= 2 and dd.nodes[child][0] == level+1))
                    for child in children),
                ('collection level preservation', dd.base, dd.width, i))
    require(accepted_words(dd, new_root) == expected,
            ('collection complete language', dd.base, dd.width))
    stats['complete_set_gc_controls'] += 1
    return new_root


def check_cut_tables(stats):
    """Compare every supported-base column to literal bounded digit equations."""
    for base in range(2, 63):
        options = set()
        alphabet = set(slots(base))
        for outer in alphabet:
            for x, high_next in product(range(2*base-1), (0, 1)):
                result = exterior_mdd.cut_step(base, outer, x, high_next)
                expected = literal_column(base, outer, x, high_next)
                stats['cut_step_inputs'] += 1
                require(result == expected,
                        ('literal local equality', base, outer, x, high_next,
                         result, expected))
                if result is None:
                    continue
                inner, output = result
                require(inner in alphabet, ('inner slot alphabet', base, inner))
                require(0 <= output <= 2*(base-1),
                        ('output coefficient range', base, outer, x, output))
                options.add((outer, inner, x, output))
        stats['local_table_options'] += len(options)
        stats['supported_bases'] += 1
    print('EXACT_LOCAL_TABLE_EQUALITY bases2..62',
          'inputs', stats['cut_step_inputs'], 'options', stats['local_table_options'])


def check_boundaries(stats):
    for base in range(2, 63):
        h = base-1
        empty = exterior_mdd.MDD(base, 0)
        full = empty.full()
        require(full == 1 and empty.count(full) == 1 and empty.contains(full, ()),
                ('width-zero initial universe', base))
        require(empty.preimage(full) == 0, ('width-zero preimage', base))
        require(integer_image(base, ()) == ((base,), 0, 1),
                ('width-zero integer image', base))
        stats['empty_width_controls'] += 1

        # Each fixture uses a target singleton, rather than the full universe.
        fixtures = (
            ((h,), (base,), True),          # carry at x+h_next=b
            ((2*h,), (h,), False),          # overflow has a nonneutral last digit
            ((2*h, h), (h, base-2), True),  # maximum source coefficient
            ((h, 0), (2*h, 1), True),       # maximum target coefficient
            ((0,), (1,), False),            # positive physical head is mandatory
            ((0, h), (1, h), False),
        )
        for source, target, expected in fixtures:
            raw, e, overflow = integer_image(base, source)
            center = [2*h] if e == 0 else [0]
            require(tuple(mirror.nextB(base, list(source), center)) == raw,
                    ('boundary mirror equality', base, source))
            semantic = bool(source and source[0] > 0
                            and raw == target+(h,)*overflow)
            require(semantic == expected,
                    ('boundary fixture arithmetic', base, source, target, raw))
            dd = exterior_mdd.MDD(base, len(source))
            target_root = singleton(dd, target)
            preimage = dd.preimage(target_root)
            require(dd.contains(preimage, source) == expected,
                    ('boundary fixture preimage', base, source, target, expected))
            stats['boundary_singleton_controls'] += 1
    print('BOUNDARIES bases2..62', 'width0', stats['empty_width_controls'],
          'singleton_fixtures', stats['boundary_singleton_controls'])


def check_known_cycles(stats):
    rows = []
    for base, edges in mirror._lean_certs():
        require(mirror.cycleOK(base, edges, *edges[0][:2]),
                ('known certificate mirror', base))
        cores = [canonical(base, edge[0]) for edge in edges]
        width = max(map(len, cores))
        words = [pad(base, core, width) for core in cores]
        dd = exterior_mdd.MDD(base, width)
        target_set = 0
        singletons = {}
        for word in set(words):
            singletons[word] = singleton(dd, word)
            target_set = dd.union(target_set, singletons[word])
        require(dd.count(target_set) == len(set(words)),
                ('known word-set construction', base))
        set_preimage = dd.preimage(target_set)
        for t, source in enumerate(words):
            target = words[(t+1) % len(words)]
            raw, _, overflow = integer_image(base, source)
            require(source[0] > 0 and raw == target+(base-1,)*overflow,
                    ('known fixed-width integer edge', base, t, source, target))
            require(dd.contains(dd.preimage(singletons[target]), source),
                    ('known singleton preimage', base, t))
            require(dd.contains(set_preimage, source),
                    ('known invariant subset', base, t))
            stats['known_singleton_preimage_edges'] += 1
        stats['known_invariant_subsets'] += 1
        rows.append((base, width, len(edges), len(set(words))))
        print('KNOWN_POSITIVE_INVARIANT_SUBSET',
              'base', base, 'width', width, 'edges', len(edges),
              'distinct_words', len(set(words)), 'preimage_words', dd.count(set_preimage))
    require(sorted(row[0] for row in rows) == [2, 4, 8, 11, 16, 17, 26, 32],
            'all eight known positive controls required')


def check_correlated_targets(stats):
    cases = ((2, 4), (3, 3), (4, 3), (5, 3), (10, 3),
             (11, 2), (17, 2), (26, 2), (32, 2))
    predicates = (
        ('empty', lambda w, h: False),
        ('diagonal', lambda w, h: w[0] == w[-1]),
        ('antidiagonal', lambda w, h: w[0]+w[-1] == 2*h),
        ('weighted_mod7', lambda w, h: sum((k+1)*x for k, x in enumerate(w)) % 7 == 3),
        ('alternating_mod5', lambda w, h: (sum(w[::2])-sum(w[1::2])) % 5 in (1, 4)),
        ('end_parity_xor', lambda w, h: w[0] % 2 != w[-1] % 2),
        ('two_fibres', lambda w, h: (w[0] == 1 and w[-1] in (0, 2*h))
                                  or (w[0] == 2*h and w[-1] == h)),
    )
    for base, width in cases:
        h = base-1
        universe = tuple((head,)+rest for head in range(1, 2*base-1)
                         for rest in product(range(2*base-1), repeat=width-1))
        images = {}
        for word in universe:
            raw, e, g = integer_image(base, word)
            center = [2*h] if e == 0 else [0]
            require(tuple(mirror.nextB(base, list(word), center)) == raw,
                    ('correlated integer/mirror equality', base, word))
            if not g or raw[-1] == h:
                images[word] = raw[:-1] if g else raw
        for name, predicate in predicates:
            target = {word for word in universe if predicate(word, h)}
            expected = {source for source, image in images.items() if image in target}
            dd = exterior_mdd.MDD(base, width)
            target_root = word_set(dd, target)
            require(accepted_words(dd, target_root) == target,
                    ('target construction', base, width, name))
            preimage = dd.preimage(target_root)
            actual = accepted_words(dd, preimage)
            require(actual == expected,
                    ('complete correlated preimage', base, width, name,
                     sorted(actual-expected)[:1], sorted(expected-actual)[:1]))
            require(dd.count(preimage) == len(expected),
                    ('correlated preimage count', base, width, name))
            # Retain the original correlated target, discard all cached IDs,
            # and compute its preimage again in the new arena.
            target_root = collect_checked(dd, target_root, target, stats)
            preimage = dd.preimage(target_root)
            require(accepted_words(dd, preimage) == expected,
                    ('correlated preimage after target collection', base, width, name))
            # Now retain that preimage and independently check the next one.
            preimage = collect_checked(dd, preimage, expected, stats)
            second_expected = {source for source, image in images.items() if image in expected}
            second_actual = accepted_words(dd, dd.preimage(preimage))
            require(second_actual == second_expected,
                    ('second preimage after collection', base, width, name))
            stats['correlated_target_sets'] += 1
            stats['correlated_source_memberships'] += len(universe)
        stats['integer_mirror_source_images'] += len(universe)
        print('COMPLETE_CORRELATED_PREIMAGES', 'base', base, 'width', width,
              'source_words', len(universe), 'target_sets', len(predicates))


def main():
    stats = Counter()
    check_cut_tables(stats)
    check_boundaries(stats)
    check_known_cycles(stats)
    check_correlated_targets(stats)
    print('COUNTS', dict(sorted(stats.items())))
    print('ALL EXTERIOR MDD ARITHMETIC CONTROLS PASSED')


if __name__ == '__main__':
    main()
