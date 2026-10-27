#!/usr/bin/env python3
"""Independent validator for Agent117 generic center-strip lasso witnesses.

This imports no C++/mirror/solver code.  It derives each spatial edge from
ordinary normalization carries and the coefficient identity after trimming.
A verified lasso is an infinite GENERIC strip; midpoint closure is absent,
so it certifies neither a finite center nor any Lychrel number.  Exploration
counts and EXHAUSTED claims cannot be independently verified by a lasso.

Usage: python3 common_padding_verify.py --selftest
       python3 common_padding_verify.py witness.json [more.json ...]
Exit 0: all supplied witnesses replayed.  Exit 1: invalid witness.
Exit 2: at least one supplied record contains no lasso to verify.
"""
from __future__ import annotations

import argparse
from collections import deque
import copy
import json
from pathlib import Path
import re
import signal
import sys
import time


FORMAT = "agent117-common-padding-strip-v1"


class InvalidWitness(ValueError):
    pass


class MissingWitness(ValueError):
    pass


class ReferenceCapReached(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidWitness(message)


def integer(value):
    return type(value) is int


def bits(values, length=None):
    return (type(values) is list and bool(values)
            and (length is None or len(values) == length)
            and all(integer(x) and x in (0, 1) for x in values))


def initial_state(base, e, g):
    return {"l": list(e), "r": [1 - x for x in e],
            "Rd": [(base - 1) * x if flag else -1 for x, flag in zip(e, g)],
            "Z": [-1] * len(e)}


def check_state(state, base, g, v, initial=False):
    period = len(g)
    require(type(state) is dict and set(state) == {"l", "r", "Rd", "Z"},
            "state requires exactly l,r,Rd,Z")
    for name in state:
        require(type(state[name]) is list and len(state[name]) == period
                and all(integer(x) for x in state[name]), "invalid state vector " + name)
    require(all(x in (0, 1) for x in state["l"] + state["r"]), "nonbinary carry")
    for t in range(period):
        rd, z = state["Rd"][t], state["Z"][t]
        require((0 <= rd < base) if g[t] else rd == -1, "invalid/inactive Rd")
        require(z == -1 if initial or not v[t] else 0 <= z <= 2 * base - 2,
                "invalid/inactive Z")


def verify_edge(source, target, columns, base, e, g, v, first):
    """At depth j, columns[t] is C_t[j], before any midpoint is reached.

    source.l is the carry entering the left coefficient; source.r is the
    carry leaving its mirrored right coefficient.  target.r is the inward
    carry entering that right coefficient.  Their two base-b divisions fix
    target.l and both emitted digits independently of the solver's search.
    """
    period = len(e)
    require(type(columns) is list and len(columns) == period
            and all(integer(c) and 0 <= c <= 2 * base - 2 for c in columns),
            "invalid coefficient column")
    check_state(source, base, g, v, initial=first)
    check_state(target, base, g, v)
    for t, c in enumerate(columns):
        left_out, left_digit = divmod(c + source["l"][t], base)
        right_out, right_digit = divmod(c + target["r"][t], base)
        require(left_out == target["l"][t], f"phase{t}: forward carry")
        require(right_out == source["r"][t], f"phase{t}: reverse carry")
        if g[t]:
            # An overflow shifts the reflected partner outward by one column.
            partner = (base - 1) * e[t] if first else source["Rd"][t]
            require(target["Rd"][t] == right_digit, f"phase{t}: stored right digit")
        else:
            partner = right_digit
        raw = left_digit + partner
        nxt = (t + 1) % period
        if v[t]:
            # raw[j] = h for j=0, and C_(t+1)[j-1] for j>0.
            wanted = base - 1 if first else source["Z"][t]
            require(raw == wanted, f"phase{t}: trimmed coefficient equation")
            require(target["Z"][t] == columns[nxt], f"phase{t}: next-phase coefficient memory")
        else:
            require(raw == columns[nxt], f"phase{t}: same-depth temporal equation")


def check_walk(walk, base, e, g, v, boundary):
    require(type(walk) is dict and set(walk) == {"states", "columns"}, "invalid walk shape")
    states, columns = walk["states"], walk["columns"]
    require(type(states) is list and type(columns) is list and bool(columns)
            and len(states) == len(columns) + 1, "walk state/edge lengths disagree")
    for j, column in enumerate(columns):
        verify_edge(states[j], states[j + 1], column, base, e, g, v,
                    first=boundary and j == 0)


def verify_record(record):
    require(type(record) is dict and record.get("format") == FORMAT, "unknown witness format")
    if record.get("status") != "SPATIAL_CYCLE":
        raise MissingWitness("status=" + str(record.get("status"))
                             + "; no generic lasso supplied; no negative verified")
    require(record.get("decision") == "INFINITE_GENERIC_STRIP_WITNESS", "mislabelled decision")
    base = record.get("base")
    require(integer(base) and base >= 2, "invalid base")
    e, g, v = record.get("e"), record.get("g"), record.get("v")
    require(bits(e), "invalid carry stream")
    require(bits(g, len(e)) and bits(v, len(e)), "invalid overflow/trim stream")
    require(sum(g) > 0 and sum(g) == 2 * sum(v), "unbalanced fixed length schedule")
    require(type(record.get("gauge_filtered")) is bool, "missing gauge policy")
    require(record.get("initial_complete") is True, "incomplete initial frontier")
    witness = record.get("witness")
    require(type(witness) is dict and set(witness) == {"prefix", "cycle"}, "missing lasso")
    prefix, cycle = witness["prefix"], witness["cycle"]
    check_walk(prefix, base, e, g, v, boundary=True)
    check_walk(cycle, base, e, g, v, boundary=False)
    require(prefix["states"][0] == initial_state(base, e, g), "wrong outer boundary state")
    require(prefix["states"][-1] == cycle["states"][0], "prefix does not meet cycle")
    require(cycle["states"][0] == cycle["states"][-1], "spatial cycle does not close")
    all_neutral = all(c == base - 1 for c in prefix["columns"][0])
    ghost = (prefix["states"][1]["l"] == e
             and prefix["states"][1]["r"] == [1 - x for x in e])
    require(all_neutral == ghost, "initial ghost/noncollision criterion disagrees")
    if record["gauge_filtered"]:
        require(not all_neutral, "filtered witness begins with removed common padding")
    # Counts are metadata, not proof.  Check only their internal consistency.
    before, removed, after = (record.get("initial_" + key) for key in ("before", "removed", "after"))
    require(all(integer(x) and x >= 0 for x in (before, removed, after))
            and before - removed == after, "inconsistent frontier metadata")
    require(record.get("initial_ghosts") == 1 and removed == int(record["gauge_filtered"]),
            "inconsistent ghost metadata")
    return {"status": "VERIFIED_GENERIC_STRIP", "period": len(e),
            "gauge_filtered": record["gauge_filtered"],
            "prefix_edges": len(prefix["columns"]), "cycle_edges": len(cycle["columns"]),
            "finite_center_verified": False, "exhaustion_counts_verified": False}


def ghost_control():
    e, g, v = [0, 1], [1, 1], [1, 0]
    start = initial_state(10, e, g)
    ghost = copy.deepcopy(start)
    ghost["Z"][0] = 9
    return {"format": FORMAT, "base": 10, "e": e, "g": g, "v": v,
            "status": "SPATIAL_CYCLE", "decision": "INFINITE_GENERIC_STRIP_WITNESS",
            "gauge_filtered": False, "initial_complete": True,
            "initial_before": 1, "initial_ghosts": 1, "initial_removed": 0, "initial_after": 1,
            "witness": {"prefix": {"states": [start, ghost], "columns": [[9, 9]]},
                        "cycle": {"states": [copy.deepcopy(ghost), copy.deepcopy(ghost)],
                                  "columns": [[9, 9]]}}}


def selftest():
    verify_record(ghost_control())
    rejected = 0
    changes = [
        lambda r: r["witness"]["prefix"]["columns"][0].__setitem__(0, 8),
        lambda r: r["witness"]["prefix"]["states"][0]["l"].__setitem__(0, 1),
        lambda r: r["witness"]["cycle"]["states"][1]["r"].__setitem__(0, 0),
        lambda r: r["witness"]["cycle"]["states"][1]["Rd"].__setitem__(1, 8),
        lambda r: r["witness"]["cycle"]["states"][1]["Z"].__setitem__(0, 8),
        lambda r: r.__setitem__("gauge_filtered", True),
        lambda r: r["g"].__setitem__(1, 0),
        lambda r: r["witness"]["cycle"].__setitem__("columns", []),
        lambda r: r.__setitem__("decision", "FINITE_CENTER"),
    ]
    for change in changes:
        record = copy.deepcopy(ghost_control())
        change(record)
        try:
            verify_record(record)
        except InvalidWitness:
            rejected += 1
        else:
            raise AssertionError("mutated witness accepted")
    cases = 0
    for base in range(2, 41):
        for e in (0, 1):
            for c in range(2 * base - 1):
                unchanged = ((c + e) // base == e and (c + 1 - e) // base == 1 - e)
                if unchanged != (c == base - 1):
                    raise AssertionError("ghost key collision")
                cases += 1
    print(json.dumps({"selftest": "PASS", "positive_lassos": 1,
                      "rejected_mutations": rejected, "ghost_scalar_cases": cases}))


def state_key(state):
    return tuple(tuple(state[name]) for name in ("l", "r", "Rd", "Z"))


def from_key(key):
    return dict(zip(("l", "r", "Rd", "Z"), map(list, key)))


def independent_successors(source, e, g, v, first, deadline, base=10, cap=300000):
    """Fresh temporal coefficient enumeration, independent of segment code."""
    period = len(e)
    columns = [0] * period
    new_left, new_right, new_digits = [0] * period, [0] * period, [-1] * period
    outputs = {}

    def emit():
        if time.monotonic() > deadline:
            raise TimeoutError("independent successor wall cap")
        new_z = [columns[(t + 1) % period] if v[t] else -1 for t in range(period)]
        key = tuple(map(tuple, (new_left, new_right, new_digits, new_z)))
        if key not in outputs:
            if len(outputs) >= cap:
                raise ReferenceCapReached("per-successor state cap reached before materialization")
            outputs[key] = tuple(columns)

    def visit(t, c, c0):
        if time.monotonic() > deadline:
            raise TimeoutError("independent successor wall cap")
        columns[t] = c
        carry, digit = divmod(c + source["l"][t], base)
        new_left[t] = carry
        for inward in (0, 1):
            right_out, right_digit = divmod(c + inward, base)
            if right_out != source["r"][t]:
                continue
            new_right[t] = inward
            new_digits[t] = right_digit if g[t] else -1
            partner = ((base - 1) * e[t] if first else source["Rd"][t]) if g[t] else right_digit
            raw = digit + partner
            if v[t]:
                wanted = base - 1 if first else source["Z"][t]
                if raw != wanted:
                    continue
                if t == period - 1:
                    emit()
                else:
                    for nxt in range(2 * base - 1):
                        visit(t + 1, nxt, c0)
            elif 0 <= raw <= 2 * base - 2:
                if t == period - 1:
                    if raw == c0:
                        emit()
                else:
                    visit(t + 1, raw, c0)

    for initial in range(2 * base - 1):
        visit(0, initial, initial)
    for key, cols in outputs.items():
        if time.monotonic() > deadline:
            raise TimeoutError("independent replay wall cap")
        verify_edge(source, from_key(key), list(cols), base, e, g, v, first)
    return outputs


def reference_graph(E, G, V, cap=300000, seconds=60, base=10, filtered=True):
    """Independent small exact graph audit; any resource stop is UNDECIDED."""
    require(E and len(E) <= 32 and len(E) == len(G) == len(V) and not set(E + G + V) - {"0", "1"},
            "reference graph requires equal nonempty binary streams")
    require(integer(base) and 2 <= base <= 62 and integer(cap) and 1 <= cap <= 300000
            and integer(seconds) and 1 <= seconds <= 60, "reference budgets out of bounds")
    e, g, v = list(map(int, E)), list(map(int, G)), list(map(int, V))
    require(sum(g) > 0 and sum(g) == 2 * sum(v), "reference length imbalance")
    started = time.monotonic()
    deadline = started + seconds
    initial = initial_state(base, e, g)
    old_handler = None
    if hasattr(signal, "SIGALRM"):
        def alarm_handler(_signum, _frame):
            raise TimeoutError("independent graph hard wall cap")
        old_handler = signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(seconds)
    try:
        first = independent_successors(initial, e, g, v, True, deadline, base, cap)
        nonghosts = {key for key, column in first.items() if any(c != base - 1 for c in column)}
        require(len(first) - len(nonghosts) == 1, "reference initial ghost count")
        seeds = nonghosts if filtered else set(first)
        if len(seeds) > cap:
            return {"reference": "UNDECIDED", "reason": "initial state cap", "states": len(seeds)}
        graph = {}
        reached = set(seeds)
        queue = deque(sorted(seeds))
        while queue:
            if time.monotonic() > deadline:
                raise TimeoutError("independent graph wall cap")
            key = queue.popleft()
            outputs = independent_successors(from_key(key), e, g, v, False, deadline, base, cap)
            graph[key] = tuple(outputs)
            for target in outputs:
                if target not in reached:
                    if len(reached) >= cap:
                        return {"reference": "UNDECIDED", "reason": "state cap", "states": len(reached)}
                    reached.add(target)
                    queue.append(target)
        indegree = dict.fromkeys(reached, 0)
        for targets in graph.values():
            if time.monotonic() > deadline:
                raise TimeoutError("independent graph audit wall cap")
            for target in targets:
                indegree[target] += 1
        ready = deque(key for key, deg in indegree.items() if deg == 0)
        distance = {key: int(key in seeds) for key in reached}
        removed = 0
        while ready:
            if time.monotonic() > deadline:
                raise TimeoutError("independent graph peel wall cap")
            key = ready.popleft()
            removed += 1
            for target in graph[key]:
                distance[target] = max(distance[target], distance[key] + 1)
                indegree[target] -= 1
                if indegree[target] == 0:
                    ready.append(target)
        layers = [1, len(seeds)]
        if removed == len(reached):
            frontier = set(seeds)
            while frontier:
                if time.monotonic() > deadline:
                    raise TimeoutError("independent frontier audit wall cap")
                frontier = {target for key in frontier for target in graph[key]}
                layers.append(len(frontier))
        return {"reference": "GENERIC_DAG" if removed == len(reached) else "GENERIC_CYCLE_PRESENT",
                "base": base, "period": len(e), "gauge_filtered": filtered,
                "initial_before": len(first), "initial_removed": int(filtered),
                "initial_after": len(seeds), "states": len(reached),
                "generic_arcs": sum(map(len, graph.values())),
                "transitions_including_unfiltered_initial": len(first) + sum(map(len, graph.values())),
                "peeled": removed, "max_generic_columns": max(distance.values(), default=0) if removed == len(reached) else None,
                "frontiers": layers, "elapsed_seconds": round(time.monotonic() - started, 6),
                "finite_center_verified": False}
    except TimeoutError as error:
        return {"reference": "UNDECIDED", "reason": str(error),
                "elapsed_seconds": round(time.monotonic() - started, 6)}
    except ReferenceCapReached as error:
        return {"reference": "UNDECIDED", "reason": str(error),
                "elapsed_seconds": round(time.monotonic() - started, 6)}
    finally:
        if old_handler is not None:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)


def integer_norm(base, word, incoming):
    value, power = incoming, 1
    for coefficient in word:
        value += coefficient * power
        power *= base
    digits = []
    for _ in word:
        value, digit = divmod(value, base)
        digits.append(digit)
    return digits, value


def center_raw(base, center, e, g):
    digits, out = integer_norm(base, center, e)
    require(out == 1 - e, "positive control carry flip")
    if g:
        digits.append((base - 1) * e)
    return [a + b for a, b in zip(digits, reversed(digits))]


def padding_depth(base, word):
    depth = 0
    while 2 * depth + 1 < len(word) and word[depth] == word[-depth - 1] == base - 1:
        depth += 1
    return depth


def read_positive_sources(root):
    def numbers(text):
        return [int(x) for x in re.findall(r"\d+", text)]
    results = []
    for relative in ("lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean",
                     "lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean"):
        source = (root / relative).read_text()
        constants = {name: numbers(body) for name, body in
                     re.findall(r"def\s+(\w+)\s*:\s*List Nat\s*:=\s*\[([^\]]*)\]", source)}
        for base, body in re.findall(r"def cert(\d+)\s*:\s*List Edge\s*:=\s*(.*?)\n\n", source, re.S):
            edges = []
            for entry in re.findall(r"⟨(.*?)⟩", body):
                fields = re.findall(r"\[[^\]]*\]|\w+", entry)
                require(len(fields) == 6, "unexpected positive source syntax")
                lists = [numbers(field) if field.startswith("[") else constants[field]
                         for field in fields[:4]]
                edges.append((*lists, int(fields[4]), int(fields[5])))
            results.append((int(base), edges))
    require(sorted(base for base, _ in results) == [2, 4, 8, 11, 16, 17, 26, 32],
            "positive source coverage incomplete")
    return sorted(results)


def known_controls():
    """Read actual Lean fixture data; all arithmetic remains independent."""
    root = Path(__file__).resolve().parents[2]
    fixtures = read_positive_sources(root)
    summaries = []
    edge_checks = first_layers = 0
    for base, edges in fixtures:
        centers = [edge[1] for edge in edges]
        common = min(padding_depth(base, center) for center in centers)
        reduced = [center[common:len(center) - common] for center in centers]
        require(all(reduced) and any(center[0] != base - 1 for center in reduced),
                "positive control was entirely removed by gauge")
        es = [integer_norm(base, edge[0], 0)[1] for edge in edges]
        gs = [integer_norm(base, edge[0][::-1], 1 - e)[1] for edge, e in zip(edges, es)]
        vs = [edge[5] for edge in edges]
        require(bits(es) and bits(gs, len(edges)) and bits(vs, len(edges)), "nonbinary fixture streams")
        for extra in (0, 1, 3):
            stripped = common + extra
            for t, (B, C, B2, C2, u, v) in enumerate(edges):
                require(C2 == centers[(t + 1) % len(edges)], "positive center chain mismatch")
                padded = [base - 1] * extra + C + [base - 1] * extra
                target = [base - 1] * extra + C2 + [base - 1] * extra
                require(center_raw(base, padded, es[t], gs[t]) == [base - 1] * v + target + [base - 1] * v,
                        "fixed-v padded positive edge")
                core = padded[stripped:len(padded) - stripped]
                require(core == reduced[t], "common strip mismatch")
                raw = center_raw(base, core, es[t], gs[t])
                require(raw == [base - 1] * v + reduced[(t + 1) % len(edges)] + [base - 1] * v,
                        "fixed-v reduced positive edge")
                require(center_raw(base, padded, es[t], gs[t]) == [base - 1] * stripped + raw + [base - 1] * stripped,
                        "common padding covariance")
                edge_checks += 1
        if min(map(len, reduced)) >= 3:
            columns = [center[0] for center in reduced]
            state = initial_state(base, es, gs)
            target = {"l": [], "r": [], "Rd": [], "Z": []}
            for t, center in enumerate(reduced):
                right = integer_norm(base, center[:-1], es[t])[1]
                target["l"].append((columns[t] + es[t]) // base)
                target["r"].append(right)
                target["Rd"].append((columns[t] + right) % base if gs[t] else -1)
                target["Z"].append(columns[(t + 1) % len(edges)] if vs[t] else -1)
            verify_edge(state, target, columns, base, es, gs, vs, first=True)
            require(any(c != base - 1 for c in columns), "positive first column removed")
            first_layers += 1
        summaries.append({"base": base, "edges": len(edges), "common_depth": common,
                          "min_reduced_length": min(map(len, reduced))})
    print(json.dumps({"known_source_controls": "PASS", "fixtures": summaries,
                      "original_edges": sum(len(edges) for _, edges in fixtures),
                      "padded_and_reduced_edge_checks": edge_checks,
                      "preserved_first_generic_layers": first_layers,
                      "new_lean_verification": False}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--known-controls", action="store_true")
    parser.add_argument("--reference", nargs=3, metavar=("E", "G", "V"))
    parser.add_argument("--reference-cap", type=int, default=300000)
    parser.add_argument("--reference-seconds", type=int, default=60)
    parser.add_argument("--reference-unfiltered", action="store_true")
    parser.add_argument("--base", type=int, default=10)
    args = parser.parse_args()
    if args.selftest:
        selftest()
    if args.known_controls:
        known_controls()
    if args.reference:
        result = reference_graph(*args.reference, cap=args.reference_cap,
                                 seconds=args.reference_seconds, base=args.base,
                                 filtered=not args.reference_unfiltered)
        print(json.dumps(result))
        if result["reference"] == "UNDECIDED":
            return 2
    if not args.files:
        if not args.selftest and not args.reference and not args.known_controls:
            parser.error("provide witness JSON files, --selftest, or --reference E G V")
        return 0
    exitcode = 0
    for filename in args.files:
        try:
            record = json.loads(Path(filename).read_text())
            result = verify_record(record)
            print(json.dumps({"file": filename, **result}))
        except MissingWitness as error:
            print(json.dumps({"file": filename, "status": "NO_WITNESS_VERIFIED", "detail": str(error)}))
            exitcode = max(exitcode, 2)
        except (InvalidWitness, OSError, ValueError, TypeError, KeyError) as error:
            print(json.dumps({"file": filename, "status": "INVALID", "detail": str(error)}))
            return 1
    return exitcode


if __name__ == "__main__":
    sys.exit(main())
