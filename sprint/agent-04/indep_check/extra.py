import time, numpy as np, scipy.sparse as sp
from defs import forwardPrefix
from graph import all_valid_words, forward_np, encode, B

for k in (4, 5):
    t0 = time.time()
    W = all_valid_words(k)
    N = len(W)
    tg = [encode(forward_np(W, e)) for e in (0, 1)]
    # full literal check
    for j in range(N):
        s = W[j].tolist()
        for e in (0, 1):
            pi = 0
            for v in forwardPrefix(s, e):
                pi = pi * B + v
            assert pi - B ** (k - 1) == tg[e][j]
    t1 = time.time()
    src = np.concatenate([np.arange(N), np.arange(N)[tg[1] != tg[0]]])
    dst = np.concatenate([tg[0], tg[1][tg[1] != tg[0]]])
    A = sp.csr_matrix((np.ones(len(src), dtype=np.float64), (src, dst)), shape=(N, N))
    M = A.copy()
    traces = []
    for L in range(1, 6):
        traces.append(int(round(M.diagonal().sum())))
        M = (M @ A).tocsr()
    print(f"k={k}: literal check all {N} words x 2 carries OK ({t1-t0:.1f}s); trace(A^L), L=1..5: {traces} ({time.time()-t1:.1f}s)")
