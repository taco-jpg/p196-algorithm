#!/usr/bin/env python3
"""Generate neutral-band inputs for the K1 centre-horizon solver.
A neutral lattice has spatial period one with coefficient b-1, and the
incoming band carry in each time phase equals the exterior's e-stream.
"""
from pathlib import Path
import sys
out = Path(sys.argv[1] if len(sys.argv)>1 else '.')
out.mkdir(parents=True, exist_ok=True)
targets = (
    ('neutral_p11', 10, 29, '11100010000', '10100110011'),
    ('neutral_p12', 10, 53, '100010001000', '101010010101'),
    # Positive control: known Lean base-26 cert26, four-edge E/G streams.
    ('neutral_b26_control', 26, 8, '0101', '0101'),
)
for name, b, nB, g, e in targets:
    assert len(g)==len(e) and set(g+e)<={'0','1'}
    s = [f'{len(g)} {nB} 1 {b}', ' '.join(g)]
    s += [str(b-1)] * len(g)
    s += list(e)
    (out / f'{name}.txt').write_text('\n'.join(s)+'\n')
    print(out / f'{name}.txt')
