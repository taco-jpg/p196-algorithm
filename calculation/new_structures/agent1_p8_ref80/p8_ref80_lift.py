#!/usr/bin/env python3
"""Exact all-centre p8/m20 80-step shield, sufficient for a one-width all-time lift.
Run from repository root: python3 calculation/new_structures/agent1_p8_ref80/p8_ref80_lift.py
Only standard-library Python and the EXISTING N10 phase.json are used.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PHASE = ROOT / 'calculation/new_structures/agent-N10/phase.json'

def step(prefix):
    """Universal common prefix of a true daughter, for any unknown symmetric tail.
    All possible inward high carries (0,1) are explicitly enumerated.
    Caller proves prefix length k lies at least two sites below the midpoint.
    """
    k = len(prefix)
    low, carry = [], 0
    for x in prefix:
        v = x + carry
        low.append(v % 10)
        carry = v // 10
    outcomes = []
    for incoming in (0, 1):
        high = [0] * k
        carry = incoming
        for i in range(k - 1, -1, -1):
            v = prefix[i] + carry
            high[i] = v % 10
            carry = v // 10
        gamma = carry
        if gamma:
            out = [low[0] + 1] + [low[i] + high[i - 1] for i in range(1, k)]
        else:
            out = [low[i] + high[i] for i in range(k)]
        outcomes.append((gamma, out))
    assert outcomes[0][0] == outcomes[1][0], 'clock not universally forced'
    a, b = outcomes[0][1], outcomes[1][1]
    m = next((i for i in range(k) if a[i] != b[i]), k)
    return outcomes[0][0], a[:m]

def check():
    data = json.loads(PHASE.read_text())
    B, W = data['phase_B'], data['phase_W']
    assert len(B) == len(W) == 8
    assert all(len(x) == 39 for x in B)
    assert all(len(x) == 20 for x in W)
    assert data['gammas'] == [1,0,1,0,1,0,1,0]
    assert B[0][0] == 17
    assert all(any(x % 2 for x in row) for row in B)
    # Minimal reference q=5, minimal centre length 4; any larger centre
    # increases n, never affecting the two-inlet prefix computation.
    p = B[0] + W[0] * 5
    n = 2 * len(p) + 4
    rows = []
    for t in range(81):
        assert len(p) + 2 <= n // 2, (t, len(p), n)
        assert p[:59] == B[t % 8] + W[t % 8], (t, 'root mismatch')
        rows.append((t, len(p), n))
        if t == 80: break
        gamma, p = step(p)
        assert gamma == data['gammas'][t % 8], (t, gamma)
        n += gamma
    assert rows[0][1] == 139 and rows[-1][1] == 77
    assert rows[-1][2] == 322
    print('PAPER-PROOF finite kernel PASS: 81/81 rooted phase states,')
    print('80/80 universally forced clock bits; 40 overflows; prefix 139->77,')
    print('all centres |C|>=4; all q>=5 by published N10 insertion theorem.')
    print('Conditional infinite criterion: one actual 80-step P(q,C)->P(q+1,C)')
    print('at ANY q>=5 implies all q>=that q and permanent nonpalindromicity.')
    return rows

if __name__ == '__main__':
    check()
