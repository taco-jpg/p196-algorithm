#!/usr/bin/env python3
"""replay_fast.py -- numpy-accelerated integer replay of a hybrid cycle in a power-of-two base (control) .
Checks at EVERY step: pairs(digits(X_s)) == template(B_{s+1},C_{s+1},c_{s+1},g_{s+1},h_{s+1}) and X_s is not a palindrome.
usage: replay_fast.py <steps> [out.json]"""
import sys, json, time
import numpy as np
from hyb import *
from ext import *
from replay import verify_cycle, find_cycles

def digits_b4(X):
    nb = (X.bit_length() + 7) // 8
    a = np.frombuffer(X.to_bytes(nb, 'little'), dtype=np.uint8)
    d = np.stack([a & 3, (a >> 2) & 3, (a >> 4) & 3, (a >> 6) & 3], axis=1).reshape(-1)
    n = len(d)
    while n and d[n - 1] == 0: n -= 1
    return d[:n].astype(np.int16)

def val_b4(d):
    n = len(d); pad = (-n) % 4
    d = np.concatenate([d, np.zeros(pad, dtype=d.dtype)]).astype(np.uint8).reshape(-1, 4)
    byt = d[:, 0] | (d[:, 1] << 2) | (d[:, 2] << 4) | (d[:, 3] << 6)
    return int.from_bytes(byt.astype(np.uint8).tobytes(), 'little')

def tmpl_np(b, B, C, c, g, h):
    N = b - 1
    return np.concatenate([np.array(B, dtype=np.int16), np.full(g, N, dtype=np.int16), np.array(C, dtype=np.int16),
                           np.full(h, c, dtype=np.int16), np.array(C[::-1], dtype=np.int16), np.full(g, N, dtype=np.int16), np.array(B[::-1], dtype=np.int16)])

def replay_fast(b, cyc, ph, C0, c0, steps, g0=None, h0=None, log=None):
    assert b == 4
    vc = verify_cycle(b, cyc, ph, C0, c0)
    assert vc['ok'] and vc['hybrid_ok'], vc
    es = vc['edges']; T = vc['T']
    if g0 is None: g0 = 3 + 2 * T
    if h0 is None: h0 = 3 + 3 * T + 2 * vc['Sp']
    B, C, c = es[0][1], es[0][2], es[0][3]
    g, h = g0, h0
    P0 = tmpl_np(b, B, C, c, g, h)
    assert np.array_equal(P0, P0[::-1])
    X = val_b4(P0 & 3) + (val_b4(P0 >> 2) << 2)
    # sanity: val_b4 agrees with generic val on the first template
    assert X == val(b, [int(x) for x in P0])
    mg, mh = g, h
    t0 = time.time()
    for s in range(steps):
        e = es[s % T]
        gam, u, v, p = e[7], e[8], e[9], e[10]
        d = digits_b4(X)
        if np.array_equal(d, d[::-1]): return dict(ok=False, why='palindrome at step %d' % s)
        g1 = g - gam + u + v; h1 = h - 2 + gam + 2 * p
        Pn = tmpl_np(b, e[4], e[5], e[6], g1, h1)
        act = d + d[::-1]
        if len(act) != len(Pn) or not np.array_equal(act, Pn):
            return dict(ok=False, why='template mismatch at step %d' % s)
        if g1 < 3 or h1 < 3: return dict(ok=False, why='g/h too small at step %d' % s)
        mg = min(mg, g1); mh = min(mh, h1)
        X = X + val_b4(d[::-1])
        g, h = g1, h1
        if log and s % 2000 == 0: print(f"  step {s} digits={len(d)} g={g} h={h} {time.time()-t0:.1f}s", file=log, flush=True)
    return dict(ok=True, steps=steps, T=T, g0=g0, h0=h0, g_final=g, h_final=h, min_g=mg, min_h=mh, digits_final=len(digits_b4(X)),
                vc={k: vc[k] for k in ('Sgam', 'A', 'Su', 'Sp', 'dg', 'dh')})

if __name__ == '__main__':
    steps = int(sys.argv[1]); outj = sys.argv[2] if len(sys.argv) > 2 else None
    b = 4
    an = parse_accepts('/home/claude/research/w1_bases/out/ext4/b4_p12.txt')
    done = False
    for a in an:
        cyc = cycle_from(b, a['Bs'][0])
        if cyc is None: continue
        cvals = [c for c in range(2 * b - 1) if c != b - 1]
        for (C, c, ph) in find_cycles(b, cyc, 1, cvals, maxcount=5):
            vc = verify_cycle(b, cyc, ph, C, c)
            if not vc['hybrid_ok']: continue
            print('control cycle: stream gam=%s e1=%s T=%d C=%s c=%d ph=%d Sgam=%d A=%d dg=%d dh=%d' % (
                ''.join(str(x[1]) for x in cyc), ''.join(str(x[2]) for x in cyc), vc['T'], C, c, ph, vc['Sgam'], vc['A'], vc['dg'], vc['dh']), flush=True)
            r = replay_fast(b, cyc, ph, C, c, steps, log=sys.stdout)
            print('REPLAY', r, flush=True)
            if outj and r.get('ok'):
                json.dump(dict(base=b, label='CONTROL base 4 hybrid cycle (positive control for the engine)', B_cycle=[[list(x[0]), x[1], x[2], x[3]] for x in cyc],
                               phase=ph, C=C, c=c, result=r), open(outj, 'w'))
            done = True; break
        if done: break
