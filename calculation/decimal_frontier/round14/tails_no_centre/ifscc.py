#!/usr/bin/env python3
"""ifscc.py (main session, round 14 scoping; runs on the Studio only).
Interface graph of d-periodic rooted heads (notation of r13c Theorem B): node = interface, edge = one d-periodic column.
Every infinite path from the root is a d-periodic infinite closed history (exterior, band template or lattice).
Reports: node count (must equal the r13c values), non-trivial SCCs, cycle rank, entropy, closed-walk length spectrum, shortest cycles,
which census bands with T | d are tails of a rooted d-periodic history, and where the known lattices sit.
usage: ifscc.py G d [spectrum_max]
"""
import sys, re, glob, os, math, time, collections
b = int(os.environ.get('LYB', '10'))
H = os.environ.get('P196_H', os.path.expanduser('~/p196_run'))  # round14 copy: P196_H=data uses the shipped inputs


def col_succ(g, T, st):
    c, xb, A, root = st

    def step(t, v):
        ys = set()
        for h in (0, 1):
            Hb = (v + h) // b
            if not (A[t] >> Hb) & 1:
                continue
            if g[t]:
                part = 1 if xb[t] == -1 else (xb[t] + Hb) % b
            else:
                part = (v + h) % b
            ys.add((v + c[t]) % b + part)
        return ys
    starts = range(1, 2 * b - 1) if root else range(0, 2 * b - 1)
    path = [0] * (T + 1)
    out = []

    def dfs(t):
        if t == T:
            if path[T] == path[0]:
                out.append(tuple(path[:T]))
            return
        for y in step(t, path[t]):
            if y < 0 or y > 2 * b - 2:
                continue
            path[t + 1] = y
            dfs(t + 1)
    for v0 in starts:
        path[0] = v0
        dfs(0)
    return out


def succ_iface(g, T, st, col):
    c, xb, A, root = st
    cn = [0] * T
    xn = [0] * T
    An = [0] * T
    for t in range(T):
        v = col[t]
        vnext = col[(t + 1) % T]
        cn[t] = (v + c[t]) // b
        xn[t] = v if g[t] else 0
        mask = 0
        for h in (0, 1):
            Hb = (v + h) // b
            if not (A[t] >> Hb) & 1:
                continue
            part = (1 if xb[t] == -1 else (xb[t] + Hb) % b) if g[t] else (v + h) % b
            y = (v + c[t]) % b + part
            if y == vnext:
                mask |= (1 << h)
        An[t] = mask
    return (tuple(cn), tuple(xn), tuple(An), False)


def build(g, T):
    root = (tuple([0] * T), tuple([-1] * T), tuple(1 << g[t] for t in range(T)), True)
    ids = {root: 0}
    states = [root]
    adj = []
    level = [0]
    i = 0
    while i < len(states):
        st = states[i]
        out = {}
        for col in col_succ(g, T, st):
            s2 = succ_iface(g, T, st, col)
            j = ids.get(s2)
            if j is None:
                j = len(states)
                ids[s2] = j
                states.append(s2)
                level.append(level[i] + 1)
            out[col] = j
        adj.append(out)
        i += 1
    return states, adj, level


def tarjan(n, succ):
    index = [-1] * n
    low = [0] * n
    on = [False] * n
    st = []
    comps = []
    idx = 0
    for r in range(n):
        if index[r] != -1:
            continue
        work = [(r, 0)]
        index[r] = low[r] = idx
        idx += 1
        st.append(r)
        on[r] = True
        while work:
            v, pi = work.pop()
            adv = False
            sv = succ[v]
            while pi < len(sv):
                w = sv[pi]
                pi += 1
                if index[w] == -1:
                    work.append((v, pi))
                    index[w] = low[w] = idx
                    idx += 1
                    st.append(w)
                    on[w] = True
                    work.append((w, 0))
                    adv = True
                    break
                elif on[w]:
                    low[v] = min(low[v], index[w])
            if adv:
                continue
            if low[v] == index[v]:
                comp = []
                while True:
                    w = st.pop()
                    on[w] = False
                    comp.append(w)
                    if w == v:
                        break
                comps.append(comp)
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
    return comps


def row_step(x, gam):
    n = len(x)
    al = [0] * n
    for _ in range(n + 2):
        for c in range(n):
            al[(c + 1) % n] = 1 if x[c] + al[c] >= 10 else 0
    be = [0] * n
    for _ in range(n + 2):
        for c in range(n - 1, -1, -1):
            be[c] = 1 if x[c] + be[(c + 1) % n] >= 10 else 0
    lo = [(x[c] + al[c]) % 10 for c in range(n)]
    hi = [(x[c] + be[(c + 1) % n]) % 10 for c in range(n)]
    return [lo[c] + (hi[(c - 1) % n] if gam else hi[c]) for c in range(n)]


def alive_pairs(adj, nodes, cols):
    """pairs (node, r) with an infinite path labelled cols[r], cols[r+1], ... (periodic). Returns the alive set."""
    s = len(cols)
    nxt = {}
    for I in nodes:
        for r in range(s):
            j = adj[I].get(cols[r])
            if j is not None:
                nxt[(I, r)] = (j, (r + 1) % s)
    changed = True
    while changed:
        changed = False
        for k in list(nxt):
            if nxt[k] not in nxt:
                del nxt[k]
                changed = True
    return nxt


def main():
    G = sys.argv[1]
    d = int(sys.argv[2])
    smax = int(sys.argv[3]) if len(sys.argv) > 3 else 120
    g = [int(ch) for ch in (G * (d // len(G) + 1))[:d]]
    t0 = time.time()
    states, adj, level = build(g, d)
    n = len(states)
    nedges = sum(len(a) for a in adj)
    print(f'== clock {G} d={d}: interfaces {n}, height of saturation {max(level)}, labelled edges {nedges}, {time.time()-t0:.1f}s', flush=True)
    succ = [sorted(set(a.values())) for a in adj]
    comps = tarjan(n, succ)
    nontriv = []
    for comp in comps:
        if len(comp) > 1 or comp[0] in succ[comp[0]]:
            nontriv.append(comp)
    comp_of = {}
    for i, comp in enumerate(nontriv):
        for v in comp:
            comp_of[v] = i
    print(f'non-trivial SCCs: {len(nontriv)}, nodes on cycles: {len(comp_of)}', flush=True)
    # reachability among non-trivial SCCs
    order = sorted(range(len(nontriv)), key=lambda i: -len(nontriv[i]))
    for rank, i in enumerate(order[:40]):
        comp = nontriv[i]
        cs = set(comp)
        idx = {v: k for k, v in enumerate(comp)}
        E = sum(1 for v in comp for col, w in adj[v].items() if w in cs)
        rk = E - len(comp) + 1
        # period
        dist = {comp[0]: 0}
        q = collections.deque([comp[0]])
        per = 0
        while q:
            v = q.popleft()
            for w in adj[v].values():
                if w in cs:
                    if w not in dist:
                        dist[w] = dist[v] + 1
                        q.append(w)
                    else:
                        per = math.gcd(per, dist[v] + 1 - dist[w])
        # entropy by power iteration on A + I
        x = [1.0] * len(comp)
        ed = [(idx[v], idx[w]) for v in comp for col, w in adj[v].items() if w in cs]
        lam = 0.0
        for _ in range(400):
            y = x[:]
            for u, w in ed:
                y[w] += x[u]
            m = max(y)
            lam = m
            x = [a / m for a in y]
        # spectrum
        preds = [[] for _ in comp]
        for u, w in ed:
            preds[w].append(u)
        R = [1 << k for k in range(len(comp))]
        spec = []
        for k in range(1, smax + 1):
            Rn = [0] * len(comp)
            for w in range(len(comp)):
                acc = 0
                for u in preds[w]:
                    acc |= R[u]
                Rn[w] = acc
            R = Rn
            if any((R[v] >> v) & 1 for v in range(len(comp))):
                spec.append(k)
        # shortest cycle with labels
        best = None
        for s0 in comp[:3000]:
            par = {s0: None}
            q = collections.deque([s0])
            found = None
            while q and found is None:
                v = q.popleft()
                for col, w in adj[v].items():
                    if w not in cs:
                        continue
                    if w == s0:
                        found = (v, col)
                        break
                    if w not in par:
                        par[w] = (v, col)
                        q.append(w)
            if found is None:
                continue
            path = [found[1]]
            v = found[0]
            while par[v] is not None:
                u, col = par[v]
                path.append(col)
                v = u
            path.reverse()
            if best is None or len(path) < len(best):
                best = path
        minh = min(level[v] for v in comp)
        tper = 0
        print(f'SCC#{rank}: nodes {len(comp)} edges {E} rank {rk} period(gcd) {per} growth {lam-1:.5f} min height from root {minh}', flush=True)
        print(f'   closed-walk lengths <= {smax}: {spec[:60]}{" ..." if len(spec) > 60 else ""}', flush=True)
        if best:
            cols = best
            # minimal time period of the shortest cycle
            def tp(cols):
                for p in range(1, d + 1):
                    if d % p == 0 and all(c[(t + p) % d] == c[t] for c in cols for t in range(d)):
                        return p
            print(f'   shortest cycle length {len(cols)}, time period {tp(cols)}; row at t=0: {[c[0] for c in cols][:60]}', flush=True)
    if len(nontriv) > 40:
        print(f'... {len(nontriv)-40} smaller SCCs not listed; sizes {sorted((len(c) for c in nontriv), reverse=True)[:80]}')
    core = set(comp_of)
    # census bands
    tot = ok = 0
    okl = []
    hist = collections.Counter()
    for fn in sorted(glob.glob(f'{H}/mchk13a/logs/bc_{G}_s*.txt')):
        for line in open(fn):
            m = re.match(r'BAND (\S+) T=(\d+)', line)
            if not m:
                continue
            V = [int(x) for x in m.group(1).split(',')]
            T = int(m.group(2))
            if d % T:
                continue
            tot += 1
            rows = [V]
            for t in range(T - 1):
                rows.append(row_step(rows[t], g[t]))
            assert row_step(rows[-1], g[T - 1]) == V
            s = len(V)
            cols = [tuple(rows[t % T][i] for t in range(d)) for i in range(s)]
            al = alive_pairs(adj, core, cols)
            if al:
                okl.append((V, T, len(al)))
    print(f'census bands (s<=8) with T | {d}: {tot}; with a rooted {d}-periodic left end: {len(okl)}', flush=True)
    for V, T, k in okl:
        print(f'   LEFTEND band {V} T={T} (alive pairs {k})', flush=True)
    # known lattices
    for fn in sorted(glob.glob(f'{H}/mchk13b/lat/*.txt')):
        with open(fn) as f:
            lines = [l.split() for l in f if l.strip()]
        base, tp, nB, m = map(int, lines[0])
        if base != 10 or d % tp:
            continue
        clk = list(map(int, lines[1]))
        ext = [(g[t]) for t in range(tp)]
        if clk != ext:
            print(f'lattice {os.path.basename(fn)}: clock differs from this graph, skipped', flush=True)
            continue
        W = [list(map(int, lines[2 + nB and 0] if False else lines[2 + tp + t])) for t in range(tp)] if len(lines[2]) == nB else None
        if W is None:
            print('format?', fn)
            continue
        B = [list(map(int, lines[2 + t])) for t in range(tp)]
        cols = [tuple(W[t % tp][x] for t in range(d)) for x in range(m)]
        al = alive_pairs(adj, core, cols)
        where = sorted({comp_of[I] for (I, r) in al})
        # the head: follow from root
        cur = 0
        okh = True
        for x in range(nB):
            col = tuple(B[t % tp][x] for t in range(d))
            nx = adj[cur].get(col)
            if nx is None:
                okh = False
                print(f'   head of {os.path.basename(fn)} leaves the graph at column {x}')
                break
            cur = nx
        print(f'lattice {os.path.basename(fn)}: m={m} alive pairs {len(al)}, in SCC list-index {[order.index(i) for i in where]}; head from root follows graph: {okh}; interface after head on cycle: {cur in core}', flush=True)
    print(f'done {time.time()-t0:.1f}s', flush=True)


if __name__ == "__main__":
    main()
