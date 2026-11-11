#!/usr/bin/env python3
"""Main-session read-only tally of r12e: census shard sums vs repo CSV; per-level identity of rerun vs original."""
import glob, re, os, csv, sys
R = os.path.expanduser('~/p196_run/r12e')
CSV = os.path.expanduser('~/p196_repo/calculation/decimal_frontier/exterior_census/data/f1_b10_p33_60.csv')
ref = {int(r['p']): (int(r['necklaces']), int(r['primitive'])) for r in csv.DictReader(open(CSV))}
print('T  shards words(summary) dies survives survfile | FCE-emitted primitive-emitted totalline | CSV | ok')
allw = alls = 0
for T in range(49, 57):
    outs = sorted(f for f in glob.glob(f'{R}/out/census/T{T}_s*.out'))
    words = dies = surv = 0
    nshard = 0
    for f in outs:
        s = [l for l in open(f, errors='replace') if l.startswith('KHXC_SUMMARY')]
        if not s:
            print('  no summary in', f); continue
        m = re.search(r'words=(\d+) dies=(\d+) survives=(\d+) badl=(\d+)', s[-1])
        w, d, v, b = map(int, m.groups())
        assert b == 0, f
        words += w; dies += d; surv += v; nshard += 1
    em = emp = 0; tot = set(); ns = set()
    for f in glob.glob(f'{R}/logs/census*/fce_T{T}_s*.log'):
        for l in open(f, errors='replace'):
            m = re.match(r'FCE b=10 p=(\d+) total=(\d+) primitive=(\d+) shard=(\d+)/(\d+) emitted=(\d+) emitted_primitive=(\d+)', l)
            if m:
                _, t, p, s_, n, e, ep = map(int, m.groups())
                tot.add((t, p, n)); ns.add((s_, n)); em += e; emp += ep
    sf = f'{R}/out/census/surv_T{T}.txt'
    ls = sum(1 for l in open(sf) if l.strip()) if os.path.exists(sf) else -1
    ok = (words == ref[T][0] and em == ref[T][0] and emp == ref[T][1] and dies + surv == words and all(t[:2] == ref[T] for t in tot) and len(tot) == 1)
    print(T, nshard, words, dies, surv, ls, '|', em, emp, sorted(tot), '|', ref[T], '|', 'OK' if ok else 'MISMATCH', '| shards distinct', len(ns))
    allw += words; alls += surv
print('total words', allw, 'survivors', alls)

def levels(fn, top=None):
    d = {}
    for l in open(fn, errors='replace'):
        m = re.match(r'\s*(TOP )?K=(\d+) (.*)$', l)
        if not m: continue
        k = int(m.group(2)); body = re.sub(r' t=[0-9.]+', '', m.group(3)).strip()
        d[(bool(m.group(1)), k)] = body
    return d
for name, a, b, top in (('T52w', 'out/decisive/T52w.err', 'out/confirm/T52w_K1710.err', 1710), ('p21sq', 'out/taskA/p21sq.err', 'out/confirm/p21sq_K2750.err', 2750), ):
    A = levels(f'{R}/{a}'); B = levels(f'{R}/{b}')
    keys = [k for k in B if k[1] <= top and not k[0]]
    bad = [k for k in keys if A.get(k) != B[k]]
    maxk = max(k[1] for k in keys)
    print(name, 'levels compared', len(keys), 'max K', maxk, 'mismatches', len(bad), bad[:3])
    if bad:
        print('  orig', A.get(bad[0])); print('  rerun', B[bad[0]])
    # are all levels 1..top present in both?
    miss = [k for k in range(1, top + 1) if (False, k) not in A or (False, k) not in B]
    print('  levels absent', len(miss), miss[:10])
