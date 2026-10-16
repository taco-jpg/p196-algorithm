#!/usr/bin/env python3
"""Small realized boundaries and counterexamples to weakened hypotheses."""
import json
from pathlib import Path
from two_column_controls import trajectory

specs = [
    ('high_L2_z0', [16, 16], 2),
    ('low_L3_z0', [16, 0, 16], 2),
    ('high_L3_z0', [16, 16, 16], 2),
    ('low_L4_z1', [16, 1, 1, 16], 2),
    ('high_L4_z1', [16, 17, 17, 16], 2),
    ('neutral_second_low_core', [7, 9, 0, 9, 7], 1),
    ('neutral_second_high_core', [7, 9, 10, 9, 7], 1),
    ('z2_L5_low_core', [16, 2, 0, 2, 16], 2),
    ('z2_L5_high_core', [16, 2, 18, 2, 16], 2),
]
examples = []
for label, q, steps in specs:
    ns, words, carries = trajectory(q, steps)
    examples.append({'label': label, 'integers': ns,
                     'words': words, 'carries': carries})
assert examples[5]['words'][-1][0] == 14
assert examples[6]['words'][-1][0] == 15
assert examples[7]['words'][-1][0] == 14
assert examples[8]['words'][-1][0] == 15
out = {'status': 'FINITE_BOUNDARY_EXAMPLES_NOT_LEAN_PROOF', 'examples': examples}
text = json.dumps(out, indent=2) + '\n'
(Path(__file__).parent / 'two-column-boundary-examples.json').write_text(text)
print(text, end='')
