#!/usr/bin/env python3
"""Correlation-preserving spatial lift of every seven-step 44 return.

The complete 128-control certificate supplies all three boundary branches.
Merged equal phase/prefix vertices permit arbitrary branch switching.
Both deeper carries are kept at every subsequent lift. No fixed temporal
period is imposed on the free columns.
"""

from array import array
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
MAX_VERTICES = 500000
MAX_EDGES = 2000000
MAX_WIDTH = 32
NONE = 2 ** 32 - 1
CLOCK = (0, 0, 1, 0, 1, 0, 1)


def empty(width):
    return dict(width=width, phase=bytearray(), last=bytearray(), low=bytearray(),
                parent=array("I"), source=array("I"), target=array("I"), label=bytearray())


def initial_graph():
    report = json.loads((HERE / "two_column_controls.json").read_text())
    records = [r for r in report["records"] if r["returned"]]
    states = sorted({(t, tuple(record["prefixes"][t]))
                     for record in records for t in range(7)})
    index = {state: i for i, state in enumerate(states)}
    graph = empty(2)
    for phase, prefix in states:
        carry = 0
        for coefficient in prefix:
            carry = (coefficient + carry) // 10
        graph["phase"].append(phase)
        graph["last"].append(prefix[-1])
        graph["low"].append(carry)
        graph["parent"].append(NONE)
    edges = set()
    for record in records:
        assert tuple(record["overflows"]) == CLOCK
        for t, control in enumerate(record["controls"]):
            source = index[(t, tuple(record["prefixes"][t]))]
            target = index[((t + 1) % 7, tuple(record["prefixes"][t + 1]))]
            edges.add((source, target, control))
    for source, target, label in sorted(edges):
        graph["source"].append(source)
        graph["target"].append(target)
        graph["label"].append(label)
    start = index[(0, (4, 4))]
    paths = {(start, ())}
    for _ in range(7):
        paths = {(target, controls + (label,))
                 for vertex, controls in paths for source, target, label in edges
                 if source == vertex}
    assert paths == {(start, tuple(record["controls"])) for record in records}
    return graph, states


def lift(graph):
    result = empty(graph["width"] + 1)
    for vertex in range(len(graph["phase"])):
        for coefficient in range(19):
            result["phase"].append(graph["phase"][vertex])
            result["last"].append(coefficient)
            result["low"].append((coefficient + graph["low"][vertex]) // 10)
            result["parent"].append(vertex)
    for source, target, gamma in zip(graph["source"], graph["target"], graph["label"]):
        phase = graph["phase"][source]
        for coefficient in range(19):
            for deeper in (0, 1):
                if (coefficient + deeper) // 10 != gamma:
                    continue
                lower_digit = (coefficient + graph["low"][source]) % 10
                reflected_digit = ((graph["last"][source] + gamma) % 10
                                   if CLOCK[phase] else (coefficient + deeper) % 10)
                successor = lower_digit + reflected_digit
                result["source"].append(19 * source + coefficient)
                result["target"].append(19 * target + successor)
                result["label"].append(deeper)
    assert len(result["source"]) == 19 * len(graph["source"])
    return result


def csr(vertices, sources, targets):
    offsets = array("I", [0]) * (vertices + 1)
    for source in sources:
        offsets[source + 1] += 1
    for vertex in range(vertices):
        offsets[vertex + 1] += offsets[vertex]
    cursor = array("I", offsets)
    neighbors = array("I", [0]) * len(sources)
    for source, target in zip(sources, targets):
        neighbors[cursor[source]] = target
        cursor[source] += 1
    return offsets, neighbors


def recurrent_part(graph):
    # Same elementary iterative Kosaraju operation as the earlier 440 lift.
    vertices = len(graph["phase"])
    offsets, neighbors = csr(vertices, graph["source"], graph["target"])
    reverse_offsets, reverse_neighbors = csr(vertices, graph["target"], graph["source"])
    seen = bytearray(vertices)
    cursor = array("I", offsets)
    finished, stack = array("I"), array("I")
    for root in range(vertices):
        if seen[root]:
            continue
        seen[root] = 1
        stack.append(root)
        while stack:
            vertex = stack[-1]
            if cursor[vertex] == offsets[vertex + 1]:
                finished.append(stack.pop())
                continue
            target = neighbors[cursor[vertex]]
            cursor[vertex] += 1
            if not seen[target]:
                seen[target] = 1
                stack.append(target)
    component = array("I", [NONE]) * vertices
    sizes = array("I")
    for root in reversed(finished):
        if component[root] != NONE:
            continue
        identity, count = len(sizes), 0
        component[root] = identity
        stack.append(root)
        while stack:
            vertex = stack.pop()
            count += 1
            for i in range(reverse_offsets[vertex], reverse_offsets[vertex + 1]):
                target = reverse_neighbors[i]
                if component[target] == NONE:
                    component[target] = identity
                    stack.append(target)
        sizes.append(count)
    cyclic = bytearray(size > 1 for size in sizes)
    for source, target in zip(graph["source"], graph["target"]):
        if source == target:
            cyclic[component[source]] = 1
    result = empty(graph["width"])
    remap = array("I", [NONE]) * vertices
    for vertex in range(vertices):
        if cyclic[component[vertex]]:
            remap[vertex] = len(result["phase"])
            for key in ("phase", "last", "low", "parent"):
                result[key].append(graph[key][vertex])
    for source, target, label in zip(graph["source"], graph["target"], graph["label"]):
        if remap[source] != NONE and remap[target] != NONE:
            result["source"].append(remap[source])
            result["target"].append(remap[target])
            result["label"].append(label)
    metadata = dict(raw_vertices=vertices, raw_edges=len(graph["source"]),
                    components=len(sizes), cyclic_components=sum(cyclic),
                    cyclic_component_size_counts=dict(sorted(Counter(
                        sizes[i] for i in range(len(sizes)) if cyclic[i]).items())),
                    retained_vertices=len(result["phase"]), retained_edges=len(result["source"]))
    return result, metadata


def save(graph, suffix):
    path = HERE / ("branch_width_%02d_%s.bin.gz" % (graph["width"], suffix))
    with path.open("wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", mtime=0, filename="") as stream:
            stream.write(b"P196BRC1")
            stream.write(struct.pack("<III", graph["width"], len(graph["phase"]), len(graph["source"])))
            for record in zip(graph["phase"], graph["last"], graph["low"], graph["parent"]):
                stream.write(struct.pack("<BBBI", *record))
            for edge in zip(graph["source"], graph["target"], graph["label"]):
                stream.write(struct.pack("<IIB", *edge))
    return dict(filename=path.name, compressed_bytes=path.stat().st_size,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest())


def main():
    graph, states = initial_graph()
    result = dict(status="RUNNING", base_vertices=states, overflow_clock=CLOCK,
                  caps=dict(raw_vertices=MAX_VERTICES, raw_edges=MAX_EDGES, width=MAX_WIDTH),
                  source_control_sha256=hashlib.sha256((HERE / "two_column_controls.json").read_bytes()).hexdigest(),
                  graph_format=dict(magic="P196BRC1", byte_order="little endian",
                                    header="uint32 width,vertices,edges",
                                    vertex="uint8 phase,last,low; uint32 parent_previous_retained_graph_vertex",
                                    edge="uint32 source,target; uint8 deeper_carry_label", no_parent=NONE),
                  completed_graphs=[],
                  scope="Necessary arbitrary-carry relation with all three return branches and temporal correlations preserved. A surviving graph does not establish a realizable infinite integer orbit.")
    while True:
        raw_artifact = save(graph, "raw")
        graph, metadata = recurrent_part(graph)
        metadata.update(width=graph["width"], raw_artifact=raw_artifact,
                        retained_artifact=save(graph, "recurrent"))
        result["completed_graphs"].append(metadata)
        print(json.dumps(metadata), flush=True)
        if not graph["phase"]:
            result["status"] = "EMPTY_AT_FINITE_WIDTH"
            result["empty_width"] = graph["width"]
            break
        vertices, edges = 19 * len(graph["phase"]), 19 * len(graph["source"])
        if vertices > MAX_VERTICES or edges > MAX_EDGES or graph["width"] >= MAX_WIDTH:
            result["status"] = "UNKNOWN_CAP"
            result["next_lift"] = dict(width=graph["width"] + 1, raw_vertices=vertices, raw_edges=edges)
            break
        (HERE / "branching_lift.json").write_text(json.dumps(result, indent=2) + "\n")
        graph = lift(graph)
    (HERE / "branching_lift.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(status=result["status"], last_width=graph["width"])))


if __name__ == "__main__":
    main()
