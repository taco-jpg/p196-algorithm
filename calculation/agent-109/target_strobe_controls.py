#!/usr/bin/env python3
"""Independent arithmetic and correlated-set controls for target_strobe_mdd.

Replay the prescribed center using whole integers and the exact mirror;
check fixed-phase preimages, shared-arena caches, multi-root collection, and
known nondecimal drivers.  These finite controls assert no decimal B cycle.
The complete stroboscopic survivor oracle is owned by a separate script.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import sys

import target_strobe_mdd as primary

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror


E = '010100110100101011001011'
G = '110001001000110001001000'
V = '100001000000100001000000'
C0 = (9, 14, 13, 18, 13, 14, 9)


def require(condition, context):
    if not condition:
        raise AssertionError(context)


def value(base, word):
    return sum(x*base**k for k, x in enumerate(word))


def normalize_integer(base, word, carry):
    width = len(word)
    total = value(base, word)+carry
    return tuple(total//base**k % base for k in range(width)), total//base**width


def exterior_image(base, word):
    low, e = normalize_integer(base, word, 0)
    rev, g = normalize_integer(base, tuple(reversed(word)), 1-e)
    high = tuple(reversed(rev))
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


def replay_center(stats):
    require((primary.E, primary.G, primary.V, tuple(primary.C0)) == (E, G, V, C0),
            'primary target constants differ')
    base, h = 10, 9
    center = C0
    rows = []
    witnesses = {(0, 0): (1, 0), (0, 1): (h,),
                 (1, 0): (1, 0, base), (1, 1): (base,)}
    for t, (e, g, trim) in enumerate(zip(map(int, E), map(int, G), map(int, V))):
        width = len(center)
        digits, end = normalize_integer(base, center, e)
        require(end == 1-e, ('center complementary carry', t, center, e, end))
        require(center == center[::-1], ('center symmetry', t, center))
        left, right = digits, digits[::-1]
        if g:
            left, right = left+(h*e,), (h*e,)+right
        raw = tuple(x+y for x, y in zip(left, right))
        require(len(raw) >= 2*trim and raw[:trim] == (h,)*trim
                and raw[len(raw)-trim:] == (h,)*trim,
                ('center prescribed neutral trim', t, raw, trim))
        target = raw[trim:len(raw)-trim] if trim else raw
        witness = witnesses[(e, g)]
        require(mirror.hyp(base, list(witness), list(center)), ('center mirror Hyp', t))
        require((mirror.e1(base, list(witness)),
                 mirror.gam(base, list(witness), list(center))) == (e, g),
                ('center mirror driver', t))
        require(tuple(mirror.nextC(base, list(witness), list(center))) == raw,
                ('center mirror update', t))
        normalized_value = value(base, center)+e-(1-e)*base**width
        require(normalized_value == value(base, digits), ('normalized center value', t))
        reverse_value = value(base, digits[::-1])
        numeric_raw = (normalized_value+reverse_value if not g else
                       normalized_value+base*reverse_value+h*e*(base**width+1))
        require(numeric_raw == value(base, raw), ('ordinary-integer center update', t))
        removed = (base**trim-1)*(1+base**(len(raw)-trim))
        require(numeric_raw == removed+base**trim*value(base, target),
                ('ordinary-integer center trim', t))
        rows.append((t, e, g, trim, center, target))
        print('CENTER_PHASE', t, 'e', e, 'g', g, 'v', trim,
              'C', list(center), 'Cnext', list(target), 'integer', value(base, center))
        center = target
        stats['center_integer_mirror_edges'] += 1
    require(len(rows) == 24 and center == C0, ('center full-lap closure', center))
    require(sum(map(int, G)) == 2*sum(map(int, V)) == 8,
            'center length accounting')
    print('CENTER_CLOSED', 'period', len(rows), 'overflow_sum', 8, 'trim_sum', 4)
    return rows


def word_set(dd, words, level=0):
    if not words:
        return 0
    if level == dd.width:
        return 1
    groups = [[] for _ in range(dd.arity)]
    for word in words:
        groups[word[level]].append(word)
    return dd.node(level, [word_set(dd, group, level+1) for group in groups])


def accepted_words(dd, root):
    result = set()
    stack = [(root, ())]
    while stack:
        node, prefix = stack.pop()
        if node == 0:
            continue
        if node == 1:
            require(len(prefix) == dd.width, ('terminal level', prefix))
            result.add(prefix)
            continue
        level, children = dd.nodes[node]
        require(level == len(prefix), ('expanded node level', level, prefix))
        stack.extend((child, prefix+(digit,)) for digit, child in enumerate(children) if child)
    return result


def collect_checked(dd, roots, languages, stats):
    roots = tuple(roots)
    require(len(roots) == len(languages), 'retained language count')
    seen = set()
    stack = list(roots)
    while stack:
        node = stack.pop()
        if node < 2 or node in seen:
            continue
        seen.add(node)
        stack.extend(dd.nodes[node][1])
    started, peaks = dd.started, (dd.peak_nodes, dd.peak_cache)
    equality = tuple(a == b for a in roots for b in roots)
    remapped = dd.collect_many(roots)
    require(len(remapped) == len(roots), 'collection root count')
    require(tuple(a == b for a in remapped for b in remapped) == equality,
            'collection equality/duplicate preservation')
    require(dd.started == started and (dd.peak_nodes, dd.peak_cache) == peaks,
            'collection budget history')
    require(not dd.pre_cache and not dd.union_cache and dd.count_cache == {0: 0, 1: 1},
            'collection clears every identifier cache')
    require(len(dd.nodes)-2 == len(seen), 'collection joint reachable-node count')
    require(dd.unique == {node: i for i, node in enumerate(dd.nodes) if i >= 2},
            'collection unique table')
    for i, (level, children) in enumerate(dd.nodes[2:], start=2):
        require(len(children) == dd.arity and any(children)
                and all(0 <= child < i for child in children), ('collection topology', i))
        require(all(child == 0 or (child == 1 and level == dd.width-1)
                    or (child >= 2 and dd.nodes[child][0] == level+1) for child in children),
                ('collection preserved levels', i))
    for root, language in zip(remapped, languages):
        require(accepted_words(dd, root) == language, 'collection complete accepted language')
        stats['retained_root_language_checks'] += 1
    stats['collect_many_controls'] += 1
    return remapped


def fixed_images(base, width):
    words = tuple((head,)+rest for head in range(1, 2*base-1)
                  for rest in product(range(2*base-1), repeat=width-1))
    maps = {(e, g): {} for e, g in product((0, 1), repeat=2)}
    for word in words:
        raw, e, g = exterior_image(base, word)
        center = [2*(base-1)] if e == 0 else [0]
        require(tuple(mirror.nextB(base, list(word), center)) == raw,
                ('whole-integer/mirror exterior', base, word))
        require(mirror.e1(base, list(word)) == e
                and mirror.gam(base, list(word), center) == g,
                ('whole-integer/mirror exterior bits', base, word))
        if not g or raw[-1] == base-1:
            maps[(e, g)][word] = raw[:-1] if g else raw
    return words, maps


def correlated_phase_controls(stats):
    cases = ((2, 4), (3, 3), (4, 3), (5, 3), (10, 3),
             (11, 2), (17, 2), (26, 2), (32, 2))
    predicates = (
        ('empty', lambda w, h: False),
        ('diagonal', lambda w, h: w[0] == w[-1]),
        ('antidiagonal', lambda w, h: w[0]+w[-1] == 2*h),
        ('weighted_mod7', lambda w, h: sum((i+1)*x for i, x in enumerate(w)) % 7 == 3),
        ('alternating_mod5', lambda w, h: (sum(w[::2])-sum(w[1::2])) % 5 in (1, 4)),
        ('end_parity_xor', lambda w, h: w[0] % 2 != w[-1] % 2),
    )
    for base, width in cases:
        words, maps = fixed_images(base, width)
        stats['integer_mirror_exterior_words'] += len(words)
        for name, predicate in predicates:
            target = {word for word in words if predicate(word, base-1)}
            expected = [{source for source, image in maps[bits].items() if image in target}
                        for bits in product((0, 1), repeat=2)]
            dd = primary.StrobeMDD(base, width)
            root = word_set(dd, target)
            roots = [dd.phase_preimage(root, e, g) for e, g in product((0, 1), repeat=2)]
            for phase, image, truth in zip(product((0, 1), repeat=2), roots, expected):
                require(accepted_words(dd, image) == truth,
                        ('complete fixed-phase preimage', base, width, name, phase))
                require(dd.count(image) == len(truth), ('fixed-phase count', base, name, phase))
                stats['correlated_phase_preimages'] += 1
                stats['correlated_source_memberships'] += len(words)
            # Keep the checkpoint, every phase result, zero, and a duplicate.
            retained = collect_checked(dd, (root, *roots, 0, root),
                                       (target, *expected, set(), target), stats)
            root, roots = retained[0], retained[1:5]
            for index in reversed(range(4)):
                e, g = tuple(product((0, 1), repeat=2))[index]
                require(dd.phase_preimage(root, e, g) == roots[index],
                        ('phase preimage after multi-root collection', base, name, e, g))
            stats['correlated_target_sets'] += 1
        print('COMPLETE_FIXED_PHASE_PREIMAGES', 'base', base, 'width', width,
              'source_words', len(words), 'targets', len(predicates), 'phases', 4)


def zero_width_controls(stats):
    for base in range(2, 63):
        dd = primary.StrobeMDD(base, 0)
        full = dd.full()
        for e, g in product((0, 1), repeat=2):
            require(dd.phase_preimage(full, e, g) == 0, ('empty-word phase', base, e, g))
            stats['zero_width_phase_controls'] += 1
        roots = collect_checked(dd, (full, 0, full), ({()}, set(), {()}), stats)
        require(roots == (1, 0, 1), ('empty-width retained roots', base))


def known_driver_controls(stats):
    for base, edges in mirror._lean_certs():
        require(mirror.cycleOK(base, edges, *edges[0][:2]), ('known cycle mirror', base))
        cores = [canonical(base, edge[0]) for edge in edges]
        width = max(map(len, cores))
        words = [pad(base, word, width) for word in cores]
        es, gs = [], []
        for t, source in enumerate(words):
            target = words[(t+1) % len(words)]
            raw, e, g = exterior_image(base, source)
            require(raw == target+(base-1,)*g, ('known padded exterior edge', base, t))
            dd = primary.StrobeMDD(base, width)
            root = word_set(dd, {target})
            require(dd.contains(dd.phase_preimage(root, e, g), source),
                    ('known fixed-phase positive', base, t))
            for wrong_e, wrong_g in product((0, 1), repeat=2):
                if (wrong_e, wrong_g) != (e, g):
                    require(not dd.contains(dd.phase_preimage(root, wrong_e, wrong_g), source),
                            ('known wrong-driver rejection', base, t, wrong_e, wrong_g))
                    stats['known_wrong_phase_rejections'] += 1
            es.append(e); gs.append(g)
            stats['known_fixed_phase_edges'] += 1
        print('KNOWN_FIXED_DRIVER', 'base', base, 'width', width, 'period', len(edges))
        if base not in (2, 4, 8, 16, 32):
            continue
        universe, maps = fixed_images(base, width)
        def explicit_preimage(target, repetitions):
            for _ in range(repetitions):
                for e, g in reversed(tuple(zip(es, gs))):
                    target = {source for source, image in maps[(e, g)].items() if image in target}
            return target
        for repetitions in (1, 2, 3):
            target = {words[0]}
            expected = explicit_preimage(target, repetitions)
            results = []
            for collect in (False, True):
                dd = primary.StrobeMDD(base, width)
                root = word_set(dd, target)
                old, image = dd.lap_preimage(root, es*repetitions, gs*repetitions, collect=collect)
                require(accepted_words(dd, old) == target, ('lap checkpoint retained', base, repetitions))
                actual = accepted_words(dd, image)
                require(actual == expected and words[0] in actual,
                        ('known repeated-lap complete preimage', base, repetitions, collect))
                results.append(actual)
                stats['known_repeated_lap_controls'] += 1
            require(results[0] == results[1], ('lap collection comparison', base, repetitions))


def main():
    stats = Counter()
    replay_center(stats)
    zero_width_controls(stats)
    correlated_phase_controls(stats)
    known_driver_controls(stats)
    print('COUNTS', dict(sorted(stats.items())))
    print('ALL TARGET STROBE CONTROLS PASSED')


if __name__ == '__main__':
    main()
