#!/usr/bin/env python3
"""Exact-integer controls for GeneralCarryMass's exterior model.
These controls are finite regression evidence, not a Lean proof.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
import json
from pathlib import Path

@dataclass(frozen=True)
class State:
    c: int
    B: tuple[int, ...]

def normalize(m: int, word: tuple[int, ...], carry: int) -> tuple[tuple[int, ...], int]:
    digits = []
    for coefficient in word:
        carry, digit = divmod(coefficient + carry, m + 1)
        digits.append(digit)
    return tuple(digits), carry

def overflow(m: int, s: State) -> int:
    return normalize(m, s.B[::-1], int(m + 1 <= s.c))[1]

def raw_step(m: int, s: State) -> State:
    k = int(m + 1 <= s.c)
    low, carry_low = normalize(m, s.B, 0)
    high, carry_high = normalize(m, s.B[::-1], k)
    t = s.c - m * k
    u = s.c + carry_low - (m + 1) * k
    other = high[::-1] + (t,) if carry_high == 0 else (1,) + high[::-1]
    assert len(low) + 1 == len(other)
    return State(2 * t, tuple(a + b for a, b in zip(low + (u,), other)))

def step(m: int, s: State) -> State:
    out = raw_step(m, s)
    word = out.B
    while word and word[-1] == out.c:
        word = word[:-1]
    return State(out.c, word)

def phase(m: int, c: int) -> bool:
    return 0 < c < 2 * m and c != m

def bounded(m: int, s: State) -> bool:
    return all(0 <= a <= 2 * m for a in s.B)

def positive(s: State) -> bool:
    return not s.B or s.B[0] > 0

def outer_head(s: State) -> int:
    return s.B[0] if s.B else s.c

def moment(s: State) -> int:
    return 2 * sum(a if i % 2 == 0 else -a for i, a in enumerate(s.B)) + (-1) ** len(s.B) * s.c

def snapshot(s: State) -> dict:
    return {'c': s.c, 'B': list(s.B), 'moment': moment(s)}

def main() -> None:
    counts = {'initial_states': 0, 'tested_steps': 0, 'positive_paths': 0}
    failures = []
    latest_first_overflow = -1
    latest_witness = None
    for m, max_width in [(1, 3), (3, 4), (5, 3), (7, 3), (9, 3), (11, 2)]:
        for width in range(max_width + 1):
            for B in product(range(2 * m + 1), repeat=width):
                for c in (c for c in range(1, 2 * m) if c != m):
                    s = State(c, B)
                    counts['initial_states'] += 1
                    after = raw_step(m, s)
                    assert phase(m, after.c)
                    assert bounded(m, after), (m, s, after)
                    seen_overflow = False
                    first_overflow = None
                    initial_positive = positive(s)
                    if initial_positive:
                        counts['positive_paths'] += 1
                    trajectory = [snapshot(s)]
                    # Six post-initial states suffice for the decimal sharp bound;
                    # all bases below 13 are controlled for eight transitions.
                    for t in range(8):
                        assert phase(m, s.c) and bounded(m, s)
                        g = overflow(m, s)
                        assert g in (0, 1)
                        out = step(m, s)
                        assert phase(m, out.c) and bounded(m, out)
                        if initial_positive:
                            assert positive(out)
                            if g == 0:
                                assert 2 * outer_head(s) <= outer_head(out)
                                assert outer_head(s) <= m
                        modulus = 2 * (m + 2)
                        assert moment(out) % modulus == (0 if g else 2 * moment(s) % modulus)
                        if g:
                            seen_overflow = True
                            if first_overflow is None:
                                first_overflow = t
                        if seen_overflow:
                            assert moment(out) % modulus == 0
                        trajectory.append(snapshot(out))
                        counts['tested_steps'] += 1
                        s = out
                    if initial_positive:
                        bound = m.bit_length()  # smallest h with 2**h > m
                        assert first_overflow is not None and first_overflow <= bound
                        if m == 9 and first_overflow > latest_first_overflow:
                            latest_first_overflow = first_overflow
                            latest_witness = {'m': m, 'start': {'c': c, 'B': list(B)}, 'trace': trajectory,
                                              'first_overflow_transition_index': first_overflow}
    # Neutral phases are deliberately excluded: the dropped hypothesis is false.
    neutral = State(9, (1, 18))
    neutral_raw = raw_step(9, neutral)
    neutral_out = step(9, neutral)
    assert not bounded(9, neutral_out)
    report = {
        'status': 'FINITE_CONTROLS_PASS_NOT_FORMAL_VERIFICATION',
        'counts': counts,
        'odd_m_cases': [1, 3, 5, 7, 9, 11],
        'phase_domain': 'all integer c with 0 < c < 2*m and c != m',
        'width_caps': {'1': 3, '3': 4, '5': 3, '7': 3, '9': 3, '11': 2},
        'transitions_per_initial_state': 8,
        'decimal_sharpness': latest_witness,
        'neutral_phase_counterexample': {'start': snapshot(neutral), 'raw_successor': snapshot(neutral_raw),
                                         'trimmed_successor': snapshot(neutral_out)},
        'lean_build': 'NOT_RUN_NO_COMPILER_AVAILABLE',
        'remote_publication': 'NOT_PERFORMED_NO_WRITE_ACTION_AVAILABLE'
    }
    path = Path(__file__).with_name('model_controls.json')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'counts': counts, 'max_first_decimal_overflow_index': latest_first_overflow,
                      'decimal_start': latest_witness['start'] if latest_witness else None,
                      'neutral_counterexample': report['neutral_phase_counterexample']}, indent=2))

if __name__ == '__main__':
    main()
