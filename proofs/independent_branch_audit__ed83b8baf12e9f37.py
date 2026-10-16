#!/usr/bin/env python3
"""Literal-integer and independent-Tarjan audit of every broader-44 lift.

All checkpoints are decoded, all raw vertices and control outcomes are
checked, and every recurrent part is recomputed without importing the
producer.  The final empty recurrent graph has a separate Kahn certificate.
"""

from collections import Counter, deque
from hashlib import sha256
from pathlib import Path
import gzip
import json
import struct
import sys


HERE = Path(__file__).resolve().parent
CLOCK = (0, 0, 1, 0, 1, 0, 1)
NONE = 2**32 - 1
sys.setrecursionlimit(100000)


def read_graph(filename, previous, base):
    path = HERE / filename
    data = gzip.decompress(path.read_bytes())
    assert data[:8] == b'P196BRC1'
    width, count, n_edges = struct.unpack_from('<III', data, 8)
    offset, vertices, metadata = 20, [], []
    for i in range(count):
        phase, last, low, parent = struct.unpack_from('<BBBI', data, offset)
        offset += 7
        if width == 2:
            assert parent == NONE
            prefix = tuple(base[i][1])
            assert phase == base[i][0]
        else:
            assert parent < len(previous)
            prefix = previous[parent][1] + (last,)
            assert phase == previous[parent][0]
        assert last == prefix[-1]
        assert low == sum(a * 10**i for i, a in enumerate(prefix)) // 10**width
        vertices.append((phase, prefix))
        metadata.append((phase, last, low, parent))
    edges = [struct.unpack_from('<IIB', data, offset + 9 * i) for i in range(n_edges)]
    assert offset + 9 * n_edges == len(data)
    assert len(set(edges)) == len(edges)
    assert all(a < count and b < count and c in (0, 1) for a, b, c in edges)
    return vertices, edges, metadata, sha256(path.read_bytes()).hexdigest()


def literal(prefix, incoming):
    width = len(prefix)
    q = prefix + (18 * incoming,) + tuple(reversed(prefix))
    value = sum(a * 10**i for i, a in enumerate(q))
    c = sum(a * 10**i for i, a in enumerate(q[:width + 1])) // 10**(width + 1)
    assert c == incoming
    gamma = sum(a * 10**i for i, a in enumerate(q[:width + 2])) // 10**(width + 2)
    digits = []
    while value:
        value, digit = divmod(value, 10)
        digits.append(digit)
    out = tuple(a + b for a, b in zip(digits, reversed(digits)))[:width]
    return out, len(digits) - len(q), gamma


def tarjan(vertices, edges):
    successors = [[] for _ in vertices]
    for a, b, _ in edges:
        successors[a].append(b)
    index = [-1] * len(vertices)
    low = [0] * len(vertices)
    stack, active, groups = [], set(), []
    counter = 0

    def visit(v):
        nonlocal counter
        index[v] = low[v] = counter
        counter += 1
        stack.append(v)
        active.add(v)
        for w in successors[v]:
            if index[w] == -1:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in active:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            group = []
            while True:
                w = stack.pop()
                active.remove(w)
                group.append(w)
                if w == v:
                    break
            groups.append(sorted(group))

    for v in range(len(vertices)):
        if index[v] == -1:
            visit(v)
    groups.sort()
    cyclic = [g for g in groups if len(g) > 1 or g[0] in successors[g[0]]]
    keep = sorted(v for g in cyclic for v in g)
    return groups, cyclic, keep


def dag_certificate(count, edges):
    successors = [[] for _ in range(count)]
    indegree = [0] * count
    for a, b, _ in edges:
        successors[a].append(b)
        indegree[b] += 1
    queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for w in successors[v]:
            indegree[w] -= 1
            if indegree[w] == 0:
                queue.append(w)
    assert len(order) == count
    ranks = [0] * count
    for v in reversed(order):
        ranks[v] = max((ranks[w] + 1 for w in successors[v]), default=0)
    assert all(ranks[a] > ranks[b] for a, b, _ in edges)
    return order, ranks


def main():
    report_path = HERE / 'branching_lift.json'
    report = json.loads(report_path.read_text())
    assert report['status'] == 'EMPTY_AT_FINITE_WIDTH'
    base = report['base_vertices']
    previous, previous_edges = None, None
    layers, all_controls, total_controls = [], bytearray(b'P196BIA1'), 0
    all_controls.extend(struct.pack('<I', len(report['completed_graphs'])))
    for row in report['completed_graphs']:
        width = row['width']
        vs, es, meta, raw_hash = read_graph(row['raw_artifact']['filename'], previous, base)
        assert raw_hash == row['raw_artifact']['sha256']
        if previous is not None:
            assert vs == [(phase, p + (a,)) for phase, p in previous for a in range(19)]
        index = {v: i for i, v in enumerate(vs)}
        assert len(index) == len(vs)
        parent_index = {v: i for i, v in enumerate(previous or [])}
        parent_edges = set(previous_edges or [])
        rebuilt = []
        all_controls.extend(struct.pack('<II', width, 2 * len(vs)))
        for source, (phase, p) in enumerate(vs):
            for incoming in (0, 1):
                out, overflow, gamma = literal(p, incoming)
                target = index.get(((phase + 1) % 7, out))
                accepted = overflow == CLOCK[phase] and target is not None
                if previous is not None:
                    parent_source = parent_index[phase, p[:-1]]
                    parent_target = parent_index.get(((phase + 1) % 7, out[:-1]))
                    accepted = accepted and (parent_source, parent_target, gamma) in parent_edges
                all_controls.extend(bytes(out + (overflow, int(accepted))))
                total_controls += 1
                if accepted:
                    rebuilt.append((source, target, incoming))
        assert sorted(rebuilt) == sorted(es), width
        groups, cyclic, keep = tarjan(vs, es)
        remap = {v: i for i, v in enumerate(keep)}
        retained_vs = [vs[v] for v in keep]
        retained_edges = [(remap[a], remap[b], c) for a, b, c in es if a in remap and b in remap]
        saved_vs, saved_edges, saved_meta, retained_hash = read_graph(
            row['retained_artifact']['filename'], previous, base)
        assert saved_vs == retained_vs and saved_meta == [meta[v] for v in keep]
        assert sorted(saved_edges) == sorted(retained_edges)
        assert retained_hash == row['retained_artifact']['sha256']
        sizes = {str(k): v for k, v in sorted(Counter(map(len, cyclic)).items())}
        assert (len(vs), len(es), len(groups), len(cyclic), sizes,
                len(saved_vs), len(saved_edges)) == (
                    row['raw_vertices'], row['raw_edges'], row['components'],
                    row['cyclic_components'], row['cyclic_component_size_counts'],
                    row['retained_vertices'], row['retained_edges'])
        layers.append(dict(width=width, vertices=len(vs), edges=len(es),
                           recurrent_vertices=len(saved_vs), recurrent_edges=len(saved_edges),
                           raw_sha256=raw_hash, recurrent_sha256=retained_hash,
                           components=groups, cyclic_components=cyclic,
                           recurrent_raw_vertex_indices=keep))
        previous, previous_edges = saved_vs, saved_edges
        if not saved_vs:
            order, ranks = dag_certificate(len(vs), es)
            layers[-1].update(topological_order=order, sink_ranks=ranks,
                              maximum_path_edges=max(ranks, default=0))
        print(json.dumps({k: layers[-1][k] for k in (
            'width', 'vertices', 'edges', 'recurrent_vertices', 'recurrent_edges')}), flush=True)
    assert not previous and layers[-1]['width'] == 14
    controls_path = HERE / 'independent_branch_controls.bin.gz'
    with controls_path.open('wb') as raw:
        with gzip.GzipFile(fileobj=raw, mode='wb', filename='', mtime=0) as stream:
            stream.write(all_controls)
    result = dict(status='PASS_EMPTY_AT_WIDTH14', literal_controls=total_controls,
                  layers=layers,
                  producer_source_sha256=sha256((HERE / 'branching_lift.py').read_bytes()).hexdigest(),
                  producer_report_sha256=sha256(report_path.read_bytes()).hexdigest(),
                  controls_artifact=dict(filename=controls_path.name,
                                         sha256=sha256(controls_path.read_bytes()).hexdigest(),
                                         magic='P196BIA1', byte_order='little endian',
                                         header='uint32 number_of_layers',
                                         layer_header='uint32 width,number_of_controls',
                                         control_order='2*raw_vertex+incoming',
                                         control_payload='width uint8 output coefficients, uint8 overflow, uint8 accepted',
                                         input_word='full_prefix + [18*incoming] + reversed(full_prefix)'),
                  scope='All three returning branches and all labeled parent correlations retained. Local realization is not temporal path realization.')
    (HERE / 'independent_branch_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'layers'}))


if __name__ == '__main__':
    main()
