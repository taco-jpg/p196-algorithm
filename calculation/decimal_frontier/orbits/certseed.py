#!/usr/bin/env python3
"""certseed.py -- real integer orbits of the Lean certificate seeds (bases 2,4,8,16,32,11,17,26 and PR#356 base 20):
 (1) replay: the pair word of x_t equals tmpl(B_{t+1},C_{t+1},g_{t+1}) predicted by the cycle, for many steps; no palindrome;
 (2) perturbation experiments: change one digit of the seed (in B zone / lower band / C zone / upper band / top digits), follow the
     orbit and record how long the observed best single-band template stays inside a certificate basin (mirror canonical run = cycle with cert).
usage: certseed.py replay | perturb BASE G NPERT STEPS
"""
import sys, os, re, json, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rar, nbs

PR356 = "/home/claude/r/lean/P196/Agent116Base20Certificate/Certificate.lean"

def load_certs():
    certs = {b: es for b, es in nbs._lean_certs()}
    src = open(PR356).read()
    L = lambda s: [int(x) for x in s.split(",")] if s.strip() else []
    defs = {m[1]: L(m[2]) for m in re.finditer(r"def (\w+)\s*:\s*List Nat\s*:=\s*\[([^\]]*)\]", src)}
    m = re.search(r"def cert20\s*:\s*List Edge\s*:=\s*(\[.*?\])\n\n", src, re.S)
    es = [(defs[e[1]], defs[e[2]], defs[e[3]], defs[e[4]], int(e[5]), int(e[6])) for e in
          re.finditer(r"⟨(\w+), (\w+), (\w+), (\w+), (\d+), (\d+)⟩", m[1])]
    certs[20] = es
    return certs

def tmpl(b, B, C, g): return list(B) + [b - 1] * g + list(C) + [b - 1] * g + list(B[::-1])

def digits_of_template(b, w):
    d, c = rar.normalize(np.array(w, dtype=np.int64), b)
    d = d.astype(np.int16)
    if c: d = np.concatenate((d, np.array([1], dtype=np.int16)))
    return d

def replay(b, es, g0, steps):
    B, C = es[0][0], es[0][1]
    d = digits_of_template(b, tmpl(b, B, C, g0))
    g = g0; k = 0; ok = True; pal = None; first_bad = None
    for t in range(steps):
        if rar.is_pal(d): pal = t; break
        P = rar.pairword(d)
        E = es[k % len(es)]
        gm = nbs.gam(b, E[0], E[1])
        g = g - gm + E[4] + E[5]
        nB, nC = E[2], E[3]
        pred = np.array(tmpl(b, nB, nC, g))
        if len(pred) != len(P) or not np.array_equal(pred, P):
            ok = False; first_bad = t; break
        d, _, _ = rar.revadd(d, b); k += 1
    return ok, pal, first_bad, g

def basin_run(b, d, steps, imax=300):
    """follow orbit of digit array d; at each step: best single-band template, mirror run outcome.  Returns list of outcome strings"""
    out = []
    for t in range(steps):
        if rar.is_pal(d): out.append('PAL'); break
        P = rar.pairword(d)
        bb = [x for x in rar.bands(P, b, ming=2) if x[0] <= imax]
        res = 'none'
        if bb:
            i, g, L = max(bb, key=lambda x: (x[1], -x[0])); n = len(P)
            B = P[:i].tolist(); C = P[i + g:n - i - g].tolist()
            if len(B) + len(C) <= 350:
                r = nbs.run(b, B, C, maxsteps=1200, maxlen=500)
                res = r[0] if r[0] != 'cycle' else ('cert' if nbs.is_cert(b, r[1]) else 'cyc-nocert')
                if r[0] in ('break',): res = 'break'
            else: res = 'big'
        out.append(res)
        d, _, _ = rar.revadd(d, b)
    return out

if __name__ == '__main__':
    certs = load_certs()
    if sys.argv[1] == 'replay':
        for b in sorted(certs):
            es = certs[b]
            for g0 in (4, 6, 40):
                ok, pal, bad, g = replay(b, es, g0, 600)
                print(f"base {b:2d} edges {len(es):2d} |B|={[len(e[0]) for e in es][:3]}.. |C|={[len(e[1]) for e in es][:3]}.. g0={g0:3d}: 600-step replay template==pairword {ok} palindrome {pal} first_bad {bad} final g {g}")
    elif sys.argv[1] == 'perturb':
        b = int(sys.argv[2]); g0 = int(sys.argv[3]); NP = int(sys.argv[4]); steps = int(sys.argv[5])
        es = certs[b]; B, C = es[0][0], es[0][1]
        base = digits_of_template(b, tmpl(b, B, C, g0))
        n = len(base); rng = np.random.default_rng(b * 1000 + g0)
        lb, lc = len(B), len(C)
        zones = {'B_low': (0, lb), 'band_low': (lb, lb + g0), 'C_low': (lb + g0, lb + g0 + lc // 2 + 1),
                 'C_up': (lb + g0 + lc // 2 + 1, lb + g0 + lc), 'band_up': (lb + g0 + lc, lb + 2 * g0 + lc), 'B_up': (lb + 2 * g0 + lc, n)}
        res = collections.defaultdict(list)
        # control
        ctl = basin_run(b, base.copy(), steps)
        print('control (unperturbed) outcomes:', collections.Counter(ctl))
        for zname, (lo, hi) in zones.items():
            hi = min(hi, n)
            if hi <= lo: continue
            for _ in range(NP):
                pos = int(rng.integers(lo, hi)); dd = base.copy()
                dd[pos] = (int(dd[pos]) + int(rng.integers(1, b))) % b
                if dd[-1] == 0: dd[-1] = 1
                oc = basin_run(b, dd, steps)
                # lifetime = number of initial steps with outcome 'cert'
                life = 0
                for o in oc:
                    if o == 'cert': life += 1
                    else: break
                res[zname].append((life, oc[-1] if oc else None, sum(1 for o in oc if o == 'cert')))
        for zname in zones:
            if zname not in res: continue
            lv = np.array([x[0] for x in res[zname]]); tot = np.array([x[2] for x in res[zname]])
            print(f"zone {zname:9s}: n={len(lv)}  cert-basin lifetime (initial run): mean {lv.mean():.2f} median {np.median(lv):.0f} max {lv.max()}  frac(life>=steps) {np.mean(lv >= steps):.2f}  any-cert-steps mean {tot.mean():.1f} final outcomes {dict(collections.Counter(x[1] for x in res[zname]).most_common(3))}")
