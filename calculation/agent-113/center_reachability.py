#!/usr/bin/env python3
"""Independent global-tuple verifier for a fixed periodic center driver.

The carry model is the existing exact center-layer model. The cumulative
reachability reduction is credited to campaign Agent 101. This implementation
keeps the full temporal tuple and performs one chronological constraint walk;
it does not import or reproduce the optimized solver's segment factorization.

All coefficients are least significant first. Only binary trim schedules are
supported. The state cap bounds each materialized state set, not aggregate
process memory. The CLI additionally limits address space. A cap, allocation
failure, or deadline produces UNDECIDED, never an absence claim.
"""
from __future__ import annotations

import argparse
from collections import deque
import gc
from itertools import islice
import json
import math
import os
import resource
import time

NONE = -1
GEN, ODD, EVEN, EXTRA, INACTIVE = range(5)


class _Limit(Exception):
    pass


_RECOVERABLE = (_Limit, MemoryError, RecursionError)


class _Budget:
    def __init__(self, cap: int, seconds: float):
        if not isinstance(cap, int) or cap < 1:
            raise ValueError("cap must be a positive integer")
        if not math.isfinite(seconds) or not 0 < seconds <= 1800:
            raise ValueError("seconds must be in (0, 1800]")
        self.cap = cap
        self.start = time.monotonic()
        self.deadline = self.start + seconds
        # Leave enough memory to report an allocation failure after releasing
        # this reserve. The process address-space ceiling still includes it.
        self.report_reserve = bytearray(1 << 20)
        self.stats = dict(search_nodes=0, transition_calls=0,
                          generated_states=0, frontier_peak=0,
                          generic_states=0, generic_expanded=0,
                          fixed_cases=0, tail_cases=0)

    def tick(self):
        self.stats["search_nodes"] += 1
        if self.stats["search_nodes"] % 128 == 0:
            self.check()

    def check(self):
        if time.monotonic() >= self.deadline:
            raise _Limit("wall-time budget reached")

    def size(self, n, label="frontier"):
        self.stats["frontier_peak"] = max(self.stats["frontier_peak"], n)
        if n > self.cap:
            raise _Limit(label + " state cap reached")


def _bits(value):
    if isinstance(value, str):
        if not value or any(c not in "01" for c in value):
            raise ValueError("streams must be nonempty binary strings")
        return tuple(int(c) for c in value)
    out = tuple(value)
    if not out or any(not isinstance(c, int) or c not in (0, 1) for c in out):
        raise ValueError("streams must contain only integer bits")
    return out


class CenterProblem:
    def __init__(self, b: int, e, g, v):
        if not isinstance(b, int) or not 2 <= b <= 62:
            raise ValueError("supported bases are integers 2 through 62")
        self.b = b
        self.e, self.g, self.v = map(_bits, (e, g, v))
        self.p = len(self.e)
        if not len(self.g) == len(self.v) == self.p or self.p > 128:
            raise ValueError("equal stream lengths from 1 through 128 required")
        if sum(self.g) != 2 * sum(self.v):
            raise ValueError("closed lengths require sum(g) = 2 sum(v)")
        offsets = [0]
        for t in range(self.p - 1):
            offsets.append(offsets[-1] + self.g[t] - 2 * self.v[t])
        self.offsets = tuple(offsets)
        self.dmin = min(offsets)
        self.start = tuple((self.e[t], 1-self.e[t],
                            (b-1)*self.e[t] if self.g[t] else NONE, NONE)
                           for t in range(self.p))

    def _lengths(self, m0):
        if not isinstance(m0, int) or m0 < 1:
            raise ValueError("initial width must be a positive integer")
        return tuple(m0+d for d in self.offsets)

    def _profiles(self, lengths):
        """Lazy profiles avoid allocating a list proportional to initial width."""
        half = tuple((n+1)//2 for n in lengths)
        raw_half = tuple((n+self.g[t]+1)//2 for t, n in enumerate(lengths))
        for j in range(max(raw_half)):
            yield tuple(
                GEN if j < half[t]-1 else
                (ODD if lengths[t] % 2 else EVEN) if j == half[t]-1 else
                EXTRA if j < raw_half[t] else INACTIVE
                for t in range(self.p))

    def _transfer(self, source, profile, first, budget, columns=False):
        """Every simultaneous next-layer tuple, preserving temporal closure."""
        budget.check()
        budget.stats["transition_calls"] += 1
        b, p, h = self.b, self.p, self.b-1
        result = {}
        coeffs, updated = [NONE]*p, [None]*p

        def choices(kind):
            return range(2*b-1) if kind <= EVEN else (NONE,)

        def walk(t, c, c0):
            budget.tick()
            kind = profile[t]
            if (kind <= EVEN and not 0 <= c <= 2*b-2) or (kind > EVEN and c != NONE):
                return
            coeffs[t] = c
            lin, rout, previous_high, old_target = source[t]
            options = []
            if kind <= EVEN:
                low = (c+lin) % b
                lnext = (c+lin) // b
                if kind == ODD:
                    if lnext == rout:
                        options.append((lnext, rout, low))
                else:
                    incoming = (lnext,) if kind == EVEN else (0, 1)
                    for rin in incoming:
                        if (c+rin)//b == rout:
                            options.append((lnext, rin, (c+rin) % b))
            else:
                options.append((lin, rout, previous_high))
            for lnext, rnext, high in options:
                if kind <= EVEN:
                    raw = low + (previous_high if self.g[t] else high)
                    next_high = high if self.g[t] else NONE
                else:
                    raw = 2*previous_high if kind == EXTRA else NONE
                    next_high = previous_high
                updated[t] = (lnext, rnext, next_high)
                if self.v[t]:
                    if raw != (h if first else old_target):
                        continue
                    targets = choices(profile[(t+1) % p])
                else:
                    targets = (raw,)
                if t+1 == p:
                    if not self.v[t] and raw != c0:
                        continue
                    successor = tuple((*updated[q],
                                       coeffs[(q+1) % p] if self.v[q] else NONE)
                                      for q in range(p))
                    if successor not in result:
                        result[successor] = tuple(coeffs) if columns else None
                        budget.stats["generated_states"] += 1
                        budget.size(len(result), "single-transfer")
                else:
                    for target in targets:
                        walk(t+1, target, c0)

        for c0 in choices(profile[0]):
            walk(0, c0, c0)
        return result

    def _advance(self, frontier, profile, first, budget):
        out = set()
        for state in sorted(frontier):
            out.update(self._transfer(state, profile, first, budget))
            budget.size(len(out))
        return out

    def _fixed(self, m0, budget, witness):
        budget.stats["fixed_cases"] += 1
        lengths = self._lengths(m0)
        if min(lengths) < 1:
            return False, None
        profiles = self._profiles(lengths)
        frontier, parents = {self.start}, []
        for j, profile in enumerate(profiles):
            budget.check()
            out, layer_parent = set(), {}
            for state in sorted(frontier):
                successors = self._transfer(state, profile, j == 0, budget, witness)
                for dest, columns in successors.items():
                    if dest not in out:
                        out.add(dest)
                        if witness:
                            layer_parent[dest] = (state, columns)
                budget.size(len(out))
            if not out:
                return False, None
            frontier = out
            if witness:
                parents.append(layer_parent)
        if not witness:
            return True, None
        state, layers = min(frontier), []
        for layer_parent in reversed(parents):
            state, columns = layer_parent[state]
            layers.append(columns)
        layers.reverse()
        centers = []
        for t, n in enumerate(lengths):
            half = []
            for j in range((n+1)//2):
                if j % 1024 == 0:
                    budget.check()
                half.append(layers[j][t])
            centers.append(half + half[:n//2][::-1])
        if not self.verify_centers(centers, _budget=budget):
            raise RuntimeError("reconstructed center cycle failed direct replay")
        return True, centers

    def verify_centers(self, centers, *, _budget=None):
        if len(centers) != self.p:
            return False
        for t, center in enumerate(centers):
            if (not center or list(center) != list(center)[::-1] or
                    any(not isinstance(c, int) or not 0 <= c <= 2*self.b-2 for c in center)):
                return False
            digits, carry = [], self.e[t]
            for i, coefficient in enumerate(center):
                if _budget is not None and i % 1024 == 0:
                    _budget.check()
                total = coefficient + carry
                digits.append(total % self.b)
                carry = total // self.b
            if carry != 1-self.e[t]:
                return False
            if self.g[t]:
                digits.append((self.b-1)*self.e[t])
            raw = [x+y for x, y in zip(digits, reversed(digits))]
            v = self.v[t]
            if v:
                if len(raw) < 3 or raw[0] != self.b-1 or raw[-1] != self.b-1:
                    return False
                raw = raw[1:-1]
            if raw != list(centers[(t+1) % self.p]):
                return False
        return True

    def _result(self, budget, status, scope, reason, **extra):
        budget.report_reserve = None
        return dict(status=status, scope=scope, reason=reason, base=self.b,
                    period=self.p, counts=dict(budget.stats),
                    seconds=round(time.monotonic()-budget.start, 6), **extra)

    def fixed_width(self, m0, *, cap=50000, seconds=30, witness=False):
        budget = _Budget(cap, seconds)
        try:
            possible, centers = self._fixed(m0, budget, witness)
            budget.check()
            extra = dict(initial_width=m0)
            if centers is not None:
                extra["centers"] = centers
            return self._result(budget, "FEASIBLE" if possible else "EXHAUSTED",
                                "fixed initial center width and supplied schedule",
                                "complete global carry-layer decision", **extra)
        except _RECOVERABLE as exc:
            budget.report_reserve = None
            reason = str(exc) if isinstance(exc, _Limit) else type(exc).__name__
            centers = None
            exc.__traceback__ = None  # release any large unwound layer frontiers
            if isinstance(exc, MemoryError):
                gc.collect()
            return self._result(budget, "UNDECIDED", "fixed initial center width",
                                reason, initial_width=m0)

    def all_widths(self, *, cap=50000, seconds=30, witness=False):
        budget = _Budget(cap, seconds)
        scope = "all positive initial center widths for supplied binary schedule"
        try:
            # Exactly the two admissible widths whose common generic prefix is empty.
            for m0 in (1-self.dmin, 2-self.dmin):
                possible, centers = self._fixed(m0, budget, witness)
                if possible:
                    budget.check()
                    extra = dict(initial_width=m0)
                    if centers is not None:
                        extra["centers"] = centers
                    return self._result(budget, "FEASIBLE", scope,
                                        "finite boundary case", **extra)
            # For every q>=1 the two tail sequences equal these q=1 representatives.
            # These representatives have widths at most 2P+4, so their tails
            # can be retained without allocating proportional to a user width.
            tails = [tuple(islice(self._profiles(self._lengths(m0)), 1, None))
                     for m0 in (3-self.dmin, 4-self.dmin)]
            generic = (GEN,)*self.p
            first = self._transfer(self.start, generic, True, budget)
            seen = set(first)
            budget.size(len(seen), "generic-reachability")
            queue = deque((state, 1) for state in sorted(seen))
            budget.stats["generic_states"] = len(seen)
            while queue:
                state, depth = queue.popleft()
                for parity, profiles in enumerate(tails):
                    budget.stats["tail_cases"] += 1
                    frontier = {state}
                    for profile in profiles:
                        frontier = self._advance(frontier, profile, False, budget)
                        if not frontier:
                            break
                    if frontier:
                        m0 = 2*depth + 1 + parity - self.dmin
                        extra = dict(initial_width=m0, generic_depth=depth)
                        if witness:
                            possible, centers = self._fixed(m0, budget, True)
                            if not possible:
                                raise RuntimeError("reachability hit failed fixed-width replay")
                            extra["centers"] = centers
                        budget.check()
                        return self._result(budget, "FEASIBLE", scope,
                                            "reachable generic state with complete parity tail", **extra)
                successors = self._transfer(state, generic, False, budget)
                budget.stats["generic_expanded"] += 1
                for dest in successors:
                    if dest not in seen:
                        seen.add(dest)
                        budget.stats["generic_states"] = len(seen)
                        budget.size(len(seen), "generic-reachability")
                        queue.append((dest, depth+1))
            budget.check()
            return self._result(budget, "EXHAUSTED", scope,
                                "complete generic reachability and both parity tails")
        except _RECOVERABLE as exc:
            budget.report_reserve = None
            reason = str(exc) if isinstance(exc, _Limit) else type(exc).__name__
            # This handler shares a frame with the BFS. Free its large sets
            # before allocating the small structured failure report.
            first = seen = queue = frontier = successors = None
            exc.__traceback__ = None
            if isinstance(exc, MemoryError):
                gc.collect()
            return self._result(budget, "UNDECIDED", scope, reason)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", type=int)
    parser.add_argument("e")
    parser.add_argument("g")
    parser.add_argument("v")
    parser.add_argument("--width", type=int)
    parser.add_argument("--cap", type=int, default=50000)
    parser.add_argument("--seconds", type=float, default=30)
    parser.add_argument("--witness", action="store_true")
    parser.add_argument("--memory-mib", type=int, default=2048)
    args = parser.parse_args()
    try:
        if not 64 <= args.memory_mib <= 8192:
            raise ValueError("memory-mib must be in 64 through 8192")
        inherited = resource.getrlimit(resource.RLIMIT_AS)
        ceiling = min([args.memory_mib << 20] +
                      [limit for limit in inherited if limit != resource.RLIM_INFINITY])
        resource.setrlimit(resource.RLIMIT_AS, (ceiling, ceiling))
        problem = CenterProblem(args.base, args.e, args.g, args.v)
        options = dict(cap=args.cap, seconds=args.seconds, witness=args.witness)
        result = problem.all_widths(**options) if args.width is None else problem.fixed_width(args.width, **options)
    except ValueError as exc:
        result = dict(status="INVALID", reason=str(exc))
    except MemoryError:
        os.write(1, b'{"status":"UNDECIDED","reason":"MemoryError"}\n')
        return 3
    except RecursionError as exc:
        result = dict(status="UNDECIDED", reason=type(exc).__name__)
    except RuntimeError as exc:
        result = dict(status="UNDECIDED", reason="internal verification error", detail=str(exc))
    try:
        print(json.dumps(result, sort_keys=True))
    except MemoryError:
        os.write(1, b'{"status":"UNDECIDED","reason":"MemoryError"}\n')
        return 3
    return 0 if result["status"] in ("FEASIBLE", "EXHAUSTED") else 2 if result["status"] == "INVALID" else 3


if __name__ == "__main__":
    raise SystemExit(main())
