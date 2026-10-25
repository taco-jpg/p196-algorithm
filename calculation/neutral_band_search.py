#!/usr/bin/env python3
"""Search for neutral one-band return certificates (Agent #120 format) in any base, in particular base 10.

Background. lean/P196/Drafts/Agent120NeutralBandCalibration proves, for EVERY base b >= 2, that a cycle
certificate accepted by `Agent120.Neutral.cycleOK b es B C` gives a base-b Lychrel number
(`lychrel_of_cycle`). The template is the coefficient word (least significant first)

    tmpl b B C g = B ++ (b-1)^g ++ C ++ (b-1)^g ++ reverse B

(two bands of neutral coefficients b-1, i.e. pair sum 9 in base 10). Certificates are known and
kernel-checked in bases 2, 4, 8, 16, 32 (A120PowerTwo) and 11, 17, 26 (Agent213KnownBaseMechanisms).
**No base-10 certificate is known.** One would prove that a decimal Lychrel number exists.

This file is an exact Python mirror of the Lean definitions (norm, e1, e2, DB, DC, DR, gam, xd, yd, nextB,
nextC, Hyp, edgeOK, cycleOK). Between edges the only freedom is how many neutral coefficients are moved
into the band; `step` moves the maximal number (this is without loss of generality, because a neutral
coefficient next to the band behaves exactly like a band coefficient), so from a given (B, C) the
canonical run is deterministic.

Validation (python3 calculation/neutral_band_search.py selftest): the mirror accepts every Lean
certificate in A120PowerTwo (bases 2..32) and Agent213KnownBaseMechanisms (11, 17, 26), the canonical run
reproduces each cycle, and the orbit scan finds the certificate cycle at every step of the real orbits
of the base-11 and base-26 Lychrel seeds.

Usage:
    python3 neutral_band_search.py selftest
    python3 neutral_band_search.py small  <maxLenB> <maxLenC>      # every (B, C), C symmetric, base 10
    python3 neutral_band_search.py orbits <steps> <seed> ...        # scan decimal orbits for templates

Results so far (2026-10-25, base 10): see the "Neutral-band search" paragraph in RESULTS.md.
A cycle printed with gain >= gam is a candidate certificate; check it with `cycleOK 10` in Lean
(`decide`) before claiming anything.
"""
import itertools, collections, re, sys, os


# ---- exact mirror of A120Base / A120Template / A120Certificate ----
def norm(b, w, c):
    out = []
    for v in w:
        out.append((v + c) % b); c = (v + c) // b
    return out, c
def e1(b, B): return norm(b, B, 0)[1]
def e2(b, B, C): return norm(b, C, e1(b, B))[1]
def DB(b, B): return norm(b, B, 0)[0]
def DC(b, B, C): return norm(b, C, e1(b, B))[0]
def DR(b, B, C): return norm(b, B[::-1], e2(b, B, C))[0]
def gam(b, B, C): return norm(b, B[::-1], e2(b, B, C))[1]
def xd(b, B): return (b - 1) * (1 - e1(b, B))
def yd(b, B, C): return (b - 1) * (1 - e2(b, B, C))
def _zw(x, y): return [p + q for p, q in zip(x, y)]
def nextB(b, B, C):
    if gam(b, B, C) == 0: return _zw(DB(b, B), DR(b, B, C)[::-1])
    return _zw(DB(b, B) + [xd(b, B)], [1] + DR(b, B, C)[::-1])
def nextC(b, B, C):
    d = DC(b, B, C)
    if gam(b, B, C) == 0: return _zw(d, d[::-1])
    y = yd(b, B, C); return _zw(d + [y], [y] + d[::-1])
def hyp(b, B, C):
    return (b >= 2 and all(v <= 2 * (b - 1) for v in B) and all(v <= 2 * (b - 1) for v in C)
            and (not B or B[0] != 0) and e1(b, B) != e2(b, B, C))
def edgeOK(b, E):
    B, C, B2, C2, u, v = E
    return hyp(b, B, C) and nextB(b, B, C) == B2 + [b - 1] * u and nextC(b, B, C) == [b - 1] * v + C2 + [b - 1] * v
def cycleOK(b, es, B, C):
    if not es: return False
    cb, cc = B, C
    for E in es:
        if (E[0], E[1]) != (cb, cc) or not edgeOK(b, E): return False
        cb, cc = E[2], E[3]
    return (cb, cc) == (B, C) and sum(gam(b, E[0], E[1]) for E in es) <= sum(E[4] + E[5] for E in es)


# ---- canonical deterministic run ----
def trim(b, B2, C2):
    u = 0
    while B2 and B2[-1] == b - 1: B2 = B2[:-1]; u += 1
    v = 0
    while len(C2) >= 2 and C2[0] == b - 1 and C2[-1] == b - 1: C2 = C2[1:-1]; v += 1
    return B2, C2, u, v
def step(b, B, C):
    if not hyp(b, B, C): return None
    B2, C2, u, v = trim(b, nextB(b, B, C), nextC(b, B, C))
    return (B, C, B2, C2, u, v)
def run(b, B, C, maxsteps=2000, maxlen=400):
    """('cycle', edges) | ('break', t) | ('grow', t) | ('long', maxsteps)"""
    seen, es, cur = {}, [], (tuple(B), tuple(C))
    for t in range(maxsteps):
        if cur in seen: return ('cycle', es[seen[cur]:])
        seen[cur] = t
        E = step(b, list(cur[0]), list(cur[1]))
        if E is None: return ('break', t)
        es.append(E); cur = (tuple(E[2]), tuple(E[3]))
        if len(cur[0]) + len(cur[1]) > maxlen: return ('grow', t)
    return ('long', maxsteps)
def is_cert(b, es):
    return sum(e[4] + e[5] for e in es) >= sum(gam(b, e[0], e[1]) for e in es)


# ---- templates inside real orbits ----
def digits(b, x):
    d = []
    while x: d.append(x % b); x //= b
    return d
def template_of(b, x, ming=2):
    """the (B, C, g) decomposition of the pair word of x with the longest outer neutral band"""
    d = digits(b, x); P = _zw(d, d[::-1]); n = len(P); i = 0; best = None
    while i < n // 2:
        if P[i] == b - 1:
            j = i
            while j < n and P[j] == b - 1: j += 1
            g = min(j - i, (n - 2 * i) // 2)
            if g >= ming and i > 0 and (best is None or g > best[2]): best = (P[:i], P[i + g:n - i - g], g)
            i = j
        else: i += 1
    return best
def rev_add(b, x):
    d = digits(b, x); return x + sum(v * b ** k for k, v in enumerate(d[::-1]))


def _lean_certs():
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lean", "P196")
    out = []
    L = lambda s: [int(x) for x in s.split(",")] if s.strip() else []
    src = open(os.path.join(root, "Drafts", "Agent120NeutralBandCalibration", "A120PowerTwo.lean")).read()
    for m in re.finditer(r"def cert(\d+) : List Edge :=\s*(\[.*?\])\n\n", src, re.S):
        es = [(L(e[1]), L(e[2]), L(e[3]), L(e[4]), int(e[5]), int(e[6])) for e in
              re.finditer(r"⟨\[([^\]]*)\], \[([^\]]*)\], \[([^\]]*)\], \[([^\]]*)\], (\d+), (\d+)⟩", m[2])]
        out.append((int(m[1]), es))
    src = open(os.path.join(root, "Agent213KnownBaseMechanisms", "KnownBases.lean")).read()
    defs = {m[1]: L(m[2]) for m in re.finditer(r"def (\w+)\s*:\s*List Nat\s*:=\s*\[([^\]]*)\]", src)}
    for m in re.finditer(r"def cert(\d+)\s*:\s*List Edge\s*:=\s*(\[.*?\])\n\n", src, re.S):
        es = [(defs[e[1]], defs[e[2]], defs[e[3]], defs[e[4]], int(e[5]), int(e[6])) for e in
              re.finditer(r"⟨(\w+), (\w+), (\w+), (\w+), (\d+), (\d+)⟩", m[2])]
        out.append((int(m[1]), es))
    return out


def selftest():
    ok = True
    for b, es in _lean_certs():
        r = run(b, es[0][0], es[0][1])
        good = cycleOK(b, es, es[0][0], es[0][1]) and r[0] == 'cycle' and len(r[1]) == len(es) and is_cert(b, r[1])
        print(f"base {b}: {len(es)} edges, cycleOK {cycleOK(b, es, es[0][0], es[0][1])}, canonical run {r[0]}")
        ok &= good
        if b in (11, 26):
            x = sum(v * b ** k for k, v in enumerate(es[0][0] + [b - 1] * 6 + es[0][1] + [b - 1] * 6 + es[0][0][::-1]))
            for t in range(8):
                B, C, g = template_of(b, x); rr = run(b, B, C); ok &= rr[0] == 'cycle' and is_cert(b, rr[1])
                x = rev_add(b, x)
            print(f"  orbit scan of the base-{b} seed finds the certificate at 8 consecutive steps")
    print("SELFTEST", "PASSED" if ok else "FAILED"); return ok


def small(LB, LC, b=10):
    res, cycles, longest = collections.Counter(), [], (0, None)
    def sym(L):
        for half in itertools.product(range(2 * b - 1), repeat=(L + 1) // 2):
            yield list(half) + list(half[:L // 2][::-1])
    for lb in range(1, LB + 1):
        for B in itertools.product(range(2 * b - 1), repeat=lb):
            if B[0] == 0: continue
            for lc in range(LC + 1):
                for C in sym(lc):
                    r = run(b, list(B), C, maxsteps=400, maxlen=80); res[r[0]] += 1
                    if r[0] == 'cycle': cycles.append((B, tuple(C), r[1]))
                    elif r[0] == 'break' and r[1] > longest[0]: longest = (r[1], (B, tuple(C)))
    print(f"base {b}, |B| <= {LB}, symmetric |C| <= {LC}: {dict(res)}; longest run before break {longest}")
    for B, C, es in cycles:
        print("CYCLE", B, C, len(es), "edges", "CERTIFICATE CANDIDATE" if is_cert(b, es) else "(gain < overflows)")


def orbits(steps, seeds, b=10):
    for s in seeds:
        x, out, best, cyc = s, collections.Counter(), 0, 0
        for t in range(steps):
            tp = template_of(b, x)
            if tp:
                r = run(b, tp[0], tp[1], maxsteps=3000, maxlen=400); out[r[0]] += 1
                if r[0] == 'break': best = max(best, r[1])
                if r[0] == 'cycle':
                    cyc += 1; print("CYCLE seed", s, "t", t, "CERTIFICATE CANDIDATE" if is_cert(b, r[1]) else "")
            x = rev_add(b, x)
        print(f"seed {s}: {sum(out.values())} template occurrences {dict(out)}, longest run before break {best}, cycles {cyc}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "selftest": sys.exit(0 if selftest() else 1)
    if a[0] == "small": small(int(a[1]), int(a[2]))
    if a[0] == "orbits": orbits(int(a[1]), [int(s) for s in a[2:]])
