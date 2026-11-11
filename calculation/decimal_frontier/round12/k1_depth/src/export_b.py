#!/usr/bin/env python3
"""r12g export_b.py -- bulk lattice tables (.tbl, header "P M B") for kink7/kfwd in any base, written from the definitions
(independent of klib's base-10 code, compared with it for base 10).
  cell(t, x) = B[t][x] (x < nB) else W[t][(x-nB) % m]
  UP[t][j] = ascending carry into bulk cell x = nB + 5m + j   (computed from x = 0 on a long row)
  DN[t][j] = descending carry into the mirror of that cell, lattice continued upward (computed from the top of a long row)
Checks: carries periodic in the bulk; the bulk lattice is an exact solution of the local rule P'_x = e_x + r_{x-g}.
usage: export_b.py rec0|rec1|rec2|p12m9|b9r0|b9r1 OUT.tbl [--compare klib.tbl]"""
import sys, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../repo/calculation/decimal_frontier/lattice_kinks/edge_relaxation'))


def load(name):
    if name in ('rec0', 'rec1', 'rec2', 'p12m9'):
        import klib
        L = klib.load(name)
        return 10, L.g, L.B, L.W
    fn = {'b9r0': 'cert_b9_rec0.json', 'b9r1': 'cert_b9_rec1.json'}[name]
    J = json.load(open(os.path.join(HERE, '../ctrl', fn)))
    return J['base'], J['gam'], J['B_t'], J['w_t']


def main():
    name, out = sys.argv[1], sys.argv[2]
    b, g, B, W = load(name)
    p = len(g); nB = len(B[0]); m = len(W[0])
    assert len(B) == p and len(W) == p
    cell = lambda t, x: B[t % p][x] if x < nB else W[t % p][(x - nB) % m]
    Ltot = nB + 60 * m; base = nB + 5 * m; mid = nB + 30 * m
    UP, DN, ROW = [], [], []
    for t in range(p):
        row = [cell(t, x) for x in range(Ltot)]
        up = [0] * Ltot; c = 0
        for x in range(Ltot): up[x] = c; c = (row[x] + c) // b
        dn = [0] * Ltot; d = 0
        for x in range(Ltot - 1, -1, -1): dn[x] = d; d = (row[x] + d) // b
        for j in range(m):   # periodic in the bulk
            assert up[base + j] == up[base + j + m] == up[mid + j], ('up not periodic', t, j)
            assert dn[base + j] == dn[base + j + m] == dn[mid + j], ('dn not periodic', t, j)
        ROW.append([row[base + j] for j in range(m)]); UP.append([up[base + j] for j in range(m)]); DN.append([dn[base + j] for j in range(m)])
    # the bulk lattice is an exact solution: P'_x = e_x + r_{x-g}
    bad = 0
    for t in range(p):
        for j in range(m):
            x = j; xm = (j - g[t]) % m
            e = (ROW[t][x] + UP[t][x]) % b; r = (ROW[t][xm] + DN[t][xm]) % b
            if e + r != ROW[(t + 1) % p][x]: bad += 1
    with open(out, 'w') as f:
        f.write(f'{p} {m} {b}\n' + ' '.join(map(str, g)) + '\n')
        for t in range(p):
            f.write(' '.join(map(str, ROW[t])) + '\n' + ' '.join(map(str, UP[t])) + '\n' + ' '.join(map(str, DN[t])) + '\n')
    print(f'{name}: base {b} p {p} m {m} nB {nB} g {"".join(map(str, g))} bulk-rule mismatches {bad} -> {out}')
    if '--compare' in sys.argv:
        ref = open(sys.argv[sys.argv.index('--compare') + 1]).read().split()
        mine = open(out).read().split()
        # klib tables have header "p m"; ours "p m b"
        print('  identical to', sys.argv[sys.argv.index('--compare') + 1], ':', ref[:2] + ref[2:] == mine[:2] + mine[3:])


if __name__ == '__main__':
    main()
