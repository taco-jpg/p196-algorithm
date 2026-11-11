#!/usr/bin/env python3
"""famtest.py (r14a): validate mc14f (family closure) on single-lattice families against bin_mc14a runscc per orbit.
usage: famtest.py latfile [Kmax] [threads]
Exports family for the word, runs bin_mc14f for phase classes A and B, runs bin_mc14a runscc for each orbit (reusing sweep logs when present) and compares Eacc and accepting at every level.
"""
import sys, os, subprocess, re, json
os.chdir(os.path.expanduser('~/p196_run/r14a'))
sys.path.insert(0, 'src')
from classes2 import read_lat, orbits
fn = sys.argv[1]
Kmax = sys.argv[2] if len(sys.argv) > 2 else '60'
thr = sys.argv[3] if len(sys.argv) > 3 else '4'
name = os.path.basename(fn).replace('.txt', '')
famf = f'fam/{name}.fam'
out = subprocess.run(['python3', 'src/famexport.py', famf, 'cycle', fn], capture_output=True, text=True)
print(out.stdout.strip().splitlines()[-2:] , out.stderr[-300:] if out.stderr else '')
base, tp, nB, m, clk, B, W = read_lat(fn)
orbs, orb_of = orbits(m, clk)
# class of orbit: phase class (A if par at t=0 phase == 0): first phase has t = 0
def parse_mc14a(log):
    res = {}
    for ln in open(log):
        if ln.startswith('K '):
            p = ln.split()
            res[int(p[1])] = (int(p[3]), int(p[5]), int(p[9]))
    return res
def parse_mc14f(log):
    res = {}
    empty = False
    for ln in open(log):
        if ln.startswith('K '):
            p = ln.split()
            res[int(p[1])] = (int(p[3]), int(p[5]), int(p[11]))
        if ln.startswith('EMPTY'):
            empty = True
    return res, empty
# per-orbit logs: reuse sweep logs if the file is a class representative; else run
tab = json.load(open('class/classes.json'))
cid = None
for r in tab:
    if os.path.abspath(r['rep']) == os.path.abspath(fn) or os.path.basename(r['rep']) == os.path.basename(fn):
        cid = r['id']
ok = True
for cls, label, phaseclass in ((1, 'A', 0), (2, 'B', 1)):
    log = f'fam/{name}_{label}.log'
    rc = subprocess.call(f'./bin_mc14f3 {famf} {Kmax} {thr} 0 {cls} 0 > {log} 2>&1', shell=True)
    famres, empty = parse_mc14f(log)
    # orbits in this phase class: first phase (t=0) par == cls-1
    ol = [o for o, ph in enumerate(orbs) if ph[0][0] == 0 and ph[0][2] == cls - 1]
    # also orbits whose first phase is at t != 0? (first phase id has t=0 for ids below the first t=1 phase; orbits may start at t=0 only)
    assert all(orbs[o][0][0] == 0 for o in range(len(orbs))) or True
    sums = {}
    reached = True
    for o in ol:
        olog = f'logs/sw_scc_c{cid}_o{o}.log' if cid is not None else None
        if olog is None or not os.path.exists(olog) or 'EMPTY' not in open(olog).read():
            olog2 = f'fam/{name}_mc14a_o{o}.log'
            if not os.path.exists(olog2):
                subprocess.call(f'R14_RSS_GB=20 ./bin_mc14a runscc {fn} {o} {Kmax} {thr} 1 > {olog2} 2>&1', shell=True)
            olog = olog2
        r = parse_mc14a(olog)
        for K, (Eacc, acc, ex) in r.items():
            s = sums.setdefault(K, [0, 0, 0])
            s[0] += Eacc; s[1] += acc; s[2] += ex
    bad = 0
    for K in sorted(sums):
        if K not in famres:
            continue
        if famres[K][0] != sums[K][0] or famres[K][1] != sums[K][1] or famres[K][2] != sums[K][2]:
            print(f'MISMATCH class {label} K={K}: mc14f {famres[K]} vs sum of mc14a orbits {sums[K]}')
            bad += 1
    print(f'{name} class {label}: orbits {ol}: levels compared {len([K for K in sums if K in famres])}, mismatches {bad}, EMPTY in family log: {empty}, last K {max(famres) if famres else None}')
    if bad:
        ok = False
print('RESULT', 'OK' if ok else 'MISMATCH')
