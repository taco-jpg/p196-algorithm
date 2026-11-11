#!/usr/bin/env python3
"""classes2.py (r14a): symmetry classes of lattice words with phase-orbit classes.
Input: list of lat files. Group: time rotation R (t->t+2), complement C, cyclic rotation S (x->x+1).
Output class/classes.json + class/classes.txt.  For each class: representative file, L, T, stabiliser elements (r,c,sigma),
phase orbits and their classes under the stabiliser symmetries Phi(t,j,par,w) = (t+tau, j+sigma, par, C^c w), tau = 2r, sigma = shift with
C^c W(t,x) = W(t+tau, x+sigma)."""
import sys, os, json, glob, collections
def read_lat(fn):
    with open(fn) as f:
        toks = f.read().split()
    base, tp, nB, m = map(int, toks[:4]); p = 4
    clk = [int(x) for x in toks[p:p+tp]]; p += tp
    B = []
    for t in range(tp):
        B.append([int(x) for x in toks[p:p+nB]]); p += nB
    W = []
    for t in range(tp):
        W.append([int(x) for x in toks[p:p+m]]); p += m
    assert p == len(toks), fn
    return base, tp, nB, m, clk, B, W
def cols(W, m): return tuple(tuple(W[t][x] for t in range(8)) for x in range(m))
def tw(word, r, c):
    out = []
    for col in word:
        v = tuple(col[(t + 2 * r) % 8] for t in range(8))
        if c: v = tuple(18 - x for x in v)
        out.append(v)
    return tuple(out)
def canon(w):
    n = len(w)
    return min(w[i:] + w[:i] for i in range(n))
def orbits(m, clk):
    # phase orbits of nu on (t,j,par); identical to mc13c all_orbits labelling
    tot = 8 * m * 2
    seen = [False] * tot
    orb = {}
    out = []
    for cid in range(tot):
        if seen[cid]: continue
        o = []
        cur = cid
        while not seen[cur]:
            seen[cur] = True
            par = cur & 1; rest = cur >> 1; t = rest // m; j = rest % m
            o.append((t, j, par))
            gg = clk[t]; dh = 1 if gg == 1 and par == 0 else 0
            t2 = (t + 1) % 8; j2 = (j + dh) % m; p2 = (par + gg) % 2
            cur = ((t2 * m + j2) * 2) + p2
        for ph in o: orb[ph] = len(out)
        out.append(o)
    return out, orb
if __name__ == '__main__':
    files = sys.argv[1:]
    classes = {}
    for fn in files:
        base, tp, nB, m, clk, B, W = read_lat(fn)
        assert base == 10 and tp == 8 and clk == [1,0,1,0,1,0,1,0], fn
        w = cols(W, m)
        can = min(canon(tw(w, r, c)) for r in range(4) for c in range(2))
        classes.setdefault(can, []).append(fn)
    cl = sorted(classes.items(), key=lambda kv: ((4 if len(kv[0]) % 2 == 0 else 8) * len(kv[0]), len(kv[0]), kv[0]))
    table = []
    for i, (can, mem) in enumerate(cl):
        L = len(can); T = (4 * L if L % 2 == 0 else 8 * L)
        rep = mem[0]
        base, tp, nB, m, clk, B, W = read_lat(rep)
        w = cols(W, m)
        # stabiliser elements with their spatial shift: C^c W(t,x) = W(t+2r, x+sigma)
        st = []
        for r in range(4):
            for c in range(2):
                wv = tw(w, r, c)
                # find sigma with wv(x) == w(x + sigma)   [tw gives col x -> C^c col(t+2r)]; we need C^c W(t,x) = W(t+2r, x+sigma), i.e. the word u(x) := C^c W(.,x) at time t equals W(t+2r,x+sigma)
                for sigma in range(m):
                    ok = True
                    for x in range(m):
                        for t in range(8):
                            a = W[t][x] if c == 0 else 18 - W[t][x]
                            if a != W[(t + 2 * r) % 8][(x + sigma) % m]:
                                ok = False; break
                        if not ok: break
                    if ok:
                        st.append((r, c, sigma))
        orbs, orb_of = orbits(m, clk)
        # union-find on the orbits
        parent = list(range(len(orbs)))
        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]; a = parent[a]
            return a
        for (r, c, sigma) in st:
            tau = 2 * r
            for k, o in enumerate(orbs):
                t, j, par = o[0]
                im = ((t + tau) % 8, (j + sigma) % m, par)
                k2 = orb_of[im]
                a, b = find(k), find(k2)
                if a != b: parent[a] = b
        ocl = collections.defaultdict(list)
        for k in range(len(orbs)): ocl[find(k)].append(k)
        table.append({'id': i, 'L': L, 'T': T, 'rep': rep, 'n_files': len(mem), 'stab': st, 'n_orbits': len(orbs), 'orbit_classes': sorted(sorted(v) for v in ocl.values()), 'members': mem})
    json.dump(table, open('class/classes.json', 'w'))
    with open('class/classes.txt', 'w') as f:
        f.write('# classes %d, total files %d\n' % (len(table), len(files)))
        for rec in table:
            f.write('class %3d L=%3d T=%4d files=%2d rep=%s stab=%s orbit_classes=%s\n' % (rec['id'], rec['L'], rec['T'], rec['n_files'], os.path.basename(rec['rep']), rec['stab'], rec['orbit_classes']))
