#!/usr/bin/env python3
"""Independent chain for the budget-frame closure, plain Python.  Rule written with explicit carries; everything below the
window is evaluated down to column 0 with the true boundary (no periodic carry tables), the closure is its own iterative
Tarjan on arrays.  Usage: pybudget.py LATFILE B KMAX [zero]"""
import sys, time
from array import array
fn, Bud, kmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
ZERO = len(sys.argv) > 4 and sys.argv[4] == 'zero'
tk = open(fn).read().split()
BASE, tp, nB, m = map(int, tk[:4])
clk = list(map(int, tk[4:4 + tp]))
v_ = list(map(int, tk[4 + tp:]))
Bt = [v_[t * nB:(t + 1) * nB] for t in range(tp)]
v_ = v_[tp * nB:]
W = [v_[t * m:(t + 1) * m] for t in range(tp)]
BS = 2 * BASE - 1
QQ = 6
L = lambda t, x: Bt[t][x] if x < nB else W[t][(x - nB) % m]

# what the lattice below the window does: ascending carry into the window; for each descending carry bb entering column c-1
LOW = {}
for t in range(tp):
    g = clk[t]
    tn = (t + 1) % tp
    for j in range(m):
        c = nB + j + QQ * m
        a = 0
        e = [0] * c
        for x in range(c):
            s = L(t, x) + a
            e[x] = s % BASE
            a = 1 if s >= BASE else 0
        res = {}
        for bb in (0, 1):
            cur = bb
            r = [0] * c
            for x in range(c - 1, -1, -1):
                s = L(t, x) + cur
                r[x] = s % BASE
                cur = 1 if s >= BASE else 0
            ok = (cur == g)
            for y in range(c):
                rr = r[y - g] if y - g >= 0 else 1
                if e[y] + rr != L(tn, y):
                    ok = False
                    break
            res[bb] = (ok, r[c - 1])
        LOW[(t, j)] = (a, res)

# new top cell at a shift during an overflow-free step, as a function of (ascending carry into new cell, descending carry out of it)
T0 = {}
for a in (0, 1):
    for din in (0, 1):
        vals = set()
        for p in range(BS):
            for bp in (0, 1):
                if (1 if p + bp >= BASE else 0) == din:
                    vals.add((p + a) % BASE + (p + bp) % BASE)
        T0[(a, din)] = sorted(vals)

NP = tp * m * Bud
def phid(t, j, b):
    return (t * m + j) * Bud + b

def succs(t, j, beta, w):
    """yield (ph2, head tuple (K-1 cells), tops list)"""
    K = len(w)
    g = clk[t]
    tn = (t + 1) % tp
    ac, low = LOW[(t, j)]
    a = ac
    e = [0] * K
    for i in range(K):
        s = w[i] + a
        e[i] = s % BASE
        a = 1 if s >= BASE else 0
    out = []
    for din in (0, 1):
        b = din
        r = [0] * K
        for i in range(K - 1, -1, -1):
            s = w[i] + b
            r[i] = s % BASE
            b = 1 if s >= BASE else 0
        ok, rb1 = low[b]
        if not ok:
            continue
        ph2 = phid(tn, j, beta - 1 if beta > 0 else 0)
        if g == 0:
            nw = [e[i] + r[i] for i in range(K)]
        else:
            nw = [e[0] + rb1] + [e[i] + r[i - 1] for i in range(1, K)]
        out.append((ph2, tuple(nw[:-1]), [nw[-1]]))
        if beta == 0 and not ZERO:
            leave = e[0] + (rb1 if g == 1 else r[0])
            if leave == W[tn][j]:
                ph3 = phid(tn, (j + 1) % m, Bud - 1)
                if g == 1:
                    head = tuple(e[i + 1] + r[i] for i in range(K - 1))
                    out.append((ph3, head, [tv + r[K - 1] for tv in range(BASE)]))
                else:
                    head = tuple(e[i + 1] + r[i + 1] for i in range(K - 1))
                    out.append((ph3, head, T0[(a, din)]))
    return out

parents = [[()] for _ in range(NP)]
for K in range(1, kmax + 1):
    T0_ = time.time()
    index = [{p: i for i, p in enumerate(parents[ph])} for ph in range(NP)]
    base = [0] * (NP + 1)
    for ph in range(NP):
        base[ph + 1] = base[ph] + len(parents[ph]) * BS
    N = base[NP]
    off = array('Q', bytes(8 * (N + 1)))
    dst = array('I')
    acc = bytearray(N)
    node = 0
    for ph in range(NP):
        beta = ph % Bud
        rest = ph // Bud
        t = rest // m
        j = rest % m
        latcell = W[t][j]
        for p in parents[ph]:
            for v in range(BS):
                w = p + (v,)
                acc[node] = 1 if w[0] != latcell else 0
                seen = set()
                for ph2, head, tops in succs(t, j, beta, w):
                    pi = index[ph2].get(head)
                    if pi is None:
                        continue
                    for tv in tops:
                        seen.add(base[ph2] + pi * BS + tv)
                dst.extend(sorted(seen))
                node += 1
                off[node] = len(dst)
    assert node == N
    # iterative Tarjan
    order = array('i', [-1]) * N
    low = array('i', [0]) * N
    onst = bytearray(N)
    keep = bytearray(N)
    st = []
    counter = 0
    for root in range(N):
        if order[root] != -1:
            continue
        order[root] = low[root] = counter
        counter += 1
        st.append(root)
        onst[root] = 1
        work = [(root, off[root])]
        while work:
            u, e_ = work[-1]
            if e_ < off[u + 1]:
                work[-1] = (u, e_ + 1)
                x = dst[e_]
                if order[x] == -1:
                    order[x] = low[x] = counter
                    counter += 1
                    st.append(x)
                    onst[x] = 1
                    work.append((x, off[x]))
                elif onst[x]:
                    if order[x] < low[u]:
                        low[u] = order[x]
            else:
                work.pop()
                if work:
                    pu = work[-1][0]
                    if low[u] < low[pu]:
                        low[pu] = low[u]
                if low[u] == order[u]:
                    i = len(st) - 1
                    while st[i] != u:
                        i -= 1
                    comp = st[i:]
                    del st[i:]
                    hasacc = False
                    for z in comp:
                        onst[z] = 0
                        if acc[z]:
                            hasacc = True
                    if hasacc and len(comp) >= 2:
                        for z in comp:
                            keep[z] = 1
    new = [[] for _ in range(NP)]
    tot = nacc = 0
    for ph in range(NP):
        for ip, p in enumerate(parents[ph]):
            for v in range(BS):
                nodeid = base[ph] + ip * BS + v
                if keep[nodeid]:
                    new[ph].append(p + (v,))
                    tot += 1
                    if acc[nodeid]:
                        nacc += 1
    print(f'K {K} CycAccBudget {tot} accepting {nacc} candidates {N} edges {len(dst)} time {time.time()-T0_:.1f}', flush=True)
    parents = new
    if tot == 0:
        print(f'EMPTY at K={K}')
        break
