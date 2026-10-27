#!/usr/bin/env python3
"""Independent CP-SAT backend for the prescribed two-lap exterior problem.

Uses fresh bounded Int/Bool column constraints, with no SMT encoding import.
Credit: calculation/neutral_band/structure/bcp.py supplies the prior generic
CP-SAT B-cycle model; Agent 4 supplies the scalar-head projection. Only the
optional head-support helper is shared with two_lap_solver.py. Whole-integer
auditing and known source data come from the independent two_lap_oracle.py.

Padding to common width W is exact for cycles with every original B width
at most W. It changes the exterior trims to u=g, preserves both streams,
and allows padded empty phases. Only the full supplied period closes.

Dependency: ortools==9.15.6755. Example commands:
  PYTHONPATH=/tmp/p196-agent115-cpsat python3 calculation/agent-115/two_lap_cp_solver.py selftest --seconds 120
  PYTHONPATH=/tmp/p196-agent115-cpsat python3 calculation/agent-115/two_lap_cp_solver.py solve --width 8 --seconds 120

One solver worker, at most 1200 seconds and 6144 MiB address space. A parent
process enforces the wall deadline and classifies killed/failed workers as
UNDECIDED. Only CP-SAT INFEASIBLE yields computational UNSAT. Target SAT
results include the complete edge list only after independent integer and
unchanged-mirror cycleOK checks. Such a candidate still needs Lean checking.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

import two_lap_oracle as oracle


ROOT = Path(__file__).resolve().parents[2]
MIRROR_PATH = ROOT / "calculation/neutral_band_search.py"
E48 = "010100110100101011001011" * 2
G48 = "110001001000110001001000" * 2
PIN = "9.15.6755"


class CheckFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def load_mirror():
    spec = importlib.util.spec_from_file_location("a115_cp_reference_mirror", MIRROR_PATH)
    require(spec is not None and spec.loader is not None, "unchanged mirror unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit_exterior(base, phases, e, g, mirror):
    period = len(e)
    require(len(g) == period == len(phases) and period > 0, "exterior phase count")
    width = len(phases[0])
    require(width > 0, "empty padded exterior")
    for t, row in enumerate(phases):
        require(len(row) == width and row[0] > 0, "exterior width or head")
        require(all(isinstance(x, int) and 0 <= x <= 2 * base - 2 for x in row),
                "exterior coefficient range")
        successor = phases[(t + 1) % period]
        step = oracle.exterior_step(base, tuple(row))
        require(step is not None, "integer oracle rejects constant-width trim")
        actual, et, gt = step
        require((et, gt) == (int(e[t]), int(g[t])) and actual == tuple(successor),
                "integer oracle rejects exterior edge or streams")
        center = [base] if et == 0 else [0]
        require(mirror.hyp(base, row, center), "one-edge mirror hypothesis")
        require(mirror.e1(base, row) == et and mirror.gam(base, row, center) == gt,
                "mirror exterior stream mismatch")
        require(mirror.nextB(base, row, center) == successor + [base - 1] * gt,
                "mirror exterior edge mismatch")
    return {"integer_edges": period, "mirror_edges": period,
            "full_period_return": True,
            "half_period_return": period % 2 == 0 and all(
                phases[t] == phases[t + period // 2] for t in range(period // 2))}


def couple_and_audit(base, phases, centers, trims, e, g, mirror):
    period = len(phases)
    require(len(centers) == len(trims) == len(e) == len(g) == period,
            "coupled phase count")
    edges = [(row, list(centers[t]), phases[(t + 1) % period],
              list(centers[(t + 1) % period]), int(g[t]), int(trims[t]))
             for t, row in enumerate(phases)]
    es, gs = oracle.check_cycle(base, edges)
    require(es == tuple(map(int, e)) and gs == tuple(map(int, g)),
            "coupled integer streams mismatch")
    for edge in edges:
        oracle.integer_transition_fixture(base, tuple(edge[0]), tuple(edge[1]))
    require(mirror.cycleOK(base, edges, edges[0][0], edges[0][1]),
            "unchanged mirror rejects full coupled cycle")
    return edges


def build_model(cp_model, base, width, e, g, head_prune, pinned=None):
    """Fresh finite-domain formulation; all carry variables are Boolean."""
    period = len(e)
    model = cp_model.CpModel()
    B = [[model.new_int_var(0, 2 * base - 2, f"x_{t}_{j}")
          for j in range(width)] for t in range(period)]
    support = None
    if head_prune:
        # Shared only as a proved redundant projection, not as an encoder.
        from two_lap_solver import head_cycle_support
        support = head_cycle_support(base, g)
    for t in range(period):
        et, gt = int(e[t]), int(g[t])
        digits = [model.new_int_var(0, base - 1, f"d_{t}_{j}") for j in range(width)]
        reverse = [model.new_int_var(0, base - 1, f"q_{t}_{j}") for j in range(width)]
        low = [model.new_bool_var(f"f_{t}_{j}") for j in range(width + 1)]
        high = [model.new_bool_var(f"r_{t}_{j}") for j in range(width + 1)]
        model.add(low[0] == 0)
        model.add(low[width] == et)
        model.add(high[width] == 1 - et)
        model.add(high[0] == gt)
        model.add(B[t][0] >= 1)
        if support is not None:
            model.add_allowed_assignments([B[t][0]], [(x,) for x in support[t]])
        for j in range(width):
            model.add(B[t][j] + low[j] == digits[j] + base * low[j + 1])
            model.add(B[t][j] + high[j + 1] == reverse[j] + base * high[j])
            following = B[(t + 1) % period][j]
            if gt:
                model.add(following == digits[j] + (1 if j == 0 else reverse[j - 1]))
            else:
                model.add(following == digits[j] + reverse[j])
        if gt:
            model.add(reverse[width - 1] == (base - 1) * et)
    if pinned is not None:
        require(len(pinned) == period and all(len(row) == width for row in pinned),
                "pinned dimensions mismatch")
        for row, supplied in zip(B, pinned):
            for variable, value in zip(row, supplied):
                model.add(variable == value)
    problem = model.validate()
    require(not problem, "CP-SAT model validation failed: " + problem)
    return model, B, {"variables": len(model.proto.variables),
                      "constraints": len(model.proto.constraints),
                      "head_pruning": head_prune,
                      "head_support_sizes": [len(row) for row in support] if support is not None else None}


def solve(cp_model, base, width, e, g, deadline, memory_mib, head_prune=True, pinned=None):
    started = time.monotonic()
    common = {"base": base, "width": width, "period": len(e), "e": e, "g": g,
              "sum_g": g.count("1"), "pinned_B": pinned is not None,
              "workers": 1, "classification": "COMPUTED",
              "scope": "all original exterior phase widths at most W; only full-P closure"}
    if width == 0:
        return dict(common, status="UNSAT", classification="PAPER PROOF",
                    reason="Empty B emits [base], which cannot be trimmed to an empty neutral suffix.")
    mirror = load_mirror()
    if pinned is not None:
        audit_exterior(base, pinned, e, g, mirror)
    model, B, details = build_model(cp_model, base, width, e, g, head_prune, pinned)
    # Leave time for witness replay and JSON delivery before the parent's
    # hard wall deadline; a native timeout is still only UNDECIDED.
    remaining = deadline - time.monotonic() - 1.0
    if remaining <= 0:
        return dict(common, status="UNDECIDED", reason="deadline reached during model construction")
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.max_time_in_seconds = remaining
    solver.parameters.max_memory_in_mb = max(128, memory_mib - 256)
    solver.parameters.random_seed = 0
    solver.parameters.log_search_progress = False
    status = solver.solve(model)
    result = dict(common, **details, solver_status=solver.status_name(status),
                  search_budget_seconds=round(remaining, 6),
                  seconds=round(time.monotonic() - started, 6),
                  solver_seconds=round(solver.wall_time, 6),
                  branches=solver.num_branches, conflicts=solver.num_conflicts)
    if status == cp_model.INFEASIBLE:
        return dict(result, status="UNSAT")
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return dict(result, status="UNDECIDED", reason=solver.solution_info())
    phases = [[solver.value(x) for x in row] for row in B]
    replay = audit_exterior(base, phases, e, g, mirror)
    result.update(status="SAT", B=phases, u=list(map(int, g)), replay=replay)
    if base == 10 and e == E48 and g == G48:
        center = oracle.target_center(2)
        edges = couple_and_audit(base, phases, center["C"], center["v"], e, g, mirror)
        result.update(candidate=True, cycleOK10=True, edges=edges,
                      candidate_scope="Python cycleOK candidate; Lean verification remains required")
    else:
        result["candidate"] = False
    return result


def selftest(cp_model, deadline, memory_mib, head_prune):
    checks = []
    mirror = load_mirror()
    for control in oracle.known_controls():
        base, width = control["base"], control["width"]
        e, g = ("".join(map(str, control[key])) for key in ("e", "g"))
        pinned = [list(row) for row in control["B"]]
        result = solve(cp_model, base, width, e, g, deadline, memory_mib, head_prune, pinned)
        if result["status"] != "SAT":
            return {"status": "UNDECIDED" if result["status"] == "UNDECIDED" else "FAILED",
                    "reason": "known pinned positive control did not return SAT", "result": result,
                    "checks": checks}
        couple_and_audit(base, result["B"], control["C"], control["v"], e, g, mirror)
        checks.append({"kind": "pinned source certificate", "base": base, "width": width,
                       "period": len(e), "status": "SAT", "full_cycleOK": True,
                       "seconds": result["seconds"]})
    result = solve(cp_model, 2, 2, "1010", "1010", deadline, memory_mib, head_prune)
    if result["status"] != "SAT":
        return {"status": "UNDECIDED" if result["status"] == "UNDECIDED" else "FAILED",
                "reason": "unconstrained base-2 positive control failed", "result": result,
                "checks": checks}
    checks.append({"kind": "unconstrained positive", "base": 2, "width": 2,
                   "period": 4, "status": "SAT", "seconds": result["seconds"]})
    for base, width, e, g in ((2, 1, "1010", "1010"), (2, 2, "0000", "0000"),
                              (3, 2, "0101", "1010"), (4, 2, "1010", "1010")):
        brute = oracle.brute_exterior_cycles(base, width, len(e), tuple(map(int, e)), tuple(map(int, g)))
        require(not brute, "tiny negative oracle unexpectedly found a cycle")
        result = solve(cp_model, base, width, e, g, deadline, memory_mib, head_prune)
        if result["status"] != "UNSAT":
            return {"status": "UNDECIDED" if result["status"] == "UNDECIDED" else "FAILED",
                    "reason": "tiny exhaustive negative control disagreed", "result": result,
                    "checks": checks}
        checks.append({"kind": "exhaustive negative", "base": base, "width": width,
                       "period": len(e), "status": "UNSAT", "oracle_count": 0,
                       "seconds": result["seconds"]})
    for width in (1, 2, 4):
        result = solve(cp_model, 10, width, E48, G48, deadline, memory_mib, head_prune)
        if result.get("candidate"):
            # An unexpected verified full cycle takes precedence over an
            # assumed negative control; never hide its complete edge list.
            result["selftest_checks_before_candidate"] = checks
            return result
        if result["status"] != "UNSAT":
            return {"status": "UNDECIDED" if result["status"] == "UNDECIDED" else "FAILED",
                    "reason": "tiny target control did not return UNSAT", "result": result,
                    "checks": checks}
        checks.append({"kind": "tiny target comparison", "base": 10, "width": width,
                       "period": 48, "status": "UNSAT", "seconds": result["seconds"]})
    return {"status": "SELFTEST_PASSED", "classification": "COMPUTED",
            "head_pruning": head_prune, "checks": checks}


def worker(options):
    started = time.monotonic()
    deadline = started + options["seconds"]
    requested = options["memory_mib"] * 1024 * 1024
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    finite = [x for x in (requested, soft, hard) if x != resource.RLIM_INFINITY]
    resource.setrlimit(resource.RLIMIT_AS, (min(finite), hard))
    cpu = math.ceil(options["seconds"])
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    finite = [x for x in (cpu, soft, hard) if x != resource.RLIM_INFINITY]
    cap = min(finite)
    resource.setrlimit(resource.RLIMIT_CPU, (cap, cap))
    try:
        import ortools
        from ortools.sat.python import cp_model
        require(ortools.__version__ == PIN, "expected ortools==" + PIN)
        if options["command"] == "selftest":
            result = selftest(cp_model, deadline, options["memory_mib"], not options["no_head_prune"])
        else:
            result = solve(cp_model, options["base"], options["width"], options["e"], options["g"],
                           deadline, options["memory_mib"], not options["no_head_prune"])
        result["solver_version"] = ortools.__version__
    except (ImportError, CheckFailure, MemoryError, RuntimeError, ValueError, OverflowError) as error:
        result = {"status": "UNDECIDED", "reason": type(error).__name__ + ": " + str(error)}
    result["worker_seconds"] = round(time.monotonic() - started, 6)
    result["peak_mib"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss /
                               (1024 * 1024 if sys.platform == "darwin" else 1024), 3)
    result["mirror_sha256"] = hashlib.sha256(MIRROR_PATH.read_bytes()).hexdigest()
    print(json.dumps(result, sort_keys=True), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("selftest", "solve"))
    parser.add_argument("--base", type=int, default=10)
    parser.add_argument("--width", type=int, default=8)
    parser.add_argument("--e", default=E48)
    parser.add_argument("--g", default=G48)
    parser.add_argument("--seconds", type=float, default=120.0)
    parser.add_argument("--memory-mib", type=int, default=6144)
    parser.add_argument("--no-head-prune", action="store_true")
    args = parser.parse_args()
    if not 2 <= args.base <= 256 or not 0 <= args.width <= 128:
        parser.error("base must be 2..256 and width 0..128")
    if not args.e or len(args.e) != len(args.g) or any(x not in "01" for x in args.e + args.g):
        parser.error("e and g must be nonempty equal-length binary streams")
    if len(args.e) > 256 or len(args.e) * max(1, args.width) > 8192:
        parser.error("model size guard exceeded")
    if not math.isfinite(args.seconds) or not 0 < args.seconds <= 1200:
        parser.error("seconds must be finite, positive and at most 1200")
    if not 512 <= args.memory_mib <= 6144:
        parser.error("memory budget must be 512..6144 MiB")
    environment = dict(os.environ)
    for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        environment[name] = "1"
    command = [sys.executable] + (["-O"] if sys.flags.optimize else []) + [str(Path(__file__).resolve()), "--worker"]
    started = time.monotonic()
    try:
        completed = subprocess.run(command, input=json.dumps(vars(args)), capture_output=True,
                                   text=True, timeout=args.seconds, env=environment, check=False)
        if completed.returncode:
            result = {"status": "UNDECIDED", "reason": "worker process failed or reached a resource limit",
                      "worker_returncode": completed.returncode, "worker_stderr": completed.stderr[-1000:]}
        else:
            try:
                result = json.loads(completed.stdout)
            except json.JSONDecodeError:
                result = {"status": "UNDECIDED", "reason": "worker did not return a valid result",
                          "worker_stderr": completed.stderr[-1000:]}
    except subprocess.TimeoutExpired:
        result = {"status": "UNDECIDED", "reason": "parent-enforced wall deadline reached"}
    except OSError as error:
        result = {"status": "UNDECIDED", "reason": "could not start worker: " + str(error)}
    result.setdefault("peak_mib", round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss /
                                        (1024 * 1024 if sys.platform == "darwin" else 1024), 3))
    result["request"] = vars(args)
    result["process_seconds"] = round(time.monotonic() - started, 6)
    result["wall_budget_seconds"] = args.seconds
    result["address_space_limit_mib"] = args.memory_mib
    print(json.dumps(result, sort_keys=True, indent=2), flush=True)
    return 0 if result["status"] in ("SAT", "UNSAT", "SELFTEST_PASSED") else 2


if __name__ == "__main__":
    if sys.argv[1:] == ["--worker"]:
        worker(json.load(sys.stdin))
    else:
        raise SystemExit(main())
