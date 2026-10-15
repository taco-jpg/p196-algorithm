#!/usr/bin/env python3
"""Bounded literal-integer controls for HIGH_CARRY_RENEWAL.md."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digits(n: int, b: int) -> list[int]:
    out = []
    while n:
        n, d = divmod(n, b)
        out.append(d)
    return out or [0]


def evaluate(ds: list[int], b: int) -> int:
    return sum(d * b**i for i, d in enumerate(ds))


def step(n: int, b: int) -> int:
    return n + evaluate(digits(n, b)[::-1], b)


def pairs(n: int, b: int) -> list[int]:
    ds = digits(n, b)
    return [a + c for a, c in zip(ds, ds[::-1])]


def seed(q: tuple[int, ...], b: int) -> int:
    assert q == q[::-1] and q[0] >= b
    assert all(0 <= c <= 2*b-2 for c in q)
    ds = [0] * len(q)
    for i in range(len(q)//2):
        ds[i] = min(q[i], b-1)
        ds[-1-i] = q[i] - ds[i]
    if len(q) % 2:
        assert q[len(q)//2] % 2 == 0
        ds[len(q)//2] = q[len(q)//2] // 2
    n = evaluate(ds, b)
    assert tuple(pairs(n, b)) == q
    return n


def inspect(q: tuple[int, ...], b: int) -> dict:
    n = seed(q, b)
    ns = [n]
    for _ in range(4):
        ns.append(step(ns[-1], b))
    qs = [pairs(x, b) for x in ns]
    pal = [digits(x, b) == digits(x, b)[::-1] for x in ns]
    high = all(b-1 <= c <= 2*b-2 for c in q)
    a = q[0]-b+1
    checked = []
    if a >= (b+3)//2:
        assert not pal[1] and not pal[3]
        assert qs[2][0] not in range(b) and qs[2][0] != b+1
        checked.append('universal_exterior_third_safety')
    if high and len(q) >= 2:
        r = [c-b+1 for c in q]
        p = [a] + [x+y for x,y in zip(r,r[1:])] + [a]
        assert qs[1] == p
        checked.append('exact_first_high_carry_map')
        if q[0] == 2*b-2 and q[1] >= b+1:
            assert qs[2][0] == b and qs[2][1] == q[1]-b
            assert 1 <= qs[2][1] < b and not pal[3]
            checked.append('maximum_exterior_regeneration')
        z = q[0]+q[1]-2*b+2
        if (b//2 <= a <= b-2 and
                b+1 <= z <= b+(b-2)//2):
            v = 0
            for coefficient in p[:len(q)-1]:
                v = (coefficient+v)//b
            assert v in (0,1)
            assert qs[2][0] == 2*a+1
            assert qs[2][1] == 2*(z-b)+v
            assert qs[2][0] >= b and 1 <= qs[2][1] < b
            assert not pal[3]
            checked.append('nonoverflowing_exterior_regeneration')
        if b == 10 and any(x.endswith('regeneration') for x in checked):
            assert not any(pal[1:4])
            checked.append('three_safe_positive_outputs')
        sums = [x+y for x,y in zip(q,q[1:])]
        if b == 10 and len(q) >= 3 and q[0] <= 17 and min(sums) >= 28:
            expected = [2*q[0]-17, 2*sums[0]-55]
            expected += [2*s-54 for s in sums[1:-1]]
            expected += [2*sums[-1]-55, 2*q[0]-17]
            assert qs[2] == expected
            returns = qs[2][0] >= 10 and all(9 <= c <= 18 for c in qs[2])
            assert returns == (min(sums) >= 32)
            checked.append('restricted_high_region_return_iff')
    return {'base': b, 'initial_pair_word': q, 'seed': n,
            'integers': ns, 'pair_words': qs, 'palindromic': pal,
            'checked': checked}


def main() -> None:
    specifications = set()
    # Fixed small parameter grid, not a trajectory search.
    for a in range(14,19):
        for c in range(9,19):
            for middle in (9,18):
                specifications.add((10,(a,c,middle,middle,c,a)))
    for a in range(10,19):
        specifications.add((10,(a,a)))
        if a % 2 == 0:
            specifications.add((10,(a,)))
    for a in (14,17):
        for middle in (10,18):
            specifications.add((10,(a,middle,a)))
    for b in range(3,10):
        for c in (b+1,2*b-2):
            for middle in (b-1,2*b-2):
                specifications.add((b,(2*b-2,c,middle,middle,c,2*b-2)))
        for a in range(b//2,b-1):
            for z in (b+1,b+(b-2)//2):
                c = z-a+b-1
                if b+1 <= z <= b+(b-2)//2 and b-1 <= c <= 2*b-2:
                    specifications.add((b,(a+b-1,c,b-1,b-1,c,a+b-1)))
    for a in (15,18):
        specifications.add((10,(a,0,0,a)))
    specifications.update({(10,(15,18,18,15)), (10,(17,18,18,17)),
                           (3,(4,4)), (10,(11,11,11,11))})
    rows = [inspect(q,b) for b,q in sorted(specifications)]
    twice = next(r for r in rows if r['base']==10 and
                 r['initial_pair_word']==(17,18,18,17))
    assert twice['pair_words'][2] == [17,15,18,15,17]
    assert twice['pair_words'][4] == [17,9,12,12,9,17]
    counter = next(r for r in rows if r['base']==10 and
                   r['initial_pair_word']==(15,18,18,15))
    assert counter['pair_words'][2] == [13,11,18,11,13]
    assert all(c >= 10 for c in counter['pair_words'][2])
    # Boundary recurrence proves the restricted template cannot hold three times.
    boundary_rows = []
    for a in range(14,18):
        for c in range(9,19):
            if a+c < 32:
                continue
            path = [(a,c)]
            for _ in range(2):
                x,y = path[-1]
                path.append((2*x-17,2*x+2*y-55))
            assert path[1][0]+path[1][1] < 32 or path[2][0]+path[2][1] < 32
            boundary_rows.append(path)
    control = {'records': rows, 'boundary_recurrence_controls': boundary_rows,
               'rejected_generalization': {
                   'claim': 'Exterior at least15 forces a mixed certificate after two steps.',
                   'counterexample_initial_pair_word': [15,18,18,15],
                   'second_pair_word': [13,11,18,11,13],
                   'status': 'FALSE; the exterior still certifies third-output safety.'}}
    output = json.dumps(control,indent=2,sort_keys=True)+'\n'
    (HERE/'controls.json').write_text(output)
    counts = {}
    for row in rows:
        for name in row['checked']:
            counts[name] = counts.get(name,0)+1
    report = {'result':'PASS','control_count':len(rows),'checks':counts,
              'boundary_recurrence_controls':len(boundary_rows),
              'method':'Literal integer reversal, canonical digit reconstruction, and actual pair-word recomputation. No persistence search.',
              'controls_sha256':hashlib.sha256(output.encode()).hexdigest(),
              'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'scope':'Finite controls only; all-parameter statements are proved in HIGH_CARRY_RENEWAL.md.'}
    (HERE/'verification.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
