#!/usr/bin/env python3
"""Bounded diagnostics, not proof or cycle search. Never stops at a palindrome."""
from pathlib import Path
import hashlib
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / "periodic_word_quotient__8404d0a63dd1fa13.py"
EXPECTED = "122fcd390283f956f97d21327ec6cb9d4ae193e9bd3ab1b155bb65e1e61c2425"
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
spec = importlib.util.spec_from_file_location("original_periodic", SOURCE)
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)
Z = (0, 0, 0, 0)


def quotient_without_safety(state):
    # The historical transition wrapper asserts safety. These diagnostics
    # explicitly use its original full/image/valid functions and literal slices
    # and stripping loops; they do not claim to execute that guarded wrapper.
    assert original.valid(state)
    B, H, w = state
    out, gamma = original.image(original.full(state, 3))
    rb = out[:len(B) + 4]
    rw = out[len(B) + 4:len(B) + 8]
    rh = out[len(B) + 8:len(B) + 8 + len(H) + 8 + gamma]
    assert out == original.full((rb, rh, rw), 1)
    u = v = 0
    while len(rb) >= 4 and rb[-4:] == rw:
        rb = rb[:-4]
        u += 1
    while len(rh) >= 8 and rh[:4] == rw and rh[-4:] == rw[::-1]:
        rh = rh[4:-4]
        v += 1
    target = rb, rh, rw
    assert original.valid(target)
    assert 2 * len(rb) + len(rh) + 8 * (u + v - 2) == 2 * len(B) + len(H) + gamma
    return target, u, v, gamma


def pair_of_integer(n):
    ds = tuple(map(int, str(n)[::-1]))
    return tuple(x + y for x, y in zip(ds, ds[::-1]))


def realize(q):
    assert q and q[0] > 0 and q == q[::-1] and max(q) <= 18
    ds = [0] * len(q)
    for i in range(len(q) // 2):
        ds[i] = max(q[i] - 9, 0)
        ds[-1-i] = q[i] - ds[i]
    if len(q) % 2:
        assert q[len(q) // 2] % 2 == 0
        ds[len(q) // 2] = q[len(q) // 2] // 2
    n = sum(d * 10**i for i, d in enumerate(ds))
    assert n > 0 and ds[-1] > 0 and max(ds) <= 9
    assert len(str(n)) == len(q) and pair_of_integer(n) == q
    assert 2 * sum(map(int, str(n))) == sum(q)
    return n


ZERO_STATES = [
    ((1,), (), Z), ((10,), (), Z), ((18,), (), Z),
    ((1, 0), (0,), Z), ((10, 0), (18,), Z),
    ((1, 18, 9), (2, 2), Z), ((11, 0), (18, 0, 18), Z),
    ((18, 9, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0), Z),
]
REALIZATIONS = ZERO_STATES + [
    ((), (), (1, 0, 9, 18)), ((), (2,), (9, 9, 9, 9)),
    ((1, 0), (), (0, 18, 9, 2)), ((10,), (2, 0, 2), (18, 18, 18, 18)),
]

pointwise = 0
for state in REALIZATIONS:
    assert original.valid(state)
    for k in (1, 3, 7):
        q = original.full(state, k)
        n = realize(q)
        successor = n + int(str(n)[::-1])
        image, _ = original.image(q)
        assert pair_of_integer(successor) == image
        pointwise += 1

clocks = set()
shifts = set()
trajectory_checks = 0
unsafe_sources = 0
max_width = 0
for initial in ZERO_STATES:
    # Fixed six-step trace to obtain a finite diagnostic M; no repeated-state
    # search or inference from lack of a repetition is performed.
    states = [initial]
    edges = []
    for _ in range(6):
        edge = quotient_without_safety(states[-1])
        assert edge[0][2] == Z
        edges.append(edge)
        states.append(edge[0])
    M = max(2 * len(s[0]) + len(s[1]) for s in states)
    mass_bound = max(2 * sum(s[0]) + sum(s[1]) for s in states)
    k = M + 3
    n = realize(original.full(initial, k))
    for state, (target, u, v, gamma) in zip(states, edges):
        q = original.full(state, k)
        assert k >= 3 and len(q) >= M + 24
        assert pair_of_integer(n) == q
        assert sum(q) == 2 * sum(state[0]) + sum(state[1]) <= mass_bound
        assert 2 * sum(map(int, str(n))) == sum(q)
        newk = (k - 2) + u + v
        targetq = original.full(target, newk)
        image, actual_gamma = original.image(q)
        assert actual_gamma == gamma and image == targetq
        assert len(targetq) == len(q) + gamma
        n = n + int(str(n)[::-1])
        assert pair_of_integer(n) == targetq
        clocks.add(gamma)
        shifts.add(u + v - 2)
        unsafe_sources += not original.safe(state)
        max_width = max(max_width, len(targetq))
        k = newk
        trajectory_checks += 1

assert clocks == {0, 1}
assert unsafe_sources > 0
assert not original.valid(((), (), Z))
assert not original.valid(((1,), (1,), Z))
assert not original.valid(((0,), (), Z))
print(json.dumps({
    "status": "PASS", "scope": "finite diagnostic controls only; no cycle search or theorem",
    "original_python_sha256": EXPECTED,
    "pointwise_realizations": pointwise,
    "fixed_seed_trajectory_steps": trajectory_checks,
    "zero_initial_states": len(ZERO_STATES), "steps_per_state": 6,
    "actual_carry_cases": sorted(clocks), "observed_signed_shifts": sorted(shifts),
    "unsafe_predecessor_steps_continued": unsafe_sources,
    "maximum_coefficient_width": max_width,
    "no_safety_assertion": True,
    "invalid_cases": ["empty zero exterior", "odd central coefficient", "zero outside head"],
}, indent=2))
