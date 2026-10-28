#!/usr/bin/env python3
"""gt.py -- generalized self-similar templates for reverse-and-add (W3 formats).

A TEMPLATE (base b) is a palindromic *pair word*  P = Hs ++ core ++ mirror(Hs)  (coefficients LSB first,
values in 0..2b-2) where Hs is a tuple of ITEMS describing the lower half:
    ('L', (c0,c1,...))        literal block (non-empty)
    ('B', (w0,...,w_{m-1}), pid)   band: the block w repeated g_pid times (g_pid symbolic, 'large')
and core is a palindromic literal tuple (may be empty).  mirror reverses item order, reverses literals and
band blocks, and keeps the pid, so mirrored bands share one parameter (the upper copy of band pid has
exponent g_pid too).  The single neutral band of Agent120 is Hs = (('L',B), ('B',(b-1,),0)), core = C.

step(T) computes EXACTLY (for all sufficiently large parameters; see 'assumptions') the digit word
O = digits(val(P)) (value of the pair word == reverse-and-add image of an integer with that pair word) and the next
pair word  P' = pairs(O)  as a template T' together with the parameter map  g'_j = mult*g_pid + off.

assumptions: all pids are 'large' (every comparison of a symbolic length against a constant, or of two lengths
with different symbolic parts, is decided by the pid coefficients); step raises Ambiguous / Unsupported otherwise.
Exactness is validated against big-integer reverse-and-add in test_gt.py.
"""
from math import gcd
from functools import lru_cache


class Ambiguous(Exception):
    pass


class Unsupported(Exception):
    pass


# ---------------------------------------------------------------------------------------------------
# affine lengths  c + sum d[pid]*g_pid
class Ln:
    __slots__ = ("c", "d")

    def __init__(self, c=0, d=None):
        self.c = c
        self.d = {k: v for k, v in (d or {}).items() if v}

    def __add__(self, o):
        d = dict(self.d)
        for k, v in o.d.items():
            d[k] = d.get(k, 0) + v
        return Ln(self.c + o.c, d)

    def __sub__(self, o):
        d = dict(self.d)
        for k, v in o.d.items():
            d[k] = d.get(k, 0) - v
        return Ln(self.c - o.c, d)

    def sign(self):
        if not self.d:
            return (self.c > 0) - (self.c < 0)
        pos = any(v > 0 for v in self.d.values())
        neg = any(v < 0 for v in self.d.values())
        if pos and neg:
            raise Ambiguous(repr(self))
        return 1 if pos else -1

    def is_const(self):
        return not self.d

    def __repr__(self):
        return f"Ln({self.c},{self.d})"


def ln_const(c):
    return Ln(c)


# ---------------------------------------------------------------------------------------------------
# carry normalisation
def norm(b, w, c):
    out = []
    for v in w:
        t = v + c
        out.append(t % b)
        c = t // b
    return tuple(out), c


def primitive(w):
    """(u, r) with w = u^r, u primitive"""
    m = len(w)
    for q in range(1, m + 1):
        if m % q == 0 and w[:q] * (m // q) == w:
            return w[:q], m // q
    return w, 1


def mirror_item(it):
    if it[0] == 'L':
        return ('L', it[1][::-1])
    return ('B', it[1][::-1], it[2])


class Template:
    __slots__ = ("b", "Hs", "core")

    def __init__(self, b, Hs, core):
        self.b = b
        self.Hs = tuple(Hs)
        self.core = tuple(core)

    def key(self):
        return (self.b, self.Hs, self.core)

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, o):
        return self.key() == o.key()

    def pids(self):
        return [it[2] for it in self.Hs if it[0] == 'B']

    def __repr__(self):
        return f"T({fmt(self)})"

    def lit_size(self):
        return sum(len(it[1]) for it in self.Hs if it[0] == 'L') + len(self.core)

    def validate(self):
        b = self.b
        for it in self.Hs:
            if it[0] == 'L':
                assert it[1] and all(0 <= v <= 2 * b - 2 for v in it[1]), it
            else:
                assert it[1] and all(0 <= v <= 2 * b - 2 for v in it[1]), it
        assert self.core == self.core[::-1], "core must be a palindrome"
        pids = self.pids()
        assert len(set(pids)) == len(pids)
        return True


def fmt(T):
    s = []
    for it in T.Hs:
        if it[0] == 'L':
            s.append("[" + ",".join(map(str, it[1])) + "]")
        else:
            s.append("(" + ",".join(map(str, it[1])) + ")^g%d" % it[2])
    s.append("|" + ",".join(map(str, T.core)) + "|")
    return " ".join(s)


def mk_one_band(b, B, C):
    """Agent120 template  B (b-1)^g C (b-1)^g rev B"""
    Hs = []
    if B:
        Hs.append(('L', tuple(B)))
    Hs.append(('B', (b - 1,), 0))
    return Template(b, Hs, tuple(C))


# ---------------------------------------------------------------------------------------------------
# instantiate (brute force reference)
def instantiate(T, g):
    """pair word as an explicit list; g: dict pid -> int"""
    lo = []
    for it in T.Hs:
        if it[0] == 'L':
            lo.extend(it[1])
        else:
            lo.extend(list(it[1]) * g[it[2]])
    up = []
    for it in reversed(T.Hs):
        if it[0] == 'L':
            up.extend(it[1][::-1])
        else:
            up.extend(list(it[1][::-1]) * g[it[2]])
    return lo + list(T.core) + up


def val(b, w):
    x = 0
    for v in reversed(w):
        x = x * b + v
    return x


def digits_of(b, x):
    d = []
    while x:
        d.append(x % b)
        x //= b
    return d


# ---------------------------------------------------------------------------------------------------
# symbolic segments: ('L', data) | ('B', w, pid, mult, off)  copies = mult*g_pid + off
def seg_len(s):
    if s[0] == 'L':
        return Ln(len(s[1]))
    m = len(s[1])
    return Ln(m * s[4], {s[2]: m * s[3]})


def full_segments(T):
    """segments of P (lower, core, upper) with copies = g_pid exactly (mult 1, off 0)"""
    segs = []
    for it in T.Hs:
        segs.append(('L', it[1]) if it[0] == 'L' else ('B', it[1], it[2], 1, 0))
    if T.core:
        segs.append(('L', T.core))
    for it in reversed(T.Hs):
        if it[0] == 'L':
            segs.append(('L', it[1][::-1]))
        else:
            segs.append(('B', it[1][::-1], it[2], 1, 0))
    return segs


def merge_lits(segs):
    out = []
    for s in segs:
        if s[0] == 'L':
            if not s[1]:
                continue
            if out and out[-1][0] == 'L':
                out[-1] = ('L', out[-1][1] + s[1])
                continue
        out.append(s)
    return out


def norm_pass(b, segs):
    """carry-normalise the segment list; returns (O segments, gam)"""
    out = []
    c = 0
    for s in segs:
        if s[0] == 'L':
            d, c = norm(b, s[1], c)
            out.append(('L', d))
        else:
            w = s[1]
            d0, c1 = norm(b, w, c)
            if c1 == c:
                out.append(('B', d0, s[2], s[3], s[4]))
            else:
                d1, c2 = norm(b, w, c1)
                assert c2 == c1, "carry map must be monotone with fixed point"
                out.append(('L', d0))
                out.append(('B', d1, s[2], s[3], s[4] - 1))
            c = c1
    gam = c
    if gam:
        out.append(('L', (1,)))
    out = [reduce_band(s) for s in out]
    return merge_lits(out), gam


def reduce_band(s):
    if s[0] != 'B':
        return s
    u, r = primitive(s[1])
    if r == 1:
        return s
    return ('B', u, s[2], s[3] * r, s[4] * r)


def rev_segs(segs):
    out = []
    for s in reversed(segs):
        if s[0] == 'L':
            out.append(('L', s[1][::-1]))
        else:
            out.append(('B', s[1][::-1], s[2], s[3], s[4]))
    return out


def seg_value(s, off):
    """value at offset (Ln) inside segment"""
    if s[0] == 'L':
        if not off.is_const():
            raise Ambiguous("offset into literal not constant")
        return s[1][off.c]
    m = len(s[1])
    for k, v in off.d.items():
        if v % m:
            raise Unsupported("band phase depends on parameter mod m")
    return s[1][off.c % m]


def lcm(a, b):
    return a * b // gcd(a, b)


def pair_walk(O):
    """elementwise sum of O and rev(O), as pieces.  piece = (start Ln, kind, payload)
    kinds: ('L', data) ; ('B', wsum, pid, mult, off)  [copies = mult*g+off], followed by an 'L' tail piece.
    returns (pieces, total Ln, differs)  differs=True iff O != rev(O) for generic large parameters."""
    A = O
    R = rev_segs(O)
    i = j = 0
    ca = Ln(0)
    cb = Ln(0)
    pos = Ln(0)
    pieces = []
    differs = False
    while i < len(A) and j < len(R):
        sa, sb = A[i], R[j]
        ra = seg_len(sa) - ca
        rb = seg_len(sb) - cb
        d = ra - rb
        sg = d.sign()
        if sg == 0:
            ell = ra
        elif sg < 0:
            ell = ra
        else:
            ell = rb
        # content of the piece
        if ell.is_const():
            n = ell.c
            vals = []
            for k in range(n):
                va = seg_value(sa, ca + Ln(k))
                vb = seg_value(sb, cb + Ln(k))
                vals.append(va + vb)
                if va != vb:
                    differs = True
            pieces.append((pos, ('L', tuple(vals))))
        else:
            if sa[0] != 'B' or sb[0] != 'B':
                raise Unsupported("symbolic piece against literal")
            mA, mB = len(sa[1]), len(sb[1])
            Lc = lcm(mA, mB)
            for k, v in ca.d.items():
                if v % mA:
                    raise Unsupported("phase A")
            for k, v in cb.d.items():
                if v % mB:
                    raise Unsupported("phase B")
            phA = ca.c % mA
            phB = cb.c % mB
            wsum = tuple(sa[1][(phA + k) % mA] + sb[1][(phB + k) % mB] for k in range(Lc))
            for k in range(Lc):
                if sa[1][(phA + k) % mA] != sb[1][(phB + k) % mB]:
                    differs = True
            if len(ell.d) != 1:
                raise Unsupported("piece with several parameters")
            (p, coef), = ell.d.items()
            if coef % Lc:
                raise Unsupported("piece coefficient not multiple of period")
            copies_mult = coef // Lc
            q, r = divmod(ell.c, Lc)
            u, rr = primitive(wsum)
            if rr > 1:
                wsum2 = u
                copies_mult *= rr
                q = q * rr + r // len(u)
                r = r % len(u)
            else:
                wsum2 = wsum
            pieces.append((pos, ('B', wsum2, p, copies_mult, q)))
            if r:
                pieces.append((pos + Ln(len(wsum2) * q, {p: len(wsum2) * copies_mult}), ('L', tuple(wsum2[:r]))))
        pos = pos + ell
        # advance
        if sg == 0:
            i += 1
            j += 1
            ca = Ln(0)
            cb = Ln(0)
        elif sg < 0:
            i += 1
            ca = Ln(0)
            cb = cb + ell
        else:
            j += 1
            cb = Ln(0)
            ca = ca + ell
    if i != len(A) or j != len(R):
        raise Ambiguous("walk did not end together")
    return pieces, pos, differs


def piece_len(pc):
    kind = pc[1]
    if kind[0] == 'L':
        return Ln(len(kind[1]))
    _, w, p, mult, off = kind
    return Ln(len(w) * off, {p: len(w) * mult})


def eval_pos(pieces, q):
    """value of the walk result at symbolic position q (Ln)"""
    for start, kind in pieces:
        ell = piece_len((start, kind))
        if (q - start).sign() >= 0 and (start + ell - q).sign() > 0:
            off = q - start
            if kind[0] == 'L':
                if not off.is_const():
                    continue
                return kind[1][off.c]
            w = kind[1]
            m = len(w)
            for k, v in off.d.items():
                if v % m:
                    raise Unsupported("phase")
            return w[off.c % m]
    raise Ambiguous("position not found")


def halve(pieces, total, b):
    """extract (Hs_raw as segments with (mult,off), core) from palindromic walk result"""
    # half = total/2 : all pid coefficients of total must be even
    for k, v in total.d.items():
        if v % 2:
            raise Unsupported("odd pid coefficient in total")
    half2 = total  # compare 2*end <= total
    lower = []
    a = Ln(0)
    for start, kind in pieces:
        ell = piece_len((start, kind))
        end = start + ell
        # fully lower iff 2*end <= total
        dd = (end + end) - total
        s = dd.sign()
        if s <= 0:
            lower.append((start, kind))
            a = end
        else:
            break
    # drop trailing literal pieces: they belong to the core region
    while lower and lower[-1][1][0] == 'L':
        start, kind = lower.pop()
        a = start
    core_len = total - a - a
    if not core_len.is_const() or core_len.c < 0:
        raise Unsupported(f"core length not constant: {core_len}")
    core = tuple(eval_pos(pieces, a + Ln(k)) for k in range(core_len.c))
    if core != core[::-1]:
        raise Unsupported("core not palindromic (internal error)")
    return [k for (_, k) in lower], core


# ---------------------------------------------------------------------------------------------------
# canonicalisation of (lower items with (mult,off) , core)
def canonicalize(items, core):
    """items: list of ('L',data) | ('B', w, pid, mult, off).  Maximal periodic extension of each band (rotation),
    floor copies, tails into literals, merges.  returns (items, core)."""
    items = merge_lits([reduce_band(s) for s in items])
    core = tuple(core)
    i = 0
    while i < len(items):
        s = items[i]
        if s[0] != 'B':
            i += 1
            continue
        _, w, pid, mult, off = s
        m = len(w)
        left = items[i - 1][1] if (i > 0 and items[i - 1][0] == 'L') else ()
        delta = 0
        while delta < len(left) and left[len(left) - 1 - delta] == w[(m - 1 - delta) % m]:
            delta += 1
        into_core = False
        if i + 1 < len(items):
            right = items[i + 1][1] if items[i + 1][0] == 'L' else ()
            lim = len(right)
        else:
            right = core
            lim = len(core) // 2
            into_core = True
        eps = 0
        while eps < lim and right[eps] == w[eps % m]:
            eps += 1
        tot = delta + eps
        add_c, rem = divmod(tot, m)
        sh = (-delta) % m
        w2 = w[sh:] + w[:sh]
        tail = w2[:rem]
        band = ('B', w2, pid, mult, off + add_c)
        if delta:
            rest = left[:len(left) - delta]
            before = items[:i - 1] + ([('L', rest)] if rest else [])
        else:
            before = items[:i]
        if into_core:
            inner = core[eps:len(core) - eps]
            core = tuple(tail) + tuple(inner) + tuple(tail[::-1])
            after = []
        else:
            if items[i + 1][0] == 'L':
                lit = tuple(tail) + tuple(right[eps:])
                after = ([('L', lit)] if lit else []) + items[i + 2:]
            else:
                after = ([('L', tuple(tail))] if tail else []) + items[i + 1:]
        items = merge_lits(before + [band] + after)
        i = len(merge_lits(before + [band])) 
    return items, core


def step(T):
    """one reverse-and-add step.  returns (T2, gmap, info); gmap: new pid -> (old pid, mult, off) meaning
    g'_new = mult*g_old + off.  info = dict(gam=..., differs=...)"""
    b = T.b
    segs = merge_lits(full_segments(T))
    O, gam = norm_pass(b, segs)
    pieces, total, differs = pair_walk(O)
    lower, core = halve(pieces, total, b)
    items, core = canonicalize(lower, core)
    # relabel pids
    gmap = {}
    Hs = []
    seen = {}
    for s in items:
        if s[0] == 'L':
            Hs.append(s)
        else:
            _, w, pid, mult, off = s
            if pid in seen:
                raise Unsupported("band splits into two bands with the same parameter")
            seen[pid] = len(seen)
            newid = seen[pid]
            gmap[newid] = (pid, mult, off)
            Hs.append(('B', w, newid))
    T2 = Template(b, Hs, core)
    return T2, gmap, dict(gam=gam, differs=differs)
