#!/usr/bin/env python3
"""Independent literal-integer reconstruction of the full six-column DAG.

No graph-generator module is imported.  Both accepted and rejected local
controls are preserved.  An independent source-deletion topological sort
recomputes every sink rank in the producer's complete certificate.
"""

from collections import deque
from hashlib import sha256
from pathlib import Path
import gzip
import json
import struct


HERE = Path(__file__).resolve().parent
PREFIXES = ((4, 4, 0), (8, 8, 0), (16, 16, 0), (7, 14, 7),
            (15, 8, 15), (6, 14, 14), (13, 9, 9))
CLOCK = (0, 0, 1, 0, 1, 0, 1)
PHASE_SIZE = 19**3
VERTICES = 7 * PHASE_SIZE


def normalize_literal(q):
    n = sum(a * 10**i for i, a in enumerate(q))
    digits = []
    while n:
        n, d = divmod(n, 10)
        digits.append(d)
    return digits


def next_pair(q):
    d = normalize_literal(q)
    return tuple(a + b for a, b in zip(d, reversed(d)))


def decode(vertex):
    phase, rest = divmod(vertex, PHASE_SIZE)
    a, rest = divmod(rest, 19**2)
    b, c = divmod(rest, 19)
    return phase, PREFIXES[phase] + (a, b, c)


def encode(phase, p):
    a, b, c = p[-3:]
    return phase * PHASE_SIZE + a * 19**2 + b * 19 + c


def main():
    report_path = HERE / 'direct_six_graph.json'
    certificate_path = HERE / 'direct_six_graph.bin.gz'
    report = json.loads(report_path.read_text())
    certificate = gzip.decompress(certificate_path.read_bytes())
    assert certificate[:8] == b'P196DAG1'
    vertices, edges_count = struct.unpack_from('<II', certificate, 8)
    assert vertices == VERTICES
    producer_ranks = list(struct.unpack_from('<' + 'I' * vertices, certificate, 16))
    edge_offset = 16 + 4 * vertices
    producer_edges = [struct.unpack_from('<IIB', certificate, edge_offset + 9 * i)
                      for i in range(edges_count)]
    assert edge_offset + 9 * edges_count == len(certificate)
    controls = bytearray(b'P196INT1')
    controls.extend(struct.pack('<I', 2 * VERTICES))
    edges = []
    successors = [[] for _ in range(VERTICES)]
    indegree = [0] * VERTICES
    counts = [[dict(accepted=0, rejected=0) for _ in range(2)] for _ in range(7)]
    for source in range(VERTICES):
        phase, p = decode(source)
        for incoming in (0, 1):
            # This center forces the carry entering the high prefix.
            q = p + (18 * incoming,) + tuple(reversed(p))
            d = normalize_literal(q)
            carry = sum(a * 10**i for i, a in enumerate(q[:7])) // 10**7
            assert carry == incoming
            out = tuple(a + b for a, b in zip(d, reversed(d)))[:6]
            overflow = len(d) - len(q)
            controls.extend(bytes(out + (overflow,)))
            accepted = out[:3] == PREFIXES[(phase + 1) % 7] and overflow == CLOCK[phase]
            counts[phase][incoming]['accepted' if accepted else 'rejected'] += 1
            if accepted:
                target = encode((phase + 1) % 7, out)
                edges.append((source, target, incoming))
                successors[source].append(target)
                indegree[target] += 1
    assert edges == producer_edges
    assert counts == report['controls_by_phase_and_input']

    # The producer deletes sinks; this audit independently deletes sources.
    queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for w in successors[v]:
            indegree[w] -= 1
            if indegree[w] == 0:
                queue.append(w)
    assert len(order) == VERTICES
    positions = [0] * VERTICES
    for i, v in enumerate(order):
        positions[v] = i
    assert all(positions[a] < positions[b] for a, b, _ in edges)
    ranks = [0] * VERTICES
    for v in reversed(order):
        ranks[v] = max((1 + ranks[w] for w in successors[v]), default=0)
    assert ranks == producer_ranks
    maxima = [max(ranks[t * PHASE_SIZE:(t + 1) * PHASE_SIZE]) for t in range(7)]
    assert maxima == report['max_path_edges_by_phase'] == [26, 25, 24, 26, 25, 28, 27]
    assert all(ranks[a] > ranks[b] for a, b, _ in edges)

    edge_set = set(edges)
    witness = report['phase0_longest_path']
    assert len(witness) - 1 == maxima[0]
    for i, row in enumerate(witness):
        phase, p = decode(row['vertex'])
        assert phase == row['phase'] and list(p) == row['prefix']
        assert ranks[row['vertex']] == row['rank'] == maxima[0] - i
        if i + 1 < len(witness):
            assert (row['vertex'], witness[i + 1]['vertex'], row['incoming_carry']) in edge_set

    # This is an actual whole-word trajectory, unlike a freely chosen graph path.
    q = (4, 4, 0) + (1, 1, 14, 16, 14, 1, 1) + (0, 4, 4)
    actual = []
    for t in range(29):
        phase = t % 7
        matches = q[:3] == PREFIXES[phase]
        normalized = normalize_literal(q)
        overflow = len(normalized) - len(q)
        actual.append(dict(time=t, pair_word=q, prescribed_prefix=PREFIXES[phase],
                           prefix_matches=matches,
                           actual_overflow=overflow, prescribed_overflow=CLOCK[phase],
                           first_six_rank=ranks[encode(phase, q[:6])] if matches else None,
                           next_iterate_palindromic=normalized == normalized[::-1]))
        q = next_pair(q)
    assert all(row['prefix_matches'] for row in actual[:27])
    assert all(row['actual_overflow'] == row['prescribed_overflow'] for row in actual[:26])
    assert not actual[27]['prefix_matches']
    assert [actual[t]['pair_word'][:3] for t in (7, 14, 21)] == [(4, 4, 0)] * 3
    assert actual[28]['pair_word'][:3] != (4, 4, 0)
    assert all(not row['next_iterate_palindromic'] for row in actual[:28])

    controls_path = HERE / 'independent_direct_controls.bin.gz'
    with controls_path.open('wb') as raw:
        with gzip.GzipFile(fileobj=raw, mode='wb', mtime=0, filename='') as stream:
            stream.write(controls)
    result = dict(status='PASS_COMPLETE_DAG', literal_controls=2 * VERTICES,
                  vertices=VERTICES, edges=len(edges), source_deleted_vertices=len(order),
                  max_path_edges_by_phase=maxima, maximum_complete_seven_step_returns=3,
                  producer_certificate_sha256=sha256(certificate_path.read_bytes()).hexdigest(),
                  producer_report_sha256=sha256(report_path.read_bytes()).hexdigest(),
                  producer_source_sha256=sha256((HERE / 'direct_six_graph.py').read_bytes()).hexdigest(),
                  controls_artifact=dict(filename=controls_path.name,
                                         sha256=sha256(controls_path.read_bytes()).hexdigest(),
                                         magic='P196INT1', header='uint32 number of controls',
                                         control_order='2*vertex+incoming, with producer vertex encoding',
                                         control_payload='7 uint8: six next pair coefficients, final overflow',
                                         word='prefix + [18*incoming] + reversed(prefix)',
                                         byte_order='little endian'),
                  actual_sharpness_example=actual,
                  scope='All local controls, all edges and ranks checked independently. Actual example attains three safe returns; arbitrary graph paths need not be actual trajectories.')
    (HERE / 'independent_direct_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'actual_sharpness_example'}))


if __name__ == '__main__':
    main()
