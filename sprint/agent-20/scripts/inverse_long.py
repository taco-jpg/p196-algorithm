#!/usr/bin/env python3
"""On-demand inverse of the width-k abstract step (sprint agent 20).

Same model as recompute_ranks.py, but predecessors are found by a column-by-column
search over carries instead of enumerating all 18*19^(k-1) states, so k = 6..10
backward searches are possible.  `check_against_index(k)` verifies, for k <= 5,
that this solver returns exactly the reverse index built by forward enumeration.

Usage: inverse_long.py K PREFIX [CLAIMED_BOUND]   e.g.  inverse_long.py 7 2641 5
"""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__file__))
from recompute_ranks import (forward_long, next_full, admissible_short_words,
                             build_predecessors, initial_words, no_overflow_pre)


def long_preds(w, k):
    out = []
    # non-overflow branch: (p_0+u_0)//10 == 0, w_j = s_j + t_j
    def rec_no(j, c, need, p):
        if j == k:
            out.append(tuple(p)); return
        for a in range(1 if j == 0 else 0, 19):
            for u in (0, 1):
                if (a + u) // 10 != need:
                    continue
                if (a + c) % 10 + (a + u) % 10 != w[j]:
                    continue
                p.append(a); rec_no(j + 1, (a + c) // 10, u, p); p.pop()
    rec_no(0, 0, 0, [])
    # overflow branch: (p_0+u_0)//10 == 1, w_0 = s_0 + 1, w_j = s_j + t_{j-1}
    def rec_ov(j, c, need, tprev, p):
        if j == k:
            out.append(tuple(p)); return
        for a in range(1 if j == 0 else 0, 19):
            for u in (0, 1):
                if (a + u) // 10 != need:
                    continue
                s = (a + c) % 10
                if j == 0:
                    if s + 1 != w[0]:
                        continue
                elif s + tprev != w[j]:
                    continue
                p.append(a); rec_ov(j + 1, (a + c) // 10, u, (a + u) % 10, p); p.pop()
    rec_ov(0, 0, 1, None, [])
    return out


class LazyPred:
    def __init__(self, k):
        self.k = k
        self.short_pred = {}
        for s in admissible_short_words(k):
            self.short_pred.setdefault(next_full(s), []).append(s)
        self.cache = {}

    def get(self, w, default=()):
        r = self.cache.get(w)
        if r is None:
            r = list(self.short_pred.get(w, ()))
            if len(w) == self.k:
                r += long_preds(w, self.k)
            self.cache[w] = r
        return r


def check_against_index(k):
    idx = build_predecessors(k)
    lp = LazyPred(k)
    n = 0
    for w, ps in idx.items():
        a = sorted(set(ps)); b = sorted(set(lp.get(w)))
        if a != b:
            raise SystemExit(f"inverse mismatch at k={k} w={w}: {len(a)} vs {len(b)}")
        n += 1
    # every other long state must have no predecessors here either
    from itertools import product
    extra = 0
    for w in product(range(1, 19), *[range(19)] * (k - 1)):
        if w not in idx and lp.get(w):
            extra += 1
    if extra:
        raise SystemExit(f"inverse has {extra} spurious targets at k={k}")
    print(f"[k={k}] lazy inverse equals forward index on {n} targets; "
          f"no spurious predecessors on the other long states", file=sys.stderr)


if __name__ == "__main__":
    if sys.argv[1] == "--check":
        for k in map(int, sys.argv[2:]):
            check_against_index(k)
        sys.exit(0)
    from recompute_ranks import Ranker
    k = int(sys.argv[1]); pre = [int(c) for c in sys.argv[2]]
    assert no_overflow_pre(pre)
    t0 = time.time()
    R = Ranker(LazyPred(k))
    ws = initial_words(pre, k)
    rk = max(R.get(w) for w in ws)
    claimed = sys.argv[3] if len(sys.argv) > 3 else "-"
    print(f"{sys.argv[2]} k={k} initial={len(ws)} recomputed={rk} claimed={claimed} "
          f"states={len(R.rank)} time={time.time()-t0:.1f}s")
