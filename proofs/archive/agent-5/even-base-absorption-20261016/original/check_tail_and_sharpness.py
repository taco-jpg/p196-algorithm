#!/usr/bin/env python3
"""Exact finite controls for recurring overflow and necessary hypotheses.

No random sampling, floating-point arithmetic, or proof-status upgrades are used.
"""
from __future__ import annotations
from itertools import product
from pathlib import Path
import json
from check_model import State, step, overflow, moment, phase, outer_head, snapshot


def trace(m: int, initial: State, transitions: int) -> list[dict]:
    rows = []
    s = initial
    for t in range(transitions + 1):
        rows.append({'time': t, **snapshot(s), 'residue': moment(s) % (2*(m+2)),
                     'next_overflow': overflow(m, s), 'head': outer_head(s)})
        s = step(m, s)
    return rows


def main() -> None:
    count = windows = steps = 0
    transitions = 30
    for m in (3, 5, 9, 11):
        H = m.bit_length()
        for width in range(3):
            for B in product(range(2*m + 1), repeat=width):
                if B and B[0] == 0:
                    continue
                for c in range(1, 2*m):
                    if c == m:
                        continue
                    s = State(c, B)
                    gs = []
                    count += 1
                    for _ in range(transitions):
                        assert phase(m, s.c) and outer_head(s) > 0
                        g = overflow(m, s)
                        assert g in (0, 1)
                        gs.append(g)
                        s = step(m, s)
                        steps += 1
                    for start in range(transitions-H):
                        assert 1 in gs[start:start+H+1], (m, c, B, start, gs)
                        windows += 1
    sharp = trace(9, State(2, (1, 0)), 5)
    assert [row['next_overflow'] for row in sharp[:5]] == [0, 0, 0, 0, 1]
    assert [row['residue'] for row in sharp] == [4, 8, 16, 10, 20, 0]
    zero = trace(9, State(2, (0,)), 5)
    assert zero[5]['residue'] == 2
    assert all(row['next_overflow'] == 0 for row in zero[:5])
    odd_base = trace(2, State(1, ()), 1)
    assert phase(2, odd_base[0]['c']) and not phase(2, odd_base[1]['c'])
    neutral = trace(9, State(9, (1,18)), 1)
    assert neutral[1]['B'] == [3,16,19]
    result = {'status': 'FINITE_TAIL_AND_SHARPNESS_CONTROLS_PASS',
        'parameters': {'m_values': [3,5,9,11], 'initial_width_cap': 2,
                       'transitions_per_start': transitions,
                       'phase_domain': 'all positive nonneutral interior phases',
                       'head_domain': 'strictly positive'},
        'initial_states': count, 'transitions': steps, 'complete_windows_tested': windows,
        'sharp_absorption_trace': sharp, 'zero_head_trace': zero,
        'odd_base_phase_failure': odd_base, 'neutral_coefficient_failure': neutral,
        'scope': 'Finite regression evidence only. Universal claims remain written derivations with uncompiled Lean source.'}
    Path(__file__).with_name('tail_and_sharpness_controls.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,list)}, indent=2))


if __name__ == '__main__':
    main()
