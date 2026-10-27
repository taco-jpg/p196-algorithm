#!/usr/bin/env python3
"""Finite-prefix obstructions for decimal exterior cycles with overflow (1000)^G.

Each right boundary carry is independently relaxed to 0 or 1.  A cyclic
component in this graph is only a necessary condition, not a B-cycle.
"""
from __future__ import annotations

import argparse
import collections
import math
import time


def prefix_step(word: tuple[int, ...], incoming: int):
    """Exact low prefix update for a specified unknown inward boundary carry."""
    reverse = [0] * (len(word) + 1)
    reverse[-1] = incoming
    for i in range(len(word) - 1, -1, -1):
        reverse[i] = (word[i] + reverse[i + 1]) // 10
    overflow = reverse[0]
    low_carry = 0
    out = []
    for i, digit in enumerate(word):
        low = (digit + low_carry) % 10
        low_carry = (digit + low_carry) // 10
        if not overflow:
            partner = (digit + reverse[i + 1]) % 10
        elif i == 0:
            partner = 1
        else:
            partner = (word[i - 1] + reverse[i]) % 10
        out.append(low + partner)
    return overflow, tuple(out)


def block_successors(word: tuple[int, ...]):
    states = {word}
    for overflow, head in zip((1, 0, 0, 0), (1, 2, 5, 10)):
        nxt = set()
        for state in states:
            for carry in (0, 1):
                got, target = prefix_step(state, carry)
                if got == overflow and target[0] == head:
                    nxt.add(target)
        states = nxt
    return states


def cyclic_components(adj):
    """Iterative Kosaraju: avoid recursion limits on genuinely large graphs."""
    rev = {u: [] for u in adj}
    for u, vs in adj.items():
        for v in vs:
            rev[v].append(u)
    seen, order = set(), []
    for root in adj:
        if root in seen:
            continue
        seen.add(root)
        stack = [(root, iter(adj[root]))]
        while stack:
            u, it = stack[-1]
            v = next(it, None)
            if v is None:
                order.append(u)
                stack.pop()
            elif v not in seen:
                seen.add(v)
                stack.append((v, iter(adj[v])))
    seen, comps = set(), []
    for root in reversed(order):
        if root in seen:
            continue
        seen.add(root)
        comp, todo = [], [root]
        while todo:
            u = todo.pop()
            comp.append(u)
            for v in rev[u]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        if len(comp) > 1 or root in adj[root]:
            comps.append(comp)
    return comps


def period_gcd(adj, comp):
    """GCD of lengths of all closed walks in a strongly connected component."""
    members = set(comp)
    dist = {comp[0]: 0}
    todo = collections.deque(dist)
    while todo:
        u = todo.popleft()
        for v in adj[u]:
            if v in members and v not in dist:
                dist[v] = dist[u] + 1
                todo.append(v)
    result = 0
    for u in comp:
        for v in adj[u]:
            if v in members:
                result = math.gcd(result, dist[u] + 1 - dist[v])
    return result


def explore(max_depth: int, cap: int, seconds: float):
    started = time.monotonic()
    recurrent = {(10,)}
    for depth in range(1, max_depth + 1):
        if depth == 1:
            candidates = recurrent
        else:
            if 19 * len(recurrent) > cap:
                print(f"UNDECIDED depth={depth} candidate_cap={cap}", flush=True)
                return
            candidates = {w + (a,) for w in recurrent for a in range(19)}
        adj = {}
        for i, word in enumerate(sorted(candidates)):
            if i % 512 == 0 and time.monotonic() - started > seconds:
                print(f"UNDECIDED depth={depth} time_cap={seconds}", flush=True)
                return
            adj[word] = block_successors(word) & candidates
        comps = cyclic_components(adj)
        recurrent = {w for comp in comps for w in comp}
        summary = collections.Counter((len(c), period_gcd(adj, c)) for c in comps)
        print(f"depth={depth} candidates={len(candidates)} edges={sum(map(len, adj.values()))} "
              f"recurrent={len(recurrent)} scc_size_gcd={sorted(summary.items())} "
              f"seconds={time.monotonic()-started:.3f}", flush=True)
        if depth <= 4:
            for comp in comps:
                if len(comp) <= 20:
                    print("  component", sorted(comp), flush=True)
        if not recurrent:
            return


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depth", type=int, default=12)
    parser.add_argument("--cap", type=int, default=1000000)
    parser.add_argument("--seconds", type=float, default=300)
    args = parser.parse_args()
    if args.depth < 1 or args.cap < 19 or args.seconds <= 0:
        parser.error("positive depth/time and cap>=19 required")
    explore(args.depth, args.cap, args.seconds)


if __name__ == "__main__":
    main()
