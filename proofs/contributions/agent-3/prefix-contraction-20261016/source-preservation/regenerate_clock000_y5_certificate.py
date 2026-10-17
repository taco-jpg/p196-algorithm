#!/usr/bin/env python3
"""Reproduce the clock000/y5 subset-DFA certificate using only Python stdlib.

This intentionally regenerates one case only. It does not load or claim to
recover the omitted historical certificate. Output is computational evidence,
not a Lean proof.
"""
from collections import deque
import json

def local(st, s, h):
    a, b, t = st
    out = []
    for x in range(19):
        for bn in (0, 1):
            if (x + bn) // 10 != b:
                continue
            an, lo = divmod(x + a, 10)
            hi = (x + bn) % 10
            if (lo + t if h else lo + hi) == s:
                out.append(((an, bn, hi if h else -1), x))
    return tuple(out)

def layers(st, s, clock):
    if not st:
        return (((), ()),)
    h = clock[0]
    return tuple(((ns,) + tail, (x,) + labels)
                 for ns, x in local(st[0], s, h)
                 for tail, labels in layers(st[1:], x, clock[1:]))

def build(clock=(0, 0, 0), y=5):
    root = tuple((0, h, 1 if h else -1) for h in clock)
    first = frozenset(ns for ns, labels in layers(root, y + 9, clock)
                      if all(labels))
    states, index = [first], {first: 0}
    transitions, todo = [], deque([first])
    while todo:
        st = todo.popleft()
        row = []
        for s in (y, y + 9):
            nxt = frozenset(ns for path in st
                            for ns, _ in layers(path, s, clock))
            if nxt not in index:
                index[nxt] = len(states)
                states.append(nxt)
                todo.append(nxt)
            row.append(index[nxt])
        transitions.append(row)
    empty = index[frozenset()]
    reverse = [[] for _ in states]
    for v, row in enumerate(transitions):
        for bit, w in enumerate(row):
            reverse[w].append((v, bit))
    distance, kill_bit = [None] * len(states), [None] * len(states)
    distance[empty] = 0
    todo = deque([empty])
    while todo:
        w = todo.popleft()
        for v, bit in reverse[w]:
            if distance[v] is None:
                distance[v], kill_bit[v] = distance[w] + 1, bit
                todo.append(v)
    assert all(d is not None for d in distance)
    def witness(i):
        bits = []
        while i != empty:
            bit = kill_bit[i]
            assert bit is not None
            bits.append(bit)
            i = transitions[i][bit]
        return bits
    def sort_state(st):
        return tuple(sorted(st))
    states_out = [sorted(st) for st in states]
    records = []
    for i, st in enumerate(states):
        bits = witness(i)
        records.append({
            "index": i, "subset": states_out[i],
            "distance_to_empty": distance[i], "kill_bit": kill_bit[i],
            "kill_digits": [5 if b == 0 else 14 for b in bits],
            "kill_bits": "".join(map(str, bits)),
            "transition_5": transitions[i][0],
            "transition_14": transitions[i][1],
        })
    result = {
        "schema_version": 1,
        "title": "Regenerated clock=(0,0,0), y=5 finite rejecting-block certificate",
        "status": "COMPUTATIONAL_WIP_NOT_LEAN_CHECKED",
        "parameters": {"clock": [0,0,0], "y": 5,
                       "inputDigits": [5,14], "initialTargetDigit": 14},
        "summary": {"state_count": len(states),
                    "live_state_count": sum(bool(st) for st in states),
                    "empty_state_index": empty,
                    "max_rejection_length": max(distance),
                    "all_states_reach_empty": all(d is not None for d in distance)},
        "state_representation": "Each nonempty automaton state is a singleton set containing a 3-tuple of original local states [a,b,-1]; empty set is absorbing.",
        "states": records,
        "transitions": transitions,
        "empty_state_index": empty,
        "distance": distance,
        "kill_bit": kill_bit,
    }
    assert len(states) == 65 and empty == 13 and max(distance) == 9
    for i in range(len(states)):
        j = i
        for bit in witness(i):
            j = transitions[j][bit]
        assert j == empty and len(witness(i)) == distance[i] <= 9
    return result

if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
