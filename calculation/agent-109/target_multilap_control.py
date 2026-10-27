#!/usr/bin/env python3
"""Physical two-lap calibration supplied by Agent 105.

Credit: Agent 105, coordination issue #289, comment 6433504667:
https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6433504667

Independently replays the supplied four-edge base-6 exterior cycle, pads
it to width 6, and checks the two-lap stroboscopic cycle for e=g=01.
An explicit finite-width oracle compares complete survivor sets and
singleton/set preimages. This does NOT reproduce or claim Agent 105's
separate all-width one-lap exclusion. No center or new certificate is
provided. Existing frozen audit files are imported without modification.
"""
import argparse
import json
from pathlib import Path
import resource
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror
import target_strobe_mdd as candidate
from target_strobe_audit import (
    audit_case, decode, encode, expand, full_map, lap_map,
)

BASE, WIDTH = 6, 6
E = G = '01'
CANONICAL = (
    (4, 7, 7, 8, 3),
    (9, 3, 4, 5, 8),
    (4, 7, 7, 10, 2, 2),
    (9, 3, 4, 9),
)
TRIMS = (0, 0, 2, 0)
PADDED = tuple(word+(BASE-1,)*(WIDTH-len(word)) for word in CANONICAL)


def normalize(word, carry):
    digits = []
    for coefficient in word:
        quotient, digit = divmod(coefficient+carry, BASE)
        digits.append(digit)
        carry = quotient
    return tuple(digits), carry


def raw_successor(word):
    """Independent integer arithmetic, then a full A120-mirror comparison."""
    low, e = normalize(word, 0)
    high, g = normalize(word[::-1], 1-e)
    high = high[::-1]
    if g:
        low = low+((BASE-1)*(1-e),)
        high = (1,)+high
    raw = tuple(x+y for x, y in zip(low, high))
    # A one-coefficient center realizes the required complementary carry.
    # These auxiliary centers are not asserted to form a joint cycle.
    center = [2*BASE-2] if e == 0 else [0]
    assert mirror.hyp(BASE, list(word), center)
    assert e == mirror.e1(BASE, list(word))
    assert g == mirror.gam(BASE, list(word), center)
    assert raw == tuple(mirror.nextB(BASE, list(word), center))
    return raw, e, g


def lap_word(word):
    for ee, gg in zip(E, G):
        raw, e, g = raw_successor(word)
        assert (e, g) == (int(ee), int(gg))
        assert len(raw) == WIDTH+g
        assert not g or raw[-1] == BASE-1
        word = raw[:WIDTH]
        assert word[0] > 0
    return word


def replay_fixture():
    records = []
    for phase, word in enumerate(CANONICAL):
        raw, e, g = raw_successor(word)
        following = CANONICAL[(phase+1) % len(CANONICAL)]
        assert (e, g) == (phase % 2, phase % 2)
        assert raw == following+(BASE-1,)*TRIMS[phase]
        padded_raw, pe, pg = raw_successor(PADDED[phase])
        assert (pe, pg) == (e, g)
        assert padded_raw == PADDED[(phase+1) % len(PADDED)]+(BASE-1,)*g
        records.append(dict(B=word, padded=PADDED[phase], e=e, g=g,
                            natural_trim=TRIMS[phase], padded_trim=g))
    assert PADDED[0] != PADDED[2]
    assert lap_word(PADDED[0]) == PADDED[2]
    assert lap_word(PADDED[2]) == PADDED[0]
    print('AGENT105_FIXTURE_REPLAY', json.dumps(records, separators=(',', ':')), flush=True)
    print('PHYSICAL_TWO_LAP_CYCLE', json.dumps([PADDED[0], PADDED[2]],
                                             separators=(',', ':')), flush=True)


def finite_set_node(diagram, words):
    root = 0
    for word in words:
        leaf = 1
        for level in range(WIDTH-1, -1, -1):
            children = [0]*diagram.arity
            children[word[level]] = leaf
            leaf = diagram.node(level, children)
        root = diagram.union(root, leaf)
    return root


def target_preimages(mapping, lap, deadline):
    checks = 0
    for words in ((PADDED[0],), (PADDED[2],), (PADDED[0], PADDED[2])):
        codes = {encode(word, 2*BASE-1) for word in words}
        expected = {mapping.first+i for i, target in enumerate(lap)
                    if target >= 0 and mapping.first+target in codes}
        for collect in (False, True):
            diagram = candidate.StrobeMDD(BASE, WIDTH,
                                          seconds=max(1, deadline-time.monotonic()))
            target = finite_set_node(diagram, words)
            old, preimage = diagram.lap_preimage(target, E, G, collect=collect)
            assert expand(diagram, old) == codes
            assert expand(diagram, preimage) == expected
            assert diagram.count(preimage) == len(expected)
            checks += 1
        print('EXACT_TARGET_PREIMAGE', json.dumps({
            'target_words': words, 'preimage_words':
            [decode(code, 2*BASE-1) for code in sorted(expected)]
        }, separators=(',', ':')), flush=True)
    return checks


def replay_seed(summary):
    seed = tuple(summary['surviving_seed'])
    current, path, positions = seed, [], {}
    while current not in positions:
        if len(path) >= 1000:
            raise RuntimeError('surviving seed replay exceeds 1000 laps')
        positions[current] = len(path)
        path.append(current)
        current = lap_word(current)
    cycle = path[positions[current]:]
    assert len(cycle) > 1
    print('SURVIVING_SEED_REPLAY', json.dumps({
        'seed': seed, 'prefix_laps': positions[current],
        'period_laps': len(cycle), 'cycle': cycle
    }, separators=(',', ':')), flush=True)


def run(seconds=55):
    started = time.monotonic()
    deadline = started+seconds
    replay_fixture()
    mapping = full_map(BASE, WIDTH, state_cap=2000000)
    assert len(mapping.successor) == 1610510
    lap = lap_map(mapping, E, G)
    a, b = (encode(PADDED[j], 2*BASE-1)-mapping.first for j in (0, 2))
    assert lap[a] == b and lap[b] == a and a != b
    preimage_checks = target_preimages(mapping, lap, deadline)
    totals = dict(cases=0, set_comparisons=0, checkpoint_comparisons=0,
                  run_comparisons=0, positive_cases=0)
    results = []
    for collect in (False, True):
        result = audit_case(BASE, WIDTH, E, G, mapping, collect, totals, deadline)
        assert result['status'] == 'FIXED_POINT'
        assert 2 in result['cycle_laps']
        results.append(result)
        print('PHYSICAL_MULTILAP_FULL_SET_AUDIT',
              json.dumps(result, separators=(',', ':')), flush=True)
    assert results[0]['counts'] == results[1]['counts']
    summary, records = candidate.run(base=BASE, width=WIDTH, e_stream=E, g_stream=G,
                                     quiet=True, seconds=max(1, deadline-time.monotonic()))
    assert summary['status'] == 'FIXED_POINT'
    assert encode(tuple(summary['surviving_seed']), 2*BASE-1)-mapping.first in range(len(lap))
    replay_seed(summary)
    if time.monotonic() > deadline:
        raise RuntimeError('whole-control time cap')
    print('ALL PHYSICAL MULTILAP CONTROLS PASSED', json.dumps({
        'credit': 'Agent105 issue289 comment6433504667',
        'explicit_words': len(lap), 'target_preimage_checks': preimage_checks,
        **totals, 'survivor_counts': [record['words'] for record in records],
        'seconds': round(time.monotonic()-started, 3),
        'maxrss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    }, separators=(',', ':')), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=float, default=55)
    args = parser.parse_args()
    if not 0 < args.seconds <= 60:
        parser.error('seconds must be in(0,60]')
    run(args.seconds)


if __name__ == '__main__':
    try:
        main()
    except (MemoryError, RuntimeError, ValueError) as error:
        print(f'UNDECIDED: {error}', file=sys.stderr, flush=True)
        raise SystemExit(2)
