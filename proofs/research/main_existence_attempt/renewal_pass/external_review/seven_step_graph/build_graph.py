#!/usr/bin/env python3
"""Independent reconstruction of the six-column necessary phase graph.

Based on the mathematical boundary formula, not imported from the other
stream's graph implementation. Every labeled accepted/rejected control
and every rank is retained. No actual realization of arbitrary graph
paths is assumed.
"""
from collections import deque
from pathlib import Path
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent
PHASES = ((4,4,0),(8,8,0),(16,16,0),(7,14,7),(15,8,15),(6,14,14),(13,9,9))
PER_PHASE = 19**3
SIZE = 7 * PER_PHASE


def decode(v):
    phase, suffix = divmod(v, PER_PHASE)
    a, suffix = divmod(suffix, 19**2)
    b, c = divmod(suffix, 19)
    return phase, PHASES[phase] + (a,b,c)


def normalize(word, incoming):
    digits = []
    carry = incoming
    for q in word:
        carry, digit = divmod(q + carry, 10)
        digits.append(digit)
    return digits, carry


def boundary(p, c):
    width = len(p)
    low, _ = normalize(p, 0)
    high, overflow = normalize(tuple(reversed(p)), c)
    if overflow == 0:
        return tuple(low[i] + high[width-1-i] for i in range(width))
    assert overflow == 1
    return (low[0] + 1,) + tuple(low[i] + high[width-i] for i in range(1,width))


def main():
    targets = []
    predecessors = [[] for _ in range(SIZE)]
    remaining = [0] * SIZE
    for v in range(SIZE):
        phase, p = decode(v)
        next_phase = (phase + 1) % 7
        row = []
        for c in (0,1):
            q = boundary(p, c)
            assert all(0 <= x <= 18 for x in q)
            target = -1
            if q[:3] == PHASES[next_phase]:
                target = next_phase * PER_PHASE + q[3]*19**2 + q[4]*19 + q[5]
                predecessors[target].append(v)
                remaining[v] += 1
            row.append(target)
        targets.append(row)
    rank = [0] * SIZE
    queue = deque(v for v in range(SIZE) if remaining[v] == 0)
    removed = 0
    while queue:
        v = queue.popleft()
        removed += 1
        for pred in predecessors[v]:
            rank[pred] = max(rank[pred], rank[v] + 1)
            remaining[pred] -= 1
            if remaining[pred] == 0:
                queue.append(pred)
    assert removed == SIZE, "Graph contains a directed cycle"
    maximum = max(rank[:PER_PHASE])
    assert maximum == 26
    prefix_controls = []
    for mask in range(128):
        controls = [(mask >> t) & 1 for t in range(7)]
        p = PHASES[0]
        trace = [p]
        overflows = []
        for c in controls:
            _, e = normalize(tuple(reversed(p)), c)
            overflows.append(e)
            p = boundary(p,c)
            trace.append(p)
        returned = p == PHASES[0]
        guard = all(controls[t] == 0 for t in (0,1,3,5)) and controls[6] == 1
        assert returned == guard
        if returned:
            assert trace == list(PHASES) + [PHASES[0]]
            assert overflows == [0,0,1,0,1,0,1]
        prefix_controls.append({"controls": controls, "trace": trace,
                                "overflows": overflows, "returned": returned})
    assert sum(r['returned'] for r in prefix_controls) == 4
    payload = {"phases": PHASES, "vertex_order": "phase then lexicographic coefficient3,4,5 in 0..18",
               "targets": targets, "rank": rank,
               "seven_step_prefix_controls": prefix_controls,
               "target_schema": "two entries per vertex, actual deeper incoming carry0 then1; -1 means rejected next phase"}
    decoded = json.dumps(payload, separators=(',', ':')).encode()
    archive = gzip.compress(decoded, mtime=0)
    (HERE/'six_prefix_graph.json.gz').write_bytes(archive)
    edges = sum(t >= 0 for row in targets for t in row)
    result = {"status": "ACYCLIC_NECESSARY_GRAPH", "vertices": SIZE,
              "labeled_controls": 2*SIZE, "accepted_labeled_edges": edges,
              "rejected_controls": 2*SIZE-edges, "rank_max_by_phase":
              [max(rank[i*PER_PHASE:(i+1)*PER_PHASE]) for i in range(7)],
              "phase_zero_maximum_rank": maximum,
              "four_seven_step_returns_excluded": True,
              "all_seven_step_prefix_controls": 128, "returning_control_words": 4,
              "actual_orbit_inclusion": "separate written argument",
              "graph_rank_kernel_checked_in_Lean": False,
              "main_existence_proved": False,
              "compressed_sha256": hashlib.sha256(archive).hexdigest(),
              "decoded_sha256": hashlib.sha256(decoded).hexdigest(),
              "compressed_bytes": len(archive), "decoded_bytes": len(decoded),
              "external_claim_commit": "8a42fe14262fee12ce1c8b40bf25e97b94044742"}
    (HERE/'graph_summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
