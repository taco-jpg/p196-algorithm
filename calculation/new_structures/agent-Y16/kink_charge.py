#!/usr/bin/env python3
"""Exact all-width charge obstruction for the X23 period-3 decimal kink crystal.

No SAT caps, no fixed interface width.  The only finite classifications are
18 explicitly displayed periodic ring phases and their three spatial cuts.
Reproduce: python3 calculation/new_structures/agent-Y16/kink_charge.py
"""
B = (17, 5, 0, 1, 13, 4, 14, 12, 9, 8, 15, 16, 17, 13, 17, 9,
     1, 4, 4, 11, 8, 16, 0, 9, 14, 11, 9, 11, 6, 13, 18, 9,
     4, 7, 17, 15, 9, 7, 13)
W = (17, 3, 1, 13, 17, 11, 14, 3, 18, 1, 2, 0, 7, 3,
     14, 12, 15, 9, 7, 13)
BASE = 10

def cyclic_carries(row, forward):
    n = len(row)
    indices = range(n) if forward else range(n - 1, -1, -1)
    answers = []
    for initial in (0, 1):
        incoming, digits, c = [0] * n, [0] * n, initial
        for j in indices:
            incoming[j] = c
            digits[j] = (row[j] + c) % BASE
            c = (row[j] + c) // BASE
        if c == initial:
            answers.append((tuple(incoming), tuple(digits)))
    assert len(answers) == 1, (row, answers)
    return answers[0]

def ring_step(row, gamma):
    lo, dlo = cyclic_carries(row, True)
    hi, dhi = cyclic_carries(row, False)
    n = len(row)
    return tuple(dlo[j] + dhi[(j - gamma) % n] for j in range(n))

def periodic_ring():
    row = (8, 6, 8)
    for t in range(12):
        row = ring_step(row, 1 - (t & 1))
    assert row == (4, 14, 4)
    rows = []
    for t in range(18):
        rows.append(row)
        row = ring_step(row, 1 - (t & 1))
    assert row == rows[0] and len(set(rows)) == 18
    return tuple(rows)

def cut_charge(rows, phase, laps):
    """Return (Q for 3 cuts, number of exact column equations checked)."""
    period = 18 * laps
    assert period % 6 == 0
    values = [0] * 3
    equations = 0
    for t in range(period):
        at = (phase + t) % 18
        row = rows[at]
        next_row = rows[(at + 1) % 18]
        gamma = 1 - (at & 1)
        asc, da = cyclic_carries(row, True)
        desc, dd = cyclic_carries(row, False)
        lam = pow(2, -t, 9)  # multiplicative inverse of 2**t (not 2**(-t))
        for j in range(3):
            L, H, Y = asc[j], desc[(j - 1) % 3], dd[(j - 1) % 3]
            L_next, H_next, Y_next = asc[(j + 1) % 3], desc[j], dd[j]
            x, xnext = row[j], next_row[j]
            assert L_next == (x + L) // 10
            assert H == (x + H_next) // 10
            assert Y_next == (x + H_next) % 10
            if gamma:
                assert xnext == x + L + Y - 10 * L_next
            else:
                assert xnext == 2 * x + L + H_next - 10 * (L_next + H)
            values[j] += lam * (L - H + (Y if gamma else 0))
            equations += 1
    return tuple(v % 9 for v in values), equations

def root_charge(phase, length):
    result = 0
    for t in range(length):
        gamma = 1 - ((phase + t) & 1)
        L, H, Y = 0, gamma, 1
        result += pow(2, -t, 9) * (L - H + (Y if gamma else 0))
    return result % 9

def pairword(N):
    digits = tuple(map(int, str(N)[::-1]))
    return tuple(digits[i] + digits[-1 - i] for i in range(len(digits)))

def coeff_step(P):
    out, carry = [], 0
    for x in P:
        z = x + carry
        out.append(z % 10)
        carry = z // 10
    if carry:
        out.append(carry)
    return tuple(out[i] + out[-1 - i] for i in range(len(out)))

def canonical_seed(q, r):
    half = B + W * q + (4, 14, 4) * r
    p = half + half[::-1]
    n = len(p)
    digits = [0] * n
    for i, x in enumerate(half):
        digits[n - 1 - i] = x - min(9, x)
        digits[i] = min(9, x)
    s = ''.join(map(str, digits))
    assert s[0] != '0'
    result = int(s)
    assert pairword(result) == p
    return result, p

def independent_integer_check(rows, q, r, horizon=144):
    # Completely separate ordinary-bigint arithmetic vs pairword normalization.
    # Only probes the protected interior; this is a validation, not an infinity claim.
    N, P = canonical_seed(q, r)
    start = len(B) + len(W) * q
    j = start + 3 * (r // 2)
    assert start + 100 < j < start + 3 * r - 100
    for t in range(horizon + 1):
        assert pairword(N) == P, (t, 'full integer vs coefficient pairword')
        assert P[j] == rows[t % 18][(j - start) % 3], (t, 'interior ring')
        if t == horizon:
            break
        old_len = len(str(N))
        N = N + int(str(N)[::-1])
        assert len(str(N)) - old_len == 1 - (t & 1)
        P = coeff_step(P)
    return len(str(N))

def main():
    rows = periodic_ring()
    print('ring18:', ' '.join(''.join(f'{d:02d}' for d in row) for row in rows))
    for phase in range(18):
        assert root_charge(phase, 72) == root_charge(phase, 144) == 0
        q72, n72 = cut_charge(rows, phase, 4)
        q144, n144 = cut_charge(rows, phase, 8)
        q216, n216 = cut_charge(rows, phase, 12)
        expected72 = 3 if phase % 2 == 0 else 6
        assert q72 == (expected72,) * 3, (phase, q72)
        assert q144 == ((2 * expected72) % 9,) * 3
        assert q216 == (0, 0, 0)
        print(f'phase={phase:02d} cutQ72={q72} cutQ144={q144} cutQ216={q216}')
    # X23's distinct spatial-six 96-step crystal is charge-neutral: a live
    # alternative rather than an excluded route (not a positive certificate).
    six = (18, 12, 6, 6, 12, 18)
    six_rows = []
    for t in range(96):
        six_rows.append(six)
        six = ring_step(six, 1 - (t & 1))
    assert six == six_rows[0]
    q6 = []
    for j in range(6):
        charge = 0
        for t, row in enumerate(six_rows):
            asc, _ = cyclic_carries(row, True)
            desc, digits = cyclic_carries(row, False)
            charge += pow(2, -t, 9) * (asc[j] - desc[(j - 1) % 6]
                   + (digits[(j - 1) % 6] if t % 2 == 0 else 0))
        q6.append(charge % 9)
    assert q6 == [0] * 6
    print('m6 period-96 control charge:', tuple(q6))
    # No finite width can connect charge-0 root to charge-3/6 bulk for 72 or 144.
    for q, r in ((15, 180), (16, 181)):
        n = independent_integer_check(rows, q, r)
        print(f'independent_bigint q={q} r={r} t=144 final_digits={n} PASS')
    print('PASS: 18 time phases, 3 cuts, 72/144/216; 2 independent decimal seeds')
if __name__ == '__main__':
    main()