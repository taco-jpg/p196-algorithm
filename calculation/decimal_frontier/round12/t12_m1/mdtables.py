#!/usr/bin/env python3
"""r12a: Markdown tables for FINAL.md from the result logs (run from the r12a directory)."""
import os, re

def us():
    return [tuple((9, a, 18 - a)[r:] + (9, a, 18 - a)[:r]) for a in range(0, 19, 2) for r in range(3)]

def result_line(path):
    if not os.path.exists(path):
        return None
    for line in open(path):
        if line.startswith('RESULT'):
            return line.strip()
    return None

def dset(path):
    l = result_line(path)
    if l is None:
        return 'n/a'
    m = re.search(r'[DE]=(\[[^\]]*\])', l)
    if not m:
        return 'n/a'
    return 'empty' if m.group(1) == '[]' else '{' + m.group(1)[1:-1] + '}'

def tsec(path):
    l = result_line(path)
    if l is None:
        return None
    m = re.search(r'(?:time=)?(\d+(?:\.\d+)?)s', l)
    return float(m.group(1)) if m else None

def rss(path):
    if not os.path.exists(path):
        return None
    m = re.search(r'(\d+)\s+maximum resident set size', open(path).read())
    return int(m.group(1)) / 1e9 if m else None

U = us()
print('### Seam defect sets D_R(V) (letters that can precede a maximal band V^inf)')
print('| V | word | D_1 (rigid2/cadical) | D_12 rigid2/cadical195 | D_12 indep enc2/cadical195 | D_12 rigid2/kissat404 |')
print('|---|------|------|------|------|------|')
for i in range(30):
    print(f'| U{i} | {U[i]} | {dset(f"rig2/defect_U{i}_r1.log")} | {dset(f"rig2/defect_U{i}_r12.log")} | '
          f'{dset(f"indep/defect_V{i}_R12_cadical195.log")} | {dset(f"xsolver/defect_U{i}_r12_kissat404.log")} |')
ts = [tsec(f'rig2/defect_U{i}_r12.log') for i in range(30)] + [tsec(f'indep/defect_V{i}_R12_cadical195.log') for i in range(30)] + \
     [tsec(f'xsolver/defect_U{i}_r12_kissat404.log') for i in range(30)]
ts = [t for t in ts if t is not None]
print(f'\nD_12 solve times {min(ts):.0f}-{max(ts):.0f} s over {len(ts)} runs.')

print('\n### Centre comoving defect sets E_R(V) (letters that can follow a maximal band, comoving return)')
print('| V | word | E_4 (rigid2/cadical) | R used | E_R rigid2/cadical195 | E_R indep enc2/cadical195 | E_R rigid2/kissat404 |')
print('|---|------|------|---|------|------|------|')
for i in range(30):
    R = 6 if i in (5, 8, 23, 26) else 4
    print(f'| U{i} | {U[i]} | {dset(f"cdef/cdefect_U{i}_r4.log")} | {R} | {dset(f"cdef/cdefect_U{i}_r{R}.log")} | '
          f'{dset(f"indep/cdefect_V{i}_R{R}_cadical195.log")} | {dset(f"xsolver/cdefect_U{i}_r{R}_kissat404.log")} |')
extra = [(i, dset(f'cdef/cdefect_U{i}_r8.log')) for i in (5, 8, 23, 26)]
print('\nAlso E_8 (rigid2/cadical): ' + ', '.join(f'U{i} {e}' for i, e in extra) + '.')

def task(prefix, lengths, name):
    cnt = {}; tmin = {}; tmax = {}; rmax = 0
    for L in lengths:
        for i in range(30):
            f = f'{prefix}_U{i}_L{L}.log'
            l = result_line(f)
            k = 'missing' if l is None else ('UNSAT' if 'UNSAT' in l else ('SAT' if 'SAT' in l else 'other'))
            cnt[(L, k)] = cnt.get((L, k), 0) + 1
            t = tsec(f)
            if t is not None:
                tmin[L] = min(tmin.get(L, 1e9), t); tmax[L] = max(tmax.get(L, 0), t)
            rmax = max(rmax, rss(f) or 0)
    print(f'\n### {name}')
    print('| length | UNSAT | SAT | other/missing | solve time min-max (s) |')
    print('|---|---|---|---|---|')
    for L in lengths:
        print(f'| {L} | {cnt.get((L, "UNSAT"), 0)} | {cnt.get((L, "SAT"), 0)} | '
              f'{cnt.get((L, "other"), 0) + cnt.get((L, "missing"), 0)} | {tmin.get(L, 0):.0f}-{tmax.get(L, 0):.0f} |')
    print(f'max RSS {rmax:.1f} GB')

task('sat_seam/seam', (10, 11, 12), 'Task 1: seam SAT (seamsat.py), all 30 U')
task('sat_centre/centre', (13, 14, 15), 'Task 2: centre SAT (satc.py), all 30 U')
