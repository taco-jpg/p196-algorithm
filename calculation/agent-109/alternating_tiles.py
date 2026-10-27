#!/usr/bin/env python3
"""Exact finite experiments with Agent9.AlternatingScalarBoundary.Tile.

This is the paired-time no-overflow/overflow spatial relation, not a new
certificate checker.  A relaxed slot path requires a separate physical
boundary/carry audit before it can be interpreted as an exterior B cycle.
"""
from collections import defaultdict
from itertools import product
import argparse

OUTSIDE = (0, 0, 0, 0)
SLOTS = tuple(product((0, 1), (0, 1), (0, 1), range(-1, 10)))
NEUTRAL = frozenset((a, b, 1-a, 10*b-1) for a, b in product((0, 1), repeat=2))

# Constant-in-time slots forming a closed spatial walk.  The neutral start
# satisfies the genuine overflow flip b_j = 1 - a_(j+1).  The walk deliberately
# does not contain the physical outside slot, so it is not an exterior cycle.
NEUTRAL_SPATIAL_CYCLE = (
    (0, 1, 1, 9), (1, 0, 0, 0), (0, 1, 1, 6), (1, 0, 1, 5),
    (1, 0, 1, 8), (1, 0, 0, 3), (0, 1, 0, 1), (0, 1, 0, 4),
)
NEUTRAL_CYCLE_Q = (10, 7, 12, 13, 11, 5, 7, 4)
NEUTRAL_CYCLE_R = (0, 16, 5, 8, 3, 11, 14, 9)
NEUTRAL_CYCLE_E = (0, 1, 0, 0, 0, 1, 1, 0)


def valid(s):
    return s[0] in (0, 1) and s[1] in (0, 1) and s[2] in (0, 1) and -1 <= s[3] <= 9


def tile(x, y, q, r, e, q_next):
    """Literal translation of the Lean Tile fields, with next-q bounded."""
    return (valid(x) and valid(y) and 0 <= q <= 18 and 0 <= r <= 18
            and e in (0, 1) and 0 <= q_next <= 18
            and r == y[3] + 10*e
            and (r >= 9 or e == 0) and (r <= 9 or e == 1)
            and (q+x[0])//10 == y[0]
            and (q+x[0])%10 + (q+y[2])%10 == r
            and (r+x[1])//10 == y[1]
            and x[2] == (q+y[2])//10
            and q_next == (r+x[1])%10 + x[3] + e
            and 0 <= x[3]+e <= 9)


def tiles():
    """Generate by the column arithmetic and replay the literal predicate."""
    result = []
    for x in SLOTS:
        for q in range(19):
            for high_in in (0, 1):
                if (q+high_in)//10 != x[2]:
                    continue
                a = (q+x[0])//10
                r = (q+x[0])%10 + (q+high_in)%10
                b = (r+x[1])//10
                for e in (0, 1):
                    y = (a, b, high_in, r-10*e)
                    q_next = (r+x[1])%10 + x[3] + e
                    if tile(x, y, q, r, e, q_next):
                        result.append((x, y, q, r, e, q_next))
    return tuple(result)


def components(vertices, edges):
    """Iterative Kosaraju; component IDs suffice for recurrent-edge tests."""
    adjacency = defaultdict(list)
    reverse = defaultdict(list)
    for a, b in edges:
        adjacency[a].append(b)
        reverse[b].append(a)
    visited = set()
    finish = []
    for start in vertices:
        if start in visited:
            continue
        visited.add(start)
        stack = [(start, iter(adjacency[start]))]
        while stack:
            v, iterator = stack[-1]
            try:
                w = next(iterator)
            except StopIteration:
                finish.append(v)
                stack.pop()
                continue
            if w not in visited:
                visited.add(w)
                stack.append((w, iter(adjacency[w])))
    component = {}
    index = 0
    for start in reversed(finish):
        if start in component:
            continue
        component[start] = index
        stack = [start]
        while stack:
            for w in reverse[stack.pop()]:
                if w not in component:
                    component[w] = index
                    stack.append(w)
        index += 1
    return component


def alphabet_predecessor(alphabet, table):
    eligible = [t for t in table if t[1] in alphabet]
    comp = components(range(19), ((t[2], t[5]) for t in eligible))
    recurrent = [t for t in eligible if comp[t[2]] == comp[t[5]]]
    return frozenset(t[0] for t in recurrent), recurrent


def neutral_fiber_check(table):
    count = 0
    for x, y, q, r, e, q_next in table:
        if y not in NEUTRAL:
            continue
        a, b = y[:2]
        assert r == 9 and e == 1-b
        assert x[:2] == (a, b)
        assert q == 4+5*(a+x[2])
        assert q_next == x[3]+10*(1-b)
        count += 1
    return count


def flip_fiber_fixture(a, c):
    """Every bit pair of cyclic traces gives a valid neutral predecessor.

    Inner: N_j=(a_j,1-a_(j+1),1-a_j,9-10*a_(j+1)).
    Outer: X_j=(a_j,1-a_(j+1),c_j,4+5*(c_(j+1)-a_(j+1))).
    Tile coefficients are q_j=4+5*(a_j+c_j), r_j=9, e_j=a_(j+1).
    """
    if not a or len(a) != len(c) or any(bit not in (0,1) for bit in (*a,*c)):
        raise ValueError('two nonempty equally long binary traces are required')
    result = []
    for j in range(len(a)):
        k = (j+1)%len(a)
        inner = (a[j],1-a[k],1-a[j],9-10*a[k])
        outer = (a[j],1-a[k],c[j],4+5*(c[k]-a[k]))
        q = 4+5*(a[j]+c[j])
        q_next = 4+5*(a[k]+c[k])
        row = (outer,inner,q,9,a[k],q_next)
        if not tile(*row):
            raise AssertionError(row)
        result.append(row)
    return tuple(result)


def counterexample_check():
    count = 0
    for m in range(1,7):
        for bits in product((0,1),repeat=2*m):
            count += len(flip_fiber_fixture(bits[:m],bits[m:]))
    print('flip_fiber_local_checks',count)
    cycle = NEUTRAL_SPATIAL_CYCLE
    for i,x in enumerate(cycle):
        y = cycle[(i+1)%len(cycle)]
        q,r,e = NEUTRAL_CYCLE_Q[i],NEUTRAL_CYCLE_R[i],NEUTRAL_CYCLE_E[i]
        if not tile(x,y,q,r,e,q):
            raise AssertionError((i,x,y,q,r,e))
        print('tile',i,'outer',x,'inner',y,'q',q,'r',r,'e',e,'qNext',q)
    if cycle[0] not in NEUTRAL or OUTSIDE in cycle:
        raise AssertionError('wrong interpretation of the spatial example')
    if any(s in NEUTRAL for s in cycle[1:]):
        raise AssertionError('intervening slots were meant to be nonneutral')
    print('CONSTANT_TEMPORAL_TRACE_SPATIAL_CYCLE',len(cycle))
    print('TWO_COLUMN_ERASURE_COUNTEREXAMPLE',cycle[-2],cycle[-1],cycle[0])
    print('PHYSICAL_OUTSIDE_NOT_REACHED; NOT_A_B_CYCLE_OR_CERTIFICATE')


def sofic_predecessor(edges, table, cap):
    """Exact inverse image of a labelled temporal graph under one Tile column.

    Every edge (u,v,label) represents the slot at one paired time.  State
    products retain the complete old temporal memory and q at this column.
    Cyclic SCC pruning preserves exactly the periodic temporal traces.
    """
    by_inner = defaultdict(list)
    for x, y, q, r, e, q_next in table:
        by_inner[y].append((x, q, q_next, r, e))
    new = set()
    physical = set()
    for u, v, y in edges:
        for x, q, q_next, r, e in by_inner[y]:
            arc = (19*u+q, 19*v+q_next, x)
            new.add(arc)
            if x == OUTSIDE and e == 1 and q > 0:
                physical.add(arc)
        if len(new) > cap:
            return None, None, len(new)
    vertices = set()
    for u, v, _ in new:
        vertices.add(u)
        vertices.add(v)
    comp = components(vertices, ((u,v) for u,v,_ in new))
    new = {(u,v,x) for u,v,x in new if comp[u] == comp[v]}
    physical &= new
    vertices = sorted({u for u,_,_ in new} | {v for _,v,_ in new})
    renumber = {v:i for i,v in enumerate(vertices)}
    return ({(renumber[u],renumber[v],x) for u,v,x in new},
            {(renumber[u],renumber[v],x) for u,v,x in physical}, len(vertices))


def has_cycle(edges):
    vertices = {u for u,v,x in edges} | {v for u,v,x in edges}
    comp = components(vertices, ((u,v) for u,v,_ in edges))
    return any(comp[u] == comp[v] for u,v,_ in edges)


def sofic_experiment(table, max_depth, cap):
    edges = {(0,0,n) for n in NEUTRAL}
    for depth in range(1,max_depth+1):
        edges, physical, count = sofic_predecessor(edges, table, cap)
        if edges is None:
            print('depth',depth,'CAPPED',count,flush=True)
            break
        relaxed = {e for e in edges if e[2] == OUTSIDE}
        print('depth',depth,'vertices',count,'edges',len(edges),
              'outside_edges',len(relaxed),'relaxed_outside_cycle',has_cycle(relaxed),
              'physical_outside_cycle',has_cycle(physical),flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sofic-depth',type=int,default=0)
    parser.add_argument('--edge-cap',type=int,default=1000000)
    parser.add_argument('--counterexample',action='store_true')
    args = parser.parse_args()
    table = tiles()
    print('tiles', len(table), 'neutral_fiber_tiles', neutral_fiber_check(table))
    if args.counterexample:
        counterexample_check()
        return
    if args.sofic_depth:
        sofic_experiment(table, args.sofic_depth, args.edge_cap)
        return
    alphabet = NEUTRAL
    seen = set()
    for depth in range(20):
        print('depth', depth, 'alphabet_size', len(alphabet), 'outside', OUTSIDE in alphabet)
        if alphabet in seen:
            print('ALPHABET_PROJECTION_REPEATED')
            break
        seen.add(alphabet)
        alphabet, _ = alphabet_predecessor(alphabet, table)


if __name__ == '__main__':
    main()
