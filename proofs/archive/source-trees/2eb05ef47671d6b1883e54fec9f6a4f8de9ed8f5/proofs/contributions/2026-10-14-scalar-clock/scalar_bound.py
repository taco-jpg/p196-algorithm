#!/usr/bin/env python3
"""Weighted finite bound for the saved seven_4 scalar-clock hierarchy.

The graph producer and its completed checkpoints are read-only inputs.
The generic, already audited broader-return condensation helper is reused
with its exact dependency hash recorded in this new report.
"""

import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
GRAPHS = HERE / "seven_4"
DEPENDENCY = HERE.parent / "2026-10-14-broader-return" / "finite_bound.py"
SPEC = importlib.util.spec_from_file_location("generic_condensation_bound", DEPENDENCY)
BOUND = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BOUND)


def width_one_check():
    word = (4,)
    trace = [word]
    for _ in range(4):
        value = sum(coefficient * 10 ** i for i, coefficient in enumerate(word))
        digits = tuple(map(int, str(value)[::-1]))
        word = tuple(a + b for a, b in zip(digits, reversed(digits)))
        trace.append(word)
    assert trace == [(4,), (8,), (16,), (7, 7), (14, 14)]
    prescribed = (4, 8, 16, 7, 15)
    assert all(trace[t][0] == prescribed[t] for t in range(4))
    assert trace[4][0] != prescribed[4]
    return dict(unique_initial_word=[4], pair_word_trace=trace,
                first_failed_phase_time=4, maximum_complete_periods=0)


def main():
    source_path = GRAPHS / "scalar_clock.json"
    source = json.loads(source_path.read_text())
    assert source["status"] == "EMPTY_AT_FINITE_WIDTH"
    assert source["outer_coefficients"] == [4, 8, 16, 7, 15, 6, 13]
    assert source["overflow_clock"] == [0, 0, 1, 0, 1, 0, 1]
    records, next_bound = [], None
    for graph in reversed(source["completed_graphs"]):
        path = GRAPHS / graph["raw_artifact"]["filename"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == graph["raw_artifact"]["sha256"]
        width, vertices, edges = BOUND.read_graph(path)
        assert width == graph["width"]
        record = BOUND.bound_graph(width, vertices, edges, next_bound)
        assert len(record["cyclic_components"]) == graph["cyclic_components"]
        next_bound = record["max_path_vertices_bound"]
        records.append(record)
        print(json.dumps(dict(width=width, vertex_bound=next_bound,
                              cyclic_components=len(record["cyclic_components"]))), flush=True)
    records.reverse()
    phase0_vertices = records[0]["path_vertices_bound_by_start_phase"][0]
    periods = (phase0_vertices - 1) // 7
    payload = (json.dumps(dict(records=records), separators=(",", ":")) + "\n").encode()
    artifact = HERE / "scalar_bound_certificate.json.gz"
    with artifact.open("wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", filename="", mtime=0) as stream:
            stream.write(payload)
    report = dict(
        status="WEIGHTED_SCALAR_CLOCK_BOUND", clock=source["outer_coefficients"],
        overflow_clock=source["overflow_clock"], minimum_width_for_direct_bound=source["empty_width"],
        phase0_max_path_vertices_bound=phase0_vertices,
        phase0_max_path_edges_bound=phase0_vertices - 1,
        max_complete_periods_at_width14_or_more=periods,
        max_complete_periods_at_width_L="max(0,ceil((14-L)/3)) + " + str(periods),
        coarse_width_preparation_bound_at_all_widths_at_least1=5 + periods,
        max_complete_periods_at_all_widths_at_least1=4 + periods,
        width_one_check=width_one_check(),
        dependency=dict(path=str(DEPENDENCY.relative_to(HERE.parent)),
                        sha256=hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest()),
        graph_report_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),
        graph_producer_sha256=hashlib.sha256((HERE / "scalar_clock.py").read_bytes()).hexdigest(),
        levels=[{k: record[k] for k in (
            "width", "vertices", "edges", "next_level_vertex_bound", "max_path_vertices_bound",
            "path_vertices_bound_by_start_phase")} for record in records],
        certificate=dict(filename=artifact.name, compressed_bytes=artifact.stat().st_size,
                         sha256=hashlib.sha256(artifact.read_bytes()).hexdigest(),
                         uncompressed_sha256=hashlib.sha256(payload).hexdigest()),
        scope="Conservative bound on consecutive complete periods of the prescribed scalar clock; neither a sharp bound nor an eventual-palindrome theorem.")
    (HERE / "scalar_bound.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in (
        "status", "phase0_max_path_vertices_bound", "phase0_max_path_edges_bound",
        "max_complete_periods_at_width14_or_more", "max_complete_periods_at_all_widths_at_least1")}))


if __name__ == "__main__":
    main()
