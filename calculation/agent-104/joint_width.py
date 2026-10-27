#!/usr/bin/env python3
"""COMPUTED controls for the exact joint normalized finite functional graph.

States have B width M and C width W-1 or W, with alphabet 0..2b-2.  All
coefficient states are included, even when Hyp is false.  An edge requires
source Hyp and the exact trim equations; destination Hyp is not prefiltered.
The forced trims are u=gamma and v=1 iff gamma=1 and len(C)=W.

The finite carrier has N=(2b-1)^M*((2b-1)^(W-1)+(2b-1)^W) states.  Extracted
simple cycles have period <=N.  Exhaustion is reported only as COMPLETE;
state/time cutoffs are UNDECIDED and carry no negative cycle verdict.

Run bounded controls: python3 -O calculation/agent-104/joint_width.py selftest
Optional tiny graph:  python3 calculation/agent-104/joint_width.py graph 2 2 4

Known-fixture normalization reuses Agent114's uniform exterior padding and
Agent104's balanced_width.py.  Independent all-trim checks use Agent114's
whole-integer state arithmetic; found cycles also use the distinct whole-
integer oracle in balanced_width.py.  No logs or result files are written.
"""

import argparse
from collections import Counter
import importlib
import importlib.util
from itertools import product
import json
import math
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
BASES = {2, 4, 8, 11, 16, 17, 26, 32}
sys.dont_write_bytecode = True


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def parameters(base, exterior_width, center_cap):
    require(type(base) is int and base >= 2, "base must be a natural integer >=2")
    require(type(exterior_width) is int and exterior_width >= 0, "M must be natural")
    require(type(center_cap) is int and center_cap >= 2, "W must be a natural integer >=2")


def state_count(base, exterior_width, center_cap):
    parameters(base, exterior_width, center_cap)
    q = 2*base-1
    return (q+1) * q**(exterior_width+center_cap-1)


def node(base, exterior_width, center_cap, value):
    parameters(base, exterior_width, center_cap)
    require(isinstance(value, (tuple, list)) and len(value) == 2, "state must have B,C")
    require(all(isinstance(word, (tuple, list)) for word in value), "state words must be sequences")
    B, C = map(tuple, value)
    require(len(B) == exterior_width and len(C) in (center_cap-1, center_cap),
            "state is outside the prescribed widths")
    require(all(type(x) is int and 0 <= x < 2*base-1 for x in B+C),
            "state contains a nonalphabet coefficient")
    return B, C


def load_dependencies():
    path = ROOT / "calculation/agent-104/balanced_width.py"
    spec = importlib.util.spec_from_file_location("a104_joint_balanced", path)
    require(spec is not None and spec.loader is not None, "cannot load balanced-width dependency")
    balanced = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(balanced)
    mirror, transport = balanced.load_dependencies()
    sys.path.insert(0, str(ROOT / "calculation/agent-114"))
    try:
        uniform = importlib.import_module("uniform_exterior_controls")
    finally:
        sys.path.pop(0)
    return mirror, transport, balanced, uniform


def successor(mirror, base, exterior_width, center_cap, value):
    B, C = node(base, exterior_width, center_cap, value)
    B, C = list(B), list(C)
    if not mirror.hyp(base, B, C):
        return None
    gamma = mirror.gam(base, B, C)
    require(gamma in (0, 1), "valid source has nonbinary overflow")
    u, v = gamma, int(gamma == 1 and len(C) == center_cap)
    raw_B, raw_C = mirror.nextB(base, B, C), mirror.nextC(base, B, C)
    require(len(raw_B) == exterior_width+gamma and len(raw_C) == len(C)+gamma,
            "raw length law failed")
    B2 = raw_B[:exterior_width]
    C2 = raw_C[v:len(raw_C)-v] if v else raw_C
    h = base-1
    if raw_B != B2 + [h]*u or raw_C != [h]*v + C2 + [h]*v:
        return None
    target = node(base, exterior_width, center_cap, (B2, C2))
    edge = (B, C, B2, C2, u, v)
    require(mirror.edgeOK(base, edge), "forced edge disagrees with exact mirror")
    return target, edge


def integer_candidates(uniform, base, exterior_width, center_cap, source):
    """Enumerate every permitted trim; do not assume either forced trim."""
    arithmetic, canonical = uniform.arithmetic, uniform.canonical
    B, C = source
    if not arithmetic.hyp(base, B, C):
        return []
    raw = arithmetic.state(base, B, C)
    result = []
    for B2, u in canonical.all_suffix_splits(base, raw.next_b):
        if len(B2) != exterior_width:
            continue
        for C2, v in canonical.all_center_splits(base, raw.next_c):
            if len(C2) in (center_cap-1, center_cap):
                target = node(base, exterior_width, center_cap, (B2, C2))
                edge = arithmetic.Edge(B, C, B2, C2, u, v)
                require(arithmetic.edge_ok(base, edge), "independent trim enumeration failed")
                result.append((target, u, v))
    return result


def all_target_candidates(uniform, base, source, states, check_time):
    """A separate literal all-target/all-natural-trim equality relation."""
    if not uniform.arithmetic.hyp(base, *source):
        return [], 0
    raw = uniform.arithmetic.state(base, *source)
    h = (base-1,)
    result = []
    for i, target in enumerate(states):
        if i % 128 == 0:
            check_time()
        B2, C2 = target
        for u in range(len(raw.next_b)+1):
            if raw.next_b != B2 + h*u:
                continue
            for v in range(len(raw.next_c)//2+1):
                if raw.next_c == h*v + C2 + h*v:
                    result.append((target, u, v))
    return result, len(states)


class Cutoff(Exception):
    pass


def complete_graph(dependencies, base, exterior_width, center_cap,
                   max_states=20000, seconds=30, all_targets=False):
    parameters(base, exterior_width, center_cap)
    require(type(max_states) is int and max_states > 0, "state cap must be positive")
    require(type(seconds) in (int, float) and math.isfinite(seconds) and 0 < seconds <= 1500,
            "wall budget must be finite, positive and <=1500 seconds")
    mirror, _, balanced, uniform = dependencies
    q, exponent = 2*base-1, exterior_width+center_cap-1
    descriptor = {"base": base, "M": exterior_width, "W": center_cap,
                  "state_bound_formula": f"({q}+1)*{q}^{exponent}"}
    # Avoid constructing an enormous integer for an obviously oversized scope.
    if exponent >= max_states.bit_length():
        return {"summary": {**descriptor, "status": "UNDECIDED", "reason": "state cap"}}
    total = state_count(base, exterior_width, center_cap)
    descriptor["states"] = total
    if total > max_states:
        return {"summary": {**descriptor, "status": "UNDECIDED", "reason": "state cap"}}
    deadline = time.monotonic()+seconds

    def check_time():
        if time.monotonic() >= deadline:
            raise Cutoff("wall budget")

    try:
        states = []
        for B in product(range(q), repeat=exterior_width):
            for length in (center_cap-1, center_cap):
                for C in product(range(q), repeat=length):
                    if len(states) % 128 == 0:
                        check_time()
                    states.append((B, C))
        index = {value: i for i, value in enumerate(states)}
        require(len(states) == len(index) == total, "finite carrier enumeration is incomplete")
        following, edges = [None]*total, [None]*total
        hyp_count = edge_count = target_hyp_count = target_pairs = 0
        for i, source in enumerate(states):
            if i % 128 == 0:
                check_time()
            hyp = mirror.hyp(base, list(source[0]), list(source[1]))
            require(hyp == uniform.arithmetic.hyp(base, *source), "Hyp implementations disagree")
            hyp_count += hyp
            answer = successor(mirror, base, exterior_width, center_cap, source)
            expected = [] if answer is None else [(answer[0], answer[1][4], answer[1][5])]
            independent = integer_candidates(uniform, base, exterior_width, center_cap, source)
            require(independent == expected, "all-trim integer relation disagrees with forced successor")
            if all_targets:
                literal, pairs = all_target_candidates(uniform, base, source, states, check_time)
                require(literal == expected, "literal all-target relation disagrees with successor")
                target_pairs += pairs
            if answer is not None:
                target, edge = answer
                require(target in index, "successor leaves the enumerated carrier")
                following[i], edges[i] = index[target], edge
                edge_count += 1
                target_hyp_count += mirror.hyp(base, list(target[0]), list(target[1]))
        colors, cycles = [0]*total, []
        for start in range(total):
            if start % 128 == 0:
                check_time()
            if colors[start]:
                continue
            path, positions, current = [], {}, start
            while current is not None and colors[current] == 0:
                if len(path) % 128 == 0:
                    check_time()
                positions[current] = len(path)
                path.append(current)
                colors[current] = 1
                current = following[current]
            if current is not None and colors[current] == 1:
                require(current in positions, "cycle extraction crossed an unfinished traversal")
                ids = path[positions[current]:]
                cycle = [edges[i] for i in ids]
                require(0 < len(ids) == len(set(ids)) <= total, "simple-cycle period bound failed")
                require(mirror.cycleOK(base, cycle, cycle[0][0], cycle[0][1]),
                        "extracted graph cycle fails exact mirror")
                for edge in cycle:
                    balanced.integer_edge(base, edge)
                cycles.append(cycle)
            for i in path:
                colors[i] = 2
        require(all(color == 2 for color in colors), "functional graph traversal is incomplete")
        check_time()
        return {"summary": {**descriptor, "status": "COMPLETE", "hyp_states": hyp_count,
                "edges": edge_count, "edges_to_hyp_states": target_hyp_count,
                "integer_successor_comparisons": total, "all_targets": all_targets,
                "literal_target_pairs": target_pairs, "cycles": len(cycles),
                "cycle_periods": sorted(len(cycle) for cycle in cycles)}, "cycles": cycles}
    except (Cutoff, MemoryError) as error:
        return {"summary": {**descriptor, "status": "UNDECIDED",
                            "reason": str(error) or "memory allocation"}}


def normalize_fixture(dependencies, base, edges, exterior_width, center_cap):
    parameters(base, exterior_width, center_cap)
    mirror, transport, balanced, uniform = dependencies
    source = transport.source_edges(mirror, base, edges)
    records = [uniform.Edge(*(tuple(word) for word in edge[:4]), *edge[4:]) for edge in source]
    fixed, _, _ = uniform.uniform_chain(base, records, records[0].B, records[0].C, exterior_width)
    fixed = [edge.mirror_data() for edge in fixed]
    result = balanced.balance_cycle(mirror, transport, base, fixed, center_cap)
    require(mirror.cycleOK(base, result, result[0][0], result[0][1]), "joint fixture does not close")
    require(sum(e[4]+e[5] for e in result) == sum(e[4]+e[5] for e in source),
            "joint normalization changed total gain")
    for original, edge in zip(source, result):
        source_stream = balanced.integer_edge(base, original)
        require(balanced.integer_edge(base, edge) == source_stream, "joint stream changed")
        answer = successor(mirror, base, exterior_width, center_cap, (edge[0], edge[1]))
        require(answer is not None and answer[1] == edge, "fixture does not follow normalized graph")
    # A repeated certificate can be longer than the carrier. Extract a simple
    # closed subwalk before invoking the finite-state period bound.
    seen = {}
    states = [(tuple(e[0]), tuple(e[1])) for e in result]
    states.append((tuple(result[-1][2]), tuple(result[-1][3])))
    for i, value in enumerate(states):
        if value in seen:
            cycle = result[seen[value]:i]
            require(0 < len(cycle) <= state_count(base, exterior_width, center_cap),
                    "known-fixture simple-period bound failed")
            require(mirror.cycleOK(base, cycle, cycle[0][0], cycle[0][1]),
                    "known-fixture subcycle fails exact replay")
            return result, len(cycle)
        seen[value] = i
    raise RuntimeError("closed fixture has no repeated state")


def rejection_controls(dependencies, fixture):
    mirror = dependencies[0]
    base, edges = fixture
    tests = [
        lambda: complete_graph(dependencies, 1, 1, 2),
        lambda: complete_graph(dependencies, 2, -1, 2),
        lambda: complete_graph(dependencies, 2, True, 2),
        lambda: complete_graph(dependencies, 2, 1, 1),
        lambda: complete_graph(dependencies, 2, 1, 2.0),
        lambda: complete_graph(dependencies, 2, 1, 2, max_states=0),
        lambda: complete_graph(dependencies, 2, 1, 2, seconds=-1),
        lambda: complete_graph(dependencies, 2, 1, 2, seconds=float("nan")),
        lambda: successor(mirror, 2, 1, 2, None),
        lambda: successor(mirror, 2, 1, 2, ((), (0,))),
        lambda: successor(mirror, 2, 1, 2, ((1,), ())),
        lambda: successor(mirror, 2, 1, 2, ((-1,), (0,))),
        lambda: successor(mirror, 2, 1, 2, ((3,), (0,))),
        lambda: successor(mirror, 2, 1, 2, ((True,), (0,))),
        lambda: normalize_fixture(dependencies, base, edges, 0, 4),
        lambda: normalize_fixture(dependencies, base, edges, 2, 2),
        lambda: normalize_fixture(dependencies, base, [], 2, 4),
    ]
    for check in tests:
        try:
            check()
        except (RuntimeError, ValueError):
            continue
        raise RuntimeError("malformed graph input was accepted")
    for limit in ({"max_states": 1}, {"seconds": 1e-12}):
        result = complete_graph(dependencies, 2, 2, 4, **limit)
        require(result["summary"]["status"] == "UNDECIDED" and "cycles" not in result,
                "a cutoff acquired a false negative cycle verdict")
    return len(tests), 2


def selftest(dependencies):
    mirror, transport, _, _ = dependencies
    fixtures = sorted(mirror._lean_certs())
    require(len(fixtures) == 8 and {b for b, _ in fixtures} == BASES, "known source set changed")
    rejected, cutoff_controls = rejection_controls(dependencies, fixtures[0])
    fixture_cycles = fixture_edges = 0
    for base, original in fixtures:
        M = max(len(e[j]) for e in original for j in (0, 2))
        W = max(2, max(len(e[j]) for e in original for j in (1, 3)))
        periods = set()
        local = 0
        for repeat in (1, 2):
            for rotated in transport.distinct_rotations(original * repeat):
                for m, w in product((M, M+1), (W, W+1)):
                    normalized, period = normalize_fixture(dependencies, base, rotated, m, w)
                    fixture_cycles += 1
                    fixture_edges += len(normalized)
                    local += 1
                    periods.add(period)
        print("KNOWN_FIXTURE " + json.dumps({"base": base, "minimal_caps": [M, W],
              "normalized_cycles": local, "simple_periods": sorted(periods),
              "scope": "membership controls, not exhaustive graphs"}, sort_keys=True), flush=True)
    scopes = [(2, 0, 2), (2, 1, 2), (2, 1, 3), (2, 2, 3), (2, 2, 4),
              (2, 3, 4), (2, 2, 5), (3, 1, 2), (4, 1, 2), (10, 1, 2)]
    totals = Counter()
    for base, M, W in scopes:
        literal = state_count(base, M, W) <= 150
        result = complete_graph(dependencies, base, M, W, all_targets=literal)
        summary = result["summary"]
        require(summary["status"] == "COMPLETE", "selftest graph is UNDECIDED")
        if (base, M, W) in ((2, 2, 4), (2, 3, 4), (2, 2, 5)):
            require(summary["cycles"] > 0, "positive complete-graph control lost its cycle")
        if base == 10 and result["cycles"]:
            print("DECIMAL_CANDIDATE " + json.dumps(result["cycles"][0]), flush=True)
        for key in ("states", "edges", "integer_successor_comparisons", "literal_target_pairs", "cycles"):
            totals[key] += summary[key]
        totals["extracted_cycle_edges"] += sum(map(len, result["cycles"]))
        totals["literal_graphs"] += literal
        print("GRAPH " + json.dumps(summary, sort_keys=True), flush=True)
    print("JOINT_WIDTH_PASS " + json.dumps({"status": "COMPUTED", "known_bases": 8,
          "fixture_cycles": fixture_cycles, "fixture_edges": fixture_edges,
          "complete_graphs": len(scopes), "malformed_inputs_rejected": rejected,
          "cutoffs_undecided": cutoff_controls, "optimized_python": not __debug__,
          **totals}, sort_keys=True), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode")
    sub.add_parser("selftest")
    graph = sub.add_parser("graph")
    graph.add_argument("base", type=int)
    graph.add_argument("M", type=int)
    graph.add_argument("W", type=int)
    graph.add_argument("--max-states", type=int, default=20000)
    graph.add_argument("--seconds", type=float, default=30)
    graph.add_argument("--all-targets", action="store_true")
    graph.add_argument("--witness", action="store_true")
    args = parser.parse_args()
    dependencies = load_dependencies()
    if args.mode in (None, "selftest"):
        selftest(dependencies)
        return 0
    result = complete_graph(dependencies, args.base, args.M, args.W,
                            args.max_states, args.seconds, args.all_targets)
    print("GRAPH " + json.dumps(result["summary"], sort_keys=True), flush=True)
    if result["summary"]["status"] != "COMPLETE":
        return 2
    if result["cycles"] and (args.witness or args.base == 10):
        print(("DECIMAL_CANDIDATE " if args.base == 10 else "WITNESS ")
              + json.dumps(result["cycles"][0]), flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, ValueError) as error:
        print("CHECK FAILED: " + str(error), file=sys.stderr)
        sys.exit(1)
