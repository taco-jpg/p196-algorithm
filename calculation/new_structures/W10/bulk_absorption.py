#!/usr/bin/env python3
"""Exact 120-phase carry-reset table for U=(4,9,14), rooted gamma=1000^30."""

def T(x, c):
    return int(x + c >= 10)

def F(w, gamma):
    """Exact cyclic bulk successor from the two-sided carry equations."""
    m = len(w)
    assert any(x != 9 for x in w)
    lo = [0] * m
    c = 0
    for _ in range(2):
        for x in w:
            c = T(x, c)
    lo[0] = c
    for i in range(1, m):
        lo[i] = T(w[i - 1], lo[i - 1])
    hi = [0] * m
    c = 0
    for _ in range(2):
        for x in reversed(w):
            c = T(x, c)
    hi[0] = c
    for i in range(m - 1, 0, -1):
        hi[i] = T(w[i], hi[(i + 1) % m])
    assert all(T(w[i], lo[i]) == lo[(i + 1) % m] for i in range(m))
    assert all(T(w[i], hi[(i + 1) % m]) == hi[i] for i in range(m))
    return tuple(
        (w[i] + lo[i]) % 10
        + ((w[i] + hi[(i + 1) % m]) % 10 if not gamma
           else (w[(i - 1) % m] + hi[i]) % 10)
        for i in range(m)
    )

def cones(rows):
    left = right = 0
    for t in range(120):
        w = rows[t]
        left += 1 + int(w[left % 3] == 9)
        right += 1 + int(w[(-right - 1) % 3] == 9) - int(t % 4 == 0)
    return left, right

def main():
    u0 = (4, 9, 14)
    rows = [u0]
    for t in range(120):
        rows.append(F(rows[-1], int(t % 4 == 0)))
    assert rows[-1] == u0
    assert len(set(rows)) == 30
    assert all(sum(w) == 27 and w.count(9) == 1 for w in rows)
    assert cones(rows) == (150, 120)
    # Every row is absorbing: its carry transfer forgets the inlet bit.
    for w in rows:
        outs = []
        for inlet in (0, 1):
            c = inlet
            for x in w:
                c = T(x, c)
            outs.append(c)
        assert outs[0] == outs[1]
    print("BULK_ABSORPTION_PASS phases=120 states=30 return=True one_9_per_phase=True")
    print("carry_reset=True; no phase is the all-9 neutral word")
    print("rot-2 T12 cone bounds: junction-side=150, centre-side=120; U^100 has 300 coefficients, leaving 30 protected")

if __name__ == "__main__":
    main()
