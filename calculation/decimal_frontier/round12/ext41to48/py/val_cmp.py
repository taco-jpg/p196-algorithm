#!/usr/bin/env python3
"""Compare khx output with the round-11 bx3 verdicts.  usage: val_cmp.py r11_p{p}.tsv khx_out_files...
Rules (khx keeps a superset of the nodes on closed walks of length p, so it can never die before bx's last complete layer):
  bx EXHAUSTED at depth D  =>  khx DIES at K >= D   (K == D unless bx stopped by recurrence)
  bx CAPPED with wdone W   =>  khx does not die at K <= W."""
import sys, re, collections
ref = {}
for l in open(sys.argv[1]):
    p, g, st, d, w = l.split('\t'); ref[g] = (st, int(d), int(w))
res = {}
for fn in sys.argv[2:]:
    for l in open(fn):
        m = re.match(r'KHX b=10 p=(\d+) g=([01]+) (DIES|SURVIVES) K=(\d+)', l)
        if m: res[m[2]] = (m[3], int(m[4]))
c = collections.Counter(); bad = []
for g, (st, d, w) in ref.items():
    if g not in res: c['missing'] += 1; continue
    ks, K = res[g]
    if st == 'EXHAUSTED':
        if ks == 'DIES' and K == d: c['EXH_same_depth'] += 1
        elif ks == 'DIES' and K > d: c['EXH_khx_later'] += 1
        elif ks == 'DIES' and K < d: c['VIOLATION_EXH_khx_earlier'] += 1; bad.append((g, st, d, ks, K))
        else: c['EXH_khx_survives'] += 1
    else:
        if ks == 'DIES' and K <= w: c['VIOLATION_CAP_khx_dies_at_or_below_wdone'] += 1; bad.append((g, st, w, ks, K))
        elif ks == 'DIES': c['CAP_khx_dies'] += 1
        else: c['CAP_khx_survives'] += 1
print(sys.argv[1], dict(sorted(c.items())))
for x in bad[:20]: print('BAD', x)
