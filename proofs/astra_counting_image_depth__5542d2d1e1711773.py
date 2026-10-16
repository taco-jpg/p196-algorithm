"""Exact inverse image-depth experiments for decimal pair-sum dynamics.

All values are integer coefficients, low digit first. No heuristic tests.
"""
from functools import lru_cache
from itertools import product
import json


def step(q):
    carry = 0
    d = []
    for x in q:
        carry, z = divmod(x + carry, 10)
        d.append(z)
    if carry:
        d.append(carry)
    return tuple(x + y for x, y in zip(d, reversed(d))), carry


def admissible(q):
    return bool(q) and q[0] > 0 and q == q[::-1] and all(0 <= x <= 18 for x in q) and (len(q) % 2 == 0 or q[len(q)//2] % 2 == 0)


@lru_cache(None)
def edge(st, x, h):
    a, b, t = st
    ans = []
    for bn in (0, 1):
        if (x + bn) // 10 != b:
            continue
        an, lo = divmod(x + a, 10)
        hi = (x + bn) % 10
        ans.append(((an, bn, hi if h else -1), lo + t if h else lo + hi))
    return tuple(ans)


def predecessors(r, branch=None, positive=True):
    """Enumerate exact canonical q with G(q)=r, once each."""
    for h in (0, 1) if branch is None else (branch,):
        n = len(r) - h
        if n < 1:
            continue
        m = n // 2
        def visit(i, st, half):
            a, b, t = st
            if i < m:
                for x in range(1 if i == 0 and positive else 0, 19):
                    for ns, y in edge(st, x, h):
                        if y == r[i]:
                            yield from visit(i+1, ns, half+(x,))
                return
            if n % 2 == 0:
                if a == b and (not h or 2*t == r[m]):
                    yield half + half[::-1]
            else:
                for c in range(2 if n == 1 and positive else 0, 19, 2):
                    if (c+a)//10 != b:
                        continue
                    z = (c+a)%10
                    y = z+t if h else 2*z
                    if y == r[m]:
                        yield half+(c,)+half[::-1]
        yield from visit(0, (0,h,1 if h else -1), ())


@lru_cache(None)
def image_depth_at_least(q, depth):
    if depth == 0:
        return True
    return any(image_depth_at_least(p, depth-1) for p in predecessors(q))


def all_words(n):
    if n == 1:
        yield from ((x,) for x in range(2,19,2))
        return
    for a in range(1,19):
        for tail in product(range(19), repeat=n//2-1):
            half=(a,)+tail
            for center in (range(0,19,2) if n%2 else (None,)):
                yield half+(() if center is None else (center,))+half[::-1]


def validate():
    for n in range(1,7):
        expected={}
        for q in all_words(n):
            r,h=step(q)
            expected.setdefault((r,h),set()).add(q)
        for (r,h), qs in expected.items():
            got=set(predecessors(r,h))
            assert got == qs, (n,r,h,got^qs)
    return True


def survey(max_m=12,max_depth=4):
    rows=[]
    for m in range(2,max_m+1):
        for kind in ('fibonacci','binary'):
            r=((11,)+(9,)*(2*m-2)+(11,)) if kind=='fibonacci' else ((5,)+(10,)*(2*m-1)+(5,))
            h=0 if kind=='fibonacci' else 1
            ps=tuple(predecessors(r,h))
            counts=[len(ps)]
            for d in range(1,max_depth+1):
                counts.append(sum(image_depth_at_least(p,d) for p in ps))
            rows.append(dict(kind=kind,half_width=m,target=list(r),counts_by_incoming_depth=counts))
            print(rows[-1],flush=True)
    return rows


if __name__=='__main__':
    validate()
    rows=survey()
    with open('astra_counting_image_depth_results.json','w') as f:
        json.dump(dict(validation='exhaustive through input width 6',rows=rows),f,indent=2)
