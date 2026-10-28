#!/usr/bin/env python3
"""spectrum.py BASE T NORB -- averaged periodograms of the half pair word and of the digit word of orbit snapshots; flags lines > 12x mean."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rar, base10_stats
b = int(sys.argv[1]); T = int(sys.argv[2]); NO = int(sys.argv[3])
seeds = [rar.to_digits(196, b)] + base10_stats.rand_survivors(b, NO - 1, seed=31)[0]
cps = [T // 2, T]
L = 1024
acc = {'H': np.zeros(L // 2 + 1), 'D': np.zeros(L // 2 + 1)}; accs = {'H': np.zeros(L // 2 + 1), 'D': np.zeros(L // 2 + 1)}; cnt = 0
rng = np.random.default_rng(5)
for dg in seeds:
    d = dg.copy()
    for t in range(T + 1):
        if t in cps:
            n = len(d); P = rar.pairword(d); H = P[:(n + 1) // 2].astype(float); D = d.astype(float)
            for name, X in (('H', H), ('D', D)):
                for off in (len(X) // 8, len(X) // 2 - L // 2):   # two windows per snapshot (bulk, not ends)
                    w = X[off:off + L]; w = w - w.mean()
                    f = np.abs(np.fft.rfft(w * np.hanning(L))) ** 2
                    acc[name] += f
                    ws = rng.permutation(X[off:off + L]); ws = ws - ws.mean()
                    accs[name] += np.abs(np.fft.rfft(ws * np.hanning(L))) ** 2
            cnt += 2
        d, _, _ = rar.revadd(d, b)
for name in ('H', 'D'):
    S = acc[name] / cnt; Ss = accs[name] / cnt
    ratio = S / Ss
    print(name, 'mean power ratio orbit/shuffled over freq bins (should be ~1 if white):', np.round(np.mean(ratio[1:]), 3))
    # print coarse spectrum ratio in 16 bands
    bands = np.array_split(np.arange(1, len(S)), 16)
    print('  coarse ratio by band:', [round(float(np.mean(ratio[bd])), 2) for bd in bands])
    # lines
    thr = 12
    peaks = [(int(k), round(float(ratio[k]), 1), round(L / k, 3)) for k in range(1, len(S)) if ratio[k] > 6 and S[k] > 6 * np.mean(Ss)]
    print('  bins with orbit/shuffled power >6 (bin, ratio, period):', peaks[:20])
    print('  max single-bin ratio', round(float(ratio[1:].max()), 2), 'at period', round(L / (1 + int(np.argmax(ratio[1:]))), 3), ' snapshots', cnt)
