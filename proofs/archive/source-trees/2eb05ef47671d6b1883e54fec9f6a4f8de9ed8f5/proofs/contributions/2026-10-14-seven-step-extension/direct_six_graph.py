#!/usr/bin/env python3
"""Complete six-column graph for the seven-phase 440 return clock.

All 7*19**3 prefixes and both deeper carry inputs are enumerated.  The
preserved edges and sink ranks are a finite certificate, not an orbit scan.
No source from the smaller spatial lift is imported.
"""

from array import array
from collections import Counter, deque
import gzip
import hashlib
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
PREFIXES = ((4, 4, 0), (8, 8, 0), (16, 16, 0), (7, 14, 7),
            (15, 8, 15), (6, 14, 14), (13, 9, 9))
OVERFLOWS = (0, 0, 1, 0, 1, 0, 1)
PHASE_SIZE = 19 ** 3
VERTICES = 7 * PHASE_SIZE


def encode(phase, tail):
    a, b, c = tail
    return PHASE_SIZE * phase + (19 * a + b) * 19 + c


def decode(vertex):
    phase, residual = divmod(vertex, PHASE_SIZE)
    a, residual = divmod(residual, 19 ** 2)
    b, c = divmod(residual, 19)
    return phase, PREFIXES[phase] + (a, b, c)


def transition(prefix, deeper):
    low_digits = []
    carry = 0
    for coefficient in prefix:
        total = coefficient + carry
        low_digits.append(total % 10)
        carry = total // 10
    high_digits = [0] * 6
    carry = deeper
    for index in range(5, -1, -1):
        total = prefix[index] + carry
        high_digits[index] = total % 10
        carry = total // 10
    overflow = carry
    if overflow:
        reflected = [1] + high_digits[:-1]
    else:
        reflected = high_digits
    return tuple(a + b for a, b in zip(low_digits, reflected)), overflow


def main():
    edges = []
    successors = [[] for _ in range(VERTICES)]
    predecessors = [[] for _ in range(VERTICES)]
    controls = [[dict(accepted=0, rejected=0) for _ in range(2)] for _ in range(7)]
    for source in range(VERTICES):
        phase, prefix = decode(source)
        assert encode(phase, prefix[3:]) == source
        next_phase = (phase + 1) % 7
        for deeper in (0, 1):
            target_prefix, overflow = transition(prefix, deeper)
            accepted = (overflow == OVERFLOWS[phase]
                        and target_prefix[:3] == PREFIXES[next_phase])
            controls[phase][deeper]["accepted" if accepted else "rejected"] += 1
            if not accepted:
                continue
            assert all(0 <= coefficient <= 18 for coefficient in target_prefix)
            target = encode(next_phase, target_prefix[3:])
            edges.append((source, target, deeper))
            successors[source].append((target, deeper))
            predecessors[target].append(source)

    # Parallel edges are counted individually and are removed individually.
    remaining = array("I", map(len, successors))
    ranks = array("I", [0]) * VERTICES
    queue = deque(vertex for vertex, degree in enumerate(remaining) if degree == 0)
    deleted = 0
    while queue:
        target = queue.popleft()
        deleted += 1
        for source in predecessors[target]:
            ranks[source] = max(ranks[source], 1 + ranks[target])
            remaining[source] -= 1
            if remaining[source] == 0:
                queue.append(source)
    assert deleted == VERTICES, "Nonempty cyclic remainder: no DAG claim is justified"
    assert all(ranks[source] > ranks[target] for source, target, _ in edges)
    assert all(ranks[source] == max((1 + ranks[target] for target, _ in successors[source]),
                                    default=0) for source in range(VERTICES))

    phase_max = [max(ranks[phase * PHASE_SIZE:(phase + 1) * PHASE_SIZE])
                 for phase in range(7)]
    phase0_start = next(v for v in range(PHASE_SIZE) if ranks[v] == phase_max[0])
    witness = []
    vertex = phase0_start
    while True:
        phase, prefix = decode(vertex)
        record = dict(vertex=vertex, phase=phase, prefix=prefix, rank=ranks[vertex])
        witness.append(record)
        if not ranks[vertex]:
            break
        target, deeper = next((target, deeper) for target, deeper in successors[vertex]
                              if ranks[target] + 1 == ranks[vertex])
        record["incoming_carry"] = deeper
        vertex = target

    # Vertices are implicit in the encoding; ranks use uint32 for portability.
    data = bytearray(b"P196DAG1")
    data.extend(struct.pack("<II", VERTICES, len(edges)))
    for rank in ranks:
        data.extend(struct.pack("<I", rank))
    for edge in edges:
        data.extend(struct.pack("<IIB", *edge))
    artifact = HERE / "direct_six_graph.bin.gz"
    with artifact.open("wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", mtime=0, filename="") as stream:
            stream.write(data)
    result = dict(
        status="COMPLETE_DAG", vertices=VERTICES, edges=len(edges),
        raw_controls=2 * VERTICES, deleted_vertices=deleted,
        prefix_width=6, phase_prefixes=PREFIXES, overflow_clock=OVERFLOWS,
        max_path_edges=max(ranks), max_path_edges_by_phase=phase_max,
        max_complete_returns_from_phase0=phase_max[0] // 7,
        phase0_longest_path=witness,
        controls_by_phase_and_input=controls,
        rank_histograms_by_phase=[dict(sorted(Counter(
            ranks[t * PHASE_SIZE:(t + 1) * PHASE_SIZE]).items())) for t in range(7)],
        certificate=dict(filename=artifact.name, compressed_bytes=artifact.stat().st_size,
                         sha256=hashlib.sha256(artifact.read_bytes()).hexdigest(),
                         uncompressed_sha256=hashlib.sha256(data).hexdigest(),
                         magic="P196DAG1", byte_order="little endian",
                         header="uint32 vertices,edges",
                         vertex_encoding="phase*19^3 + a*19^2 + b*19 + c",
                         vertex_payload="one uint32 sink rank per vertex in ID order",
                         edge_payload="uint32 source,target; uint8 deeper incoming carry"),
        scope="All deeper carry choices; exact necessary local relation for actual symmetric words of width at least 6. Failure of this clock does not imply a palindrome.")
    (HERE / "direct_six_graph.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "status", "vertices", "edges", "raw_controls", "max_path_edges",
        "max_path_edges_by_phase", "max_complete_returns_from_phase0", "certificate")}))


if __name__ == "__main__":
    main()
