"""Cross-checks of the forward step (COMPUTED evidence, not a proof).

1. For width k = 3 exhaustively (and k = 4, 5 on random targets): for every
   source word s with 0 < s[0] and entries < 19, and every target p,
      s in prefixPredecessors(p)  <=>  p in {forwardPrefix(s,0), forwardPrefix(s,1)}.
2. Along the real orbit of 196 (t = 0..400, k = 3..10, only while width >= k):
   the actual next projection is one of the two forward successors.
"""
import itertools
import random
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from ref import forward_prefix, prefix_predecessors, column_word, reverse_add  # noqa: E402


def exhaustive(k):
    srcs = [list(s) for s in itertools.product(range(19), repeat=k) if s[0] > 0]
    fwd = {}
    for s in srcs:
        for e in (0, 1):
            fwd.setdefault(tuple(forward_prefix(s, e)), set()).add(tuple(s))
    bad = 0
    for p in itertools.product(range(19), repeat=k):
        pred = set(map(tuple, prefix_predecessors(list(p))))
        if pred != fwd.get(p, set()):
            bad += 1
    return len(srcs), bad


def sampled(k, n, seed):
    rng = random.Random(seed)
    bad = 0
    for _ in range(n):
        s = [rng.randrange(1, 19)] + [rng.randrange(19) for _ in range(k - 1)]
        for e in (0, 1):
            p = forward_prefix(s, e)
            if s not in prefix_predecessors(p):
                bad += 1
        # converse direction on a random target
        p = [rng.randrange(19) for _ in range(k)]
        for s2 in prefix_predecessors(p):
            if p not in (forward_prefix(s2, 0), forward_prefix(s2, 1)):
                bad += 1
    return bad


def orbit_check(T):
    n, bad, checks = 196, 0, 0
    for t in range(T):
        m = reverse_add(n)
        for k in range(3, 11):
            if len(str(n)) >= k:
                s = column_word(n, k)
                nxt = column_word(m, k)
                checks += 1
                if nxt not in (forward_prefix(s, 0), forward_prefix(s, 1)):
                    bad += 1
        n = m
    return checks, bad


if __name__ == "__main__":
    nsrc, bad3 = exhaustive(3)
    print(f"k=3 exhaustive: {nsrc} sources, all 6859 targets, mismatches={bad3}")
    for k in (4, 5):
        print(f"k={k} sampled 3000 sources/targets: mismatches={sampled(k, 3000, k)}")
    checks, bad = orbit_check(400)
    print(f"196 orbit t<400, k=3..10: {checks} transitions checked, mismatches={bad}")
