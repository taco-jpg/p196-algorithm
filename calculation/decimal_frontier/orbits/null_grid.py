#!/usr/bin/env python3
"""null_grid.py BASE K OUT -- static panels of K random digit strings at a log grid of lengths (20..20000)."""
import sys, os, json, gzip
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbit2
b = int(sys.argv[1]); K = int(sys.argv[2]); out = sys.argv[3]
grid = sorted(set(int(round(x)) for x in np.geomspace(20, 20000, 24)))
with gzip.open(out, 'wt') as f:
    for n in grid:
        for r in orbit2.null_records(b, [n], K=K, seed=n + b):
            r['base'] = b; f.write(json.dumps(r) + '\n')
        f.flush(); print(n, flush=True)
