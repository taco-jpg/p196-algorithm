#!/usr/bin/env python3
"""mk_table.py (r14a): build per-class results table from logs/sweep_scc.txt, logs/rerun_scc.txt, logs/sweep_run.txt, logs/rerun_run.txt.
A later EMPTY result overrides an earlier BUDGET one."""
import json, re, os, collections, glob, sys
os.chdir(os.path.expanduser('~/p196_run/r14a'))
t = json.load(open('class/classes.json'))
res = collections.defaultdict(dict)
files = {'scc': ['logs/sweep_scc.txt', 'logs/rerun_scc.txt'], 'run': ['logs/sweep_run.txt', 'logs/rerun_run.txt']}
pat = re.compile(r'(scc|run) class (\d+) L=(\d+) T=(\d+) orbit (\d+) rep (\S+) rc=(-?\d+) status=(\w+) lastK=(\S+) peak=(\d+) exactlines=(\d+) time=(\d+)s')
for md, fl in files.items():
    for fn in fl:
        if not os.path.exists(fn): continue
        for ln in open(fn):
            m = pat.match(ln)
            if not m: continue
            cid = int(m.group(2)); o = int(m.group(5))
            rec = dict(status=m.group(8), lastK=m.group(9), peak=int(m.group(10)), ex=int(m.group(11)), time=int(m.group(12)), src=os.path.basename(fn))
            old = res[(cid, o)].get(md)
            if old is None or (old['status'] != 'EMPTY' and rec['status'] == 'EMPTY') or (old['status'] != 'EMPTY' and rec['peak'] >= old['peak']):
                res[(cid, o)][md] = rec
lines = ['| class | L | T | files | rep | orbit class | runscc (all periods): status / last K / peak | run (T_min): status / last K / peak | exact orbit lines (scc/run) |', '|---|---|---|---|---|---|---|---|---|']
counts = collections.Counter(); perclass = {}
for rec in t:
    cid = rec['id']
    st_all = []
    for oc in rec['orbit_classes']:
        o = oc[0]
        r = res.get((cid, o), {})
        s = r.get('scc'); rr = r.get('run')
        def fmt(x):
            if not x: return '-'
            return f"{x['status']} K={x['lastK']} peak={x['peak']}"
        lines.append(f"| {cid} | {rec['L']} | {rec['T']} | {rec['n_files']} | {os.path.basename(rec['rep'])} | {oc} | {fmt(s)} | {fmt(rr)} | {(s or {}).get('ex','-')}/{(rr or {}).get('ex','-')} |")
        if s: counts[s['status']] += 1
        st_all.append((s or {}).get('status', '-'))
    perclass[cid] = st_all
print('\n'.join(lines))
print()
print('scc status counts over orbit classes:', dict(counts))
closed = [c for c, st in perclass.items() if t[c]['T'] >= 256 and all(x == 'EMPTY' for x in st)]
print('classes (T >= 256) closed for all periods (every orbit class EMPTY):', len(closed), 'of', sum(1 for r in t if r['T'] >= 256))
print('list L of closed classes:', sorted(t[c]['L'] for c in closed))
