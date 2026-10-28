#!/usr/bin/env python3
"""det.py -- additional self-similarity detectors for pair words / digit words (numpy, exact where claimed).

All sequences are int arrays, least-significant end first.  'H' = half pair word  P[:ceil(n/2)].
"""
import numpy as np, zlib, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rar

M1 = 2147483647
M2 = 2147483629
_rng = np.random.default_rng(12345)
B1 = int(_rng.integers(1000, M1 - 1000)); B2 = int(_rng.integers(1000, M2 - 1000))
_pw = {}

def _powers(m):
    """B^k mod M for k< m, for both moduli; and inverse powers (cached by size)."""
    key = m
    if key in _pw: return _pw[key]
    if len(_pw) > 6: _pw.clear()
    res = []
    for B, M in ((B1, M1), (B2, M2)):
        p = np.empty(m + 1, dtype=np.int64); inv = np.empty(m + 1, dtype=np.int64)
        p[0] = 1; inv[0] = 1; binv = pow(B, M - 2, M)
        # vectorised doubling
        cur = 1
        while cur < m + 1:
            nxt = min(2 * cur, m + 1)
            mult = pow(B, cur, M); imult = pow(binv, cur, M)
            p[cur:nxt] = (p[0:nxt - cur] * mult) % M
            inv[cur:nxt] = (inv[0:nxt - cur] * imult) % M
            cur = nxt
        res.append((p, inv, M))
    _pw[key] = res
    return res

def _winhash(h, L, pre):
    """normalised hash of every window of length L; pre = (S1,S2,[(p,inv,M),...])."""
    S1, S2, pw = pre
    m = len(h)
    s = np.arange(0, m - L + 1)
    out = []
    for S, (p, inv, M) in zip((S1, S2), pw):
        w = (S[s + L] - S[s]) % M
        out.append((w * inv[s]) % M)
    return (out[0] << 31) | out[1], s

def _prehash(h):
    m = len(h); pw = _powers(m + 1)
    hv = h.astype(np.int64) + 1
    S = []
    for (p, inv, M) in pw:
        t = (hv * p[:m]) % M
        c = np.concatenate((np.zeros(1, np.int64), np.cumsum(t) % M))
        S.append(c % M)
    return S[0], S[1], pw

def lrs_nonoverlap(h, nonover=True):
    """longest repeated block with two occurrences starting >= L apart (nonover) or any two distinct starts.
    returns (L, i, j) verified by direct comparison, or (0,-1,-1)."""
    h = np.asarray(h); m = len(h)
    if m < 2: return (0, -1, -1)
    pre = _prehash(h)
    def exists(L):
        if L <= 0: return None
        key, s = _winhash(h, L, pre)
        order = np.argsort(key, kind='stable')
        ks = key[order]; ss = s[order]
        same = ks[1:] == ks[:-1]
        if not same.any(): return None
        # group boundaries
        idx = np.flatnonzero(same)           # pairs (idx, idx+1) in same group
        # first/last of runs of same: compute via run starts
        grp_start = np.concatenate(([True], ~same))
        gid = np.cumsum(grp_start) - 1
        first = ss[grp_start]
        lastpos = np.flatnonzero(np.concatenate((~same, [True])))
        last = ss[lastpos]
        ok = (last - first) >= (L if nonover else 1)
        if not ok.any(): return None
        k = int(np.flatnonzero(ok)[0])
        i, j = int(first[k]), int(last[k])
        if np.array_equal(h[i:i + L], h[j:j + L]): return (i, j)
        return None   # hash collision (negligible)
    lo, hi = 0, m // 2 if nonover else m - 1
    best = (0, -1, -1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        r = exists(mid)
        if r is not None: lo = mid; best = (mid, r[0], r[1])
        else: hi = mid - 1
    return best

def half(P):
    n = len(P); return P[:(n + 1) // 2]

def comp_ratio(h):
    raw = h.astype(np.uint8).tobytes()
    return len(zlib.compress(raw, 9)) / max(1, len(raw))

def hist(h, K):
    return np.bincount(h, minlength=K).tolist()

def static_panel(d, P, b, imax=300, do_lrs=True):
    """static structure statistics of one element given digits d (int16) and pair word P (full, symmetric)."""
    n = len(d); H = half(P).astype(np.int64); m = len(H); nb = b - 1
    out = {'n': n}
    # neutral coefficient runs
    st, ln = rar.runs_of(H == nb)
    out['r9_max'] = int(ln.max()) if len(ln) else 0
    out['r9_n2'] = int((ln >= 2).sum()); out['r9_n3'] = int((ln >= 3).sum())
    srt = np.sort(ln)[::-1]
    out['r9_top3'] = srt[:3].tolist()
    bb = rar.best_band(P, b)
    out['band_g'] = bb[1] if bb else 0; out['band_i'] = bb[0] if bb else -1
    # runs of zero and of top value
    for name, val in (('r0', 0), ('rtop', 2 * nb)):
        s2, l2 = rar.runs_of(H == val); out[name] = int(l2.max()) if len(l2) else 0
    stc, lnc, vc = rar.const_runs(H)
    k = int(np.argmax(lnc)); out['rany'] = int(lnc[k]); out['rany_val'] = int(vc[k])
    for p in (2, 3, 4, 5, 6):
        out['per%d' % p] = rar.periodic_stretch(H, p)[0]
    # digit word runs
    stc, lnc, vc = rar.const_runs(d.astype(np.int64)); k = int(np.argmax(lnc))
    out['d_rany'] = int(lnc[k]); out['d_rany_val'] = int(vc[k])
    if do_lrs:
        L, i, j = lrs_nonoverlap(H, True); out['lrs'] = L; out['lrs_i'] = i; out['lrs_j'] = j
        L2, i2, j2 = lrs_nonoverlap(d.astype(np.int64), True); out['dlrs'] = L2
    out['cr'] = round(comp_ratio(H), 4)
    out['hist'] = hist(H, 2 * b - 1)
    return out

def common_prefix(a, b_):
    L = min(len(a), len(b_))
    if L == 0: return 0
    ne = a[:L] != b_[:L]
    if not ne.any(): return L
    return int(np.argmax(ne))

def frozen(Hcur, hist_list, qmax=24):
    """Hcur: current half pair word; hist_list: list of earlier half words, most recent LAST (index -q = step t-q).
    returns (Fb, qb, Fc, qc): longest temporal-periodic prefix (bottom frame) and 'suffix' (centre frame)."""
    Fb = Fc = 0; qb = qc = 0
    Hr = Hcur[::-1]
    for q in range(1, min(qmax, len(hist_list)) + 1):
        Hp = hist_list[-q]
        f = common_prefix(Hcur, Hp)
        if f > Fb: Fb, qb = f, q
        g = common_prefix(Hr, Hp[::-1])
        if g > Fc: Fc, qc = g, q
    return Fb, qb, Fc, qc
