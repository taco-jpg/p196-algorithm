#!/usr/bin/env python3
"""Independent exact central-window graph for decimal reverse-and-add.

Agent 115, T1.central-window5-8-safety. No repository modules are imported.
At radius R an odd window has 2R+1 coefficients and an even window 2R+2.
All local carry choices are checked with ordinary positive integer fixtures.
The greatest universally closed safe subset is computed by reverse BFS from
unsafe states, rather than by repeatedly pruning the live subset.

This is a universal-completion abstraction. An abstract path can combine
incompatible integer completions; empty closure does not exclude an actual
infinite safe orbit.

Reproduce:
    python3 calculation/agent-115/central_window_radius_independent.py --radii 0 1 2 3
"""

import argparse
from array import array
from collections import Counter
from itertools import product
import json
import resource
import sys
import time


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def normalize(word, c):
    ds = []
    for x in word:
        ds.append((x + c) % 10)
        c = (x + c) // 10
    return tuple(ds), c


def integer_from_fold(q):
    require(q and q[0] > 0 and q == q[::-1], "invalid positive symmetric fold")
    require(all(0 <= x <= 18 for x in q), "fold coefficient outside range")
    n = len(q)
    ds = [0] * n
    for i in range(n // 2):
        ds[n - 1 - i] = min(q[i], 9)
        ds[i] = q[i] - ds[n - 1 - i]
    if n % 2:
        require(q[n // 2] % 2 == 0, "odd middle coefficient")
        ds[n // 2] = q[n // 2] // 2
    return sum(d * 10**i for i, d in enumerate(ds))


def folded_integer(n):
    ds = tuple(map(int, str(n)[::-1]))
    return tuple(a + b for a, b in zip(ds, ds[::-1]))


def successor_integer(n):
    return n + int(str(n)[::-1])


class Model:
    def __init__(self, radius):
        self.r = radius
        self.odd_count = 10 * 19**radius
        self.count = 29 * 19**radius

    def half_from_id(self, state):
        if state < self.odd_count:
            code, center = divmod(state, 10)
            tail = [2 * center]
            length = self.r
            odd = True
        else:
            code = state - self.odd_count
            tail = []
            length = self.r + 1
            odd = False
        digits = [0] * length
        for i in range(length - 1, -1, -1):
            code, digits[i] = divmod(code, 19)
        require(code == 0, "state decode overflow")
        return odd, tuple(digits + tail)

    def state_id(self, odd, half):
        require(len(half) == self.r + 1, "wrong half width")
        require(all(0 <= x <= 18 for x in half), "invalid target coefficient")
        code = 0
        for x in half[:-1] if odd else half:
            code = code * 19 + x
        if odd:
            require(half[-1] % 2 == 0, "invalid odd target center")
            return 10 * code + half[-1] // 2
        return self.odd_count + code

    def state_of_fold(self, q):
        odd = len(q) % 2 == 1
        m = len(q) // 2
        start = m - self.r if odd else m - self.r - 1
        require(start >= 0, "integer below the window domain")
        return self.state_id(odd, q[start:start + self.r + 1])

    @staticmethod
    def window(odd, half):
        return half + (half[:-1] if odd else half)[::-1]

    @staticmethod
    def safe(half):
        return max(half) >= 10 and any(x not in (0, 11) for x in half)

    def choices(self, odd, half):
        """Yield target state and a fully realizable folded input word."""
        w = self.window(odd, half)
        if odd:
            # No overflow: pair the entire normalized odd window.
            for c in (0, 1):
                ds, _ = normalize(w, c)
                out = tuple(ds[i] + ds[-1 - i] for i in range(self.r + 1))
                q = (1, 10 * c) + w + (10 * c, 1)
                yield self.state_id(True, out), q, 0
            # Overflow: one extra digit enters on the right. Its old folded
            # coefficient z is also the mirrored coefficient just left of w;
            # therefore the entering carry is forced to (z+k)//10.
            for z, k in product(range(19), (0, 1)):
                c = (z + k) // 10
                ds, h = normalize(w, c)
                extended = ds + ((z + h) % 10,)
                out = tuple(extended[i] + extended[-1 - i] for i in range(self.r + 1))
                q = (10, 10 * k, z) + w + (z, 10 * k, 10)
                yield self.state_id(False, out), q, 1
        else:
            for c, g in product((0, 1), repeat=2):
                ds, _ = normalize(w, c)
                # Overflow shifts the center right by half a position, so
                # the new odd window uses the normalized digits ds[1:].
                selected = ds[1:] if g else ds
                out = tuple(selected[i] + selected[-1 - i] for i in range(self.r + 1))
                v = 10 if g else 1
                q = (v, 10 * c) + w + (10 * c, v)
                yield self.state_id(bool(g), out), q, g


def analyze(radius):
    started = time.perf_counter()
    model = Model(radius)
    offsets = array("I", [0])
    adjacency = array("I")
    safe = bytearray(model.count)
    reverse_counts = array("I", [0]) * model.count
    edge_types = Counter()
    fixture_count = 0
    unsafe_checks = 0
    minimum_width_checks = 0

    for state in range(model.count):
        odd, half = model.half_from_id(state)
        safe[state] = model.safe(half)
        targets = set()
        for target, q, g in model.choices(odd, half):
            n = integer_from_fold(q)
            require(folded_integer(n) == q, "fixture realization mismatch")
            require(model.state_of_fold(q) == state, "fixture source mismatch")
            out = successor_integer(n)
            require(model.state_of_fold(folded_integer(out)) == target, "integer successor mismatch")
            require(len(str(out)) - len(str(n)) == g, "fixture overflow mismatch")
            if safe[state]:
                require(str(out) != str(out)[::-1], "safe fixture has palindromic successor")
            targets.add(target)
            fixture_count += 1
        require(targets, "source has no successors")
        for target in sorted(targets):
            adjacency.append(target)
            reverse_counts[target] += 1
            edge_types[("O" if odd else "E", "O" if target < model.odd_count else "E")] += 1
        offsets.append(len(adjacency))

        # Every valid folded word at either minimum width is represented by
        # exactly one half-word. Width-one zero is not a positive input.
        w = model.window(odd, half)
        if w[0] > 0:
            n = integer_from_fold(w)
            actual = model.state_of_fold(folded_integer(successor_integer(n)))
            require(actual in targets, "minimum-width edge missing")
            minimum_width_checks += 1

        if not safe[state]:
            v = 1 if max(half) <= 9 else 11
            q = (v,) + w + (v,)
            n = integer_from_fold(q)
            out = successor_integer(n)
            require(model.state_of_fold(folded_integer(n)) == state, "unsafe completion source mismatch")
            require(str(out) == str(out)[::-1], "unsafe completion is not a palindrome")
            unsafe_checks += 1

    # Construct a compact reverse graph, then find shortest distance to an
    # unsafe state. This is exactly the removal rank for universal closure.
    reverse_offsets = array("I", [0])
    for count in reverse_counts:
        reverse_offsets.append(reverse_offsets[-1] + count)
    require(reverse_offsets[-1] == len(adjacency), "reverse edge total mismatch")
    reverse_edges = array("I", [0]) * len(adjacency)
    cursor = array("I", reverse_offsets[:-1])
    for source in range(model.count):
        for i in range(offsets[source], offsets[source + 1]):
            target = adjacency[i]
            reverse_edges[cursor[target]] = source
            cursor[target] += 1
    unseen = 65535
    rank = array("H", [unseen]) * model.count
    queue = array("I")
    for state in range(model.count):
        if not safe[state]:
            rank[state] = 0
            queue.append(state)
    head = 0
    while head < len(queue):
        target = queue[head]
        head += 1
        for i in range(reverse_offsets[target], reverse_offsets[target + 1]):
            source = reverse_edges[i]
            if rank[source] == unseen:
                require(rank[target] + 1 < unseen, "rank representation overflow")
                rank[source] = rank[target] + 1
                queue.append(source)

    histogram = Counter(rank)
    closed_count = histogram.pop(unseen, 0)
    safe_counts = [sum(safe)]
    for distance in range(1, max(histogram) + 1):
        safe_counts.append(safe_counts[-1] - histogram[distance])
    require(safe_counts[-1] == closed_count, "closure/rank total mismatch")
    for state in range(model.count):
        if safe[state]:
            minimum = min(rank[adjacency[i]] for i in range(offsets[state], offsets[state + 1]))
            if rank[state] == unseen:
                require(minimum == unseen, "claimed closed state has an escaping edge")
            else:
                require(rank[state] == minimum + 1, "shortest-escape rank equation fails")
        else:
            require(rank[state] == 0, "unsafe rank is not zero")

    last_rank = max(histogram)
    last_states = []
    if histogram[last_rank] <= 32:
        for state in range(model.count):
            if rank[state] == last_rank:
                odd, half = model.half_from_id(state)
                last_states.append(["O" if odd else "E", list(half)])
    max_rss_kib = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        max_rss_kib = (max_rss_kib + 1023) // 1024
    return {
        "radius": radius,
        "odd_window_width": 2 * radius + 1,
        "even_window_width": 2 * radius + 2,
        "states": model.count,
        "odd_states": model.odd_count,
        "even_states": model.count - model.odd_count,
        "edges": len(adjacency),
        "edge_types": {a + "->" + b: count for (a, b), count in sorted(edge_types.items())},
        "integer_fixture_checks": fixture_count,
        "minimum_width_checks": minimum_width_checks,
        "unsafe_palindrome_checks": unsafe_checks,
        "safe_set_sizes": safe_counts,
        "closed_safe_states": closed_count,
        "rank_histogram": dict(sorted(histogram.items())),
        "max_rank": last_rank,
        "last_removed_states": last_states,
        "rank_equation_checks": model.count,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "max_rss_kib": max_rss_kib,
        "classification": "COMPUTED",
        "status": "ALL INDEPENDENT CHECKS PASSED",
        "scope": "Universal closure over compatible completions; no individual-orbit exclusion."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--radii", nargs="+", type=int, choices=range(4), default=[0, 1, 2, 3])
    args = parser.parse_args()
    for radius in args.radii:
        print(json.dumps(analyze(radius), sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
