#!/usr/bin/env python3
"""Build the lattice files for mc13b directly from lattice_formats/p8_scc.txt (no r12g/r13b tables),
and, as a cross-check only, compare with r13b's tbl/*.rows.  Base-9 controls are read from r13b's .tbl."""
import re, sys, os
src = os.path.expanduser('~/p196_repo/calculation/decimal_frontier/lattice_formats/p8_scc.txt')
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
names = ['rec0', 'rec1', 'rec2']
k = 0
for line in open(src):
    if not line.startswith('SCC'):
        continue
    mm = re.search(r'p=(\d+) g=(\d+) size=(\d+) cyclen=(\d+) depth=(\d+)', line)
    p, g, size, cyc, depth = int(mm[1]), mm[2], int(mm[3]), int(mm[4]), int(mm[5])
    rest = line.split('path=')[1]
    pathpart, cycpart = rest.split('cyc=')
    pathcols = [list(map(int, c.split(','))) for c in re.findall(r'\[([0-9,]+)\]', pathpart)]
    cyccols = [list(map(int, c.split(','))) for c in re.findall(r'\[([0-9,]+)\]', cycpart)]
    assert len(pathcols) == depth and len(cyccols) == cyc, (len(pathcols), depth, len(cyccols), cyc)
    clk = [int(c) for c in g]
    assert len(clk) == p
    fn = os.path.join(out, names[k] + '.txt')
    with open(fn, 'w') as f:
        f.write(f'10 {p} {depth} {cyc}\n')
        f.write(' '.join(map(str, clk)) + '\n')
        for t in range(p):
            f.write(' '.join(str(c[t]) for c in pathcols) + '\n')
        for t in range(p):
            f.write(' '.join(str(c[t]) for c in cyccols) + '\n')
    # cross-check only
    rows = os.path.expanduser(f'~/p196_run/r13b/tbl/{names[k]}.rows')
    tk = open(rows).read().split()
    a = list(map(int, tk[:3]))
    assert a == [p, depth, cyc], a
    vals = list(map(int, tk[3:]))
    assert vals[:p] == clk
    vals = vals[p:]
    mine = [c[t] for t in range(p) for c in pathcols] + [c[t] for t in range(p) for c in cyccols]
    print(names[k], 'nB', depth, 'm', cyc, 'equal to r13b rows:', vals == mine)
    k += 1

# base-9 controls: r13b's .tbl format "tp m / clock / for each t: W row, UP row, DN row"
for nm in ['b9r0', 'b9r1']:
    tk = open(os.path.expanduser(f'~/p196_run/r13b/tbl/lat_{nm}.tbl')).read().split()
    tp, mm_, bs = int(tk[0]), int(tk[1]), int(tk[2])
    assert bs == 9
    clk = tk[3:3 + tp]
    v = tk[3 + tp:]
    rows = [v[i * 3 * mm_: i * 3 * mm_ + mm_] for i in range(tp)]
    with open(os.path.join(out, nm + '.txt'), 'w') as f:
        f.write(f'9 {tp} 0 {mm_}\n')
        f.write(' '.join(clk) + '\n')
        for r in rows:
            f.write(' '.join(r) + '\n')
    print(nm, 'tp', tp, 'm', mm_, 'clock', ''.join(clk))
