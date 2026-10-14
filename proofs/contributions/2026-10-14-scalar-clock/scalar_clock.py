#!/usr/bin/env python3
"""Retain arbitrary temporal correlations for prescribed scalar outer clocks.

This extends the reviewed broader-return graph lift to a one-column root.
No temporal period is imposed on any of the subsequently added columns.
Every raw and recurrent graph is retained; caps give UNKNOWN, not exclusion.
"""

import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
DEPENDENCY = HERE.parent / "2026-10-14-broader-return" / "branching_lift.py"
SPEC = importlib.util.spec_from_file_location("branching_lift", DEPENDENCY)
LIFT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LIFT)
CLOCKS = {
    "seven_4": (4, 8, 16, 7, 15, 6, 13),
    "seven_1": (1, 2, 4, 9, 18, 9, 10),
    "primitive14": (3, 6, 13, 4, 8, 17, 8, 17, 8, 16, 7, 15, 6, 12),
}


def initial(coefficients):
    graph = LIFT.empty(1)
    # In particular q=9 can overflow or not. Compute the actual carry
    # from each input and retain only controls giving the required successor.
    for phase, q in enumerate(coefficients):
        graph["phase"].append(phase)
        graph["last"].append(q)
        graph["low"].append(q // 10)
        graph["parent"].append(LIFT.NONE)
    actual_overflows = []
    for phase, q in enumerate(coefficients):
        target = (phase + 1) % len(coefficients)
        accepted_overflows = set()
        for incoming in (0, 1):
            high, e = (q + incoming) % 10, (q + incoming) // 10
            next_q = q % 10 + (1 if e else high)
            if next_q != coefficients[target]:
                continue
            graph["source"].append(phase)
            graph["target"].append(target)
            graph["label"].append(incoming)
            accepted_overflows.add(e)
        assert len(accepted_overflows) == 1
        actual_overflows.append(accepted_overflows.pop())
    return graph, tuple(actual_overflows)


def run(name):
    output = HERE / name
    output.mkdir(exist_ok=True)
    graph, clock = initial(CLOCKS[name])
    LIFT.HERE, LIFT.CLOCK = output, clock
    result = dict(status="RUNNING", outer_coefficients=CLOCKS[name],
                  overflow_clock=clock, root_width=1,
                  caps=dict(raw_vertices=500000, raw_edges=2000000, width=24),
                  dependency=str(DEPENDENCY.relative_to(HERE.parent.parent.parent)),
                  dependency_sha256=hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest(),
                  completed_graphs=[],
                  scope="Necessary exact prefix relation; arbitrary deeper temporal histories included. A surviving graph is not an infinite integer witness.")
    while True:
        artifact = LIFT.save(graph, "raw")
        graph, metadata = LIFT.recurrent_part(graph)
        metadata.update(width=graph["width"], raw_artifact=artifact,
                        retained_artifact=LIFT.save(graph, "recurrent"))
        result["completed_graphs"].append(metadata)
        print(json.dumps(dict(clock=name, **metadata)), flush=True)
        if not graph["phase"]:
            result["status"] = "EMPTY_AT_FINITE_WIDTH"
            result["empty_width"] = graph["width"]
            break
        vertices, edges = 19 * len(graph["phase"]), 19 * len(graph["source"])
        if vertices > 500000 or edges > 2000000 or graph["width"] >= 24:
            result["status"] = "UNKNOWN_CAP"
            result["next_lift"] = dict(width=graph["width"] + 1,
                                       raw_vertices=vertices, raw_edges=edges)
            break
        (output / "scalar_clock.json").write_text(json.dumps(result, indent=2) + "\n")
        graph = LIFT.lift(graph)
    (output / "scalar_clock.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(clock=name, status=result["status"], last_width=graph["width"])))


if __name__ == "__main__":
    for selected in (sys.argv[1:] or ["seven_4"]):
        run(selected)
