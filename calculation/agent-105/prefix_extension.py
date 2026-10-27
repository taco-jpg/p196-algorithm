#!/usr/bin/env python3
"""Exact local extensions of LONG neutral-center prefix transitions.

Every returned edge has one source extension through r+v positions and one
inward carry.  Its paired raw prefix is (b-1)^v followed by the entire target
r-prefix.  This removes the arbitrary fresh coefficients of prefix_budget.

Positive loops are necessary local data, not globally consistent centers.
The search deliberately restricts to LONG projected states: a failed search
does not exclude cycles visiting shorter centers.  Short/overlap negatives
are not claimed.  Each positive edge instead has a disjoint full-center lift
at every source length m >= 2*(r+v)+1.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import product
import json
import math
from pathlib import Path
import random
import sys
import time

from prefix_budget import PrefixModel, find_closed, norm, verify_witness


class CapacityLimit(RuntimeError):
    pass


class ExtensionModel(PrefixModel):
    def __init__(self, depth=4, base=10, seconds=30.0, max_states=200000,
                 max_extension_cases=200000):
        if type(depth) is not int or type(base) is not int:
            raise ValueError("integer depth and base required")
        if not math.isfinite(seconds) or not 0 < seconds <= 1800:
            raise ValueError("finite positive time budget <= 1800 seconds required")
        if type(max_states) is not int or max_states <= 0:
            raise ValueError("positive integer state cap required")
        if type(max_extension_cases) is not int or max_extension_cases <= 0:
            raise ValueError("positive integer extension cap required")
        super().__init__(depth, base)
        self.deadline = time.monotonic() + seconds
        self.max_states = max_states
        self.max_extension_cases = max_extension_cases
        self.tables = {}
        self.operations = 0

    def check_budget(self):
        self.operations += 1
        if self.operations % 512 == 0 and time.monotonic() > self.deadline:
            raise TimeoutError

    @lru_cache(maxsize=None)
    def states(self, e):
        count = (self.b - 1) * (2 * self.b - 1) ** (self.r - 1)
        if count > self.max_states:
            raise CapacityLimit(f"LONG state count {count} exceeds {self.max_states}")
        heads = range(self.h) if e else range(self.b, 2 * self.b - 1)
        return tuple((a,) + tail for a in heads
                     for tail in product(self.alphabet, repeat=self.r - 1))

    def extension_outputs(self, v, left_carry, boundary_carry):
        """Map output tails to one exact (source extension, deep carry).

        Their arithmetic depends only on these three arguments, not on the
        already observed source prefix.  Distinct realizations of the same
        output tail can safely be deduplicated for this existential model.
        """
        key = (v, left_carry, boundary_carry)
        if key in self.tables:
            return self.tables[key]
        count = 2 * (2 * self.b - 1) ** v
        if count > self.max_extension_cases:
            raise CapacityLimit(f"extension cases {count} exceed {self.max_extension_cases}")
        table = {}
        for extension in product(self.alphabet, repeat=v):
            self.check_budget()
            left, _ = norm(self.b, extension, left_carry)
            for deep in (0, 1):
                backward, carry = norm(self.b, extension[::-1], deep)
                if carry != boundary_carry:
                    continue
                tail = tuple(a + b for a, b in zip(left, backward[::-1]))
                table.setdefault(tail, (extension, deep))
        self.tables[key] = table
        return table

    def raw_prefix(self, source, e, g, inner):
        left, left_carry = norm(self.b, source, e)
        backward, exit_carry = norm(self.b, source[::-1], inner)
        if exit_carry != 1 - e:
            return None
        right = backward[::-1]
        if g:
            raw = (left[0] + self.h * e,) + tuple(
                left[i] + right[i - 1] for i in range(1, self.r))
        else:
            raw = tuple(x + y for x, y in zip(left, right))
        return raw, left_carry

    def choices(self, source, e, g, next_e, budget):
        """Yield target, trim, original-depth carry, extension, deep carry."""
        self.check_budget()
        if len(source) != self.r or self.entry(source) != e or budget < 0:
            return
        seen = set()
        for inner in (0, 1):
            computed = self.raw_prefix(source, e, g, inner)
            if computed is None:
                continue
            raw, left_carry = computed
            j = 0
            while j < self.r and raw[j] == self.h:
                j += 1
            if g and j:
                raise ArithmeticError("canonical overflow has neutral head")
            costs = (j,) if j < self.r else range(self.r, budget + 1)
            for cost in costs:
                if cost > budget or (g and cost):
                    continue
                if cost == 0:
                    if self.entry(raw) == next_e and (raw, 0, inner) not in seen:
                        seen.add((raw, 0, inner))
                        yield raw, 0, inner, (), inner
                    continue
                if cost < self.r and int(raw[cost] < self.h) != next_e:
                    continue
                for tail, (extension, deep) in self.extension_outputs(
                        cost, left_carry, inner).items():
                    self.check_budget()
                    full_raw = raw + tail
                    if any(x != self.h for x in full_raw[:cost]):
                        continue
                    target = full_raw[cost:]
                    if len(target) != self.r or target[0] == self.h:
                        continue
                    if self.entry(target) != next_e:
                        continue
                    identity = (target, cost, inner)
                    if identity not in seen:
                        seen.add(identity)
                        yield target, cost, inner, extension, deep

    def edges(self, source, e, g, next_e, budget):
        for target, cost, inner, _, _ in self.choices(source, e, g, next_e, budget):
            yield target, cost, inner

    def lift_edge(self, source, target, e, g, v, inner=None):
        """Find the exact extension for a specified projected edge."""
        next_e = self.entry(target)
        for boundary in (0, 1) if inner is None else (inner,):
            computed = self.raw_prefix(source, e, g, boundary)
            if computed is None or (g and v):
                continue
            raw, left_carry = computed
            if v == 0:
                if raw == target and target[0] != self.h:
                    return {"extension": [], "deep_carry": boundary, "inner": boundary}
                continue
            if v < self.r:
                if raw[:v] != (self.h,) * v or raw[v:] != target[:self.r - v]:
                    continue
                tail = target[self.r - v:]
            else:
                if raw != (self.h,) * self.r:
                    continue
                tail = (self.h,) * (v - self.r) + target
            hit = self.extension_outputs(v, left_carry, boundary).get(tail)
            if hit is not None:
                extension, deep = hit
                return {"extension": list(extension), "deep_carry": deep, "inner": boundary}
        return None


def validate_drivers(e, g, repetitions, seconds):
    if repetitions < 1 or not math.isfinite(seconds) or not 0 < seconds <= 1800 or not e or not g:
        raise ValueError("positive repetitions/time and nonempty drivers required")
    if len(e) != len(g) or set(e + g) - {"0", "1"}:
        raise ValueError("equally long binary drivers required")
    return tuple(map(int, e)) * repetitions, tuple(map(int, g)) * repetitions


def attach_and_verify_lifts(model, ee, gg, result):
    """Verify projected data, construct ordinary mirror-tested local lifts."""
    verify_witness(model, ee, gg, result)
    path = result["path"]
    for edge in path:
        lift = model.lift_edge(tuple(edge["source"]), tuple(edge["target"]),
                               edge["e"], edge["g"], edge["v"], edge["inner"])
        if lift is None:
            return {"status": "OLD_WALK_EDGE_NOT_LOCALLY_LIFTABLE", "phase": edge["t"],
                    "edge": edge, "depth": model.r}
        edge.update(lift)
    # Choose one closed width schedule with disjoint observed boundary blocks.
    drift, offsets, minimum = 0, [], 1
    for edge in path:
        offsets.append(drift)
        minimum = max(minimum, 2 * (model.r + edge["v"]) + 1 - drift)
        drift += edge["g"] - 2 * edge["v"]
    if drift != 0:
        raise ValueError("width schedule does not close")
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror
    centers, targets = [], []
    for edge, offset in zip(path, offsets):
        width = minimum + offset
        x = edge["source"] + edge["extension"]
        middle_len = width - 2 * len(x)
        if middle_len < 1:
            raise ValueError("insufficient room for local carry reset")
        center = x + [2 * model.h * edge["deep_carry"]] * middle_len + x[::-1]
        exterior = [model.b if edge["g"] else 1, 0, model.b * edge["e"]]
        if not mirror.hyp(model.b, exterior, center):
            raise ValueError("constructed local source violates Hyp")
        if (mirror.e1(model.b, exterior), mirror.gam(model.b, exterior, center)) != (edge["e"], edge["g"]):
            raise ValueError("constructed exterior has wrong drivers")
        raw = mirror.nextC(model.b, exterior, center)
        _, target, _, trim = mirror.trim(model.b, [], raw)
        if trim != edge["v"] or target[:model.r] != edge["target"]:
            raise ValueError("ordinary mirror local lift failed")
        if len(target) != width + edge["g"] - 2 * edge["v"]:
            raise ValueError("local lift has the wrong target length")
        edge["source_width"] = width
        edge["target_width"] = len(target)
        centers.append(center)
        targets.append(target)
    seam_matches = [i for i in range(len(path))
                    if targets[i] == centers[(i + 1) % len(path)]]
    result["local_lifts_checked"] = len(path)
    result["initial_width"] = minimum
    result["full_center_seam_matches"] = seam_matches
    result["full_centers_form_cycle"] = len(seam_matches) == len(path)
    result["scope"] = "Locally liftable LONG prefix loop; full center seam compatibility is separate."
    return result


def refine_old_loop(depth=4, e="10100110011", g="11100010000", repetitions=1,
                    seconds=30.0, base=10):
    ee, gg = validate_drivers(e, g, repetitions, seconds)
    model = ExtensionModel(depth, base, seconds)
    try:
        model.states(ee[0])  # Apply the explicit state cap before the old search.
        old = find_closed(PrefixModel(depth, base), e, g, repetitions, seconds)
    except (CapacityLimit, TimeoutError) as exc:
        return {"status": "UNDECIDED_OLD_SEARCH_CAP", "reason": str(exc)}
    if old["status"] != "ABSTRACT_BUDGET_WITNESS":
        return old
    if any(len(edge["source"]) != depth for edge in old["path"]):
        return {"status": "UNDECIDED_SHORT_STATE_IN_OLD_WITNESS"}
    try:
        result = attach_and_verify_lifts(model, ee, gg, old)
    except (CapacityLimit, TimeoutError) as exc:
        return {"status": "UNDECIDED_LOCAL_LIFT_CAP", "reason": str(exc)}
    if result["status"] == "ABSTRACT_BUDGET_WITNESS":
        result["status"] = "OLD_LOOP_LOCALLY_LIFTED"
    return result


def find_refined_loop(depth=4, e="10100110011", g="11100010000", repetitions=1,
                      seconds=30.0, base=10):
    ee, gg = validate_drivers(e, g, repetitions, seconds)
    model = ExtensionModel(depth, base, seconds)
    try:
        result = find_closed(model, e, g, repetitions, seconds)
        if result["status"] == "ABSTRACT_BUDGET_WITNESS":
            result = attach_and_verify_lifts(model, ee, gg, result)
            if result["status"] == "ABSTRACT_BUDGET_WITNESS":
                result["status"] = "REFINED_LONG_PROJECTION_WITNESS"
        elif result["status"] == "EXHAUSTED_NO_ABSTRACT_BUDGET_CYCLE":
            result["status"] = "NO_LONG_PROJECTION_LOOP_AT_THIS_PERIOD"
            result["scope"] = "Only the stated LONG projection, period, and budget were exhausted."
        return result
    except (CapacityLimit, TimeoutError) as exc:
        return {"status": "UNDECIDED_CAP", "reason": str(exc)}


def selftest(seconds=30.0):
    """Actual-edge projection coverage, including overlap and deep trimming."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror
    deadline = time.monotonic() + seconds
    models = {(b, r): ExtensionModel(r, b, seconds, max_extension_cases=500000)
              for b in (2, 3, 4, 5, 10) for r in range(1, 5)}
    counts = {"projection_edges": 0, "overlap_edges": 0, "trim_at_least_depth": 0,
              "constructive_lifts": 0, "exhaustive_source_words": 0,
              "random_source_words": 0, "explicit_source_words": 0}

    def check_source(base, center):
        # The official mirror supplies the source normalization and exact edge.
        _, center, _, _ = mirror.trim(base, [], list(center))
        if not center or center[0] == base - 1:
            return
        e = int(center[0] < base - 1)
        for g in (0, 1):
            exterior = [base if g else 1, 0, base * e]
            if not mirror.hyp(base, exterior, center):
                raise ValueError("generated control source is not valid")
            raw = mirror.nextC(base, exterior, center)
            _, target, _, v = mirror.trim(base, [], raw)
            if not target or target[0] == base - 1:
                continue
            for r in range(1, 5):
                if min(len(center), len(target)) < r:
                    continue
                if time.monotonic() > deadline:
                    raise TimeoutError("selftest time limit")
                model = models[(base, r)]
                s = r + v
                # Both source and target lengths >= r imply s <= source length.
                actual_x = tuple(center[:s])
                actual_deep = mirror.norm(base, center[:len(center) - s], e)[1]
                left, _ = norm(base, actual_x, e)
                backward, exit_carry = norm(base, actual_x[::-1], actual_deep)
                if exit_carry != 1 - e:
                    raise ValueError("actual mirrored block has wrong exit carry")
                right = backward[::-1]
                observed = (tuple(x + y for x, y in zip(left, right)) if not g else
                            (left[0] + (base - 1) * e,) + tuple(
                                left[i] + right[i - 1] for i in range(1, s)))
                if observed != (base - 1,) * v + tuple(target[:r]):
                    raise ValueError("actual extended source disagrees with mirror prefix")
                lift = model.lift_edge(tuple(center[:r]), tuple(target[:r]), e, g, v)
                if lift is None:
                    raise ValueError("a genuine full-center edge was excluded")
                counts["projection_edges"] += 1
                counts["overlap_edges"] += int(len(center) < 2 * s)
                counts["trim_at_least_depth"] += int(v >= r)
                # Independently check the returned extension by a full mirror
                # step on its explicit disjoint constant-middle completion.
                x = list(center[:r]) + lift["extension"]
                local = x + [2 * (base - 1) * lift["deep_carry"]] + x[::-1]
                local_raw = mirror.nextC(base, exterior, local)
                _, local_target, _, local_v = mirror.trim(base, [], local_raw)
                if not mirror.hyp(base, exterior, local) or local_v != v:
                    raise ValueError("returned local completion has invalid carry/trim")
                if local_target[:r] != target[:r]:
                    raise ValueError("returned local completion has wrong target prefix")
                counts["constructive_lifts"] += 1

    try:
        for base in (2, 3, 4, 5):
            for length in range(1, 7):
                for half in product(range(2 * base - 1), repeat=(length + 1) // 2):
                    center = half + half[:length // 2][::-1]
                    counts["exhaustive_source_words"] += 1
                    check_source(base, center)
        rng = random.Random(105_2984389)
        for _ in range(5000):
            length = rng.randrange(1, 11)
            half = tuple(rng.randrange(19) for _ in range((length + 1) // 2))
            counts["random_source_words"] += 1
            check_source(10, half + half[:length // 2][::-1])
        # This exact input has v=4 on g=0, so every tested r includes a case
        # whose trim reaches or passes the stored boundary prefix.
        boundary = (4, 4, 14, 14)
        counts["explicit_source_words"] += 1
        check_source(10, boundary + (0,) * 6 + boundary[::-1])
    except (CapacityLimit, TimeoutError) as exc:
        return {"status": "UNDECIDED_TEST_CAP", "reason": str(exc), **counts}
    if not counts["overlap_edges"] or not counts["trim_at_least_depth"]:
        raise ValueError("required boundary test cases were not exercised")
    return {"status": "PASS", **counts}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", choices=("audit", "search", "selftest"))
    ap.add_argument("--depth", type=int, choices=range(1, 5), default=4)
    ap.add_argument("--base", type=int, default=10)
    ap.add_argument("--e", default="10100110011")
    ap.add_argument("--g", default="11100010000")
    ap.add_argument("--repetitions", type=int, default=1)
    ap.add_argument("--seconds", type=float, default=30.0)
    args = ap.parse_args()
    if args.mode == "selftest":
        result = selftest(args.seconds)
    else:
        fn = refine_old_loop if args.mode == "audit" else find_refined_loop
        result = fn(args.depth, args.e, args.g, args.repetitions, args.seconds, args.base)
    print(json.dumps(result))
    if result["status"].startswith("UNDECIDED"):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
