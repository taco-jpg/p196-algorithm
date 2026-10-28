#!/usr/bin/env python3
"""analyze_b10.py ORBITS.jsonl.gz NULL.jsonl.gz -- compare detector statistics of orbit windows vs random-digit-string null."""
import sys, json, gzip, collections
import numpy as np
orb = [json.loads(l) for l in gzip.open(sys.argv[1], 'rt')]
nul = [json.loads(l) for l in gzip.open(sys.argv[2], 'rt')]
summ = [r for r in orb if 'summary' in r]
orb = [r for r in orb if 'summary' not in r]
metrics = ['r9_max', 'r0', 'rtop', 'rany', 'per2', 'per3', 'per4', 'per5', 'per6', 'lrs', 'dlrs', 'd_rany', 'cr', 'band_g']
grid = sorted(set(r['n'] for r in nul))
def bin_of(n): return min(grid, key=lambda g: abs(np.log(g) - np.log(n)))
nulb = collections.defaultdict(list)
for r in nul: nulb[r['n']].append(r)
groups = collections.defaultdict(list)
for r in orb:
    nm = r['seedname']; groups['named' if nm.startswith('n') else 'random'].append(r)
print('orbit windows:', {k: len(v) for k, v in groups.items()}, ' null samples:', len(nul))
# 1) overall per-metric mean ratio orbit/null per length bin, restricted to n >= 500
print('\nmetric: mean over n-bins >=500 [orbit-named, orbit-random, null] ; exceedance of null 99th pct; max orbit vs max null (same bins)')
for m in metrics:
    row = {}
    for gname in ('named', 'random'):
        vals = [(r['n'], r[m]) for r in groups[gname] if r['n'] >= 500]
        mean_o = np.mean([v for _, v in vals])
        # null mean at matched n
        nm = np.mean([np.mean([x[m] for x in nulb[bin_of(n)]]) for n, _ in vals])
        q99 = [np.quantile([x[m] for x in nulb[bin_of(n)]], 0.99) for n, _ in vals]
        q50 = [np.quantile([x[m] for x in nulb[bin_of(n)]], 0.50) for n, _ in vals]
        ex = np.mean([v > q for (_, v), q in zip(vals, q99)])
        row[gname] = (mean_o, nm, ex, max(v for _, v in vals))
    mxn = max(x[m] for r in nul for x in [r] if x['n'] >= 500)
    print(f"{m:8s} named: orb {row['named'][0]:.3f} null {row['named'][1]:.3f} exc99 {row['named'][2]:.3f} max {row['named'][3]} | random: orb {row['random'][0]:.3f} null {row['random'][1]:.3f} exc99 {row['random'][2]:.3f} max {row['random'][3]} | null max(n>=500) {mxn}")
# 2) Temporal: Fb Fc distribution for orbits
for m in ('Fb', 'Fc'):
    vals = [r[m] for r in orb if r['n'] >= 500]
    print(m, 'orbit windows n>=500: mean %.2f  q50 %d q90 %d q99 %d q999 %d max %d' % (np.mean(vals), *np.quantile(vals, [.5, .9, .99, .999]), max(vals)))
# 3) pred_ok / template statistics
tp = [r for r in orb if r['n'] >= 500]
print('pred_ok True count', sum(1 for r in tp if r.get('pred_ok') is True), 'of', len(tp), ' with tpl run cycle:', sum(1 for r in orb if r.get('run') == 'cycle'))
print('hist of band_g among orbit windows n>=500', collections.Counter(r['band_g'] for r in tp).most_common(12))
# worst offenders
for m in ('r9_max', 'rany', 'per2', 'per3', 'per4', 'lrs', 'dlrs', 'Fb', 'Fc', 'r0', 'rtop'):
    top = sorted(orb, key=lambda r: -r[m])[:3]
    print(m, [(r['seedname'], r['t'], r['n'], r[m]) for r in top])
