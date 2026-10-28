#!/usr/bin/env python3
"""Differential tests of gt.step against big-integer reverse-and-add."""
import random, sys, collections
sys.path.insert(0, '/home/claude/research/w3_formats/code')
from gt import *


def pairs(O):
    return [a + c for a, c in zip(O, O[::-1])]


def check_step(T, g, verbose=False):
    """returns None if step unsupported (exception), else raises AssertionError on mismatch, True if ok"""
    b = T.b
    try:
        T2, gmap, info = step(T)
    except (Ambiguous, Unsupported) as e:
        return ('unsupported', str(e)[:60])
    P = instantiate(T, g)
    M = val(b, P)
    O = digits_of(b, M)
    assert len(O) == len(P) + info['gam'], (fmt(T), g, len(O), len(P), info)
    Pn = pairs(O)
    g2 = {nid: mult * g[old] + off for nid, (old, mult, off) in gmap.items()}
    assert all(v >= 1 for v in g2.values()), ("small gap", g2)
    Pt = instantiate(T2, g2)
    if Pn != Pt:
        raise AssertionError(f"MISMATCH\nT={fmt(T)}\nT2={fmt(T2)}\ng={g}\ng2={g2}\nPn={Pn}\nPt={Pt}\n")
    pal = (O == O[::-1])
    assert pal == (not info['differs']), ("palindrome flag", fmt(T), g, pal, info)
    return True


def rand_template(rng, b, maxbands=3, maxm=3, maxlit=4, maxcore=4, neutral_bias=0.6):
    nb = rng.randint(0, maxbands)
    Hs = []
    pid = 0

    def rlit(n):
        return tuple(rng.randint(0, 2 * b - 2) for _ in range(n))
    for k in range(nb + 1):
        n = rng.randint(0, maxlit)
        if n:
            Hs.append(('L', rlit(n)))
        if k < nb:
            if rng.random() < neutral_bias:
                w = (b - 1,)
            else:
                m = rng.randint(1, maxm)
                w = rlit(m)
            Hs.append(('B', w, pid))
            pid += 1
    # merge adjacent literals not an issue (we put one literal between bands)
    nc = rng.randint(0, maxcore)
    half = rlit((nc + 1) // 2)
    core = half + half[:nc // 2][::-1]
    T = Template(b, Hs, core)
    # leading coefficient must be >= 1
    first = T.Hs[0] if T.Hs else None
    if first is None:
        return None
    lead = first[1][0]
    if lead == 0:
        return None
    return T


def main(n=3000, seed=1):
    rng = random.Random(seed)
    stats = collections.Counter()
    unsup = collections.Counter()
    for i in range(n):
        b = rng.choice([2, 3, 4, 5, 7, 10, 10, 10, 11, 16, 26])
        T = rand_template(rng, b)
        if T is None or not T.Hs:
            continue
        g = {p: rng.randint(25, 70) for p in T.pids()}
        # iterate a few steps from the same template
        cur = T
        gcur = g
        for s in range(6):
            r = check_step(cur, gcur)
            if r is True:
                stats['ok'] += 1
                T2, gmap, info = step(cur)
                gcur = {nid: mult * gcur[old] + off for nid, (old, mult, off) in gmap.items()}
                if any(v < 20 for v in gcur.values()):
                    break
                cur = T2
            else:
                stats['unsupported'] += 1
                unsup[r[1]] += 1
                break
    print(dict(stats))
    for k, v in unsup.most_common(8):
        print('  ', v, k)


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3000, int(sys.argv[2]) if len(sys.argv) > 2 else 1)
