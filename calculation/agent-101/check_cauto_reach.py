#!/usr/bin/env python3
"""Independent regression for cauto_reach's EXISTENTIAL all-length decision.

Build the comparator from calculation/neutral_band/structure/cauto_fast.cpp,
not cauto.cpp (whose old 128-bit key is unsafe on the period-22 fixtures).

Usage:
  python3 calculation/agent-101/check_cauto_reach.py \
      --engine /tmp/a101_reach --old /tmp/a101_old

The default exhaustive family is bases 2..5, periods 2..4, every binary e/g/v
with positive even sum(g) and sum(g)=2*sum(v): exactly 2,240 cases. Caps and
timeouts stay UNDECIDED. A test of a synthetic 121-cycle demonstrates a generic
frontier-periodicity limitation; it is expressly NOT an actual center instance.
Agent 116's separate base-20 research fixture is also independently replayed;
it is not counted among the eight pre-existing Lean-source positive controls.
No transcript, cache, or generated dataset is written.
"""
import argparse
import importlib.util
import itertools
import json
from pathlib import Path
import random
import re
import subprocess
import sys
import time


class TestFailure(RuntimeError):
    pass


def require(condition, message):
    """Keep regression checks active under python -O as well."""
    if not condition:
        raise TestFailure(message)


def bits(values):
    return "".join(map(str, values))


def center_image(base, center, entry, growth, trim):
    """Independent fixed-width INTEGER arithmetic; no engine/mirror step call."""
    number = entry + sum(x * base ** j for j, x in enumerate(center))
    if number // base ** len(center) != 1 - entry:
        return None
    digits = [(number // base ** j) % base for j in range(len(center))]
    if growth:
        digits.append((base - 1) * entry)
    image = [x + y for x, y in zip(digits, reversed(digits))]
    if len(image) - 2 * trim < 1:
        return None
    if any(x != base - 1 for x in image[:trim]):
        return None
    if trim and any(x != base - 1 for x in image[-trim:]):
        return None
    return image[trim:len(image) - trim] if trim else image


def verify_witness(case, result):
    base, es, gs, vs = case
    centers = result.get("C")
    require(isinstance(centers, list) and len(centers) == len(es),
            f"Missing/malformed witness C for {case}: {result}")
    for center in centers:
        require(isinstance(center, list) and len(center) >= 1,
                f"Empty/malformed center for {case}")
        require(all(type(x) is int and 0 <= x <= 2 * base - 2 for x in center),
                f"Out-of-range coefficient for {case}")
        require(center == center[::-1], f"Asymmetric center for {case}")
    require(type(result.get("m0")) is int and result["m0"] == len(centers[0]),
            f"Incorrect witness length for {case}")
    for t, center in enumerate(centers):
        got = center_image(base, center, int(es[t]), int(gs[t]), int(vs[t]))
        require(got == centers[(t + 1) % len(es)],
                f"Independent integer replay failed for {case}, phase {t}")
    offsets = [0]
    for g, v in zip(gs[:-1], vs[:-1]):
        offsets.append(offsets[-1] + int(g) - 2 * int(v))
    minimum = 1 - min(offsets)
    return len(centers[0]) < minimum + 2


def known_cases():
    """Read witnesses from the actual registered Lean-source certificate files."""
    mirror = Path(__file__).resolve().parents[1] / "neutral_band_search.py"
    spec = importlib.util.spec_from_file_location("agent101_existing_mirror", mirror)
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    records = []
    for base, edges in module._lean_certs():
        require(edges, f"Empty Lean-source certificate in base {base}")
        entry = []
        growth = []
        trim = []
        for exterior, center, _, _, _, v in edges:
            # Derive driver carries by independent positional integer arithmetic.
            carry = sum(x * base ** j for j, x in enumerate(exterior)) // base ** len(exterior)
            reverse_value = 1 - carry + sum(x * base ** j for j, x in enumerate(reversed(exterior)))
            overflow = reverse_value // base ** len(exterior)
            entry.append(carry)
            growth.append(overflow)
            trim.append(v)
        require(all(x in (0, 1) for x in entry + growth + trim),
                f"Control lies outside binary driver/trim model: base {base}")
        case = base, bits(entry), bits(growth), bits(trim)
        source_witness = {"m0": len(edges[0][1]), "C": [edge[1] for edge in edges]}
        verify_witness(case, source_witness)
        records.append(case)
    require(sorted(c[0] for c in records) == [2, 4, 8, 11, 16, 17, 26, 32],
            "The eight expected source controls were not recovered")
    return records


def exhaustive_cases():
    for base in range(2, 6):
        for period in range(2, 5):
            for gs in itertools.product((0, 1), repeat=period):
                total = sum(gs)
                if total == 0 or total % 2:
                    continue
                for positions in itertools.combinations(range(period), total // 2):
                    vs = bits(int(t in positions) for t in range(period))
                    for es in itertools.product((0, 1), repeat=period):
                        yield base, bits(es), bits(gs), vs


def random_cases(count, seed):
    rng = random.Random(seed)
    for _ in range(count):
        period = rng.randint(5, 8)
        total = rng.choice(list(range(2, period + 1, 2)))
        growth = set(rng.sample(range(period), total))
        trims = set(rng.sample(range(period), total // 2))
        yield (rng.choice([2, 3, 4, 5, 7, 10]),
               bits(rng.randrange(2) for _ in range(period)),
               bits(int(t in growth) for t in range(period)),
               bits(int(t in trims) for t in range(period)))


def negative_fixtures():
    families = [
        ("10100110011", "11100010000", [(0, 1), (3, 7), (9, 10)]),
        ("10100110011" * 2, "11100010000" * 2,
         [(0, 1, 11, 12), (3, 7, 14, 18), (8, 9, 19, 20)]),
        ("101010010101" * 2, "100010001000" * 2,
         [(0, 8, 16), (3, 11, 19), (7, 15, 23)]),
    ]
    for es, gs, trim_sets in families:
        for indices in trim_sets:
            vs = bits(int(t in indices) for t in range(len(es)))
            yield 10, es, gs, vs


def synthetic_cycle():
    """A finite-graph demonstration, not a reverse-and-add/center example."""
    frontier = frozenset([0])
    history = {frontier}
    repeated = False
    for _ in range(120):
        frontier = frozenset((x + 1) % 121 for x in frontier)
        if frontier in history:
            repeated = True
        history.add(frontier)
    require(not repeated, "Synthetic frontier repeated too early")
    reached, queue = {0}, [0]
    for x in queue:
        y = (x + 1) % 121
        if y not in reached:
            reached.add(y)
            queue.append(y)
    require(len(reached) == 121 and 120 in reached,
            "Synthetic cumulative reachability failed")
    return {"synthetic_graph_only": True, "cycle_states": 121,
            "frontier_repeated_within_120_steps": repeated,
            "cumulative_closure_states": len(reached), "tail_target_reachable": True}


class Runner:
    def __init__(self, args):
        self.args = args
        self.started = time.monotonic()
        self.last_progress = self.started
        self.undecided = []
        self.stats = {"known_controls": 0, "agent116_base20_fixture": 0, "exhaustive_cases": 0,
                      "random_cases": 0, "negative_fixtures": 0,
                      "terminal_agreements": 0, "old_undecided": 0,
                      "new_undecided": 0, "verified_witnesses": 0,
                      "short_length_witnesses": 0, "guard_cases": 0}

    def invoke(self, command, timeout=None):
        if time.monotonic() - self.started > self.args.budget_seconds:
            raise TimeoutError("Whole regression budget exhausted")
        try:
            return subprocess.run(command, capture_output=True, text=True,
                                  timeout=self.args.timeout if timeout is None else timeout)
        except subprocess.TimeoutExpired:
            return None

    def new(self, case, extra=(), timeout=None):
        base, es, gs, vs = case
        command = [self.args.engine, str(base), es, gs, vs, "--cap", str(self.args.cap),
                   "--seconds", str(max(1, int(self.args.timeout) - 1)), *extra]
        process = self.invoke(command, timeout)
        if process is None:
            return {"status": "UNDECIDED", "reason": "external timeout"}
        try:
            result = json.loads(process.stdout)
        except (ValueError, TypeError) as exc:
            raise TestFailure(f"Invalid engine JSON for {case}: exit={process.returncode}, "
                              f"stdout={process.stdout[:300]!r}, stderr={process.stderr[:300]!r}") from exc
        require(isinstance(result, dict) and result.get("status") in ("NONE", "FEASIBLE", "UNDECIDED"),
                f"Unexpected engine status for {case}: {result}")
        if result["status"] != "UNDECIDED":
            require(process.returncode == 0, f"Terminal result with nonzero exit for {case}")
        if result["status"] == "FEASIBLE":
            short = verify_witness(case, result)
            self.stats["verified_witnesses"] += 1
            self.stats["short_length_witnesses"] += int(short)
        return result

    def old(self, case):
        base, es, gs, vs = case
        # Even the legacy fallback of cauto_fast is safely packed here.
        require(2 * len(es) + 6 * gs.count("1") + 7 * vs.count("1") <= 256,
                "Comparator key exceeds cauto_fast's safe capacity")
        command = [self.args.old, str(base), es, gs, "1", "1", "-v", vs,
                   "-allm", "-cap", str(self.args.cap)]
        process = self.invoke(command)
        if process is None:
            return "UNDECIDED"
        require(process.returncode == 0,
                f"Old comparator failed for {case}: {process.stderr[:300]}")
        if re.search(r"^FEASIBLE(?:_CLASS)?\b", process.stdout, re.M):
            return "FEASIBLE"
        statuses = re.findall(r"^DONE .*\bstatus=(\w+)", process.stdout, re.M)
        require(len(statuses) == 1, f"Missing exact old completion status for {case}")
        if statuses[0] == "none":
            return "NONE"
        require(statuses[0] in ("capped", "noperiod"),
                f"Unexpected old comparator status {statuses[0]} for {case}")
        return "UNDECIDED"

    def agent116_fixture(self):
        """Credited center regression, not a new certificate discovery/theorem."""
        case = (20, "10100101", "10001000", "00100000")
        result = self.new(case, ("--cap", "250000", "--seconds", "30",
                                 "--memory-mb", "1024"), timeout=31)
        require(result["status"] == "FEASIBLE",
                f"Agent 116 base-20 fixture was not accepted: {result}")
        self.stats["agent116_base20_fixture"] += 1
        process = self.invoke([self.args.old, "20", case[1], case[2], "1", "1",
                               "-v", case[3], "-allm", "-cap", "250000"], timeout=31)
        old = {"status": "UNDECIDED", "reason": "external_timeout"}
        if process is not None:
            require(process.returncode == 0, "Old engine failed on Agent 116 fixture")
            done = re.findall(r"^DONE (.*)$", process.stdout, re.M)
            require(len(done) == 1, "Missing old completion status for Agent 116 fixture")
            fields = dict(re.findall(r"(\w+)=([^ ]+)", done[0]))
            raw_status = fields.get("status")
            require(raw_status in ("hit", "capped", "noperiod"),
                    f"Old engine contradicts a replayed positive: {raw_status}")
            old = {"status": "FEASIBLE" if raw_status == "hit" else "UNDECIDED",
                   "reported_status": raw_status.upper()}
            for key in ("maxstates", "tails", "sec", "rssMB"):
                if key in fields:
                    old[key] = float(fields[key]) if key == "sec" else int(fields[key])
        # A capped/NOPERIOD old run is an incomplete decision, not a disagreement.
        if old["status"] == "UNDECIDED":
            self.stats["old_undecided"] += 1
            self.undecided.append({"case": case, "family": "agent116_base20_fixture",
                                   "new": "FEASIBLE", "old": "UNDECIDED",
                                   "old_reported_status": old.get("reported_status", "TIMEOUT")})
        else:
            self.stats["terminal_agreements"] += 1
        return {"credit": "Agent 116",
                "source": "https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432893018",
                "case": case, "cap": 250000, "independent_integer_replay": True,
                "new": {key: result[key] for key in ("status", "m0", "visited", "generic_depth",
                        "max_frontier", "tail_calls", "seconds") if key in result},
                "old": old}

    def compare(self, case, kind, expected_none=False):
        new = self.new(case)
        old = self.old(case)
        status = new["status"]
        self.stats[kind] += 1
        self.stats["new_undecided"] += status == "UNDECIDED"
        self.stats["old_undecided"] += old == "UNDECIDED"
        if status == "UNDECIDED" or old == "UNDECIDED":
            self.undecided.append({"case": case, "family": kind,
                                   "new": status, "new_reason": new.get("reason"),
                                   "old": old})
        if status != "UNDECIDED" and old != "UNDECIDED":
            require(status == old, f"Differential mismatch for {case}: new={status}, old={old}")
            self.stats["terminal_agreements"] += 1
        if expected_none:
            require(status != "FEASIBLE" and old != "FEASIBLE",
                    f"Published bounded fixture unexpectedly feasible: {case}")
        now = time.monotonic()
        if now - self.last_progress >= 10:
            print(json.dumps({"progress": self.stats, "seconds": round(now-self.started, 2)}),
                  file=sys.stderr, flush=True)
            self.last_progress = now

    def guards(self):
        # Unsupported/malformed domains must not silently become a negative answer.
        cases = [(1, "0101", "0101", "0001"),
                 (63, "0101", "0101", "0001"),
                 (10, "", "", ""),
                 (10, "01", "0101", "0001"),
                 (10, "0121", "0101", "0001"),
                 (10, "0101", "0121", "0001"),
                 (10, "0101", "0101", "0002"),
                 (10, "0" * 33, "11" + "0" * 31, "1" + "0" * 32)]
        for case in cases:
            process = self.invoke([self.args.engine, *map(str, case)])
            require(process is not None, f"Input guard timed out for {case}")
            try:
                result = json.loads(process.stdout)
            except ValueError:
                result = {}
            require(result.get("status") not in ("NONE", "FEASIBLE"),
                    f"Unsupported input was assigned a mathematical verdict: {case}")
            require(process.returncode != 0 or result.get("status") == "UNDECIDED",
                    f"Unsupported input silently succeeded: {case}")
            self.stats["guard_cases"] += 1
        # This long known-positive family needs a nontrivial generic prefix.
        limited = self.new((11, "011011", "001001", "000001"), ("--cap", "1"))
        require(limited["status"] == "UNDECIDED", "Tiny state cap must remain UNDECIDED")
        self.stats["guard_cases"] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", required=True)
    parser.add_argument("--old", required=True)
    parser.add_argument("--random", type=int, default=32)
    parser.add_argument("--seed", type=int, default=101)
    parser.add_argument("--timeout", type=float, default=5)
    parser.add_argument("--cap", type=int, default=200000)
    parser.add_argument("--budget-seconds", type=float, default=900)
    parser.add_argument("--quick", action="store_true",
                        help="Use bases2..3/P<=3 only (160 exhaustive cases)")
    args = parser.parse_args()
    require(args.timeout >= 2 and args.cap >= 1 and args.random >= 0 and args.budget_seconds > 0,
            "Invalid regression budget")
    runner = Runner(args)
    summary = {"status": "PASS", "synthetic": synthetic_cycle()}
    try:
        controls = known_cases()
        for case in controls:
            result = runner.new(case)
            require(result["status"] == "FEASIBLE", f"Known positive not accepted: {case}: {result}")
            runner.stats["known_controls"] += 1
        summary["credited_base20_fixture"] = runner.agent116_fixture()
        cases = list(exhaustive_cases())
        require(len(cases) == 2240, "Incorrect exhaustive test-family cardinality")
        if args.quick:
            cases = [case for case in cases if case[0] <= 3 and len(case[1]) <= 3]
        summary["expected_exhaustive_cases"] = len(cases)
        for case in cases:
            runner.compare(case, "exhaustive_cases")
        for case in random_cases(args.random, args.seed):
            runner.compare(case, "random_cases")
        for case in negative_fixtures():
            runner.compare(case, "negative_fixtures", expected_none=True)
        runner.guards()
        if runner.stats["new_undecided"] or runner.stats["old_undecided"]:
            summary["status"] = "PASS_WITH_UNDECIDED_COMPARISONS"
    except TimeoutError as exc:
        summary.update(status="INCOMPLETE", reason=str(exc))
    except TestFailure as exc:
        summary.update(status="FAIL", reason=str(exc))
    summary["checks"] = runner.stats
    summary["undecided_comparisons"] = runner.undecided
    summary["seconds"] = round(time.monotonic() - runner.started, 3)
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 1 if summary["status"] == "FAIL" else 3 if summary["status"] == "INCOMPLETE" else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except TestFailure as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}))
        sys.exit(1)
