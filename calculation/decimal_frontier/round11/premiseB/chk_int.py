# Integer-level step checks (genuine reverse-and-add on Python integers).
# WIRE: pair word E 9^m C 9^m rev(E), one-coefficient centre C realising e2 = 1-e1.  Claim: the reach one-step WIRE-accepting
#       branches of column E are exactly {(g, P'[0..H-1])} if P'[H] = b-1, else none; g = the true overflow bit.
# BAND: pair word E u^m rev(E), u a uniform-band value.  Claims: (i) reach strict band acceptance at height H with next column E''
#       implies the true next pair word is E'' f(u)^(m+g) rev(E'') ; (ii) if the true next pair word has that form (template step),
#       then strict acceptance holds at height H, or at height H+1 with column E+u (one band cell absorbed into the left end).
import sys, itertools, collections
from rmodel import *
def val(b, P): return sum(p * b ** i for i, p in enumerate(P))
def digs(b, x):
    d = []
    while x: d.append(x % b); x //= b
    return d
def pw(b, x): d = digs(b, x); return [u + v for u, v in zip(d, d[::-1])]
def fband(b, v): c = 1 if v >= b else 0; return 2 * ((v + c) % b)
def band_values(b):
    vals = set()
    for v0 in range(2 * b - 1):
        v = v0
        for _ in range(4 * b): v = fband(b, v)
        u = v; cyc = []
        while True:
            cyc.append(u); u = fband(b, u)
            if u == v: break
        if b - 1 not in cyc: vals |= set(cyc)
    return sorted(vals)
def wire(b, H, ms=(2, 3, 4)):
    n = bad = acc = 0
    for E in itertools.product(range(2 * b - 1), repeat=H):
        if E[0] == 0: continue
        e1 = phi(b, trim(b, E))[1]; C = [2 * b - 2] if e1 == 0 else [0]
        for mm in ms:
            P = list(E) + [b - 1] * mm + C + [b - 1] * mm + list(E[::-1])
            x = val(b, P); y = x  # N + rev N = val(P) for any digit split
            Pn = pw(b, x); g = 1 if len(Pn) > len(P) else 0
            got = {(gg, vn) for gg in (0, 1) for vn, c, d, r in reach_step(b, E, gg) if wire_ok(b, gg, c, d, r)}
            want = {(g, tuple(Pn[:H]))} if Pn[H] == b - 1 else set()
            n += 1; acc += len(want)
            if got != want: bad += 1; print('WIRE MISMATCH', b, E, mm, got, want) if bad < 10 else None
    print(f'WIRE base {b} H={H}: {n} pair words, {acc} with the 9-wire kept, mismatches {bad}'); return bad
def band(b, H, ms=(3, 4, 5, 6)):
    st = collections.Counter(); bad = 0
    U = band_values(b)
    for E in itertools.product(range(2 * b - 1), repeat=H):
        if E[0] == 0: continue
        for u in U:
            BC = 1 if u >= b else 0; BR = (u + BC) % b; u2 = fband(b, u)
            for mm in ms:
                if mm % 2 and u % 2: continue
                P = list(E) + [u] * mm + list(E[::-1]); Pn = pw(b, val(b, P)); n2 = len(Pn); g = 1 if n2 > len(P) else 0
                tmpl = n2 - 2 * H >= 1 and all(p == u2 for p in Pn[H:n2 - H])
                En = tuple(Pn[:H])
                SH = {vn for vn, c, d, r in reach_step(b, E, g) if band_ok(b, g, c, d, r, BC, BR)}
                SH1 = {vn for vn, c, d, r in reach_step(b, E + (u,), g) if band_ok(b, g, c, d, r, BC, BR)}
                # (i) soundness of strict acceptance
                for vn in SH:
                    if not (tmpl and vn == En): bad += 1; print('BAND (i) FAIL', b, E, u, mm, vn, Pn)
                tmpl1 = n2 - 2 * H - 2 >= 1 and all(p == u2 for p in Pn[H + 1:n2 - H - 1])
                for vn in SH1:
                    if not (tmpl1 and vn == tuple(Pn[:H + 1])): bad += 1; print('BAND (i,H+1) FAIL', b, E, u, mm, vn, Pn)
                if tmpl:
                    if tuple(Pn[:H + 1]) not in SH1: bad += 1; print('BAND (ii,H+1) FAIL', b, E, u, mm, Pn)
                    if En not in SH and not g: bad += 1; print('BAND relaxed case without overflow', b, E, u, mm, Pn)
                    if En in SH: st['template, strict at H'] += 1
                    elif En + (u2,) in SH1: st['template, strict only at H+1 (overflow, c_H != BC)'] += 1; ex = (E, u, mm, Pn)
                    else: bad += 1; print('BAND (ii) FAIL', b, E, u, mm, Pn)
                else: st['no template step'] += 1
    print(f'BAND base {b} H={H} values {U}: {dict(st)}, failures {bad}')
    if st['template, strict only at H+1 (overflow, c_H != BC)']: print('   example of the relaxed case:', ex)
    return bad
if __name__ == '__main__':
    t = 0
    for b, H in [(3, 4), (4, 4), (10, 2), (10, 3), (13, 2)]: t += wire(b, H)
    for b, H in [(4, 4), (10, 2), (10, 3), (13, 2)]: t += band(b, H)
    print('TOTAL FAILURES', t)
