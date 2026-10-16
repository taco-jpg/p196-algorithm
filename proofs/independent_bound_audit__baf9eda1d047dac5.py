#!/usr/bin/env python3
"""Check the weighted-SCC bound against independently obtained components.

Uses the previously retained independent Tarjan result, decodes every raw
edge again, and recomputes condensation ranks in a separate component
ordering.  No producer module is imported.
"""

from collections import deque
from hashlib import sha256
from pathlib import Path
import gzip
import json
import struct


HERE = Path(__file__).resolve().parent


def main():
    audit_path = HERE / 'independent_branch_audit.json'
    prior = json.loads(audit_path.read_text())
    assert prior['status'] == 'PASS_EMPTY_AT_WIDTH14'
    source = json.loads((HERE / 'branching_lift.json').read_text())
    report_path = HERE / 'finite_bound.json'
    report = json.loads(report_path.read_text())
    cert_path = HERE / report['certificate']['filename']
    assert sha256(cert_path.read_bytes()).hexdigest() == report['certificate']['sha256']
    cert_data = gzip.decompress(cert_path.read_bytes())
    assert sha256(cert_data).hexdigest() == report['certificate']['uncompressed_sha256']
    cert = json.loads(cert_data)
    next_bound, records, total_components = None, [], 0
    for graph_row, audit, claim in reversed(list(zip(source['completed_graphs'], prior['layers'], cert['records']))):
        width = graph_row['width']
        assert width == audit['width'] == claim['width']
        raw_path = HERE / graph_row['raw_artifact']['filename']
        assert sha256(raw_path.read_bytes()).hexdigest() == audit['raw_sha256']
        raw = gzip.decompress(raw_path.read_bytes())
        w, n, m = struct.unpack_from('<III', raw, 8)
        assert (w, n, m) == (width, claim['vertices'], claim['edges'])
        phases = [raw[20 + 7 * i] for i in range(n)]
        es = [struct.unpack_from('<IIB', raw, 20 + 7 * n + 9 * i) for i in range(m)]
        groups = audit['components']
        ids = [-1] * n
        for component, group in enumerate(groups):
            for v in group:
                assert ids[v] == -1
                ids[v] = component
        assert all(i >= 0 for i in ids)
        producer_ids = claim['component_of_vertex']
        producer_groups = [[] for _ in claim['component_sizes']]
        for v, i in enumerate(producer_ids):
            producer_groups[i].append(v)
        assert sorted(producer_groups) == groups
        cyclic_sets = {tuple(g) for g in audit['cyclic_components']}
        cyclic = [tuple(g) in cyclic_sets for g in groups]
        assert {tuple(producer_groups[i]) for i in claim['cyclic_components']} == cyclic_sets
        assert claim['next_level_vertex_bound'] == next_bound
        assert next_bound is not None or not any(cyclic)
        weights = [next_bound if c else 1 for c in cyclic]
        quotient = sorted({(ids[a], ids[b]) for a, b, _ in es if ids[a] != ids[b]})
        producer_quotient = sorted({(producer_ids[a], producer_ids[b]) for a, b, _ in es
                                   if producer_ids[a] != producer_ids[b]})
        assert producer_quotient == [tuple(e) for e in claim['condensation_edges']]
        successors = [[] for _ in groups]
        indegree = [0] * len(groups)
        for a, b in quotient:
            successors[a].append(b)
            indegree[b] += 1
        queue = deque(i for i, d in enumerate(indegree) if d == 0)
        order = []
        while queue:
            v = queue.popleft()
            order.append(v)
            for target in successors[v]:
                indegree[target] -= 1
                if indegree[target] == 0:
                    queue.append(target)
        assert len(order) == len(groups)
        ranks = [0] * len(groups)
        for v in reversed(order):
            ranks[v] = weights[v] + max((ranks[t] for t in successors[v]), default=0)
        for v in range(n):
            assert weights[ids[v]] == claim['component_weights'][producer_ids[v]]
            assert ranks[ids[v]] == claim['weighted_sink_ranks'][producer_ids[v]]
        bounds = [max((ranks[ids[v]] for v in range(n) if phases[v] == t), default=0)
                  for t in range(7)]
        next_bound = max(ranks, default=0)
        assert next_bound == claim['max_path_vertices_bound']
        assert bounds == claim['path_vertices_bound_by_start_phase']
        total_components += len(groups)
        records.append(dict(width=width, components=len(groups),
                            cyclic_components=sum(cyclic), vertex_bound=next_bound,
                            phase_vertex_bounds=bounds,
                            weighted_ranks_sha256=sha256(json.dumps(ranks).encode()).hexdigest()))
    records.reverse()
    initial_vertices = records[0]['phase_vertex_bounds'][0]
    assert initial_vertices == 1600
    initial_edges = initial_vertices - 1
    complete_returns = initial_edges // 7
    assert initial_edges == report['phase0_max_path_edges_bound'] == 1599
    assert complete_returns == report['max_complete_returns_at_width14_or_more'] == 228
    width_adjustments = {str(length): max(0, (14 - length + 2) // 3) for length in range(2, 18)}
    assert max(width_adjustments.values()) == 4
    assert complete_returns + 4 == report['max_complete_returns_at_all_widths_at_least2'] == 232
    result = dict(status='PASS_BOUND_232', checked_components=total_components,
                  levels=records, initial_path_vertices_bound=initial_vertices,
                  initial_path_edges_bound=initial_edges,
                  maximum_returns_width_at_least14=complete_returns,
                  width_adjustments=width_adjustments,
                  maximum_returns_all_widths_at_least2=232,
                  producer_certificate_sha256=sha256(cert_path.read_bytes()).hexdigest(),
                  producer_report_sha256=sha256(report_path.read_bytes()).hexdigest(),
                  independent_graph_audit_sha256=sha256(audit_path.read_bytes()).hexdigest(),
                  scope='Conservative actual-path bound using cyclic-component interval lifts; vertex counts include both endpoints.')
    (HERE / 'independent_bound_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('levels', 'width_adjustments')}))


if __name__ == '__main__':
    main()
