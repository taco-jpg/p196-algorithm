#!/usr/bin/env python3
"""Exact necessary exterior-prefix graphs for a repeated overflow driver.

The phase graph allows ANY positive number of driver laps.  Its inward
reverse carry is free at each edge; the terminal e stream is not imposed.
Neutral suffix padding projects every finite exterior cycle into each
prefix graph.  Iterative indegree/outdegree deletion preserves all cycles.

Run the scoped decimal search: python3 calculation/agent-117/p42_prefix_audit.py
Independent arithmetic/positive controls: add --selftest.
Credits: Agent6's prefix projection and #367 fixed-itinerary obstruction;
Agent7/114 neutral suffix padding.  No prefix trace is assumed in advance.
"""

import argparse
from collections import deque
import itertools
import json
from pathlib import Path
import random
import signal
import sys
import time

from exterior_inverse_audit import norm, raw_exterior


G_UNIT = "101000101001001010100"


def require(value, message):
    if not value:
        raise AssertionError(message)


class Incomplete(Exception):
    pass


def projected(base, word):
    """Digit-carry relation; all unresolved inward carry choices retained."""
    result = set()
    width = len(word)
    for inward in (0, 1):
        right = [0] * (width + 1)
        right[width] = inward
        for j in range(width - 1, -1, -1):
            right[j] = (word[j] + right[j + 1]) // base
        overflow = right[0]
        lower, carry = [], 0
        for coefficient in word:
            lower.append((coefficient + carry) % base)
            carry = (coefficient + carry) // base
        upper = [(word[j] + right[j + 1]) % base for j in range(width)]
        target = tuple(lower[j] + (1 if j == 0 else upper[j - 1])
                       if overflow else lower[j] + upper[j] for j in range(width))
        result.add((overflow, target))
    return result


def pad_prefix(base, word, width):
    return tuple((list(word) + [base - 1] * width)[:width])


def graph_layer(base, driver, previous, width, state_cap):
    if width == 1:
        if len(driver) * (2 * base - 2) > state_cap:
            raise Incomplete("candidate-state cap")
        keys = [(t, (x,)) for t in range(len(driver)) for x in range(1, 2 * base - 1)]
    else:
        if len(previous) * (2 * base - 1) > state_cap:
            raise Incomplete("candidate-state cap")
        keys = [(t, word + (x,)) for t, word in sorted(previous)
                for x in range(2 * base - 1)]
    if len(keys) > state_cap:
        raise Incomplete("candidate-state cap")
    ids = {key: i for i, key in enumerate(keys)}
    adjacency, reverse = [[] for _ in keys], [[] for _ in keys]
    for i, (phase, word) in enumerate(keys):
        for overflow, target in projected(base, word):
            if overflow != driver[phase]:
                continue
            j = ids.get(((phase + 1) % len(driver), target))
            if j is not None and j not in adjacency[i]:
                adjacency[i].append(j)
                reverse[j].append(i)
    indegree, outdegree = list(map(len, reverse)), list(map(len, adjacency))
    queue = deque(i for i in range(len(keys)) if not indegree[i] or not outdegree[i])
    alive = bytearray([1]) * len(keys)
    while queue:
        i = queue.popleft()
        if not alive[i]:
            continue
        alive[i] = 0
        for j in adjacency[i]:
            if alive[j]:
                indegree[j] -= 1
                if not indegree[j]:
                    queue.append(j)
        for j in reverse[i]:
            if alive[j]:
                outdegree[j] -= 1
                if not outdegree[j]:
                    queue.append(j)
    survivors = {keys[i] for i in range(len(keys)) if alive[i]}
    counts = [sum(phase == t for phase, _ in survivors) for t in range(len(driver))]
    record = {"width": width, "candidate_states": len(keys),
              "unique_arcs": sum(map(len, adjacency)), "survivors": len(survivors),
              "surviving_arcs": sum(sum(alive[j] for j in adjacency[i])
                                    for i in range(len(keys)) if alive[i]),
              "survivors_per_phase": counts,
              "domain": "all positive heads" if width == 1 else "extensions of previous bicore"}
    if counts and all(count == 1 for count in counts):
        record["forced_prefixes"] = [list(next(word for phase, word in survivors if phase == t))
                                     for t in range(len(driver))]
    if not survivors:
        # All vertices of THIS layer's candidate graph, including peeled ones.
        indegree = list(map(len, reverse))
        queue = deque(i for i, degree in enumerate(indegree) if not degree)
        distance, removed = [0] * len(keys), 0
        while queue:
            i = queue.popleft()
            removed += 1
            for j in adjacency[i]:
                distance[j] = max(distance[j], distance[i] + 1)
                indegree[j] -= 1
                if not indegree[j]:
                    queue.append(j)
        require(removed == len(keys), "empty bicore disagrees with topological traversal")
        record["longest_path_edges_in_candidate_graph"] = max(distance, default=0)
        record["path_scope"] = "this lifted candidate graph only; no unrestricted trajectory bound"
    return survivors, record


def arithmetic_controls():
    table_rows = projections = trimmed = 0
    for base in (2, 3, 4, 10):
        for width in range(1, 4):
            for word in itertools.product(range(2 * base - 1), repeat=width):
                expected = set()
                for inward in (0, 1):
                    low, _ = norm(base, word, 0)
                    right, overflow = norm(base, word[::-1], inward)
                    upper = right[::-1]
                    if overflow:
                        upper = [1] + upper[:-1]
                    expected.add((overflow, tuple(a + b for a, b in zip(low, upper))))
                require(projected(base, word) == expected, "independent integer local relation")
                table_rows += 1
    words = [list(word) for width in range(4)
             for word in itertools.product(range(19), repeat=width)
             if not word or word[0]]
    rng = random.Random(11742)
    for _ in range(1000):
        width = rng.randrange(4, 40)
        words.append([rng.randrange(1, 19)] + [rng.randrange(19) for _ in range(width - 1)])
    for word in words:
        raw, _, overflow = raw_exterior(10, word)
        for trim in range(len(raw) + 1):
            if trim and raw[-trim] != 9:
                break
            target = raw[:len(raw) - trim] if trim else raw
            for width in range(1, 7):
                require((overflow, pad_prefix(10, target, width))
                        in projected(10, pad_prefix(10, word, width)),
                        "whole exterior/neutral-trim projection")
                projections += 1
            trimmed += 1
    return {"local_integer_relation_words": table_rows, "whole_exterior_words": len(words),
            "legal_trim_cases": trimmed, "whole_exterior_prefix_checks": projections}


def positive_controls(state_cap):
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root / "calculation"))
    from neutral_band_search import _lean_certs  # Fixtures only.
    fixtures, checks = [], 0
    for base, edges in sorted(_lean_certs()):
        words = [edge[0] for edge in edges]
        driver = tuple(raw_exterior(base, word)[2] for word in words)
        previous = None
        for width in (1, 2):
            previous, record = graph_layer(base, driver, previous, width, state_cap)
            for phase, word in enumerate(words):
                key = phase, pad_prefix(base, word, width)
                require(key in previous, "peeling lost a known positive cycle vertex")
                target = pad_prefix(base, words[(phase + 1) % len(words)], width)
                require((driver[phase], target) in projected(base, key[1]),
                        "known positive prefix edge missing")
                checks += 1
        fixtures.append([base, len(edges)])
    require([base for base, _ in fixtures] == [2, 4, 8, 11, 16, 17, 26, 32], "positive fixtures")
    return {"fixtures": fixtures, "positive_graph_vertex_edge_checks": checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--g", default=G_UNIT)
    parser.add_argument("--base", type=int, default=10)
    parser.add_argument("--max-width", type=int, default=6)
    parser.add_argument("--states", type=int, default=500000)
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if (not args.g or any(c not in "01" for c in args.g) or not 2 <= args.base <= 62
            or not 1 <= args.max_width <= 64 or not 1 <= args.states <= 1000000
            or not 1 <= args.seconds <= 1200):
        parser.error("invalid driver/base or unsupported resource bound")
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(Incomplete("wall-clock limit")))
    signal.alarm(args.seconds)
    start = time.monotonic()
    try:
        if args.selftest:
            print(json.dumps({"arithmetic_controls": arithmetic_controls()}, sort_keys=True), flush=True)
            print(json.dumps({"positive_controls": positive_controls(args.states)}, sort_keys=True), flush=True)
        previous = None
        driver = tuple(map(int, args.g))
        for width in range(1, args.max_width + 1):
            previous, record = graph_layer(args.base, driver, previous, width, args.states)
            print(json.dumps(record, sort_keys=True), flush=True)
            if not previous:
                print(json.dumps({"status": "ACYCLIC_PREFIX_OBSTRUCTION", "base": args.base,
                                  "g_unit": args.g, "width": width,
                                  "scope": "every positive repetition, arbitrary finite exterior width/natural trim",
                                  "elapsed_seconds": time.monotonic() - start}, sort_keys=True))
                return 0
        print(json.dumps({"status": "UNDECIDED", "reason": "surviving prefix relaxation",
                          "tested_width": args.max_width, "elapsed_seconds": time.monotonic() - start}))
        return 2
    except (Incomplete, MemoryError) as exc:
        print(json.dumps({"status": "UNDECIDED", "reason": str(exc) or "memory limit",
                          "elapsed_seconds": time.monotonic() - start}))
        return 2
    finally:
        signal.alarm(0)


if __name__ == "__main__":
    raise SystemExit(main())
