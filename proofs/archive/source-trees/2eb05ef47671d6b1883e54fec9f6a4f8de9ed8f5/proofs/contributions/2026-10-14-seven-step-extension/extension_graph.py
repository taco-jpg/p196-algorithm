#!/usr/bin/env python3
"""Exact necessary spatial extensions of the seven-step prefix clock.

Every deeper incoming carry is retained.  Graph exclusion is therefore
sound without constructing an independently chosen carry history.
"""

from collections import deque
import json
from pathlib import Path


ROOT_PREFIX = ((4, 4, 0), (8, 8, 0), (16, 16, 0), (7, 14, 7),
               (15, 8, 15), (6, 14, 14), (13, 9, 9))
CLOCK = (0, 0, 1, 0, 1, 0, 1)


def prefix_update(p, incoming):
    low, high = [], []
    carry = 0
    for x in p:
        carry, digit = divmod(x + carry, 10)
        low.append(digit)
    lower_carry = carry
    carry = incoming
    for x in reversed(p):
        carry, digit = divmod(x + carry, 10)
        high.append(digit)
    high.reverse()
    overflow = carry
    out = tuple(low[i] + (1 if i == 0 else high[i - 1]) for i in range(len(p))) if overflow else tuple(a + b for a, b in zip(low, high))
    return out, overflow, lower_carry


def phase_edges(p, target, expected_overflow):
    allowed = []
    for incoming in (0, 1):
        out, overflow, lower = prefix_update(p, incoming)
        if out == target and overflow == expected_overflow:
            allowed.append(incoming)
    edges = [[] for _ in range(19)]
    for a in range(19):
        for deeper in (0, 1):
            carry = (a + deeper) // 10
            if carry not in allowed:
                continue
            low_digit = (a + lower) % 10
            high_digit = ((p[-1] + carry) % 10 if expected_overflow
                          else (a + deeper) % 10)
            nxt = low_digit + high_digit
            assert 0 <= nxt <= 18
            edges[a].append(dict(deeper=deeper, carry=carry, next=nxt))
    return edges, allowed, lower


def components(graph):
    index = 0
    indices, low, stack, active, result = {}, {}, [], set(), []

    def visit(v):
        nonlocal index
        indices[v] = low[v] = index
        index += 1
        stack.append(v)
        active.add(v)
        for w in graph[v]:
            if w not in indices:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in active:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            group = []
            while True:
                w = stack.pop()
                active.remove(w)
                group.append(w)
                if w == v:
                    break
            result.append(sorted(group))

    for v in range(19):
        if v not in indices:
            visit(v)
    return sorted(result)


def analyze(prefixes, label):
    phases, carries, lower = [], [], []
    for t in range(7):
        edges, allowed, low = phase_edges(prefixes[t], prefixes[(t + 1) % 7], CLOCK[t])
        phases.append(edges)
        carries.append(allowed)
        lower.append(low)
    macro = []
    closed_paths = {}
    for start in range(19):
        paths = {(start,)}
        for phase in phases:
            paths = {path + (edge["next"],) for path in paths for edge in phase[path[-1]]}
        macro.append(sorted({p[-1] for p in paths}))
        closed_paths[str(start)] = sorted([list(p[:-1]) for p in paths if p[-1] == start])
    sccs = components(macro)
    cyclic = [s for s in sccs if len(s) > 1 or s[0] in macro[s[0]]]
    ranks = {}
    while True:
        new = {v: 1 + max((ranks[w] for w in macro[v]), default=-1)
               for v in range(19) if v not in ranks and all(w in ranks for w in macro[v])}
        if not new:
            break
        ranks.update(new)
    for v, rank in ranks.items():
        assert all(w in ranks and ranks[w] < rank for w in macro[v])
    forced_children = []
    complete_reduction = True
    for component in cyclic:
        if len(component) != 1:
            complete_reduction = False
            continue
        a = component[0]
        paths = closed_paths[str(a)]
        if len(paths) != 1:
            complete_reduction = False
            continue
        path = paths[0]
        child = tuple(tuple(prefixes[t]) + (path[t],) for t in range(7))
        forced_children.append((label + "/" + str(a), child))
    report = dict(label=label, prefix_width=len(prefixes[0]), prefixes=prefixes,
                  overflow_clock=CLOCK, allowed_carries=carries, lower_carries=lower,
                  phase_edges=phases, macro_edges=macro, sccs=sccs, cyclic_sccs=cyclic,
                  sink_deletion_ranks={str(v): ranks[v] for v in sorted(ranks)},
                  live_states=[v for v in range(19) if v not in ranks],
                  closed_one_period_paths={k: v for k, v in closed_paths.items() if v},
                  forced_child_labels=[name for name, _ in forced_children],
                  complete_eventual_clock_reduction=complete_reduction,
                  status="NO_INFINITE_EXTENSION" if not cyclic else "NECESSARY_EXTENSION_SURVIVES")
    return report, forced_children


def main():
    queue = deque([("440", ROOT_PREFIX)])
    records, frontier = [], []
    while queue and len(records) < 200:
        label, prefix = queue.popleft()
        report, children = analyze(prefix, label)
        records.append(report)
        print(json.dumps(dict(label=label, width=len(prefix[0]),
                              cyclic_sccs=report["cyclic_sccs"],
                              children=report["forced_child_labels"],
                              complete=report["complete_eventual_clock_reduction"])), flush=True)
        if not report["complete_eventual_clock_reduction"]:
            frontier.append(dict(label=label, reason="nontrivial SCC or multiple period paths"))
        elif len(prefix[0]) >= 12 and children:
            frontier.append(dict(label=label, reason="prefix width cap12"))
        else:
            queue.extend(children)
    frontier.extend(dict(label=label, reason="node cap200") for label, _ in queue)
    result = dict(status="NO_PERPETUAL_440_CLOCK" if not frontier else "UNRESOLVED_FRONTIER",
                  records=records, unresolved_frontier=frontier,
                  scope="Necessary arbitrary-carry spatial relations; no surviving graph is an actual infinite decimal orbit.")
    Path(__file__).with_name("extension_graph.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(dict(status=result["status"], analyzed_clocks=len(records), frontier=frontier)))


if __name__ == "__main__":
    main()
