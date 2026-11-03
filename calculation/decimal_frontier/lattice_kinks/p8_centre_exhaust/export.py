#!/usr/bin/env python3
"""Export B_t,W_t,g of rec0/rec1 (klib.load_rec) as a plain text table for the C++ enumerator."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../calculation/decimal_frontier/lattice_kinks/edge_relaxation'))
from klib import load_rec
for r in (0, 1):
    L = load_rec(r)
    with open(f'rec{r}.tbl', 'w') as f:
        f.write(f'{L.p} {L.nB} {L.m}\n' + ' '.join(map(str, L.g)) + '\n')
        for t in range(L.p): f.write(' '.join(map(str, L.B[t])) + '\n')
        for t in range(L.p): f.write(' '.join(map(str, L.W[t])) + '\n')
