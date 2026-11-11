#!/usr/bin/env python3
"""famexport.py (r14a): export a family (set of edges of the clock-10, d=8 interface graph) for mc14f2.
usage: famexport.py OUT all | OUT cycle LATFILE ... | OUT subfamily-tag
Format: "nE", then per edge: I J tag v[8] c[8] xb[8] A[8].
tag = 1 for an edge on one of the four 48-cycles (rec2 lattice), else 0.
Also verifies (for mode cycle) that lattice tables derived from the word equal the interface data."""
import sys, os, collections
sys.path.insert(0, os.path.expanduser('~/p196_run/mchk14'))
import ifscc

out = sys.argv[1]
mode = sys.argv[2]
g = [1, 0] * 4
d = 8
states, adj, level = ifscc.build(g, d)
n = len(states)
succ = [sorted(set(a.values())) for a in adj]
comps = [c for c in ifscc.tarjan(n, succ) if len(c) > 1 or c[0] in succ[c[0]]]
comps.sort(key=len, reverse=True)
comp = comps[0]
cs = set(comp)
edges = {v: [(col, w) for col, w in adj[v].items() if w in cs] for v in comp}

# 48-cycles: the shortest cycles; find them by DFS of length exactly 48 in the SCC
def find_cycles48():
    found = []
    for s0 in sorted(comp):
        stack = [(s0, [])]
        # DFS without repeated nodes, bounded length 48
        path = []
        seen = {s0}
        res = []
        def dfs(v, L):
            for col, w in edges[v]:
                if w == s0 and L + 1 == 48:
                    res.append(list(path) + [(v, col, w)])
                elif w not in seen and L + 1 < 48 and w > s0:
                    seen.add(w)
                    path.append((v, col, w))
                    dfs(w, L + 1)
                    path.pop()
                    seen.discard(w)
        dfs(s0, 0)
        for r in res:
            found.append(r)
    return found

cyc48 = find_cycles48()
edges48 = set()
for r in cyc48:
    for (v, col, w) in r:
        edges48.add((v, col))
print('48-cycles found', len(cyc48), 'edges on them', len(edges48))

def write_family(edge_list, fn):
    # edge_list: list of (I, col, J); per edge also Rinv and Comp image edge indices (-1 if absent)
    index = {(I, col): k for k, (I, col, J) in enumerate(edge_list)}
    ids = {s: i for i, s in enumerate(states)}
    def R_inv_state(st):
        c, xb, A, root = st
        return (tuple(c[(t + 6) % 8] for t in range(8)), tuple(xb[(t + 6) % 8] for t in range(8)), tuple(A[(t + 6) % 8] for t in range(8)), root)
    def C_state(st):
        c, xb, A, root = st
        swap = lambda a: ((a & 1) << 1) | ((a >> 1) & 1)
        return (tuple(1 - x for x in c), tuple(18 - xb[t] if g[t] else 0 for t in range(8)), tuple(swap(a) for a in A), root)
    def Rinv_col(col): return tuple(col[(t + 6) % 8] for t in range(8))
    def C_col(col): return tuple(18 - x for x in col)
    with open(fn, 'w') as f:
        f.write(f'{len(edge_list)}\n')
        for (I, col, J) in edge_list:
            c, xb, A, root = states[I]
            assert not root
            tag = 1 if (I, col) in edges48 else 0
            sv = states[I]
            ri = ids.get(R_inv_state(sv))
            ci = ids.get(C_state(sv))
            rimg = index.get((ri, Rinv_col(col)), -1) if ri is not None else -1
            cimg = index.get((ci, C_col(col)), -1) if ci is not None else -1
            vals = [I, J, tag, rimg, cimg] + list(col) + list(c) + [x if x >= 0 else 0 for x in xb] + list(A)
            f.write(' '.join(map(str, vals)) + '\n')
    print('wrote', fn, 'edges', len(edge_list))

if mode == 'all':
    el = []
    for v in sorted(comp):
        for col, w in sorted(edges[v]):
            el.append((v, col, w))
    write_family(el, out)
elif mode == 'cycle':
    sys.path.insert(0, 'src')
    from classes2 import read_lat
    fams = []
    for fn in sys.argv[3:]:
        base, tp, nB, m, clk, B, W = read_lat(fn)
        word = [tuple(W[t][x] for t in range(8)) for x in range(m)]
        # find a node s0 of the SCC such that the word is readable as a closed walk (possibly from a rotation)
        found = None
        for rot in range(m):
            w2 = word[rot:] + word[:rot]
            for s0 in comp:
                v = s0; ok = True; path = []
                for col in w2:
                    nxt = None
                    for c2, w3 in edges[v]:
                        if c2 == col:
                            nxt = w3; break
                    if nxt is None:
                        ok = False; break
                    path.append((v, col, nxt)); v = nxt
                if ok and v == s0:
                    found = (rot, path); break
            if found: break
        if not found:
            print('no closed walk for', fn); sys.exit(1)
        rot, path = found
        # verification of the interface data against lattice tables computed from the word itself
        wd = word[rot:] + word[:rot]
        Lw = len(wd)
        # compute UP, DN like mc13c prep
        W2 = [[wd[x][t] for x in range(Lw)] for t in range(8)]
        def tables():
            UP = [[0] * Lw for _ in range(8)]; DN = [[0] * Lw for _ in range(8)]
            for t in range(8):
                res = [0, 0]
                for st in (0, 1):
                    a = st
                    for x in range(4 * Lw):
                        a = 1 if W2[t][x % Lw] + a >= 10 else 0
                    res[st] = a
                assert res[0] == res[1], 'UP not unique'
                a = res[0]
                for x in range(Lw):
                    UP[t][x] = a
                    a = 1 if W2[t][x] + a >= 10 else 0
                for st in (0, 1):
                    b = st
                    for i in range(4 * Lw):
                        x = Lw - 1 - (i % Lw)
                        b = 1 if W2[t][x] + b >= 10 else 0
                    res[st] = b
                assert res[0] == res[1], 'DN not unique'
                b = res[0]
                for x in range(Lw - 1, -1, -1):
                    DN[t][x] = b
                    b = 1 if W2[t][x] + b >= 10 else 0
            return UP, DN
        UP, DN = tables()
        EE = [[(W2[t][x] + UP[t][x]) % 10 for x in range(Lw)] for t in range(8)]
        bad = 0
        for j, (I, col, J) in enumerate(path):
            c, xb, A, root = states[I]
            for t in range(8):
                # forward carry into column j at time t
                if c[t] != UP[t][j]:
                    bad += 1
                # xb(t) when g_t = 1 is the previous column's value
                if g[t] == 1 and xb[t] != W2[t][(j - 1) % Lw]:
                    bad += 1
                # A(t) vs lattice BOK: admissible carries leaving column j into the column below:
                # BOK from the word (LIM = 3*Lw like mc13c prep)
                allowed = 0
                for bb in (0, 1):
                    # r digits below: rr[l] for column j-l, starting with carry bb into column j-1
                    gg = g[t]; tn = (t + 1) % 8
                    b = bb; rr = {}
                    LIM = 3 * Lw + 2
                    for l in range(1, LIM + 3):
                        cc = (j - l) % Lw
                        s = W2[t][cc] + b
                        rr[l] = s % 10
                        b = 1 if s >= 10 else 0
                    ok = True
                    for l in range(1, LIM + 1):
                        cy = (j - l) % Lw
                        val = EE[t][cy] + rr[l + 1 if gg else l]
                        if val != W2[tn][cy]:
                            ok = False; break
                    if ok: allowed |= (1 << bb)
                if (A[t] & 3) != allowed:
                    bad += 1
        print(f'{os.path.basename(fn)}: L={m} rotation {rot}: interface vs lattice table mismatches: {bad}')
        fams.append(path)
    el = []
    seen = set()
    for path in fams:
        for (I, col, J) in path:
            if (I, col) not in seen:
                seen.add((I, col))
                el.append((I, col, J))
    write_family(el, out)
else:
    print('bad mode'); sys.exit(2)
