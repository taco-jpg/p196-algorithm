#!/usr/bin/env python3
"""Independent audit of exact component restrictions and weighted bounds.

The raw arithmetic hierarchies were separately replayed by literal integer
oracles.  This checker reopens every checkpoint, verifies each induced
job and child projection, recomputes SCCs with an independent Tarjan
implementation, and evaluates all weighted ranks in reverse spatial order.
"""

from collections import deque
from hashlib import sha256
from pathlib import Path
import gzip
import importlib.util
import json
import struct


HERE = Path(__file__).resolve().parent
CONTRIBUTIONS = HERE.parent
AUDIT_HELPER = CONTRIBUTIONS / '2026-10-14-broader-return' / 'independent_branch_audit.py'
spec = importlib.util.spec_from_file_location('independent_tarjan_audit', AUDIT_HELPER)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def read_graph(path):
    raw = gzip.decompress(path.read_bytes())
    assert raw[:8] == b'P196BRC1'
    width, n, m = struct.unpack_from('<III', raw, 8)
    assert len(raw) == 20 + 7 * n + 9 * m
    metadata = [struct.unpack_from('<BBBI', raw, 20 + 7 * i) for i in range(n)]
    edges = [struct.unpack_from('<IIB', raw, 20 + 7 * n + 9 * i) for i in range(m)]
    return width, metadata, edges


def main():
    report_path = HERE / 'component_bound.json'
    report = json.loads(report_path.read_text())
    assert report['status'] == 'COMPLETE'
    assert report['jobs'] == report['completed_jobs'] < report['max_jobs']
    producer_helper = CONTRIBUTIONS / report['helper_dependency']['path']
    assert sha256(producer_helper.read_bytes()).hexdigest() == report['helper_dependency']['sha256']
    cert_path = HERE / report['certificate']['filename']
    assert sha256(cert_path.read_bytes()).hexdigest() == report['certificate']['sha256']
    raw = gzip.decompress(cert_path.read_bytes())
    assert sha256(raw).hexdigest() == report['certificate']['uncompressed_sha256']
    jobs = json.loads(raw)['jobs']
    assert len(jobs) == report['jobs']
    assert [job['id'] for job in jobs] == list(range(len(jobs)))
    hierarchies = {}
    for dependency in report['dependencies']:
        name = dependency['name']
        path = CONTRIBUTIONS / dependency['report_path']
        assert sha256(path.read_bytes()).hexdigest() == dependency['report_sha256']
        prior_path = (CONTRIBUTIONS / '2026-10-14-scalar-clock/seven_4/independent_scalar_audit.json'
                      if name == 'scalar' else
                      CONTRIBUTIONS / '2026-10-14-broader-return/independent_branch_audit.json')
        prior = json.loads(prior_path.read_text())
        assert prior['status'] == 'PASS_EMPTY_AT_WIDTH14'
        prior_levels = {record['width']: record for record in prior['layers']}
        levels = {}
        for record in dependency['graphs']:
            raw_path = CONTRIBUTIONS / record['raw_path']
            retained_path = CONTRIBUTIONS / record['retained_path']
            assert sha256(raw_path.read_bytes()).hexdigest() == record['raw_sha256']
            assert sha256(retained_path.read_bytes()).hexdigest() == record['retained_sha256']
            width, metadata, edges = read_graph(raw_path)
            retained_width, retained_metadata, retained_edges = read_graph(retained_path)
            assert retained_width == width == record['width']
            earlier = prior_levels[width]
            assert earlier['raw_sha256'] == record['raw_sha256']
            assert earlier['recurrent_sha256'] == record['retained_sha256']
            kept = earlier['recurrent_raw_vertex_indices']
            assert retained_metadata == [metadata[v] for v in kept]
            inverse = {v: i for i, v in enumerate(kept)}
            assert sorted(retained_edges) == sorted((inverse[a], inverse[b], c)
                for a, b, c in edges if a in inverse and b in inverse)
            levels[width] = dict(metadata=metadata, edges=edges,
                                 retained_to_raw=kept, raw_to_retained=inverse)
        hierarchies[name] = levels

    checked, reachable = {}, set()
    for job in sorted(jobs, key=lambda j: (-j['width'], j['id'])):
        identity, name, width = job['id'], job['hierarchy'], job['width']
        assert job['status'] == 'COMPLETE'
        graph = hierarchies[name][width]
        allowed = [row[0] for row in job['vertices']]
        assert allowed == sorted(set(allowed))
        assert job['vertices'] == [[v, *graph['metadata'][v]] for v in allowed]
        allowed_set = set(allowed)
        expected_edges = [edge for edge in graph['edges'] if edge[0] in allowed_set and edge[1] in allowed_set]
        assert [tuple(edge) for edge in job['edges']] == expected_edges
        local = {v: i for i, v in enumerate(allowed)}
        local_edges = [(local[a], local[b], c) for a, b, c in expected_edges]
        groups_local, cyclic_local, _ = helper.tarjan(allowed, local_edges)
        groups = [[allowed[v] for v in group] for group in groups_local]
        cyclic = {tuple(allowed[v] for v in group) for group in cyclic_local}
        assert sorted(job['components']) == groups
        producer_components = job['components']
        producer_ids = {v: i for i, group in enumerate(producer_components) for v in group}
        assert {tuple(producer_components[i]) for i in job['cyclic_components']} == cyclic
        children = {tuple(producer_components[entry['component']]): entry for entry in job['children']}
        assert len(children) == len(job['children']) and set(children) == cyclic
        weights = []
        child_checks = []
        for group in groups:
            key = tuple(group)
            if key not in cyclic:
                assert len(group) == 1
                weights.append(1)
                continue
            entry = children[key]
            child_id = entry['child_job']
            child = jobs[child_id]
            assert child_id in checked
            assert (child['hierarchy'], child['width']) == (name, width + 1)
            retained_parents = sorted(graph['raw_to_retained'][v] for v in group)
            assert entry['parent_retained_ids'] == retained_parents
            parent_set = set(retained_parents)
            next_graph = hierarchies[name][width + 1]
            expected_child_vertices = [v for v, metadata in enumerate(next_graph['metadata'])
                                       if metadata[3] in parent_set]
            assert len(expected_child_vertices) == 19 * len(group)
            assert [row[0] for row in child['vertices']] == expected_child_vertices
            projection = [[v, graph['retained_to_raw'][next_graph['metadata'][v][3]]]
                          for v in expected_child_vertices]
            assert entry['child_to_parent_raw'] == projection
            projection = dict(projection)
            group_set = set(group)
            parent_edges = {edge for edge in expected_edges if edge[0] in group_set and edge[1] in group_set}
            assert len(child['edges']) == 19 * len(parent_edges)
            for a, b, v in child['edges']:
                coefficient = next_graph['metadata'][a][1]
                assert (projection[a], projection[b], (coefficient + v) // 10) in parent_edges
            weights.append(checked[child_id]['vertex_bound'])
            child_checks.append(dict(child_job=child_id, parent_vertices=len(group),
                                     parent_internal_edges=len(parent_edges),
                                     child_vertices=len(expected_child_vertices),
                                     child_edges=len(child['edges'])))
        ids = {v: i for i, group in enumerate(groups) for v in group}
        quotient = sorted({(ids[a], ids[b]) for a, b, _ in expected_edges if ids[a] != ids[b]})
        producer_quotient = sorted({(producer_ids[a], producer_ids[b]) for a, b, _ in expected_edges
                                   if producer_ids[a] != producer_ids[b]})
        assert producer_quotient == [tuple(edge) for edge in job['condensation_edges']]
        successors = [[] for _ in groups]
        indegree = [0] * len(groups)
        for a, b in quotient:
            successors[a].append(b)
            indegree[b] += 1
        queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
        order = []
        while queue:
            component = queue.popleft()
            order.append(component)
            for target in successors[component]:
                indegree[target] -= 1
                if indegree[target] == 0:
                    queue.append(target)
        assert len(order) == len(groups)
        ranks = [0] * len(groups)
        for component in reversed(order):
            ranks[component] = weights[component] + max((ranks[w] for w in successors[component]), default=0)
        for v in allowed:
            assert weights[ids[v]] == job['component_weights'][producer_ids[v]]
            assert ranks[ids[v]] == job['weighted_sink_ranks'][producer_ids[v]]
        phase_bounds = [max((ranks[ids[v]] for v in allowed if graph['metadata'][v][0] == phase), default=0)
                        for phase in range(7)]
        bound = max(ranks, default=0)
        assert bound == job['max_path_vertices_bound']
        assert phase_bounds == job['path_vertices_bound_by_start_phase']
        checked[identity] = dict(job=identity, hierarchy=name, width=width,
                                 vertices=len(allowed), edges=len(expected_edges),
                                 components=len(groups), cyclic_components=len(cyclic),
                                 vertex_bound=bound, phase_bounds=phase_bounds,
                                 child_checks=child_checks)

    roots = []
    def mark(identity):
        if identity in reachable:
            return
        reachable.add(identity)
        for child in jobs[identity]['children']:
            mark(child['child_job'])
    for root in report['roots']:
        identity, name = root['root_job'], root['hierarchy']
        first = min(hierarchies[name])
        assert jobs[identity]['width'] == first
        assert [v[0] for v in jobs[identity]['vertices']] == list(range(len(hierarchies[name][first]['metadata'])))
        vertices = checked[identity]['phase_bounds'][0]
        periods = (vertices - 1) // 7
        assert (vertices, vertices - 1, periods, periods + 4) == (
            root['phase0_path_vertices_bound'], root['phase0_path_edges_bound'],
            root['full_periods_at_width14_or_more'], root['uniform_bound'])
        roots.append(dict(hierarchy=name, vertices_bound=vertices, edges_bound=vertices - 1,
                          periods_at_width14=periods, uniform_bound=periods + 4))
        mark(identity)
    assert reachable == set(range(len(jobs)))
    assert roots == [dict(hierarchy='scalar', vertices_bound=659, edges_bound=658,
                         periods_at_width14=94, uniform_bound=98),
                     dict(hierarchy='broader', vertices_bound=636, edges_bound=635,
                         periods_at_width14=90, uniform_bound=94)]
    word, width_one_trace = [4], [[4]]
    for _ in range(4):
        value = sum(a * 10**i for i, a in enumerate(word))
        digits = []
        while value:
            value, digit = divmod(value, 10)
            digits.append(digit)
        word = [a + b for a, b in zip(digits, reversed(digits))]
        width_one_trace.append(word)
    assert width_one_trace == [[4], [8], [16], [7, 7], [14, 14]]
    assert width_one_trace[4][0] != 15
    result = dict(status='PASS_COMPONENT_BOUNDS_98_94', jobs_checked=len(jobs),
                  induced_vertices_checked=sum(row['vertices'] for row in checked.values()),
                  induced_edges_checked=sum(row['edges'] for row in checked.values()),
                  roots=roots, jobs=[checked[i] for i in sorted(checked)],
                  scalar_width_one_exact_trace=width_one_trace,
                  certificate_sha256=sha256(cert_path.read_bytes()).hexdigest(),
                  producer_source_sha256=sha256((HERE / 'component_bound.py').read_bytes()).hexdigest(),
                  producer_report_sha256=sha256(report_path.read_bytes()).hexdigest(),
                  independent_tarjan_source_sha256=sha256(AUDIT_HELPER.read_bytes()).hexdigest(),
                  scope='Exact induced restrictions, all child projections, independent SCCs and all ranks checked; no additional orbit search or sharpness claim.')
    (HERE / 'independent_component_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'jobs'}))


if __name__ == '__main__':
    main()
