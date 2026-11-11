#!/usr/bin/env python3
"""check that every mchk14 lattice file (476 simple cycles) is a member of a class of class/classes.json (word-wise, up to rotation and the group)."""
import sys, os, json, glob
os.chdir(os.path.expanduser('~/p196_run/r14a'))
sys.path.insert(0, 'src')
from classes2 import read_lat, cols, tw, canon
tab = json.load(open('class/classes.json'))
# canonical word -> class id
canon_map = {}
for rec in tab:
    base, tp, nB, m, clk, B, W = read_lat(rec['rep'])
    w = cols(W, m)
    can = min(canon(tw(w, r, c)) for r in range(4) for c in range(2))
    canon_map[can] = rec['id']
missing = 0
counts = {}
for fn in sorted(glob.glob(os.path.expanduser('~/p196_run/mchk14/lat/10_d8_scc0_len*.txt'))):
    base, tp, nB, m, clk, B, W = read_lat(fn)
    w = cols(W, m)
    can = min(canon(tw(w, r, c)) for r in range(4) for c in range(2))
    if can not in canon_map:
        missing += 1
        print('MISSING', os.path.basename(fn), 'L', m)
    else:
        counts[canon_map[can]] = counts.get(canon_map[can], 0) + 1
print('files checked', sum(counts.values()) + missing, 'missing', missing, 'classes hit', len(counts))
