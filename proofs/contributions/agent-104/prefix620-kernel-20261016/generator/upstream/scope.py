#!/usr/bin/env python3
"""Scoping: for each 3-digit prefix, find minimal certificate width k in {4,5,6,7}
such that the backward closure (prefix words of width k + full short words) from
all initial words is finite/acyclic; report height bound and node count.
Untrusted exploration only."""
import sys, json
from itertools import product
from functools import lru_cache
from collections import defaultdict

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
        yield from ((v,) for v in range(2, 19, 2)); return
    for a in range(1, 19):
        for tail in product(range(19), repeat=n // 2 - 1):
            left = (a,) + tail
            if n % 2:
                for center in range(0, 19, 2):
                    yield left + (center,) + left[::-1]
            else:
                yield left + left[::-1]

LOCAL = {}
for p, x, y in product(range(19), range(2), range(2)):
    LOCAL[p, x, y] = [(s, (s + x) // 10, z) for s in range(19) for z in (0, 1)
        if (s + z) // 10 == y and 2 * s + x + z - 10 * ((s + x) // 10 + y) == p]

@lru_cache(maxsize=None)
def prefix_predecessors(p):
    states = {((), 0, 0)}
    for v in p:
        states = {(word + (s,), xx, yy) for word, x, y in states
                  for s, xx, yy in LOCAL[v, x, y] if word or s > 0}
    answer = {word for word, _, _ in states}
    if p[0] > 10:
        return frozenset(answer)
    first = p[0] + 9 if p[0] <= 9 else 9
    states = {((first,), first // 10, 1)}
    for v in p[1:]:
        nxt = set()
        for word, x, y in states:
            for yy in (0, 1):
                if (word[-1] + yy) // 10 != y: continue
                digit = v - word[-1] - yy + 10 * y
                if not 0 <= digit <= 9: continue
                for xx in (0, 1):
                    s = digit + 10 * xx - x
                    if 0 <= s <= 18:
                        nxt.add((word + (s,), xx, yy))
        states = nxt
    answer.update(word for word, _, y in states if any((word[-1] + z) // 10 == y for z in (0, 1)))
    return frozenset(answer)

SHORT_BACK = {}
def short_back(k):
    if k not in SHORT_BACK:
        sb = defaultdict(set)
        for n in range(1, k):
            for s in raw_words(n):
                sb[F(s)].add(s)
        SHORT_BACK[k] = sb
    return SHORT_BACK[k]

def initial_words(abc, k):
    init = {abc + t for t in product(range(10), repeat=k - 3)}
    for n in range(3, k):
        for half in product(range(10), repeat=(n + 1) // 2):
            p = half + half[:n // 2][::-1]
            if p[:3] == abc and (n % 2 == 0 or p[n // 2] % 2 == 0):
                init.add(p)
    return init

def certify(abc, k, node_cap=400000):
    sb = short_back(k)
    def parents(p):
        ps = set(sb.get(p, ()))
        if len(p) == k:
            ps |= prefix_predecessors(p)
        return ps
    # DFS with cycle detection, memo heights
    height = {}
    state = {}
    init = initial_words(abc, k)
    sys.setrecursionlimit(100000)
    stack = []
    for root in init:
        if root in height: continue
        stack.append((root, iter(sorted(parents(root)))))
        state[root] = 1
        while stack:
            node, it = stack[-1]
            advanced = False
            for q in it:
                st = state.get(q)
                if st == 1:
                    return None, 'cycle', len(state)
                if st is None:
                    state[q] = 1
                    stack.append((q, iter(sorted(parents(q)))))
                    advanced = True
                    if len(state) > node_cap:
                        return None, 'cap', len(state)
                    break
            if not advanced:
                stack.pop()
                ps = parents(node)
                height[node] = 0 if not ps else 1 + max(height[q] for q in ps)
                state[node] = 2
    bound = 1 + max(height[p] for p in init)
    return bound, 'ok', len(height)

if __name__ == '__main__':
    base = json.load(open(sys.argv[1]))
    prefixes = sys.argv[2].split(',') if len(sys.argv) > 2 else sorted(base)
    widths = [int(w) for w in (sys.argv[3].split(',') if len(sys.argv) > 3 else ['4','5','6'])]
    out = {}
    for pre in prefixes:
        abc = tuple(int(c) for c in pre)
        res = {}
        for k in widths:
            b, status, n = certify(abc, k)
            res[k] = (b, status, n)
            if status == 'ok':
                break
        out[pre] = {'baseline': base.get(pre), 'results': res}
        print(pre, base.get(pre), res, flush=True)
    json.dump(out, open('scope_out.json', 'w'), indent=1)
