#!/usr/bin/env python3
"""Independent physical-FIRST controls for an exterior invariant checker.

The priority P24 forced-head observation is credited to Agents115/106.
This module independently proves its all-repetition FIRST language by an
exact finite head graph. It generates candidate fixtures, not invariants
asserted to be closed under later spatial images.
"""
from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from itertools import product
import json
from math import prod
from pathlib import Path


TARGET_E = "010100110100101011001011"
TARGET_G = "110001001000110001001000"
TARGET_HEADS = (9, 10, 1, 2, 5, 11, 2, 5, 10, 1, 2, 4) * 2


@dataclass
class Candidate:
    base: int
    e: str
    g: str
    start: int
    accepting: list[bool]
    edges: list[dict[int, int]]


def validate(base: int, e: str, g: str) -> None:
    if type(base) is not int or not 2 <= base <= 62:
        raise ValueError("base must be an integer in2..62")
    if not e or len(e) != len(g) or set(e + g) - {"0", "1"} or "1" not in g:
        raise ValueError("equal nonempty binary streams with positive overflow required")


def symbol(base: int, phase: int, low: int, high: int, digit: int) -> int:
    return phase * (4 * base) + low * (2 * base) + high * base + digit


def first_rows(base: int, overflow: int, head: int):
    """Rows (next_head,next_low,next_high,next_Y) at the physical low boundary.

    Independently derived from L=0,H=g,Y=g and whole-coefficient division.
    Every supplied head is positive; each next head is checked explicitly.
    """
    if not 1 <= head <= 2 * base - 2:
        return
    for inward in (0, 1):
        quotient, high_digit = divmod(head + inward, base)
        if quotient != overflow:
            continue
        low_carry, low_digit = divmod(head, base)
        following = low_digit + (1 if overflow else high_digit)
        if 1 <= following <= 2 * base - 2:
            yield following, low_carry, inward, high_digit if overflow else 0


def cyclic_vertices(adjacency: list[set[int]]) -> set[int]:
    """Exact iterative Kosaraju SCCs; only vertices on directed cycles survive."""
    n = len(adjacency)
    reverse = [set() for _ in range(n)]
    for source, targets in enumerate(adjacency):
        for target in targets:
            reverse[target].add(source)
    seen, finished = set(), []
    for source in range(n):
        if source in seen:
            continue
        seen.add(source)
        stack = [(source, iter(adjacency[source]))]
        while stack:
            vertex, targets = stack[-1]
            target = next(targets, None)
            if target is None:
                finished.append(vertex)
                stack.pop()
            elif target not in seen:
                seen.add(target)
                stack.append((target, iter(adjacency[target])))
    seen, cyclic = set(), set()
    for source in reversed(finished):
        if source in seen:
            continue
        component, todo = [], [source]
        seen.add(source)
        while todo:
            vertex = todo.pop()
            component.append(vertex)
            for target in reverse[vertex]:
                if target not in seen:
                    seen.add(target)
                    todo.append(target)
        if len(component) > 1 or source in adjacency[source]:
            cyclic.update(component)
    return cyclic


def head_graph(base: int, g: str):
    span, period = 2 * base - 2, len(g)
    graph = [set() for _ in range(span * period)]
    for phase in range(period):
        for head in range(1, span + 1):
            graph[phase * span + head - 1] = {
                ((phase + 1) % period) * span + row[0] - 1
                for row in first_rows(base, int(g[phase]), head)}
    return graph, cyclic_vertices(graph)


def positive_phase_product(base: int, e: str, g: str, choices) -> Candidate:
    period = len(g)
    if len(choices) != period or any(not row for row in choices):
        return empty_candidate(base, e, g)
    edges = [{int(label): phase + 1 for label in choices[phase]}
             for phase in range(period)]
    edges.append({int(label): 1 for label in choices[0]})
    return Candidate(base, e, g, 0, [False] * period + [True], edges)


def empty_candidate(base: int, e: str, g: str) -> Candidate:
    validate(base, e, g)
    return Candidate(base, e, g, 0, [False], [{}])


def universal_candidate(base: int, e: str, g: str) -> Candidate:
    validate(base, e, g)
    choices = [[symbol(base, phase, low, high, digit)
                for low in (0, 1) for high in (0, 1)
                for digit in (range(base) if overflow == "1" else (0,))]
               for phase, overflow in enumerate(g)]
    return positive_phase_product(base, e, g, choices)


def first_candidate(base: int, e: str, g: str):
    """Return exact FIRST when the cyclic head graph has at most one head/phase.

    Multiple surviving heads are explicitly unsupported by this fixture
    constructor; they are not discarded or interpreted as nonexistence.
    """
    validate(base, e, g)
    graph, cyclic = head_graph(base, g)
    span, period = 2 * base - 2, len(g)
    metadata = {"head_vertices": len(graph), "head_arcs": sum(map(len, graph)),
                "cyclic_vertices": len(cyclic)}
    if not cyclic:
        metadata.update(heads=[], choices_per_phase=[], blocks_per_unit=0)
        return empty_candidate(base, e, g), metadata
    heads = [[head for head in range(1, span + 1)
              if phase * span + head - 1 in cyclic] for phase in range(period)]
    if any(len(row) != 1 for row in heads):
        raise ValueError("multiple cyclic heads: fixture constructor is inconclusive")
    forced = tuple(row[0] for row in heads)
    choices = []
    for phase, head in enumerate(forced):
        row = sorted({symbol(base, phase, low, high, digit)
                      for following, low, high, digit in first_rows(base, int(g[phase]), head)
                      if following == forced[(phase + 1) % period]})
        if not row:
            raise RuntimeError("cyclic head vertex has no cyclic successor")
        choices.append(row)
    metadata.update(heads=forced, choices_per_phase=list(map(len, choices)),
                    blocks_per_unit=prod(map(len, choices)))
    return positive_phase_product(base, e, g, choices), metadata


def render(candidate: Candidate) -> str:
    """Strict documented text interchange, with no supplied arithmetic tables."""
    accepted = [i for i, value in enumerate(candidate.accepting) if value]
    arcs = [(source, label, target) for source, row in enumerate(candidate.edges)
            for label, target in sorted(row.items())]
    lines = ["P196_EXTERIOR_INVARIANT 1", f"base {candidate.base}",
             f"period {len(candidate.g)}", f"e {candidate.e}", f"g {candidate.g}",
             f"states {len(candidate.edges)}", f"start {candidate.start}",
             "accept " + " ".join(map(str, [len(accepted), *accepted])),
             f"transitions {len(arcs)}"]
    lines.extend(f"{source} {label} {target}" for source, label, target in arcs)
    return "\n".join([*lines, "end", ""])


def words(candidate: Candidate, length: int) -> set[tuple[int, ...]]:
    frontier = {(candidate.start, ())}
    for _ in range(length):
        frontier = {(target, word + (label,)) for source, word in frontier
                    for label, target in candidate.edges[source].items()}
        if len(frontier) > 1000000:
            raise RuntimeError("fixture enumeration cap")
    return {word for state, word in frontier if candidate.accepting[state]}


def explicit_first_words(base: int, g: str, repetitions: int) -> set[tuple[int, ...]]:
    """Complete finite temporal paths, without SCC/forced-head simplification."""
    output = set()
    period, length = len(g), len(g) * repetitions
    for initial in range(1, 2 * base - 1):
        frontier = {(initial, ())}
        for position in range(length):
            phase = position % period
            following = set()
            for head, word in frontier:
                for target, low, high, digit in first_rows(base, int(g[phase]), head):
                    following.add((target, word + (symbol(base, phase, low, high, digit),)))
            frontier = following
            if len(frontier) > 1000000:
                raise RuntimeError("explicit FIRST enumeration cap")
        output.update(word for final, word in frontier if final == initial)
    return output


def selftest():
    graph_cases = fixtures = comparisons = total_words = inconclusive = 0
    for base in range(2, 7):
        for period in range(1, 5):
            for bits in product("01", repeat=period):
                g = "".join(bits)
                if "1" not in g:
                    continue
                graph, cyclic = head_graph(base, g)
                # Independent positive-length reachability criterion for each
                # vertex, with no SCC algorithm or bounded path-length guess.
                expected = set()
                for source in range(len(graph)):
                    seen, todo = set(), deque(graph[source])
                    while todo:
                        vertex = todo.popleft()
                        if vertex == source:
                            expected.add(source)
                            break
                        if vertex in seen:
                            continue
                        seen.add(vertex)
                        todo.extend(graph[vertex] - seen)
                if cyclic != expected:
                    raise RuntimeError("head SCC/reachability mismatch")
                graph_cases += 1
                try:
                    candidate, _ = first_candidate(base, "0" * period, g)
                except ValueError as error:
                    if "multiple cyclic heads" not in str(error):
                        raise
                    inconclusive += 1
                    continue
                fixtures += 1
                for repetitions in (1, 2):
                    actual = words(candidate, period * repetitions)
                    expected_words = explicit_first_words(base, g, repetitions)
                    if actual != expected_words:
                        raise RuntimeError("forced-head FIRST language mismatch")
                    comparisons += 1
                    total_words += len(actual)
    target, metadata = first_candidate(10, TARGET_E, TARGET_G)
    if tuple(metadata["heads"]) != TARGET_HEADS or metadata["blocks_per_unit"] != 64:
        raise RuntimeError("priority FIRST control differs from credited106/115")
    for repetitions in (1, 2):
        actual = words(target, len(TARGET_G) * repetitions)
        if actual != explicit_first_words(10, TARGET_G, repetitions):
            raise RuntimeError("priority complete FIRST mismatch")
        if len(actual) != 64 ** repetitions:
            raise RuntimeError("mixed-block FIRST count mismatch")
        comparisons += 1
        total_words += len(actual)
    return {"graph_cases": graph_cases, "exact_first_fixtures": fixtures,
            "unsupported_multiple_head_cases": inconclusive,
            "complete_word_set_comparisons": comparisons, "compared_words": total_words,
            "priority_first": metadata}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--kind", choices=("first", "empty", "universal"), default="first")
    parser.add_argument("--base", type=int, default=10)
    parser.add_argument("--e", default=TARGET_E)
    parser.add_argument("--g", default=TARGET_G)
    args = parser.parse_args()
    if args.selftest:
        print("FIRST_LANGUAGE_CONTROLS " + json.dumps(selftest(), sort_keys=True))
    if args.output:
        if args.kind == "first":
            candidate, metadata = first_candidate(args.base, args.e, args.g)
        else:
            candidate = (empty_candidate if args.kind == "empty" else universal_candidate)(
                args.base, args.e, args.g)
            metadata = {"kind": args.kind}
        args.output.write_text(render(candidate))
        print(json.dumps({"path": str(args.output), "states": len(candidate.edges),
                          "arcs": sum(map(len, candidate.edges)), **metadata}, sort_keys=True))
    if not args.selftest and not args.output:
        parser.error("provide --selftest or --output")


if __name__ == "__main__":
    main()
