"""Exact closure checking for integer-valued additive folded-word scores.

For fixed weights, this decides whether a canonical decimal pair word w can
have S(w) >= 1 and S(qstep(w)) <= 0.  It does NOT synthesize a score or establish
safety; the caller must separately prove that S > 0 excludes bad words.

The finite folded transducer is augmented by the previous input/output digit
categories. An accepting path is represented by nonnegative integer edge
multiplicities, unit source/sink flow, and a rank certificate making every used
vertex reachable from the source through used edges. These conditions are
equivalent to existence of an Euler trail through the resulting directed
multigraph. In particular, disconnected cycles cannot produce fake witnesses.
UNSAT therefore covers every finite length. A timeout yields UNKNOWN only.

Returned SAT words are reconstructed and independently checked using qstep.
The graph/transducer implementation remains Python, not a Lean formalization.
"""

from functools import lru_cache
from itertools import product
import time
import z3
import creative_regular_invariant as r
from creative_regular_direct import fst_graph


def cat(q):
    return 1 if q < 9 else 2 if q == 9 else 3


def score(weights, terminals, word):
    value, previous = 0, 0
    for q in word[0]:
        value += weights[previous][q]
        previous = cat(q)
    return value + terminals[previous][r.terminal_index(word[1])]


@lru_cache(maxsize=1)
def topology():
    fs, fe = fst_graph()
    outgoing = [[] for _ in fs]
    for a, q, s, b in fe:
        outgoing[a].append((q, s, b))
    states = [(0, 0, 0), (1, 0, 0)]
    ids = {st: i for i, st in enumerate(states)}
    edges, terminals = [], []
    for st in states:
        x, ia, oa = st
        u = ids[st]
        overflow, a, b, delay, started = fs[x]
        for center in [None] + list(range(0, 19, 2)):
            if not started and (center is None or center == 0):
                continue
            extra = None
            if center is None:
                if a != b:
                    continue
                oc = 2 * delay if overflow else None
            else:
                if r.C(center, a) != b:
                    continue
                if overflow:
                    extra, oc = r.D(center, a) + delay, None
                else:
                    oc = 2 * r.D(center, a)
            terminals.append((u, ia, oa, center, extra, oc))
        for q, s, y in outgoing[x]:
            ns = y, cat(q), cat(s)
            if ns not in ids:
                ids[ns] = len(states)
                states.append(ns)
            edges.append((u, ids[ns], ia, oa, q, s))
    return states, edges, terminals


def weighted_graph(weights, terminals):
    states, trans, final = topology()
    source, sink = len(states), len(states) + 1
    # Edge: source, target, input cost, output cost, kind, data.
    edges = [(source, j, 0, 0, 'start', None) for j in (0, 1)]
    for u, v, ia, oa, q, s in trans:
        edges.append((u, v, weights[ia][q], weights[oa][s], 'pair', q))
    for u, ia, oa, center, extra, oc in final:
        output_cost = terminals[oa][r.terminal_index(oc)]
        if extra is not None:
            output_cost = weights[oa][extra] + terminals[cat(extra)][0]
        edges.append((u, sink, terminals[ia][r.terminal_index(center)],
                      output_cost, 'terminal', center))
    # Equal endpoints and costs are interchangeable for score existence; keep
    # a real transducer edge as representative so reconstruction stays valid.
    unique = {}
    for edge in edges:
        unique.setdefault(edge[:4], edge)
    return len(states) + 2, source, sink, list(unique.values())


def check(weights, terminals, seconds=30, max_witness=100000):
    """Return {'status': 'SAT'|'UNSAT'|'UNKNOWN', ...}.

    SAT supplies word, output, input_score, output_score. UNSAT is an exact
    all-length closure result, conditional on the supplied integer score.
    A SAT model longer than max_witness is conservatively returned UNKNOWN.
    """
    began = time.monotonic()
    assert len(weights) == len(terminals) == 4
    assert all(len(row) == 19 for row in weights)
    assert all(len(row) == 11 for row in terminals)
    assert all(type(x) is int for row in weights + terminals for x in row)
    # Cheap actual-word witnesses also keep routine CEGIS feedback short.
    # Failure of this search has no logical status; the unbounded solver below
    # is still required before reporting UNSAT.
    for length in range(3):
        for pairs in product(range(19), repeat=length):
            if pairs and pairs[0] == 0:
                continue
            for center in [None] + list(range(0, 19, 2)):
                word = pairs, center
                if not r.valid(word):
                    continue
                si = score(weights, terminals, word)
                if si < 1:
                    continue
                output = r.qstep(word)
                so = score(weights, terminals, output)
                if so <= 0:
                    return {'status': 'SAT', 'method': 'short witness',
                            'word': word, 'output': output,
                            'input_score': si, 'output_score': so,
                            'seconds': time.monotonic() - began}
    n, source, sink, edges = weighted_graph(weights, terminals)
    solver = z3.SolverFor('QF_LIA')
    count = [z3.Int('edge_%d' % j) for j in range(len(edges))]
    rank = [z3.Int('rank_%d' % v) for v in range(n)]
    incoming, outgoing = [[] for _ in range(n)], [[] for _ in range(n)]
    for j, (u, v, *_rest) in enumerate(edges):
        outgoing[u].append(j)
        incoming[v].append(j)
        solver.add(count[j] >= 0)
    solver.add(rank[source] == 0)
    for v in range(n):
        solver.add(rank[v] >= 0, rank[v] < n)
        solver.add(z3.Sum([count[j] for j in outgoing[v]]) -
                   z3.Sum([count[j] for j in incoming[v]]) ==
                   (1 if v == source else -1 if v == sink else 0))
        if v != source:
            used = z3.Or([count[j] > 0 for j in outgoing[v] + incoming[v]])
            parent = z3.Or([z3.And(count[j] > 0,
                                   rank[edges[j][0]] < rank[v])
                            for j in incoming[v]])
            solver.add(z3.Implies(used, parent))
    solver.add(z3.Sum([count[j] * e[2] for j, e in enumerate(edges) if e[2]]) >= 1)
    solver.add(z3.Sum([count[j] * e[3] for j, e in enumerate(edges) if e[3]]) <= 0)
    remaining = seconds - (time.monotonic() - began)
    if remaining <= 0:
        return {'status': 'UNKNOWN', 'reason': 'construction timeout',
                'seconds': time.monotonic() - began}
    solver.set(timeout=max(1, int(1000 * remaining)))
    status = solver.check()
    result = {'status': str(status).upper(), 'seconds': time.monotonic() - began,
              'states': n, 'edges': len(edges)}
    if status == z3.unknown:
        result['reason'] = solver.reason_unknown()
        return result
    if status == z3.unsat:
        return result
    model = solver.model()
    multiplicities = [model.eval(x).as_long() for x in count]
    trail_length = sum(multiplicities)
    if trail_length > max_witness:
        result.update(status='UNKNOWN', reason='SAT trail exceeds reconstruction limit',
                      trail_length=trail_length)
        return result
    # Hierholzer's algorithm, retaining edge labels in the final Euler trail.
    remaining_counts = multiplicities[:]
    adjacency = [[j for j in row if remaining_counts[j]] for row in outgoing]
    stack, reverse_trail = [(source, None)], []
    while stack:
        u = stack[-1][0]
        while adjacency[u] and remaining_counts[adjacency[u][-1]] == 0:
            adjacency[u].pop()
        if adjacency[u]:
            j = adjacency[u][-1]
            remaining_counts[j] -= 1
            stack.append((edges[j][1], j))
        else:
            _v, j = stack.pop()
            if j is not None:
                reverse_trail.append(j)
    trail = reverse_trail[::-1]
    assert len(trail) == trail_length and not any(remaining_counts)
    current, pairs, center, ended = source, [], None, False
    for j in trail:
        u, v, _ic, _oc, kind, label = edges[j]
        assert u == current and not ended
        current = v
        if kind == 'pair':
            pairs.append(label)
        elif kind == 'terminal':
            center, ended = label, True
    assert current == sink and ended
    word = tuple(pairs), center
    assert r.valid(word)
    output = r.qstep(word)
    input_score = score(weights, terminals, word)
    output_score = score(weights, terminals, output)
    assert input_score >= 1 and output_score <= 0
    assert sum(multiplicities[j] * e[2] for j, e in enumerate(edges)) == input_score
    assert sum(multiplicities[j] * e[3] for j, e in enumerate(edges)) == output_score
    result.update(word=word, output=output, input_score=input_score,
                  output_score=output_score, seconds=time.monotonic() - began)
    return result


if __name__ == '__main__':
    import json
    tests = [
        ('every word positive', [[0] * 19 for _ in range(4)], [[1] * 11 for _ in range(4)], 'UNSAT'),
        ('no word positive', [[0] * 19 for _ in range(4)], [[0] * 11 for _ in range(4)], 'UNSAT'),
        ('positive pair count', [[1] * 19 for _ in range(4)], [[0] * 11 for _ in range(4)], 'UNSAT'),
        ('only single digit positive', [[-1] * 19 for _ in range(4)], [[1] * 11 for _ in range(4)], 'SAT'),
    ]
    for name, w, t, expected in tests:
        answer = check(w, t, 30)
        print(json.dumps({'test': name, **answer}), flush=True)
        assert answer['status'] == expected
