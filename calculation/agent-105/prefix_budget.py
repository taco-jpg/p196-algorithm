#!/usr/bin/env python3
"""Finite prefix relaxation of canonical neutral-center trim budgets.

A tuple of length r represents the first r coefficients of any symmetric
center of length at least r.  Shorter tuples represent complete centers.
This is an overapproximation: long states forget their length and the middle.
No accepted abstract walk alone is a center certificate.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import product
import json
from pathlib import Path
import random
import sys
import time


def norm(base, word, carry):
    digits = []
    for x in word:
        carry, digit = divmod(x + carry, base)
        digits.append(digit)
    return tuple(digits), carry


def canonical(word, base):
    word = tuple(word)
    v = 0
    while len(word) >= 2 and word[0] == word[-1] == base - 1:
        word = word[1:-1]
        v += 1
    return word, v


def exact_center_step(word, e, g, base=10):
    d, out = norm(base, word, e)
    if out != 1 - e:
        return None
    if g:
        d += ((base - 1) * e,)
    raw = tuple(x + y for x, y in zip(d, reversed(d)))
    w, v = canonical(raw, base)
    if not w or w[0] == base - 1:
        return None
    return w, v


class PrefixModel:
    def __init__(self, depth=2, base=10):
        if depth < 1 or base < 2:
            raise ValueError("depth >= 1 and base >= 2 required")
        self.r = depth
        self.b = base
        self.h = base - 1
        self.alphabet = range(2 * base - 1)

    def entry(self, state):
        if not state or state[0] == self.h:
            raise ValueError("canonical nonempty state required")
        return int(state[0] < self.h)

    def abstract(self, word):
        word, _ = canonical(word, self.b)
        if not word or word[0] == self.h:
            raise ValueError("center has no nonneutral canonical core")
        return word[:self.r]

    @lru_cache(maxsize=None)
    def short_states(self, e):
        ans = []
        for length in range(1, self.r):
            for half in product(self.alphabet, repeat=(length + 1) // 2):
                w = half + half[:length // 2][::-1]
                if w[0] != self.h and self.entry(w) == e:
                    ans.append(w)
        return tuple(ans)

    @lru_cache(maxsize=None)
    def states(self, e):
        ans = list(self.short_states(e))
        heads = range(self.h) if e else range(self.b, 2 * self.b - 1)
        ans.extend((a,) + tail for a in heads
                   for tail in product(self.alphabet, repeat=self.r - 1))
        return tuple(ans)

    def edges(self, state, e, g, next_e, budget):
        """Yield (target, exact-or-permitted trim cost, inward carry).

        For all-neutral observed raw prefixes, every cost >= r is admitted.
        Short source states use the exact full-word arithmetic.
        """
        if budget < 0 or self.entry(state) != e:
            return
        if len(state) < self.r:
            out = exact_center_step(state, e, g, self.b)
            if out is not None:
                w, v = out
                if v <= budget and self.entry(w) == next_e:
                    yield self.abstract(w), v, -1
            return
        left, _ = norm(self.b, state, e)
        seen = set()
        for inner in (0, 1):
            revdigits, exit_carry = norm(self.b, state[::-1], inner)
            if exit_carry != 1 - e:
                continue
            right = revdigits[::-1]
            if g:
                raw = (left[0] + self.h * e,) + tuple(
                    left[i] + right[i - 1] for i in range(1, self.r))
            else:
                raw = tuple(x + y for x, y in zip(left, right))
            j = 0
            while j < self.r and raw[j] == self.h:
                j += 1
            if g and j:
                raise AssertionError("canonical overflow cannot strip")
            if j == self.r:
                for cost in range(self.r, budget + 1):
                    for target in self.states(next_e):
                        key = (target, cost)
                        if key not in seen:
                            seen.add(key)
                            yield target, cost, inner
                continue
            if j > budget or int(raw[j] < self.h) != next_e:
                continue
            # Targets of length >= r: the unobserved end is unconstrained.
            for extra in product(self.alphabet, repeat=j):
                target = raw[j:] + extra
                key = (target, j)
                if key not in seen:
                    seen.add(key)
                    yield target, j, inner
            # A positive trim can expose a complete short center.  Check all
            # raw coefficients that remain visible, including its far padding.
            if j:
                for target in self.short_states(next_e):
                    if len(target) + 2 * j < self.r:
                        continue
                    visible = target + (self.h,) * j
                    if tuple(visible[:self.r - j]) != raw[j:]:
                        continue
                    key = (target, j)
                    if key not in seen:
                        seen.add(key)
                        yield target, j, inner


def find_closed(model, e, g, repetitions=1, seconds=20.0):
    if repetitions <= 0 or seconds <= 0:
        raise ValueError("positive repetitions and time budget required")
    if not e or not g or set(e + g) - {"0", "1"}:
        raise ValueError("nonempty binary driver words required")
    ee = tuple(map(int, e)) * repetitions
    gg = tuple(map(int, g)) * repetitions
    if len(ee) != len(gg) or not ee:
        raise ValueError("nonempty equally long driver words required")
    if sum(gg) % 2:
        return {"status": "ODD_OVERFLOW", "period": len(ee)}
    budget = sum(gg) // 2
    deadline = time.monotonic() + seconds
    calls = starts = 0
    total_states = len(model.states(ee[0]))
    for start in model.states(ee[0]):
        starts += 1
        failed = set()
        path = []

        def dfs(t, state, remaining):
            nonlocal calls
            calls += 1
            if calls % 1024 == 0 and time.monotonic() > deadline:
                raise TimeoutError
            if t == len(ee):
                return state == start and remaining == 0
            key = (t, state, remaining)
            if key in failed:
                return False
            for target, cost, inner in model.edges(
                    state, ee[t], gg[t], ee[(t + 1) % len(ee)], remaining):
                if t + 1 == len(ee) and (target != start or cost != remaining):
                    continue
                path.append({"t": t, "source": list(state), "e": ee[t],
                             "g": gg[t], "inner": inner, "v": cost,
                             "target": list(target)})
                if dfs(t + 1, target, remaining - cost):
                    return True
                path.pop()
            failed.add(key)
            return False
        try:
            found = dfs(0, start, budget)
        except TimeoutError:
            return {"status": "UNDECIDED_TIMEOUT", "period": len(ee),
                    "starts_checked": starts - 1, "starts_total": total_states,
                    "calls": calls}
        if found:
            result = {"status": "ABSTRACT_BUDGET_WITNESS", "period": len(ee),
                      "depth": model.r, "trim_total": budget,
                      "starts_checked": starts, "starts_total": total_states,
                      "calls": calls, "path": path}
            verify_witness(model, ee, gg, result)
            return result
    return {"status": "EXHAUSTED_NO_ABSTRACT_BUDGET_CYCLE", "period": len(ee),
            "depth": model.r, "trim_total": budget,
            "starts_checked": starts, "starts_total": total_states,
            "calls": calls}


def verify_witness(model, ee, gg, result):
    """Replay a reported abstract cycle without calling the edge generator."""
    path = result["path"]
    if len(path) != len(ee) or 2 * sum(x["v"] for x in path) != sum(gg):
        raise ValueError("wrong cycle length or trim budget")
    for t, edge in enumerate(path):
        source, target = tuple(edge["source"]), tuple(edge["target"])
        cost, inner = edge["v"], edge["inner"]
        if (edge["e"], edge["g"]) != (ee[t], gg[t]):
            raise ValueError("wrong driver labels")
        if target != tuple(path[(t + 1) % len(path)]["source"]):
            raise ValueError("not a closed abstract walk")
        for state, e in ((source, ee[t]), (target, ee[(t + 1) % len(ee)])):
            if not 1 <= len(state) <= model.r or any(x not in model.alphabet for x in state):
                raise ValueError("invalid abstract state")
            if model.entry(state) != e or (len(state) < model.r and state != state[::-1]):
                raise ValueError("invalid carry or short-center symmetry")
        if cost < 0:
            raise ValueError("negative trim")
        if len(source) < model.r:
            actual = exact_center_step(source, ee[t], gg[t], model.b)
            if actual is None or (model.abstract(actual[0]), actual[1]) != (target, cost):
                raise ValueError("invalid exact short-center edge")
            continue
        if inner not in (0, 1):
            raise ValueError("invalid inward carry")
        # Separate arithmetic loops intentionally avoid norm() and edges().
        forward, p = [], ee[t]
        for x in source:
            forward.append((x + p) % model.b)
            p = (x + p) // model.b
        right = [0] * model.r
        p = inner
        for j in range(model.r - 1, -1, -1):
            right[j] = (source[j] + p) % model.b
            p = (source[j] + p) // model.b
        if p != 1 - ee[t]:
            raise ValueError("wrong far exit carry")
        if gg[t]:
            raw = (forward[0] + model.h * ee[t],) + tuple(
                forward[j] + right[j - 1] for j in range(1, model.r))
            if cost:
                raise ValueError("overflow cannot trim a canonical source")
        else:
            raw = tuple(forward[j] + right[j] for j in range(model.r))
        if any(x != model.h for x in raw[:min(cost, model.r)]):
            raise ValueError("trimmed prefix is not neutral")
        if cost < model.r:
            if raw[cost] == model.h:
                raise ValueError("trim is not canonical")
            if len(target) == model.r:
                if target[:model.r - cost] != raw[cost:]:
                    raise ValueError("visible output prefix does not match")
            else:
                if not cost or len(target) + 2 * cost < model.r:
                    raise ValueError("impossible long-to-short length")
                if (target + (model.h,) * cost)[:model.r - cost] != raw[cost:]:
                    raise ValueError("visible short target does not match")


def selftest(samples=20000):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror
    rng = random.Random(105_22026)
    tested = 0
    for base in (2, 3, 4, 5, 10, 11, 17, 26):
        for depth in (1, 2, 3, 4):
            model = PrefixModel(depth, base)
            for _ in range(samples // 32):
                length = rng.randrange(1, 17)
                half = tuple(rng.randrange(2 * base - 1)
                             for _ in range((length + 1) // 2))
                word = half + half[:length // 2][::-1]
                word, _ = canonical(word, base)
                if not word or word[0] == base - 1:
                    continue
                e = model.entry(word)
                for g in (0, 1):
                    exterior = [base if g else 1, 0, base * e]
                    if (mirror.e1(base, exterior), mirror.gam(base, exterior, list(word))) != (e, g):
                        raise AssertionError("control exterior has wrong drivers")
                    observed = canonical(mirror.nextC(base, exterior, list(word)), base)
                    out = exact_center_step(word, e, g, base)
                    if out is None:
                        if observed[0] and observed[0][0] != base - 1:
                            raise AssertionError("independent center step disagrees with mirror")
                        continue
                    if observed != out:
                        raise AssertionError("independent center step disagrees with mirror")
                    w, cost = out
                    nexte = model.entry(w)
                    src, dst = model.abstract(word), model.abstract(w)
                    if not any(target == dst and v == cost for target, v, _ in
                               model.edges(src, e, g, nexte, cost)):
                        raise AssertionError((base, depth, word, e, g, w, cost))
                    tested += 1
    print(json.dumps({"mirror_projection_checks": tested, "status": "PASS"}))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--base", type=int, default=10)
    ap.add_argument("--e", default="10100110011")
    ap.add_argument("--g", default="11100010000")
    ap.add_argument("--repetitions", type=int, default=1)
    ap.add_argument("--seconds", type=float, default=20.0)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        return
    result = find_closed(PrefixModel(args.depth, args.base), args.e,
                         args.g, args.repetitions, args.seconds)
    print(json.dumps(result))
    if result["status"] == "UNDECIDED_TIMEOUT":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
