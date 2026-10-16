#!/usr/bin/env python3
"""Finite path bound from the saved broader-return lift hierarchy.

This reads, rather than reruns, all raw graph checkpoints. Each cyclic
SCC interval projects to the next raw graph; its vertex count is bounded
by the next-level bound. All other SCCs are loop-free singletons. Weighted
condensation ranks bound total vertex visits, counting both endpoints.
"""

from collections import deque
import gzip
import hashlib
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent


def read_graph(path):
    data = gzip.decompress(path.read_bytes())
    assert data[:8] == b"P196BRC1"
    width, vertices, edges = struct.unpack_from("<III", data, 8)
    assert len(data) == 20 + 7 * vertices + 9 * edges
    metadata = [struct.unpack_from("<BBBI", data, 20 + 7 * i)
                for i in range(vertices)]
    edge_list = [struct.unpack_from("<IIB", data, 20 + 7 * vertices + 9 * i)
                 for i in range(edges)]
    return width, metadata, edge_list


def components(vertices, edges):
    forward = [[] for _ in range(vertices)]
    reverse = [[] for _ in range(vertices)]
    for source, target, _ in edges:
        forward[source].append(target)
        reverse[target].append(source)
    seen = set()
    finished = []
    for root in range(vertices):
        if root in seen:
            continue
        seen.add(root)
        stack = [(root, iter(forward[root]))]
        while stack:
            source, children = stack[-1]
            target = next(children, None)
            if target is None:
                finished.append(source)
                stack.pop()
            elif target not in seen:
                seen.add(target)
                stack.append((target, iter(forward[target])))
    ids = [-1] * vertices
    sizes = []
    for root in reversed(finished):
        if ids[root] != -1:
            continue
        identity, size = len(sizes), 0
        ids[root] = identity
        stack = [root]
        while stack:
            target = stack.pop()
            size += 1
            for source in reverse[target]:
                if ids[source] == -1:
                    ids[source] = identity
                    stack.append(source)
        sizes.append(size)
    cyclic = [size > 1 for size in sizes]
    quotient_edges = set()
    for source, target, _ in edges:
        if source == target:
            cyclic[ids[source]] = True
        if ids[source] != ids[target]:
            quotient_edges.add((ids[source], ids[target]))
    return ids, sizes, cyclic, sorted(quotient_edges)


def bound_graph(width, metadata, edges, deeper_bound):
    ids, sizes, cyclic, quotient_edges = components(len(metadata), edges)
    assert deeper_bound is not None or not any(cyclic)
    weights = [deeper_bound if recurrent else 1 for recurrent in cyclic]
    successors = [[] for _ in sizes]
    predecessors = [[] for _ in sizes]
    for source, target in quotient_edges:
        successors[source].append(target)
        predecessors[target].append(source)
    degree = list(map(len, successors))
    queue = deque(i for i, d in enumerate(degree) if not d)
    ranks = list(weights)
    deleted = 0
    while queue:
        target = queue.popleft()
        deleted += 1
        for source in predecessors[target]:
            ranks[source] = max(ranks[source], weights[source] + ranks[target])
            degree[source] -= 1
            if not degree[source]:
                queue.append(source)
    assert deleted == len(sizes)
    assert all(ranks[source] >= weights[source] + ranks[target]
               for source, target in quotient_edges)
    assert all(ranks[source] == weights[source] + max(
        (ranks[target] for target in successors[source]), default=0)
               for source in range(len(sizes)))
    bound = max(ranks, default=0)
    phase_bounds = [max((ranks[ids[i]] for i, vertex in enumerate(metadata)
                        if vertex[0] == phase), default=0) for phase in range(7)]
    certificate = dict(width=width, vertices=len(metadata), edges=len(edges),
                       component_of_vertex=ids, component_sizes=sizes,
                       cyclic_components=[i for i, value in enumerate(cyclic) if value],
                       condensation_edges=quotient_edges,
                       component_weights=weights, weighted_sink_ranks=ranks,
                       next_level_vertex_bound=deeper_bound,
                       max_path_vertices_bound=bound,
                       path_vertices_bound_by_start_phase=phase_bounds)
    return certificate


def main():
    source = json.loads((HERE / "branching_lift.json").read_text())
    assert source["status"] == "EMPTY_AT_FINITE_WIDTH"
    records, next_bound = [], None
    for graph in reversed(source["completed_graphs"]):
        path = HERE / graph["raw_artifact"]["filename"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == graph["raw_artifact"]["sha256"]
        width, vertices, edges = read_graph(path)
        assert width == graph["width"]
        record = bound_graph(width, vertices, edges, next_bound)
        assert len(record["cyclic_components"]) == graph["cyclic_components"]
        next_bound = record["max_path_vertices_bound"]
        records.append(record)
        print(json.dumps(dict(width=width, vertex_bound=next_bound,
                              cyclic_components=len(record["cyclic_components"]))), flush=True)
    records.reverse()
    phase0_vertices = records[0]["path_vertices_bound_by_start_phase"][0]
    returns = (phase0_vertices - 1) // 7
    data = (json.dumps(dict(records=records), separators=(",", ":")) + "\n").encode()
    artifact = HERE / "finite_bound_certificate.json.gz"
    with artifact.open("wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", filename="", mtime=0) as stream:
            stream.write(data)
    report = dict(
        status="WEIGHTED_CONDENSATION_BOUND", minimum_width_for_direct_bound=source["empty_width"],
        phase0_max_path_vertices_bound=phase0_vertices,
        phase0_max_path_edges_bound=phase0_vertices - 1,
        max_complete_returns_at_width14_or_more=returns,
        max_complete_returns_at_width_L="max(0,ceil((14-L)/3)) + " + str(returns),
        max_complete_returns_at_all_widths_at_least2=4 + returns,
        levels=[{k: record[k] for k in (
            "width", "vertices", "edges", "next_level_vertex_bound", "max_path_vertices_bound",
            "path_vertices_bound_by_start_phase")} for record in records],
        certificate=dict(filename=artifact.name, compressed_bytes=artifact.stat().st_size,
                         sha256=hashlib.sha256(artifact.read_bytes()).hexdigest(),
                         uncompressed_sha256=hashlib.sha256(data).hexdigest()),
        graph_report_sha256=hashlib.sha256((HERE / "branching_lift.json").read_bytes()).hexdigest(),
        scope="Conservative actual-orbit bound using the exact graph hierarchy, not a claimed sharp bound; no implication that leaving the clock reaches a palindrome.")
    (HERE / "finite_bound.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in (
        "status", "phase0_max_path_vertices_bound", "phase0_max_path_edges_bound",
        "max_complete_returns_at_width14_or_more", "max_complete_returns_at_all_widths_at_least2")}))


if __name__ == "__main__":
    main()
