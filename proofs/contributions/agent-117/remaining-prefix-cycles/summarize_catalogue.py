#!/usr/bin/env python3
"""Catalogue summaries from the C++ class tables: closed counts per (k, D), the four-digit
refinements of the 499 open three-digit classes by minimal closing width, and the list of
four-digit classes closed at k=7 but not at k<=6.  usage: summarize_catalogue.py DIR_WITH_wf4..wf7"""
import sys, pathlib
root = pathlib.Path(sys.argv[1])
HERE = pathlib.Path(__file__).resolve().parent
rem = [l.strip() for l in open(HERE.parents[1] / '2026-10-15-seven-column-prefix/development/remaining_prefixes.txt') if l.strip()]
cyc = set(rem) - {'739'}
OVERFLOW = ('110', '111', '121', '122')

def load(k, D):
    d = {}
    for l in open(root / f'wf{k}' / f'classes{k}.tsv'):
        if l.startswith('#'):
            continue
        f = l.rstrip('\n').split('\t')
        if f[0] == str(D):
            d[f[1]] = (int(f[2]), int(f[3]))
    return d

for D in (3, 4):
    print(f'D={D}:', {k: sum(1 for p, v in load(k, D).items() if v[0] == 1 and p[:3] not in OVERFLOW) for k in (4, 5, 6, 7)})
prev = set(); tables = {k: load(k, 4) for k in (4, 5, 6, 7)}
for k in (4, 5, 6, 7):
    closed = {p for p, v in tables[k].items() if v[0] == 1 and p[:3] in cyc and p[:3] not in OVERFLOW}
    new = sorted(closed - prev)
    print(f'four-digit refinements of the 499 open classes closed at k={k}: {len(closed)}, newly at this k: {len(new)}')
    if k == 7:
        print('newly closed at k=7 (prefix bound):', ' '.join(f'{p}:{tables[7][p][1]}' for p in new))
    prev |= closed
# refinements of the three rule-only baseline classes
for p3 in ('109', '659', '769'):
    cl = [(p, tables[7][p][1]) for p in tables[7] if p[:3] == p3 and tables[7][p][0] == 1]
    print(f'refinements of {p3} closed purely at k=7: {len(cl)}/10', cl)
