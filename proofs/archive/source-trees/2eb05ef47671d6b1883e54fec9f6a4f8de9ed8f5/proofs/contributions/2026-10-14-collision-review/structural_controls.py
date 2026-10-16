#!/usr/bin/env python3
"""Finite controls of the all-width statements in COLLISION_REVIEW.md."""

from itertools import product
import json
from pathlib import Path


def admissible(q):
    return (bool(q) and 0 < q[0] <= 18 and q == q[::-1]
            and all(0 <= x <= 18 for x in q)
            and (len(q) % 2 == 0 or q[len(q) // 2] % 2 == 0))


def ordinary_normal(q):
    value = 0
    for x in reversed(q):
        value = 10 * value + x
    return tuple(map(int, str(value)[::-1]))


def update(q):
    d = ordinary_normal(q)
    return tuple(a + b for a, b in zip(d, reversed(d)))


def bad(q):
    return (max(q) <= 9 or (q[0] == 11 and all(x in (0, 11) for x in q)))


def decompositions(q):
    """All canonical B 0^g H 0^g B^R decompositions with g>=1."""
    assert admissible(q)
    result = []
    for width in range(1, len(q) // 2):
        if q[width] != 0 or not admissible(q[:width]):
            continue
        end = width
        while end < len(q) and q[end] == 0:
            end += 1
        if 2 * end < len(q):
            h = q[end:len(q) - end]
            assert admissible(h)
            result.append(dict(exterior_width=width, gap=end - width, core_width=len(h)))
    return result


def small_words():
    yield from ((x,) for x in range(2, 19, 2))
    yield from ((x, x) for x in range(1, 19))
    yield from ((x, c, x) for x in range(1, 19) for c in range(0, 19, 2))


def check_zero_gap():
    cases = 0
    words = list(small_words())
    for b, h in product(words, repeat=2):
        bd, hd = ordinary_normal(b), ordinary_normal(h)
        e, f = len(bd) - len(b), len(hd) - len(h)
        rhs = e == f and bd == bd[::-1] and hd == hd[::-1]
        for gap in (0, 1, 2):
            q = b + (0,) * gap + h + (0,) * gap + b
            d = ordinary_normal(q)
            assert (d == d[::-1]) == rhs == bad(q)
            cases += 1
    return cases


def check_positive_family():
    for width in range(3, 201):
        expected = [
            (18,) * width,
            (9,) + (18,) * (width - 1) + (9,),
            (10, 8) + (18,) * (width - 2) + (8, 10),
            (1, 9, 17) + (18,) * (width - 3) + (17, 9, 1),
        ]
        for index, q in enumerate(expected):
            assert admissible(q) and min(q) > 0 and not bad(q)
            assert not decompositions(q)
            if index < 3:
                assert update(q) == expected[index + 1]
    return dict(widths=[3, 200], checked_width_count=198, states_per_width=4)


def check_gate_resets():
    # Small driver computed with an independent integer normalization.
    b, h, loss, t = (1, 1), (1, 8, 14, 8, 1), 0, 0
    collisions = {0: (t, b, h)}
    while loss < 31:
        bd, hd = ordinary_normal(b), ordinary_normal(h)
        e, f = len(bd) - len(b), len(hd) - len(h)
        delta = max(e, f)
        core = [0] * (len(h) + 2 * delta - e)
        for i, x in enumerate(hd):
            core[delta - e + i] += x
            core[len(h) + delta - 1 - i] += x
        b = tuple(a + c for a, c in zip(bd, bd[::-1]))
        h = tuple(core)
        t += 1
        loss += delta
        collisions.setdefault(loss, (t, b, h))
    result = []
    for r in range(1, 33):
        time, b, h = collisions[r - 1]
        q = b + h + b
        states = []
        for offset in range(4):
            states.append(dict(offset=offset, pair_word=q, next_iterate_palindromic=bad(q),
                               resets=decompositions(q)))
            q = update(q)
        result.append(dict(r=r, first_zero_gap_time=time, states=states))
    return result


def exploratory_merge_check():
    # The exterior B-driver is the pair-word orbit of the seed 10.
    # Test a proposed finite reduction to the 196 orbit; absent finite
    # intersection is not an obstruction to a later merger.
    left, right = 10, 196
    left_states, right_states = {}, {}
    for t in range(1001):
        left_states[left] = t
        right_states[right] = t
        if t < 1000:
            left += int(str(left)[::-1])
            right += int(str(right)[::-1])
    shared = sorted(left_states.keys() & right_states.keys())
    return dict(seeds=[10, 196], tested_times=[0, 1000],
                exact_shared_states=[dict(value=str(x), first_seed_time=left_states[x],
                                          second_seed_time=right_states[x]) for x in shared],
                final_widths=[len(str(left)), len(str(right))],
                conclusion="No reduction found in this window; later merging remains unexcluded.")


def main():
    result = dict(
        status="all finite structural controls passed",
        zero_gap_palindrome_equivalence_cases=check_zero_gap(),
        positive_family_controls=check_positive_family(),
        remaining_gate_short_reset_controls=check_gate_resets(),
        exploratory_merge_check=exploratory_merge_check(),
        scope="Universal claims have written proofs; finite gate reset observations do not imply recurrence.",
    )
    destination = Path(__file__).with_name("structural_controls.json")
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(status=result["status"],
                          zero_gap_cases=result["zero_gap_palindrome_equivalence_cases"],
                          positive_family_widths=198, gate_parameters=32)))


if __name__ == "__main__":
    main()
