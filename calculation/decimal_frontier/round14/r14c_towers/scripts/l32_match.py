#!/usr/bin/env python3
"""l32_match.py (round 14 packaging): the 16 towers capped by the (01)^16 whole-word pass (TCAP lines of logs/ifd_L32_word.out)
against the per-tower results (TOWER lines of logs/ifd_L32_*.out, logs/main_L32_*.out), up to rotation by the clock period P=2
and with xb reduced mod 10 (the exact merges of src/ifc.cpp).  Usage (from r14c_towers/): python3 scripts/l32_match.py"""
import re, glob
L, P = 32, 2
def canon(s):
    c, xb, A = s.split('|')
    xb = [int(x) % 10 for x in xb.strip(',').split(',')]
    return min((c[k:] + c[:k], tuple(xb[k:] + xb[:k]), A[k:] + A[:k]) for k in range(0, L, P))
tc = []
for ln in open('logs/ifd_L32_word.out'):
    if ln.startswith('TCAP'):
        k = canon(re.search(r'iface=(\S+)', ln).group(1))
        if k not in tc: tc.append(k)
res = {}
for fn in sorted(glob.glob('logs/ifd_L32_*.out') + glob.glob('logs/main_L32_*.out')):
    for ln in open(fn):
        if ln.startswith('TOWER'):
            st = re.search(r'(DIES K=\d+|CAPPED\(time\))', ln).group(1)
            res.setdefault(canon(re.search(r'iface=(\S+)', ln).group(1)), []).append(st + ' (' + fn + ')')
dead = 0
for i, t in enumerate(tc):
    r = res.get(t, ['NOT RUN'])
    dead += any(x.startswith('DIES') for x in r)
    print(i, '; '.join(r))
print(f'capped towers of the word pass: {len(tc)}; with a DIES line: {dead}')
