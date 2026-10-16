#!/usr/bin/env python3
"""Component-specific path bounds using only frozen graph checkpoints.

Every recursive job is an exact induced subgraph. A cyclic SCC interval
lifts only into next-level vertices whose retained parent belongs to
that SCC. Completed jobs preserve full subgraphs and rank certificates.
"""

from collections import deque
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTRIBUTIONS = HERE.parent
HELPER_PATH = CONTRIBUTIONS / "2026-10-14-broader-return" / "finite_bound.py"
SPEC = importlib.util.spec_from_file_location("frozen_bound_helper", HELPER_PATH)
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)
MAX_JOBS = 10000


class JobCap(Exception):
    pass


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_hierarchy(name):
    if name == "scalar":
        directory = CONTRIBUTIONS / "2026-10-14-scalar-clock" / "seven_4"
        report_path = directory / "scalar_clock.json"
    else:
        directory = CONTRIBUTIONS / "2026-10-14-broader-return"
        report_path = directory / "branching_lift.json"
    source = json.loads(report_path.read_text())
    assert source["status"] == "EMPTY_AT_FINITE_WIDTH"
    levels = {}
    dependencies = []
    for record in source["completed_graphs"]:
        raw_path = directory / record["raw_artifact"]["filename"]
        retained_path = directory / record["retained_artifact"]["filename"]
        assert digest(raw_path) == record["raw_artifact"]["sha256"]
        assert digest(retained_path) == record["retained_artifact"]["sha256"]
        width, vertices, edges = HELPER.read_graph(raw_path)
        retained_width, retained_vertices, retained_edges = HELPER.read_graph(retained_path)
        assert width == retained_width == record["width"]
        raw_lookup = {tuple(vertex): i for i, vertex in enumerate(vertices)}
        assert len(raw_lookup) == len(vertices)
        retained_to_raw = [raw_lookup[tuple(vertex)] for vertex in retained_vertices]
        raw_to_retained = {raw: retained for retained, raw in enumerate(retained_to_raw)}
        assert {(retained_to_raw[u], retained_to_raw[v], label)
                for u, v, label in retained_edges} == {
                    (u, v, label) for u, v, label in edges
                    if u in raw_to_retained and v in raw_to_retained}
        levels[width] = dict(vertices=vertices, edges=edges,
                             retained_to_raw=retained_to_raw,
                             raw_to_retained=raw_to_retained)
        dependencies.append(dict(width=width,
                                 raw_path=str(raw_path.relative_to(CONTRIBUTIONS)),
                                 raw_sha256=digest(raw_path),
                                 retained_path=str(retained_path.relative_to(CONTRIBUTIONS)),
                                 retained_sha256=digest(retained_path)))
    return levels, dict(name=name, report_path=str(report_path.relative_to(CONTRIBUTIONS)),
                        report_sha256=digest(report_path), graphs=dependencies)


class Solver:
    def __init__(self):
        self.jobs = []
        self.memo = {}
        self.hierarchies = {}

    def solve(self, name, width, allowed):
        allowed = tuple(sorted(allowed))
        key = (name, width, allowed)
        if key in self.memo:
            return self.memo[key]
        if len(self.jobs) >= MAX_JOBS:
            raise JobCap()
        identity = len(self.jobs)
        self.memo[key] = identity
        job = dict(id=identity, hierarchy=name, width=width, status="STARTED")
        self.jobs.append(job)
        hierarchy = self.hierarchies[name]
        graph = hierarchy[width]
        local = {vertex: i for i, vertex in enumerate(allowed)}
        edges = [edge for edge in graph["edges"] if edge[0] in local and edge[1] in local]
        local_edges = [(local[u], local[v], label) for u, v, label in edges]
        ids, sizes, cyclic, quotient = HELPER.components(len(allowed), local_edges)
        groups = [[] for _ in sizes]
        for vertex in allowed:
            groups[ids[local[vertex]]].append(vertex)
        job.update(vertices=[[vertex, *graph["vertices"][vertex]] for vertex in allowed],
                   edges=edges, components=groups,
                   cyclic_components=[i for i, value in enumerate(cyclic) if value],
                   condensation_edges=quotient, children=[])
        weights = [1] * len(groups)
        for component, recurrent in enumerate(cyclic):
            if not recurrent:
                assert sizes[component] == 1
                continue
            assert width + 1 in hierarchy
            parent_vertices = groups[component]
            retained_parents = {graph["raw_to_retained"][vertex] for vertex in parent_vertices}
            next_graph = hierarchy[width + 1]
            next_vertices = [i for i, vertex in enumerate(next_graph["vertices"])
                             if vertex[3] in retained_parents]
            assert len(next_vertices) == 19 * len(parent_vertices)
            child = self.solve(name, width + 1, next_vertices)
            child_job = self.jobs[child]
            assert child_job["status"] == "COMPLETE"
            internal_parent_edges = [edge for edge in edges
                                     if ids[local[edge[0]]] == component
                                     and ids[local[edge[1]]] == component]
            assert len(child_job["edges"]) == 19 * len(internal_parent_edges)
            projection = [[vertex, graph["retained_to_raw"][next_graph["vertices"][vertex][3]]]
                          for vertex in next_vertices]
            parent_edge_set = set(internal_parent_edges)
            projection_dict = dict(projection)
            for u, v, deeper in child_job["edges"]:
                coefficient = next_graph["vertices"][u][1]
                assert (projection_dict[u], projection_dict[v],
                        (coefficient + deeper) // 10) in parent_edge_set
            weights[component] = child_job["max_path_vertices_bound"]
            job["children"].append(dict(component=component, child_job=child,
                                         parent_retained_ids=sorted(retained_parents),
                                         child_to_parent_raw=projection))

        successors = [[] for _ in groups]
        predecessors = [[] for _ in groups]
        for u, v in quotient:
            successors[u].append(v)
            predecessors[v].append(u)
        remaining = list(map(len, successors))
        queue = deque(i for i, degree in enumerate(remaining) if not degree)
        ranks = list(weights)
        deleted = 0
        while queue:
            v = queue.popleft()
            deleted += 1
            for u in predecessors[v]:
                ranks[u] = max(ranks[u], weights[u] + ranks[v])
                remaining[u] -= 1
                if not remaining[u]:
                    queue.append(u)
        assert deleted == len(groups)
        assert all(ranks[u] == weights[u] + max((ranks[v] for v in successors[u]), default=0)
                   for u in range(len(groups)))
        bound = max(ranks, default=0)
        phase_bounds = [max((ranks[ids[local[v]]] for v in allowed
                            if graph["vertices"][v][0] == phase), default=0)
                        for phase in range(7)]
        job.update(status="COMPLETE", component_weights=weights,
                   weighted_sink_ranks=ranks, max_path_vertices_bound=bound,
                   path_vertices_bound_by_start_phase=phase_bounds)
        print(json.dumps(dict(job=identity, hierarchy=name, width=width,
                              vertices=len(allowed), edges=len(edges),
                              cyclic_components=sum(cyclic), vertex_bound=bound)), flush=True)
        return identity


def main():
    solver = Solver()
    dependencies, roots = [], []
    status = "COMPLETE"
    try:
        for name in ("scalar", "broader"):
            hierarchy, dependency = load_hierarchy(name)
            dependencies.append(dependency)
            solver.hierarchies[name] = hierarchy
            first = min(hierarchy)
            root = solver.solve(name, first, range(len(hierarchy[first]["vertices"])))
            job = solver.jobs[root]
            vertices = job["path_vertices_bound_by_start_phase"][0]
            periods = (vertices - 1) // 7
            roots.append(dict(hierarchy=name, root_job=root, initial_prefix_width=first,
                              physical_width_for_direct_bound=max(hierarchy),
                              phase0_path_vertices_bound=vertices,
                              phase0_path_edges_bound=vertices - 1,
                              full_periods_at_width14_or_more=periods,
                              width_dependent_bound="max(0,ceil((14-L)/3)) + " + str(periods),
                              uniform_bound=periods + 4,
                              minimum_physical_width=1 if name == "scalar" else 2,
                              width_one_exception="scalar (4) fails the prescribed clock at t=4" if name == "scalar" else None))
    except JobCap:
        status = "UNKNOWN_JOB_CAP"
    payload = (json.dumps(dict(jobs=solver.jobs), separators=(",", ":")) + "\n").encode()
    artifact = HERE / "component_certificates.json.gz"
    with artifact.open("wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", filename="", mtime=0) as stream:
            stream.write(payload)
    report = dict(status=status, max_jobs=MAX_JOBS, jobs=len(solver.jobs),
                  completed_jobs=sum(job["status"] == "COMPLETE" for job in solver.jobs),
                  roots=roots, dependencies=dependencies,
                  helper_dependency=dict(path=str(HELPER_PATH.relative_to(CONTRIBUTIONS)),
                                         sha256=digest(HELPER_PATH)),
                  certificate=dict(filename=artifact.name, compressed_bytes=artifact.stat().st_size,
                                   sha256=digest(artifact), uncompressed_sha256=hashlib.sha256(payload).hexdigest()),
                  scope="Component-specific conservative actual-path bounds; all exact induced graphs and projections are retained. No sharpness or eventual-palindrome claim.")
    (HERE / "component_bound.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(dict(status=status, jobs=report["jobs"], roots=roots)))


if __name__ == "__main__":
    main()
