#!/usr/bin/env python3
"""life_study.py OUT.json base1 base2 ... -- single-band template lifetime study for each base (calls cpp/tpl sequentially).
 (a) tpl rand: N random templates (|B|<=LB, symmetric |C|<=LC; cells = sum of two uniform digits): lifetime histogram, tail slope, break reasons.
 (b) tpl climb: hill-climbing for longest lifetime; cycles found.
 (c) nested family B=[B1], C=[x, (b-1)^m, x]: best lifetime over (B1,x) as function of m; slope.
"""
import sys, os, json, subprocess, time, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TPL = os.path.join(HERE, 'cpp', 'tpl')

def parse(out):
    hist = {}; top = []; hdr = {}
    for line in out.split('\n'):
        if line.startswith('# cycles'):
            parts = line.replace('(', ' ').replace(')', ' ').split()
            hdr['cycles'] = int(parts[1].split('=')[1]); hdr['certs'] = int(parts[3]); hdr['grow'] = int(parts[4].split('=')[1]); hdr['long'] = int(parts[5].split('=')[1])
        elif line.startswith('H '):
            _, t, c, r1, r2, r3 = line.split(); hist[int(t)] = (int(c), int(r1), int(r2), int(r3))
        elif line.startswith('T '):
            top.append(line[2:])
    return hdr, hist, top

def tail_slope(hist, lo=6, hi=40):
    ts = [t for t in range(lo, hi + 1) if hist.get(t, (0,))[0] >= 5]
    if len(ts) < 4: return None
    y = np.log([hist[t][0] for t in ts]); A = np.polyfit(ts, y, 1)
    return float(A[0])

def run_tpl(args, timeout=900):
    return subprocess.run([TPL] + [str(a) for a in args], capture_output=True, text=True, timeout=timeout).stdout

def nested(b, ms=(8, 16, 32, 64)):
    inp = []; meta = []
    for m in ms:
        for B1 in range(1, 2 * b - 1):
            for x in range(0, 2 * b - 1):
                C = [x] + [b - 1] * m + [x]
                inp.append(f"1 {B1} {len(C)} {' '.join(map(str, C))}"); meta.append((m, B1, x))
    out = subprocess.run([TPL, 'eval', str(b), '3000'], input='\n'.join(inp) + '\n', capture_output=True, text=True).stdout.split('\n')
    best = {}; nonbreak = 0
    for (m, B1, x), line in zip(meta, out):
        k, t, rea, cl, sg, gn = map(int, line.split())
        if k != 0: nonbreak += 1; continue
        if t > best.get(m, (0,))[0]: best[m] = (t, B1, x)
    ms2 = sorted(best); slope = float(np.polyfit(ms2, [best[m][0] for m in ms2], 1)[0]) if len(ms2) >= 3 else None
    return {'best': {m: best[m] for m in best}, 'slope': slope, 'nonbreak': nonbreak}

if __name__ == '__main__':
    outfn = sys.argv[1]; bases = [int(x) for x in sys.argv[2:]]
    res = json.load(open(outfn)) if os.path.exists(outfn) else {}
    for b in bases:
        t0 = time.time(); R = {}
        o = run_tpl(['rand', b, 3000000, 11, 10, 16, 400]); hdr, hist, top = parse(o)
        tot = sum(v[0] for v in hist.values()) + hdr['cycles'] + hdr['grow'] + hdr['long']
        r12 = [sum(v[1] for v in hist.values()), sum(v[2] for v in hist.values()), sum(v[3] for v in hist.values())]
        R['rand'] = {'N': 3000000, 'hdr': hdr, 'frac_t0': hist.get(0, (0,))[0] / 3e6, 'maxlife': max(hist) if hist else 0,
                     'slope': tail_slope(hist), 'reasons(e1=e2=0,e1=e2=1,other)': r12, 'top': top[:3], 'hist_head': {t: hist[t][0] for t in sorted(hist)[:12]}}
        o = run_tpl(['climb', b, 800, 5, 12, 20, 4000, 600]); hdr, hist, top = parse(o)
        R['climb'] = {'restarts': 800, 'LB': 12, 'LC': 20, 'hdr': hdr, 'maxlife': max(hist) if hist else 0, 'top': top[:4]}
        R['nested'] = nested(b) if not os.environ.get('NONEST') else None
        R['secs'] = round(time.time() - t0, 1)
        res[str(b)] = R
        json.dump(res, open(outfn, 'w'))
        nl = R['nested'] or {'slope': None}
        print(f"b={b} rand: t0frac {R['rand']['frac_t0']:.3f} slope {R['rand']['slope']} maxlife {R['rand']['maxlife']} reasons {r12} | climb maxlife {R['climb']['maxlife']} cycles {R['climb']['hdr']['cycles']} certs {R['climb']['hdr']['certs']} | nested slope {nl['slope']} {R['secs']}s", flush=True)
