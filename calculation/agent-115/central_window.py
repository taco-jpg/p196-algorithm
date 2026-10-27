#!/usr/bin/env python3
"""Exact central-three/central-four abstraction of decimal reverse-and-add.

An odd state O(a,r) records the folded coefficient window (a,r,a), with
r even. An even state E(a,s) records (a,s,s,a). The domain consists of
ordinary positive integers of odd width >=3 or even width >=4. There is
no bound on the full width. A graph edge is existential over compatible
integer inputs; the safe-invariant pruning quantifies over EVERY edge.

The local relation is exact. For odd inputs, normalize the five central
coefficients (z,a,r,a,z) with incoming carry c in {0,1}. Every actual
longer input supplies such z,c. Width-three inputs use virtual z=c=0.
Every enumerated case is realized by the symmetric folded word
    (v,u,z,a,r,a,z,u,v), v=1+9*g, u=10*c.
The outer v forces overflow g, and u forces the carry entering z.
For even inputs, normalize (a,s,s,a) with incoming carry c. Every case
is realized by (v,u,a,s,s,a,u,v). Thus no independently guessed carry
is accepted without a compatible ordinary-integer fixture.

Every graph edge is checked against bigint n + int(str(n)[::-1]),
independently of the local carry arithmetic. Every rejected safety
state has an explicit completion producing a palindrome in one step.

Scope: an empty universally safe invariant does NOT exclude an
individual infinite safe orbit, a full neutral-band certificate, or a
decimal Lychrel number. Counterexample completions may differ per edge.
This is a computed abstraction audit, not a Lean-verified theorem.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from typing import NamedTuple


class State(NamedTuple):
    parity: str
    outer: int
    middle: int

    def label(self) -> str:
        return f"{self.parity}({self.outer},{self.middle})"

    def window(self) -> tuple[int, ...]:
        a, x = self.outer, self.middle
        return (a, x, a) if self.parity == "O" else (a, x, x, a)


class Edge(NamedTuple):
    overflow: int
    target: State


class Fixture(NamedTuple):
    seed: int
    coefficients: tuple[int, ...]
    incoming: int
    neighbor: int | None


def require(condition: bool, message: str) -> None:
    """Test-harness check that is also active under python -O."""
    if not condition:
        raise AssertionError(message)


def all_states() -> tuple[State, ...]:
    odd = (State("O", a, r) for a in range(19) for r in range(0, 19, 2))
    even = (State("E", a, s) for a in range(19) for s in range(19))
    return tuple(sorted((*odd, *even)))


def state_id(state: State) -> int:
    """Stable O-first numbering shared with the finite Lean verification."""
    if state.parity == "O":
        return 10 * state.outer + state.middle // 2
    return 190 + 19 * state.outer + state.middle


def normalize(word: tuple[int, ...], carry: int) -> tuple[int, ...]:
    digits = []
    for coefficient in word:
        total = coefficient + carry
        digits.append(total % 10)
        carry = total // 10
    return tuple(digits)


def realize(coefficients: tuple[int, ...]) -> int:
    """Realize a symmetric valid folded word as a canonical positive integer."""
    q = coefficients
    require(bool(q) and q[0] > 0 and q == q[::-1], "invalid folded word")
    require(all(0 <= x <= 18 for x in q), "coefficient outside 0..18")
    n = len(q)
    ds = [0] * n
    for i in range(n // 2):
        ds[n - 1 - i] = min(9, q[i])
        ds[i] = q[i] - ds[n - 1 - i]
    if n % 2:
        require(q[n // 2] % 2 == 0, "odd folded middle must be even")
        ds[n // 2] = q[n // 2] // 2
    return sum(digit * 10**i for i, digit in enumerate(ds))


def decimal_fold(n: int) -> tuple[int, ...]:
    require(n > 0, "positive integer required")
    ds = tuple(int(x) for x in str(n)[::-1])
    return tuple(a + b for a, b in zip(ds, ds[::-1]))


def state_of(n: int) -> State:
    q = decimal_fold(n)
    h = len(q) // 2
    if len(q) % 2:
        require(len(q) >= 3, "odd domain starts at width three")
        return State("O", q[h - 1], q[h])
    require(len(q) >= 4, "even domain starts at width four")
    return State("E", q[h - 2], q[h - 1])


def next_integer(n: int) -> int:
    return n + int(str(n)[::-1])


def edge_cases(source: State):
    """Yield all local cases and their finite realizations, without bigint use."""
    a, x = source.outer, source.middle
    for g in (0, 1):
        v = 1 + 9 * g
        for carry in (0, 1):
            u = 10 * carry
            if source.parity == "O":
                for z in range(19):
                    ds = normalize((z, a, x, a, z), carry)
                    target = (State("E", ds[1] + ds[4], ds[2] + ds[3])
                              if g else State("O", ds[1] + ds[3], 2 * ds[2]))
                    q = (v, u, z, a, x, a, z, u, v)
                    yield Edge(g, target), q, carry, z
            else:
                ds = normalize((a, x, x, a), carry)
                target = (State("O", ds[1] + ds[3], 2 * ds[2])
                          if g else State("E", ds[0] + ds[3], ds[1] + ds[2]))
                q = (v, u, a, x, x, a, u, v)
                yield Edge(g, target), q, carry, None


def build_graph() -> dict[State, dict[Edge, Fixture]]:
    graph: dict[State, dict[Edge, Fixture]] = {}
    for source in all_states():
        edges: dict[Edge, Fixture] = {}
        for edge, q, carry, neighbor in edge_cases(source):
            if edge not in edges:
                edges[edge] = Fixture(realize(q), q, carry, neighbor)
        graph[source] = dict(sorted(edges.items()))
    return graph


def universally_safe(state: State) -> bool:
    q = state.window()
    return max(q) >= 10 and any(x not in (0, 11) for x in q)


def palindrome_completion(state: State) -> int:
    require(not universally_safe(state), "state is universally safe")
    q = state.window()
    outside = 1 if max(q) <= 9 else 11
    return realize((outside, *q, outside))


def prune(graph: dict[State, dict[Edge, Fixture]]):
    """Greatest universally closed safe subset; ranks are existential escape depth."""
    live = {s for s in graph if universally_safe(s)}
    counts = [len(live)]
    rank = {s: 0 for s in graph if s not in live}
    bad_successor: dict[State, Edge] = {}
    round_number = 1
    while live:
        removed = {
            s for s in live if any(edge.target not in live for edge in graph[s])
        }
        if not removed:
            break
        for s in sorted(removed):
            options = [edge for edge in graph[s] if edge.target not in live]
            bad_successor[s] = min(options, key=lambda e: (rank[e.target], e))
        for s in removed:
            rank[s] = round_number
        live -= removed
        counts.append(len(live))
        round_number += 1
    return counts, frozenset(live), rank, bad_successor


def verify(graph, ranks, bad_successor) -> dict[str, int]:
    """Independent integer checks for every edge, unsafe state, and short width."""
    edge_checks = 0
    for source, successors in graph.items():
        for edge, fixture in successors.items():
            n = fixture.seed
            nxt = next_integer(n)
            require(decimal_fold(n) == fixture.coefficients, "realization failed")
            require(state_of(n) == source, "fixture has wrong source state")
            require(state_of(nxt) == edge.target, "bigint successor differs")
            require(len(str(nxt)) - len(str(n)) == edge.overflow, "wrong overflow")
            if universally_safe(source):
                require(str(nxt) != str(nxt)[::-1], "safe fixture became palindrome")
            edge_checks += 1

    unsafe_checks = 0
    for source in graph:
        if not universally_safe(source):
            n = palindrome_completion(source)
            nxt = next_integer(n)
            require(state_of(n) == source, "palindrome completion source differs")
            require(str(nxt) == str(nxt)[::-1], "unsafe completion is not a palindrome")
            unsafe_checks += 1

    # Exhaust every realizable folded word at the two minimum widths.
    short_checks = 0
    for source in graph:
        q = source.window()
        if q[0] == 0:
            continue
        n = realize(q)
        nxt = next_integer(n)
        edge = Edge(len(str(nxt)) - len(str(n)), state_of(nxt))
        require(edge in graph[source], "short-width transition is absent")
        short_checks += 1

    for source, edge in bad_successor.items():
        require(edge in graph[source], "rank witness edge is absent")
        require(ranks[edge.target] + 1 == ranks[source], "rank witness does not decrease")
    return {"integer_edge_checks": edge_checks,
            "unsafe_palindrome_checks": unsafe_checks,
            "minimum_width_checks": short_checks,
            "rank_witness_checks": len(bad_successor)}


def state_record(state, graph, ranks, bad_successor):
    record = {"state": state.label(), "universally_safe": universally_safe(state),
              "rank": ranks.get(state), "outdegree": len(graph[state])}
    if not universally_safe(state):
        n = palindrome_completion(state)
        record["palindrome_seed"] = n
        record["palindrome_successor"] = next_integer(n)
    elif state in bad_successor:
        edge = bad_successor[state]
        fixture = graph[state][edge]
        record["counterexample_edge"] = {
            "overflow": edge.overflow, "target": edge.target.label(),
            "seed": fixture.seed, "successor": next_integer(fixture.seed),
            "coefficients": fixture.coefficients}
    return record


def lean_data(graph, counts, ranks, bad_successor):
    """Reproducible rank/control export; unsafe rows have unused dummy controls."""
    rows = []
    for source in sorted(graph, key=state_id):
        row = {"id": state_id(source), "state": source.label(),
               "parity": source.parity, "a": source.outer, "middle": source.middle,
               "rank": ranks[source], "safe": universally_safe(source)}
        if source in bad_successor:
            edge = bad_successor[source]
            fixture = graph[source][edge]
            row.update(g=edge.overflow, c=fixture.incoming,
                       z=fixture.neighbor if fixture.neighbor is not None else 0,
                       target_id=state_id(edge.target), target=edge.target.label(),
                       target_rank=ranks[edge.target], seed=fixture.seed,
                       coefficients=fixture.coefficients)
        else:
            row.update(g=0, c=0, z=0, target_id=state_id(source),
                       target=source.label(), target_rank=0,
                       palindrome_seed=palindrome_completion(source))
        rows.append(row)
    return {"state_indexing": "O(a,r):10*a+r/2; E(a,s):190+19*a+s",
            "safe_set_sizes": counts, "max_rank": max(ranks.values()), "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print exact summary as JSON")
    parser.add_argument("--states", action="store_true", help="include every rank/counterexample")
    parser.add_argument("--edges", action="store_true", help="include every integer edge fixture")
    parser.add_argument("--lean-data", action="store_true", help="export O-first ranks and legal control witnesses")
    args = parser.parse_args()
    graph = build_graph()
    counts, invariant, ranks, bad_successor = prune(graph)
    checks = verify(graph, ranks, bad_successor)
    if args.lean_data:
        print(json.dumps(lean_data(graph, counts, ranks, bad_successor), indent=2, sort_keys=True))
        return
    edge_counts = Counter((s.parity, e.overflow) for s in graph for e in graph[s])
    summary = {
        "classification": "COMPUTED",
        "states": len(graph),
        "odd_states": sum(s.parity == "O" for s in graph),
        "even_states": sum(s.parity == "E" for s in graph),
        "labelled_edges": sum(map(len, graph.values())),
        "edges_by_source_parity_and_overflow": {
            f"{parity},g={g}": count for (parity, g), count in sorted(edge_counts.items())},
        "safe_set_sizes": counts,
        "greatest_universally_safe_invariant": [s.label() for s in sorted(invariant)],
        "rank_histogram": dict(sorted(Counter(ranks.values()).items())),
        "max_rank": max(ranks.values(), default=0),
        "checks": checks,
        "scope": "Universal closure over compatible completions; no individual-orbit or Lychrel no-go.",
    }
    if args.states:
        summary["state_records"] = [state_record(s, graph, ranks, bad_successor) for s in graph]
    if args.edges:
        summary["edge_records"] = [
            {"source": s.label(), "overflow": e.overflow, "target": e.target.label(),
             "seed": f.seed, "successor": next_integer(f.seed), "coefficients": f.coefficients}
            for s, successors in graph.items() for e, f in successors.items()]
    if args.json or args.states or args.edges:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"states={summary['states']} odd={summary['odd_states']} even={summary['even_states']}")
        print(f"labelled_edges={summary['labelled_edges']} by_parity_g={summary['edges_by_source_parity_and_overflow']}")
        print(f"safe_set_sizes={counts} invariant_size={len(invariant)}")
        print(f"rank_histogram={summary['rank_histogram']} max_rank={summary['max_rank']}")
        print(" ".join(f"{name}={count}" for name, count in checks.items()))
        print("ALL CHECKS PASSED")
        print("COMPUTED: universal-completion abstraction only; not an individual-orbit no-go.")


if __name__ == "__main__":
    main()
