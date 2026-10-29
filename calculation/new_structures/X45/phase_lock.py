#!/usr/bin/env python3
"""X45: phase locking for cross-width moving seams in rooted p12/m9 T*.

Run from any working directory:
    python3 calculation/new_structures/X45/phase_lock.py

This is a differential control for the paper lemma in CELL_REPORT.md.  It
does NOT search for a complete seam return and does NOT claim a Lychrel seed.
"""
from pathlib import Path
import sys

sys.set_int_max_str_digits(10000)


def load_root():
    here = Path(__file__).resolve()
    repo = here.parents[3]
    data = repo / "calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt"
    rows = [
        [int(x) for x in line.split()]
        for line in data.read_text().splitlines()
        if line.strip()
    ]
    assert rows[0] == [12, 34, 9, 10]
    assert len(rows) >= 27
    assert len(rows[1]) == 12 and len(rows[2]) == 9 and len(rows[26]) == 34
    # Published layout: header, overflow clock, 12 W rows, 12 auxiliary rows,
    # then 12 B rows. Only the exact phase-zero B/W rows are needed to build
    # the source; the full 120-step orbit is recomputed independently below.
    return rows[26], rows[2]


def all_u3():
    out = []
    for a in range(0, 19, 2):
        word = (9, a, 18 - a)
        for shift in range(3):
            u = word[shift:] + word[:shift]
            if u not in out:
                out.append(u)
    assert len(out) == 30
    return out


def rotate_left(word, amount):
    amount %= len(word)
    word = list(word)
    return word[amount:] + word[:amount]


def bulk_step(U, gamma):
    """Exact cyclic U3 successor F_gamma from the two periodic carry maps."""
    U = list(U)
    m = len(U)
    low_solutions = []
    for initial in (0, 1):
        carry = initial
        for x in U:
            carry = (x + carry) // 10
        if carry == initial:
            low_solutions.append(initial)
    high_solutions = []
    for initial in (0, 1):
        beta = [0] * (m + 1)
        beta[m] = initial
        for i in range(m - 1, -1, -1):
            beta[i] = (U[i] + beta[i + 1]) // 10
        if beta[0] == initial:
            high_solutions.append(initial)
    assert len(low_solutions) == 1 and len(high_solutions) == 1
    alpha = [0] * (m + 1)
    alpha[0] = low_solutions[0]
    for i in range(m):
        alpha[i + 1] = (U[i] + alpha[i]) // 10
    beta = [0] * (m + 1)
    beta[m] = high_solutions[0]
    for i in range(m - 1, -1, -1):
        beta[i] = (U[i] + beta[i + 1]) // 10
    if gamma == 0:
        return [
            (U[i] + alpha[i]) % 10 + (U[i] + beta[i + 1]) % 10
            for i in range(m)
        ]
    return [
        (U[i] + alpha[i]) % 10 + (U[(i - 1) % m] + beta[i]) % 10
        for i in range(m)
    ]


def bulk_phase_rows(U):
    rows = [list(U)]
    current = list(U)
    for t in range(120):
        current = bulk_step(current, 1 if t % 4 == 0 else 0)
        rows.append(list(current))
    assert rows[120] == list(U)
    for delta in (-1, 1):
        for t in range(120):
            gamma = 1 if t % 4 == 0 else 0
            assert bulk_step(rotate_left(rows[t], delta), gamma) == rotate_left(rows[t + 1], delta)
    return rows


def insert_block(word, cut, block):
    return word[:cut] + list(block) + word[cut:]


def template_pairword(B, W, q, k, J, U, C):
    half = list(B) + list(W) * q + list(J) + list(U) * k
    p = half + list(C) + half[::-1]
    assert p == p[::-1]
    assert all(0 <= x <= 18 for x in p)
    assert list(C) == list(C)[::-1]
    if len(p) % 2:
        assert p[len(p) // 2] % 2 == 0
    return p


def realize_pairword(p):
    """Canonical decimal realization, digits stored least-significant first."""
    n = len(p)
    d = [0] * n
    for i in range(n // 2):
        x = p[i]
        d[i] = max(0, x - 9)
        d[n - 1 - i] = min(9, x)
    if n % 2:
        assert p[n // 2] % 2 == 0
        d[n // 2] = p[n // 2] // 2
    assert d[-1] != 0
    assert [d[i] + d[n - 1 - i] for i in range(n)] == p
    return d


def step_digit_array(d):
    """Fresh-buffer schoolbook n + reverse(n), no in-place read/write aliasing."""
    n = len(d)
    out = [0] * n
    carry = 0
    for i in range(n):
        s = d[i] + d[n - 1 - i] + carry
        out[i] = s % 10
        carry = s // 10
    if carry:
        out.append(carry)
    return out


def step_bigint(n):
    s = str(n)
    return n + int(s[::-1])


def digits_from_bigint(n):
    return [int(ch) for ch in str(n)[::-1]]


def pairword_from_digits(d):
    n = len(d)
    return [d[i] + d[n - 1 - i] for i in range(n)]


def check_one(B, W, U, q, k, direction, phase_rows):
    if direction == "3to4-even":
        J, C, Jp, Cp, delta = [5, 7, 12], [8, 8, 8, 8], [3, 14, 6, 10], [6, 6], 1
    elif direction == "4to3-even":
        J, C, Jp, Cp, delta = [5, 7, 12, 4], [6, 6], [3, 14, 6], [8, 8, 8, 8], -1
    elif direction == "3to4-odd":
        J, C, Jp, Cp, delta = [5, 7, 12], [8, 8, 8, 8, 8], [3, 14, 6, 10], [6, 8, 6], 1
    else:
        assert direction == "4to3-odd"
        J, C, Jp, Cp, delta = [5, 7, 12, 4], [6, 8, 6], [3, 14, 6], [8, 8, 8, 8, 8], -1

    assert 2 * len(J) + len(C) == 2 * len(Jp) + len(Cp)
    source = template_pairword(B, W, q, k, J, U, C)
    d = realize_pairword(source)
    assert d != d[::-1], ("palindromic source", U, q, k, direction)
    n = int("".join(map(str, d[::-1])))
    assert digits_from_bigint(n) == d
    overflow = []
    source_u_start = len(B) + len(W) * q + len(J)
    cut = source_u_start + 55 * len(U)

    for t in range(120):
        expected_now = [phase_rows[t][(i - cut) % 3] for i in range(cut - 3, cut + 6)]
        got_now = [d[i] + d[len(d) - 1 - i] for i in range(cut - 3, cut + 6)]
        assert got_now == expected_now, ("protected U phase failed", U, q, k, direction, t)
        d2 = step_digit_array(d)
        n2 = step_bigint(n)
        db = digits_from_bigint(n2)
        assert db == d2, (U, q, k, direction, t)
        overflow.append(len(d2) - len(d))
        assert d2 != d2[::-1], ("palindrome", U, q, k, direction, t + 1)
        d, n = d2, n2

    assert overflow == [1 if t % 4 == 0 else 0 for t in range(120)]
    assert sum(overflow) == 30
    out = pairword_from_digits(d)
    expected = [U[(i - source_u_start) % 3] for i in range(cut - 3, cut + 6)]
    assert out[cut - 3 : cut + 6] == expected, ("source U phase failed at 120", U, q, k, direction)
    U_rot = rotate_left(U, delta)
    target = template_pairword(B, W, q, k + 5, Jp, U_rot, Cp)
    assert len(target) == len(out)
    assert target[cut - 3 : cut + 6] == expected, ("forced rotated target failed", U, q, k, direction)

    target_unrotated = template_pairword(B, W, q, k + 5, Jp, U, Cp)
    assert target_unrotated[cut - 3 : cut + 6] != expected, ("unrotated U aligned", U, q, k, direction)

    # In every bulk phase, inserting U_t at c or its shifted rotation at c+delta
    # gives the same word. Reflection shifts the mirrored cut by -delta.
    for phase, u_t in enumerate(phase_rows[:120]):
        periodic = u_t * 12
        c = 12
        left_insert = insert_block(periodic, c, u_t)
        right_insert = insert_block(periodic, c + delta, rotate_left(u_t, delta))
        assert left_insert == right_insert, ("shifted insertion identity", U, phase, delta)
        reflected_left = insert_block(periodic[::-1], len(periodic) - c, u_t[::-1])
        reflected_right = insert_block(
            periodic[::-1], len(periodic) - (c + delta), rotate_left(u_t, delta)[::-1]
        )
        assert reflected_left == reflected_right, ("reflected insertion identity", U, phase, delta)
    return len(source), len(out)

def main():
    B, W = load_root()
    widths = [(20, 100), (40, 100), (80, 100), (160, 100)]
    trajectories = 0
    steps = 0
    digit_lengths = []
    for U in all_u3():
        phase_rows = bulk_phase_rows(U)
        for q, k in widths:
            for direction in ("3to4-even", "4to3-even", "3to4-odd", "4to3-odd"):
                before, after = check_one(B, W, U, q, k, direction, phase_rows)
                digit_lengths.append((before, after))
                trajectories += 1
                steps += 120
    print(
        "X45_PHASE_LOCK_PASS "
        f"U3={len(all_u3())} widths={len(widths)} directions=4 "
        f"trajectories={trajectories} exact_steps={steps} "
        f"digit_length_range={min(x[0] for x in digit_lengths)}.."
        f"{max(x[1] for x in digit_lengths)} "
        "checks=bigint-vs-digit-array,clock,palindrome-guard,even+odd-centres,all-phase-U-bulk,shifted-insertion"
    )


if __name__ == "__main__":
    main()

