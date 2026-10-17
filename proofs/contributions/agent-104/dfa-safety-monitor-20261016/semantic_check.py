#!/usr/bin/env python3
"""Independent finite sanity check for the original four-state monitor.

This checks only all admissible symmetric q-words of lengths 1..7. It is
discovery/semantic evidence, NOT a proof of the universally quantified Lean
statement and NOT a substitute for the Lean kernel build.
"""
from itertools import product


def monitor_step(state, q):
    if state == 0:
        return 1 if q <= 9 else (2 if q == 11 else 3)
    if state == 1:
        return 1 if q <= 9 else 3
    if state == 2:
        return 2 if q in (0, 11) else 3
    return 3


def monitor_run(symbols):
    state = 0
    for q in symbols:
        state = monitor_step(state, q)
    return state


def bad_terminal(state, center):
    # The learner excludes none and some(0) before the first pair.
    if state == 0 and center in (None, 0):
        return False
    low = state in (0, 1)
    exceptional = state in (1, 2)
    return ((low and (center is None or center <= 9))
            or (exceptional and (center is None or center == 0)))


def bad_word(q):
    return (all(x <= 9 for x in q)
            or (q[0] == 11 and all(x in (0, 11) for x in q)))


def check_length(length):
    half_len = length // 2
    count = 0
    if half_len == 0:
        # For one digit, the positive even center is also q[0].
        for center in range(2, 19, 2):
            q = [center]
            assert bad_terminal(monitor_run([]), center) == bad_word(q), (q, center)
            count += 1
        return count
    for q0 in range(1, 19):
        for tail in product(range(19), repeat=half_len - 1):
            half = (q0,) + tail
            centers = [None] if length % 2 == 0 else list(range(2, 19, 2))
            for center in centers:
                q = list(half)
                if length % 2:
                    q.append(center)
                q += list(reversed(half))
                assert len(q) == length
                state = monitor_run(q[:half_len])
                actual_center = center if length % 2 else None
                assert bad_terminal(state, actual_center) == bad_word(q), (
                    length, q, state, actual_center,
                    bad_terminal(state, actual_center), bad_word(q))
                count += 1
    return count


if __name__ == "__main__":
    total = 0
    for length in range(1, 8):
        count = check_length(length)
        total += count
        print(f"length={length} checked={count} PASS")
    print(f"TOTAL checked={total} PASS")
