#!/usr/bin/env python3
"""Rebuild the small correlated lift from full prefixes and integer sums.

No producer module is imported.  Every local control is realized by a
whole symmetric word.  Reachability trims width five; a Kahn ordering and
strictly decreasing sink ranks certify the width-six DAG.  All raw graphs
and arithmetic controls are retained in the output JSON.
"""

from collections import deque
from hashlib import sha256
from pathlib import Path
import gzip
import json
import struct


HERE = Path(__file__).resolve().parent
CLOCK = (0, 0, 1, 0, 1, 0, 1)
PREFIXES = ((4, 4, 0, 3), (8, 8, 0, 6), (16, 16, 0, 13),
            (7, 14, 7, 4), (15, 8, 15, 9), (6, 14, 14, 5),
            (13, 9, 9, 12))


def decimal_digits(n):
    out = []
    while n:
        n, digit = divmod(n, 10)
        out.append(digit)
    return out


def literal_transition(prefix, incoming):
    q = prefix + (18 * incoming,) + tuple(reversed(prefix))
    n = sum(a * 10**i for i, a in enumerate(q))
    digits = decimal_digits(n)
    width = len(prefix)
    high_start = width + 1
    carry = sum(a * 10**i for i, a in enumerate(q[:high_start])) // 10**high_start
    assert carry == incoming
    out = tuple(a + b for a, b in zip(digits, reversed(digits)))
    return out[:width], len(digits) - len(q), q, digits


def initial_graph():
    vertices = [(t, p) for t, p in enumerate(PREFIXES)]
    edges, controls = [], []
    for t, p in vertices:
        for c in (0, 1):
            out, overflow, q, digits = literal_transition(p, c)
            accepted = out == PREFIXES[(t + 1) % 7] and overflow == CLOCK[t]
            controls.append(dict(source=t, incoming=c, word=q, digits=digits,
                                 next_prefix=out, overflow=overflow, accepted=accepted))
            if accepted:
                edges.append((t, (t + 1) % 7, c))
    return vertices, edges, controls


def lift(vertices, edges):
    # The vertex stores the entire actual prefix, not merely its last digit.
    child_vertices = [(t, p + (a,)) for t, p in vertices for a in range(19)]
    index = {v: i for i, v in enumerate(child_vertices)}
    parent_index = {v: i for i, v in enumerate(vertices)}
    parent_edges = set(edges)
    child_edges, controls = [], []
    for source, (t, p) in enumerate(child_vertices):
        for c in (0, 1):
            out, overflow, q, digits = literal_transition(p, c)
            target = index.get(((t + 1) % 7, out))
            # Compute the carry entering the old high prefix from the whole
            # literal coefficient integer, independently of (a+c)//10.
            high_parent_start = len(p) + 2
            gamma = sum(a * 10**i for i, a in enumerate(q[:high_parent_start])) // 10**high_parent_start
            parent_source = parent_index[t, p[:-1]]
            parent_target = parent_index.get(((t + 1) % 7, out[:-1]))
            accepted = (overflow == CLOCK[t] and target is not None
                        and (parent_source, parent_target, gamma) in parent_edges)
            controls.append(dict(source=source, incoming=c, word=q, digits=digits,
                                 next_prefix=out, overflow=overflow,
                                 parent_carry=gamma, accepted=accepted))
            if accepted:
                child_edges.append((source, target, c))
    return child_vertices, child_edges, controls


def cyclic_vertices(vertices, edges):
    successors = [[] for _ in vertices]
    for a, b, _ in edges:
        successors[a].append(b)
    cyclic = []
    for root in range(len(vertices)):
        reached, stack = set(), list(successors[root])
        while stack:
            v = stack.pop()
            if v in reached:
                continue
            reached.add(v)
            stack.extend(successors[v])
        if root in reached:
            cyclic.append(root)
    return cyclic


def trim(vertices, edges):
    keep = cyclic_vertices(vertices, edges)
    remap = {v: i for i, v in enumerate(keep)}
    return ([vertices[v] for v in keep],
            [(remap[a], remap[b], c) for a, b, c in edges if a in remap and b in remap],
            keep)


def kahn_certificate(vertices, edges):
    successors = [[] for _ in vertices]
    indegree = [0] * len(vertices)
    for a, b, _ in edges:
        successors[a].append(b)
        indegree[b] += 1
    queue = deque(v for v, deg in enumerate(indegree) if deg == 0)
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for w in successors[v]:
            indegree[w] -= 1
            if indegree[w] == 0:
                queue.append(w)
    assert len(order) == len(vertices), 'A directed cycle survived.'
    position = {v: i for i, v in enumerate(order)}
    assert all(position[a] < position[b] for a, b, _ in edges)
    ranks = [0] * len(vertices)
    for v in reversed(order):
        ranks[v] = max((ranks[w] + 1 for w in successors[v]), default=0)
    assert all(ranks[a] > ranks[b] for a, b, _ in edges)
    return order, ranks


def read_checkpoint(width, expected_vertices, expected_edges, previous_vertices=None):
    path = HERE / ('lift_width_%02d.bin.gz' % width)
    data = gzip.decompress(path.read_bytes())
    assert data[:8] == b'P196LFT1'
    w, n, m = struct.unpack_from('<III', data, 8)
    assert w == width
    offset = 20
    decoded = []
    for _ in range(n):
        phase, last, low, parent = struct.unpack_from('<BBBI', data, offset)
        offset += 7
        prefix = PREFIXES[phase] if previous_vertices is None else previous_vertices[parent][1] + (last,)
        carry = sum(a * 10**i for i, a in enumerate(prefix)) // 10**width
        assert low == carry and prefix[-1] == last
        decoded.append((phase, prefix))
    edges = []
    for _ in range(m):
        edges.append(struct.unpack_from('<IIB', data, offset))
        offset += 9
    assert offset == len(data)
    assert decoded == expected_vertices
    assert sorted(edges) == sorted(expected_edges)
    return dict(filename=path.name, sha256=sha256(path.read_bytes()).hexdigest(),
                vertices=n, edges=m)


def main():
    reports, hashes = [], {}
    vertices4, edges4, controls4 = initial_graph()
    assert len(vertices4) == 7 and len(edges4) == 9
    hashes['width4'] = read_checkpoint(4, vertices4, edges4)
    vertices5, edges5, controls5 = lift(vertices4, edges4)
    trimmed5, trimmed_edges5, keep5 = trim(vertices5, edges5)
    assert (len(vertices5), len(edges5), len(trimmed5), len(trimmed_edges5)) == (133, 171, 21, 33)
    hashes['width5'] = read_checkpoint(5, trimmed5, trimmed_edges5, vertices4)
    vertices6, edges6, controls6 = lift(trimmed5, trimmed_edges5)
    assert (len(vertices6), len(edges6)) == (399, 627)
    order, ranks = kahn_certificate(vertices6, edges6)
    assert cyclic_vertices(vertices6, edges6) == []
    hashes['width6'] = read_checkpoint(6, [], [], trimmed5)
    for width, vs, es, controls, keep in ((4, vertices4, edges4, controls4, list(range(7))),
                                       (5, vertices5, edges5, controls5, keep5),
                                       (6, vertices6, edges6, controls6, [])):
        reports.append(dict(width=width, vertices=vs, edges=es, raw_controls=controls,
                            cyclic_vertex_indices=keep))
    result = dict(status='PASS_EMPTY_AT_WIDTH6', checkpoints=hashes,
                  literal_controls=len(controls4) + len(controls5) + len(controls6),
                  graphs=reports, width6_topological_order=order, width6_sink_ranks=ranks,
                  width6_longest_path_edges=max(ranks),
                  producer_source_sha256=sha256((HERE / 'spatial_lift.py').read_bytes()).hexdigest(),
                  producer_report_sha256=sha256((HERE / 'spatial_lift.json').read_bytes()).hexdigest(),
                  scope='Complete necessary local relations and finite DAG certificate; no arbitrary temporal carry realization is assumed.')
    (HERE / 'independent_lift_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('graphs', 'width6_topological_order', 'width6_sink_ranks')}))


if __name__ == '__main__':
    main()
