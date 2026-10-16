#!/usr/bin/env python3
"""Independently audit the existing width-1..3 fixed-clock classifications.

The transition oracle uses ordinary decimal integers. The graph audit uses
reverse breadth-first search and indegree pruning, independently of the
path-label algorithms in the two reviewed scripts. No larger width is used.
"""

from collections import defaultdict, deque
from functools import lru_cache
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
REVIEWED = [HERE / name for name in (
    "fixed_clock_controls.py", "fixed_zero_prefix.py",
    "fixed_clock_results.json", "fixed_zero_prefix.json",
)]


def hashes():
    result = {}
    for path in REVIEWED:
        blob = path.read_bytes()
        result[path.name] = {
            "sha256": hashlib.sha256(blob).hexdigest(),
            "git_blob_sha1": hashlib.sha1(f"blob {len(blob)}\0".encode() + blob).hexdigest(),
        }
    return result


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(None)
def integer_transition(prefix, gamma):
    width = len(prefix)
    # Pair coefficients are prefix, center 18*gamma, reversed prefix.
    # At the center, adding either carry zero or one gives outgoing gamma.
    digits = ([max(q - 9, 0) for q in prefix] + [9 * gamma]
              + [min(q, 9) for q in reversed(prefix)])
    assert digits[-1] > 0 and all(0 <= d <= 9 for d in digits)
    coefficients = tuple(digits[i] + digits[-1-i] for i in range(len(digits)))
    assert coefficients[:width] == prefix
    carry = 0
    for q in coefficients[:width+1]:
        carry = (q + carry) // 10
    assert carry == gamma
    n = int("".join(map(str, reversed(digits))))
    next_n = n + int(str(n)[::-1])
    out = tuple(map(int, reversed(str(next_n))))
    next_prefix = tuple(out[i] + out[-1-i] for i in range(width))
    assert 1 <= next_prefix[0] <= 18
    assert all(0 <= q <= 18 for q in next_prefix)
    return next_prefix, n, next_n


def is_unsafe(prefix):
    fits_small_branch = all(q <= 9 for q in prefix)
    fits_overflow_branch = prefix[0] == 11 and set(prefix) <= {0, 11}
    return fits_small_branch or fits_overflow_branch


def canonical_cycle(cycle):
    cycle = tuple(cycle)
    return min(cycle[i:] + cycle[:i] for i in range(len(cycle)))


def audit_graph(width, schedule):
    states = [((a,) + tail, phase)
              for a in range(1, 19)
              for tail in product(range(19), repeat=width-1)
              for phase in range(len(schedule))]
    state_set = set(states)
    successor = {}
    predecessors = defaultdict(list)
    for prefix, phase in states:
        target = (integer_transition(prefix, schedule[phase])[0],
                  (phase + 1) % len(schedule))
        assert target in state_set
        if not is_unsafe(prefix):
            successor[(prefix, phase)] = target
            predecessors[target].append((prefix, phase))

    distances = {state: 0 for state in states if is_unsafe(state[0])}
    queue = deque(distances)
    while queue:
        target = queue.popleft()
        for state in predecessors[target]:
            if state not in distances:
                distances[state] = distances[target] + 1
                queue.append(state)

    survivors = state_set - set(distances)
    indegree = {state: 0 for state in survivors}
    for state in survivors:
        assert successor[state] in survivors
        indegree[successor[state]] += 1
    queue = deque(state for state in survivors if indegree[state] == 0)
    removed = set()
    while queue:
        state = queue.popleft()
        removed.add(state)
        target = successor[state]
        indegree[target] -= 1
        if indegree[target] == 0:
            queue.append(target)

    unvisited = survivors - removed
    cycles = []
    while unvisited:
        start = min(unvisited)
        cycle, state = [], start
        while state not in cycle:
            assert state in unvisited
            cycle.append(state)
            unvisited.remove(state)
            state = successor[state]
        assert state == start
        cycles.append(canonical_cycle(cycle))
    cycles.sort()

    witnesses = []
    for cycle in cycles:
        edges = []
        for prefix, phase in cycle:
            gamma = schedule[phase]
            target, n, next_n = integer_transition(prefix, gamma)
            assert str(next_n) != str(next_n)[::-1]
            edges.append({"prefix": prefix, "phase": phase, "gamma": gamma,
                          "ordinary_seed": n, "ordinary_next": next_n,
                          "next_prefix": target,
                          "next_phase": (phase+1) % len(schedule)})
        witnesses.append(edges)
    return {
        "width": width,
        "schedule": schedule,
        "phase_augmented_states": len(states),
        "initially_unsafe_states": sum(is_unsafe(p) for p, _ in states),
        "states_eventually_unsafe": len(distances),
        "states_in_safe_cycle_basins": len(survivors),
        "max_escape_steps_among_escaping_states": max(distances.values()),
        "safe_cycle_count": len(cycles),
        "safe_cycle_basin_states": sorted(survivors),
        "cycle_edges_with_independent_integer_realizations": witnesses,
    }, cycles


def main():
    original_hashes = hashes()
    clock = load_module("reviewed_fixed_clock", HERE / "fixed_clock_controls.py")
    zero = load_module("reviewed_fixed_zero", HERE / "fixed_zero_prefix.py")
    for width in range(1, 4):
        for a in range(1, 19):
            for tail in product(range(19), repeat=width-1):
                prefix = (a,) + tail
                assert clock.safe(prefix) == zero.safe(prefix) == (not is_unsafe(prefix))
                for gamma in (0, 1):
                    target = integer_transition(prefix, gamma)[0]
                    assert clock.next_prefix(prefix, gamma) == target
                    if gamma == 0:
                        assert zero.successor(prefix) == target

    clock_reports = json.loads((HERE / "fixed_clock_results.json").read_text())["results"]
    zero_reports = json.loads((HERE / "fixed_zero_prefix.json").read_text())["widths"]
    audits = []
    for width in range(1, 4):
        for schedule in ((0,), (1,), (0, 1)):
            result, cycles = audit_graph(width, schedule)
            if schedule == (0,):
                expected = next(row for row in zero_reports if row["width"] == width)
                assert result["phase_augmented_states"] == expected["canonical_prefixes"]
                assert result["initially_unsafe_states"] == expected["initially_unsafe"]
                assert result["states_eventually_unsafe"] == expected["eventual_unsafe_prefixes"]
                assert result["states_in_safe_cycle_basins"] == expected["safe_cycle_basin_prefixes"]
                assert result["max_escape_steps_among_escaping_states"] == expected["maximum_finite_escape_steps"]
                expected_cycles = sorted(canonical_cycle(tuple((tuple(p), 0) for p in cycle))
                                         for cycle in expected["safe_cycles"])
            else:
                expected = next(row for row in clock_reports if row["width"] == width
                                and tuple(row["schedule"]) == schedule)
                for key in ("phase_augmented_states", "states_eventually_unsafe",
                            "states_in_safe_cycle_basins", "max_escape_steps_among_escaping_states"):
                    assert result[key] == expected[key], (width, schedule, key)
                for cycle in expected["complete_safe_cycles"]:
                    for state in cycle:
                        assert state["outgoing_input"] == schedule[state["phase"]]
                expected_cycles = sorted(canonical_cycle(tuple((tuple(s["prefix"]), s["phase"])
                                                                for s in cycle))
                                         for cycle in expected["complete_safe_cycles"])
            assert cycles == expected_cycles, (width, schedule, "cycle mismatch")
            audits.append(result)
    assert hashes() == original_hashes, "Reviewed inputs changed during audit"
    report = {
        "result": "PASS",
        "reviewed_sources": original_hashes,
        "independent_ordinary_integer_transition_checks": integer_transition.cache_info().currsize,
        "total_classified_phase_states": sum(row["phase_augmented_states"] for row in audits),
        "audit_method": "ordinary integer transition oracle; reverse BFS to unsafe states; indegree pruning for safe cycles",
        "results": audits,
        "limitations": [
            "Only the already reported widths 1,2,3 and schedules 0,1,01 were audited.",
            "Each cycle edge has its own independent finite integer realization.",
            "The realizations need not concatenate into one integer orbit or realize the clock forever.",
            "Unsafe prefix means absence of this prefix obstruction, not necessarily a palindromic next integer.",
        ],
    }
    (HERE / "independent_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in
                     ("result", "independent_ordinary_integer_transition_checks", "total_classified_phase_states")}))


if __name__ == "__main__":
    main()
