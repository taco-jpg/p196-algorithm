#!/usr/bin/env python3
"""r12e census summary (pass 1).  For every T with all shards done: check that the khxc word counts add up to the fc_enum2 totals
and to data/f1_b10_p33_60.csv, merge the death-level histograms, list the survivors (primitive / imprimitive with root),
collect the sampled verdicts (for the kh2 cross-check) and the deaths with K >= 40.
usage: census_sum.py [T ...]      writes out/census/summary_T{T}.json, out/census/surv_T{T}.txt, out/census/samp_T{T}.txt"""
import sys, os, re, json, glob, collections
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the route directory (Studio: ~/p196_run/r12e)
CSV = {49: (94598340, 94598336), 50: (146010697, 146007261), 51: (225446789, 225446658), 52: (348243213, 348238031),
       53: (538112178, 538112178), 54: (831810647, 831802584), 55: (1286235064, 1286235048), 56: (1989587605, 1989575663)}
def root(w):
    n = len(w)
    for d in range(1, n + 1):
        if n % d == 0 and w[:d] * (n // d) == w: return w[:d]
Ts = [int(a) for a in sys.argv[1:]] or sorted(CSV)
for T in Ts:
    outs = sorted(glob.glob(f'{D}/out/census/T{T}_s*.out'))
    if not outs: continue
    N = None; tot = 0; dies = 0; surv = []; hist = collections.Counter(); samp = []; deep = []; fce = []; missing = []
    for fo in outs:
        s = re.search(r'_s(\d+)\.out$', fo).group(1)
        if not os.path.exists(fo.replace('.out', '.done')): missing.append(s)
        fl = f'{D}/logs/census/fce_T{T}_s{s}.log'
        if os.path.exists(fl):
            for l in open(fl):
                if l.startswith('FCE'):
                    m = dict(re.findall(r'(\w+)=([\d/]+)', l)); fce.append(m)
        for l in open(fo):
            if l.startswith('KHXC_SUMMARY'):
                m = dict(re.findall(r'(\w+)=([^\s]+)', l))
                tot += int(m['words']); dies += int(m['dies'])
                if m['hist']:
                    for kv in m['hist'].split(','):
                        k, c = kv.split(':'); hist[int(k)] += int(c)
            elif l.startswith('KHX '):
                g = re.search(r' g=([01]+)', l).group(1)
                if ' SURVIVES' in l: surv.append((g, l.strip()))
                elif ' samp' in l: samp.append(l.strip())
                if ' DIES' in l:
                    K = int(re.search(r'DIES K=(\d+)', l).group(1))
                    if K >= 40: deep.append(l.strip())
    nsh = int(fce[0]['shard'].split('/')[1]) if fce else None
    totals = set(int(m['total']) for m in fce); prims = set(int(m['primitive']) for m in fce)
    emitted = sum(int(m['emitted']) for m in fce)
    csv_tot, csv_prim = CSV.get(T, (None, None))
    ok = (len(fce) == nsh and not missing and totals == {csv_tot} and prims == {csv_prim} and emitted == csv_tot and tot == csv_tot)
    res = dict(T=T, shards=len(outs), shards_expected=nsh, missing_done=missing, words_khxc=tot, fce_total=sorted(totals),
               fce_primitive=sorted(prims), fce_emitted_sum=emitted, csv_total=csv_tot, csv_primitive=csv_prim, counts_ok=ok,
               dies=dies, survivors=len(surv), hist=dict(sorted(hist.items())), maxK=max(hist) if hist else None,
               sampled=len(samp), deep_deaths_K40=len(deep))
    json.dump(res, open(f'{D}/out/census/summary_T{T}.json', 'w'), indent=1)
    with open(f'{D}/out/census/surv_T{T}.txt', 'w') as f:
        for g, l in surv:
            r = root(g); typ = 'prim' if r == g else f'imprim(root {len(r)})'
            reason = re.search(r'reason=(\w+)', l).group(1); Kr = re.search(r'SURVIVES K=(\d+)', l).group(1)
            f.write(f'{T} {g} {reason} {Kr} {typ}\n')
    with open(f'{D}/out/census/samp_T{T}.txt', 'w') as f:
        for l in samp + deep: f.write(l + '\n')
    print(json.dumps({k: res[k] for k in ('T', 'shards', 'words_khxc', 'csv_total', 'csv_primitive', 'fce_primitive', 'counts_ok', 'dies', 'survivors', 'maxK', 'sampled', 'deep_deaths_K40')}))
