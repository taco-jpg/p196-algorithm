#!/usr/bin/env python3
"""r12g2 mklat.py -- independent parser of lattice_formats/p8_scc.txt (written from the file format, not from klib):
writes the explicit lattice rows for the independent C++ checker indep.cpp.
SCC line: 'g=<clock>' ... 'path=[c_0][c_1]...' (exterior columns, x = 0..nB-1) 'cyc=[w_0]...[w_{m-1}]' (bulk columns);
each column lists the cell at t = 0..p-1.   cell(t,x) = path[x][t] (x < nB), cyc[(x-nB) % m][t] (x >= nB).
output: 'p nB m' / g_0..g_{p-1} / p rows of nB exterior cells / p rows of m bulk cells.
usage: mklat.py p8_scc.txt INDEX OUT       (INDEX 0,1,2 = the three SCC lines in file order)"""
import sys, re
src, idx, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
lines = [l.strip() for l in open(src) if l.startswith('SCC')]
line = lines[idx]
g = re.search(r'\bg=([01]+)\b', line).group(1)
path_part = line.split('path=', 1)[1].split(' cyc=', 1)[0]
cyc_part = line.split(' cyc=', 1)[1]
def cols(s):
    return [[int(v) for v in c.split(',')] for c in re.findall(r'\[([0-9,]+)\]', s)]
P, C = cols(path_part), cols(cyc_part)
p = len(g)
assert all(len(c) == p for c in P + C), 'column length != period'
assert all(0 <= v <= 18 for c in P + C for v in c)
nB, m = len(P), len(C)
size = int(re.search(r'size=(\d+)', line).group(1)); cyclen = int(re.search(r'cyclen=(\d+)', line).group(1))
depth = int(re.search(r'depth=(\d+)', line).group(1))
assert cyclen == m and depth == nB, (cyclen, m, depth, nB)
with open(out, 'w') as f:
    f.write(f'{p} {nB} {m}\n' + ' '.join(g) + '\n')
    for t in range(p): f.write(' '.join(str(P[x][t]) for x in range(nB)) + '\n')
    for t in range(p): f.write(' '.join(str(C[j][t]) for j in range(m)) + '\n')
print(f'{out}: SCC #{idx} p={p} g={g} nB={nB} m={m} (size={size})')
