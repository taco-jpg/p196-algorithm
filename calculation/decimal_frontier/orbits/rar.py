#!/usr/bin/env python3
"""rar.py -- vectorised reverse-and-add orbits in any base b and orbit-structure detectors (W4 'orbits').

Conventions (match the mirror neutral_band_search.py): numbers are digit lists / arrays LEAST significant
digit first.  The 'pair word' of x with n digits is P_i = d_i + d_{n-1-i}  (symmetric).  Next orbit element is
the carry-normalisation of P (possibly with one extra top digit; that extra digit is 'gam').

Everything here is exact integer arithmetic (numpy int16), validated against Python big ints in selfcheck().
"""
import numpy as np, zlib, math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nbs  # exact mirror copy (selftest-validated) of neutral_band_search.py

_AR = {}
def _arange(n):
    a = _AR.get(n)
    if a is None:
        if len(_AR) > 8: _AR.clear()
        a = np.arange(n, dtype=np.int32); _AR[n] = a
    return a

# ------------------------------------------------------------------ conversion
def to_digits(x, b):
    d = []
    while x:
        d.append(x % b); x //= b
    return np.array(d, dtype=np.int16)

def to_int(d, b):
    # divide-and-conquer-free Horner is fine for n <= ~20000; use python ints
    r = 0
    for v in reversed([int(v) for v in d]): r = r * b + v
    return r

def pairword(d):
    return d + d[::-1]

def normalize(P, b):
    """carry-normalise coefficient array P (values in [0, 2b-2]) -> (digits int16, final carry 0/1)."""
    n = len(P)
    gen = P >= b
    prop = P == (b - 1)
    idx = np.where(prop, np.int32(-1), _arange(n))
    last = np.maximum.accumulate(idx)
    safe = np.maximum(last, 0)
    cout = gen[safe] & (last >= 0)           # carry out of position i
    cin = np.empty(n, dtype=np.int16)
    cin[0] = 0
    cin[1:] = cout[:-1]
    dig = (P + cin) % b
    return dig.astype(np.int16), int(cout[-1])

def revadd(d, b):
    """one reverse-and-add step.  returns (next_digits, P, gam)"""
    P = pairword(d)
    nd, c = normalize(P, b)
    if c: nd = np.concatenate((nd, np.array([1], dtype=np.int16)))
    return nd, P, c

def is_pal(d):
    return bool(np.array_equal(d, d[::-1]))

def selfcheck(b=10, seed=196, steps=300):
    x = seed; d = to_digits(seed, b)
    for t in range(steps):
        d, P, c = revadd(d, b)
        x = nbs.rev_add(b, x)
        assert to_int(d, b) == x, (b, seed, t)
    return True

# ------------------------------------------------------------------ run / interval helpers
def runs_of(mask):
    m = np.concatenate((np.zeros(1, np.int8), mask.astype(np.int8), np.zeros(1, np.int8)))
    dm = np.diff(m)
    st = np.flatnonzero(dm == 1); en = np.flatnonzero(dm == -1)
    return st, en - st

def const_runs(h):
    """maximal runs of equal value: (starts, lens, values)"""
    m = len(h)
    if m == 0: return np.zeros(0, int), np.zeros(0, int), np.zeros(0, int)
    chg = np.flatnonzero(h[1:] != h[:-1]) + 1
    st = np.concatenate(([0], chg)); en = np.concatenate((chg, [m]))
    return st, en - st, h[st]

def longest_val_run(h, val):
    st, ln = runs_of(h == val)
    if len(ln) == 0: return (0, -1)
    k = int(np.argmax(ln)); return (int(ln[k]), int(st[k]))

def periodic_stretch(h, p):
    """longest stretch of h with h[i]==h[i+p] throughout and the length-p window NOT constant
    (i.e. genuinely period-p, not just a constant run).  returns (length, start)."""
    m = len(h)
    if m <= p + 1: return (0, -1)
    eq = h[p:] == h[:-p]                      # length m-p
    chg = h[1:] != h[:-1]                     # length m-1
    nc = np.zeros(m - p, dtype=bool)
    for k in range(p - 1): nc |= chg[k:k + (m - p)]
    st, ln = runs_of(eq & nc)
    if len(ln) == 0: return (0, -1)
    k = int(np.argmax(ln)); return (int(ln[k]) + p, int(st[k]))

# ------------------------------------------------------------------ template (single neutral band) detector
def bands(P, b, ming=1):
    """all maximal runs of the neutral coefficient b-1 starting in the first half of the (symmetric) word P.
    returns list of (start i, g, runlen); g = min(runlen, (n-2i)//2) exactly as nbs.template_of (but also i == 0)."""
    n = len(P)
    st, ln = runs_of(P == (b - 1))
    out = []
    for i, L in zip(st.tolist(), ln.tolist()):
        if i >= n // 2: break
        g = min(L, (n - 2 * i) // 2)
        if g >= ming: out.append((i, g, L))
    return out

def best_band(P, b):
    """the band with largest g (ties: smallest start).  (i, g, L) or None"""
    bs = bands(P, b)
    if not bs: return None
    return max(bs, key=lambda t: (t[1], -t[0]))

def template(P, b, band=None):
    n = len(P)
    band = band or best_band(P, b)
    if band is None: return None
    i, g, L = band
    return (P[:i].tolist(), P[i + g:n - i - g].tolist(), g, i, L)

# ------------------------------------------------------------------ full per-step detector panel
def compress_ratio(arr):
    raw = arr.astype(np.uint8).tobytes()
    return len(zlib.compress(raw, 6)) / max(1, len(raw))

def panel(d, P, b, heavy=True):
    """structure statistics for one orbit element (digit array d, its pair word P)."""
    n = len(d)
    h = P[:(n + 1) // 2]
    out = {'n': n}
    nb = b - 1
    # neutral coefficient runs in the half pair word
    L9, s9 = longest_val_run(h, nb); out['pw_run_nb'] = L9; out['pw_run_nb_start'] = s9
    bb = best_band(P, b)
    out['band_i'], out['band_g'] = (bb[0], bb[1]) if bb else (-1, 0)
    L0, s0 = longest_val_run(h, 0); out['pw_run_0'] = L0
    L2, s2 = longest_val_run(h, 2 * nb); out['pw_run_top'] = L2
    st, ln, v = const_runs(h)
    k = int(np.argmax(ln)); out['pw_run_any'] = int(ln[k]); out['pw_run_any_val'] = int(v[k]); out['pw_run_any_start'] = int(st[k])
    for p in (2, 3, 4):
        out['pw_per%d' % p] = periodic_stretch(h, p)[0]
    # digit-word (the number itself)
    st, ln, v = const_runs(d)
    k = int(np.argmax(ln)); out['dw_run_any'] = int(ln[k]); out['dw_run_any_val'] = int(v[k])
    out['dw_run_nb'] = longest_val_run(d, nb)[0]; out['dw_run_0'] = longest_val_run(d, 0)[0]
    for p in (2, 3, 4):
        out['dw_per%d' % p] = periodic_stretch(d, p)[0]
    out['frac_nb'] = float(np.mean(h == nb))
    if heavy:
        out['cr_pw'] = compress_ratio(h); out['cr_dw'] = compress_ratio(d)
    return out

if __name__ == '__main__':
    print('selfcheck base10 196:', selfcheck(10, 196, 400))
    for b, s in ((2, 22), (3, 10), (7, 100), (11, 10), (20, 19)):
        print('selfcheck', b, s, selfcheck(b, s, 200))
