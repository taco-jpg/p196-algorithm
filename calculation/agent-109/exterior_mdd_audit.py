#!/usr/bin/env python3
"""Independent complete-set audit of exterior_mdd.py.

Builds the finite fixed-width exterior map from the established mirror's
directional normalizations, retaining exactly u=g neutral suffix trims.
Then explicitly peels sets of integer-encoded words.  At every round,
independently expands every accepting MDD digit path and compares the
ENTIRE represented set, before separately checking the reported count.

This validates finite computations only.  It does not prove the general
MDD recurrence, and positive controls are B-side exteriors, not new B/C
certificates.  Dependencies: exterior_mdd.py and neutral_band_search.py.
"""
from array import array
import argparse
import json
from pathlib import Path
import sys
from time import perf_counter

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror
import exterior_mdd


def encode(word, radix):
    value = 0
    for coefficient in word:
        value = radix*value + coefficient
    return value


def decode(value, radix):
    coefficients = []
    while value:
        value, coefficient = divmod(value, radix)
        coefficients.append(coefficient)
    return tuple(reversed(coefficients))


def successor_word(base, word):
    """Whole-word normalizations, independent of the MDD column relation."""
    low, e = mirror.norm(base, word, 0)
    reflected, g = mirror.norm(base, word[::-1], 1-e)
    reflected.reverse()
    if g:
        low.append((base-1)*(1-e))
        reflected.insert(0, 1)
    assert len(low) == len(reflected)
    return tuple(x+y for x, y in zip(low, reflected)), g


def fixed_map(base, width, state_cap=2600000):
    """All positive-head words of length W; at W=0 use the empty word."""
    radix = 2*base-1
    first, limit = ((0, 1) if width == 0 else
                    (radix**(width-1), radix**width))
    count = limit-first
    if count > state_cap or count >= 2**31:
        raise RuntimeError(f'{count} fixed states exceed cap {state_cap}')
    successor = array('i', [-1])*count
    for source in range(first, limit):
        word = decode(source, radix)
        assert len(word) == width and (not word or word[0] > 0)
        raw, g = successor_word(base, word)
        assert len(raw) == width+g
        if g and raw[-1] != base-1:
            continue
        target = raw[:width]
        if target and target[0] == 0:
            continue
        target_index = encode(target, radix)-first
        assert 0 <= target_index < count
        successor[source-first] = target_index
    return first, successor


def surviving_sets(first, successor, max_rounds=1000):
    """S0 is the full finite domain; successively remove dead futures."""
    current = set(range(first, first+len(successor)))
    yield 0, current, 'initial'
    for iteration in range(1, max_rounds+1):
        following = {source for source in current
                     if successor[source-first] >= 0
                     and first+successor[source-first] in current}
        status = ('empty' if not following else
                  'fixed' if following == current else 'shrinking')
        yield iteration, following, status
        if status in ('empty', 'fixed'):
            return
        current = following
    raise RuntimeError(f'peeling exceeds {max_rounds} rounds')


def expand_mdd_words(diagram, root):
    """Interpret digit-labelled paths without using MDD count/contains."""
    words = set()

    def visit(node, level, value):
        if node == 0:
            return
        if node == 1:
            assert level == diagram.width
            words.add(value)
            return
        actual_level, children = diagram.nodes[node]
        assert actual_level == level and len(children) == diagram.arity
        for coefficient, child in enumerate(children):
            if child:
                visit(child, level+1, diagram.arity*value+coefficient)

    visit(root, 0, 0)
    return words


def audit(base, width, state_cap=2600000):
    started = perf_counter()
    first, successor = fixed_map(base, width, state_cap)
    diagram = exterior_mdd.MDD(base, width)
    root = diagram.full()
    counts = []
    for iteration, survivors, status in surviving_sets(first, successor):
        counts.append(len(survivors))
        represented = expand_mdd_words(diagram, root)
        assert represented == survivors, (
            base, width, iteration,
            'extra', sorted(represented-survivors)[:8],
            'missing', sorted(survivors-represented)[:8])
        assert diagram.count(root) == len(survivors)
        if status == 'empty':
            assert root == 0
        elif status == 'fixed':
            assert diagram.preimage(root) == root
        else:
            root = diagram.preimage(root)
    result = {'base': base, 'width': width, 'counts': counts,
              'status': status, 'round': iteration,
              'full_set_comparisons': len(counts), 'comparison': 'PASS',
              'seconds': round(perf_counter()-started, 3)}
    if status == 'empty':
        result['maximum_valid_steps'] = iteration-1
    else:
        # The final repeated set is retained to test equality explicitly.
        result['first_fixed_iteration'] = iteration-1
    print('FULL_SET_AUDIT', json.dumps(result, separators=(',', ':')), flush=True)
    return result, survivors


def positive_controls():
    """Known power-of-two B cycles padded uniformly to length two."""
    known = {2: ((2, 1), (1, 0)),
             4: ((4, 3), (1, 0), (2, 1))}
    for base, cycle in known.items():
        result, survivors = audit(base, 2)
        assert result['status'] == 'fixed'
        for j, word in enumerate(cycle):
            target = cycle[(j+1) % len(cycle)]
            raw, g = successor_word(base, word)
            assert raw == target+(base-1,)*g
            assert encode(word, 2*base-1) in survivors
        print('KNOWN_POSITIVE', json.dumps({
            'base': base, 'width': 2, 'period': len(cycle),
            'cycle': cycle, 'surviving_words': len(survivors)
        }, separators=(',', ':')), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bases', type=int, nargs='+', default=[10])
    parser.add_argument('--max-width', type=int, default=4)
    parser.add_argument('--state-cap', type=int, default=2600000)
    parser.add_argument('--positive-controls', action='store_true')
    args = parser.parse_args()
    if (any(not 2 <= b <= 62 for b in args.bases)
            or args.max_width < 0 or args.state_cap < 1):
        parser.error('bases in2..62, max-width>=0, and positive state-cap required')
    try:
        comparisons = 0
        for base in args.bases:
            for width in range(args.max_width+1):
                result, _ = audit(base, width, args.state_cap)
                comparisons += result['full_set_comparisons']
        if args.positive_controls:
            positive_controls()
        print(f'ALL FULL-SET AUDITS PASSED comparisons={comparisons}; '
              'FINITE VALIDATION ONLY')
    except (MemoryError, RuntimeError) as error:
        print(f'UNDECIDED: {error}', flush=True)
        raise SystemExit(2)


if __name__ == '__main__':
    main()
