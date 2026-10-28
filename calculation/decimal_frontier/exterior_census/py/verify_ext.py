#!/usr/bin/env python3
"""Verify an exterior B-cycle witness produced by `bx -w`:
  (1) mirror replay: B_{t+1} = Bstep(B_t) exactly (trimmed lists), e1/gam streams equal e/g, B_p = B_0;
  (2) real-integer replay of each step: N_t = tmpl(B_t, gap, C_t) with a one-coefficient centre C_t in {[18],[0]} chosen so that
      e2 = 1-e1; one true reverse-and-add step; the pair word of N_{t+1} must start with B_{t+1} followed by the (shrunk) neutral band.
usage: verify_ext.py b g [e]      (runs bx -w itself)         or  import verify(b,g,e,Bts)"""
import sys, re, subprocess, os
sys.path.insert(0, '/home/claude/taco-jpg/p196-algorithm/calculation')
import neutral_band_search as m
HERE = os.path.dirname(os.path.abspath(__file__)); BX = os.path.join(os.path.dirname(HERE), 'bin', 'bx')
def Bstep(b, B):
    e1 = m.e1(b, B); e2 = 1 - e1
    DB = m.DB(b, B); R, gm = m.norm(b, B[::-1], e2)
    xd = (b - 1) * (1 - e1)
    nb = m._zw(DB, R[::-1]) if gm == 0 else m._zw(DB + [xd], [1] + R[::-1])
    u = 0
    while nb and nb[-1] == b - 1: nb = nb[:-1]; u += 1
    return nb, e1, gm, u
def to_int(b, digits): return sum(d * b ** i for i, d in enumerate(digits))
def int_digits(b, x):
    d = []
    while x: d.append(x % b); x //= b
    return d
def number_from_pairword(b, P):
    n = len(P); d = [0] * n
    for i in range(n // 2):
        d[i] = P[i] // 2; d[n - 1 - i] = P[i] - P[i] // 2        # low half floor, high half ceil
    if n % 2: assert P[n // 2] % 2 == 0; d[n // 2] = P[n // 2] // 2
    assert all(0 <= x <= b - 1 for x in d) and d[-1] != 0, (P, d)
    return to_int(b, d)
def pairword(b, x):
    d = int_digits(b, x); return [u + v for u, v in zip(d, d[::-1])]
def verify(b, g, e, Bts, gap=8):
    p = len(g); ok = True; msgs = []
    for t in range(p):
        nb, e1, gm, u = Bstep(b, Bts[t])
        if e1 != int(e[t]) or gm != int(g[t]): ok = False; msgs.append(f't={t}: stream mismatch e1={e1} gam={gm}')
        if nb != Bts[(t + 1) % p]: ok = False; msgs.append(f't={t}: B mismatch {nb} vs {Bts[(t+1)%p]}')
    # integer replay
    for t in range(p):
        B = Bts[t]; e1 = m.e1(b, B); C = [18 if b == 10 else 2 * (b - 1)] if e1 == 0 else [0]
        # centre coefficient must be even for odd total length; 2(b-1) is even
        P = B + [b - 1] * gap + C + [b - 1] * gap + B[::-1]
        if len(P) % 2 == 0: ok = False; msgs.append('even length'); break
        x = number_from_pairword(b, P)
        y = x + int(''.join(map(str, int_digits(b, x)[::-1])) and 0) if False else None
        d = int_digits(b, x); rev = to_int(b, d[::-1]); y = x + rev
        Pn = pairword(b, y)
        nb, e1_, gm, u = Bstep(b, B)
        want = nb + [b - 1] * (gap - gm + u)
        # compare lower part and mirror symmetric top
        if Pn[:len(want)] != want or Pn != Pn[::-1]:
            ok = False; msgs.append(f'integer step t={t} mismatch: got {Pn[:len(want)+2]} want {want}')
    return ok, msgs
def run_bx(b, g, extra=()):
    r = subprocess.run([BX, str(b), '-g', g, '-w', '-cap', '20000000'] + list(extra), capture_output=True, text=True)
    return r.stdout
def parse(out):
    res = []; wit = None
    for l in out.splitlines():
        if l.startswith('RES'): res.append(l)
        if l.startswith('WIT'):
            wit = [[int(x) for x in s.split(',')] if s else [] for s in re.findall(r'\[([^\]]*)\]', l.split('B_t=')[1])]
    return res, wit
if __name__ == '__main__':
    b = int(sys.argv[1]); g = sys.argv[2]
    out = run_bx(b, g, ['-first']); res, wit = parse(out)
    print('\n'.join(res))
    es = re.findall(r' e=([01]+)@', ' '.join(res))
    if not wit: print('no witness'); sys.exit(1)
    # witness belongs to the first-found accept; recover its e from the mirror
    e = ''.join(str(m.e1(b, B)) for B in wit)
    ok, msgs = verify(b, g, e, wit)
    print('B_t:', wit[0], '...', 'lengths', sorted(set(len(B) for B in wit)))
    print('witness e =', e, ' VERIFIED' if ok else ' FAILED', *msgs[:5])
