#!/usr/bin/env python3
"""r12e: structure of a khxt -wdump (exact closed-L-walk node set at level K with full windows).
Prints: prefix-tree counts n_k = #distinct (phase, x_0..x_{k-1}) among the dumped nodes, for k = 1..K (= number of level-k nodes
that are projections of level-K closed-walk nodes); distinct top-j suffix patterns; trailing-9 statistics; top-digit histogram."""
import sys, numpy as np, collections
fn = sys.argv[1]
rows = []; ts = []
K = None
with open(fn) as f:
    for l in f:
        if l.startswith('#'):
            if ' K=' in l: K = int(l.split(' K=')[1].split()[0])
            continue
        h, xs = l.split(':')
        ts.append(int(h.split()[1])); rows.append(np.array(xs.split(), dtype=np.uint8))
X = np.vstack(rows); T = np.array(ts, dtype=np.int64); n, K = X.shape
print(f"nodes={n} K={K} phases={T.max()+1}")
# prefix counts via incremental hashing
hsh = T.astype(np.uint64) * np.uint64(1000003)
pc = []
for k in range(K):
    hsh = (hsh * np.uint64(1099511628211)) ^ (X[:, k].astype(np.uint64) + np.uint64(7))
    pc.append(len(np.unique(hsh)))
print("prefix counts n_k (k=1..K, every 10th):", [pc[k] for k in range(0, K, 10)] + [pc[-1]])
for j in (5, 10, 20, 40, 80):
    if j <= K:
        top = X[:, K - j:]
        u = np.unique(np.hstack([T[:, None].astype(np.uint8), top]), axis=0)
        print(f"distinct (phase, top-{j} digits): {len(u)}")
tr9 = np.zeros(n, dtype=np.int64)
for i in range(n):
    r = X[i][::-1]; c = 0
    while c < K and r[c] == 9: c += 1
    tr9[i] = c
print("trailing-9 count histogram:", sorted(collections.Counter(tr9.tolist()).items())[:20])
print("top digit histogram:", sorted(collections.Counter(X[:, -1].tolist()).items()))
# most common top-20 patterns
top20 = collections.Counter(tuple(r) for r in X[:, max(0, K - 20):])
print("most common top-20 suffixes:")
for pat, c in top20.most_common(8): print("  ", c, ' '.join(map(str, pat)))
# first position where windows (same phase) start to differ: depth of the common bottom part per phase
for t in range(min(3, T.max() + 1)):
    S = X[T == t]
    d = 0
    while d < K and np.all(S[:, d] == S[0, d]): d += 1
    print(f"phase {t}: {len(S)} nodes, common bottom prefix length {d}: {' '.join(map(str, S[0, :min(d, 40)]))}")
