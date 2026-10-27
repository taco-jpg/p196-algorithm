#!/usr/bin/env python3
"""Exact cycle-set controls for simultaneous driver phase rotation.

For phase maps f_0,...,f_(p-1), write P=f_(r-1)...f_0 and
Q=f_(p-1)...f_r.  Original and rotated lap maps are H=QP and K=PQ.
On cyclic vertices P is a bijection satisfying PH=KP.  Injectivity follows
because H is a permutation on its cyclic vertices; the inverse at y is
Q(K^{-1}(y)).  Thus every cycle's period in laps is preserved.  Survival
sets can contain feeders, so no bijection of those larger sets is claimed.

For certificate replay, rotate E/G/V together and start the center at C_r.
This file tests explicit complete cycle sets, their induced prefix map,
the public rotation API, and surviving-seed membership.  It proves no new
unrestricted-width result and does not modify previous audit programs.
"""
import argparse
import json
import time

import target_strobe_mdd as candidate
from target_strobe_audit import (
    TARGET_E, TARGET_G, cycles_of, decode, encode,
    full_map, lap_map, next_survivors,
)


def stable_set(lap, max_rounds=1000):
    current = set(range(len(lap)))
    counts = [len(current)]
    for _ in range(max_rounds):
        following = next_survivors(current, lap)
        counts.append(len(following))
        if not following or following == current:
            return following, counts
        current = following
    raise RuntimeError('explicit survival iteration cap')


def prefix(mapping, source, e, g):
    for ee, gg in zip(e, g):
        assert source >= 0
        assert (mapping.e[source], mapping.g[source]) == (int(ee), int(gg))
        source = mapping.successor[source]
    assert source >= 0
    return source


def cycle_vertices(lap):
    cycles = cycles_of(lap, range(len(lap)))
    vertices = {x for cycle in cycles for x in cycle}
    return vertices, cycles


def check_rotation(mapping, e, g, rotation):
    period = len(e)
    r = rotation % period
    original = lap_map(mapping, e, g)
    rotated = lap_map(mapping, e[r:]+e[:r], g[r:]+g[:r])
    old_vertices, old_cycles = cycle_vertices(original)
    new_vertices, new_cycles = cycle_vertices(rotated)
    phi = {x: prefix(mapping, x, e[:r], g[:r]) for x in old_vertices}
    assert len(set(phi.values())) == len(old_vertices)
    assert set(phi.values()) == new_vertices
    assert sorted(map(len, old_cycles)) == sorted(map(len, new_cycles))
    for x in old_vertices:
        assert phi[original[x]] == rotated[phi[x]]
    rotated_predecessor = {rotated[y]: y for y in new_vertices}
    assert len(rotated_predecessor) == len(new_vertices)
    for x, y in phi.items():
        assert prefix(mapping, rotated_predecessor[y], e[r:], g[r:]) == x
    images = {frozenset(phi[x] for x in cycle) for cycle in old_cycles}
    assert images == {frozenset(cycle) for cycle in new_cycles}
    return rotated, old_vertices, new_vertices, old_cycles


def primitive_driver(e, g):
    for period in range(1, len(e)+1):
        if len(e) % period == 0 and all(
                (e[j], g[j]) == (e[j % period], g[j % period]) for j in range(len(e))):
            return e[:period], g[:period]
    raise AssertionError('a finite word has its own length as a period')


def public_run_control(base, width, mapping, e, g, rotation, lap, deadline):
    survivors, counts = stable_set(lap)
    for collect in (False, True):
        summary, records = candidate.run(
            base=base, width=width, e_stream=e, g_stream=g,
            rotate=rotation, collect=collect, quiet=True,
            seconds=max(1, deadline-time.monotonic()))
        status = 'FIXED_POINT' if survivors else 'EMPTY'
        assert summary['status'] == status
        assert summary['phase_start'] == rotation % len(e)
        assert summary['words'] == len(survivors)
        expected = counts[:-1] if survivors else counts
        assert [record['words'] for record in records] == expected
        if survivors:
            word = tuple(summary['surviving_seed'])
            assert len(word) == width
            index = encode(word, 2*base-1)-mapping.first
            assert index in survivors
            assert decode(index+mapping.first, 2*base-1) == word
        else:
            assert 'surviving_seed' not in summary
    return len(survivors)


def synthetic_control():
    # H=QP has a feeder; K=PQ does not.  Both have one two-lap cycle.
    p, q = (0, 1, 0), (1, 0, -1)
    h = tuple(q[p[x]] for x in range(3))
    k = tuple(p[q[x]] if q[x] >= 0 else -1 for x in range(3))
    hv, hc = cycle_vertices(h)
    kv, kc = cycle_vertices(k)
    assert hv == kv == {0, 1}
    assert sorted(map(len, hc)) == sorted(map(len, kc)) == [2]
    assert {p[x] for x in hv} == kv
    assert all(p[h[x]] == k[p[x]] for x in hv)
    hs, _ = stable_set(h)
    ks, _ = stable_set(k)
    assert hs == {0, 1, 2} and ks == {0, 1}
    print('SYNTHETIC_ROTATION period_laps=2 survivors_before=3 '
          'survivors_after=2 cyclic_vertices=2 PASS; NOT_A_B_WITNESS', flush=True)


def run_controls(seconds=180):
    deadline = time.monotonic()+seconds
    rotation_checks = public_checks = drivers = 0
    # Positive fixtures are obtained directly from the small explicit B maps;
    # this is a calibration exercise, not a separate exterior-cycle census.
    for base, width in ((2, 4), (3, 7), (4, 3), (4, 6), (6, 5), (8, 4)):
        mapping = full_map(base, width)
        raw_cycles = cycles_of(mapping.successor, range(len(mapping.successor)))
        assert raw_cycles
        seen = set()
        for cycle in raw_cycles:
            e = ''.join(str(mapping.e[x]) for x in cycle)
            g = ''.join(str(mapping.g[x]) for x in cycle)
            e, g = primitive_driver(e, g)
            if (e, g) in seen:
                continue
            seen.add((e, g))
            drivers += 1
            survivor_counts = []
            cyclic_counts = []
            for rotation in range(len(e)):
                if time.monotonic() >= deadline:
                    raise RuntimeError('rotation audit time cap')
                lap, old, new, _ = check_rotation(mapping, e, g, rotation)
                assert old and new
                rotation_checks += 1
                cyclic_counts.append(len(new))
                if width <= 4:
                    survivor_counts.append(public_run_control(
                        base, width, mapping, e, g, rotation, lap, deadline))
                    public_checks += 2
            print('PHYSICAL_ROTATION_DRIVER', json.dumps({
                'base': base, 'width': width, 'e': e, 'g': g,
                'rotations': len(e), 'cyclic_counts': cyclic_counts,
                'survivor_counts_if_public_checked': survivor_counts
            }, separators=(',', ':')), flush=True)

    # Pinned target: both empty-cycle-set equivalence and rotation normalization.
    for width in range(5):
        mapping = full_map(10, width)
        for rotation in (0, 2, 26, -22):
            lap, old, new, _ = check_rotation(mapping, TARGET_E, TARGET_G, rotation)
            assert not old and not new
            rotation_checks += 1
            public_run_control(10, width, mapping, TARGET_E, TARGET_G,
                               rotation, lap, deadline)
            public_checks += 2
    synthetic_control()
    print('ALL ROTATION CONTROLS PASSED', json.dumps({
        'positive_drivers': drivers, 'cycle_set_rotations': rotation_checks,
        'public_run_and_seed_checks': public_checks,
        'seconds': round(seconds-(deadline-time.monotonic()), 3)
    }, separators=(',', ':')), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=float, default=180)
    args = parser.parse_args()
    if not 0 < args.seconds <= 600:
        parser.error('seconds must be in(0,600]')
    run_controls(args.seconds)


if __name__ == '__main__':
    try:
        main()
    except (MemoryError, RuntimeError, ValueError) as error:
        print(f'UNDECIDED: {error}', file=sys.stderr, flush=True)
        raise SystemExit(2)
