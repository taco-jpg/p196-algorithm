#!/usr/bin/env python3
"""Independent recomputation of prefix ancestry bounds (sprint agent 20).

Written from the mathematical description only (no code shared with the Lean
generator or with Agent124's gen_code.py).

Model, width k.  For a positive integer n with L digits d_0..d_{L-1} (units
first) let q_i = d_i + d_{L-1-i} (column sums, symmetric, entries 0..18).
  * L >= k  -> state = (q_0, ..., q_{k-1})            ("long")
  * L <  k  -> state = (q_0, ..., q_{L-1})  full word  ("short")
One reverse-and-add step acts on the column word:
  low digits  s_j = (q_j + c_j) mod 10, c_0 = 0                (exact)
  high digits t_j = digit in column L-1-j, computed from q_{k-1}..q_0 with an
              unknown carry c_in into column L-k                (one free bit)
  no overflow: q'_j = s_j + t_j
  overflow   : q'_0 = s_0 + 1,  q'_j = s_j + t_{j-1}  (j >= 1)
Short words step exactly.  A backward path of length r ending in a state means r
steps of some actual orbit can precede it, so the longest backward path ("rank")
of every possible last-predecessor projection bounds the time to reach a
palindrome with the given prefix: t <= rank + 1.  A cycle means no bound.

Last predecessors of a palindrome P beginning with `pre` (ordinary final step):
its column word equals P's digits (all <= 9), so its projection is
pre ++ (digits) of length min(W, k), symmetric with even centre when W < k.
(The overflow final step is excluded by the same noOverflowPre test the Lean
endpoint uses; we only recompute entries that pass it.)

Usage:
  recompute_ranks.py K entries.json [--sample N --seed S] [--validate SEEDS]
Reads the JSON produced by extract_entries.py, keeps entries with width K,
samples N of them (default: all) and prints  prefix  claimed  recomputed  status.
"""
import argparse, json, random, sys, time
from functools import lru_cache


def next_full(q):
    """Exact next column word of a full (short) column word q."""
    L = len(q)
    d = []
    c = 0
    for i in range(L):
        v = q[i] + c
        d.append(v % 10)
        c = v // 10
    if c:
        d.append(1)
    L2 = len(d)
    return tuple(d[i] + d[L2 - 1 - i] for i in range(L2))


def forward_long(w, k):
    """All abstract successors of a long state (L >= k)."""
    s = []
    c = 0
    for j in range(k):
        v = w[j] + c
        s.append(v % 10)
        c = v // 10
    out = set()
    for cin in (0, 1):
        t = [0] * k
        u = cin
        for j in range(k - 1, -1, -1):
            v = w[j] + u
            t[j] = v % 10
            u = v // 10
        if u == 0:
            out.add(tuple(s[j] + t[j] for j in range(k)))
        else:
            out.add(tuple([s[0] + 1] + [s[j] + t[j - 1] for j in range(1, k)]))
    return out


def admissible_short_words(k):
    """All symmetric words of length < k, entries 0..18, q_0 >= 1, odd centre even."""
    res = []
    for L in range(1, k):
        h = (L + 1) // 2
        def rec(prefix):
            if len(prefix) == h:
                w = [prefix[min(i, L - 1 - i)] for i in range(L)]
                if w[0] >= 1 and (L % 2 == 0 or w[L // 2] % 2 == 0):
                    res.append(tuple(w))
                return
            for a in range(19):
                rec(prefix + [a])
        rec([])
    return res


def build_predecessors(k):
    """Reverse index of the abstract step at width k (long and short states)."""
    t0 = time.time()
    pred = {}
    # long -> long
    def gen(prefix):
        if len(prefix) == k:
            yield tuple(prefix)
            return
        lo = 1 if not prefix else 0
        for a in range(lo, 19):
            prefix.append(a)
            yield from gen(prefix)
            prefix.pop()
    n = 0
    for w in gen([]):
        n += 1
        for v in forward_long(w, k):
            pred.setdefault(v, []).append(w)
    # short -> short / long
    shorts = admissible_short_words(k)
    for s in shorts:
        v = next_full(s)
        if len(v) > k:  # cannot happen: len(v) <= len(s)+1 <= k
            raise AssertionError
        pred.setdefault(v, []).append(s)
    print(f"[k={k}] {n} long states, {len(shorts)} short words, "
          f"{len(pred)} targets indexed in {time.time()-t0:.1f}s", file=sys.stderr)
    return pred


def initial_words(pre, k):
    out = []
    m = len(pre)

    def tails(n):
        if n == 0:
            yield ()
            return
        for a in range(10):
            for rest in tails(n - 1):
                yield (a,) + rest
    for L in range(m, k + 1):
        for tl in tails(L - m):
            w = tuple(pre) + tl
            if L == k:
                out.append(w)
            else:
                sym = all(w[i] == w[L - 1 - i] for i in range(L))
                if sym and (L % 2 == 0 or w[L // 2] % 2 == 0):
                    out.append(w)
    return out


class Ranker:
    INF = float("inf")

    def __init__(self, pred):
        self.pred = pred
        self.rank = {}

    def get(self, w):
        """Longest backward path from w; INF if a cycle is reachable backwards."""
        if w in self.rank:
            return self.rank[w]
        # iterative DFS with colouring
        GREY = -1
        stack = [(w, iter(self.pred.get(w, ())))]
        self.rank[w] = GREY
        best = {w: 0}
        while stack:
            node, it = stack[-1]
            advanced = False
            for p in it:
                r = self.rank.get(p)
                if r is None:
                    self.rank[p] = GREY
                    best[p] = 0
                    stack.append((p, iter(self.pred.get(p, ()))))
                    advanced = True
                    break
                if r == GREY:
                    # cycle: mark everything on the stack as INF
                    for n_, _ in stack:
                        self.rank[n_] = self.INF
                    best_node = self.INF
                    # unwind
                    for n_, _ in stack:
                        best.pop(n_, None)
                    return self.INF
                best[node] = max(best[node], r + 1)
            if not advanced:
                stack.pop()
                val = best.pop(node)
                self.rank[node] = val
                if stack:
                    parent = stack[-1][0]
                    best[parent] = max(best[parent], val + 1)
        return self.rank[w]


def no_overflow_pre(pre):
    return pre[0] >= 2 or any(d >= 3 for d in pre)


def validate_model(k, nseeds, T, rng):
    """Check the model against actual orbits: every actual projected step must be
    an abstract step.  Returns number of checked steps."""
    def proj(n):
        d = [int(x) for x in str(n)[::-1]]
        L = len(d)
        q = tuple(d[i] + d[L - 1 - i] for i in range(L))
        return q[:k] if L >= k else q
    checked = 0
    for _ in range(nseeds):
        n = rng.randrange(1, 10 ** rng.randrange(1, 25))
        w = proj(n)
        for _t in range(T):
            n2 = n + int(str(n)[::-1])
            w2 = proj(n2)
            if len(w) == k and len(str(n)) >= k:
                ok = w2 in forward_long(w, k)
            else:
                ok = w2 == next_full(w)
            if not ok:
                raise SystemExit(f"MODEL ERROR: n={n} proj={w} -> {w2}")
            checked += 1
            n, w = n2, w2
    return checked


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("k", type=int)
    ap.add_argument("entries")
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--seed", type=int, default=20)
    ap.add_argument("--modules", default="", help="comma-separated module substrings to keep")
    ap.add_argument("--validate", type=int, default=2000, help="random seeds for model validation")
    a = ap.parse_args()
    rng = random.Random(a.seed)
    if a.validate:
        n = validate_model(a.k, a.validate, 60, rng)
        print(f"[k={a.k}] model validated on {n} actual reverse-and-add steps", file=sys.stderr)
    ents = [e for e in json.load(open(a.entries)) if e["k"] == a.k]
    if a.modules:
        keep = a.modules.split(",")
        ents = [e for e in ents if any(m in e["module"] for m in keep)]
    if a.sample and a.sample < len(ents):
        ents = rng.sample(ents, a.sample)
    pred = build_predecessors(a.k)
    R = Ranker(pred)
    agree = worse = better = cyc = 0
    for e in sorted(ents, key=lambda e: e["prefix"]):
        pre = e["prefix"]
        assert no_overflow_pre(pre)
        ws = initial_words(pre, a.k)
        rk = max(R.get(w) for w in ws)
        if rk == Ranker.INF:
            status = "CYCLE"; cyc += 1
        elif rk == e["bound"]:
            status = "equal"; agree += 1
        elif rk < e["bound"]:
            status = "claimed>recomputed"; better += 1
        else:
            status = "RECOMPUTED>CLAIMED"; worse += 1
        print(f"{''.join(map(str, pre))} {e['module']} claimed={e['bound']} recomputed={rk} {status}")
    print(f"[k={a.k}] {len(ents)} entries: equal {agree}, claimed>recomputed {better}, "
          f"recomputed>claimed {worse}, cycle {cyc}", file=sys.stderr)


if __name__ == "__main__":
    main()
