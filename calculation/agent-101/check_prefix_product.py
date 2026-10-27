#!/usr/bin/env python3
"""Independent arithmetic checks for the finite exterior-prefix/center product.

This validates a necessary projection, not a decimal Lychrel certificate.
All coefficient lists are least significant first. Standard library only.
"""
import argparse
import itertools
import json
import random
import sys
from array import array
from pathlib import Path


def norm_integer(word, carry, base=10):
    value = carry + sum(x * base**i for i, x in enumerate(word))
    digits = []
    for _ in word:
        value, d = divmod(value, base)
        digits.append(d)
    return tuple(digits), value


def exact_exterior(word):
    low, e = norm_integer(word, 0)
    high, g = norm_integer(word[::-1], 1-e)
    if g:
        left, right = low + (9*(1-e),), (1,) + high[::-1]
    else:
        left, right = low, high[::-1]
    return tuple(x+y for x, y in zip(left, right)), e, g


def prefix(word, width):
    return (tuple(word) + (9,)*width)[:width]


def projected_edges(p):
    """All projected edges, retaining the unknown incoming reverse carry."""
    result = set()
    for inner in (0, 1):
        high = [0]*len(p) + [inner]
        for i in reversed(range(len(p))):
            high[i] = (p[i] + high[i+1]) // 10
        low = 0
        out = []
        for i, x in enumerate(p):
            low, d = divmod(x+low, 10)
            if high[0]:
                other = 1 if i == 0 else (p[i-1]+high[i]) % 10
            else:
                other = (x+high[i+1]) % 10
            out.append(d+other)
        result.add((tuple(out), high[0]))
    return result


def center_edges(c, g, bound=None, base=10):
    result = set()
    for e in (0, 1):
        digits, carry = norm_integer(c, e, base)
        if carry != 1-e:
            continue
        w = digits + ((base-1)*e,) if g else digits
        raw = tuple(a+b for a, b in zip(w, w[::-1]))
        v = 0
        while raw:
            if bound is None or len(raw) <= bound:
                result.add((raw, e, v))
            if len(raw) < 2 or raw[0] != base-1 or raw[-1] != base-1:
                break
            raw = raw[1:-1]
            v += 1
    return result


def centers(bound):
    for n in range(1, bound+1):
        for h in itertools.product(range(19), repeat=(n+1)//2):
            c = h + h[:n//2][::-1]
            if any(norm_integer(c, e)[1] == 1-e for e in (0, 1)):
                yield c


def reference_graph(width, bound):
    cs = list(centers(bound))
    ix = {c: i for i, c in enumerate(cs)}
    ps = [(a,)+r for a in range(1, 19)
          for r in itertools.product(range(19), repeat=width-1)]
    pi = {p: i for i, p in enumerate(ps)}
    n = len(cs)*len(ps)
    pe = [[(pi[q], g) for q, g in projected_edges(p)] for p in ps]
    ce = {g: [[ix[d] for d, _, _ in center_edges(c, g, bound) if d in ix]
              for c in cs] for g in (0, 1)}
    indegree = array('I', [0])*n
    total_edges = 0
    for psucc in pe:
        for ci in range(len(cs)):
            for qp, g in psucc:
                for qc in ce[g][ci]:
                    indegree[qp*len(cs)+qc] += 1
                    total_edges += 1
    queue = array('I', (i for i, degree in enumerate(indegree) if degree == 0))
    removed = 0
    while removed < len(queue):
        p, c = divmod(queue[removed], len(cs))
        removed += 1
        for qp, g in pe[p]:
            for qc in ce[g][c]:
                dst = qp*len(cs)+qc
                assert indegree[dst] > 0
                indegree[dst] -= 1
                if indegree[dst] == 0:
                    queue.append(dst)
    result = dict(prefix_width=width, center_bound=bound, centers=len(cs),
                  states=n, edges=total_edges, removed=removed,
                  residual=n-removed)
    print(json.dumps(result, sort_keys=True))
    return result


def check_witness(path):
    items = [json.loads(line) for line in Path(path).read_text().splitlines()
             if line.startswith('{')]
    witness = next(x for x in items if x.get('projected_cycle'))
    edges = witness['edges']
    assert edges and len(edges) == witness['period']
    for i, edge in enumerate(edges):
        p, q = tuple(edge['prefix']), tuple(edge['next_prefix'])
        c, d = tuple(edge['C']), tuple(edge['next_C'])
        assert (q, edge['g']) in projected_edges(p)
        assert (d, edge['e'], edge['v']) in center_edges(c, edge['g'])
        nxt = edges[(i+1) % len(edges)]
        assert tuple(nxt['prefix']) == q and tuple(nxt['C']) == d
    assert sum(e['g'] for e in edges) == witness['sum_g']
    assert 2*sum(e['v'] for e in edges) == witness['sum_g']
    print(f"PASS projected_cycle period={len(edges)} sum_g={witness['sum_g']} "
          f"sum_v={witness['sum_v']} actual_certificate=False")


def selftest():
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    import neutral_band_search as mirror
    checked = 0
    # All valid B words of length at most three, including the empty exterior.
    words = [()]
    words += [(a,)+tail for n in range(1, 4) for a in range(1, 19)
              for tail in itertools.product(range(19), repeat=n-1)]
    rng = random.Random(101)
    # Long words, long neutral suffixes, short exteriors, and independent trims.
    for _ in range(10000):
        n = rng.randrange(1, 81)
        w = (rng.randrange(1, 19),) + tuple(rng.randrange(19) for _ in range(n-1))
        words.append(w + (9,)*rng.randrange(16))
    for b in words:
        raw, e, g = exact_exterior(b)
        c = [10] if e == 0 else [0]
        assert mirror.hyp(10, list(b), c)
        assert raw == tuple(mirror.nextB(10, list(b), c))
        assert g == mirror.gam(10, list(b), c)
        for width in (1, 2, 3):
            permitted = projected_edges(prefix(b, width))
            for u in range(len(raw)+1):
                if u and raw[-u:] != (9,)*u:
                    break
                target = raw[:-u] if u else raw
                assert (prefix(target, width), g) in permitted
                checked += 1
    cchecked = 0
    for c in centers(5):
        e = next(e for e in (0, 1) if norm_integer(c, e)[1] == 1-e)
        b = [1] if e == 0 else [10]
        for g in (0, 1):
            # Independent normalization and output pairing versus direct columns.
            digits, out = mirror.norm(10, list(c), e)
            assert out == 1-e
            w = digits+[9*e] if g else digits
            raw = tuple(a+b for a, b in zip(w, reversed(w)))
            expected = set()
            v = 0
            while raw:
                expected.add((raw, e, v))
                if len(raw) < 2 or raw[0] != 9 or raw[-1] != 9:
                    break
                raw = raw[1:-1]
                v += 1
            assert center_edges(c, g) == expected
            cchecked += 1
    # Complete existing nondecimal certificates remain positive controls.
    positive_edges = 0
    for base, es in mirror._lean_certs():
        assert mirror.cycleOK(base, es, es[0][0], es[0][1])
        for b, c, b2, c2, u, v in es:
            g = mirror.gam(base, b, c)
            assert (tuple(c2), mirror.e1(base, b), v) in center_edges(tuple(c), g, base=base)
            positive_edges += 1
    print(f'PASS exterior_trim_projections={checked} center_cases={cchecked} '
          f'known_certificate_edges={positive_edges}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--graph', nargs=2, type=int, metavar=('PREFIX', 'CENTER'))
    parser.add_argument('--witness', type=Path)
    args = parser.parse_args()
    if args.graph:
        r, d = args.graph
        if not (1 <= r <= 2 and 1 <= d <= 6):
            parser.error('Python reference supports prefix 1..2 and center 1..6')
        reference_graph(r, d)
    elif args.witness:
        check_witness(args.witness)
    else:
        selftest()
