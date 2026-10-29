#!/usr/bin/env python3
"""Exact orbit-wide radius-window condition for the independent 100k decimal run."""
import csv,sys
r=list(csv.DictReader(open(sys.argv[1])))
assert len(r)==100001
n=[int(x['n']) for x in r]
e=[int(x['dist_exp']) for x in r]
d=[int(x['deficit']) for x in r]
h=[int(x['hamming']) for x in r]
H=128
assert n[0]==3 and n[-1]==41490
assert min(h)>0
assert max(d)==26 and d.index(26)==44105
assert min(n[t+H]//2-n[t]//2 for t in range(len(r)-H))==21
assert min(e[t+H]-e[t] for t in range(len(r)-H))==1
assert all(x['macro_drop']=='0' for x in r)
assert all(e[t+H] >= n[t]//2 for t in range(len(r)-H))
print('ADAPTIVE_RADIUS_100K_PASS states=100001 windows=99873 max_deficit=26 at=44105 min_half_gain=21 min_exp_gain=1 adaptive_bad=0 pal=0')