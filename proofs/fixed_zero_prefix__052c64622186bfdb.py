#!/usr/bin/env python3
"""Classify fixed-interior-carry-zero controls at prefix widths 1..3.

These are abstract controls, not trajectories of a fixed decimal seed.
"""

from itertools import product
import json
from pathlib import Path


def successor(prefix):
    low, high = [], []
    carry = 0
    for coefficient in prefix:
        carry, digit = divmod(coefficient + carry, 10)
        low.append(digit)
    carry = 0
    for coefficient in reversed(prefix):
        carry, digit = divmod(coefficient + carry, 10)
        high.append(digit)
    high.reverse()
    if carry:
        return tuple([low[0] + 1] + [low[i] + high[i - 1] for i in range(1, len(prefix))])
    return tuple(a + b for a, b in zip(low, high))


def safe(prefix):
    return max(prefix) >= 10 and not (prefix[0] == 11 and all(x in (0, 11) for x in prefix))


def classify(width):
    outcomes = {}
    cycles = []
    states = [(a,) + tail for a in range(1, 19)
              for tail in product(range(19), repeat=width - 1)]
    for start in states:
        path, position = [], {}
        q = start
        while q not in outcomes:
            if not safe(q):
                outcomes[q] = ("escape", 0)
                break
            if q in position:
                cycle = path[position[q]:]
                index = len(cycles)
                cycles.append(cycle)
                for state in cycle:
                    outcomes[state] = ("cycle", index)
                break
            position[q] = len(path)
            path.append(q)
            q = successor(q)
        for state in reversed(path):
            if state in outcomes:
                continue
            kind, amount = outcomes[successor(state)]
            outcomes[state] = (kind, amount + 1 if kind == "escape" else amount)
    for cycle in cycles:
        for a, b in zip(cycle, cycle[1:] + cycle[:1]):
            assert safe(a) and successor(a) == b
            # Independent ordinary-integer realization of carry zero.
            digits = [max(x - 9, 0) for x in a] + [0] + [min(x, 9) for x in a[::-1]]
            n = int("".join(map(str, digits[::-1])))
            n += int(str(n)[::-1])
            d = tuple(map(int, str(n)[::-1]))
            assert tuple(d[i] + d[-1 - i] for i in range(width)) == b
    return dict(width=width, canonical_prefixes=len(states),
                initially_unsafe=sum(not safe(q) for q in states),
                eventual_unsafe_prefixes=sum(outcomes[q][0] == "escape" for q in states),
                safe_cycle_basin_prefixes=sum(outcomes[q][0] == "cycle" for q in states),
                maximum_finite_escape_steps=max(v[1] for v in outcomes.values() if v[0] == "escape"),
                safe_cycles=cycles)


def main():
    report = dict(status="complete fixed-zero classification at widths 1..3",
                  widths=[classify(k) for k in range(1, 4)],
                  interpretation="A safe cycle disproves fixed-zero as a universal escape controller; it is not an actual infinite decimal orbit.")
    Path(__file__).with_name("fixed_zero_prefix.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
