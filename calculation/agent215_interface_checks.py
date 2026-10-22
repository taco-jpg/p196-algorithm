#!/usr/bin/env python3
"""Focused checks for REPORT_215.md; this does not search for Lychrel seeds."""
from dataclasses import dataclass
from math import gcd
import random
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def norm(word, incoming=0):
    digits, carry, carry_sum = [], incoming, 0
    for symbol in word:
        digit, carry = (symbol + carry) % 10, (symbol + carry) // 10
        digits.append(digit)
        carry_sum += carry
    return digits, carry, carry_sum


def pair(word):
    return [a + b for a, b in zip(word, reversed(word))]


def zipper(left, right):
    assert len(left) == len(right)
    return [a + b for a, b in zip(left, right)]


def stable(symbol):
    assert 0 <= symbol <= 18 and symbol != 9
    carry = int(symbol >= 10)
    return carry, symbol - 9 * carry


@dataclass
class State:
    phases: list
    blocks: list
    center: list
    lengths: list

    def expand(self):
        half = []
        for block, symbol, size in zip(self.blocks, self.phases, self.lengths):
            half.extend(block)
            half.extend([symbol] * size)
        return half + self.center + half[::-1]

    def width(self):
        return 2 * (sum(map(len, self.blocks)) + sum(self.lengths)) + len(self.center)


def raw_step(state):
    """The exact general-r block formulas, with all outgoing carries summed."""
    assert min(state.lengths) >= 2
    phases, blocks, center = state.phases, state.blocks, state.center
    r = len(phases)
    k = [stable(s)[0] for s in phases]
    t = [stable(s)[1] for s in phases]
    following = [2 * z for z in t]
    d, u, kd = norm(blocks[0], 0)
    e, gamma, ke = norm(blocks[0][::-1], k[0])
    entrance = phases[0] + u - 10 * k[0]
    right = e[::-1] + [t[0]] if gamma == 0 else [1] + e[::-1]
    out = [zipper(d + [entrance], right)]
    epsilon = 2 - gamma
    assert sum(out[0]) == 2 * sum(blocks[0]) + epsilon * t[0] - 9 * (kd + ke)
    for j in range(1, r):
        a, b, block = phases[j - 1], phases[j], blocks[j]
        ka, kb, ta, tb = k[j - 1], k[j], t[j - 1], t[j]
        d, u, kd = norm(block, ka)
        e, v, ke = norm(block[::-1], kb)
        left = d + [b + u - 10 * kb]
        right = [a + v - 10 * ka] + e[::-1]
        if gamma == 0:
            left, right = [ta] + left, right + [tb]
        raw = zipper(left, right)
        assert len(raw) == len(block) + epsilon
        assert sum(raw) == 2 * sum(block) + epsilon * (a + b) - 9 * (
            epsilon * (ka + kb) + kd + ke)
        charge = 2 * sum(block) - (a + b) * len(block)
        raw_charge = 2 * sum(raw) - (following[j - 1] + following[j]) * len(raw)
        assert raw_charge == 2 * charge + 18 * ((ka + kb) * len(block) - kd - ke)
        out.append(raw)
    d, u, kd = norm(center, k[-1])
    central_digits = d + [phases[-1] + u - 10 * k[-1]]
    if gamma == 0:
        central_digits = [t[-1]] + central_digits
    central = pair(central_digits)
    assert len(central) == len(center) + epsilon
    assert sum(central) == 2 * sum(center) + epsilon * following[-1] - 18 * kd
    result = State(following, out, central, [n - epsilon for n in state.lengths])
    assert result.width() == state.width() + gamma
    return result, gamma


def trim(state):
    """Move actual end letters to adjacent bands; no guessed transitions."""
    phases = state.phases[:]
    blocks = [b[:] for b in state.blocks]
    center, lengths = state.center[:], state.lengths[:]
    while blocks[0] and blocks[0][-1] == phases[0]:
        blocks[0].pop()
        lengths[0] += 1
    for j in range(1, len(phases)):
        while blocks[j] and blocks[j][0] == phases[j - 1]:
            blocks[j].pop(0)
            lengths[j - 1] += 1
        while blocks[j] and blocks[j][-1] == phases[j]:
            blocks[j].pop()
            lengths[j] += 1
    while len(center) >= 2 and center[0] == center[-1] == phases[-1]:
        center = center[1:-1]
        lengths[-1] += 1
    return State(phases, blocks, center, lengths)


def invariants(state):
    result = {}
    s, b = state.phases[0], state.blocks[0]
    if gcd(s, 9) == 1:
        result["J"] = (2 * pow(s, -1, 9) * (sum(b) - s * len(b)) + state.width()) % 9
    for j in range(1, len(state.phases)):
        a, b = state.phases[j - 1:j + 1]
        difference = a - b
        if gcd(difference, 9) != 1:
            continue
        block = state.blocks[j]
        inner = 2 * sum(state.lengths[j:]) + 2 * sum(map(len, state.blocks[j + 1:])) + len(state.center)
        charge = 2 * sum(block) - (a + b) * len(block)
        result[f"I{j}"] = (pow(difference, -1, 9) * charge - len(block) - inner) % 9
    return result


def realize(q):
    assert q and q == q[::-1] and q[0] > 0
    d = [0] * len(q)
    for i in range(len(q) // 2):
        d[-1 - i] = min(9, q[i])
        d[i] = q[i] - d[-1 - i]
    if len(q) % 2:
        assert q[len(q) // 2] % 2 == 0
        d[len(q) // 2] = q[len(q) // 2] // 2
    assert pair(d) == q and d[-1] > 0
    return int("".join(map(str, d[::-1])))


def check_normalization():
    count = 0
    for s in range(19):
        for incoming in range(2):
            for length in (1, 2, 7):
                digits, outgoing, _ = norm([s] * length, incoming)
                if s == 9:
                    expected, last = [9 * (1 - incoming)] * length, incoming
                else:
                    k, t = stable(s)
                    expected, last = [t + incoming - k] + [t] * (length - 1), k
                assert (digits, outgoing) == (expected, last)
                count += 1
    print(f"normalization: {count} symbol/carry/length cases passed")


def check_templates():
    rng = random.Random(215)
    alphabet = [s for s in range(19) if s != 9]
    invariant_counts = {"J": 0, "I": 0}
    for _ in range(1000):
        r = rng.randrange(1, 5)
        phases = [rng.choice(alphabet) for _ in range(r)]
        blocks = [[rng.randrange(19) for _ in range(rng.randrange(6))] for _ in range(r)]
        if blocks[0]:
            blocks[0][0] = rng.randrange(1, 19)
        elif phases[0] == 0:
            blocks[0] = [1]
        half = [rng.randrange(19) for _ in range(rng.randrange(4))]
        middle = [2 * rng.randrange(10)] if rng.randrange(2) else []
        state = State(phases, blocks, half + middle + half[::-1], [rng.randrange(2, 14) for _ in range(r)])
        q = state.expand()
        old = invariants(state)
        raw, gamma = raw_step(state)
        digits, actual_gamma, _ = norm(q)
        output = digits + ([1] if actual_gamma else [])
        assert gamma == actual_gamma and pair(output) == raw.expand()
        short = State(phases, blocks, state.center, [2] * r)
        short_digits, short_gamma, _ = norm(short.expand())
        short_output = short_digits + ([1] if short_gamma else [])
        assert short_gamma == gamma
        assert (output == output[::-1]) == (short_output == short_output[::-1])
        canonical = trim(raw)
        assert canonical.expand() == raw.expand()
        assert old == invariants(canonical)
        invariant_counts["J"] += int("J" in old)
        invariant_counts["I"] += sum(key.startswith("I") for key in old)
        integer = realize(q)
        integer += int(str(integer)[::-1])
        assert list(map(int, str(integer)[::-1])) == output
    print(f"templates: 1000 seeded cases passed; J checks={invariant_counts['J']}; I checks={invariant_counts['I']}")


def check_long_orbit():
    state = State([2, 4, 2], [[1, 9, 10], [7, 9, 11], [4, 9, 12]], [8, 6, 8], [2002, 2003, 2004])
    integer = realize(state.expand())
    start_width = state.width()
    initial_invariants = invariants(state)
    overflows, palindromes = 0, 0
    for _ in range(1000):
        old_width = state.width()
        raw, gamma = raw_step(state)
        integer += int(str(integer)[::-1])
        digits = list(map(int, str(integer)[::-1]))
        assert pair(digits) == raw.expand()
        assert len(digits) == old_width + gamma
        assert invariants(raw) == initial_invariants
        palindromes += int(digits == digits[::-1])
        overflows += gamma
        state = raw
    print(f"orbit calibration: 1000 exact steps passed; width {start_width}->{state.width()}; overflows={overflows}; palindromic outputs={palindromes}")
    print(f"orbit final: protected lengths={state.lengths}; block lengths={list(map(len, state.blocks))}; center length={len(state.center)}")
    print("orbit scope: raw blocks grew; protected runs shrank; no returning construction is claimed")


def check_outer_potential():
    h = [0, 0, 0, 0, 1, 0, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 3]
    rows = []
    for a in range(1, 19):
        slacks = []
        for incoming in range(2):
            gamma = (a + incoming) // 10
            following = 2 * a + incoming if gamma == 0 else a % 10 + 1
            slack = 1 - 2 * gamma + h[a] - h[following]
            assert slack >= 0
            slacks.append(slack)
        rows.append(tuple(slacks))
    print("outer potential: all 36 exact transitions passed")
    print(f"outer potential slacks, a=1..18: {rows}")


def minimum_gains(phases):
    divisors = [9 // gcd(phases[0], 9)] + [9 // gcd(a - b, 9) for a, b in zip(phases, phases[1:])]
    suffix, gains = 0, [0] * len(phases)
    for j in reversed(range(len(phases))):
        current = divisors[j] * (suffix // divisors[j] + 1)
        gains[j], suffix = current - suffix, current
    return divisors, gains, suffix


def check_algebra():
    transient = permutation = ray = (10, 10)
    for _ in range(1000):
        x, y = transient
        transient = (x + y, 1)
        x, y = permutation
        permutation = (y + 2, x - 1)
        x, y = ray
        ray = (2 * x - y + 1, -x + 2 * y + 1)
        assert min(transient + permutation + ray) > 0
    print(f"algebra, 1000 steps: transient={transient}; permutation={permutation}; ray-only={ray}")
    x = (10, 10)
    first_failure = None
    for step in range(1, 1001):
        x = (x[0] - 1, x[1] + 2)
        if x[0] < 0 and first_failure is None:
            first_failure = step
    print(f"positive total drift counterexample: first negative coordinate at return {first_failure}; endpoint={x}")
    for phases in ([2], [2, 6], [2, 8], [2, 6, 10], [2, 8, 14]):
        divisors, gains, total = minimum_gains(phases)
        print(f"arithmetic only: phases={phases}; D={divisors}; min gains={gains}; base period bound={4 * total}")


def check_guard_formula():
    matrix = [
        [0, 1, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    weights = (1, 1, 2, 2, 2, 3, 6)
    offset = (3, -2, -4, 5, 1, -3, 2)
    u, period = 7, 6

    def multiply(vector):
        return tuple(sum(a * b for a, b in zip(row, vector)) for row in matrix)

    def add(left, right):
        return tuple(a + b for a, b in zip(left, right))

    assert tuple(sum(weights[i] * matrix[i][j] for i in range(7)) for j in range(7)) == weights
    drift, vector = (0,) * 7, offset
    for t in range(u + period):
        if t >= u:
            drift = add(drift, vector)
        vector = multiply(vector)
    values = [(10, 12, 14, 16, 18, 20, 22)]
    for _ in range(1000):
        values.append(add(multiply(values[-1]), offset))
    for residue in range(period):
        for n in range((1000 - u - residue) // period + 1):
            assert values[u + residue + n * period] == tuple(
                x + n * d for x, d in zip(values[u + residue], drift))
    assert min(min(x) for x in values) > 0
    assert all(x[5] - x[0] >= -100 for x in values[:u + period])
    failure = next(t for t, x in enumerate(values) if x[5] - x[0] < -100)
    print(f"guard formula, 1000 steps: u={u}; p={period}; D={drift}; endpoint={values[-1]}")
    print(f"guard counterexample: finite prefix passes; drift=-6; first failure={failure}")


def main():
    check_normalization()
    check_templates()
    check_long_orbit()
    check_outer_potential()
    check_algebra()
    check_guard_formula()
    print("ALL AGENT 215 CHECKS PASSED")


if __name__ == "__main__":
    main()
