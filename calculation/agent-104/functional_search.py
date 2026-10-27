#!/usr/bin/env python3
"""COMPUTED controls for the literal bounded positive-return search.

This follows Agent104.NeutralFunctionalSearch: test the cheap carrier predicate,
compute raw nextB/nextC, construct the sole forced-trim target, and apply exact
edgeOK.  Destination Hyp is deliberately not tested.  A return requires at
least one accepted edge; a dead successor stops immediately.  The iteration
does not use graph coloring or reject a foreign repeated state early.

The Lean theorem concerns its own definitions.  These external Python controls
are differential computations, not a formally proved extraction/refinement.
They compare every successor and every N-fuel return in ten small complete
graphs against joint_width.py, whose oracle enumerates all natural trims using
independent whole-integer arithmetic.  Known certificates are orbit controls;
their much larger carriers are not exhausted.  Resource cutoffs are UNDECIDED
and have no Boolean verdict.  No logs or result files are written.

Run: python3 -O calculation/agent-104/functional_search.py selftest
     python3 calculation/agent-104/functional_search.py graph 2 2 4 --witness
"""

import argparse
from collections import Counter
import importlib.util
from itertools import product
import json
import math
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
BASES = {2, 4, 8, 11, 16, 17, 26, 32}
SCOPES = [(2, 0, 2), (2, 1, 2), (2, 1, 3), (2, 2, 3), (2, 2, 4),
          (2, 3, 4), (2, 2, 5), (3, 1, 2), (4, 1, 2), (10, 1, 2)]
sys.dont_write_bytecode = True


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def parameters(base, M, W):
    require(type(base) is int and base >= 2, "base must be a natural integer >=2")
    require(type(M) is int and M >= 0, "M must be a natural integer")
    require(type(W) is int and W >= 2, "W must be a natural integer >=2")


def key(value):
    """Reject objects outside the Lean State type; shape/alphabet are predicates."""
    require(isinstance(value, (tuple, list)) and len(value) == 2, "state must contain B,C")
    require(all(isinstance(word, (tuple, list)) for word in value), "state words must be sequences")
    B, C = map(tuple, value)
    require(all(type(x) is int and x >= 0 for x in B+C), "state coefficients must be natural integers")
    return B, C


def state_ok(base, M, W, value):
    parameters(base, M, W)
    B, C = key(value)
    return len(B) == M and len(C) in (W-1, W) and all(x < 2*base-1 for x in B+C)


def state_count(base, M, W):
    parameters(base, M, W)
    q = 2*base-1
    return q**M * (q**(W-1)+q**W)


def states(base, M, W):
    parameters(base, M, W)
    q = 2*base-1
    for B in product(range(q), repeat=M):
        for length in (W-1, W):
            for C in product(range(q), repeat=length):
                yield B, C


def successor(mirror, base, M, W, value):
    """Literal successor: no source Hyp shortcut and no destination Hyp filter."""
    B, C = key(value)
    if not state_ok(base, M, W, (B, C)):
        return None
    B, C = list(B), list(C)
    gamma = mirror.gam(base, B, C)
    v = int(gamma == 1 and len(C) == W)
    raw_B, raw_C = mirror.nextB(base, B, C), mirror.nextC(base, B, C)
    # Lean: rawB.take M; (rawC.drop v).take (rawC.length - 2*v).
    B2, C2 = raw_B[:M], raw_C[v:v+max(0, len(raw_C)-2*v)]
    target = tuple(B2), tuple(C2)
    edge = B, C, B2, C2, gamma, v
    if state_ok(base, M, W, target) and mirror.edgeOK(base, edge):
        return target, edge
    return None


def load_dependencies():
    spec = importlib.util.spec_from_file_location(
        "a104_functional_joint", ROOT / "calculation/agent-104/joint_width.py")
    require(spec is not None and spec.loader is not None, "cannot load joint-width oracle")
    joint = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(joint)
    return joint, joint.load_dependencies()


class Cutoff(Exception):
    pass


class Engine:
    """Cache only this file's successor; all loop iterations still consume fuel."""
    def __init__(self, mirror, base, M, W, max_states=20000, max_steps=2000000, seconds=30):
        parameters(base, M, W)
        require(type(max_states) is int and max_states > 0, "state cap must be positive")
        require(type(max_steps) is int and max_steps > 0, "step cap must be positive")
        require(type(seconds) in (int, float) and math.isfinite(seconds) and 0 < seconds <= 1500,
                "wall budget must be finite, positive and <=1500 seconds")
        self.mirror, self.base, self.M, self.W = mirror, base, M, W
        self.max_states, self.max_steps = max_states, max_steps
        self.deadline = time.monotonic()+seconds
        self.cache, self.calls = {}, 0

    def check_time(self):
        if time.monotonic() >= self.deadline:
            raise Cutoff("wall budget")

    def step(self, current):
        self.check_time()
        if self.calls >= self.max_steps:
            raise Cutoff("step cap")
        if current not in self.cache:
            if len(self.cache) >= self.max_states:
                raise Cutoff("state cap")
            self.cache[current] = successor(self.mirror, self.base, self.M, self.W, current)
        self.calls += 1
        self.check_time()
        return self.cache[current]


def returns(engine, start, current, fuel):
    """Literal positive-length recursion as a loop, raising Cutoff if unfinished."""
    require(type(fuel) is int and fuel >= 0, "fuel must be a natural integer")
    start, current = key(start), key(current)
    initial_calls, edges = engine.calls, []
    while fuel:
        answer = engine.step(current)
        if answer is None:
            return {"returns": False, "reason": "dead successor",
                    "attempts": engine.calls-initial_calls, "accepted_edges": len(edges)}
        current, edge = answer
        edges.append(edge)
        if current == start:
            return {"returns": True, "reason": "positive return", "edges": edges,
                    "attempts": engine.calls-initial_calls, "accepted_edges": len(edges)}
        fuel -= 1
    return {"returns": False, "reason": "fuel exhausted",
            "attempts": engine.calls-initial_calls, "accepted_edges": len(edges)}


def bounded_return(mirror, base, M, W, start, current, fuel, **limits):
    engine = Engine(mirror, base, M, W, **limits)
    try:
        result = returns(engine, start, current, fuel)
        return {"status": "COMPLETE", **result, "evaluated_states": len(engine.cache)}
    except (Cutoff, MemoryError) as error:
        return {"status": "UNDECIDED", "reason": str(error) or "memory allocation",
                "attempts": engine.calls, "evaluated_states": len(engine.cache)}


def functional_search(mirror, base, M, W, **limits):
    """Existential scan in Lean carrier order; a positive return stops the scan."""
    engine = Engine(mirror, base, M, W, **limits)
    q, exponent = 2*base-1, M+W-1
    descriptor = {"base": base, "M": M, "W": W,
                  "state_bound_formula": f"({q}+1)*{q}^{exponent}"}
    # q>=3: this implies N>max_states without constructing a huge integer.
    if exponent >= engine.max_states.bit_length():
        return {**descriptor, "status": "UNDECIDED", "reason": "state cap"}
    total = state_count(base, M, W)
    descriptor["states"] = total
    if total > engine.max_states:
        return {**descriptor, "status": "UNDECIDED", "reason": "state cap"}
    checked = 0
    try:
        for start in states(base, M, W):
            answer = returns(engine, start, start, total)
            checked += 1
            if answer["returns"]:
                edges = answer["edges"]
                require(mirror.cycleOK(base, edges, list(start[0]), list(start[1])),
                        "positive functional search did not reconstruct a certificate")
                engine.check_time()
                return {**descriptor, "status": "COMPLETE", "exists": True,
                        "carrier_exhausted": False, "starts_checked": checked,
                        "attempts": engine.calls, "evaluated_states": len(engine.cache), "edges": edges}
        require(checked == total, "functional search did not enumerate the full carrier")
        engine.check_time()
        return {**descriptor, "status": "COMPLETE", "exists": False,
                "carrier_exhausted": True, "starts_checked": checked,
                "attempts": engine.calls, "evaluated_states": len(engine.cache)}
    except (Cutoff, MemoryError) as error:
        return {**descriptor, "status": "UNDECIDED", "reason": str(error) or "memory allocation",
                "starts_checked": checked, "attempts": engine.calls,
                "evaluated_states": len(engine.cache)}


def guard_controls(mirror):
    s, t = ((1,), (10,)), ((3,), (0,))
    tests = [
        lambda: successor(mirror, 1, 1, 2, s),
        lambda: successor(mirror, 2, -1, 2, s),
        lambda: successor(mirror, 2, True, 2, s),
        lambda: successor(mirror, 2, 1, 1, s),
        lambda: successor(mirror, 2, 1, 2.0, s),
        lambda: successor(mirror, 2, 1, 2, None),
        lambda: successor(mirror, 2, 1, 2, ((1,), 0)),
        lambda: successor(mirror, 2, 1, 2, ((-1,), (0,))),
        lambda: successor(mirror, 2, 1, 2, ((True,), (0,))),
        lambda: successor(mirror, 2, 1, 2, ((1.0,), (0,))),
        lambda: bounded_return(mirror, 10, 1, 2, s, s, -1),
        lambda: bounded_return(mirror, 10, 1, 2, s, s, True),
        lambda: bounded_return(mirror, 10, 1, 2, s, s, 1.0),
        lambda: bounded_return(mirror, 10, 1, 2, s, s, 2, max_states=0),
        lambda: bounded_return(mirror, 10, 1, 2, s, s, 2, max_states=True),
        lambda: bounded_return(mirror, 10, 1, 2, s, s, 2, max_steps=0),
        lambda: bounded_return(mirror, 10, 1, 2, s, s, 2, seconds=-1),
        lambda: bounded_return(mirror, 10, 1, 2, s, s, 2, seconds=float("nan")),
        lambda: bounded_return(mirror, 10, 1, 2, s, s, 2, seconds=float("inf")),
        lambda: functional_search(mirror, 2, 1, 2, seconds=1501),
    ]
    for test in tests:
        try:
            test()
        except RuntimeError:
            continue
        raise RuntimeError("malformed input was accepted")
    outside = [((), (0,)), ((1,), ()), ((19,), (0,)), ((1,), (0, 0, 0))]
    for value in outside:
        require(not state_ok(10, 1, 2, value) and successor(mirror, 10, 1, 2, value) is None,
                "cheap carrier predicate accepted an out-of-carrier state")
    require(mirror.hyp(10, list(s[0]), list(s[1])) and
            not mirror.hyp(10, list(t[0]), list(t[1])), "target-Hyp countercontrol changed")
    answer = successor(mirror, 10, 1, 2, s)
    require(answer is not None and answer[0] == t, "valid edge to Hyp-false target was lost")
    require(successor(mirror, 10, 1, 2, t) is None, "Hyp-false target did not stop next step")
    controls = [
        (s, s, 0, False, 0, 0, "fuel exhausted"),
        (t, t, 1, False, 1, 0, "dead successor"),
        (s, s, 1, False, 1, 1, "fuel exhausted"),
        (s, s, 2, False, 2, 1, "dead successor"),
        (t, s, 1, True, 1, 1, "positive return"),
    ]
    for start, current, fuel, verdict, attempts, edges, reason in controls:
        result = bounded_return(mirror, 10, 1, 2, start, current, fuel)
        require(result["status"] == "COMPLETE" and result["returns"] is verdict and
                result["attempts"] == attempts and result["accepted_edges"] == edges and
                result["reason"] == reason, "positive-length or early-dead control failed")
    cutoffs = []
    for limits in ({"max_states": 1}, {"max_steps": 1}, {"seconds": 1e-12}):
        cutoffs.append(bounded_return(mirror, 10, 1, 2, s, s, 2, **limits))
        cutoffs.append(functional_search(mirror, 2, 2, 4, **limits))
    for result in cutoffs:
        require(result["status"] == "UNDECIDED" and "returns" not in result and
                "exists" not in result and "edges" not in result, "cutoff acquired a Boolean verdict")
    return {"malformed_inputs_rejected": len(tests), "outside_carrier_controls": len(outside),
            "return_semantics_controls": len(controls), "cutoffs_undecided": len(cutoffs),
            "target_hyp_false_control": 1}


def fixture_controls(joint, dependencies):
    mirror, _, balanced, _ = dependencies
    fixtures = sorted(mirror._lean_certs())
    require(len(fixtures) == 8 and {base for base, _ in fixtures} == BASES, "known fixture set changed")
    totals = Counter()
    for base, original in fixtures:
        M = max(len(e[j]) for e in original for j in (0, 2))
        W = max(2, max(len(e[j]) for e in original for j in (1, 3)))
        local = Counter()
        for m, w in product((M, M+1), (W, W+1)):
            normalized, period = joint.normalize_fixture(dependencies, base, original, m, w)
            require(period == len(normalized), "baseline fixture unexpectedly has a smaller period")
            total = state_count(base, m, w)
            for rotation in range(period):
                rotated = normalized[rotation:]+normalized[:rotation]
                start = key(rotated[0][:2])
                result = bounded_return(mirror, base, m, w, start, start, total,
                                        max_states=period, max_steps=period)
                require(result["status"] == "COMPLETE" and result["returns"] and
                        result["edges"] == rotated and result["accepted_edges"] == period,
                        "known normalized orbit did not return within the exact finite-state bound")
                require(mirror.cycleOK(base, result["edges"], *rotated[0][:2]), "returned fixture failed replay")
                for edge in result["edges"]:
                    balanced.integer_edge(base, edge)
                local["fixture_returns"] += 1
                local["fixture_return_edges"] += period
            start = key(normalized[0][:2])
            for fuel in (period-1, 2*period):
                result = bounded_return(mirror, base, m, w, start, start, fuel,
                                        max_states=period, max_steps=period)
                require(result["status"] == "COMPLETE" and result["returns"] == (fuel >= period),
                        "short/double-fuel fixture verdict is wrong")
                if fuel < period:
                    require(result["accepted_edges"] == fuel, "short fuel stopped prematurely")
                    local["short_fuel_false"] += 1
                else:
                    require(result["accepted_edges"] == period, "search did not stop at first positive return")
                    local["double_fuel_returns"] += 1
        totals.update(local)
        print("KNOWN_ORBITS " + json.dumps({"base": base, "minimal_caps": [M, W],
              "period": len(original), "scope": "orbit controls; carriers not exhausted", **local},
              sort_keys=True), flush=True)
    return totals


def graph_controls(joint, dependencies):
    mirror = dependencies[0]
    totals = Counter()
    for base, M, W in SCOPES:
        reference = joint.complete_graph(dependencies, base, M, W)
        require(reference["summary"]["status"] == "COMPLETE", "reference graph is UNDECIDED")
        total = state_count(base, M, W)
        require(total == reference["summary"]["states"], "carrier cardinality disagrees")
        cycle_states = {key(edge[:2]) for cycle in reference["cycles"] for edge in cycle}
        engine = Engine(mirror, base, M, W)
        accepted = hyp_false_targets = enumerated = 0
        for source in states(base, M, W):
            actual = engine.step(source)
            expected = joint.successor(mirror, base, M, W, source)
            require(actual == expected, "literal and graph successors disagree")
            enumerated += 1
            if actual is not None:
                accepted += 1
                hyp_false_targets += not mirror.hyp(base, *actual[1][2:4])
        require(enumerated == len(engine.cache) == total, "successor comparison missed a state")
        positives = attempts = maximum = 0
        for start in states(base, M, W):
            answer = returns(engine, start, start, total)
            require(answer["returns"] == (start in cycle_states), "N-fuel return disagrees with graph cycles")
            positives += answer["returns"]
            attempts += answer["attempts"]
            maximum = max(maximum, answer["attempts"])
            if answer["returns"]:
                require(mirror.cycleOK(base, answer["edges"], list(start[0]), list(start[1])),
                        "complete-graph positive return fails exact replay")
        search = functional_search(mirror, base, M, W)
        require(search["status"] == "COMPLETE" and search["exists"] == bool(reference["cycles"]),
                "existential functional search disagrees with the complete graph")
        require(accepted == reference["summary"]["edges"] and positives == len(cycle_states),
                "complete graph counts disagree")
        summary = {"base": base, "M": M, "W": W, "states": total, "edges": accepted,
                   "hyp_false_targets_retained": hyp_false_targets, "positive_starts": positives,
                   "return_attempts": attempts, "max_return_attempts": maximum,
                   "functional_exists": search["exists"], "search_starts": search["starts_checked"],
                   "search_attempts": search["attempts"], "status": "COMPLETE"}
        for name in ("states", "edges", "hyp_false_targets_retained", "positive_starts", "return_attempts"):
            totals[name] += summary[name]
        totals["max_return_attempts"] = max(totals["max_return_attempts"], maximum)
        totals["reference_cycles"] += len(reference["cycles"])
        totals["functional_positive_graphs"] += search["exists"]
        print("GRAPH_COMPARISON " + json.dumps(summary, sort_keys=True), flush=True)
    return totals


def selftest(joint, dependencies):
    guards = guard_controls(dependencies[0])
    fixtures = fixture_controls(joint, dependencies)
    graphs = graph_controls(joint, dependencies)
    print("FUNCTIONAL_SEARCH_PASS " + json.dumps({"status": "COMPUTED", "known_bases": 8,
          "complete_graphs": len(SCOPES), "optimized_python": not __debug__,
          **guards, **fixtures, **graphs}, sort_keys=True), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode")
    sub.add_parser("selftest")
    graph = sub.add_parser("graph")
    graph.add_argument("base", type=int)
    graph.add_argument("M", type=int)
    graph.add_argument("W", type=int)
    graph.add_argument("--max-states", type=int, default=20000)
    graph.add_argument("--max-steps", type=int, default=2000000)
    graph.add_argument("--seconds", type=float, default=30)
    graph.add_argument("--witness", action="store_true")
    args = parser.parse_args()
    joint, dependencies = load_dependencies()
    if args.mode in (None, "selftest"):
        selftest(joint, dependencies)
        return 0
    result = functional_search(dependencies[0], args.base, args.M, args.W,
                               max_states=args.max_states, max_steps=args.max_steps, seconds=args.seconds)
    edges = result.pop("edges", None)
    print("FUNCTIONAL_SEARCH " + json.dumps(result, sort_keys=True), flush=True)
    if edges and (args.witness or args.base == 10):
        print(("DECIMAL_CANDIDATE " if args.base == 10 else "WITNESS ")+json.dumps(edges), flush=True)
    return 2 if result["status"] == "UNDECIDED" else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, ValueError, Cutoff) as error:
        print("CHECK FAILED: " + str(error), file=sys.stderr)
        sys.exit(1)
