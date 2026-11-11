#!/usr/bin/env python3
"""mk_compact.py (r14a): one line per class: id L T files orbit-classes, all-period status (closed K0 range / budget count), fixed period status."""
import json, re, os, collections
os.chdir(os.path.expanduser('~/p196_run/r14a'))
t = json.load(open('class/classes.json'))
pat = re.compile(r'(scc|run) class (\d+) L=(\d+) T=(\d+) orbit (\d+) rep (\S+) rc=(-?\d+) status=(\w+) lastK=(\S+) peak=(\d+) exactlines=(\d+) time=(\d+)s')
res = collections.defaultdict(dict)
for fn in ['logs/sweep_scc.txt', 'logs/rerun_scc.txt', 'logs/sweep_run.txt', 'logs/rerun_run.txt']:
    if not os.path.exists(fn): continue
    for ln in open(fn):
        m = pat.match(ln)
        if not m: continue
        md, cid, o = m.group(1), int(m.group(2)), int(m.group(5))
        rec = (m.group(8), int(m.group(9)) if m.group(9) != '-' else -1, int(m.group(10)), int(m.group(11)))
        old = res[(cid, o)].get(md)
        if old is None or (old[0] != 'EMPTY' and (rec[0] == 'EMPTY' or rec[2] >= old[2])):
            res[(cid, o)][md] = rec
print('id L T files nOC | all-period: closed-orbit-classes/total, K0 range, max peak | fixed-Tmin: closed/total, K range, max peak')
tot = collections.Counter()
for rec in t:
    cid = rec['id']
    ocs = [oc[0] for oc in rec['orbit_classes']]
    s = [res[(cid, o)].get('scc') for o in ocs]
    r = [res[(cid, o)].get('run') for o in ocs]
    done = [x for x in s if x and x[0] == 'EMPTY']
    budget = [x for x in s if x and x[0] != 'EMPTY']
    missing = sum(1 for x in s if x is None)
    k0 = (min(x[1] for x in done), max(x[1] for x in done)) if done else None
    pk = max((x[2] for x in s if x), default=0)
    rd = [x for x in r if x and x[0] == 'EMPTY']
    rk0 = (min(x[1] for x in rd), max(x[1] for x in rd)) if rd else None
    rp = max((x[2] for x in r if x), default=0)
    status = 'CLOSED-ALL' if done and len(done) == len(s) else ('PARTIAL' if done else ('BUDGET' if s[0] else '-'))
    if rec['T'] >= 256:
        tot[status] += 1
    print(f"{cid:3d} L={rec['L']:3d} T={rec['T']:4d} f={rec['n_files']:2d} oc={len(ocs)} | {status:10s} {len(done)}/{len(s)} K0={k0} maxpeak={pk} missing={missing} | Tmin {len(rd)}/{len(r)} K={rk0} peak={rp}")
print('classes with T>=256 by status:', dict(tot))
