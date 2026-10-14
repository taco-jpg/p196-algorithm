#!/usr/bin/env python3
"""Correlation-preserving spatial lift of the remaining seven-step clock.

An edge label is the actual high-side carry entering the known prefix.
All binary deeper carries are retained.  Cyclic SCC trimming preserves
the possibility of an infinite tail, not an arbitrary finite transient.
"""

from array import array
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import struct

from extension_graph import CLOCK, ROOT_PREFIX, prefix_update

MAX_VERTICES = 500000
MAX_EDGES = 2000000
MAX_WIDTH = 32
NONE = 2 ** 32 - 1
HERE = Path(__file__).resolve().parent


def empty_graph(width):
    return dict(width=width, phase=bytearray(), last=bytearray(), low=bytearray(),
                parent=array("I"), source=array("I"), target=array("I"), label=bytearray())


def initial_graph():
    added = (3, 6, 13, 4, 9, 5, 12)
    prefixes = tuple(ROOT_PREFIX[t] + (added[t],) for t in range(7))
    g = empty_graph(4)
    for t, prefix in enumerate(prefixes):
        _, _, low = prefix_update(prefix, 0)
        g["phase"].append(t)
        g["last"].append(prefix[-1])
        g["low"].append(low)
        g["parent"].append(NONE)
        for carry in (0, 1):
            nxt, overflow, _ = prefix_update(prefix, carry)
            if nxt == prefixes[(t + 1) % 7] and overflow == CLOCK[t]:
                g["source"].append(t)
                g["target"].append((t + 1) % 7)
                g["label"].append(carry)
    return g, prefixes


def lift(g):
    result = empty_graph(g["width"] + 1)
    for vertex in range(len(g["phase"])):
        for coefficient in range(19):
            result["phase"].append(g["phase"][vertex])
            result["last"].append(coefficient)
            result["low"].append((coefficient + g["low"][vertex]) // 10)
            result["parent"].append(vertex)
    for source, target, gamma in zip(g["source"], g["target"], g["label"]):
        phase = g["phase"][source]
        for coefficient in range(19):
            for deeper in (0, 1):
                if (coefficient + deeper) // 10 != gamma:
                    continue
                low_digit = (coefficient + g["low"][source]) % 10
                high_digit = ((g["last"][source] + gamma) % 10 if CLOCK[phase]
                              else (coefficient + deeper) % 10)
                nxt = low_digit + high_digit
                assert 0 <= nxt <= 18
                result["source"].append(19 * source + coefficient)
                result["target"].append(19 * target + nxt)
                result["label"].append(deeper)
    assert len(result["source"]) == 19 * len(g["source"])
    return result


def csr(vertices, sources, targets):
    offsets = array("I", [0]) * (vertices + 1)
    for source in sources:
        offsets[source + 1] += 1
    for i in range(vertices):
        offsets[i + 1] += offsets[i]
    cursor = array("I", offsets)
    neighbors = array("I", [0]) * len(sources)
    for source, target in zip(sources, targets):
        neighbors[cursor[source]] = target
        cursor[source] += 1
    return offsets, neighbors


def trim_cyclic(g):
    vertices = len(g["phase"])
    offsets, neighbors = csr(vertices, g["source"], g["target"])
    reverse_offsets, reverse_neighbors = csr(vertices, g["target"], g["source"])
    seen = bytearray(vertices)
    cursor = array("I", offsets)
    finish = array("I")
    stack = array("I")
    for root in range(vertices):
        if seen[root]:
            continue
        seen[root] = 1
        stack.append(root)
        while stack:
            vertex = stack[-1]
            if cursor[vertex] == offsets[vertex + 1]:
                finish.append(stack.pop())
                continue
            nxt = neighbors[cursor[vertex]]
            cursor[vertex] += 1
            if not seen[nxt]:
                seen[nxt] = 1
                stack.append(nxt)
    component = array("I", [NONE]) * vertices
    sizes = array("I")
    for root in reversed(finish):
        if component[root] != NONE:
            continue
        index = len(sizes)
        count = 0
        component[root] = index
        stack.append(root)
        while stack:
            vertex = stack.pop()
            count += 1
            for i in range(reverse_offsets[vertex], reverse_offsets[vertex + 1]):
                nxt = reverse_neighbors[i]
                if component[nxt] == NONE:
                    component[nxt] = index
                    stack.append(nxt)
        sizes.append(count)
    cyclic = bytearray(size > 1 for size in sizes)
    for source, target in zip(g["source"], g["target"]):
        if source == target:
            cyclic[component[source]] = 1
    remap = array("I", [NONE]) * vertices
    result = empty_graph(g["width"])
    for vertex in range(vertices):
        if not cyclic[component[vertex]]:
            continue
        remap[vertex] = len(result["phase"])
        for key in ("phase", "last", "low", "parent"):
            result[key].append(g[key][vertex])
    for source, target, label in zip(g["source"], g["target"], g["label"]):
        if remap[source] != NONE and remap[target] != NONE:
            result["source"].append(remap[source])
            result["target"].append(remap[target])
            result["label"].append(label)
    metadata = dict(raw_vertices=vertices, raw_edges=len(g["source"]),
                    components=len(sizes), cyclic_components=sum(cyclic),
                    cyclic_component_size_counts=dict(sorted(Counter(
                        sizes[i] for i in range(len(sizes)) if cyclic[i]).items())),
                    retained_vertices=len(result["phase"]), retained_edges=len(result["source"]))
    return result, metadata


def save_graph(g):
    destination = HERE / ("lift_width_%02d.bin.gz" % g["width"])
    with destination.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, filename="") as stream:
            stream.write(b"P196LFT1")
            stream.write(struct.pack("<III", g["width"], len(g["phase"]), len(g["source"])))
            buffer = bytearray()
            for phase, last, low, parent in zip(g["phase"], g["last"], g["low"], g["parent"]):
                buffer.extend(struct.pack("<BBBI", phase, last, low, parent))
                if len(buffer) >= 1048576:
                    stream.write(buffer)
                    buffer.clear()
            stream.write(buffer)
            buffer.clear()
            for source, target, label in zip(g["source"], g["target"], g["label"]):
                buffer.extend(struct.pack("<IIB", source, target, label))
                if len(buffer) >= 1048576:
                    stream.write(buffer)
                    buffer.clear()
            stream.write(buffer)
    digest = hashlib.sha256()
    with destination.open("rb") as stream:
        while chunk := stream.read(1048576):
            digest.update(chunk)
    return dict(filename=destination.name, compressed_bytes=destination.stat().st_size,
                sha256=digest.hexdigest())


def main():
    graph, prefixes = initial_graph()
    records = []
    result = dict(status="RUNNING", base_prefixes=prefixes, overflow_clock=CLOCK,
                  caps=dict(raw_vertices=MAX_VERTICES, raw_edges=MAX_EDGES, width=MAX_WIDTH),
                  graph_format=dict(magic="P196LFT1", header="uint32 width,vertices,edges",
                                    vertex="uint8 phase,last,low; uint32 parent_previous_graph_vertex",
                                    edge="uint32 source,target; uint8 incoming_carry_label",
                                    byte_order="little endian", no_parent=NONE),
                  completed_graphs=records,
                  scope="Necessary correlation-preserving spatial lifts; surviving graphs do not prove a finite infinite orbit.")
    while True:
        graph, metadata = trim_cyclic(graph)
        metadata.update(width=graph["width"], artifact=save_graph(graph))
        records.append(metadata)
        print(json.dumps(metadata), flush=True)
        (HERE / "spatial_lift.json").write_text(json.dumps(result, indent=2) + "\n")
        if not graph["phase"]:
            result["status"] = "EMPTY_AT_FINITE_WIDTH"
            result["empty_width"] = graph["width"]
            break
        next_vertices = 19 * len(graph["phase"])
        next_edges = 19 * len(graph["source"])
        if next_vertices > MAX_VERTICES or next_edges > MAX_EDGES or graph["width"] >= MAX_WIDTH:
            result["status"] = "UNKNOWN_CAP"
            result["next_lift"] = dict(width=graph["width"] + 1,
                                       raw_vertices=next_vertices, raw_edges=next_edges)
            break
        graph = lift(graph)
    (HERE / "spatial_lift.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(status=result["status"], last_completed_width=graph["width"])), flush=True)


if __name__ == "__main__":
    main()
