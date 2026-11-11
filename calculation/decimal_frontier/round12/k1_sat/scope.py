#!/usr/bin/env python3
"""r12d scope.py -- combined exclusion scope per (lattice, K): prior cen2 bounds (r11a, P8Rec1FixedCentreLen16) + this run
(SAT UNSAT in logs/prod, cubes2 full partitions, cen3 0 returns).  Writes scope_table.md."""
import os, re, glob, collections
os.chdir(os.path.dirname(os.path.abspath(__file__)))
prior = {('rec1', 1): 16, ('rec0', 1): 14, ('rec1', 2): 14, ('rec0', 2): 12, ('rec1', 3): 13, ('rec0', 3): 12}
q0 = {1: 5, 2: 8, 3: 11, 4: 15, 5: 18, 6: 21}; q0r2 = {1: 4, 2: 6, 3: 9}
mine = collections.defaultdict(dict)   # (lat,K) -> L -> method
for f in glob.glob('logs/prod/ret_*.log'):
    m = re.match(r'logs/prod/ret_(rec\d)_K(\d+)_L(\d+)r?\.log', f)
    if not m: continue
    if any(l.startswith('RESULT UNSAT') for l in open(f)):
        mine[(m.group(1), int(m.group(2)))][int(m.group(3))] = 'SAT-solver'
# cubes2: a length counts only if the c0-splits cover [0,19) completely and all are UNSAT
splits = collections.defaultdict(list)
for f in glob.glob('logs/prod/cubes2_*.log') + glob.glob('logs/test/cubes2_*.log'):
    for l in open(f):
        m = re.search(r'RESULT (\w+) cubes2 ret lat=(rec\d) q0=\d+ K=(\d+) L=(\d+) first=\[(\d+),(\d+)\)', l)
        if m: splits[(m.group(2), int(m.group(3)), int(m.group(4)))].append((m.group(1), int(m.group(5)), int(m.group(6))))
for (lat, K, L), sp in splits.items():
    cov = set()
    for st, lo, hi in sp:
        if st == 'UNSAT': cov |= set(range(lo, hi))
    if cov >= set(range(19)): mine[(lat, K)].setdefault(L, 'SAT-solver (cubes)')
for f in glob.glob('logs/cen/cen_*.log'):
    m = re.match(r'logs/cen/cen_(rec\d)_K(\d+)_L(\d+)b?\.log', f)
    for l in open(f):
        if l.startswith('RESULT') and ' returns=0 ' in l and ' clockdev=0 lenerr=0 guardfail=0 ' in l:
            mine[(m.group(1), int(m.group(2)))].setdefault(int(m.group(3)), 'enumeration')
rows = []
keys = sorted(set(list(prior) + list(mine)), key=lambda k: (k[0] != 'rec1', k[0], k[1]))
for key in keys:
    lat, K = key
    p = prior.get(key, 3)
    cov = set(range(4, p + 1)) | set(mine[key])
    top = 3
    while top + 1 in cov: top += 1
    extra = sorted(L for L in mine[key] if L > top)
    meth = collections.Counter(mine[key][L] for L in mine[key] if p < L <= top)
    per = (192 if lat == 'rec2' else 80) * K
    qq = (q0r2 if lat == 'rec2' else q0)[K]
    rows.append(f'| {lat} | {K} ({per}) | {qq} | {"<= " + str(p) + " (cen2, r11a)" if key in prior else "-"} | '
                f'**4..{top}** | {", ".join(f"{k}: {v}" for k, v in meth.items()) or "-"} | {extra or "-"} |')
out = ['| exterior | K (period) | q0 | before this run | excluded now, all \\|C\\| in | new lengths by | further isolated lengths |',
       '|---|---|---|---|---|---|---|'] + rows
open('scope_table.md', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
