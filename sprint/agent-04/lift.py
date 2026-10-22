#!/usr/bin/env python3
"""Lifting tower of a cycle of the k-column abstraction.

By Agent117.forwardPrefix_append_take, the first k entries of
forwardPrefix(s ++ [x], e') equal forwardPrefix(s, (x + e') // 10).  So a cycle
(w_0, e_0) -> (w_1, e_1) -> ... -> (w_{n-1}, e_{n-1}) -> w_0 of width k lifts to width k+1
exactly along the product graph on states (i, x), x in 0..18:
    (i, x) --e'--> (i+1 mod n, forwardPrefix(w_i ++ [x], e')[k])   whenever (x + e') // 10 == e_i.
Every (k+1)-closed walk projecting onto repetitions of the cycle is a cycle of this product graph
(its length is a multiple m*n).  We take the shortest lifted simple cycle at each level and lift it
again, up to a maximum width.  Prints, per level, the number of lifted cycles found (by start state)
and the shortest multiple m.

usage: lift.py WORDS_AND_CARRIES_JSON MAXWIDTH
  where the JSON is [[word, e], ...] in forward order (word -> next with carry e).
"""
import json
import sys
from collections import deque

from absref import forward_prefix, high_digits


def lift_once(cycle):
    """Return the shortest simple lifted cycle (forward order) or None, plus stats."""
    n = len(cycle)
    k = len(cycle[0][0])
    succ = {}
    for i, (w, e) in enumerate(cycle):
        for x in range(19):
            outs = []
            for ep in (0, 1):
                if (x + ep) // 10 != e:
                    continue
                p = forward_prefix(list(w) + [x], ep)
                assert p[:k] == list(cycle[(i + 1) % n][0]), "projection lemma violated"
                outs.append((p[k], ep))
            succ[(i, x)] = outs
    best = None
    n_start_with_cycle = 0
    # BFS from each state (0, x) back to itself: shortest closed walk through it
    for x0 in range(19):
        start = (0, x0)
        prev = {start: None}
        dq = deque([start])
        found = None
        while dq and found is None:
            st = dq.popleft()
            i, x = st
            for (x2, ep) in succ[st]:
                nxt = ((i + 1) % n, x2)
                if nxt == start:
                    found = (st, ep)
                    break
                if nxt not in prev:
                    prev[nxt] = (st, ep)
                    dq.append(nxt)
        if found is None:
            continue
        n_start_with_cycle += 1
        # reconstruct
        path = []
        st, ep = found
        path.append((st, ep))
        while prev[st] is not None:
            st, ep2 = prev[st]
            path.append((st, ep2))
        path.reverse()
        lifted = [(tuple(list(cycle[i][0]) + [x]), ep) for ((i, x), ep) in path]
        if best is None or len(lifted) < len(best):
            best = lifted
    return best, n_start_with_cycle


def check_cycle(cycle):
    n = len(cycle)
    for i, (w, e) in enumerate(cycle):
        assert forward_prefix(list(w), e) == list(cycle[(i + 1) % n][0])


def overflows(cycle):
    return sum(high_digits(list(w), e)[0] for w, e in cycle)


def main():
    cyc = [(tuple(w), e) for w, e in json.load(open(sys.argv[1]))]
    maxw = int(sys.argv[2])
    check_cycle(cyc)
    k = len(cyc[0][0])
    print(f"width {k}: cycle length {len(cyc)}, overflows per loop {overflows(cyc)}")
    while k < maxw:
        lifted, nstart = lift_once(cyc)
        if lifted is None:
            print(f"width {k + 1}: NO lift (no closed walk over repetitions of the width-{k} cycle)")
            return
        check_cycle(lifted)
        m = len(lifted) // len(cyc)
        print(f"width {k + 1}: shortest lift has length {len(lifted)} = {m} x {len(cyc)}, "
              f"overflows {overflows(lifted)}; start columns x with a closed lift: {nstart}/19")
        cyc = lifted
        k += 1
    print("final cycle:")
    for w, e in cyc:
        print("  ", list(w), "e=", e)


if __name__ == "__main__":
    main()
