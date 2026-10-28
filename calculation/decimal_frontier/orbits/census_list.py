#!/usr/bin/env python3
"""census_list.py OUT NS T minlen maxlen base1 base2 ... -- random-seed regularization census (see census.py), arbitrary base list."""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census, rar
out = open(sys.argv[1], 'a'); NS, T, mn, mx = map(int, sys.argv[2:6]); bases = [int(x) for x in sys.argv[6:]]
for b in bases:
    rng = np.random.default_rng(5000 + b); t0 = time.time()
    cnt = {'dead': 0, 'regular': 0, 'other': 0}; regs = []
    for s in range(NS):
        nd = int(rng.integers(mn, mx + 1)); dg = rng.integers(0, b, size=nd).astype(np.int16); dg[-1] = rng.integers(1, b)
        st, t, info = census.run_seed(b, dg, T)
        cnt[st] += 1
        if st == 'regular':
            e, cyc = census.entry_dense(b, dg, T)
            regs.append({'seed': rar.to_int(dg, b), 'entry': e, 'cyc': cyc})
    res = {'base': b, 'NS': NS, 'T': T, 'len': [mn, mx], 'counts': cnt, 'regular': regs, 'secs': round(time.time() - t0, 1)}
    out.write(json.dumps(res) + '\n'); out.flush()
    ents = sorted(r['entry'] for r in regs)
    print(f"b={b} dead={cnt['dead']} regular={cnt['regular']} other={cnt['other']} entries(min/med/max)={ents[0] if ents else None}/{ents[len(ents)//2] if ents else None}/{ents[-1] if ents else None} cycs={sorted(set((r['cyc'].get('len'), r['cyc'].get('sumgam'), r['cyc'].get('cert')) for r in regs if r['cyc']))[:5]} {res['secs']}s", flush=True)
