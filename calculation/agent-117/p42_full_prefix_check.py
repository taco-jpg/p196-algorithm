#!/usr/bin/env python3
"""Independent full-Cartesian check of the repeated-G prefix obstruction.

Construct the complete width-1/2/3 phase graphs without using shorter
prefix survivors.  Local edges use whole-integer normalization, independently
of the digit-carry graph in p42_prefix_audit.  Compare the complete surviving
vertex AND edge sets after two separate source/sink deletion passes.
Then jump directly two columns beyond that independently obtained core,
without the primary algorithm's intermediate pruning, and topologically sort.

The base-6 positive control has a four-step B orbit but a two-step driver:
this explicitly checks that the phase graph retains multiple-lap cycles.
Counterexample attribution: Agent105, issue289 comment6433504667.
"""

import argparse
from collections import deque
import itertools
import json
import signal
import time

import p42_prefix_audit as primary


class Incomplete(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def integer_relation(base, word):
    """All inward carries via two ordinary integer divisions."""
    n = len(word)
    modulus = base ** n
    low_value = sum(x * base ** i for i, x in enumerate(word))
    reverse_value = sum(x * base ** (n - 1 - i) for i, x in enumerate(word))
    low = [(low_value // base ** i) % base for i in range(n)]
    output = set()
    for inward in (0, 1):
        value = reverse_value + inward
        overflow = value // modulus
        reverse_digits = [(value // base ** (n - 1 - i)) % base for i in range(n)]
        shifted = [1] + reverse_digits[:-1] if overflow else reverse_digits
        output.add((overflow, tuple(a + b for a, b in zip(low, shifted))))
    return output


def full_graph(base, g, width, cap):
    count = len(g) * (2 * base - 2) * (2 * base - 1) ** (width - 1)
    if count > cap:
        raise Incomplete("full Cartesian graph exceeds explicit state cap")
    words = [(head,) + tail for head in range(1, 2 * base - 1)
             for tail in itertools.product(range(2 * base - 1), repeat=width - 1)]
    word_id = {word: i for i, word in enumerate(words)}
    w = len(words)
    options = [{bit: sorted({word_id[target] for overflow, target in integer_relation(base, word)
                             if overflow == bit and target in word_id}) for bit in (0, 1)}
               for word in words]
    out = [[] for _ in range(count)]
    incoming = [[] for _ in range(count)]
    for phase, bit in enumerate(g):
        target_offset = ((phase + 1) % len(g)) * w
        for i in range(w):
            source = phase * w + i
            out[source] = [target_offset + j for j in options[i][bit]]
            for target in out[source]:
                incoming[target].append(source)
    # First remove every vertex with no predecessor, then every live sink.
    # Removing a live sink cannot reduce the indegree of a remaining vertex.
    alive = bytearray([1]) * count
    degrees = list(map(len, incoming))
    queue = deque(i for i, degree in enumerate(degrees) if degree == 0)
    while queue:
        i = queue.popleft()
        if not alive[i]:
            continue
        alive[i] = 0
        for j in out[i]:
            degrees[j] -= 1
            if alive[j] and degrees[j] == 0:
                queue.append(j)
    degrees = [sum(alive[j] for j in row) for row in out]
    queue = deque(i for i, degree in enumerate(degrees) if alive[i] and degree == 0)
    while queue:
        i = queue.popleft()
        if not alive[i]:
            continue
        alive[i] = 0
        for j in incoming[i]:
            degrees[j] -= 1
            if alive[j] and degrees[j] == 0:
                queue.append(j)
    key = lambda i: (i // w, words[i % w])
    vertices = {key(i) for i in range(count) if alive[i]}
    edges = {(key(i), key(j)) for i in range(count) if alive[i] for j in out[i] if alive[j]}
    return vertices, edges, {"width": width, "full_states": count,
                            "full_arcs": sum(map(len, out)),
                            "survivors": len(vertices), "surviving_arcs": len(edges)}


def compare(base, g, max_width, cap):
    previous = None
    records = []
    for width in range(1, max_width + 1):
        vertices, edges, record = full_graph(base, g, width, cap)
        previous, _ = primary.graph_layer(base, g, previous, width, cap)
        primary_edges = {((t, word), ((t + 1) % len(g), target))
                         for t, word in previous
                         for overflow, target in primary.projected(base, word)
                         if overflow == g[t] and ((t + 1) % len(g), target) in previous}
        require(vertices == previous, "full/pruned surviving vertex sets differ")
        require(edges == primary_edges, "full/pruned surviving edge sets differ")
        record["exact_vertex_edge_comparison"] = "PASS"
        records.append(record)
    return records, vertices


def two_column_lift(base, g, previous, cap):
    """Skip the primary intermediate core; delete sources only."""
    if len(previous) * (2 * base - 1) ** 2 > cap:
        raise Incomplete("two-column lift exceeds state cap")
    keys = [(phase, word + tail) for phase, word in sorted(previous)
            for tail in itertools.product(range(2 * base - 1), repeat=2)]
    ids = {key: i for i, key in enumerate(keys)}
    out, indegree = [[] for _ in keys], [0] * len(keys)
    for i, (phase, word) in enumerate(keys):
        for overflow, target in integer_relation(base, word):
            if overflow != g[phase]:
                continue
            j = ids.get(((phase + 1) % len(g), target))
            if j is not None:
                out[i].append(j)
                indegree[j] += 1
    queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
    removed = 0
    distance = [0] * len(keys)
    while queue:
        i = queue.popleft()
        removed += 1
        for j in out[i]:
            distance[j] = max(distance[j], distance[i] + 1)
            indegree[j] -= 1
            if indegree[j] == 0:
                queue.append(j)
    result = {"candidate_states": len(keys), "arcs": sum(map(len, out)),
              "removed": removed, "remaining": len(keys) - removed,
              "domain": "two-column extensions of independent complete-graph core"}
    if removed == len(keys):
        result["status"] = "ACYCLIC"
        result["longest_path_in_this_domain"] = max(distance, default=0)
    else:
        result["status"] = "UNDECIDED"
    return result


def multiple_lap_control():
    base, g = 6, (0, 1)
    words = [[4, 7, 7, 8, 3], [9, 3, 4, 5, 8],
             [4, 7, 7, 10, 2, 2], [9, 3, 4, 9]]
    trims = (0, 0, 2, 0)
    # A distinct whole-integer exterior oracle checks the actual four edges.
    from fixed_driver_verify import exterior_raw
    for t, word in enumerate(words):
        raw = exterior_raw(base, word, t % 2, t % 2)
        require(raw == words[(t + 1) % 4] + [5] * trims[t], "base6 cycle arithmetic")
    checks = 0
    for width in (1, 2, 3, 4):
        vertices, edges, _ = full_graph(base, g, width, 100000)
        projected_orbit = [(t % 2, tuple(word[:width])) for t, word in enumerate(words)]
        if width == 4:
            require(len(set(projected_orbit)) == 4,
                    "the positive control must remain a genuine two-lap projected orbit")
        for t, word in enumerate(words):
            source = (t % 2, tuple(word[:width]))
            target = ((t + 1) % 2, tuple(words[(t + 1) % 4][:width]))
            require(source in vertices and (source, target) in edges,
                    "multiple-lap positive cycle was lost")
            checks += 1
    return {"base": base, "driver_period": 2, "actual_cycle_period": 4,
            "primitive_projected_period_at_width4": 4,
            "integer_edges": 4, "preserved_prefix_edges": checks, "status": "PASS"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--g", default=primary.G_UNIT)
    parser.add_argument("--base", type=int, default=10)
    parser.add_argument("--width", type=int, default=3)
    parser.add_argument("--states", type=int, default=1000000)
    parser.add_argument("--seconds", type=int, default=120)
    args = parser.parse_args()
    if (not args.g or any(x not in "01" for x in args.g) or not 2 <= args.base <= 62
            or not 1 <= args.width <= 3 or not 1 <= args.states <= 1000000
            or not 1 <= args.seconds <= 1200):
        parser.error("invalid input or unsupported explicit audit domain")
    def timeout(*_):
        raise TimeoutError("full-prefix audit time cap")
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(args.seconds)
    start = time.monotonic()
    try:
        driver = tuple(map(int, args.g))
        records, vertices = compare(args.base, driver, args.width, args.states)
        lift = two_column_lift(args.base, driver, vertices, args.states)
        print(json.dumps({"comparison": records, "two_column_lift": lift,
                          "multiple_lap_control": multiple_lap_control(),
                          "status": "PASS", "elapsed_seconds": time.monotonic() - start}, sort_keys=True))
    except (Incomplete, MemoryError, TimeoutError) as error:
        print(json.dumps({"status": "UNDECIDED", "reason": str(error)}))
        return 2
    finally:
        signal.alarm(0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
