#!/usr/bin/env python3
"""Exact decimal central-window abstraction at an explicitly bounded radius.

At radius R, O records a symmetric central word of length 2R+1, with even
middle coefficient. E records length 2R+2. All coefficients are in 0..18.
There are 29*19**R states, covering every ordinary positive integer of width
at least 2R+1. No upper bound is imposed on the width of a compatible integer.

Every edge has an explicit integer realization. For no-overflow odd inputs,
normalize the window from either carry. For overflowing odd inputs, add one
mirrored neighboring coefficient z and normalize (z,window,z). For even
inputs, normalize the window from either carry and choose either overflow.
Fixtures are (v,u,window,u,v), or (v,u,z,window,z,u,v) for odd overflow, with
v=1+9*g and u=10*c. The exterior forces precisely the chosen carry/overflow.
The minimum odd width is included by virtual z=0 and incoming carry 0.

The exact universal next-step safety predicate is: some window coefficient
is >=10 and some coefficient is outside {0,11}. Unsafe windows have explicit
palindrome-producing completions. Reverse reachability from all unsafe
states computes the greatest safe subset closed under EVERY compatible edge.

This is a universal-completion obstruction, not an individual-orbit bound.
Successive abstract edges can use different integer completions. No decimal
Lychrel existence or nonexistence claim follows from an empty invariant.

All tests remain active under python -O. State, edge, memory and elapsed-time
guards fail as UNDECIDED. Default limits cover only radii 0 through 3.
No generated output files are written by this program.
"""

from __future__ import annotations

import argparse
from array import array
from collections import Counter
from dataclasses import dataclass
import json
import math
import resource
import sys
import time


UINT32_MAX = (1 << 32) - 1
INT32_MAX = (1 << 31) - 1


class LimitReached(RuntimeError):
    pass


def check(condition: bool, reason: str) -> None:
    if not condition:
        raise AssertionError(reason)


@dataclass
class Guard:
    seconds: float
    max_states: int
    max_edges: int
    start: float = 0.0

    def __post_init__(self) -> None:
        self.start = time.monotonic()

    def poll(self) -> None:
        if time.monotonic() - self.start > self.seconds:
            raise LimitReached(f"elapsed-time limit {self.seconds:g}s reached")


def set_memory_limit(mib: int) -> None:
    requested = mib * 1024 * 1024
    old_soft, old_hard = resource.getrlimit(resource.RLIMIT_AS)
    limit = requested
    if old_soft != resource.RLIM_INFINITY:
        limit = min(limit, old_soft)
    if old_hard != resource.RLIM_INFINITY:
        limit = min(limit, old_hard)
    resource.setrlimit(resource.RLIMIT_AS, (limit, old_hard))


def peak_mib() -> float:
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return rss / (1024 * 1024 if sys.platform == "darwin" else 1024)


def preflight_radius(radius: int, guard: Guard) -> int:
    """Reject oversized exponents before constructing Model or its power tables.

    Validated uint32 budgets make this loop take at most seven iterations,
    even if the supplied radius is an astronomically large Python integer.
    The signed rank/selected-target arrays impose an additional int32 bound.
    """
    guard.poll()
    limit = min(guard.max_states, INT32_MAX)
    states = 29
    if states > limit:
        raise LimitReached("the smallest model requires 29 states, exceeding the state budget")
    for admitted_radius in range(radius):
        if states > limit // 19:
            raise LimitReached(
                f"radius exceeds the state/representation budget; largest admissible radius is {admitted_radius}")
        states *= 19
    return states


class Model:
    def __init__(self, radius: int):
        check(radius >= 0, "radius must be nonnegative")
        self.radius = radius
        self.odd_count = 10 * 19**radius
        self.state_count = 29 * 19**radius
        self.powers10 = tuple(10**i for i in range(2 * radius + 8))

    def decode(self, state: int) -> tuple[bool, tuple[int, ...], tuple[int, ...]]:
        r = self.radius
        odd = state < self.odd_count
        if odd:
            code, m = divmod(state, 10)
            half = [0] * r + [2 * m]
            for j in range(r - 1, -1, -1):
                code, half[j] = divmod(code, 19)
            word = tuple(half + half[:-1][::-1])
        else:
            code = state - self.odd_count
            half = [0] * (r + 1)
            for j in range(r, -1, -1):
                code, half[j] = divmod(code, 19)
            word = tuple(half + half[::-1])
        return odd, tuple(half), word

    def label(self, state: int) -> str:
        odd, half, _ = self.decode(state)
        return ("O" if odd else "E") + "(" + ",".join(map(str, half)) + ")"

    def encode(self, odd: bool, half) -> int:
        value = 0
        if odd:
            for x in half[:-1]:
                value = 19 * value + x
            return 10 * value + half[-1] // 2
        for x in half:
            value = 19 * value + x
        return self.odd_count + value

    def abstract_integer(self, n: int) -> int:
        ds = tuple(map(int, str(n)[::-1]))
        width = len(ds)
        odd = bool(width % 2)
        needed = 2 * self.radius + (1 if odd else 2)
        check(width >= needed, "integer below the abstraction's minimum width")
        start = (width - needed) // 2
        half = [ds[i] + ds[width - 1 - i]
                for i in range(start, start + self.radius + 1)]
        return self.encode(odd, half)

    def realize(self, q: tuple[int, ...]) -> int:
        length = len(q)
        n = 0
        for i in range(length // 2):
            high = min(9, q[i])
            n += (q[i] - high) * self.powers10[i]
            n += high * self.powers10[length - 1 - i]
        if length % 2:
            n += (q[length // 2] // 2) * self.powers10[length // 2]
        return n

    @staticmethod
    def normalize(word, carry: int) -> tuple[int, ...]:
        out = []
        for coefficient in word:
            total = coefficient + carry
            out.append(total % 10)
            carry = total // 10
        return tuple(out)

    def successors(self, state: int, odd: bool, word: tuple[int, ...]):
        """Map every distinct target to one actual local control (g,c,z)."""
        r = self.radius
        targets: dict[int, tuple[int, int, int]] = {}
        if odd:
            for carry in (0, 1):
                ds = self.normalize(word, carry)
                half = [ds[j] + ds[2 * r - j] for j in range(r + 1)]
                targets.setdefault(self.encode(True, half), (0, carry, 0))
            for z in range(19):
                local = (z,) + word + (z,)
                for carry in (0, 1):
                    ds = self.normalize(local, carry)
                    half = [ds[j + 1] + ds[2 * r + 2 - j] for j in range(r + 1)]
                    targets.setdefault(self.encode(False, half), (1, carry, z))
        else:
            for carry in (0, 1):
                ds = self.normalize(word, carry)
                half = [ds[j] + ds[2 * r + 1 - j] for j in range(r + 1)]
                targets.setdefault(self.encode(False, half), (0, carry, 0))
                half = [ds[j + 1] + ds[2 * r + 1 - j] for j in range(r + 1)]
                targets.setdefault(self.encode(True, half), (1, carry, 0))
        return targets

    @staticmethod
    def safe(half: tuple[int, ...]) -> bool:
        return max(half) >= 10 and any(x not in (0, 11) for x in half)

    @staticmethod
    def fixture(odd: bool, word: tuple[int, ...], control) -> tuple[int, ...]:
        g, carry, z = control
        v, u = 1 + 9 * g, 10 * carry
        if odd and g:
            return (v, u, z) + word + (z, u, v)
        return (v, u) + word + (u, v)

    def verify_edge(self, state: int, target: int, odd: bool, word, control) -> None:
        q = self.fixture(odd, word, control)
        n = self.realize(q)
        ds = tuple(map(int, str(n)[::-1]))
        check(tuple(a + b for a, b in zip(ds, ds[::-1])) == q, "fixture realization mismatch")
        check(self.abstract_integer(n) == state, "fixture source mismatch")
        nxt = n + int(str(n)[::-1])
        check(self.abstract_integer(nxt) == target, "bigint edge mismatch")
        check(len(str(nxt)) - len(str(n)) == control[0], "fixture overflow mismatch")


def build(model: Model, guard: Guard):
    n = model.state_count
    if n > guard.max_states:
        raise LimitReached(f"{n} states exceed --max-states={guard.max_states}")
    offsets = array("I", [0])
    edges = array("I")
    safe = bytearray(n)
    edge_counts = Counter()
    fixture_checks = 0
    unsafe_checks = 0
    minimum_checks = 0
    for source in range(n):
        if source % 128 == 0:
            guard.poll()
        odd, half, word = model.decode(source)
        safe[source] = model.safe(half)
        targets = model.successors(source, odd, word)
        if len(edges) + len(targets) > guard.max_edges:
            raise LimitReached(f"edge count exceeds --max-edges={guard.max_edges}")
        for target in sorted(targets):
            check(0 <= target < n, "local target outside the state space")
            control = targets[target]
            model.verify_edge(source, target, odd, word, control)
            fixture_checks += 1
            edge_counts[("O" if odd else "E", control[0])] += 1
            edges.append(target)
        offsets.append(len(edges))
        if not safe[source]:
            v = 1 if max(half) <= 9 else 11
            n0 = model.realize((v,) + word + (v,))
            nxt = n0 + int(str(n0)[::-1])
            check(model.abstract_integer(n0) == source, "unsafe completion source mismatch")
            check(str(nxt) == str(nxt)[::-1], "unsafe completion did not make a palindrome")
            unsafe_checks += 1
        if word[0] > 0:
            n0 = model.realize(word)
            nxt = n0 + int(str(n0)[::-1])
            check(model.abstract_integer(n0) == source, "minimum-width source mismatch")
            check(model.abstract_integer(nxt) in targets, "missing minimum-width edge")
            minimum_checks += 1
    return offsets, edges, safe, edge_counts, {
        "distinct_edge_integer_fixtures": fixture_checks,
        "unsafe_palindrome_completions": unsafe_checks,
        "minimum_width_profiles": minimum_checks,
    }


def rank_graph(offsets, edges, safe, guard: Guard):
    """Reverse BFS computes shortest abstract distance to the unsafe states."""
    n = len(safe)
    counts = array("I", [0]) * n
    for j, target in enumerate(edges):
        counts[target] += 1
        if j % 65536 == 0:
            guard.poll()
    reverse_offsets = array("I", [0])
    total = 0
    for count in counts:
        total += count
        reverse_offsets.append(total)
    cursor = array("I", reverse_offsets[:-1])
    predecessors = array("I", [0]) * len(edges)
    for source in range(n):
        if source % 2048 == 0:
            guard.poll()
        for j in range(offsets[source], offsets[source + 1]):
            target = edges[j]
            predecessors[cursor[target]] = source
            cursor[target] += 1
    rank = array("i", [-1]) * n
    chosen = array("i", [-1]) * n
    queue = array("I")
    for s in range(n):
        if not safe[s]:
            rank[s] = 0
            queue.append(s)
    head = 0
    while head < len(queue):
        if head % 2048 == 0:
            guard.poll()
        target = queue[head]
        head += 1
        for j in range(reverse_offsets[target], reverse_offsets[target + 1]):
            source = predecessors[j]
            if rank[source] == -1:
                rank[source] = rank[target] + 1
                chosen[source] = target
                queue.append(source)
    rank_checks = 0
    invariant_checks = 0
    for source in range(n):
        if source % 2048 == 0:
            guard.poll()
        if rank[source] > 0:
            target = chosen[source]
            check(safe[source] and target in edges[offsets[source]:offsets[source + 1]],
                  "rank witness is not a legal edge")
            check(rank[target] + 1 == rank[source], "rank witness does not decrease by one")
            rank_checks += 1
        elif rank[source] == -1:
            check(bool(safe[source]), "unsafe state survived pruning")
            check(all(rank[edges[j]] == -1 for j in range(offsets[source], offsets[source + 1])),
                  "surviving safe set is not universally closed")
            invariant_checks += 1
        else:
            check(not safe[source], "safe state incorrectly assigned rank zero")
    return rank, chosen, {"rank_witness_checks": rank_checks,
                          "surviving_invariant_state_checks": invariant_checks}


def summary_for_radius(radius: int, guard: Guard):
    started = time.monotonic()
    expected_states = preflight_radius(radius, guard)
    model = Model(radius)
    check(model.state_count == expected_states, "preflight state count mismatch")
    offsets, edges, safe, edge_counts, checks = build(model, guard)
    graph_seconds = time.monotonic() - started
    rank, chosen, rank_checks = rank_graph(offsets, edges, safe, guard)
    checks.update(rank_checks)
    histogram = Counter(rank)
    invariant_size = histogram.pop(-1, 0)
    max_rank = max(histogram)
    remaining = sum(safe)
    rounds = [remaining]
    by_parity = []
    for step in range(max_rank + 1):
        if step:
            remaining -= histogram.get(step, 0)
            rounds.append(remaining)
        odd = sum(rank[s] == -1 or rank[s] > step for s in range(model.odd_count))
        by_parity.append({"round": step, "odd": odd, "even": remaining - odd})
    max_states = [s for s in range(model.state_count) if rank[s] == max_rank]
    chain = []
    if max_states:
        current = max_states[0]
        while rank[current] > 0:
            odd, _, word = model.decode(current)
            target = chosen[current]
            control = model.successors(current, odd, word)[target]
            seed = model.realize(model.fixture(odd, word, control))
            chain.append({"source": model.label(current), "rank": rank[current],
                          "target": model.label(target), "target_rank": rank[target],
                          "control_g_c_z": control, "seed": seed,
                          "next_integer": seed + int(str(seed)[::-1])})
            current = target
    return {
        "status": "COMPUTED_COMPLETE", "radius": radius,
        "window_lengths": [2 * radius + 1, 2 * radius + 2],
        "states": model.state_count, "odd_states": model.odd_count,
        "even_states": model.state_count - model.odd_count,
        "labelled_edges": len(edges),
        "edges_by_source_and_overflow": {
            f"{parity},g={g}": value for (parity, g), value in sorted(edge_counts.items())},
        "safe_set_sizes": rounds, "safe_sets_by_parity": by_parity,
        "greatest_universally_safe_invariant_size": invariant_size,
        "rank_histogram": dict(sorted(histogram.items())), "max_rank": max_rank,
        "max_rank_state_count": len(max_states),
        "max_rank_state_samples": [model.label(s) for s in max_states[:40]],
        "one_abstract_escape_chain_with_different_completions": chain,
        "checks": checks, "graph_seconds": round(graph_seconds, 6),
        "total_seconds": round(time.monotonic() - started, 6), "peak_mib": round(peak_mib(), 3),
        "scope": "Universal closure over compatible completions only; no individual-orbit or Lychrel no-go.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--radius", type=int, nargs="+", default=[0, 1, 2, 3])
    parser.add_argument("--seconds", type=float, default=1100.0)
    parser.add_argument("--memory-mib", type=int, default=6144)
    parser.add_argument("--max-states", type=int, default=300000)
    parser.add_argument("--max-edges", type=int, default=8000000)
    parser.add_argument("--json", action="store_true", help="include detailed deterministic count/rank data")
    args = parser.parse_args()
    if any(r < 0 for r in args.radius) or not math.isfinite(args.seconds) or args.seconds <= 0 or args.memory_mib <= 0:
        parser.error("radii must be nonnegative and elapsed/memory limits finite and positive")
    if not 1 <= args.max_states <= UINT32_MAX or not 1 <= args.max_edges <= UINT32_MAX:
        parser.error("state and edge caps must be positive uint32 values (1..4294967295)")
    if array("I").itemsize != 4 or array("i").itemsize != 4:
        parser.error("this implementation requires 32-bit array('I') and array('i') elements")
    set_memory_limit(args.memory_mib)
    guard = Guard(args.seconds, args.max_states, args.max_edges)
    completed = []
    try:
        for radius in args.radius:
            result = summary_for_radius(radius, guard)
            completed.append(result)
            if not args.json:
                print(f"R={radius} states={result['states']} odd={result['odd_states']} even={result['even_states']} labelled_edges={result['labelled_edges']}")
                print(f"edges_by_source_g={result['edges_by_source_and_overflow']}")
                print(f"safe_set_sizes={result['safe_set_sizes']} invariant_size={result['greatest_universally_safe_invariant_size']}")
                print(f"rank_histogram={result['rank_histogram']} max_rank={result['max_rank']} max_rank_states={result['max_rank_state_count']}")
                print(" ".join(f"{key}={value}" for key, value in result["checks"].items()))
                print(f"elapsed_seconds={result['total_seconds']} peak_mib={result['peak_mib']}")
                print("ALL CHECKS PASSED; universal-completion abstraction only.", flush=True)
        if args.json:
            print(json.dumps(completed, indent=2, sort_keys=True))
        return 0
    except (LimitReached, MemoryError) as exc:
        print(json.dumps({"status": "UNDECIDED", "reason": str(exc) or "memory limit reached",
                          "completed_radii": [x["radius"] for x in completed]}), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
