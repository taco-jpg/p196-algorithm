#!/usr/bin/env python3
"""mksummary.py (r14a): produce the summary statements (text) for FINAL.md section 0/3 from the logs: class/summary.txt"""
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
        rec = dict(status=m.group(8), K=m.group(9), peak=int(m.group(10)), ex=int(m.group(11)), t=int(m.group(12)))
        old = res[(cid, o)].get(md)
        if old is None or (old['status'] != 'EMPTY' and rec['status'] == 'EMPTY') or (old['status'] != 'EMPTY' and rec['peak'] >= old['peak']):
            res[(cid, o)][md] = rec
lines = []
closed, partial, und = [], [], []
tot = 0
for rec in t:
    if rec['T'] < 256: continue
    tot += 1
    ocs = [oc[0] for oc in rec['orbit_classes']]
    st = [res[(rec['id'], o)].get('scc') for o in ocs]
    done = [x for x in st if x and x['status'] == 'EMPTY']
    if len(done) == len(ocs):
        closed.append(rec)
    elif done:
        partial.append((rec, len(done), len(ocs)))
    else:
        und.append(rec)
lines.append(f'Classes with T >= 256: {tot} (83 big-SCC classes with L in 61..159, plus rec2 is handled separately).')
lines.append(f'All-period closure EMPTY for every orbit class ("closed for all periods"): {len(closed)} classes.')
Ks = [int(res[(r["id"], oc[0])]['scc']['K']) for r in closed for oc in r['orbit_classes']]
pk = [res[(r["id"], oc[0])]['scc']['peak'] for r in closed for oc in r['orbit_classes']]
lines.append(f'  Death level K0 over their orbit classes: min {min(Ks)}, max {max(Ks)}; peak |Cyc_acc| per job: max {max(pk)}; exact-orbit lines: {sum(res[(r["id"], oc[0])]["scc"]["ex"] for r in closed for oc in r["orbit_classes"])}.')
lines.append('  L values of the closed classes (with multiplicity): ' + ' '.join(str(r['L']) for r in closed))
lines.append(f'Partial (some orbit classes closed): {len(partial)}: ' + ', '.join(f"class {r['id']} (L={r['L']}): {d}/{n}" for r, d, n in partial))
lines.append(f'No orbit class closed within the budget: {len(und)}: L = ' + ' '.join(str(r['L']) for r in und) + ' (class ids: ' + ','.join(str(r['id']) for r in und) + ')')
# fixed-period chain data for closed classes
rr = [(r['id'], oc[0]) for r in closed for oc in r['orbit_classes']]
fin = [res[k].get('run') for k in rr]
lines.append('Fixed-period chain E_acc(K,T_min) status on closed classes: ' + repr(collections.Counter((x['status'] if x else 'not run') for x in fin)))
lines.append('Largest EMPTY level K among fixed-period runs finished: ' + str(max([int(x['K']) for x in fin if x and x['status'] == 'EMPTY'], default=None)))
open('class/summary.txt', 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
