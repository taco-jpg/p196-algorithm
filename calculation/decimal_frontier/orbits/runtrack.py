#!/usr/bin/env python3
"""runtrack.py BASE SEEDSPEC T L0 [OUT.json] -- dense space-time tracking of constant runs (length >= L0) of the half pair word.

Each step: maximal constant runs of H = P[:ceil(n/2)] with length >= L0.  Runs at consecutive steps are linked if their index
intervals (bottom frame) overlap (greedy by overlap size, same track absorbs at most one run).  A track = (birth, death, positions,
value history, length history).  Reports lifetime distribution per value class (neutral b-1, zero, top 2(b-1), other) and the longest tracks.
"""
import sys, os, json, time, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rar, orbit2

def runs_ge(H, L0):
    st, ln, v = rar.const_runs(H)
    k = ln >= L0
    return list(zip(st[k].tolist(), ln[k].tolist(), v[k].tolist()))

def track(b, dig, T, L0=4, tmax=1e9, wanted_len=None):
    d = dig.copy(); tracks = []; active = {}   # active: id -> (lo, hi, value)
    t0 = time.time(); nid = 0; pal = None; gam_hist = []
    for t in range(T + 1):
        n = len(d); P = rar.pairword(d)
        if rar.is_pal(d): pal = t; break
        H = P[:(n + 1) // 2]
        runs = runs_ge(H, L0)
        new_active = {}
        used = set()
        # match
        cand = []
        for ri, (s, l, v) in enumerate(runs):
            for tid, (lo, hi, val) in active.items():
                ov = min(hi, s + l) - max(lo, s)
                if ov > 0: cand.append((-ov, ri, tid))
        cand.sort()
        rused = set(); tused = set()
        for negov, ri, tid in cand:
            if ri in rused or tid in tused: continue
            rused.add(ri); tused.add(tid)
            s, l, v = runs[ri]
            tr = tracks[tid]
            tr['death'] = t; tr['maxlen'] = max(tr['maxlen'], l)
            if tr['vals'][-1][0] != v: tr['vals'].append((v, t))
            tr['len_last'] = l
            new_active[tid] = (s, s + l, v)
        for ri, (s, l, v) in enumerate(runs):
            if ri in rused: continue
            tracks.append({'birth': t, 'death': t, 'maxlen': l, 'len0': l, 'start0': s, 'vals': [(v, t)], 'len_last': l, 'n0': n})
            new_active[len(tracks) - 1] = (s, s + l, v)
        active = new_active
        nd, c = rar.normalize(P, b)
        if c: nd = np.concatenate((nd, np.array([1], dtype=np.int16)))
        gam_hist.append(c)
        d = nd
        if time.time() - t0 > tmax: break
    return tracks, pal, len(gam_hist)

def summarize(b, tracks, T, L0):
    nb = b - 1
    def cls(tr):
        v0 = tr['vals'][0][0]
        return 'neutral' if v0 == nb else 'zero' if v0 == 0 else 'top' if v0 == 2 * nb else 'other'
    out = {}
    for c in ('neutral', 'zero', 'top', 'other', 'all'):
        sel = [tr for tr in tracks if c == 'all' or cls(tr) == c]
        if not sel: out[c] = None; continue
        life = np.array([tr['death'] - tr['birth'] + 1 for tr in sel]); mx = np.array([tr['maxlen'] for tr in sel])
        out[c] = {'n': len(sel), 'life_mean': float(life.mean()), 'life_q': np.quantile(life, [.5, .9, .99]).tolist(), 'life_max': int(life.max()),
                  'maxlen_mean': float(mx.mean()), 'maxlen_max': int(mx.max())}
    return out

if __name__ == '__main__':
    b = int(sys.argv[1]); seed = sys.argv[2]; T = int(sys.argv[3]); L0 = int(sys.argv[4])
    dig = orbit2.parse_seed(seed, b)
    tracks, pal, steps = track(b, dig, T, L0)
    s = summarize(b, tracks, T, L0)
    print('steps', steps, 'pal', pal, 'ntracks', len(tracks))
    for k, v in s.items(): print(k, v)
    top = sorted(tracks, key=lambda tr: -(tr['death'] - tr['birth']))[:8]
    for tr in top: print({k: tr[k] for k in ('birth', 'death', 'maxlen', 'len0', 'start0', 'n0')}, 'vals', tr['vals'][:8])
    if len(sys.argv) > 5:
        json.dump({'summary': s, 'top': top}, open(sys.argv[5], 'w'))
