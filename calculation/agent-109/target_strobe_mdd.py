#!/usr/bin/env python3
"""Exact all-laps exterior search for the pinned 24-step center driver.

At fixed padded B width W, each phase uses its prescribed carry e and
overflow g. One backward lap composes phase preimages in reverse order.
Sink peeling of that lap map excludes every number of laps when EMPTY.
A nonempty FIXED_POINT guarantees only an exterior periodic orbit; an
actual B/C certificate still requires witness extraction and replay.
Its surviving_seed is at phase_start: center states and trim stream V must
be rotated to the same phase before any certificate replay.

The CLI pins the decimal driver below. The Python API permits other bases
and bit streams for independent positive and negative controls.
"""
from __future__ import annotations

import argparse
import resource
import sys
import time

from exterior_mdd import BudgetExceeded, MDD, cut_step


E = '010100110100101011001011'
G = '110001001000110001001000'
V = '100001000000100001000000'
C0 = (9, 14, 13, 18, 13, 14, 9)


def bits(stream, name):
    """Validate a nonempty finite bit stream without silently rounding."""
    if isinstance(stream, str):
        if not stream or any(c not in '01' for c in stream):
            raise ValueError(f'{name} must be a nonempty bit stream')
        return tuple(int(c) for c in stream)
    stream = tuple(stream)
    if not stream or any(not isinstance(x, int) or x not in (0, 1) for x in stream):
        raise ValueError(f'{name} must be a nonempty bit stream')
    return stream


class StrobeMDD(MDD):
    """MDD with a phase-pinned terminal condition and multi-root collection."""

    def first_word(self, root):
        """Lexicographically first accepted word; it need not be on a cycle."""
        if root == 0:
            raise ValueError('an empty diagram has no surviving seed')
        word = []
        current = root
        for level in range(self.width):
            if current <= 1 or self.nodes[current][0] != level:
                raise AssertionError('surviving seed level mismatch')
            children = self.nodes[current][1]
            digit = next(x for x, child in enumerate(children) if child)
            word.append(digit)
            current = children[digit]
        if current != 1:
            raise AssertionError('surviving seed did not reach a true terminal')
        return tuple(word)

    def phase_pre(self, target, slot, e):
        if target == 0:
            return 0
        key = (target, slot, e)
        old = self.pre_cache.get(key)
        if old is not None:
            return old
        self.budget()
        g, low, high, pending = slot
        if target == 1:
            result = int(low == e and high == 1-e
                         and (not g or pending == (self.base-1)*e))
        else:
            level, outputs = self.nodes[target]
            children = [0]*self.arity
            for x in range(1 if level == 0 else 0, self.arity):
                for high_next in (0, 1):
                    step = cut_step(self.base, slot, x, high_next)
                    if step is None:
                        continue
                    inner, y = step
                    if outputs[y] == 0:
                        continue
                    piece = self.phase_pre(outputs[y], inner, e)
                    children[x] = self.union(children[x], piece)
            result = self.node(level, children)
        self.remember(self.pre_cache, key, result)
        return result

    def phase_preimage(self, target, e, g):
        """Exact preimage under one padded phase with prescribed bits e,g."""
        if any(not isinstance(x, int) or x not in (0, 1) for x in (e, g)):
            raise ValueError('phase e and g must be bits')
        return self.phase_pre(target, (g, 0, g, g), e)

    def collect_many(self, roots):
        """Return remapped roots, retaining their joint DAG and clearing caches.

        All IDs from the previous arena become invalid. The returned roots
        preserve input order and equality, including duplicate input roots.
        """
        roots = tuple(roots)
        if any(not isinstance(r, int) or not 0 <= r < len(self.nodes) for r in roots):
            raise ValueError('collection roots must belong to the current arena')
        seen = set()
        stack = list(roots)
        while stack:
            u = stack.pop()
            if u < 2 or u in seen:
                continue
            seen.add(u)
            stack.extend(self.nodes[u][1])
        old = self.nodes
        self.nodes = [None, None]
        self.unique = {}
        self.union_cache = {}
        self.pre_cache = {}
        self.count_cache = {0: 0, 1: 1}
        mapped = {0: 0, 1: 1}
        for u in sorted(seen):
            level, children = old[u]
            mapped[u] = self.node(level, [mapped[c] for c in children])
        return tuple(mapped[r] for r in roots)

    def lap_preimage(self, target, e_stream=E, g_stream=G, collect=True,
                     phase_progress=False):
        """Return (old root, lap preimage), both in the resulting arena.

        The old root is explicitly retained during every collection. Never
        compare the input target ID with the returned preimage ID: collection
        may renumber the arena. Compare the two returned roots instead.
        """
        es, gs = bits(e_stream, 'e'), bits(g_stream, 'g')
        if len(es) != len(gs):
            raise ValueError('e and g streams must have equal lengths')
        saved, current = target, target
        for phase in range(len(es)-1, -1, -1):
            self.active_phase = phase
            current = self.phase_preimage(current, es[phase], gs[phase])
            if collect:
                saved, current = self.collect_many((saved, current))
            if phase_progress:
                print(f'phase={phase} words={self.count(current)} '
                      f'allocated_nodes={len(self.nodes)-2}', flush=True)
            if current == 0:
                break  # Every remaining preimage of the empty set is empty.
        self.active_phase = None
        return saved, current


def run(base=10, width=5, rounds=100, node_cap=1_000_000,
        cache_cap=2_000_000, seconds=300, quiet=False, collect=True,
        e_stream=E, g_stream=G, phase_progress=False, rotate=0):
    """Peel the exact lap map; records[0] is the full initial set S_0."""
    if not isinstance(rounds, int) or rounds < 0:
        raise ValueError('round bound must be a nonnegative integer')
    es, gs = bits(e_stream, 'e'), bits(g_stream, 'g')
    if len(es) != len(gs):
        raise ValueError('e and g streams must have equal lengths')
    if not isinstance(rotate, int):
        raise ValueError('phase rotation must be an integer')
    phase_start = rotate % len(es)
    es = es[phase_start:] + es[:phase_start]
    gs = gs[phase_start:] + gs[:phase_start]
    mdd = StrobeMDD(base, width, node_cap, cache_cap, seconds)
    root = mdd.full()
    records = []
    status = 'UNDECIDED'
    for iteration in range(rounds+1):
        words = mdd.count(root)
        rec = dict(iteration=iteration, words=words,
                   reachable_nodes=mdd.reachable_nodes(root),
                   allocated_nodes=len(mdd.nodes)-2,
                   pre_cache=len(mdd.pre_cache), union_cache=len(mdd.union_cache))
        records.append(rec)
        if not quiet:
            print(' '.join(f'{k}={v}' for k, v in rec.items()), flush=True)
        if root == 0:
            status = 'EMPTY'
            break
        if iteration == rounds:
            break
        old, nxt = mdd.lap_preimage(root, es, gs, collect, phase_progress)
        if old == nxt:
            root = nxt
            status = 'FIXED_POINT'
            break
        if mdd.count(nxt) >= words:
            raise AssertionError('strictly descending sets must strictly lose words')
        root = mdd.collect_many((nxt,))[0] if collect else nxt
    summary = dict(status=status, base=base, width=width, period=len(es),
                   phase_start=phase_start, iteration=iteration, words=mdd.count(root),
                   seconds=round(time.monotonic()-mdd.started, 3),
                   peak_nodes=mdd.peak_nodes, peak_cache=mdd.peak_cache,
                   maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if status == 'FIXED_POINT':
        # A survivor can be in a basin. Forward replay must locate the cycle.
        summary['surviving_seed'] = list(mdd.first_word(root))
    if not quiet:
        print(' '.join(f'{k}={v}' for k, v in summary.items()), flush=True)
    return summary, records


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--width', type=int, default=8)
    p.add_argument('--rounds', type=int, default=100)
    p.add_argument('--node-cap', type=int, default=1_000_000)
    p.add_argument('--cache-cap', type=int, default=2_000_000)
    p.add_argument('--seconds', type=float, default=300)
    p.add_argument('--no-collect', action='store_true')
    p.add_argument('--phase-progress', action='store_true')
    p.add_argument('--rotate', type=int, default=0,
                   help='start the cyclic driver at this phase (modulo 24)')
    a = p.parse_args()
    result, _ = run(width=a.width, rounds=a.rounds, node_cap=a.node_cap,
                    cache_cap=a.cache_cap, seconds=a.seconds,
                    collect=not a.no_collect, phase_progress=a.phase_progress,
                    rotate=a.rotate)
    if result['status'] == 'UNDECIDED':
        raise SystemExit(2)


if __name__ == '__main__':
    try:
        main()
    except (BudgetExceeded, MemoryError, RuntimeError) as error:
        print(f'UNDECIDED: {error}', file=sys.stderr, flush=True)
        raise SystemExit(2)
    except ValueError as error:
        print(f'INVALID INPUT: {error}', file=sys.stderr, flush=True)
        raise SystemExit(2)
