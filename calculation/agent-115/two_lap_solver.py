#!/usr/bin/env python3
"""Exact fixed-stream, common-width exterior B-cycle SMT search.

Primary task: P=48, e=(010100110100101011001011)^2,
g=(110001001000110001001000)^2, original phase widths at most W,
represented at common padded width W.
Only the full P-step return is imposed; a P/2-step return is NOT imposed.

For forward carries f and reverse-aligned carries r, the exact equations are
  B[t,j]+f[t,j]   = D[t,j]+b*f[t,j+1],
  B[t,j]+r[t,j+1] = R[t,j]+b*r[t,j].
Endpoints: f[0]=0,f[W]=e,r[W]=1-e,r[0]=g. All carries are binary,
digits 0..b-1, coefficients 0..2b-2, and every padded B head is positive.
For g=0 the successor is D[j]+R[j]. For g=1 it is D[0]+1 at j=0,
then D[j]+R[j-1]; the trimmed final symbol enforces R[W-1]=(b-1)*e.

Neutral suffix padding commutes with nextB and preserves both streams.
Padding every phase to common width W converts arbitrary nonnegative trims
to u_t=g_t. Thus fixed-W feasibility covers cycles whose EVERY original
exterior width is <=W. Empty original B phases pad to nonempty neutral rows.
W=0 cannot support a closed exterior cycle and is handled separately.

The QF_BV encoding uses enough unsigned bits for 2b-1. Given explicit
coefficient/digit bounds, no arithmetic expression can wrap. The optional
QF_LIA encoding gives a second exact arithmetic representation of this model.
Encoding bv uses SolverFor("QF_BV"); bv-direct uses the same constraints
with exactly Then("simplify", "bit-blast", "sat").solver(). The latter
converts bounded bit-vector arithmetic to propositional SAT, retaining Z3's
model converters. Encoding int uses SolverFor("QF_LIA"). All are derived
directly from unchanged neutral_band_search.py/A120.
Prior art: calculation/neutral_band/structure/bcp.py already supplies a
generic CP-SAT B-cycle formulation; this file does not claim that idea as new.

Every SAT witness is checked by ordinary integer arithmetic and replayed
through the unchanged Python mirror before it is emitted. UNSAT is a
COMPUTED bounded solver result, not Lean verification. Timeout, solver
unknown, memory failure, unavailable dependency, or failed witness replay
never becomes UNSAT. The exterior alone is not a complete certificate.

Dependency pin: z3-solver==5.3.2.0. Commands from the repository root:
  PYTHONPATH=/tmp/p196-agent115-python python3 calculation/agent-115/two_lap_solver.py selftest --encoding bv-direct --seconds 60 --memory-mib 3072
  PYTHONPATH=/tmp/p196-agent115-python python3 -O calculation/agent-115/two_lap_solver.py selftest --encoding bv-direct --no-head-prune --seconds 60 --memory-mib 3072
  PYTHONPATH=/tmp/p196-agent115-python python3 calculation/agent-115/two_lap_solver.py solve --width 8 --encoding bv-direct --seconds 120 --memory-mib 3072

Selftest checks eight pinned known certificates, including full center
coupling and cycleOK; one unconstrained tiny positive; and target widths
1, 2, 4. Explicit require checks remain active under python -O.
The CLI disables Z3 parallel solving, caps address space at --memory-mib,
and sets Z3's memory cap 512 MiB below that limit. The --seconds budget
covers model construction and the subsequent solver timeout; it is not an
external process wall timer. No solve may request over 1200 seconds or
8192 MiB. The JSON reports elapsed construction/search time and peak RSS.
"""

from __future__ import annotations

import argparse
from collections import deque
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import resource
import sys
import time


E24 = "010100110100101011001011"
G24 = "110001001000110001001000"
ROOT = Path(__file__).resolve().parents[2]
MIRROR_PATH = ROOT / "calculation" / "neutral_band_search.py"


class WitnessError(RuntimeError):
    pass


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise WitnessError(reason)


def load_mirror():
    spec = importlib.util.spec_from_file_location("a115_unchanged_mirror", MIRROR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unchanged mirror unavailable")
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    return mirror


def norm_by_integer(base: int, coefficients: list[int], carry: int):
    """Independent positional arithmetic; no column-carry loop is imported."""
    value = carry + sum(x * base**i for i, x in enumerate(coefficients))
    digits = []
    for _ in coefficients:
        value, digit = divmod(value, base)
        digits.append(digit)
    return digits, value


def audit_exterior(base: int, phases: list[list[int]], e: str, g: str) -> dict:
    mirror = load_mirror()
    period = len(e)
    require(period > 0 and len(g) == period and len(phases) == period, "wrong phase count")
    width = len(phases[0])
    require(width > 0, "empty common width cannot close")
    for t, row in enumerate(phases):
        require(len(row) == width and row[0] > 0, f"invalid width/head at phase {t}")
        require(all(isinstance(x, int) and 0 <= x <= 2 * base - 2 for x in row),
                f"invalid coefficient at phase {t}")
        et, gt = int(e[t]), int(g[t])
        forward, e_actual = norm_by_integer(base, row, 0)
        reverse_digits, g_actual = norm_by_integer(base, row[::-1], 1 - et)
        require(e_actual == et and g_actual == gt, f"integer carry stream mismatch at {t}")
        if gt:
            raw = [a + b for a, b in zip(forward + [(base - 1) * (1 - et)],
                                          [1] + reverse_digits[::-1])]
        else:
            raw = [a + b for a, b in zip(forward, reverse_digits[::-1])]
        target = phases[(t + 1) % period] + [base - 1] * gt
        require(raw == target, f"integer exterior edge mismatch at {t}")
        # This one-symbol center forces the required complement carry. It
        # is only a one-edge oracle, not a claimed center cycle.
        center = [0] if et else [2 * base - 2]
        require(mirror.e1(base, row) == et, f"mirror e mismatch at {t}")
        require(mirror.e2(base, row, center) == 1 - et, f"mirror complement mismatch at {t}")
        require(mirror.gam(base, row, center) == gt, f"mirror g mismatch at {t}")
        require(mirror.nextB(base, row, center) == target, f"mirror B-edge mismatch at {t}")
    return {"integer_edges_checked": period, "mirror_edges_checked": period,
            "all_widths": width, "sum_u": g.count("1"),
            "full_period_return": True,
            "half_period_return": period % 2 == 0 and all(
                phases[t] == phases[t + period // 2] for t in range(period // 2))}


def head_cycle_support(base: int, g: str):
    """Sound phase/head projection, crediting Agent 4's scalar-head method.

    At coefficient zero the forward entering carry is zero. Guess only
    the reverse entering carry h, require floor((x+h)/b)=g, and compute
    the next first coefficient directly from the A120 equations. Sink
    peeling removes no directed cycle; retained nodes can overapproximate
    cycle membership. This does not identify any OTHER B coefficients.
    """
    span = 2 * base - 2
    period = len(g)
    successors = [set() for _ in range(period * span)]
    predecessors = [[] for _ in successors]
    for t, bit in enumerate(g):
        gt = int(bit)
        for x in range(1, span + 1):
            source = t * span + x - 1
            for h in (0, 1):
                if (x + h) // base != gt:
                    continue
                y = x % base + (1 if gt else (x + h) % base)
                if 1 <= y <= span:
                    successors[source].add(((t + 1) % period) * span + y - 1)
            for target in successors[source]:
                predecessors[target].append(source)
    degree = [len(row) for row in successors]
    queue = deque(i for i, count in enumerate(degree) if count == 0)
    removed = [False] * len(successors)
    while queue:
        target = queue.popleft()
        if removed[target]:
            continue
        removed[target] = True
        for source in predecessors[target]:
            degree[source] -= 1
            if degree[source] == 0:
                queue.append(source)
    return [[x for x in range(1, span + 1) if not removed[t * span + x - 1]]
            for t in range(period)]


def build_model(z3, base: int, width: int, e: str, g: str, encoding: str, head_prune: bool = True):
    period = len(e)
    bit_width = (2 * base - 1).bit_length()
    is_bv = encoding in ("bv", "bv-direct")
    if encoding == "bv-direct":
        # Explicit equisatisfiable BV-to-SAT pipeline. Constraints below
        # are identical to bv, and model conversion recovers their B rows.
        solver = z3.Then("simplify", "bit-blast", "sat").solver()
    else:
        solver = z3.SolverFor("QF_BV" if is_bv else "QF_LIA")
    if is_bv:
        variable = lambda name: z3.BitVec(name, bit_width)
        constant = lambda value: z3.BitVecVal(value, bit_width)
        bound = lambda value, upper: z3.ULE(value, constant(upper))
        carry = lambda name: z3.Bool(name)
        carry_value = lambda value: z3.If(value, constant(1), constant(0))
        carry_times_base = lambda value: z3.If(value, constant(base), constant(0))
        carry_constant = lambda value: z3.BoolVal(bool(value))
    else:
        variable = z3.Int
        constant = lambda value: z3.IntVal(value)
        bound = lambda value, upper: z3.And(0 <= value, value <= upper)
        carry = z3.Int
        carry_value = lambda value: value
        carry_times_base = lambda value: base * value
        carry_constant = lambda value: z3.IntVal(value)

    B = [[variable(f"B_{t}_{j}") for j in range(width)] for t in range(period)]
    D = [[variable(f"D_{t}_{j}") for j in range(width)] for t in range(period)]
    R = [[variable(f"R_{t}_{j}") for j in range(width)] for t in range(period)]
    head_support = head_cycle_support(base, g) if head_prune else None
    for t in range(period):
        et, gt = int(e[t]), int(g[t])
        f = [carry_constant(0)] + [carry(f"f_{t}_{j}") for j in range(1, width)] + [carry_constant(et)]
        r = [carry_constant(gt)] + [carry(f"r_{t}_{j}") for j in range(1, width)] + [carry_constant(1 - et)]
        if not is_bv:
            for value in f[1:-1] + r[1:-1]:
                solver.add(0 <= value, value <= 1)
        solver.add(B[t][0] != constant(0))
        if head_support is not None:
            solver.add(z3.Or([B[t][0] == constant(x) for x in head_support[t]]))
        for j in range(width):
            solver.add(bound(B[t][j], 2 * base - 2), bound(D[t][j], base - 1), bound(R[t][j], base - 1))
            solver.add(B[t][j] + carry_value(f[j]) == D[t][j] + carry_times_base(f[j + 1]))
            solver.add(B[t][j] + carry_value(r[j + 1]) == R[t][j] + carry_times_base(r[j]))
            nxt = B[(t + 1) % period][j]
            if gt:
                solver.add(nxt == D[t][j] + (constant(1) if j == 0 else R[t][j - 1]))
            else:
                solver.add(nxt == D[t][j] + R[t][j])
        if gt:
            solver.add(R[t][width - 1] == constant((base - 1) * et))
    return solver, B, {"encoding": "QF_BV_DIRECT" if encoding == "bv-direct" else ("QF_BV" if is_bv else "QF_LIA"), "bit_width": bit_width if is_bv else None,
                       "assertions": len(solver.assertions()),
                       "coefficient_digit_variables": 3 * period * width,
                       "internal_carry_variables": 2 * period * (width - 1),
                       "head_pruning": head_prune,
                       "head_support_sizes": [len(row) for row in head_support] if head_support is not None else None,
                       "unique_head_word": [row[0] for row in head_support] if head_support is not None and all(len(row) == 1 for row in head_support) else None}


def solve(base: int, width: int, e: str, g: str, seconds: float, encoding: str = "bv", pinned_B=None, head_prune: bool = True) -> dict:
    started = time.monotonic()
    common = {"base": base, "width": width, "period": len(e), "e": e, "g": g,
              "sum_g": g.count("1"), "pinned_B": pinned_B is not None,
              "scope": "all phases have a common padded exterior width W; only full-P return required"}
    if width == 0:
        return dict(common, status="UNSAT", reason="Empty B emits [base], which cannot equal a neutral suffix or return to empty B.",
                    classification="PAPER PROOF")
    try:
        import z3
    except ImportError:
        return dict(common, status="UNDECIDED", reason="z3-solver unavailable; install pinned version 5.3.2.0")
    try:
        solver, B, details = build_model(z3, base, width, e, g, encoding, head_prune)
        if pinned_B is not None:
            audit_exterior(base, pinned_B, e, g)
            for row, expected in zip(B, pinned_B):
                for coefficient, value in zip(row, expected):
                    solver.add(coefficient == value)
        remaining = seconds - (time.monotonic() - started)
        if remaining <= 0:
            return dict(common, status="UNDECIDED", reason="time budget expired while constructing model")
        solver.set(timeout=max(1, int(remaining * 1000)), random_seed=0)
        verdict = solver.check()
        result = dict(common, solver_version=z3.get_version_string(), **details,
                      classification="COMPUTED", seconds=round(time.monotonic() - started, 6))
        if verdict == z3.unsat:
            return dict(result, status="UNSAT")
        if verdict != z3.sat:
            return dict(result, status="UNDECIDED", reason=solver.reason_unknown())
        model = solver.model()
        phases = [[model.eval(x, model_completion=True).as_long() for x in row] for row in B]
        audit = audit_exterior(base, phases, e, g)
        return dict(result, status="SAT", B=phases, u=[int(bit) for bit in g], replay=audit,
                    warning="Exterior cycle only; must combine with center edges and replay cycleOK before candidate status.")
    except (MemoryError, z3.Z3Exception) as exc:
        return dict(common, status="UNDECIDED", reason=f"solver/resource failure: {exc}",
                    seconds=round(time.monotonic() - started, 6))
    except WitnessError as exc:
        return dict(common, status="UNDECIDED", reason=f"SAT witness failed exact replay: {exc}",
                    seconds=round(time.monotonic() - started, 6))


def selftest(seconds: float, encoding: str = "bv", head_prune: bool = True) -> dict:
    started = time.monotonic()
    mirror = load_mirror()
    known = {base: es for base, es in mirror._lean_certs()}
    results = []
    # Pinning makes these encoder controls, rather than expensive attempts
    # to rediscover known source certificates. Ordinary solve never pins B.
    for base in sorted(known):
        es = known[base]
        width = max(len(edge[0]) for edge in es)
        phases = [edge[0] + [base - 1] * (width - len(edge[0])) for edge in es]
        e = "".join(str(mirror.e1(base, edge[0])) for edge in es)
        g = "".join(str(mirror.gam(base, edge[0], edge[1])) for edge in es)
        audit_exterior(base, phases, e, g)
        remaining = seconds - (time.monotonic() - started)
        if remaining <= 0:
            return {"status": "UNDECIDED", "reason": "selftest total budget expired", "checks": results}
        result = solve(base, width, e, g, remaining, encoding, pinned_B=phases, head_prune=head_prune)
        if result["status"] != "SAT":
            return {"status": "UNDECIDED" if result["status"] == "UNDECIDED" else "FAILED",
                    "reason": "known positive encoder control did not return SAT", "result": result, "checks": results}
        solved = result["B"]
        combined = [(solved[t], es[t][1], solved[(t + 1) % len(es)], es[t][3], int(g[t]), es[t][5])
                    for t in range(len(es))]
        require(mirror.cycleOK(base, combined, combined[0][0], combined[0][1]),
                f"known-base coupled control failed cycleOK at base {base}")
        results.append({"base": base, "width": width, "period": len(e), "e": e, "g": g,
                        "solver_status": "SAT", "pinned_B": True, "integer_and_mirror_B_replay": True,
                        "coupled_known_C_cycleOK": True, "seconds": result["seconds"]})
    remaining = seconds - (time.monotonic() - started)
    if remaining <= 0:
        return {"status": "UNDECIDED", "reason": "selftest total budget expired", "checks": results}
    result = solve(2, 2, "1010", "1010", remaining, encoding, head_prune=head_prune)
    if result["status"] != "SAT":
        return {"status": "UNDECIDED" if result["status"] == "UNDECIDED" else "FAILED",
                "reason": "unconstrained tiny positive search did not return SAT", "result": result, "checks": results}
    results.append({"base": 2, "width": 2, "period": 4, "solver_status": "SAT", "pinned_B": False,
                    "integer_and_mirror_B_replay": True, "seconds": result["seconds"]})
    for width in (1, 2, 4):
        remaining = seconds - (time.monotonic() - started)
        if remaining <= 0:
            return {"status": "UNDECIDED", "reason": "selftest total budget expired", "checks": results}
        result = solve(10, width, E24 * 2, G24 * 2, remaining, encoding, head_prune=head_prune)
        if result["status"] != "UNSAT":
            return {"status": result["status"], "reason": "small-width negative control did not return UNSAT",
                    "result": result, "checks": results}
        results.append({"base": 10, "width": width, "period": 48,
                        "solver_status": "UNSAT", "seconds": result["seconds"]})
    return {"status": "SELFTEST_PASSED", "classification": "COMPUTED", "checks": results,
            "encoding": encoding, "head_pruning": head_prune,
            "seconds": round(time.monotonic() - started, 6)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("selftest", "solve"))
    parser.add_argument("--base", type=int, default=10)
    parser.add_argument("--width", type=int, default=8)
    parser.add_argument("--e", default=E24 * 2)
    parser.add_argument("--g", default=G24 * 2)
    parser.add_argument("--seconds", type=float, default=60.0)
    parser.add_argument("--encoding", choices=("bv", "bv-direct", "int"), default="bv")
    parser.add_argument("--no-head-prune", action="store_true", help="disable the sound redundant first-coefficient cycle projection")
    parser.add_argument("--memory-mib", type=int, default=6144)
    args = parser.parse_args()
    if not 2 <= args.base <= 256 or not 0 <= args.width <= 128:
        parser.error("base must be 2..256 and width 0..128")
    if not args.e or len(args.e) != len(args.g) or any(c not in "01" for c in args.e + args.g):
        parser.error("e and g must be nonempty, equally long binary streams")
    if len(args.e) > 256 or len(args.e) * max(1, args.width) > 8192:
        parser.error("model size guard exceeded")
    if not math.isfinite(args.seconds) or not 0 < args.seconds <= 1200:
        parser.error("seconds must be finite, positive and at most 1200")
    if not 1024 <= args.memory_mib <= 8192:
        parser.error("memory budget must be 1024..8192 MiB")
    requested = args.memory_mib * 1024 * 1024
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    if soft != resource.RLIM_INFINITY:
        requested = min(requested, soft)
    if hard != resource.RLIM_INFINITY:
        requested = min(requested, hard)
    resource.setrlimit(resource.RLIMIT_AS, (requested, hard))
    try:
        import z3
        z3.set_param("memory_max_size", args.memory_mib - 512)
        z3.set_param("parallel.enable", False)
    except ImportError:
        pass
    try:
        result = selftest(args.seconds, args.encoding, not args.no_head_prune) if args.command == "selftest" else solve(
            args.base, args.width, args.e, args.g, args.seconds, args.encoding, head_prune=not args.no_head_prune)
    except (MemoryError, WitnessError) as exc:
        result = {"status": "UNDECIDED", "reason": str(exc) or "memory limit reached"}
    result["mirror_sha256"] = hashlib.sha256(MIRROR_PATH.read_bytes()).hexdigest()
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result["peak_mib"] = round(rss / (1024 * 1024 if sys.platform == "darwin" else 1024), 3)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    return 0 if result["status"] in ("SAT", "UNSAT", "SELFTEST_PASSED") else 2


if __name__ == "__main__":
    raise SystemExit(main())
