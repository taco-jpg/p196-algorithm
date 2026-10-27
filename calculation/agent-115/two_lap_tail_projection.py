#!/usr/bin/env python3
"""Independent necessary last-coefficient projection for constant-width B cycles.

PAPER NECESSITY ARGUMENT. Let x be the last coefficient, a the forward
carry entering it, e the outgoing forward carry, and g the overflow. Then
e=floor((x+a)/b), a in {0,1}. For g=0, the successor's last coefficient is
  y=(x+a)%b + (x+1-e)%b.
For g=1 and u=g, the trimmed last raw coefficient must be b-1, so
  (b-1)(1-e)+(x+1-e)%b=b-1.
The bound 0<=x<=2b-2 forces x=b-1, hence a=e. At width at least two,
  y=(b-1)(1-e)+d, 0<=d<=b-1.
At width one, a=0 forces e=0 and y=b; this belongs to that broad interval.
Thus the same overapproximation is necessary at every positive width.

An actual P-cycle gives a P-step closed walk in the phase-times-tail graph.
Sink peeling cannot remove that walk. Requiring an exactly P-step return
gives another necessary domain; it never imposes a P/2-step return.

The neutral tail x=b-1 always permits y=b-1, for every e/g and next e.
Consequently this projection alone cannot disprove a stream pair. This is
a necessary-domain helper, not an exact exterior-cycle decision procedure.
"""

import argparse
from collections import deque
import itertools
import json
import resource
import sys
import time

import two_lap_oracle as oracle


def require(condition, message):
    if not condition:
        raise ValueError(message)


def eligible_tail(base, e, x):
    return any((x + incoming) // base == e for incoming in (0, 1))


def local_targets(base, e, g, x):
    """A width-independent necessary relation, before the next e is imposed."""
    require(base >= 2 and e in (0, 1) and g in (0, 1), "invalid base or stream bit")
    require(0 <= x <= 2 * base - 2, "tail coefficient outside its range")
    targets = set()
    for incoming in (0, 1):
        if (x + incoming) // base != e:
            continue
        if g == 0:
            targets.add((x + incoming) % base + (x + 1 - e) % base)
        elif x == base - 1:
            targets.update((base - 1) * (1 - e) + digit for digit in range(base))
    return tuple(sorted(targets))


def phase_graph(base, es, gs):
    es, gs = tuple(map(int, es)), tuple(map(int, gs))
    require(len(es) > 0 and len(es) == len(gs), "empty or mismatched streams")
    require(all(bit in (0, 1) for bit in es + gs), "stream contains a non-bit")
    span, period = 2 * base - 1, len(es)
    rows = []
    for t in range(period):
        next_t = (t + 1) % period
        for x in range(span):
            rows.append(tuple(next_t * span + y for y in local_targets(base, es[t], gs[t], x)
                              if eligible_tail(base, es[next_t], y)))
    return rows


def sink_domains(base, es, gs):
    """Keep vertices with an infinite projected future; a necessary domain."""
    rows = phase_graph(base, es, gs)
    reverse = [[] for _ in rows]
    for source, targets in enumerate(rows):
        for target in targets:
            reverse[target].append(source)
    degree = [len(targets) for targets in rows]
    queue = deque(vertex for vertex, count in enumerate(degree) if count == 0)
    alive = [True] * len(rows)
    while queue:
        target = queue.popleft()
        if not alive[target]:
            continue
        alive[target] = False
        for source in reverse[target]:
            degree[source] -= 1
            if degree[source] == 0:
                queue.append(source)
    span = 2 * base - 1
    return tuple(tuple(x for x in range(span) if alive[t * span + x])
                 for t in range(len(es)))


def full_return_domains(base, es, gs):
    """Keep exactly those projected vertices admitting a len(es)-step return."""
    rows = phase_graph(base, es, gs)
    span, period = 2 * base - 1, len(es)
    output = []
    for t in range(period):
        keep = []
        for x in range(span):
            start = t * span + x
            reachable = {start}
            for _ in range(period):
                reachable = {target for source in reachable for target in rows[source]}
                if not reachable:
                    break
            if start in reachable:
                keep.append(x)
        output.append(tuple(keep))
    return tuple(output)


def exhaustive_edge_checks():
    """Every positive-headed word, bases 2..5 and widths 1..4, is tested."""
    records = []
    for base in range(2, 6):
        for width in range(1, 5):
            starts = valid = 0
            for B in itertools.product(range(2 * base - 1), repeat=width):
                if B[0] == 0:
                    continue
                starts += 1
                step = oracle.exterior_step(base, B)
                if step is None:
                    continue
                B2, e, g = step
                next_e = oracle.integer_norm(base, B2, 0)[1]
                x, y = B[-1], B2[-1]
                require(y in local_targets(base, e, g, x), "exact edge excluded by local tail relation")
                require(eligible_tail(base, next_e, y), "exact edge excluded by next-phase carry")
                if g:
                    require(x == base - 1, "exact overflow edge has nonneutral tail")
                C = (0,) if e else (2 * base - 2,)
                oracle.integer_transition_fixture(base, B, C)
                valid += 1
            records.append({"base": base, "width": width, "starts": starts, "valid_edges": valid})
    return records


def known_cycle_checks():
    records = []
    for control in oracle.known_controls():
        base, es, gs = control["base"], control["e"], control["g"]
        sink = sink_domains(base, es, gs)
        full = full_return_domains(base, es, gs)
        for t, B in enumerate(control["B"]):
            require(B[-1] in sink[t] and B[-1] in full[t], "known positive cycle was pruned")
            require(base - 1 in sink[t] and base - 1 in full[t], "neutral padding was pruned")
            require(set(full[t]) <= set(sink[t]), "full-return support exceeds sink support")
        padded_edges = []
        for B, C, B2, C2, u, v in control["edges"]:
            padded_edges.append((B + (base - 1,), C, B2 + (base - 1,), C2, u, v))
        padded_e, padded_g = oracle.check_cycle(base, padded_edges)
        require((padded_e, padded_g) == (es, gs), "extra neutral suffix changed streams")
        records.append({"base": base, "period": control["period"], "width": control["width"],
                        "tail_word": [B[-1] for B in control["B"]],
                        "sink_states": sum(map(len, sink)), "full_return_states": sum(map(len, full)),
                        "actual_and_extra_padded_edges": 2 * control["period"]})
    return records


def target_projection():
    es, gs = oracle.TARGET_E * 2, oracle.TARGET_G * 2
    rows = phase_graph(10, es, gs)
    sink = sink_domains(10, es, gs)
    full = full_return_domains(10, es, gs)
    require(sink == full, "target sink and exact-48-return supports differ")
    require(all(9 in domain for domain in full), "target neutral tail missing")
    require(all(full[t] == (9,) for t, bit in enumerate(gs) if bit),
            "target overflow does not force a neutral tail")
    return {"base": 10, "period": 48, "e": es, "g": gs,
            "vertices": len(rows), "edges": sum(map(len, rows)),
            "nonempty_local_rows": sum(bool(row) for row in rows),
            "sink_states": sum(map(len, sink)), "full_return_states": sum(map(len, full)),
            "supports": full, "cardinalities": tuple(map(len, full)),
            "support_table_repeats_at_24": full[:24] == full[24:],
            "scope": "Only coefficient domains repeat at 24; exterior states remain independent across all 48 phases."}


def selftest():
    started = time.perf_counter()
    edges = exhaustive_edge_checks()
    cycles = known_cycle_checks()
    neutral_local_cases = 0
    for base in range(2, 33):
        for e, g, next_e in itertools.product((0, 1), repeat=3):
            require(base - 1 in local_targets(base, e, g, base - 1), "neutral self-edge missing")
            require(eligible_tail(base, next_e, base - 1), "next carry excludes neutral tail")
            neutral_local_cases += 1
    target = target_projection()
    return {"status": "PASS", "classification": "COMPUTED",
            "exhaustive_boxes": edges, "starts": sum(row["starts"] for row in edges),
            "valid_edges_and_integer_fixtures": sum(row["valid_edges"] for row in edges),
            "known_controls": cycles, "neutral_local_cases": neutral_local_cases,
            "target": target, "wall_seconds": round(time.perf_counter() - started, 6),
            "max_rss_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                           // (1024 if sys.platform == "darwin" else 1)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", choices=("selftest", "target"), default="selftest")
    args = parser.parse_args()
    print(json.dumps(selftest() if args.command == "selftest" else target_projection(), sort_keys=True))


if __name__ == "__main__":
    main()
