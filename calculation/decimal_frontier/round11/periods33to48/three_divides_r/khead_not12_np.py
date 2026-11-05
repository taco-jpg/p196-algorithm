#!/usr/bin/env python3
"""Independent re-implementation (numpy/scipy, different code path from khead4.cpp) of the filtered K-head growth:

  S_1 = all (x0, phase), x0 in 1..18;  candidates at K = S_{K-1} x {0..18};
  edges (x,ph) -> (y,ph+1) for h in {0,1} with g(x,h) = pat[ph]   (trans() of repo py/khead_family.py);
  S_K = candidate nodes lying in a cyclic SCC whose period is NOT divisible by MOD.

Soundness: a closed walk of length L with MOD not dividing L projects onto a closed walk of the same length one level down,
so it stays inside the candidates; it lies in one cyclic SCC whose period q divides L, hence MOD does not divide q.
usage: khead_not12_np.py [Kmax=40] [pattern=0001] [MOD=12] [base=10]"""
import sys, math
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, breadth_first_order

Kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 40
pat = [int(c) for c in (sys.argv[2] if len(sys.argv) > 2 else '0001')]
MOD = int(sys.argv[3]) if len(sys.argv) > 3 else 12
P = len(pat); b = int(sys.argv[4]) if len(sys.argv) > 4 else 10; NX = 2 * b - 1

def trans(X, h):
    N, K = X.shape
    H = np.zeros((N, K + 1), np.int16); H[:, K] = h
    for i in range(K - 1, -1, -1): H[:, i] = (X[:, i] + H[:, i + 1]) // b
    g = H[:, 0].copy()
    L = np.zeros((N, K + 1), np.int16)
    for i in range(K): L[:, i + 1] = (X[:, i] + L[:, i]) // b
    Y = np.empty_like(X)
    for i in range(K):
        p1 = np.ones(N, np.int16) if i == 0 else (X[:, i - 1] + H[:, i]) % b
        p0 = (X[:, i] + H[:, i + 1]) % b
        Y[:, i] = (X[:, i] + L[:, i]) % b + np.where(g == 1, p1, p0)
    return Y, g

def keys(PH, X):
    A = np.ascontiguousarray(np.concatenate([PH[:, None], X], axis=1).astype(np.int8))
    return A.view(np.dtype((np.void, A.shape[1]))).ravel()

PH = np.repeat(np.arange(P, dtype=np.int16), NX - 1)
X = np.tile(np.arange(1, NX, dtype=np.int16), P)[:, None]
for K in range(1, Kmax + 1):
    if K > 1:
        N0 = X.shape[0]
        X = np.concatenate([np.repeat(X, NX, axis=0), np.tile(np.arange(NX, dtype=np.int16), N0)[:, None]], axis=1)
        PH = np.repeat(PH, NX)
    N = X.shape[0]
    kk = keys(PH, X); order = np.argsort(kk); ks = kk[order]
    src_l, dst_l = [], []
    for h in (0, 1):
        Y, g = trans(X, h)
        ok = g == np.array(pat, np.int16)[PH]
        tk = keys(((PH + 1) % P).astype(np.int16), Y)
        pos = np.searchsorted(ks, tk); pos = np.minimum(pos, N - 1)
        hit = ok & (ks[pos] == tk)
        src_l.append(np.nonzero(hit)[0]); dst_l.append(order[pos[hit]])
    src = np.concatenate(src_l); dst = np.concatenate(dst_l)
    A = csr_matrix((np.ones(len(src), np.int8), (src, dst)), shape=(N, N))
    nc, lab = connected_components(A, directed=True, connection='strong')
    intra = lab[src] == lab[dst]
    sizes = np.bincount(lab, minlength=nc)
    cyclic = np.zeros(nc, bool); cyclic[lab[src[intra]]] = True
    Ai = csr_matrix((np.ones(intra.sum(), np.int8), (src[intra], dst[intra])), shape=(N, N))
    dist = np.full(N, -1, np.int64); per = np.zeros(nc, np.int64)
    for c in np.nonzero(cyclic)[0]:
        root = int(np.nonzero(lab == c)[0][0])
        od, pred = breadth_first_order(Ai, root, directed=True, return_predecessors=True)
        dist[root] = 0
        for v in od[1:]: dist[v] = dist[pred[v]] + 1
    es, ed = src[intra], dst[intra]
    diff = np.abs(dist[es] + 1 - dist[ed])
    for c in np.nonzero(cyclic)[0]:
        m = lab[es] == c
        per[c] = int(np.gcd.reduce(diff[m])) if m.any() else 0
    keepc = cyclic & (per % MOD != 0)
    keep = keepc[lab]
    info = sorted(((int(sizes[c]), int(per[c])) for c in np.nonzero(cyclic)[0]), reverse=True)
    print(f'K={K}: candidates {N}, cyclic SCCs (size,period) {info[:8]}{" ..." if len(info) > 8 else ""}; kept (period not div by {MOD}): {int(keep.sum())}', flush=True)
    X = X[keep]; PH = PH[keep]
    if X.shape[0] == 0:
        print(f'=> no closed walk of length not divisible by {MOD} in the {K}-head graph of pattern {"".join(map(str, pat))}'); break
