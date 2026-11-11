# deviation map of P(q0,C) from the lattice over S steps (folded columns), lattice = B_t W_t^inf in the root frame
import sys
from retsat import *
rec, q0, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); C = list(map(int, sys.argv[4].split(",")))
lat = load_rec(rec); S = 80*K
rows, gam = simulate(lat, q0, C, S)
for t in range(0, S+1, 2):
    f = fold(rows[t]); M = len(f)
    dev = [i for i in range(M) if f[i] != lat.cell(t, i)]
    lo = min(dev) if dev else None
    line = "".join("." if f[i] == lat.cell(t, i) else "#" for i in range(100, M))
    print(f"t={t:3d} M={M} firstdev={lo} | {line}")
