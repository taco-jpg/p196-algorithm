#!/usr/bin/env python3
"""r12g collect.py -- tables for FINAL.md from the logs.
|Cyc(K)| per lattice (full set, all phase orbits): kink6 logs directly; kink7 per-orbit logs scaled by the complement symmetry
(rec0/rec1: 4 x orbit 0; rec2: 2 x (orbit 0 + orbit 1)), with an equality check wherever both exist."""
import re, glob, os, sys
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
pat = re.compile(r'K=(\d+) (?:orbit=(\d+)/4 )?candidates=(\d+) edges=(\d+) cyclicSCCs=(\d+) cyclicStates=(\d+) (?:acceptingSCCs=\d+ )?acceptingStates=(\d+) \| exact: successors-in-Cyc=(\d+) cycles=(\d+) nonlattice=(\d+)')
rows = {}
def add(lat, K, src, orb, cand, edges, sccs, cyc, acc, exs, excyc, exnl, t, rss):
    rows.setdefault((lat, K), []).append(dict(src=src, orb=orb, cand=cand, edges=edges, cyc=cyc, acc=acc, exs=exs, excyc=excyc, exnl=exnl, t=t, rss=rss))
def rss_of(errfile):
    try:
        m = re.search(r'(\d+)\s+maximum resident set size', open(errfile).read()); return int(m.group(1)) / 2**30 if m else None
    except Exception: return None
for fn in glob.glob(os.path.join(R, 'logs/ctrl/*_kink6_K3-7.log')) + glob.glob(os.path.join(R, 'logs/k6_*.log')) + glob.glob(os.path.join(R, 'logs/k7_*.log')):
    base = os.path.basename(fn)
    m0 = re.match(r'(rec\d|p12m9)_kink6', base) or re.match(r'k6_(rec\d|p12m9)_K', base) or re.match(r'k7_(rec\d|b9r\d|p12m9)_o\d_K', base)
    if not m0: continue
    lat = m0.group(1)
    for line in open(fn):
        m = pat.search(line)
        if not m: continue
        K = int(m.group(1)); orb = m.group(2)
        tm = re.search(r'\| (?:tarjan \d+s total )?(\d+)s', line)
        add(lat, K, 'kink7' if orb is not None else 'kink6', None if orb is None else int(orb), *[int(m.group(i)) for i in range(3, 11)],
            int(tm.group(1)) if tm else None, rss_of(fn[:-4] + '.err'))
print('| lattice | K | |Cyc(K)| (all orbits) | accepting | exact successors in Cyc | exact cycles (non-lattice) | source | growth |')
print('|---|---|---|---|---|---|---|---|')
prev = {}
for (lat, K) in sorted(rows, key=lambda x: (x[0], x[1])):
    rs = rows[(lat, K)]
    k6 = [r for r in rs if r['src'] == 'kink6']
    k7 = {r['orb']: r for r in rs if r['src'] == 'kink7'}
    full = None; src = ''
    if k6:
        r = k6[0]; full = (r['cyc'], r['acc'], r['exs'], r['excyc'], r['exnl']); src = 'kink6'
    sym = None
    if lat in ('rec0', 'rec1') and 0 in k7:
        o = k7[0]; sym = (4 * o['cyc'], 4 * o['acc'], 4 * o['exs'], o['excyc'], o['exnl'])
    if lat == 'rec2' and 0 in k7 and 1 in k7:
        sym = tuple(2 * (k7[0][x] + k7[1][x]) for x in ('cyc', 'acc', 'exs')) + (k7[0]['excyc'] + k7[1]['excyc'], k7[0]['exnl'] + k7[1]['exnl'])
    if full and sym:
        src += ' = kink7 x sym' if full[:3] == sym[:3] else ' MISMATCH kink7 ' + str(sym)
    elif sym:
        full = sym; src = 'kink7 (orbit 0' + (', 1' if lat == 'rec2' else '') + ') x symmetry'
    if not full: continue
    gr = f'{full[0] / prev[lat]:.2f}' if lat in prev and prev[lat] else ''
    prev[lat] = full[0]
    print(f'| {lat} | {K} | {full[0]:,} | {full[1]:,} | {full[2]:,} | {full[3]} ({full[4]}) | {src} | {gr} |')
# kfwd results
print()
print('| lattice | K | k (free top) | bottom filter | top filter | start phase | |A_0| | |A_8| | result | max lifetime | time (s) |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
for fn in sorted(glob.glob(os.path.join(R, 'logs/fwd/*.log'))):
    s = open(fn).read()
    h = re.search(r'kfwd base=(\d+) P=\d+ M=(\d+) K=(\d+) k=(\d+) filterdepth=(\d+) filterkeys=(\d+) phi0=\((\d+),(\d+),(\d+)\)', s)
    if not h: continue
    a0 = re.search(r'STEP 0 size (\d+)', s); a8 = re.search(r'STEP 8 size (\d+)', s)
    top = re.search(r'top filter depth (\d+)', s)
    res = 'EMPTY' if 'EMPTY at' in s else ('STABLE' if 'STABLE' in s else ('UNDECIDED' if 'UNDECIDED' in s else 'running'))
    lt = re.search(r'max lifetime from phi0 = (\d+)', s); tt = re.search(r'DONE \[([\d.]+)s\]', s)
    lat = os.path.basename(fn).split('_')[0]
    print(f'| {lat} | {h.group(3)} | {h.group(4)} | Cyc({h.group(5)}) ({int(h.group(6)):,} keys) | TopCyc({top.group(1) if top else 0}) | ({h.group(7)},{h.group(8)},{h.group(9)}) | '
          f'{(format(int(a0.group(1)), ",") if a0 else "")} | {a8.group(1) if a8 else ""} | {res} | {lt.group(1) if lt else ""} | {tt.group(1) if tt else ""} |')
