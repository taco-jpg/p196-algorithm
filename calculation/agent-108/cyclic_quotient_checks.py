#!/usr/bin/env python3
"""Independent finite controls for cyclic-word lifting through a graph quotient.

Hypotheses: the projection preserves labelled edges; every quotient outgoing
labelled edge lifts from EVERY vertex in its source fiber; the chosen base
fiber is finite and nonempty.  For a closed quotient word w and supplied
start, a local deterministic choice produces a path w**r followed by a
closed path w**m, with m>=1 and r+m<=the base-fiber cardinality.  Returning
to the supplied start or taking m=1 is not asserted.

The local-choice construction is compared with independent Boolean endpoint
relation composition and a breadth-first simple-lasso search.  Every output
path is checked edge by edge, including labels, quotient phases, and bound.
Exhaustive domains are printed explicitly.  The finite controls do not prove
the unrestricted theorem, instantiate an exterior graph, or supply a decimal
certificate.  All validation uses explicit exceptions, including under -O.
"""
from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass, replace
from itertools import product
import json
import time


class CheckFailure(RuntimeError):
    pass


class BudgetExceeded(RuntimeError):
    pass


def require(condition, detail):
    if not condition:
        raise CheckFailure(detail)


@dataclass(frozen=True)
class Graph:
    projection: tuple[int, ...]
    quotient_size: int
    edges: frozenset[tuple[int, int, int]]
    quotient_edges: frozenset[tuple[int, int, int]]

    def fiber(self, base):
        return tuple(v for v, image in enumerate(self.projection) if image == base)


@dataclass(frozen=True)
class ClosedWord:
    phases: tuple[int, ...]
    labels: tuple[int, ...]


@dataclass(frozen=True)
class Certificate:
    r: int
    m: int
    endpoints: tuple[int, ...]
    vertices: tuple[int, ...]


def check_shapes(graph, word):
    n = len(graph.projection)
    require(graph.quotient_size > 0, "empty quotient vertex domain")
    require(all(type(q) is int and 0 <= q < graph.quotient_size for q in graph.projection),
            "projection outside quotient domain")
    require(all(type(u) is type(a) is type(v) is int and 0 <= u < n and a in (0, 1)
                and 0 <= v < n for u, a, v in graph.edges), "malformed original edge")
    require(all(0 <= u < graph.quotient_size and a in (0, 1)
                and 0 <= v < graph.quotient_size for u, a, v in graph.quotient_edges),
            "malformed quotient edge")
    require(len(word.phases) == len(word.labels) + 1, "word phase/label length mismatch")
    require(word.phases[0] == word.phases[-1], "quotient word is not closed")
    require(all((u, a, v) in graph.quotient_edges
                for u, a, v in zip(word.phases, word.labels, word.phases[1:])),
            "word contains an absent quotient edge")


def homomorphism(graph):
    pi = graph.projection
    return all((pi[u], a, pi[v]) in graph.quotient_edges for u, a, v in graph.edges)


def pointwise_lifting(graph):
    pi = graph.projection
    return all(any((v, a, z) in graph.edges and pi[z] == target
                   for z in range(len(pi)))
               for source, a, target in graph.quotient_edges
               for v in graph.fiber(source))


def local_word_lift(graph, word, start):
    """Pointwise choice: choose the least valid original vertex at each phase."""
    require(graph.projection[start] == word.phases[0], "wrong start fiber")
    vertices = [start]
    for label, target_phase in zip(word.labels, word.phases[1:]):
        choices = [z for z, image in enumerate(graph.projection)
                   if image == target_phase and (vertices[-1], label, z) in graph.edges]
        require(bool(choices), "pointwise lift missing")
        vertices.append(choices[0])
    return tuple(vertices)


def lift_closed_word(graph, word, start):
    """Return an explicit transient-plus-cycle path, with a checked fiber bound."""
    check_shapes(graph, word)
    require(homomorphism(graph) and pointwise_lifting(graph), "quotient hypotheses fail")
    fiber = graph.fiber(word.phases[0])
    require(bool(fiber) and start in fiber, "base fiber is empty or start is outside it")
    seen, endpoints, vertices = {start: 0}, [start], [start]
    for lap in range(1, len(fiber) + 1):
        path = local_word_lift(graph, word, endpoints[-1])
        vertices.extend(path[1:])
        endpoint = path[-1]
        endpoints.append(endpoint)
        if endpoint in seen:
            r = seen[endpoint]
            result = Certificate(r, lap - r, tuple(endpoints), tuple(vertices))
            check_certificate(graph, word, start, result)
            return result
        seen[endpoint] = lap
    raise CheckFailure("finite fiber had no repeated endpoint within its cardinality")


def endpoint_relation(graph, word):
    """Independent Boolean-matrix product, not the pointwise-choice map."""
    n = len(graph.projection)
    relation = [1 << u for u in range(n)]
    for source_phase, label, target_phase in zip(word.phases, word.labels, word.phases[1:]):
        factor = [0] * n
        for u, a, v in graph.edges:
            if a == label and graph.projection[u] == source_phase and graph.projection[v] == target_phase:
                factor[u] |= 1 << v
        following = []
        for row in relation:
            target = 0
            for middle in range(n):
                if row & (1 << middle):
                    target |= factor[middle]
            following.append(target)
        relation = following
    fiber = graph.fiber(word.phases[0])
    fiber_mask = sum(1 << v for v in fiber)
    return {u: relation[u] & fiber_mask for u in fiber}


def layered_paths(graph, word, start):
    """Ordinary layered graph search supplies witnesses for EVERY reachable end."""
    reached = {start: (start,)}
    for phase, label, next_phase in zip(word.phases, word.labels, word.phases[1:]):
        following = {}
        for u, a, v in sorted(graph.edges):
            if (u in reached and a == label and graph.projection[u] == phase
                    and graph.projection[v] == next_phase and v not in following):
                following[v] = reached[u] + (v,)
        reached = following
    return reached


def endpoint_lasso(relation, start):
    """Independent BFS of simple endpoint paths; closure may follow a transient."""
    queue = deque([(start,)])
    vertices = tuple(sorted(relation))
    while queue:
        path = queue.popleft()
        for target in vertices:
            if not (relation[path[-1]] & (1 << target)):
                continue
            if target in path:
                r = path.index(target)
                return r, len(path) - r, path + (target,)
            queue.append(path + (target,))
    return None


def relation_certificate(paths, lasso):
    r, m, endpoints = lasso
    vertices = [endpoints[0]]
    for u, v in zip(endpoints, endpoints[1:]):
        vertices.extend(paths[u][v][1:])
    return Certificate(r, m, endpoints, tuple(vertices))


def check_certificate(graph, word, start, certificate):
    r, m, endpoints, vertices = (certificate.r, certificate.m,
                                  certificate.endpoints, certificate.vertices)
    fiber = graph.fiber(word.phases[0])
    require(0 <= r and 1 <= m and r + m <= len(fiber), "invalid r/m fiber bound")
    require(len(endpoints) == r + m + 1 and endpoints[0] == start, "bad endpoint sequence")
    require(all(v in fiber for v in endpoints), "endpoint left the base fiber")
    require(endpoints[r] == endpoints[-1], "cycle suffix does not close")
    labels = word.labels * (r + m)
    require(len(vertices) == len(labels) + 1 and vertices[0] == start, "bad path length/start")
    require(all(0 <= v < len(graph.projection) for v in vertices), "path vertex outside domain")
    require(all((u, a, v) in graph.edges for u, a, v in zip(vertices, labels, vertices[1:])),
            "path has an absent/mislabelled original edge")
    expected_phases = (word.phases[0],) + word.phases[1:] * (r + m)
    require(tuple(graph.projection[v] for v in vertices) == expected_phases,
            "path loses quotient phase order")
    require(all(vertices[j * len(word.labels)] == endpoints[j] for j in range(r + m + 1)),
            "endpoint labels are not complete-word boundaries")
    cycle = vertices[r * len(word.labels):]
    require(cycle[0] == cycle[-1] and len(cycle) == m * len(word.labels) + 1,
            "wrong closed-word power")


POWER_PREDICATES = {
    "nonempty": lambda w: bool(w),
    "contains_zero": lambda w: 0 in w,
    "contains_one": lambda w: 1 in w,
    "even_ones": lambda w: w.count(1) % 2 == 0,
    "balanced_bits": lambda w: w.count(0) == w.count(1),
    "positive_bit_weight": lambda w: w.count(1) > w.count(0),
}


class Audit:
    def __init__(self, seconds):
        self.started = time.monotonic()
        self.deadline = self.started + seconds
        self.totals = {}

    def budget(self):
        if time.monotonic() >= self.deadline:
            raise BudgetExceeded("explicit time budget reached")

    def run_domain(self, name, instances, expected_graphs, expected_cases, description):
        counts = {"graphs": 0, "closed_words": 0, "starts": 0, "path_certificates": 0,
                  "endpoint_pairs": 0, "power_predicate_implications": 0,
                  "max_r": 0, "max_m": 0, "max_r_plus_m": 0}
        for graph, words in instances:
            self.budget()
            require(homomorphism(graph) and pointwise_lifting(graph), "invalid generated quotient")
            counts["graphs"] += 1
            for word in words:
                check_shapes(graph, word)
                relation = endpoint_relation(graph, word)
                paths = {u: layered_paths(graph, word, u) for u in relation}
                for u, targets in paths.items():
                    require(sum(1 << v for v in targets) == relation[u], "matrix/layered relation mismatch")
                    require(bool(targets), "empty endpoint row under pointwise lifting")
                    counts["endpoint_pairs"] += len(targets)
                counts["closed_words"] += 1
                for start in relation:
                    original = lift_closed_word(graph, word, start)
                    lasso = endpoint_lasso(relation, start)
                    require(lasso is not None, "independent endpoint graph lacks a reachable cycle")
                    independent = relation_certificate(paths, lasso)
                    check_certificate(graph, word, start, independent)
                    for certificate in (original, independent):
                        for predicate in POWER_PREDICATES.values():
                            if predicate(word.labels):
                                require(predicate(word.labels * certificate.m),
                                        "power-stable predicate lost on cycle suffix")
                                counts["power_predicate_implications"] += 1
                        counts["max_r"] = max(counts["max_r"], certificate.r)
                        counts["max_m"] = max(counts["max_m"], certificate.m)
                        counts["max_r_plus_m"] = max(counts["max_r_plus_m"], certificate.r + certificate.m)
                    counts["starts"] += 1
                    counts["path_certificates"] += 2
        require(counts["graphs"] == expected_graphs and counts["starts"] == expected_cases,
                ("incomplete exhaustive domain", name, counts))
        self.totals[name] = counts
        print("DOMAIN", json.dumps({"name": name, "scope": description, **counts}, sort_keys=True), flush=True)


def single_quotient_word(labels):
    return ClosedWord((0,) * (len(labels) + 1), tuple(labels))


def deterministic_instances():
    words = tuple(single_quotient_word(w) for k in range(1, 4) for w in product((0, 1), repeat=k))
    for n in range(1, 4):
        quotient = frozenset({(0, 0, 0), (0, 1, 0)})
        for maps in product(range(n), repeat=2 * n):
            edges = frozenset((u, a, maps[a * n + u]) for a in (0, 1) for u in range(n))
            yield Graph((0,) * n, 1, edges, quotient), words


def nondeterministic_instances():
    words = tuple(single_quotient_word((0,) * k) for k in range(1, 5))
    for n in range(1, 4):
        for masks in product(range(1, 1 << n), repeat=n):
            edges = frozenset((u, 0, v) for u in range(n) for v in range(n) if masks[u] & (1 << v))
            yield Graph((0,) * n, 1, edges, frozenset({(0, 0, 0)})), words


def four_vertex_instances():
    words = tuple(single_quotient_word((0,) * k) for k in range(1, 5))
    for mapping in product(range(4), repeat=4):
        edges = frozenset((u, 0, mapping[u]) for u in range(4))
        yield Graph((0,) * 4, 1, edges, frozenset({(0, 0, 0)})), words


def two_fiber_instances():
    quotient = frozenset((q, q, target) for q in (0, 1) for target in (0, 1))
    words = []
    for base in (0, 1):
        for length in range(1, 4):
            for middle in product((0, 1), repeat=length - 1):
                phases = (base,) + middle + (base,)
                words.append(ClosedWord(phases, phases[:-1]))
    for n0, n1 in product((1, 2), repeat=2):
        pi = (0,) * n0 + (1,) * n1
        choices = tuple(product(range(1, 1 << n0), range(1, 1 << n1)))
        for rows in product(choices, repeat=n0 + n1):
            edges = set()
            for u, (left, right) in enumerate(rows):
                edges.update((u, pi[u], v) for v in range(n0) if left & (1 << v))
                edges.update((u, pi[u], n0 + v) for v in range(n1) if right & (1 << v))
            yield Graph(pi, 2, frozenset(edges), quotient), tuple(words)


def rejects(callable_):
    try:
        callable_()
    except CheckFailure:
        return True
    return False


def display_certificate(graph, word, certificate):
    offset = certificate.r * len(word.labels)
    return {"r": certificate.r, "m": certificate.m,
            "fiber_size": len(graph.fiber(word.phases[0])),
            "endpoints": certificate.endpoints, "vertices": certificate.vertices,
            "labels": word.labels * (certificate.r + certificate.m),
            "projected_phases": tuple(graph.projection[v] for v in certificate.vertices),
            "cycle_vertices": certificate.vertices[offset:], "cycle_labels": word.labels * certificate.m}


def counterexamples():
    loop = frozenset({(0, 0, 0)})
    word = single_quotient_word((0,))
    acyclic = Graph((0, 0), 1, frozenset({(0, 0, 1)}), loop)
    require(homomorphism(acyclic) and not pointwise_lifting(acyclic), "bad homomorphism counterexample")
    require(endpoint_lasso(endpoint_relation(acyclic, word), 0) is None, "acyclic graph unexpectedly cycles")
    require(rejects(lambda: lift_closed_word(acyclic, word, 0)), "missing lifting hypothesis accepted")
    print("COUNTER", json.dumps({"name": "homomorphism_alone", "original_edges": sorted(acyclic.edges),
                                 "projection": acyclic.projection, "quotient_edges": sorted(loop),
                                 "homomorphism": True, "pointwise_lifting": False,
                                 "reachable_original_cycle": False}), flush=True)

    toggle = Graph((0, 0), 1, frozenset({(0, 0, 1), (1, 0, 0)}), loop)
    toggle_cert = lift_closed_word(toggle, word, 0)
    relation = endpoint_relation(toggle, word)
    require(toggle_cert.r == 0 and toggle_cert.m == 2
            and all(not (row & (1 << u)) for u, row in relation.items()), "bad one-lap counterexample")
    print("COUNTER", json.dumps({"name": "one_lap_not_forced", **display_certificate(toggle, word, toggle_cert)}), flush=True)

    transient = Graph((0, 0), 1, frozenset({(0, 0, 1), (1, 0, 1)}), loop)
    transient_cert = lift_closed_word(transient, word, 0)
    require(transient_cert.r == 1 and transient_cert.m == 1
            and not any(v == 0 for _, _, v in transient.edges), "bad supplied-start counterexample")
    print("COUNTER", json.dumps({"name": "supplied_start_need_not_return",
                                 **display_certificate(transient, word, transient_cert)}), flush=True)

    empty = Graph((0,), 2, frozenset(), frozenset({(1, 0, 1)}))
    empty_word = ClosedWord((1, 1), (0,))
    require(homomorphism(empty) and pointwise_lifting(empty) and not empty.fiber(1),
            "bad empty-base-fiber counterexample")
    require(not endpoint_relation(empty, empty_word)
            and rejects(lambda: lift_closed_word(empty, empty_word, 0)), "empty fiber accepted")
    print("COUNTER", json.dumps({"name": "empty_base_fiber", "projection": empty.projection,
                                 "base": 1, "homomorphism": True,
                                 "pointwise_lifting_vacuous": True, "fiber_size": 0}), flush=True)

    require(len(word.labels) == 1 and len(word.labels * toggle_cert.m) != 1,
            "bad non-power-stable acceptance control")
    print("COUNTER", json.dumps({"name": "arbitrary_acceptance_not_preserved",
                                 "predicate": "word_length_is_one", "quotient_accepts": True,
                                 "lifted_cycle_accepts": False, "necessary_laps": 2}), flush=True)

    zero_word = ClosedWord((0,), ())
    zero_cert = lift_closed_word(toggle, zero_word, 0)
    require(zero_cert.r == 0 and zero_cert.m == 1 and len(zero_cert.vertices) == 1,
            "empty-word semantics failed")
    print("BOUNDARY", json.dumps({"name": "empty_word_is_zero_edge_walk",
                                  **display_certificate(toggle, zero_word, zero_cert)}), flush=True)

    sharp = Graph((0,) * 4, 1, frozenset((u, 0, (u + 1) % 4) for u in range(4)), loop)
    sharp_cert = lift_closed_word(sharp, word, 0)
    require(sharp_cert.r == 0 and sharp_cert.m == 4, "fiber bound sharpness control failed")
    print("BOUNDARY", json.dumps({"name": "fiber_bound_attained",
                                  **display_certificate(sharp, word, sharp_cert)}), flush=True)

    malformed = [replace(toggle_cert, m=0), replace(toggle_cert, r=2),
                 replace(toggle_cert, vertices=(0, 0, 0)), replace(toggle_cert, endpoints=(0, 0, 0))]
    require(all(rejects(lambda item=item: check_certificate(toggle, word, 0, item)) for item in malformed),
            "malformed certificate was accepted")
    print("COUNTER_CONTROLS", json.dumps({"counterexamples": 5, "boundary_cases": 2,
                                          "malformed_rejections": len(malformed), "status": "PASS"}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", choices=("all", "deterministic", "nondeterministic", "four", "fibers", "counterexamples"), default="all")
    parser.add_argument("--seconds", type=float, default=180)
    args = parser.parse_args()
    if not 0 < args.seconds <= 1700:
        parser.error("time budget must be in (0,1700] seconds")
    audit = Audit(args.seconds)
    domains = {
        "deterministic": (deterministic_instances, 746, 31080,
                          "all pairs of total maps on n=1..3; all binary words lengths1..3; every start"),
        "nondeterministic": (nondeterministic_instances, 353, 4192,
                             "all one-label nonempty-outgoing graphs on n=1..3; word lengths1..4; every start"),
        "four": (four_vertex_instances, 256, 4096,
                 "all total one-label maps on4 vertices; word lengths1..4; every start"),
        "fibers": (two_fiber_instances, 6616, 184856,
                   "fiber sizes1/2 each; all nonempty target subsets in BOTH fibers per source; label=source phase; every closed quotient path lengths1..3/start"),
    }
    try:
        if args.suite in ("all", "counterexamples"):
            counterexamples()
        for name, (instances, graphs, cases, scope) in domains.items():
            if args.suite in ("all", name):
                audit.run_domain(name, instances(), graphs, cases, scope)
        audit.budget()
    except BudgetExceeded:
        print("RESULT", json.dumps({"status": "UNDECIDED", "reason": "time_cap",
                                     "completed_domains": sorted(audit.totals)}), flush=True)
        return 3
    totals = {key: sum(result[key] for result in audit.totals.values())
              for key in ("graphs", "closed_words", "starts", "path_certificates", "endpoint_pairs", "power_predicate_implications")}
    print("RESULT", json.dumps({"status": "PASS", "suite": args.suite, **totals,
                                 "seconds": round(time.monotonic() - audit.started, 6)}, sort_keys=True), flush=True)
    print("ALL CYCLIC QUOTIENT CONTROLS PASSED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
