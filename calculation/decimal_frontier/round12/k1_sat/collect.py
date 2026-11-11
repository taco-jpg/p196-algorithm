#!/usr/bin/env python3
"""r12d collect.py -- aggregate all logs into result tables (prints markdown-ish text)."""
import os, re, glob, collections
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
cand = []
for f in glob.glob('logs/**/*.log', recursive=True):
    for l in open(f, errors='replace'):
        if 'CANDIDATE' in l or 'MISMATCH' in l or 'KILLED' in l or 'Traceback' in l or 'Error' in l:
            cand.append(f'{f}: {l.strip()[:200]}')
print('== ALERTS (candidates / mismatches / kills / errors):', len(cand))
for c in cand: print('  ', c)

print('\n== fixed-centre exact returns (logs/prod)')
tab = collections.defaultdict(dict)
for f in sorted(glob.glob('logs/prod/ret_*.log')):
    m = re.match(r'logs/prod/ret_(\w+?)_K(\d+)_L(\d+)\.log', f)
    if not m: continue
    lat, K, L = m.group(1), int(m.group(2)), int(m.group(3))
    res = None
    for l in open(f):
        if l.startswith('RESULT'):
            mm = re.search(r'RESULT (\w+) .* ([\d.]+)s', l); res = (mm.group(1), float(mm.group(2)))
    tab[(lat, K)][L] = res
for key in sorted(tab):
    row = tab[key]
    done = sorted(L for L in row if row[L])
    uns = [L for L in done if row[L][0] == 'UNSAT']
    sat = [L for L in done if row[L][0] == 'SAT']
    contig = 0
    for L in range(4, 200):
        if L in row and row[L] and row[L][0] == 'UNSAT': contig = L
        elif L >= min(row): break
    ts = ' '.join(f'{L}:{row[L][1]:.0f}' for L in done)
    print(f'{key[0]} K={key[1]}: UNSAT for L in {uns[:1]}..{uns[-1:]} (n={len(uns)}), SAT {sat}, running/pending {sorted(L for L in row if not row[L])}')
    print(f'    times(s) {ts}')

print('\n== walls (logs/wall)')
for f in sorted(glob.glob('logs/wall/*.log')):
    d = [l.strip() for l in open(f) if l.startswith('DONE') or l.startswith('SCAN')]
    print('  ', os.path.basename(f), ' | '.join(d)[:230])

print('\n== confined kinks (logs/surv)')
for f in sorted(glob.glob('logs/surv/*.log')):
    lt = [re.search(r'o=(\d) lifetime=(\S+)', l).groups() for l in open(f) if l.startswith('LIFETIME')]
    dn = any(l.startswith('DONE') for l in open(f))
    print('  ', os.path.basename(f), lt, 'DONE' if dn else 'running')

print('\n== other (val, lat, scale)')
for f in sorted(glob.glob('logs/val/*.log') + glob.glob('logs/lat/*.log') + glob.glob('logs/scale/*.log')):
    r = [l.strip()[:150] for l in open(f) if l.startswith(('RESULT', 'SIMCHECK', 'PLANTCHECK', 'CHECK'))]
    print('  ', os.path.basename(f), ' || '.join(r)[:300] if r else '(running)')
