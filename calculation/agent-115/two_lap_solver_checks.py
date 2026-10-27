#!/usr/bin/env python3
"""Complete small-box equivalence checks against an independent integer oracle.

The production solver is used only through solve().  For every selected
(base, width, period), the oracle first enumerates every exterior start.
Every possible pair of e/g bit strings is then compared with both solver
encodings, with scalar-head pruning enabled and disabled.  SAT witnesses
must belong to the exact oracle solution set.  When a known center fits,
the witness is coupled to that center and the full cycle is checked.

Dependency: z3-solver==5.3.2.0.  Example:
  PYTHONPATH=/tmp/p196-agent115-python python3 -O calculation/agent-115/two_lap_solver_checks.py

An unresolved solver call or exhausted budget exits 2, and a disagreement
exits 1. Neither is reported as UNSAT or as a passing comparison. No assert
statements are used, so python -O does not disable checks.
"""

import argparse
from collections import defaultdict
import importlib.metadata
import itertools
import json
import math
import resource
import sys
import time

import two_lap_oracle as oracle
import two_lap_solver as primary


# All 4**period stream pairs are checked in every listed domain.  Period four
# also exercises a period-two exterior coupled to a period-four known center.
DOMAINS = tuple((2, width, period) for width in (1, 2, 3) for period in (2, 3, 4)) + tuple(
    (3, width, period) for width in (1, 2) for period in (2, 3))
VARIANTS = tuple((encoding, head_prune) for encoding in ("bv", "int")
                 for head_prune in (False, True))


class ComparisonFailure(RuntimeError):
    pass


class UnresolvedComparison(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ComparisonFailure(message)


def oracle_partition(base, width, period):
    """Classify all streams by partitioning the complete oracle solution set."""
    groups = defaultdict(set)
    for phases in oracle.brute_exterior_cycles(base, width, period):
        es, gs = [], []
        for t, B in enumerate(phases):
            step = oracle.exterior_step(base, B)
            require(step is not None, "enumerated oracle cycle has an invalid edge")
            successor, e, g = step
            require(successor == phases[(t + 1) % period], "oracle cycle does not close")
            es.append(str(e))
            gs.append(str(g))
        groups["".join(es), "".join(gs)].add(phases)
    return groups


def audit_witness(base, width, es, gs, result, expected):
    phases = tuple(tuple(row) for row in result.get("B", ()))
    require(len(phases) == len(es), "SAT witness has the wrong number of phases")
    require(all(len(row) == width for row in phases), "SAT witness has the wrong width")
    require(phases in expected, "SAT witness is absent from the complete integer oracle")
    for t, B in enumerate(phases):
        step = oracle.exterior_step(base, B)
        require(step is not None, "SAT witness has an impossible neutral trim")
        successor, e, g = step
        require((e, g) == (int(es[t]), int(gs[t])), "SAT witness has the wrong carry streams")
        require(successor == phases[(t + 1) % len(phases)], "SAT witness has a wrong successor")
    require(result.get("u") == list(map(int, gs)), "SAT witness has the wrong trim stream")
    return phases


def couple_known_center(base, phases, es, gs, controls):
    """Check one complete known-center coupling, including ordinary integers."""
    exterior_period = len(phases)
    for control in controls:
        if control["base"] != base:
            continue
        center_period = control["period"]
        period = math.lcm(exterior_period, center_period)
        for shift in range(center_period):
            if any((int(es[t % exterior_period]), int(gs[t % exterior_period])) !=
                   (control["e"][(t + shift) % center_period],
                    control["g"][(t + shift) % center_period])
                   for t in range(period)):
                continue
            edges = []
            for t in range(period):
                phase = (t + shift) % center_period
                B, C = phases[t % exterior_period], control["C"][phase]
                B2 = phases[(t + 1) % exterior_period]
                C2 = control["C"][(phase + 1) % center_period]
                edges.append((B, C, B2, C2, int(gs[t % exterior_period]), control["v"][phase]))
                oracle.integer_transition_fixture(base, B, C)
            oracle.check_cycle(base, edges)
            return period
    return 0


def run(seconds):
    started = time.perf_counter()
    deadline = started + seconds
    version = importlib.metadata.version("z3-solver")
    require(version == "5.3.2.0", f"expected z3-solver 5.3.2.0, found {version}")
    controls = oracle.known_controls()
    totals = {"complete_domains": 0, "stream_pairs": 0, "solver_calls": 0,
              "oracle_SAT_pairs": 0, "oracle_UNSAT_pairs": 0,
              "solver_SAT": 0, "solver_UNSAT": 0,
              "independent_exterior_edges": 0, "known_center_cycles": 0,
              "known_center_edges": 0}
    records = []
    for base, width, period in DOMAINS:
        partition = oracle_partition(base, width, period)
        record = {"base": base, "width": width, "period": period,
                  "stream_pairs": 4 ** period, "oracle_SAT_pairs": len(partition),
                  "oracle_UNSAT_pairs": 4 ** period - len(partition),
                  "oracle_solutions": sum(map(len, partition.values())),
                  "solver_calls": 0, "solver_SAT": 0, "solver_UNSAT": 0}
        for bits in itertools.product("01", repeat=2 * period):
            es, gs = "".join(bits[:period]), "".join(bits[period:])
            expected = partition.get((es, gs), set())
            expected_status = "SAT" if expected else "UNSAT"
            for encoding, head_prune in VARIANTS:
                remaining = deadline - time.perf_counter()
                if remaining <= 0:
                    raise UnresolvedComparison(f"total budget expired after {totals['solver_calls']} solver calls")
                label = f"base={base} width={width} period={period} e={es} g={gs} {encoding=} {head_prune=}"
                result = primary.solve(base, width, es, gs, min(2.0, remaining),
                                       encoding, head_prune=head_prune)
                totals["solver_calls"] += 1
                record["solver_calls"] += 1
                status = result.get("status")
                if status not in ("SAT", "UNSAT"):
                    raise UnresolvedComparison(f"{label}: {status}: {result.get('reason', 'no reason')}")
                require(status == expected_status,
                        f"{label}: solver={status}, complete oracle={expected_status}")
                totals["solver_" + status] += 1
                record["solver_" + status] += 1
                if status == "SAT":
                    phases = audit_witness(base, width, es, gs, result, expected)
                    totals["independent_exterior_edges"] += period
                    center_edges = couple_known_center(base, phases, es, gs, controls)
                    if center_edges:
                        totals["known_center_cycles"] += 1
                        totals["known_center_edges"] += center_edges
                    # Every SAT case in these selected domains is base two,
                    # where the repository supplies a matching known center.
                    require(center_edges > 0, f"{label}: no known center coupling was checked")
        require(record["solver_calls"] == len(VARIANTS) * 4 ** period,
                "a selected domain was not completely checked")
        totals["complete_domains"] += 1
        totals["stream_pairs"] += 4 ** period
        totals["oracle_SAT_pairs"] += record["oracle_SAT_pairs"]
        totals["oracle_UNSAT_pairs"] += record["oracle_UNSAT_pairs"]
        records.append(record)
        print(json.dumps({"domain": record, "status": "DOMAIN_PASS"}, sort_keys=True), flush=True)
    require(totals["complete_domains"] == len(DOMAINS), "not every selected domain finished")
    require(totals["solver_calls"] == 4 * totals["stream_pairs"], "missing solver variants")
    return {"status": "PASS", "classification": "COMPUTED",
            "dependency": "z3-solver==" + version,
            "variants": [{"encoding": e, "head_pruning": h} for e, h in VARIANTS],
            "domains": records, **totals,
            "wall_seconds": round(time.perf_counter() - started, 6),
            "max_rss_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                           // (1024 if sys.platform == "darwin" else 1),
            "scope": "Complete equivalence in the listed finite boxes only; no decimal target widths are searched."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=58.0,
                        help="total comparison budget, positive and at most 60 seconds")
    args = parser.parse_args()
    if not math.isfinite(args.seconds) or not 0 < args.seconds <= 60:
        parser.error("--seconds must be positive, finite, and at most 60")
    try:
        print(json.dumps(run(args.seconds), sort_keys=True))
        return 0
    except (UnresolvedComparison, MemoryError, importlib.metadata.PackageNotFoundError) as exc:
        print(json.dumps({"status": "UNRESOLVED_COMPARISON", "reason": str(exc)}, sort_keys=True))
        return 2
    except (ComparisonFailure, ValueError, RuntimeError, ImportError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    sys.exit(main())
