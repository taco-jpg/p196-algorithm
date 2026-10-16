#!/usr/bin/env python3
"""PRECLAIM_SCOUT / FINITE: source scout only; no ownership or formal Lean claim."""
import hashlib
import importlib.util
import json
from pathlib import Path

contributions = Path(__file__).resolve().parents[2]
p = contributions / 'groupII-overlap-20261016/controls/groupII_controls.py'
assert hashlib.sha256(p.read_bytes()).hexdigest() == '50e73312a3a89a8f90a7d8fc6a40b3280724c764c5e433a2a10734ead2f28f31'
s = importlib.util.spec_from_file_location('groupII_controls', p)
c = importlib.util.module_from_spec(s)
s.loader.exec_module(c)
rows = []
for r in [1, 2, 3, 4, 5, 6, 10, 30, 100]:
    na, aa = c.integer_trajectory(c.component(r, 1, 1, 6), 6)
    nq, qq = c.integer_trajectory(c.phi(c.component(r, 1, 1, 6)), 6)
    rows.append({
        'r': r,
        'component_widths': [len(x) for x in aa],
        'whole_widths': [len(x) for x in qq],
        'component_prefix_t4_t5_t6': [x[:4] for x in aa[4:]],
        'whole_prefix_t4_t5_t6': [x[:4] for x in qq[4:]],
        'component_palindrome_flags': [c.palindromic(x) for x in na],
        'whole_palindrome_flags': [c.palindromic(x) for x in nq],
        'time6_full_difference': c.sparse_difference(qq[6], c.phi(aa[6])),
    })
out = {'status': 'PRECLAIM_SCOUT_FINITE_ONLY_NOT_FORMAL_PROOF',
       'tested_spacers': [x['r'] for x in rows], 'rows': rows}
for row in rows:
    width = 2 * row['r'] + 6
    assert row['component_widths'] == [width] * 5 + [width + 1] * 2
    assert row['whole_widths'] == [width + 1] * 5 + [width + 2] * 2
    assert row['component_prefix_t4_t5_t6'][2][0] == 14
    assert row['whole_prefix_t4_t5_t6'][2][0] == 15
    assert row['time6_full_difference'][0] == [0, 1]
summary = {
    'status': 'PRECLAIM_SCOUT_FINITE_PASS',
    'not_formal_proof': True,
    'not_in_lean_build': True,
    'tested_spacers': out['tested_spacers'],
    'tested_component_and_whole_pairs': len(rows),
    'ordinary_additions': 12 * len(rows),
    'width_and_outer_checks': 'All nine finite rows satisfy actual widths through time six and outer coefficients A6=14,Q6=15; index-zero difference equals 1.',
    'universal_scope': 'No all-r theorem or arbitrary-realization theorem is supplied by this script. One canonical integer realization of each component/whole profile is used.',
    'groupII_helper_sha256': '50e73312a3a89a8f90a7d8fc6a40b3280724c764c5e433a2a10734ead2f28f31',
}
(Path(__file__).parent / 'time6-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
(Path(__file__).with_suffix('.json')).write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
