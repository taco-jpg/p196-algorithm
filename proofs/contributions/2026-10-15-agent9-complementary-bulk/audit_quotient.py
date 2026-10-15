#!/usr/bin/env python3
"""Reproduce the initial 267,520 literal-integer quotient checks.

Finite controls, not an all-width or all-orbit assertion.
"""
from __future__ import annotations
import itertools
import json
from pathlib import Path
from complementary_bulk import PHASES, State, audit_instance, outer_step


def run() -> dict:
    count = 0
    for c in PHASES:
        for B in [()] + [(x,) for x in range(1, 19)]:
            for A in [()] + [(x,) for x in range(19)]:
                for C in [()] + [(x,) for x in range(0, 19, 2)]:
                    s = State(c, B, A, C)
                    for g, h in ((2, 2), (2, 3), (3, 2), (4, 5)):
                        audit_instance(s, g, h)
                        count += 1
    hist, witnesses = {}, {}
    for c in PHASES:
        for b in range(4):
            words = [()] if b == 0 else ((x,) + y for x in range(1, 19)
                for y in itertools.product(range(19), repeat=b-1))
            for B in words:
                if B and B[-1] == c:
                    continue
                cp, Bp, u, gamma = outer_step(c, B)
                key = str((gamma, u))
                hist[key] = hist.get(key, 0) + 1
                if u > 1 and key not in witnesses:
                    witnesses[key] = (c, B, cp, Bp)
    assert count == 267520
    return {
        'scope': 'all phases; B empty or one positive coefficient; A empty or one coefficient; C empty or one even coefficient; gaps (2,2),(2,3),(3,2),(4,5)',
        'controls': count, 'passed': True,
        'outer_scope': 'all trimmed exteriors of length <=3, all phases',
        'outer_histogram': hist, 'outer_shrink_witnesses': witnesses,
    }


if __name__ == '__main__':
    result = run()
    destination = Path(__file__).with_name('initial_audit.json')
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
