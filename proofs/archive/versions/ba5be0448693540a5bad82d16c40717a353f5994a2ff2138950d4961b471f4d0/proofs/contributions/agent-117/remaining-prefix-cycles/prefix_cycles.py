#!/usr/bin/env python3
"""Independent k-column prefix abstraction of decimal reverse-and-add on pair-sum words.

Agent #117, task agent117-remaining-prefix-cycle-diagnosis.  Pure standard library.
Independent implementation (not derived from verify_certificates.py); the predecessor
relation was cross-checked against verify_certificates.prefix_predecessors on random
states (see cross_check.py) and reproduces the 739/620 closure sizes 58,501 and 59,189.

State: a tuple of the first k pair sums (low-order end, which equals the high-order
end by symmetry) of a realizable pair word of width >= k; or a complete short word
(width < k).  Predecessor relation = all k-prefixes of pair words s such that the
k-prefix of F(s) can equal the target, allowing both values of the unobserved inner
carry.  This is an over-approximation (sound for bounding ancestry).
"""
from itertools import product
from collections import defaultdict
import sys

def normalize(s):
    digits, carry = [], 0
    for u in s:
        carry, d = divmod(u + carry, 10)
        digits.append(d)
    if carry:
        digits.append(carry)
    return tuple(digits)

def F(s):
    d = normalize(s)
    return tuple(x + y for x, y in zip(d, d[::-1]))

def raw_words(n):
    if n == 1:
        yield from ((v,) for v in range(2, 19, 2))
        return
    for a in range(1, 19):
        for tail in product(range(19), repeat=n // 2 - 1):
            left = (a,) + tail
            if n % 2:
                for center in range(0, 19, 2):
                    yield left + (center,) + left[::-1]
            else:
                yield left + left[::-1]

def forward_prefixes(s):
    """Both possible k-prefixes of F(t) for any realizable t extending prefix s."""
    k = len(s)
    low, carry = [], 0
    for v in s:
        carry, d = divmod(v + carry, 10)
        low.append(d)
    out = set()
    for inner in (0, 1):
        high, carry = [0] * k, inner
        for i in range(k - 1, -1, -1):
            carry, high[i] = divmod(s[i] + carry, 10)
        if carry:
            p = (1 + low[0],) + tuple(low[i] + high[i - 1] for i in range(1, k))
        else:
            p = tuple(a + b for a, b in zip(low, high))
        out.add(p)
    return out

class Pred:
    """Predecessor enumeration by direct inversion of forward_prefixes, column by column."""
    def __init__(self, k):
        self.k = k
        # no-growth local table: (p, x, y') -> list of (s, x', y)
        # x = carry into column i from below (low chain), x' = carry out
        # y' = carry into column i from above (high chain, running downward), y = carry out (downward)
        self.ng = defaultdict(list)
        for p in range(19):
            for x in (0, 1):
                for yin in (0, 1):
                    for s in range(19):
                        xo = (s + x) // 10
                        yo = (s + yin) // 10
                        if (s + x - 10 * xo) + (s + yin - 10 * yo) == p:
                            self.ng[p, x, yin].append((s, xo, yo))
        self.cache = {}

    def preds(self, p):
        if p in self.cache:
            return self.cache[p]
        k = self.k
        res = set()
        # ---- no-growth branch: output p_i = low_i + high_i, low chain up, high chain down
        # process columns 0..k-1; the high-chain input carry at column i is the output carry
        # from column i+1 (unknown for i = k-1: free e)
        # we go from column k-1 downward? Simpler: enumerate forward via states (x, y) where
        # x = low carry into col i, y_in = high carry into col i (from col i+1).  Since y_in for
        # column i is determined by column i+1's s, enumerate columns from 0 upward tracking
        # the "required" high carry out of column i (= high carry into column i-1).
        # state: (word, x_next, y_required_out_of_next)
        states = {((), 0, 0)}  # column 0: downward carry out must be 0 (no top overflow)
        for i in range(k):
            v = p[i]
            nxt = set()
            for word, x, yreq in states:
                for yin in (0, 1):
                    for s, xo, yo in self.ng[v, x, yin]:
                        if i == 0 and s == 0:
                            continue
                        if yreq is not None and yo != yreq:
                            continue
                        nxt.add((word + (s,), xo, yin))
            states = nxt
        # the last column's yin is the free inner carry e: any value allowed
        for word, _, _ in states:
            res.add(word)
        # ---- growth branch: output width +1, p_0 = low_0 + 1, p_i = low_i + high_{i-1}
        # top carry out of the whole word = 1 means high chain carry out of column 0 (downward) = 1
        if p[0] <= 10:
            # low_0 = p_0 - 1 ; s_0 + 0 = low_0 + 10*x1  => s_0 = p_0 - 1 + 10*x1
            for x1 in (0, 1):
                s0 = p[0] - 1 + 10 * x1
                if not 0 < s0 <= 18 or not 0 <= p[0] - 1 <= 9:
                    continue
                # high chain downward through column 0 must output carry 1:
                # (s0 + yin0)//10 == 1
                states = set()
                for yin0 in (0, 1):
                    if (s0 + yin0) // 10 == 1:
                        states.add(((s0,), x1, yin0))
                # column i >= 1: p_i = low_i + high_{i-1}; high_{i-1} = (s_{i-1} + yin_{i-1}) % 10
                for i in range(1, k):
                    v = p[i]
                    nxt = set()
                    for word, x, yin_prev in states:
                        high_prev = (word[-1] + yin_prev) % 10
                        low_i = v - high_prev
                        if not 0 <= low_i <= 9:
                            continue
                        for xo in (0, 1):
                            s = low_i + 10 * xo - x
                            if not 0 <= s <= 18:
                                continue
                            # high carry into column i-1 (yin_prev) must equal carry out of column i
                            for yin in (0, 1):
                                if (s + yin) // 10 == yin_prev:
                                    nxt.add((word + (s,), xo, yin))
                    states = nxt
                for word, _, _ in states:
                    res.add(word)
        res = frozenset(res)
        self.cache[p] = res
        return res

def initial_states(prefix, k):
    head = tuple(map(int, prefix))
    init = {head + tail for tail in product(range(10), repeat=k - 3)}
    for n in range(3, k):
        for half in product(range(10), repeat=(n + 1) // 2):
            pal = half + half[:n // 2][::-1]
            if pal[:3] == head and (n % 2 == 0 or pal[n // 2] % 2 == 0):
                init.add(pal)
    return init

def short_table(k):
    short = defaultdict(set)
    for n in range(1, k):
        for s in raw_words(n):
            short[F(s)].add(s)
    return short

def analyze(prefix, k, cap=2_000_000, want_cycle=True):
    """Iterative DFS over predecessor edges.  Returns dict with status."""
    P = Pred(k)
    short = short_table(k)
    init = initial_states(prefix, k)
    def preds(p):
        ps = set(short.get(p, ()))
        if len(p) == k:
            ps |= P.preds(p)
        return ps
    WHITE, GREY, BLACK = 0, 1, 2
    color = {}
    stack = []
    nstates = 0
    cycle = None
    for s0 in init:
        if color.get(s0, WHITE) != WHITE:
            continue
        # iterative DFS with explicit iterator stack
        color[s0] = GREY
        stack.append((s0, iter(preds(s0))))
        path = [s0]
        while stack:
            node, it = stack[-1]
            advanced = False
            for q in it:
                c = color.get(q, WHITE)
                if c == GREY:
                    # back edge -> cycle
                    idx = path.index(q)
                    cycle = path[idx:] + [q]
                    break
                if c == WHITE:
                    color[q] = GREY
                    stack.append((q, iter(preds(q))))
                    path.append(q)
                    advanced = True
                    break
            if cycle:
                break
            if not advanced:
                color[node] = BLACK
                stack.pop()
                path.pop()
            if len(color) > cap:
                return {'prefix': prefix, 'k': k, 'status': 'CAP', 'states': len(color)}
        if cycle:
            break
    if cycle:
        # path[0] is an initial state; path[:idx] leads (by predecessor edges) to the cycle
        return {'prefix': prefix, 'k': k, 'status': 'CYCLE', 'states': len(color),
                'entry_path': [list(c) for c in path[:idx]],
                'cycle_len': len(cycle) - 1, 'cycle': [list(c) for c in cycle]}
    return {'prefix': prefix, 'k': k, 'status': 'ACYCLIC', 'states': len(color)}

if __name__ == '__main__':
    k = int(sys.argv[1]); cap = int(sys.argv[2])
    for prefix in sys.argv[3:]:
        r = analyze(prefix, k, cap)
        print(r, flush=True)
