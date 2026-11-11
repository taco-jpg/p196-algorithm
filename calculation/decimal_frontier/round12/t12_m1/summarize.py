#!/usr/bin/env python3
"""r12a: collect every result log into the tables used in FINAL.md (run from the r12a directory)."""
import glob, os, re

def us():
    return [tuple((9, a, 18 - a)[r:] + (9, a, 18 - a)[:r]) for a in range(0, 19, 2) for r in range(3)]

def res(path):
    if not os.path.exists(path):
        return None
    for line in open(path):
        if line.startswith('RESULT'):
            parts = line.split()
            if parts[1].startswith(('D=', 'E=')):
                m = re.search(r'([DE]=\[[^\]]*\])\s+(EMPTY|NONEMPTY)', line)
                return m.group(1) + ' ' + m.group(2) if m else parts[1]
            return parts[1]
    return 'RUNNING/NONE'

def rss(path):
    if not os.path.exists(path):
        return None
    m = re.search(r'(\d+)\s+maximum resident set size', open(path).read())
    return int(m.group(1)) / 1e9 if m else None

def secs(path):
    if not os.path.exists(path):
        return None
    for line in open(path):
        if line.startswith('RESULT'):
            m = re.search(r'(\d+(?:\.\d+)?)s', line)
            if m:
                return float(m.group(1))
            m = re.search(r'time=(\d+(?:\.\d+)?)s', line)
            if m:
                return float(m.group(1))
    return None

U = us()
print('## Task 1: seam SAT (seamsat.py), |J| = 10, 11, 12')
tot = {'UNSAT': 0, 'SAT': 0, 'other': 0}; mx = 0; tmax = 0
for i in range(30):
    row = []
    for L in (10, 11, 12):
        f = f'sat_seam/seam_U{i}_L{L}.log'; r = res(f)
        row.append(r)
        k = r if r in ('UNSAT', 'SAT') else 'other'
        tot[k] += 1
        mx = max(mx, rss(f) or 0); tmax = max(tmax, secs(f) or 0)
    print(f'U{i:2d} {U[i]}: ' + ' '.join(str(x) for x in row))
print('totals', tot, f'max RSS {mx:.1f} GB, max time {tmax:.0f} s')

print('\n## Task 2: centre SAT (satc.py), |C| = 13, 14, 15')
tot = {'UNSAT': 0, 'SAT': 0, 'other': 0}; mx = 0; tmax = 0
for i in range(30):
    row = []
    for L in (13, 14, 15):
        f = f'sat_centre/centre_U{i}_L{L}.log'; r = res(f)
        row.append(r)
        k = r if r in ('UNSAT', 'SAT') else 'other'
        tot[k] += 1
        mx = max(mx, rss(f) or 0); tmax = max(tmax, secs(f) or 0)
    print(f'U{i:2d} {U[i]}: ' + ' '.join(str(x) for x in row))
print('totals', tot, f'max RSS {mx:.1f} GB, max time {tmax:.0f} s')

print('\n## Seam defect sets D_R(V)')
for i in range(30):
    cells = []
    for R in (1, 3, 6, 12):
        f = f'rig2/defect_U{i}_r{R}.log'
        if os.path.exists(f):
            cells.append(f'R{R}(rigid2,cadical):{res(f)}')
    f = f'indep/defect_V{i}_R12_cadical195.log'
    cells.append(f'R12(indep enc2,cadical):{res(f)}')
    f = f'xsolver/defect_U{i}_r12_kissat404.log'
    cells.append(f'R12(rigid2,kissat404):{res(f)}')
    print(f'V{i:2d} {U[i]}: ' + ' | '.join(cells))

print('\n## Depth-3 left rigidity (rigid.py Uleft, previous agent)')
print(open('rig/pool.log').read())

print('\n## Centre comoving defect sets E_R(V)')
for i in range(30):
    cells = []
    for R in (4, 6, 8):
        f = f'cdef/cdefect_U{i}_r{R}.log'
        if os.path.exists(f):
            cells.append(f'R{R}(rigid2,cadical):{res(f)}')
    for R in (4, 6, 8):
        f = f'indep/cdefect_V{i}_R{R}_cadical195.log'
        if os.path.exists(f):
            cells.append(f'R{R}(indep,cadical):{res(f)}')
    for R in (4, 6, 8):
        f = f'xsolver/cdefect_U{i}_r{R}_kissat404.log'
        if os.path.exists(f):
            cells.append(f'R{R}(rigid2,kissat):{res(f)}')
    print(f'V{i:2d} {U[i]}: ' + ' | '.join(cells))

print('\n## W right-defect (optional)')
if os.path.exists('wright/run.log'):
    print(open('wright/run.log').read().strip())
print('\n## Validation logs')
for f in sorted(glob.glob('rig2/val_*.log') + glob.glob('indep/genuine_*.log') + glob.glob('indep/cgenuine_*.log')):
    line = open(f).readline().strip()
    print(f, 'PASS' if "'PASS': True" in line else 'FAIL/INCOMPLETE')
for f in ('rig2/wleft_r9_pin_genport.log', 'logs/empty_centre.log', 'logs/ctl_seam_neg_L10.log',
          'logs/ctl_seam_plant_L10.log', 'logs/ctl_seam_wret_L10.log', 'logs/ctl_centre_selftest.log'):
    if os.path.exists(f):
        print('---', f); print(''.join(l for l in open(f) if not l.startswith(' ')).strip())
