#!/usr/bin/env python3
"""r12g3: planted bottom filter for a positive control of the K > 25 (base-D packing) path: for every phase (t,j,par) the
single bottom window of Kf lattice cells L[t][(j+i) mod M].  kink6/kink7 key format: phase << PS | sum cell_i << 5i,
PS = 100 (Kf <= 20) or 118.  Not a cyclic set: it only checks that the iteration keeps a known periodic orbit (the lattice)."""
import sys, struct
tbl, Kf, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
lines = open(tbl).read().split('\n')
hdr = lines[0].split(); P, M = int(hdr[0]), int(hdr[1])
tok = ' '.join(lines[1:]).split(); it = iter(tok)
G = [int(next(it)) for _ in range(P)]
L = []
for t in range(P):
    L.append([int(next(it)) for _ in range(M)]); [next(it) for _ in range(2 * M)]
PS = 100 if Kf <= 20 else 118
keys = []
for t in range(P):
    for j in range(M):
        for par in range(2):
            k = ((t * M + j) * 2 + par) << PS
            for i in range(Kf): k |= L[t][(j + i) % M] << (5 * i)
            keys.append(k)
keys.sort()
with open(out, 'wb') as f:
    for k in keys: f.write(struct.pack('<QQ', k & ((1 << 64) - 1), k >> 64))
print(f'{out}: {len(keys)} keys, P={P} M={M} Kf={Kf} PS={PS}')
