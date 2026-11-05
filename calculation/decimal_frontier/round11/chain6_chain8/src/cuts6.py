#!/usr/bin/env python3
"""r11f chain 6: cut keys + mod-9 charge for every primitive m=8 self-mirror cycle of clock (01)^8 (m8all output).
Same phi/cuts/charge as m2prep.py (round 8), generalised to cycle length n (temporal period P = 16 n).
Charge needs 6 | P; otherwise it is evaluated on the cycle unrolled three times (as round 8 did for P = 32).
usage: cuts6.py m8all_cyc.txt out.json"""
import sys, json
B = 10; M = 8
def phi(row, gam):
    i0 = next((i for i, x in enumerate(row) if x != B - 1), None)
    if i0 is None: return None
    A = [None] * M; D = [None] * M
    A[(i0 + 1) % M] = int(row[i0] >= B)
    for j in range(1, M):
        i = (i0 + j) % M; A[(i + 1) % M] = (row[i] + A[i]) // B
    D[(i0 - 1) % M] = int(row[i0] >= B)
    for j in range(1, M):
        i = (i0 - j) % M; D[(i - 1) % M] = (row[i] + D[i]) // B
    e = [(row[i] + A[i]) % B for i in range(M)]; f = [(row[i] + D[i]) % B for i in range(M)]
    return tuple(e[i] + (f[(i - 1) % M] if gam else f[i]) for i in range(M)), A, D
def cuts(rows, G, k):
    L = []; H = []; Y = []
    for t, row in enumerate(rows):
        _, A, D = phi(row, G[t]); L.append(A[k]); H.append((row[k] + D[k]) // B)
        if G[t]: Y.append((row[(k - 1) % M] + D[(k - 1) % M]) % B)
    return L, H, Y
def charge(S, G, P):
    L, H, Y = S
    lam = [pow(2, -t, 9) for t in range(P)]
    assert all(lam[(t - 1) % P] == (2 * lam[t]) % 9 for t in range(P))
    odd = [t for t in range(P) if G[t]]
    return (sum(lam[t] * (L[t] - H[t]) for t in range(P)) + sum(lam[odd[i]] * Y[i] for i in range(len(odd)))) % 9
def main():
    cyc = []
    for l in open(sys.argv[1]):
        if l.startswith('CYC '):
            p = l.split(); cyc.append((int(p[1]), [tuple(int(x) for x in s.split(',')) for s in p[2:]]))
    out = []; stat = {}
    for ci, (n, mem) in enumerate(cyc):
        P = 16 * n; G = [t % 2 for t in range(P)]
        rows = []; cur = mem[0]
        for t in range(P):
            rows.append(cur); o = phi(cur, G[t]); assert o is not None; cur = o[0]
        assert cur == mem[0], 'period does not close'
        for j in range(n): assert rows[16 * j] == mem[j]
        U = 1 if P % 6 == 0 else 3
        GU = [t % 2 for t in range(P * U)]; rowsU = rows * U
        for k in range(M):
            L, H, Y = cuts(rows, G, k)
            q = charge(cuts(rowsU, GU, k), GU, P * U)
            Lk = sum(b << t for t, b in enumerate(L)); Hk = sum(b << t for t, b in enumerate(H))
            out.append(dict(cycle=ci, n=n, P=P, col=k, L=Lk, H=Hk, Y=Y, charge=q))
            s = stat.setdefault(P, {}); s[q] = s.get(q, 0) + 1
    json.dump(out, open(sys.argv[2], 'w'))
    for P in sorted(stat):
        cyc0 = [c for c in range(len(cyc)) if 16 * cyc[c][0] == P and all(o['charge'] == 0 for o in out if o['cycle'] == c)]
        keys = {(o['L'], o['H'], tuple(o['Y'])) for o in out if o['P'] == P and o['charge'] == 0}
        print('P', P, 'cycles', sum(1 for c in cyc if 16 * c[0] == P), 'charge histogram', dict(sorted(stat[P].items())),
              'cycles all-charge-0', len(cyc0), 'distinct charge-0 cut keys', len(keys))
main()
