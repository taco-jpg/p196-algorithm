#!/usr/bin/env python3
"""hyb.py -- exact step function for the HYBRID format (W6).

Pair word (LSB first, entries in 0..2b-2), N = b-1:
    P = B ++ N^g ++ C ++ c^h ++ rev(C) ++ N^g ++ rev(B)           (palindromic)
c is an ABSORBING core value: c != N, c <= 2b-2, carry-out of c^h is the constant k=[c>=b] for every carry-in.
Carry flow: B (carry-in 0) -> e1; N^g passes e1; C (carry-in e1) -> e2; core absorbs -> k=[c>=b];
rev C (carry-in k) -> e3; N^g passes e3; rev B (carry-in e3) -> gam.  Neutral bands reproduce iff e1+e3 == 1.
"""
import sys, random

def norm(b, w, c):
    out = []
    for v in w:
        t = v + c
        out.append(t % b)
        c = t // b
    return out, c

def kcar(b, c):
    return 1 if c >= b else 0

def hstep_raw(b, B, C, c):
    """Exact one step on finite data.  Returns dict, or None when the flip e1+e3==1 fails.
    Pre-trim next state: B' (len |B|+gam), C' (len |C|+1), core value c'=2y, with
       g' = g - gam,  h' = h - 2 + gam   (before trims)."""
    N = b - 1
    DB, e1 = norm(b, B, 0)
    x = (N + e1) % b
    DC, e2 = norm(b, C, e1)
    k = kcar(b, c)
    z = (c + e2) % b
    y = (c + k) % b
    DRC, e3 = norm(b, C[::-1], k)
    w = (N + e3) % b
    DR, gam = norm(b, B[::-1], e3)
    if e1 + e3 != 1:
        return None
    if gam == 0:
        Bp = [p + q for p, q in zip(DB, DR[::-1])]
        Cp = [p + q for p, q in zip(DC, DRC[::-1])] + [z + y]
    else:
        Bp = [p + q for p, q in zip(DB + [x], [1] + DR[::-1])]
        Cp = [p + q for p, q in zip(DC + [z], [w] + DRC[::-1])]
    return dict(B=Bp, C=Cp, c=2 * y, gam=gam, e1=e1, e2=e2, e3=e3, k=k, x=x, w=w, y=y, z=z,
                DB=DB, DC=DC, DRC=DRC, DR=DR)

def trim(b, Bp, Cp, cp):
    """canonical trims: u = N's at top of B'; v = N's at bottom of C'; p = cp's at top of C'."""
    N = b - 1
    u = 0
    while Bp and Bp[-1] == N:
        Bp = Bp[:-1]; u += 1
    v = 0
    while Cp and Cp[0] == N:
        Cp = Cp[1:]; v += 1
    p = 0
    while Cp and Cp[-1] == cp:
        Cp = Cp[:-1]; p += 1
    return Bp, Cp, u, v, p

def hstep(b, B, C, c):
    """canonical step: (B2, C2, c2, gam, u, v, p, info) or None.
    g2 = g - gam + u + v ;  h2 = h - 2 + gam + 2p."""
    r = hstep_raw(b, B, C, c)
    if r is None:
        return None
    B2, C2, u, v, p = trim(b, r['B'], r['C'], r['c'])
    return B2, C2, r['c'], r['gam'], u, v, p, r

# ------------------------------------------------------------------------------------------------
# plain big-int reverse-and-add
def val(b, P):
    n = 0
    for v in reversed(P):
        n = n * b + v
    return n
def digits(b, n):
    d = []
    while n:
        d.append(n % b); n //= b
    return d
def pairs(d):
    return [p + q for p, q in zip(d, d[::-1])]
def rar(b, n):
    d = digits(b, n)
    return n + val(b, d[::-1])
def tmpl(b, B, C, c, g, h):
    N = b - 1
    return list(B) + [N] * g + list(C) + [c] * h + list(C)[::-1] + [N] * g + list(B)[::-1]

def predicted(b, B, C, c, g, h):
    """predicted next pair word (via hstep_raw, pre-trim) for given g,h; None if flip fails"""
    r = hstep_raw(b, B, C, c)
    if r is None:
        return None
    N = b - 1
    gam = r['gam']
    g2 = g - gam
    h2 = h - 2 + gam
    return tmpl(b, r['B'], r['C'], r['c'], g2, h2), (g2, h2)

def validate(b, trials, seed=1, maxg=14, maxh=14, maxB=8, maxC=8, verbose=False):
    rng = random.Random(seed)
    N = b - 1
    cs = [v for v in range(2 * b - 1) if v != N]
    nok = nflip = 0
    for _ in range(trials):
        lb = rng.randint(1, maxB); lc = rng.randint(0, maxC)
        B = [rng.randint(1, 2 * N)] + [rng.randint(0, 2 * N) for _ in range(lb - 1)]
        C = [rng.randint(0, 2 * N) for _ in range(lc)]
        c = rng.choice(cs)
        g = rng.randint(3, maxg); h = rng.randint(3, maxh)
        P = tmpl(b, B, C, c, g, h)
        pred = predicted(b, B, C, c, g, h)
        n = val(b, P)
        d = digits(b, n)
        act = pairs(d)
        if pred is None:
            nflip += 1
            continue
        if act != pred[0]:
            print("MISMATCH", b, B, C, c, g, h)
            print(" act ", act); print(" pred", pred[0])
            return False
        # non-palindrome witness
        if d == d[::-1]:
            print("PALINDROME", b, B, C, c, g, h); return False
        nok += 1
    print(f"base {b}: {nok} flip-ok instances matched exactly ({nflip} flip-fail skipped)")
    return True

if __name__ == '__main__':
    ok = True
    for b in (10, 13, 11, 7, 3):
        ok &= validate(b, 6000 if b == 10 else 2500, seed=b)
    print("VALIDATION", "PASSED" if ok else "FAILED")
