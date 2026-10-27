#!/usr/bin/env python3
"""Independent complete-set audit of the prescribed-driver lap map.

Whole-word mirror normalizations build an explicit partial exterior map.
Each driver phase filters its exact e/g bits; composing these maps gives H.
Explicit sink peeling tests arbitrary H cycles, rather than only H(x)=x.
Every surviving set and every collected checkpoint is compared with the
MDD's independently expanded accepting digit paths.  This is finite audit
evidence, not a new certificate or an unrestricted-width theorem.
"""
from array import array
import argparse
from dataclasses import dataclass
from itertools import product
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror
import target_strobe_mdd as candidate

TARGET_E = '010100110100101011001011'
TARGET_G = '110001001000110001001000'


def encode(word, radix):
    value = 0
    for x in word:
        value = radix*value+x
    return value


def decode(value, radix):
    word = []
    while value:
        value, x = divmod(value, radix)
        word.append(x)
    return tuple(reversed(word))


@dataclass
class FullMap:
    first: int
    successor: array
    e: bytearray
    g: bytearray


def full_map(base, width, state_cap=200000):
    radix = 2*base-1
    first, limit = ((0, 1) if width == 0 else
                    (radix**(width-1), radix**width))
    count = limit-first
    if count > state_cap or count >= 2**31:
        raise RuntimeError(f'explicit map needs {count} states; cap={state_cap}')
    successor = array('i', [-1])*count
    es, gs = bytearray(count), bytearray(count)
    for index in range(count):
        word = decode(first+index, radix)
        assert len(word) == width and (not word or word[0] > 0)
        low, e = mirror.norm(base, word, 0)
        reflected, g = mirror.norm(base, word[::-1], 1-e)
        es[index], gs[index] = e, g
        reflected.reverse()
        if g:
            low.append((base-1)*(1-e))
            reflected.insert(0, 1)
        raw = tuple(x+y for x, y in zip(low, reflected))
        assert len(raw) == width+g
        if g and raw[-1] != base-1:
            continue
        target = raw[:width]
        if target and target[0] == 0:
            continue
        nxt = encode(target, radix)-first
        assert 0 <= nxt < count
        successor[index] = nxt
    return FullMap(first, successor, es, gs)


def lap_map(mapping, e_stream, g_stream):
    assert e_stream and len(e_stream) == len(g_stream)
    phases = tuple((int(e), int(g)) for e, g in zip(e_stream, g_stream))
    assert all(e in (0, 1) and g in (0, 1) for e, g in phases)
    result = array('i', [-1])*len(mapping.successor)
    for source in range(len(result)):
        current = source
        for e, g in phases:
            if current < 0 or (mapping.e[current], mapping.g[current]) != (e, g):
                current = -1
                break
            current = mapping.successor[current]
        result[source] = current
    return result


def next_survivors(current, lap):
    return {source for source in current
            if lap[source] >= 0 and lap[source] in current}


def cycles_of(lap, survivors):
    """Explicit functional-graph cycles, including periods greater than one."""
    done, cycles = set(), []
    for start in survivors:
        if start in done:
            continue
        path, position, current = [], {}, start
        while current >= 0 and current not in done and current not in position:
            position[current] = len(path)
            path.append(current)
            current = lap[current]
        if current in position:
            cycles.append(path[position[current]:])
        done.update(path)
    return cycles


def expand(diagram, root):
    """Interpret complete accepted words, without MDD contains/count."""
    result = set()

    def visit(node, level, value):
        if node == 0:
            return
        if node == 1:
            assert level == diagram.width
            result.add(value)
            return
        actual, children = diagram.nodes[node]
        assert actual == level and len(children) == diagram.arity
        for x, child in enumerate(children):
            if child:
                visit(child, level+1, diagram.arity*value+x)

    visit(root, 0, 0)
    return result


def audit_case(base, width, e_stream, g_stream, mapping, collect, totals,
               deadline, max_laps=1000):
    if time.monotonic() >= deadline:
        raise RuntimeError('whole-audit time cap')
    lap = lap_map(mapping, e_stream, g_stream)
    diagram = candidate.StrobeMDD(base, width, seconds=max(1, deadline-time.monotonic()))
    root = diagram.full()
    current = set(range(len(lap)))
    counts = [len(current)]
    assert expand(diagram, root) == {mapping.first+s for s in current}
    totals['set_comparisons'] += 1
    status = 'UNDECIDED'
    for iteration in range(1, max_laps+1):
        if time.monotonic() >= deadline:
            raise RuntimeError('whole-audit time cap')
        following = next_survivors(current, lap)
        old, nxt = diagram.lap_preimage(root, e_stream, g_stream, collect=collect)
        assert expand(diagram, old) == {mapping.first+s for s in current}, (
            'checkpoint_corruption', base, width, e_stream, g_stream, iteration, collect)
        totals['checkpoint_comparisons'] += 1
        expected = {mapping.first+s for s in following}
        represented = expand(diagram, nxt)
        assert represented == expected, (
            base, width, e_stream, g_stream, iteration, collect,
            'extra', sorted(represented-expected)[:8],
            'missing', sorted(expected-represented)[:8])
        totals['set_comparisons'] += 1
        assert diagram.count(nxt) == len(following)
        assert (old == nxt) == (current == following)
        counts.append(len(following))
        if not following:
            assert nxt == 0
            status = 'EMPTY'
        elif following == current:
            status = 'FIXED_POINT'
        current = following
        if status != 'UNDECIDED':
            break
        root = diagram.collect_many((nxt,))[0] if collect else nxt
        assert expand(diagram, root) == expected
        totals['checkpoint_comparisons'] += 1
    if status == 'UNDECIDED':
        raise RuntimeError(f'explicit lap peeling exceeds {max_laps} laps')
    cycles = cycles_of(lap, current) if current else []
    assert (status == 'FIXED_POINT') == bool(cycles)
    summary, records = candidate.run(
        base=base, width=width, rounds=max_laps, quiet=True, collect=collect,
        e_stream=e_stream, g_stream=g_stream,
        seconds=max(1, deadline-time.monotonic()))
    expected_counts = counts[:-1] if status == 'FIXED_POINT' else counts
    assert summary['status'] == status
    assert [record['words'] for record in records] == expected_counts
    assert summary['words'] == len(current)
    totals['run_comparisons'] += 1
    totals['cases'] += 1
    totals['positive_cases'] += int(bool(cycles))
    return dict(base=base, width=width, e=e_stream, g=g_stream, collect=collect,
                counts=counts, status=status, cycle_laps=sorted(map(len, cycles)),
                fixed_points=sum(lap[s] == s for s in current))


def synthetic_multilap_control():
    """A generic H example, explicitly not a physical exterior witness."""
    lap = (1, 0, 0, -1)
    initial = set(range(4))
    survivors = next_survivors(initial, lap)
    assert survivors == {0, 1, 2}
    assert next_survivors(survivors, lap) == survivors
    assert not any(lap[s] == s for s in survivors)
    assert sorted(map(len, cycles_of(lap, survivors))) == [2]
    print('SYNTHETIC_MULTILAP_CONTROL period=2 fixed_points=0 feeders=1 PASS; '
          'NOT_AN_EXTERIOR_WITNESS', flush=True)


def small_controls(totals, deadline):
    cases_before = totals['cases']
    for base, width, max_period in ((2, 3, 3), (4, 3, 3), (10, 2, 2)):
        mapping = full_map(base, width)
        for period in range(1, max_period+1):
            for values in product(range(4), repeat=period):
                e = ''.join(str(x//2) for x in values)
                g = ''.join(str(x % 2) for x in values)
                results = [audit_case(base, width, e, g, mapping, collect,
                                      totals, deadline) for collect in (False, True)]
                assert results[0]['counts'] == results[1]['counts']
    print(f'EXHAUSTIVE_SMALL_DRIVERS cases={totals["cases"]-cases_before} PASS', flush=True)


def known_positive_controls(totals, deadline):
    for base, period in ((2, 2), (4, 3), (8, 4)):
        e = g = '1'+'0'*(period-1)
        for width in (2, 3):
            mapping = full_map(base, width)
            for repeats in (1, 2, 3):
                results = [audit_case(base, width, e*repeats, g*repeats,
                                      mapping, collect, totals, deadline)
                           for collect in (False, True)]
                assert all(r['status'] == 'FIXED_POINT' for r in results)
                assert results[0]['counts'] == results[1]['counts']
                print('KNOWN_POSITIVE_DRIVER', json.dumps(results[1], separators=(',', ':')),
                      flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-width', type=int, default=4)
    parser.add_argument('--state-cap', type=int, default=200000)
    parser.add_argument('--seconds', type=float, default=180)
    parser.add_argument('--controls', action='store_true')
    args = parser.parse_args()
    if args.max_width < 0 or args.state_cap < 1 or not 0 < args.seconds <= 600:
        parser.error('max-width>=0, positive state cap, and seconds in(0,600] required')
    assert candidate.E == TARGET_E and candidate.G == TARGET_G
    deadline = time.monotonic()+args.seconds
    totals = dict(cases=0, set_comparisons=0, checkpoint_comparisons=0,
                  run_comparisons=0, positive_cases=0)
    for width in range(args.max_width+1):
        mapping = full_map(10, width, args.state_cap)
        for collect in (False, True):
            result = audit_case(10, width, TARGET_E, TARGET_G,
                                mapping, collect, totals, deadline)
            print('TARGET_FULL_SET_AUDIT', json.dumps(result, separators=(',', ':')), flush=True)
    if args.controls:
        small_controls(totals, deadline)
        known_positive_controls(totals, deadline)
        synthetic_multilap_control()
    print('ALL STROBOSCOPIC AUDITS PASSED', json.dumps(totals, separators=(',', ':')),
          'FINITE VALIDATION ONLY', flush=True)


if __name__ == '__main__':
    try:
        main()
    except (MemoryError, RuntimeError, ValueError) as error:
        print(f'UNDECIDED: {error}', file=sys.stderr, flush=True)
        raise SystemExit(2)
