"""Constructive finite-pump search with physically constrained free clocks.

Bulk/outer cycles are candidate generators only. A complete exterior and
center proof is still required. No finite sampled orbit proves existence.
"""
from functools import lru_cache
from pathlib import Path
import argparse
import json
import random
import time

HERE = Path(__file__).resolve().parent


@lru_cache(None)
def bulk_digits(q):
    """Unique directional digits of a nonneutral periodic pair-sum row."""
    r = len(q)
    assert any(x != 9 for x in q)
    lo, hi = [], []
    for j in range(r):
        a = next(int(q[(j-k) % r] >= 10) for k in range(1, r+1)
                 if q[(j-k) % r] != 9)
        b = next(int(q[(j+k) % r] >= 10) for k in range(1, r+1)
                 if q[(j+k) % r] != 9)
        lo.append((q[j]+a) % 10)
        hi.append((q[j]+b) % 10)
    return tuple(lo), tuple(hi)


def bulk_step(q, h):
    lo, hi = bulk_digits(q)
    return tuple(x + hi[(j-h) % len(q)] for j, x in enumerate(lo))


def valid(q, residue):
    r = len(q)
    return (len(set(q)) > 1 and
            all(q[j] == q[(residue-1-j) % r] for j in range(r)) and
            (residue % 2 == 0 or q[((residue-1)//2) % r] % 2 == 0))


def outer_options(prefix):
    # Incoming carry at the units is zero; e enters from the unknown interior.
    for e in (0, 1):
        lo, hi = [], [0]*len(prefix)
        a = 0
        for x in prefix:
            lo.append((x+a) % 10)
            a = (x+a)//10
        b = e
        for i in reversed(range(len(prefix))):
            hi[i] = (prefix[i]+b) % 10
            b = (prefix[i]+b)//10
        h = b
        nxt = tuple(x + (1 if h and i == 0 else hi[i-h]) for i,x in enumerate(lo))
        yield h, nxt, e


def random_row(r, residue, rng):
    q = [-1]*r
    for j in range(r):
        if q[j] < 0:
            k = (residue-1-j) % r
            q[j] = q[k] = rng.randrange(19)
    if residue % 2:
        j = ((residue-1)//2) % r
        q[j] = 2*rng.randrange(10)
    return tuple(q)


def canonical_cycle(states, clocks, inside):
    # A zero-residue start is exactly the original all-length pump format.
    choices = [i for i, state in enumerate(states) if state[2] == 0]
    if not choices:
        return None
    i = min(choices, key=lambda i: (states[i:]+states[:i], clocks[i:]+clocks[:i]))
    states = states[i:]+states[:i]
    clocks = clocks[i:]+clocks[:i]
    inside = inside[i:]+inside[:i]
    return dict(period=len(states), growth=sum(clocks), spatial_period=len(states[0][1]),
                bulk=[list(s[1]) for s in states], outer=[s[0][0] for s in states],
                prefix=[list(s[0]) for s in states], prefix_width=len(states[0][0]),
                residues=[s[2] for s in states], clock=clocks, high_carry=inside)


def search(r=5, trials=4000, steps=300, max_period=80, prefix_width=1):
    rng = random.Random(19620261015+r)
    cycles, stats = {}, dict(walks=0, steps=0, repeats=0, dead=0)
    start = time.monotonic()
    for trial in range(trials):
        q = random_row(r, 0, rng)
        if not valid(q, 0):
            continue
        prefix = (rng.randrange(1, 19),)+tuple(rng.randrange(19) for _ in range(prefix_width-1))
        state = (prefix, q, 0)
        seen, states, clocks, inward = {}, [], [], []
        stats['walks'] += 1
        for _ in range(steps):
            if state in seen:
                stats['repeats'] += 1
                at = seen[state]
                cc, hh, ee = states[at:], clocks[at:], inward[at:]
                if sum(hh) and len(cc) <= max_period:
                    row = canonical_cycle(cc, hh, ee)
                    if row:
                        key = json.dumps([row['bulk'], row['outer'], row['clock']])
                        cycles[key] = row
                break
            seen[state] = len(states)
            states.append(state)
            prefix, q, s = state
            options = []
            for h, nx, e in outer_options(prefix):
                nq, ns = bulk_step(q, h), (s+h) % (2*r)
                if valid(nq, ns):
                    # Safety must hold even before a boundary is supplied.
                    if h == 0 and max(q+prefix) < 10:
                        continue
                    if h == 1 and prefix[0] == 11 and all(v in (0, 11) for v in q+prefix):
                        continue
                    options.append((h, nx, e, nq, ns))
            if not options:
                stats['dead'] += 1
                break
            h, nx, e, nq, ns = rng.choice(options)
            clocks.append(h)
            inward.append(e)
            state = nx, nq, ns
            stats['steps'] += 1
    rows = sorted(cycles.values(), key=lambda a: (a['period'], a['growth'], a['bulk'], a['outer']))
    return dict(scope='Sampled full-period bulk plus actual outer-column cycles; no exterior certificate yet',
                decimal_lychrel_existence_proved=False, seed=19620261015+r,
                parameters=dict(spatial_period=r, trials=trials, steps=steps, max_period=max_period,
                                prefix_width=prefix_width),
                stats=stats, seconds=time.monotonic()-start, candidates=rows)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--period', type=int, default=5)
    ap.add_argument('--trials', type=int, default=4000)
    ap.add_argument('--steps', type=int, default=300)
    ap.add_argument('--max-cycle', type=int, default=80)
    ap.add_argument('--prefix-width', type=int, default=1)
    args = ap.parse_args()
    result = search(args.period, args.trials, args.steps, args.max_cycle,args.prefix_width)
    suffix = '' if args.prefix_width == 1 else f'_k{args.prefix_width}'
    path = HERE/f'cycles_p{args.period}{suffix}.json'
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'candidates'}))
    print('cycles', len(result['candidates']))
    print('period/growth counts', sorted({(x['period'],x['growth']) for x in result['candidates']}))
