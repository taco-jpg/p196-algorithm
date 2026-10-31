#!/usr/bin/env python3
"""Independent reference tools for the lattice-kink edge relaxation (base 10).

Coordinates: lower half of the pair word, x = 0 is the least significant pair.
Lattice object: exterior B (nB cells) + bulk W (period m in space, period p in time).
    cell(t, x) = B[t%p][x] if x < nB else W[t%p][(x-nB) % m]
Everything here is written from the definitions; validated against genuine
pair-word evolution (pairword_step) and, through that, against big integers.
"""
import re, random
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
BASE = 10


# ---------------------------------------------------------------- loading
def _cols(s):
    return [list(map(int, c.split(','))) for c in re.findall(r'\[([^\]]+)\]', s)]


class Lat:
    def __init__(self, name, g, B, W):
        self.name = name
        self.g = list(g); self.p = len(g)
        self.B = B; self.W = W            # B[t][x], W[t][j]
        self.nB = len(B[0]); self.m = len(W[0])
        assert len(B) == self.p and len(W) == self.p

    def cell(self, t, x):
        t %= self.p
        return self.B[t][x] if x < self.nB else self.W[t][(x - self.nB) % self.m]

    def row(self, t, length):
        return [self.cell(t, x) for x in range(length)]


def load_rec(idx):
    """idx 0,1 -> the two m=20 SCCs, 2 -> m=48 SCC of p8_scc.txt"""
    lines = [l for l in (REPO / 'calculation/decimal_frontier/lattice_formats/p8_scc.txt').read_text().splitlines()
             if l.startswith('SCC')]
    line = lines[idx]
    g = re.search(r' g=(\d+) ', line).group(1)
    pre, cyc = line.split(' cyc=', 1)
    path = pre.split(' path=', 1)[1]
    bc, wc = _cols(path), _cols(cyc)
    p = len(g)
    B = [[col[t] for col in bc] for t in range(p)]
    W = [[col[t] for col in wc] for t in range(p)]
    return Lat(f'p8rec{idx}', [int(c) for c in g], B, W)


def load_latfile(fn, name):
    tok = Path(fn).read_text().split(); it = iter(tok)
    p = int(next(it)); nB = int(next(it)); m = int(next(it)); b = int(next(it))
    g = [int(next(it)) for _ in range(p)]
    W = [[int(next(it)) for _ in range(m)] for _ in range(p)]
    cup = [[int(next(it)) for _ in range(m)] for _ in range(p)]
    B = [[int(next(it)) for _ in range(nB)] for _ in range(p)]
    return Lat(name, g, B, W)


def load(name):
    d = REPO / 'calculation/decimal_frontier/lattice_kinks/data'
    if name == 'rec0': return load_rec(0)
    if name == 'rec1': return load_rec(1)
    if name == 'rec2': return load_rec(2)
    if name == 'p12m9': return load_latfile(d / 'lat_p12m9.txt', 'p12m9')
    raise KeyError(name)


# ---------------------------------------------------------------- genuine dynamics
def pairword_step(P):
    """full palindromic pair word -> next pair word, overflow bit"""
    n = len(P); O = []; c = 0
    for v in P:
        s = v + c; O.append(s % BASE); c = s // BASE
    if c: O.append(c)
    n2 = len(O)
    return [O[i] + O[n2 - 1 - i] for i in range(n2)], n2 - n


def carries(P):
    """carry INTO each position of the full pair word (a[0]=0), and the overflow"""
    car = []; c = 0
    for v in P:
        car.append(c); c = (v + c) // BASE
    return car, c


def full_from_lower(low, n):
    """palindromic full word of length n from lower half (h = ceil(n/2) cells)"""
    h = (n + 1) // 2
    assert len(low) == h
    return low + low[:n // 2][::-1]


# ---------------------------------------------------------------- local rule
def window_step(lat, t, c, n, win, Din, ghost):
    """One step of the K-window [c, c+K) at time t (number length n, used only for the
    frame shift dh = 1 iff g=1 and n even).  Cells below c are exact lattice at time t.
    Din   = descending carry into the mirror of the window's top cell (from cell c+K).
    ghost = e-digit of cell c+K (0..9), only used when the frame shifts.
    Returns (new_win, ok) where ok = all lattice cells below the new frame are still exact lattice
    at t+1 (including the cell left behind by a frame shift)."""
    K = len(win); g = lat.g[t % lat.p]
    dh = 1 if (g == 1 and n % 2 == 0) else 0
    # ascending carries: lattice below is exact, so carry into c is the bulk carry
    a = bulk_up_carry(lat, t, c)
    e = []; up = a
    for v in win:
        s = v + up; e.append(s % BASE); up = s // BASE
    # descending carries inside the window (D[i] = carry into mirror of cell c+i)
    D = [0] * K; D[K - 1] = Din
    for i in range(K - 1, 0, -1):
        D[i - 1] = (win[i] + D[i]) // BASE
    r = [(win[i] + D[i]) % BASE for i in range(K)]
    Dbelow = (win[0] + D[0]) // BASE            # carry into mirror of lattice cell c-1
    ok = True
    # lattice cells below c: only cells whose r-digit (or e via nothing) changes can break.
    # r_{x} for x<c changes iff the actual descending carry differs from the bulk one.
    x = c - 1; Dx = Dbelow
    r_low = {}                                  # actual r for lattice cells that differ
    while x >= 0:
        Lx = lat.cell(t, x)
        Dnom = bulk_down_carry(lat, t, x)
        if Dx == Dnom:
            break
        r_low[x] = (Lx + Dx) % BASE
        Dx = (Lx + Dx) // BASE
        x -= 1
    # check lattice cells x < c+dh at t+1 whose inputs changed
    for xx in sorted(r_low):
        tgt = xx + g                             # cell receiving r_xx
        if tgt < c:                              # pure lattice target (e is bulk)
            val = bulk_e(lat, t, tgt) + r_low[xx]
            if val != lat.cell(t + 1, tgt): ok = False
    # new window cells
    def rr(x):            # r-digit of absolute cell x at time t (x may be below the window)
        if x >= c: return r[x - c]
        if x in r_low: return r_low[x]
        return bulk_r(lat, t, x)
    new = []
    for x in range(c, c + K + dh):
        ex = e[x - c] if x < c + K else ghost
        val = ex + rr(x - g)
        new.append(val)
    if dh:
        # cell c becomes part of the lattice region at t+1
        if new[0] != lat.cell(t + 1, c): ok = False
        new = new[1:]
    return new, ok


# bulk carries / digits (computed from long lattice rows; cached)
_cache = {}


def _bulk(lat, t):
    key = (lat.name, t % lat.p)
    if key in _cache: return _cache[key]
    t %= lat.p
    L = lat.nB + 40 * lat.m
    row = lat.row(t, L)
    up = []; c = 0
    for v in row:
        up.append(c); c = (v + c) // BASE
    # descending: iterate from the top with a periodic tail long enough to converge
    dn = [0] * L; d = 0
    for x in range(L - 1, -1, -1):
        dn[x] = d; d = (row[x] + d) // BASE
    # sanity: steady state in the middle is periodic
    mid = lat.nB + 20 * lat.m
    for j in range(lat.m):
        assert dn[mid + j] == dn[mid + j + lat.m] and up[mid + j] == up[mid + j + lat.m]
    _cache[key] = (row, up, dn, mid)
    return _cache[key]


def _bx(lat, x):
    """map absolute x >= nB into the steady middle region"""
    if x < lat.nB: return x
    row_mid = lat.nB + 20 * lat.m
    return row_mid + (x - lat.nB) % lat.m


def bulk_up_carry(lat, t, x):
    row, up, dn, mid = _bulk(lat, t)
    assert x >= lat.nB + 2 * lat.m, 'window must sit in the steady bulk'
    return up[_bx(lat, x)]


def bulk_down_carry(lat, t, x):
    """descending carry into mirror of cell x in the bulk lattice continued upward"""
    row, up, dn, mid = _bulk(lat, t)
    if x < lat.nB:
        return dn[x]
    return dn[_bx(lat, x)]


def bulk_e(lat, t, x):
    return (lat.cell(t, x) + bulk_up_carry_any(lat, t, x)) % BASE


def bulk_up_carry_any(lat, t, x):
    row, up, dn, mid = _bulk(lat, t)
    return up[x] if x < lat.nB + 2 * lat.m else up[_bx(lat, x)]


def bulk_r(lat, t, x):
    return (lat.cell(t, x) + bulk_down_carry(lat, t, x)) % BASE


def check_bulk(lat):
    """the lattice continued upward is an exact solution: row t -> row t+1 (positions >= nB+2m)"""
    bad = 0
    for t in range(lat.p):
        g = lat.g[t]
        for x in range(lat.nB + 2 * lat.m, lat.nB + 4 * lat.m):
            val = bulk_e(lat, t, x) + bulk_r(lat, t, x - g)
            if val != lat.cell(t + 1, x): bad += 1
    return bad
