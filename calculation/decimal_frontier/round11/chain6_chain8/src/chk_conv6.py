#!/usr/bin/env python3
"""r11f chain 6, premise-(B) convention check, independent of cuts6.py/phi.
For every primitive m=8 cycle of clock (01)^8 in m8all_cyc.txt (all 552, every charge), unroll the full temporal period P=16n.
Carries are solved cyclically from scratch (both start bits tried, exactly one consistent solution required).
Cut x (between spatial cells x-1 and x) := (c_x, delta_x, rho_x) with c_x = forward carry into cell x, delta_x = backward carry out
of cell x (into x-1), rho_x(t) = reverse digit of cell x-1 = (v_{x-1}+delta_x) mod B.  Check that for every x and t the reach edge
rule holds with cell series v_x(t):  c_{x+1} = (v+c_x)//B ; delta_x = (v+delta_{x+1})//B ; rho_{x+1} = (v+delta_{x+1}) % B ;
v_x(t+1) = (v+c_x) % B + (g_t ? rho_x : rho_{x+1}).  Also compares (c,delta,rho at overflow) with cuts6.json (L,H,Y) and the mod-9 charge."""
import sys, json
B = 10; M = 8
def cyc_carry(vals, fwd):
    sols = []
    for a0 in (0, 1):
        a = [0] * M
        if fwd:
            a[0] = a0
            for i in range(M): 
                nxt = (vals[i] + a[i]) // B
                if i + 1 < M: a[i + 1] = nxt
            if nxt == a0: sols.append(a)
        else:   # a[i] = carry INTO cell i from above = out of cell i+1 ; out of cell i = (v_i + a[i])//B
            a[M - 1] = a0
            for i in range(M - 1, -1, -1):
                nxt = (vals[i] + a[i]) // B
                if i - 1 >= 0: a[i - 1] = nxt
            if nxt == a0: sols.append(a)
    return sols
cyc = []
for l in open("m8all_cyc.txt"):
    if l.startswith("CYC "):
        p = l.split(); cyc.append((int(p[1]), [tuple(int(x) for x in s.split(",")) for s in p[2:]]))
cuts = json.load(open("cuts6.json")); cutd = {(o["cycle"], o["col"]): o for o in cuts}
nedge = 0; bad = 0; nonuniq = 0; mism = 0
for ci, (n, mem) in enumerate(cyc):
    P = 16 * n; g = [t % 2 for t in range(P)]
    rows = [mem[0]]; C = []; Dn = []
    for t in range(P):
        v = rows[-1]; A = cyc_carry(v, True); D = cyc_carry(v, False)
        if len(A) != 1 or len(D) != 1: nonuniq += 1
        A = A[0]; D = D[0]   # D[i] = carry into cell i from cell i+1
        # delta_x = carry out of cell x downward = (v_x + D[x])//B ; rho_x = (v_{x-1} + D[x-1]) % B, D[x-1] = delta_x
        e = [(v[i] + A[i]) % B for i in range(M)]; f = [(v[i] + D[i]) % B for i in range(M)]
        new = tuple(e[i] + (f[(i - 1) % M] if g[t] else f[i]) for i in range(M))
        C.append(A); Dn.append(D); rows.append(new)
    assert rows[P] == rows[0], ("no return", ci)
    for j in range(n): assert rows[16 * j] == mem[j]
    def cut(x, t):
        v = rows[t]; c = C[t][x % M]; dl = (v[x % M] + Dn[t][x % M]) // B; rho = (v[(x - 1) % M] + Dn[t][(x - 1) % M]) % B
        return c, dl, rho
    for x in range(M):
        o = cutd[(ci, x)]; Y = []
        for t in range(P):
            c, dl, rho = cut(x, t); c1, dl1, rho1 = cut(x + 1, t); v = rows[t][x]
            ok = (c1 == (v + c) // B and dl == (v + dl1) // B and rho1 == (v + dl1) % B and
                  rows[t + 1][x] == (v + c) % B + (rho if g[t] else rho1))
            nedge += 1; bad += (not ok)
            if ((o["L"] >> t) & 1) != c or ((o["H"] >> t) & 1) != dl: mism += 1
            if g[t]: Y.append(rho)
        if Y != o["Y"]: mism += 1
print("cycles", len(cyc), "cut-to-cut cell checks", nedge, "violations", bad, "non-unique carry solutions", nonuniq, "mismatches vs cuts6.json", mism)
