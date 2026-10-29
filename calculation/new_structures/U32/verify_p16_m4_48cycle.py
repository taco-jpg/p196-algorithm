#!/usr/bin/env python3
"""Reproduce the U32 base-10 p16/m4 three-cycle charge obstruction.

Pure Python standard library. This checks the exact cyclic carry row map by a
second carry solver, exhausts all 19**4 rows for the 16-step map, checks the
48-phase mod-9 cut charge on all primitive reflection-symmetric 3-cycles, and
cross-checks the row dynamics against two independent ordinary-integer
reverse-and-add engines at band widths q=20,40,80,160.

The bigint runs are controls for the bulk row map only. Their actual overflow
clock is measured, not assumed to be (01)^24; they are not Lychrel evidence.
"""
from collections import Counter

B = 10
M = 4
P = 16
CLOCK = tuple(t & 1 for t in range(P))


def low_carry_solutions(row):
    """Solve A[i+1]=floor((row[i]+A[i])/10) cyclically by trying A[0]."""
    m = len(row)
    sols = []
    for a0 in (0, 1):
        a = a0
        carries = [a0]
        for i in range(m):
            a = (row[i] + a) // B
            carries.append(a)
        if a == a0:
            sols.append(carries[:-1])
    return sols


def high_carry_solutions(row):
    """Solve D[i-1]=floor((row[i]+D[i])/10), cyclically, from each D[0]."""
    m = len(row)
    sols = []
    for d0 in (0, 1):
        d = [None] * m
        d[0] = d0
        carry = d0
        for j in range(m):
            i = (-j) % m
            prev = (i - 1) % m
            carry = (row[i] + carry) // B
            d[prev] = carry
        if carry == d0:
            sols.append(d)
    return sols


def phi(row, gamma):
    """Exact cyclic bulk row map, using independently solved cyclic carries."""
    row = tuple(row)
    if all(x == 9 for x in row):
        return None
    aa = low_carry_solutions(row)
    dd = high_carry_solutions(row)
    assert len(aa) == len(dd) == 1, (row, aa, dd)
    A, D = aa[0], dd[0]
    low = [(row[i] + A[i]) % B for i in range(len(row))]
    high = [(row[i] + D[i]) % B for i in range(len(row))]
    out = tuple(low[i] + (high[(i - 1) % len(row)] if gamma else high[i])
                for i in range(len(row)))
    return out, A, D


def encode(row):
    value = 0
    for x in reversed(row):
        value = value * 19 + x
    return value


def decode(value):
    row = []
    for _ in range(M):
        row.append(value % 19)
        value //= 19
    return tuple(row)


def reflection_axes(row):
    return [a for a in range(M)
            if all(row[i] == row[(a - i) % M] for i in range(M))]


def primitive_m4(row):
    return all(any(row[i] != row[(i + d) % M] for i in range(M))
               for d in (1, 2))


def enumerate_functional_graph():
    size = 19 ** M
    next_state = [-1] * size
    valid = 0
    dead = 0
    for code in range(size):
        row = decode(code)
        for gamma in CLOCK:
            result = phi(row, gamma)
            if result is None:
                break
            row = result[0]
        else:
            next_state[code] = encode(row)
            valid += 1
             continue
        dead += 1

    status = [0] * size
    pos = [-1] * size
    cycles = []
    for start in range(size):
        if status[start]:
            continue
        path = []
        cur = start
        while cur >= 0 and status[cur] == 0:
            status[cur] = 1
            pos[cur] = len(path)
            path.append(cur)
            cur = next_state[cur]
        if cur >= 0 and status[cur] == 1 and pos[cur] >= 0:
            cycles.append([decode(x) for x in path[pos[cur]:]])
        for x in path:
            status[x] = 2
            pos[x] = -1

    primitive_reflected_fixed = []
    primitive_reflected_3cycles = []
    for cycle in cycles:
        if len(cycle) == 1 and reflection_axes(cycle[0]) and primitive_m4(cycle[0]):
            primitive_reflected_fixed.append(cycle)
        if len(cycle) == 3 and any(reflection_axes(row) and primitive_m4(row) for row in cycle):
            assert all(reflection_axes(row) and primitive_m4(row) for row in cycle)
            primitive_reflected_3cycles.append(cycle)
    assert (size, valid, dead) == (130321, 128126, 2195)
    assert len(cycles) == 110
    assert Counter(map(len, cycles)) == Counter({1: 60, 3: 50})
    assert len(primitive_reflected_fixed) == 48
    assert len(primitive_reflected_3cycles) == 16
    return primitive_reflected_3cycles, primitive_reflected_fixed, (size, valid, dead, len(cycles))


def phase48(cycle):
    """Lift a 3-cycle of the 16-step map to its exact 48-phase row orbit."""
    rows = []
    row = tuple(cycle[0])
    for epoch in range(3):
        for t in range(P):
            rows.append(row)
            result = phi(row, t & 1)
            assert result is not None
            row = result[0]
        assert row == tuple(cycle[(epoch + 1) % 3])
    assert len(rows) == 48 and row == tuple(cycle[0])
    return rows


def cut_state(rows, k):
    low_carries, high_carries, ydigits = [], [], []
    for t, row in enumerate(rows):
        result = phi(row, t & 1)
        assert result is not None
        _, A, D = result
        low_carries.append(A[k])
        # H_t is the carry passed from this coefficient toward the lower side.
        high_carries.append((row[k] + D[k]) // B)
        if t & 1:
            ydigits.append((row[(k - 1) % M] + D[(k - 1) % M]) % B)
    assert len(low_carries) == len(high_carries) == 48 and len(ydigits) == 24
    return low_carries, high_carries, ydigits


def charge9(state):
    """Q(S)=sum 5nt (L_t-H_t+gamma_t Y_t) mod 9 for the 48-phase clock."""
    L, H, Y = state
    yi = 0
    q = 0
    for t in range(48):
        gamma = t & 1
        y = Y[yi] if gamma else 0
        if gamma:
            yi += 1
        q = (q + pow(5, t, 9) * (L[t] - H[t] + gamma * y)) % 9
    assert yi == 24
    return q


def tonum_lsd(digits):
    value = 0
    for digit in reversed(digits):
        value = value * 10 + digit
    return value


]yúZŠ¼(­Ó