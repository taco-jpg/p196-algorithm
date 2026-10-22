"""Width-k prefix graph analysis (independent implementation)."""
import sys, time, itertools
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
from defs import forwardPrefix

B = 19


def all_valid_words(k):
    # rows = words with entries 0..18, first entry 1..18, in index order
    N = (B - 1) * B ** (k - 1)
    idx = np.arange(N, dtype=np.int64) + B ** (k - 1)
    W = np.empty((N, k), dtype=np.int64)
    t = idx.copy()
    for i in range(k - 1, -1, -1):
        W[:, i] = t % B
        t //= B
    return W


def encode(W):
    k = W.shape[1]
    idx = np.zeros(W.shape[0], dtype=np.int64)
    for i in range(k):
        idx = idx * B + W[:, i]
    return idx - B ** (k - 1)  # node id among valid words


def forward_np(W, e):
    N, k = W.shape
    lo = np.empty_like(W)
    x = np.zeros(N, dtype=np.int64)
    for i in range(k):
        s = W[:, i] + x
        lo[:, i] = s % 10
        x = s // 10
    hi = np.empty_like(W)
    c = np.full(N, e, dtype=np.int64)
    for i in range(k - 1, -1, -1):
        s = W[:, i] + c
        hi[:, i] = s % 10
        c = s // 10
    out = lo + hi
    ov = c != 0
    out_ov = lo.copy()
    out_ov[:, 0] += 1
    out_ov[:, 1:] += hi[:, :-1]
    out[ov] = out_ov[ov]
    return out


def main(k, literal_check=True):
    T = {}
    t0 = time.time()
    W = all_valid_words(k)
    N = W.shape[0]
    tgts = []
    for e in (0, 1):
        P = forward_np(W, e)
        assert P.min() >= 0 and P.max() <= 18 and P[:, 0].min() >= 1, "target out of vertex set"
        tgts.append(encode(P))
    T["build"] = time.time() - t0
    if literal_check:
        t1 = time.time()
        rng = np.random.default_rng(0)
        sample = np.arange(N) if N <= 200000 else rng.choice(N, 200000, replace=False)
        for j in sample:
            s = [int(v) for v in W[j]]
            for e in (0, 1):
                p = forwardPrefix(s, e)
                pi = 0
                for v in p:
                    pi = pi * B + v
                assert pi - B ** (k - 1) == tgts[e][j], (s, e, p)
        print(f"  literal forwardPrefix cross-check on {len(sample)} words OK ({time.time()-t1:.1f}s)")
    # dedupe edges (simple digraph)
    src = np.concatenate([np.arange(N), np.arange(N)])
    dst = np.concatenate(tgts)
    keep = np.ones(2 * N, dtype=bool)
    keep[N:] = tgts[1] != tgts[0]
    src, dst = src[keep], dst[keep]
    nself = int(np.sum(src == dst))
    A = sp.csr_matrix((np.ones(len(src), dtype=np.int8), (src, dst)), shape=(N, N))
    AT = A.T.tocsr()  # rows = target, columns = predecessors

    # Task 1 + 5: layered peeling of nodes with no remaining predecessors.
    t1 = time.time()
    indeg = np.bincount(dst, minlength=N).astype(np.int64)
    alive = np.ones(N, dtype=bool)
    rank = np.full(N, -1, dtype=np.int64)
    frontier = np.nonzero(indeg == 0)[0]
    r = 0
    while frontier.size:
        rank[frontier] = r
        alive[frontier] = False
        # decrement in-degree of successors of frontier
        succ = np.concatenate([tgts[0][frontier], tgts[1][frontier][tgts[1][frontier] != tgts[0][frontier]]])
        np.subtract.at(indeg, succ, 1)
        cand = np.unique(succ)
        frontier = cand[(indeg[cand] == 0) & alive[cand]]
        r += 1
    I = alive
    nI = int(I.sum())
    maxrank = int(rank[~I].max())
    T["peel"] = time.time() - t1
    print(f"k={k}: valid words N={N}, edges(dedup)={len(src)}, self-loops={nself}")
    print(f"  |I_{k}| = {nI}, fraction = {nI}/{N} = {nI/N:.6f}")
    print(f"  max finite backward rank (words not in I) = {maxrank}; rank histogram tail: "
          f"{np.bincount(rank[~I])[-5:].tolist()}")

    # Cross-check I via SCCs on the full graph: I = forward closure of nontrivial SCCs.
    t2 = time.time()
    ncomp, lab = connected_components(A, directed=True, connection="strong")
    sizes = np.bincount(lab)
    selfloop_nodes = src[src == dst]
    cyc = sizes[lab] > 1
    cyc[selfloop_nodes] = True
    reach = cyc.copy()
    fr = np.nonzero(reach)[0]
    while fr.size:
        nxt = np.unique(np.concatenate([tgts[0][fr], tgts[1][fr]]))
        nxt = nxt[~reach[nxt]]
        reach[nxt] = True
        fr = nxt
    assert np.array_equal(reach, I), "I mismatch between peeling and SCC-closure"
    print(f"  cross-check: forward closure of cyclic SCCs == peeled set: OK; nodes on a cycle in full graph = {int(cyc.sum())}")

    # Task 2: SCCs of the subgraph induced by I.
    Iidx = np.nonzero(I)[0]
    remap = np.full(N, -1, dtype=np.int64)
    remap[Iidx] = np.arange(nI)
    m = I[src] & I[dst]
    AI = sp.csr_matrix((np.ones(int(m.sum()), dtype=np.int8), (remap[src[m]], remap[dst[m]])), shape=(nI, nI))
    nc, labI = connected_components(AI, directed=True, connection="strong")
    sz = np.bincount(labI)
    sl = np.zeros(nI, dtype=bool)
    ssl = src[m][src[m] == dst[m]]
    sl[remap[ssl]] = True
    oncycle = (sz[labI] > 1) | sl
    order = np.sort(sz)[::-1]
    from collections import Counter
    print(f"  SCCs of I-induced subgraph: {nc}; sizes (desc, first 20) = {order[:20].tolist()}")
    print(f"  size multiset = {sorted(Counter(sz.tolist()).items(), reverse=True)[:30]}")
    print(f"  every word of I lies on a cycle: {bool(oncycle.all())} (on-cycle {int(oncycle.sum())} / {nI})")
    T["scc"] = time.time() - t2

    # Task 3: girth of whole graph and number of cycles of that length.
    # Closed walks of length L counted via trace of A^L restricted to cyclic nodes (cycles live in SCCs).
    t3 = time.time()
    C = np.nonzero(cyc)[0]
    remapC = np.full(N, -1, dtype=np.int64)
    remapC[C] = np.arange(C.size)
    mc = cyc[src] & cyc[dst] & (lab[src] == lab[dst])
    Ac = sp.csr_matrix((np.ones(int(mc.sum()), dtype=np.int64), (remapC[src[mc]], remapC[dst[mc]])), shape=(C.size, C.size))
    # successor lists inside cyclic part
    nC = C.size
    girth = None
    # walk enumeration: positions array per (start, branch) -- out-degree <= 2
    indptr, indices = Ac.indptr, Ac.indices
    deg = np.diff(indptr)
    starts = np.arange(nC)
    pos = starts.copy()
    owner = starts.copy()
    L = 0
    while girth is None:
        L += 1
        d = deg[pos]
        rep_owner = np.repeat(owner, d)
        # gather all successors
        offs = np.repeat(indptr[pos], d) + (np.arange(d.sum()) - np.repeat(np.cumsum(d) - d, d))
        pos = indices[offs]
        owner = rep_owner
        closed = pos == owner
        if closed.any():
            girth = L
            nwalks = int(closed.sum())
            cyc_starts = np.unique(owner[closed])
        if pos.size > 60_000_000:
            print("  walk enumeration too large; stopping at L =", L)
            break
    if girth is not None:
        assert nwalks % girth == 0
        print(f"  girth = {girth}; closed walks of length girth = {nwalks}; distinct cycles = {nwalks // girth}")
        # list the cycles (canonical by min node)
        cycles = []
        for st in cyc_starts:
            # find cycles of length girth through C[st] where C[st] is the minimal node
            stack = [(st, [st])]
            while stack:
                v, path = stack.pop()
                if len(path) == girth + 1:
                    if path[-1] == st and min(path[:-1]) == st:
                        cycles.append(tuple(int(C[x]) for x in path[:-1]))
                    continue
                for w in indices[indptr[v]:indptr[v + 1]]:
                    stack.append((w, path + [w]))
        cycles = sorted(set(cycles))
        print(f"  distinct cycles (enumerated, min-rotation canonical) = {len(cycles)}")
        if len(cycles) <= 12:
            for cy in cycles:
                print("   ", [W[j].tolist() for j in cy])
    T["girth"] = time.time() - t3

    # Task 4 data: return membership array and words
    print("  timings:", {a: round(b, 2) for a, b in T.items()})
    return W, I


def initial_ok(k, I):
    """For each 4-digit prefix abcd (1000..9999), does some initial word [a,b,c,d]++t (t in digits^(k-4)) lie in I?"""
    res = {}
    for n in range(1000, 10000):
        d = [int(ch) for ch in str(n)]
        ok = False
        for t in itertools.product(range(10), repeat=k - 4):
            w = d + list(t)
            j = 0
            for v in w:
                j = j * B + v
            j -= B ** (k - 1)
            if I[j]:
                ok = True
                break
        res[n] = ok
    return res


if __name__ == "__main__":
    t0 = time.time()
    W4, I4 = main(4)
    print(f"[k=4 total {time.time()-t0:.1f}s]")
    t0 = time.time()
    W5, I5 = main(5)
    print(f"[k=5 total {time.time()-t0:.1f}s]")
    t0 = time.time()
    ok4 = initial_ok(4, I4)
    ok5 = initial_ok(5, I5)
    skip = {n for n in range(1000, 10000) if str(n)[0] == "1" and all(int(c) <= 2 for c in str(n)[1:])}
    assert len(skip) == 27
    pref = [n for n in range(1000, 10000) if n not in skip]
    no4 = [n for n in pref if not ok4[n]]
    no5_but4 = [n for n in pref if ok4[n] and not ok5[n]]
    no5 = [n for n in pref if not ok5[n]]
    yes5_not4 = [n for n in pref if ok5[n] and not ok4[n]]
    print(f"Task 4: prefixes considered = {len(pref)}")
    print(f"  no initial word in I_4 (k=4): {len(no4)}")
    print(f"  no initial word in I_5 but had one in I_4: {len(no5_but4)}")
    print(f"  (total with no initial word in I_5: {len(no5)}; in I_5 but not I_4: {len(yes5_not4)})")
    print(f"  first few no4: {no4[:15]}")
    print(f"  first few no5_but4: {no5_but4[:15]}")
    print(f"[task4 {time.time()-t0:.1f}s]")
