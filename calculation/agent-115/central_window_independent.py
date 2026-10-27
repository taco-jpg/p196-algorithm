#!/usr/bin/env python3
"""Independent central-three/four exact relation and universal-safety audit.

Agent 115; independent second implementation for T1.central-window3-4-safety.
Only ordinary decimal integer arithmetic is used for the fixture checks.
No P196 implementation is imported.

Run from the repository root:
    python3 calculation/agent-115/central_window_independent.py

Closure quantifies over every integer completion separately. Consecutive
abstract edges can use incompatible completions; no actual-orbit exclusion
is asserted.
"""
from collections import Counter
from itertools import product


def carry_digits(coefficients, incoming):
    digits = []
    c = incoming
    for q in coefficients:
        digits.append((q + c) % 10)
        c = (q + c) // 10
    return tuple(digits), c


def to_integer(q):
    n = len(q)
    if q != q[::-1] or q[0] == 0:
        raise ValueError("nonrealizable profile")
    d = [0] * n
    for i in range(n // 2):
        d[n - 1 - i] = min(q[i], 9)
        d[i] = q[i] - d[n - 1 - i]
    if n % 2:
        if q[n // 2] % 2:
            raise ValueError("odd central coefficient")
        d[n // 2] = q[n // 2] // 2
    return sum(x * 10**i for i, x in enumerate(d))


def integer_profile(n):
    ds = tuple(map(int, str(n)[::-1]))
    return tuple(x + y for x, y in zip(ds, ds[::-1]))


def state_of(q):
    m = len(q) // 2
    return ("O", q[m - 1], q[m]) if len(q) % 2 else ("E", q[m - 2], q[m - 1])


def step_integer(n):
    return n + int(str(n)[::-1])


def local_choices(state):
    """Yield (target, concrete symmetric input profile), including duplicates."""
    typ, a, s = state
    if typ == "O":
        for c in (0, 1):
            ds, h = carry_digits((a, s, a), c)
            target = ("O", ds[0] + ds[2], 2 * ds[1])
            yield target, (1, 10 * c, a, s, a, 10 * c, 1)
        for t, k in product(range(19), (0, 1)):
            # The same mirrored outside coefficient t sets the entering
            # carry and contributes the new outside digit after overflow.
            c = (t + k) // 10
            ds, h = carry_digits((a, s, a), c)
            target = ("E", ds[0] + (t + h) % 10, ds[1] + ds[2])
            yield target, (10, 10 * k, t, a, s, a, t, 10 * k, 10)
    else:
        for c, g in product((0, 1), repeat=2):
            ds, h = carry_digits((a, s, s, a), c)
            if g:
                target = ("O", ds[1] + ds[3], 2 * ds[2])
            else:
                target = ("E", ds[0] + ds[3], ds[1] + ds[2])
            v = 10 if g else 1
            yield target, (v, 10 * c, a, s, s, a, 10 * c, v)


def safe(state):
    _, a, s = state
    return max(a, s) >= 10 and (a not in (0, 11) or s not in (0, 11))


def unsafe_completion(state):
    typ, a, s = state
    middle = (a, s, a) if typ == "O" else (a, s, s, a)
    v = 1 if max(a, s) <= 9 else 11
    return (v,) + middle + (v,)


def main():
    states = tuple(("O", a, r) for a in range(19) for r in range(0, 19, 2)) + tuple(
        ("E", a, s) for a in range(19) for s in range(19))
    universe = set(states)
    graph = {}
    fixtures = 0
    witnesses = {}
    for state in states:
        graph[state] = set()
        for target, q in local_choices(state):
            if target not in universe:
                raise AssertionError(("bad target", state, target))
            n = to_integer(q)
            if integer_profile(n) != q or state_of(q) != state:
                raise AssertionError(("bad source", state, q, n))
            out = step_integer(n)
            actual = state_of(integer_profile(out))
            if target != actual:
                raise AssertionError(("formula mismatch", state, target, actual, n, out))
            graph[state].add(target)
            witnesses.setdefault((state, target), (n, out))
            fixtures += 1

    edge_counts = Counter((x[0], y[0]) for x in states for y in graph[x])
    print("states", len(states), "edges", sum(map(len, graph.values())), "edge_types", dict(sorted(edge_counts.items())))
    print("labelled_integer_fixtures", fixtures, "distinct_edge_witnesses", len(witnesses))

    # Exhaust all short profiles to audit the appended-overflow-digit boundary.
    # At width three, c=0 and the outer appended digit is 1. The general
    # relation contains this edge by taking t=1-h, k=0, where h is the
    # carry after normalizing the three coefficients.
    short_total = 0
    short_extra = 0
    for L in range(3, 7):
        for h in product(range(19), repeat=(L + 1) // 2):
            if h[0] == 0 or (L % 2 and h[-1] % 2):
                continue
            q = h + (h[:-1] if L % 2 else h)[::-1]
            n = to_integer(q)
            source = state_of(q)
            target = state_of(integer_profile(step_integer(n)))
            short_total += 1
            if target not in graph[source]:
                short_extra += 1
                raise AssertionError(("missing short edge", q, source, target))
    print("short_profile_checks", short_total, "new_edges", short_extra)

    unsafe = [s for s in states if not safe(s)]
    for state in unsafe:
        n = to_integer(unsafe_completion(state))
        out = step_integer(n)
        if state_of(integer_profile(n)) != state or str(out) != str(out)[::-1]:
            raise AssertionError(("unsafe completion fails", state, n, out))
    print("unsafe_completions", len(unsafe))

    current = {s for s in states if safe(s)}
    rounds = []
    removed_at = {}
    round_no = 0
    while True:
        print("safe_round", round_no, "total", len(current), "odd", sum(s[0] == "O" for s in current), "even", sum(s[0] == "E" for s in current))
        rounds.append(len(current))
        nxt = {s for s in current if graph[s] <= current}
        for s in current - nxt:
            removed_at[s] = round_no + 1
        if nxt == current:
            break
        current = nxt
        round_no += 1
    print("greatest_closed_safe_set", sorted(current))
    print("removal_histogram", sorted(Counter(removed_at.values()).items()))
    if not current:
        # Independently verify the assigned ranks as a finite counter-strategy.
        rank = {s: removed_at.get(s, 0) for s in states}
        if any(safe(s) and not any(rank[t] < rank[s] for t in graph[s]) for s in states):
            raise AssertionError("nondecreasing rank witness")
        print("rank_counterstrategy_checked", len(states), "max_rank", max(rank.values()))
        for s in sorted(states):
            if rank[s] == max(rank.values()):
                print("last_removed", s)
    print("ALL INDEPENDENT CHECKS PASSED")


if __name__ == "__main__":
    main()
