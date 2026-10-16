#!/usr/bin/env python3
"""Exact small-state tests of proposed fixed interior-carry schedules.

Uses the established unrestricted prefix map. A safe cycle is an
obstruction to this particular escape strategy, never a Lychrel witness.
Every searched state space and every surviving cycle is retained.
"""
from itertools import product
import json
from pathlib import Path


def next_prefix(p, gamma):
    lo, hi = [], [0]*len(p)
    carry = 0
    for q in p:
        carry, digit = divmod(q+carry, 10)
        lo.append(digit)
    carry = gamma
    for i in range(len(p)-1, -1, -1):
        carry, hi[i] = divmod(p[i]+carry, 10)
    if carry:
        return (lo[0]+1, *(lo[i]+hi[i-1] for i in range(1, len(p))))
    return tuple(a+b for a, b in zip(lo, hi))


def safe(p):
    return (max(p) >= 10
            and not (p[0] == 11 and all(x in (0, 11) for x in p)))


def analyze(k, schedule):
    # Eventual label -1 means an unsafe prefix is encountered; otherwise
    # the label identifies one complete safe periodic orbit.
    labels = {}
    cycles = []
    max_escape = 0
    for first in range(1, 19):
        for tail in product(range(19), repeat=k-1):
            for phase in range(len(schedule)):
                state = ((first, *tail), phase)
                if state in labels:
                    continue
                path, local = [], {}
                while state not in labels and state not in local and safe(state[0]):
                    local[state] = len(path)
                    path.append(state)
                    p, s = state
                    state = (next_prefix(p, schedule[s]), (s+1)%len(schedule))
                if not safe(state[0]):
                    labels[state] = (-1, 0)
                if state in local:
                    start = local[state]
                    cycle = path[start:]
                    label = len(cycles)
                    cycles.append([{"prefix": list(p), "phase": s,
                                    "outgoing_input": schedule[s]} for p, s in cycle])
                    for x in cycle:
                        labels[x] = (label, 0)
                    path = path[:start]
                label, distance = labels[state]
                for x in reversed(path):
                    distance += 1
                    labels[x] = (label, distance)
                    if label == -1:
                        max_escape = max(max_escape, distance)
    total = 18*19**(k-1)*len(schedule)
    assert len(labels) == total
    for (p, s), (label, distance) in labels.items():
        if not safe(p):
            assert label == -1 and distance == 0
        elif label == -1:
            dest = (next_prefix(p, schedule[s]), (s+1)%len(schedule))
            assert labels[dest] == (-1, distance-1)
    return {"width": k, "schedule": schedule, "phase_augmented_states": total,
            "states_eventually_unsafe": sum(label == -1 for label, _ in labels.values()),
            "states_in_safe_cycle_basins": sum(label != -1 for label, _ in labels.values()),
            "max_escape_steps_among_escaping_states": max_escape,
            "complete_safe_cycles": cycles}


def main():
    results = [analyze(k, s) for s in ((1,), (0, 1)) for k in range(1, 4)]
    report = {"status": "finite strategy classification only", "results": results,
              "scope": "Fixed schedules are freely imposed abstract inputs, not actual fixed-seed carry histories. A safe cycle disproves only escape under that schedule. No universal safe trap or Lychrel witness is claimed."}
    Path(__file__).with_name("fixed_clock_results.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps([{k:v for k,v in r.items() if k != "complete_safe_cycles"}
                      | {"safe_cycle_count": len(r["complete_safe_cycles"])} for r in results]))


if __name__ == "__main__":
    main()
