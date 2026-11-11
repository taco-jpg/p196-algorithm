#!/usr/bin/env python3
"""r12b: eventual-periodicity (stabilization) check for khx kept sets, and top-boundary properties.
usage: kstruct.py [--wit WITFILE] DUMP_A DUMP_B [DUMP ...]
 * ISO test between DUMP_A (level K) and DUMP_B (level K+d): phase-preserving bijection of kept nodes preserving the attributes
   (phase t, top digit, forward carry L_K into the next position) and the labelled edges (bit h).  Found by colour refinement on the
   disjoint union (+ individualisation if a class is not a singleton pair), then verified edge by edge.
 * For EVERY dump given: TOP99 = kept nodes whose two top digits are (9,9); with --wit, how many of them are the padded stream
   (window = pad_K(B_{t mod q})); TOPUU = kept nodes whose two top digits are (u,u) with u a uniform band value (0,18,6,12,2,4,8,16,14,10)."""
import sys, re, collections
args = sys.argv[1:]; wit = None; LL = 0
while args[0].startswith("--"):
    if args[0] == "--wit": wit = args[1]; args = args[2:]
    elif args[0] == "--L": LL = int(args[1]); args = args[2:]
b = 10; BANDV = {0, 18, 6, 12, 2, 4, 8, 16, 14, 10}
Bs = None; ROTS = [0]
if wit:
    line = [l for l in open(wit) if l.startswith("WIT")][0]
    Bs = [[int(v) for v in grp.split(",")] for grp in re.findall(r"\[([0-9,]+)\]", line)]
    gw = re.search(r"g=([01]+)", line).group(1); q0 = len(gw)
    ROTS = [r for r in range(q0) if all(gw[(t + r) % q0] == gw[t] for t in range(q0))]
def is_stream(n, K):
    q = len(Bs)
    for r in ROTS:
        B = Bs[(n["t"] + r) % q]
        if len(B) <= K and n["x"] == B + [9] * (K - len(B)): return True
    return False
def load(fn):
    K = None; nodes = {}
    for l in open(fn):
        if l.startswith("#"):
            m = re.search(r" K=(\d+)", l)
            if m: K = int(m.group(1))
            continue
        head, xs = l.split(":"); h = head.split()
        x = [int(v) for v in xs.split()]
        lc = 0
        for d in x: lc = (d + lc) // b
        nodes[int(h[0])] = dict(t=int(h[1]), o=(int(h[2]), int(h[3])), x=x, lc=lc)
    return K, nodes
def f_band(u): return 2 * ((u + (1 if u >= b else 0)) % b)
def closed_nodes(nodes, S, L, P, edge_ok=lambda i, j: True):
    # nodes of the induced subgraph on S lying on a closed walk of length exactly L (brute force from every node)
    S = set(S); res = set()
    for s0 in S:
        cur = {s0}; path_ok = False
        for st in range(L):
            nxt = set()
            for u in cur:
                for o in nodes[u]["o"]:
                    if o >= 0 and o in S and edge_ok(u, o): nxt.add(o)
            cur = nxt
            if not cur: break
        if s0 in cur: res.add(s0)
    return res
def props(fn, K, nodes):
    t99 = [i for i, n in nodes.items() if n["x"][-2:] == [9, 9]]
    tuu = [i for i, n in nodes.items() if n["x"][-1] == n["x"][-2] and n["x"][-1] in BANDV]
    s = "level %d (%s): kept=%d TOP99=%d TOPUU=%d" % (K, fn, len(nodes), len(t99), len(tuu))
    if Bs is not None:
        padded = 0; other = []
        for i in t99:
            if is_stream(nodes[i], K): padded += 1
            else: other.append(i)
        s += " TOP99_padded_stream=%d TOP99_other=%d" % (padded, len(other))
    if LL:
        P = max(n["t"] for n in nodes.values()) + 1
        c99 = closed_nodes(nodes, t99, LL, P)
        cuu = closed_nodes(nodes, tuu, LL, P, lambda i, j: f_band(nodes[i]["x"][-1]) == nodes[j]["x"][-1])
        s += " | closed-L-walk nodes inside TOP99=%d" % len(c99)
        if Bs is not None:
            nonpad = [i for i in c99 if not is_stream(nodes[i], K)]
            s += " (non-stream: %d)" % len(nonpad)
        s += " inside TOPUU(f-consistent)=%d" % len(cuu)
    print(s)
    return t99, tuu
def iso(A, B):
    # disjoint union, colour refinement
    nodes = [("A", i) for i in A] + [("B", i) for i in B]
    G = {"A": A, "B": B}
    col = {v: (G[v[0]][v[1]]["t"], G[v[0]][v[1]]["x"][-1], G[v[0]][v[1]]["lc"]) for v in nodes}
    inn = collections.defaultdict(list)
    for v in nodes:
        for h, o in enumerate(G[v[0]][v[1]]["o"]):
            if o >= 0: inn[(v[0], o)].append((h, v))
    def refine(col):
        while True:
            sig = {}
            for v in nodes:
                n = G[v[0]][v[1]]
                outs = tuple(col.get((v[0], o)) if o >= 0 else None for o in n["o"])
                ins = tuple(sorted((h, col[u]) for h, u in inn[v]))
                sig[v] = (col[v], outs, ins)
            ids = {}; new = {}
            for v in nodes: new[v] = ids.setdefault(sig[v], len(ids))
            if len(ids) == len(set(col.values())): return new
            col = new
    col = refine(col)
    while True:
        cls = collections.defaultdict(lambda: ([], []))
        for v in nodes: cls[col[v]][0 if v[0] == "A" else 1].append(v)
        if any(len(a) != len(bb) for a, bb in cls.values()): return None
        nonsingle = [c for c, (a, bb) in cls.items() if len(a) > 1]
        if not nonsingle: break
        c = nonsingle[0]; a, bb = cls[c]
        col = dict(col); m = max(col.values()) + 1
        col[a[0]] = m; col[bb[0]] = m          # individualise (no backtracking: verified below)
        col = refine(col)
    psi = {}
    for c, (a, bb) in cls.items(): psi[a[0][1]] = bb[0][1]
    for i, j in psi.items():
        na, nb = A[i], B[j]
        if (na["t"], na["x"][-1], na["lc"]) != (nb["t"], nb["x"][-1], nb["lc"]): return None
        for h in (0, 1):
            oa, ob = na["o"][h], nb["o"][h]
            if (oa < 0) != (ob < 0): return None
            if oa >= 0 and psi.get(oa) != ob: return None
    return psi
loaded = [(fn,) + load(fn) for fn in args]
for fn, K, nodes in loaded: props(fn, K, nodes)
(fa, Ka, A), (fb, Kb, B) = loaded[0], loaded[1]
psi = iso(A, B)
print("stream rotations used:", ROTS)
print("ISO level %d -> level %d: %s" % (Ka, Kb, "FOUND (verified, %d nodes)" % len(psi) if psi else "NOT FOUND"))
