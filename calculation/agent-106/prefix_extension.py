#!/usr/bin/env python3
"""Extend the saturated eight-phase three-column skeleton by more columns.

Every tail coefficient 0..18 and both incoming high carry bits are allowed.
Only edges retaining the prescribed next three-column phase are kept.
The graph is an overapproximation of finite neutral B cycles after padding.
Its cycles are NOT full B-cycle certificates.

    python3 calculation/agent-106/prefix_extension.py --max-width 7
"""

import argparse
from array import array
from collections import Counter, deque
from itertools import product
from math import gcd
from pathlib import Path
import random
import re
import time


ROOT = Path(__file__).resolve().parents[2]
PROFILE = ROOT / "lean/P196/Agent2SaturatedProfile/Saturated8CycleProfile.lean"


def skeleton():
    text = PROFILE.read_text().split("def cycleState", 1)[1].split("theorem edge0", 1)[0]
    states = [tuple(map(int, match)) for match in re.findall(r"⟨(\d+),(\d+),(\d+)⟩", text)]
    assert len(states) == 8
    return states


def advance(word, inward):
    """Calculate low digits left-to-right and high digits right-to-left."""
    low = []
    carry = 0
    for coefficient in word:
        low.append((coefficient + carry) % 10)
        carry = (coefficient + carry) // 10
    high = [0] * len(word)
    for position in range(len(word) - 1, -1, -1):
        high[position] = (word[position] + inward) % 10
        inward = (word[position] + inward) // 10
    if inward == 0:
        target = tuple(a + b for a, b in zip(low, high))
    else:
        target = (low[0] + 1,) + tuple(low[i] + high[i - 1]
                                               for i in range(1, len(word)))
    return target, inward


def bigint_reference(word, inward):
    # The single middle coefficient forces the desired incoming high carry,
    # irrespective of the carry emerging from the low copy of word.
    whole = word + (18 * inward,) + word[::-1]
    value = sum(coefficient * 10 ** i for i, coefficient in enumerate(whole))
    digits = tuple(map(int, str(value)[::-1]))
    pairword = tuple(a + b for a, b in zip(digits, digits[::-1]))
    return pairword[:len(word)], len(digits) - len(whole)


def crosscheck():
    rng = random.Random(106)
    checks = 0
    for width in range(1, 12):
        for _ in range(100):
            word = (rng.randrange(1, 19),) + tuple(rng.randrange(19) for _ in range(width - 1))
            for inward in (0, 1):
                assert advance(word, inward) == bigint_reference(word, inward)
                checks += 1
    return checks


def graph(width, profile):
    tails = list(product(range(19), repeat=width - 3))
    tail_index = {tail: i for i, tail in enumerate(tails)}
    count = len(tails)
    adjacency = [[] for _ in range(8 * count)]
    reverse = [[] for _ in adjacency]
    for phase in range(8):
        target_phase = (phase + 1) % 8
        for i, tail in enumerate(tails):
            source = phase * count + i
            for inward in (0, 1):
                out, overflow = advance(profile[phase] + tail, inward)
                if overflow != phase % 2 or out[:3] != profile[target_phase]:
                    continue
                target = target_phase * count + tail_index[out[3:]]
                if target not in adjacency[source]:
                    adjacency[source].append(target)
                    reverse[target].append(source)
    return tails, adjacency, reverse


def strongly_connected(adjacency, reverse):
    size = len(adjacency)
    visited = bytearray(size)
    order = array("I")
    for root in range(size):
        if visited[root]:
            continue
        stack = [(root, 0)]
        visited[root] = 1
        while stack:
            vertex, offset = stack[-1]
            if offset == len(adjacency[vertex]):
                order.append(vertex)
                stack.pop()
            else:
                stack[-1] = vertex, offset + 1
                target = adjacency[vertex][offset]
                if not visited[target]:
                    visited[target] = 1
                    stack.append((target, 0))
    membership = array("i", [-1]) * size
    components = []
    for root in reversed(order):
        if membership[root] >= 0:
            continue
        index = len(components)
        members = array("I", [root])
        membership[root] = index
        for vertex in members:
            for source in reverse[vertex]:
                if membership[source] < 0:
                    membership[source] = index
                    members.append(source)
        components.append(members)
    return membership, components


def component_period(members, index, membership, adjacency):
    distance = {members[0]: 0}
    queue = deque([members[0]])
    while queue:
        source = queue.popleft()
        for target in adjacency[source]:
            if membership[target] == index and target not in distance:
                distance[target] = distance[source] + 1
                queue.append(target)
    assert len(distance) == len(members)
    period = 0
    for source in members:
        for target in adjacency[source]:
            if membership[target] == index:
                period = gcd(period, abs(distance[source] + 1 - distance[target]))
    assert period > 0
    return period


def first_return(root, adjacency, membership, maximum=64):
    """Shortest directed return to this root, with a simple retained witness."""
    region = membership[root]
    predecessors = {root: None}
    queue = deque([(root, 0)])
    while queue:
        vertex, depth = queue.popleft()
        if depth >= maximum:
            continue
        for target in adjacency[vertex]:
            if membership[target] != region:
                continue
            if target == root:
                path = [vertex]
                while predecessors[path[-1]] is not None:
                    path.append(predecessors[path[-1]])
                path.reverse()
                return path
            if target not in predecessors:
                predecessors[target] = vertex
                queue.append((target, depth + 1))
    return None


def inspect_width(width, profile, show_witness):
    started = time.monotonic()
    tails, adjacency, reverse = graph(width, profile)
    membership, components = strongly_connected(adjacency, reverse)
    cyclic = [(index, members) for index, members in enumerate(components)
              if len(members) > 1 or members[0] in adjacency[members[0]]]
    periods = Counter(component_period(members, index, membership, adjacency)
                      for index, members in cyclic)
    sizes = Counter(len(members) for _, members in cyclic)
    print(f"width={width} vertices={len(adjacency)} edges={sum(map(len, adjacency))} "
          f"cyclic_sccs={len(cyclic)} cyclic_vertices={sum(len(members) for _, members in cyclic)} "
          f"period_gcd_histogram={dict(sorted(periods.items()))} "
          f"scc_size_histogram={dict(sorted(sizes.items()))} sec={time.monotonic()-started:.3f}", flush=True)
    if cyclic and show_witness:
        index, members = min(cyclic, key=lambda item: (len(item[1]), min(item[1])))
        path = first_return(min(members), adjacency, membership)
        if path:
            states = [profile[v // len(tails)] + tails[v % len(tails)] for v in path]
            carry_bits = []
            for position, word in enumerate(states):
                target = states[(position + 1) % len(states)]
                choices = [inward for inward in (0, 1)
                           if advance(word, inward) == (target, path[position] // len(tails) % 2)]
                assert choices
                carry_bits.append(choices[0])
            print(f"width={width} witness_period={len(states)} "
                  f"witness_states={states} witness_high_inputs={carry_bits}", flush=True)
    return periods


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-width", type=int, default=4)
    parser.add_argument("--max-width", type=int, default=6)
    parser.add_argument("--witness", action="store_true")
    args = parser.parse_args()
    assert 3 <= args.min_width <= args.max_width <= 7
    profile = skeleton()
    print("bigint_crosschecks=" + str(crosscheck()), flush=True)
    for width in range(args.min_width, args.max_width + 1):
        inspect_width(width, profile, args.witness)


if __name__ == "__main__":
    main()
