#!/usr/bin/env python3
"""Independent ordinary-integer controls for the conditional seven-step gate."""

from itertools import product
import json
from pathlib import Path


PREFIXES = [(4, 4, 0), (8, 8, 0), (16, 16, 0), (7, 14, 7),
            (15, 8, 15), (6, 14, 14), (13, 9, 9), (4, 4, 0)]
OVERFLOW = (0, 0, 1, 0, 1, 0, 1)
LOWER = (0, 0, 0, 0, 1, 1, 1)


def value(q):
    result = 0
    for x in reversed(q):
        result = 10 * result + x
    return result


def normalized(q):
    return tuple(map(int, str(value(q))[::-1]))


def pair(d):
    return tuple(a + b for a, b in zip(d, reversed(d)))


def carry_at(q, index):
    result = value(q[:index]) // 10 ** index
    assert result in (0, 1)
    return result


def control_valid(c):
    return c[0] == c[1] == c[3] == c[5] == 0 and c[6] == 1


def prefix_successor(p, incoming):
    low, high = [], []
    c = 0
    for x in p:
        c, digit = divmod(x + c, 10)
        low.append(digit)
    c = incoming
    for x in reversed(p):
        c, digit = divmod(x + c, 10)
        high.append(digit)
    high.reverse()
    return ((low[0] + 1, low[1] + high[0], low[2] + high[1])
            if c else tuple(a + b for a, b in zip(low, high)))


def check_all_boundary_controls():
    returning = []
    for controls in product((0, 1), repeat=7):
        p = PREFIXES[0]
        for c in controls:
            p = prefix_successor(p, c)
        assert (p == PREFIXES[0]) == control_valid(controls)
        if p == PREFIXES[0]:
            returning.append(controls)
    assert len(returning) == 4
    return dict(all_control_words=128, returning_control_words=returning)


def middle_formula(w, phase, outgoing):
    width = len(w)
    number = value(w) + LOWER[phase]
    d = tuple(map(int, str(number % (10 ** width)).zfill(width)[::-1]))
    assert number // (10 ** width) == outgoing
    if not OVERFLOW[phase]:
        return pair(d)
    result = [0] * (width + 1)
    for i, x in enumerate(d):
        result[i] += x
        result[width - i] += x
    boundary = outgoing if phase == 2 else 5 + outgoing if phase == 4 else 0
    result[0] += boundary
    result[-1] += boundary
    return tuple(result)


def middles(width):
    for left in product(range(19), repeat=width // 2):
        if width % 2:
            for center in range(0, 19, 2):
                yield left + (center,) + left[::-1]
        else:
            yield left + left[::-1]


def window(w):
    q = PREFIXES[0] + w + PREFIXES[0][::-1]
    states, controls, hits = [], [], []
    for phase in range(7):
        states.append(q)
        controls.append(carry_at(q, len(q) - 3))
        d = normalized(q)
        hits.append(d == d[::-1])
        q = pair(d)
    states.append(q)
    valid = control_valid(controls)
    assert (q[:3] == PREFIXES[0]) == valid
    if valid:
        for phase in range(7):
            before, after = states[phase:phase + 2]
            assert before[:3] == PREFIXES[phase]
            assert after[:3] == PREFIXES[phase + 1]
            assert carry_at(before, 3) == LOWER[phase]
            assert len(after) - len(before) == OVERFLOW[phase]
            assert middle_formula(before[3:-3], phase, controls[phase]) == after[3:-3]
        assert len(q) == len(states[0]) + 3
        safe_condition = max(states[0][3:-3]) >= 10 and max(states[1][3:-3]) >= 10
        assert (not any(hits)) == safe_condition
    return dict(middle=w, controls=controls, returns=valid,
                first_hit=next((i + 1 for i, hit in enumerate(hits) if hit), None),
                returned_middle=q[3:-3], states=states)


def main():
    rows, representatives = [], {}
    for width in range(1, 6):
        total = returned = safe_returns = zero_ended_returns = 0
        for w in middles(width):
            case = window(w)
            total += 1
            returned += case["returns"]
            safe_returns += case["returns"] and case["first_hit"] is None
            zero_ended = case["returns"] and case["returned_middle"][0] == 0
            zero_ended_returns += zero_ended
            category = (case["returns"], case["first_hit"] is None, zero_ended)
            representatives.setdefault(str(category), case)
        rows.append(dict(width=width, middles=total, returns=returned,
                         safe_returns=safe_returns, zero_ended_returns=zero_ended_returns))

    # Literal two-return counterexample to unconditional safe recurrence.
    first = window((1, 1, 18, 1, 1))
    second = window(first["returned_middle"])
    assert first["returns"] and second["returns"]
    assert first["first_hit"] is None and second["first_hit"] is None
    third_start = PREFIXES[0] + second["returned_middle"] + PREFIXES[0][::-1]
    d = normalized(third_start)
    assert d == d[::-1]
    result = dict(
        status="PASS",
        exhaustive_boundary_controls=check_all_boundary_controls(),
        exhaustive_padded_middle_counts=rows,
        total_padded_middles=sum(r["middles"] for r in rows),
        domain="Symmetric nonempty middles, coefficients0..18, even center; zero endpoints allowed.",
        representatives=representatives,
        two_safe_returns_then_hit=dict(initial_middle=first["middle"],
                                       first_return_middle=first["returned_middle"],
                                       second_return_middle=second["returned_middle"],
                                       first_hit=15),
        scope="Finite independent controls of a conditional exact gate; no persistent-control or all-time claim.",
    )
    Path(__file__).with_name("verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("representatives",)}))


if __name__ == "__main__":
    main()
