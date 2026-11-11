#!/usr/bin/env python3
"""Independent small-K check of the all-period accepting cyclic sets, in plain Python.
No carry tables: every step is computed by explicit carries along the whole lower word from column 0 (a_0 = 0, genuine
boundary), overflow compared with the clock, every column below the new frame compared with the lattice.
The closure is plain Tarjan on explicit dictionaries.
Exact orbits: plain big-number addition N + rev(N) on the explicit word.
Usage: pyscc.py LATFILE KMAX [ORBIT]"""
import sys

fn, kmax = sys.argv[1], int(sys.argv[2])
only = int(sys.argv[3]) if len(sys.argv) > 3 else None
tk = open(fn).read().split()
BASE, tp, nB, m = map(int, tk[:4])
clk = list(map(int, tk[4:4 + tp]))
v = list(map(int, tk[4 + tp:]))
Bt = [v[t * nB:(t + 1) * nB] for t in range(tp)]
v = v[tp * nB:]
W = [v[t * m:(t + 1) * m] for t in range(tp)]
BS = 2 * BASE - 1
QQ = 6


def L(t, x):
    return Bt[t][x] if x < nB else W[t][(x - nB) % m]


def succ(t, j, par, w):
    """All R_K successors (tuples of K cells) of window w at phase (t,j,par); frame c = nB + j + QQ*m."""
    K = len(w)
    c = nB + j + QQ * m
    g = clk[t]
    tn = (t + 1) % tp
    dh = 1 if (g == 1 and par == 0) else 0
    c2 = c + dh
    Plow = [L(t, x) for x in range(c)] + list(w)
    n1 = c + K
    e = [0] * n1
    a = 0
    for x in range(n1):
        s = Plow[x] + a
        e[x] = s % BASE
        a = 1 if s >= BASE else 0
    out = set()
    for Din in (0, 1):
        r = [0] * n1
        cur = Din
        for x in range(n1 - 1, -1, -1):
            s = Plow[x] + cur
            r[x] = s % BASE
            cur = 1 if s >= BASE else 0
        if cur != g:  # overflow of the whole word must follow the clock
            continue
        ok = True
        for y in range(c2):
            rr = (r[y - g] if y - g >= 0 else 1)  # y=0, g=1: the new top digit is the carry 1
            if e[y] + rr != L(tn, y):
                ok = False
                break
        if not ok:
            continue
        cells = []
        free_top = False
        for i in range(K):
            y = c2 + i
            rr = (r[y - g] if y - g >= 0 else 1)
            if y < n1:
                cells.append(e[y] + rr)
            else:
                free_top = True
                cells.append(rr)  # top cell: e-digit free
        if free_top:
            base_ = tuple(cells[:-1])
            for tv in range(BASE):
                out.add(base_ + (cells[-1] + tv,))
        else:
            out.add(tuple(cells))
    return out


def exact(t, j, par, w):
    """Plain big-number step of the explicit word with window w = the top K folded columns. None if the lattice breaks."""
    K = len(w)
    c = nB + j + QQ * m
    h = c + K
    n = 2 * h - par
    P = [L(t, x) for x in range(c)] + list(w)
    if par == 1 and P[h - 1] % 2:
        return None
    d = [0] * n
    for x in range(h - par):
        val = min(P[x], BASE - 1)
        d[x] = val
        d[n - 1 - x] = P[x] - val
    if par == 1:
        d[h - 1] = P[h - 1] // 2
    res = []
    carry = 0
    for i in range(n):
        s = d[i] + d[n - 1 - i] + carry
        res.append(s % BASE)
        carry = 1 if s >= BASE else 0
    if carry:
        res.append(carry)
    if carry != clk[t]:
        return None
    n2 = len(res)
    h2 = (n2 + 1) // 2
    Q = [res[x] + res[n2 - 1 - x] for x in range(h2)]
    c2 = h2 - K
    tn = (t + 1) % tp
    for x in range(c2):
        if Q[x] != L(tn, x):
            return None
    return tuple(Q[c2:])


def orbits():
    seen = set()
    out = []
    for t in range(tp):
        for j in range(m):
            for par in range(2):
                if (t, j, par) in seen:
                    continue
                o = []
                cur = (t, j, par)
                while cur not in seen:
                    seen.add(cur)
                    o.append(cur)
                    tt, jj, pp = cur
                    g = clk[tt]
                    dh = 1 if (g == 1 and pp == 0) else 0
                    cur = ((tt + 1) % tp, (jj + dh) % m, (pp + g) % 2)
                out.append(o)
    return out


def tarjan(nodes, adj):
    index = {}
    low = {}
    on = set()
    st = []
    comps = []
    cnt = 0
    for root in nodes:
        if root in index:
            continue
        work = [(root, iter(adj[root]))]
        index[root] = low[root] = cnt
        cnt += 1
        st.append(root)
        on.add(root)
        while work:
            u, it = work[-1]
            adv = False
            for v_ in it:
                if v_ not in index:
                    index[v_] = low[v_] = cnt
                    cnt += 1
                    st.append(v_)
                    on.add(v_)
                    work.append((v_, iter(adj[v_])))
                    adv = True
                    break
                elif v_ in on:
                    low[u] = min(low[u], index[v_])
            if adv:
                continue
            work.pop()
            if work:
                p = work[-1][0]
                low[p] = min(low[p], low[u])
            if low[u] == index[u]:
                comp = []
                while True:
                    x = st.pop()
                    on.discard(x)
                    comp.append(x)
                    if x == u:
                        break
                comps.append(comp)
    return comps


orbs = orbits()
print('# phases orbits', len(orbs), 'lengths', sorted(set(len(o) for o in orbs)))
for oi, ph in enumerate(orbs):
    if only is not None and oi != only:
        continue
    T = len(ph)
    parents = [{()} for _ in range(T)]
    print(f'orbit {oi} first phase {ph[0]} T={T}')
    for K in range(1, kmax + 1):
        cand = [set(p + (v_,) for p in parents[l] for v_ in range(BS)) for l in range(T)]
        adj = {}
        for l in range(T):
            t, j, par = ph[l]
            nl = (l + 1) % T
            for w in cand[l]:
                adj[(l, w)] = [(nl, s) for s in succ(t, j, par, w) if s in cand[nl]]
        comps = tarjan(list(adj.keys()), adj)
        new = [set() for _ in range(T)]
        total = acc = 0
        for comp in comps:
            if len(comp) < 2:
                continue
            flag = False
            for (l, w) in comp:
                t, j, par = ph[l]
                if w[0] != W[t][j]:
                    flag = True
                    break
            if flag:
                for (l, w) in comp:
                    new[l].add(w)
        for l in range(T):
            t, j, par = ph[l]
            for w in new[l]:
                total += 1
                if w[0] != W[t][j]:
                    acc += 1
        # exact orbits of any period inside the set (big-number addition)
        nxt = {}
        for l in range(T):
            t, j, par = ph[l]
            nl = (l + 1) % T
            for w in new[l]:
                y = exact(t, j, par, w)
                if y is not None and y in new[nl]:
                    nxt[(l, w)] = (nl, y)
        cycles = 0
        color = {}
        for s in nxt:
            if s in color:
                continue
            path = []
            x = s
            while x in nxt and x not in color:
                color[x] = 1
                path.append(x)
                x = nxt[x]
            if x in color and color[x] == 1 and x in nxt:
                cycles += 1
            for p in path:
                color[p] = 2
        print(f'K {K} CycAcc {total} accepting {acc} candidates {sum(len(c) for c in cand)} exact_periodic_orbits {cycles}', flush=True)
        parents = new
        if total == 0:
            print(f'EMPTY at K={K}')
            break
