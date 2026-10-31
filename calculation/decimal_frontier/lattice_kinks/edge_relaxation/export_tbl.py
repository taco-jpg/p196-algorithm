#!/usr/bin/env python3
"""Export bulk lattice tables for the C++ relaxation: p m / g / then per t: L row, up-carry row, down-carry row (bulk columns)."""
import sys
from klib import *
for name in ['rec0', 'rec1', 'rec2', 'p12m9']:
    lat = load(name)
    base = lat.nB + 5 * lat.m
    with open(f'lat_{name}.tbl', 'w') as f:
        f.write(f'{lat.p} {lat.m}\n' + ' '.join(map(str, lat.g)) + '\n')
        for t in range(lat.p):
            f.write(' '.join(str(lat.cell(t, base + j)) for j in range(lat.m)) + '\n')
            f.write(' '.join(str(bulk_up_carry(lat, t, base + j)) for j in range(lat.m)) + '\n')
            f.write(' '.join(str(bulk_down_carry(lat, t, base + j)) for j in range(lat.m)) + '\n')
    print('wrote', name)
