#!/usr/bin/env python3
"""Independent exact three-column reverse-graph audit for Agent #113.

Finite automaton only. A directed inverse cycle is NOT an infinite ordinary
integer reverse-and-add trajectory. Standard library only, deterministic.
Usage: python3 check.py --verify [witnesses.txt]
       python3 check.py --generate > witnesses.txt
"""
from collections import defaultdict, deque
from hashlib import sha256
from pathlib import Path
import argparse
import json

BOX = tuple((x, y, z) for x in range(1, 19)
            for y in range(19) for z in range(19))
BOX_SET = set(BOX)
DESC = tuple((a, b) for a in range(1, 10) for b in range(a))
FINITE = {"10": (10, 0), "20": (10, 5, 0), "32": (10, 6, 0),
          "40": (10, 5, 3, 0), "41": (10, 6, 4, 0),
          "60": (10, 5, 2, 0), "64": (10, 5, 2, 0),
          "65": (10, 6, 10, 5, 4, 3, 0), "76": (10, 6, 4, 0),
          "80": (10, 5, 3, 2, 0), "81": (10, 6, 4, 2, 0),
          "82": (10, 5, 3, 2, 0), "83": (10, 6, 5, 3, 0)}
CYCLE = ((1, 5, 10), (10, 4, 6), (5, 2, 3), (2, 11, 1))
CYCLE_CARRY = (0, 0, 0, 1)


def top(w, e):
    x, y, z = w
    return (x + (y + (z + e) // 10) // 10) // 10


def next_t(w, e):
    x, y, z = w
    high2 = (z + e) // 10
    high1 = (y + high2) // 10
    if top(w, e) == 0:
        return ((x % 10) + ((x + high1) % 10),
                ((y + x // 10) % 10) + ((y + high2) % 10),
                ((z + (y + x // 10) // 10) % 10) + ((z + e) % 10))
    return ((x % 10) + 1,
            ((y + x // 10) % 10) + ((x + high1) % 10),
            ((z + (y + x // 10) // 10) % 10) + ((y + high2) % 10))


def graphs():
    predecessors = defaultdict(list)
    first_predecessors = defaultdict(list)
    for w in BOX:
        for e in (0, 1):
            v = next_t(w, e)
            assert v in BOX_SET, (w, e, v)
            predecessors[v].append((w, e))
            if top(w, e) == 0:
                first_predecessors[v].append((w, e))
    return predecessors, first_predecessors


def layer(predecessors, targets):
    return {w for p in targets for w, e in predecessors[p]}


def starts(a, b, first_predecessors):
    # Deterministic target and carry for each first predecessor.
    outcome = {}
    for c in range(10):
        for w, e in first_predecessors[(a, b, c)]:
            outcome.setdefault(w, (c, e))
    return outcome


def explore(a, b, predecessors, first_predecessors, *, until_cycle=False):
    initial = starts(a, b, first_predecessors)
    q = deque(sorted(initial))
    parents = {w: None for w in initial}
    goal = next((w for w in sorted(initial) if w in CYCLE), None)
    while q:
        u = q.popleft()
        if until_cycle and goal is not None:
            break
        for v, e in predecessors[u]:
            if v not in parents:
                parents[v] = (u, e)
                q.append(v)
                if until_cycle and v in CYCLE:
                    goal = v
                    break
    return initial, parents, goal


def encode(w, e):
    x, y, z = w
    assert w in BOX_SET and e in (0, 1)
    return f"{(e << 13) | (x * 361 + y * 19 + z):04x}"


def decode(payload):
    assert len(payload) % 4 == 0
    result = []
    for i in range(0, len(payload), 4):
        num = int(payload[i:i + 4], 16)
        e, code = num >> 13, num & 8191
        x, rest = divmod(code, 361)
        y, z = divmod(rest, 19)
        w = (x, y, z)
        assert w in BOX_SET and e in (0, 1)
        result.append((w, e))
    return result


def make_witness(a, b, predecessors, first_predecessors):
    initial, parents, goal = explore(a, b, predecessors,
                                     first_predecessors, until_cycle=True)
    assert goal is not None
    chain = [goal]
    while parents[chain[-1]] is not None:
        chain.append(parents[chain[-1]][0])
    chain.reverse()
    c, e0 = initial[chain[0]]
    steps = [(chain[0], e0)]
    steps.extend((chain[i + 1], parents[chain[i + 1]][1])
                 for i in range(len(chain) - 1))
    return f"{a}{b}:{c}:" + "".join(encode(w, e) for w, e in steps)


def verify_witness_line(line):
    ab, c, payload = line.split(":")
    assert len(ab) == 2 and len(c) == 1
    a, b = int(ab[0]), int(ab[1])
    assert 1 <= a <= 9 and 0 <= b < a and ab not in FINITE
    current = (a, b, int(c))
    assert 0 <= current[2] <= 9
    steps = decode(payload)
    assert steps
    for j, (prior, carry) in enumerate(steps):
        assert next_t(prior, carry) == current, (ab, j, prior, carry, current)
        if j == 0:
            assert top(prior, carry) == 0, (ab, prior, carry)
        current = prior
    assert current in CYCLE, (ab, current)
    return len(steps)


def formula_nongrowth(p):
    # Independent inverse-column-equation search, not graph traversal.
    states = {((), 0, 0)}
    for i, target in enumerate(p):
        nxt = set()
        for word, x, y in states:
            for s in range(1 if i == 0 else 0, 19):
                x_out = (s + x) // 10
                for y_out in (0, 1):
                    if (s + y_out) // 10 == y and \
                       2 * s + x + y_out - 10 * (x_out + y) == target:
                        nxt.add((word + (s,), x_out, y_out))
        states = nxt
    return {word for word, _, _ in states}


def formula_growth(p):
    if p[0] > 10:
        return set()
    first = p[0] + 9 if p[0] <= 9 else 9
    states = {((first,), first // 10, 1)}
    for target in p[1:]:
        nxt = set()
        for word, x, y in states:
            for y_out in (0, 1):
                if (word[-1] + y_out) // 10 != y:
                    continue
                digit = target - word[-1] - y_out + 10 * y
                if not 0 <= digit <= 9:
                    continue
                for x_out in (0, 1):
                    s = digit + 10 * x_out - x
                    if 0 <= s <= 18:
                        nxt.add((word + (s,), x_out, y_out))
        states = nxt
    return {word for word, x, y in states
            if any((word[-1] + t) // 10 == y for t in (0, 1))}


def verify_file(path):
    predecessor, first = graphs()
    for i, u in enumerate(CYCLE):
        v = CYCLE[(i + 1) % 4]
        assert next_t(v, CYCLE_CARRY[i]) == u, (u, v)
    # Cross-check graph inverse with independent carry equations on ALL
    # 6,498 canonical-coordinate triples (not just the 45 root layers).
    for p in BOX:
        assert {w for w, e in first[p]} == formula_nongrowth(p), p
        assert {w for w, e in predecessor[p]} == \
               formula_nongrowth(p) | formula_growth(p), p

    finite = {}
    for key, expected in FINITE.items():
        a, b = int(key[0]), int(key[1])
        cur = {(a, b, c) for c in range(10)}
        layers = [len(cur)]
        cur = layer(first, cur)
        layers.append(len(cur))
        while cur:
            cur = layer(predecessor, cur)
            layers.append(len(cur))
        assert tuple(layers) == expected, (key, layers, expected)
        finite[key] = layers

    data = Path(path).read_bytes()
    lines = [line.strip() for line in data.decode("utf-8").splitlines()
             if line.strip() and not line.startswith("#")]
    witness_sizes = {}
    for line in lines:
        ab = line.split(":", 1)[0]
        assert ab not in witness_sizes, ab
        witness_sizes[ab] = verify_witness_line(line)
    remaining = {f"{a}{b}" for a, b in DESC} - set(FINITE)
    assert set(witness_sizes) == remaining, set(witness_sizes) ^ remaining
    assert len(remaining) == 32 and len(FINITE) == 13 and len(DESC) == 45
    reach = {}
    for key in sorted(remaining):
        a, b = map(int, key)
        _, found, _ = explore(a, b, predecessor, first)
        assert set(found) == BOX_SET, (key, len(found))
        reach[key] = len(found)

    report = {"classification": "exact finite triple-graph experiment (NOT integer orbit)",
              "box_states": len(BOX), "raw_edges": len(BOX) * 2,
              "inverted_edges": sum(len(v) for v in predecessor.values()),
              "descending_prefixes": len(DESC),
              "acyclic_prefixes": finite,
              "cyclic_prefix_count": len(remaining),
              "all_32_reach_every_box_state": True,
              "common_cycle": [list(x) for x in CYCLE],
              "common_cycle_inverse_carries": list(CYCLE_CARRY),
              "witness_steps_min": min(witness_sizes.values()),
              "witness_steps_max": max(witness_sizes.values()),
              "witnesses_sha256": sha256(data).hexdigest(),
              "finite_integer_realizability_proved": False,
              "lean_compiled": False}
    return report


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    group = cli.add_mutually_exclusive_group(required=True)
    group.add_argument("--generate", action="store_true")
    group.add_argument("--verify", nargs="?", const="witnesses.txt")
    args = cli.parse_args()
    if args.generate:
        predecessors, first = graphs()
        for a, b in DESC:
            if f"{a}{b}" not in FINITE:
                print(make_witness(a, b, predecessors, first))
    else:
        print(json.dumps(verify_file(args.verify), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
