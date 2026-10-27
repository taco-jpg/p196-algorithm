#!/usr/bin/env python3
"""Independent finite-width integer model for the Agent 118 center experiment.

This model imports neither the MDD nor cauto transition tables.  It states the
coefficient, ordinary digit, and carry equations directly.  HiGHS infeasibility
is a numerical secondary check, not the foundation of an exact negative proof.
Use CODEX_PRIMARY_RUNTIME_PYTHON when scipy is absent from the default Python.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import warnings


def parameters(args):
    if args.control:
        return 26, "0101", "0101", "0001", 4
    return args.base, args.e, args.g, args.v, args.width


def make_model(base, es, gs, vs, initial_width):
    """Return exact integer equality rows and independent variable bounds."""
    if not (2 <= base <= 62 and len(es) == len(gs) == len(vs) > 0
            and set(es + gs + vs) <= {"0", "1"} and initial_width >= 1):
        raise ValueError("invalid base, streams, or initial width")
    e, g, v = [list(map(int, stream)) for stream in (es, gs, vs)]
    period = len(e)
    lengths = [initial_width]
    for overflow, trim in zip(g, v):
        lengths.append(lengths[-1] + overflow - 2 * trim)
    if lengths[-1] != initial_width or min(lengths) < 1:
        raise ValueError("invalid cyclic center length schedule")
    lengths.pop()
    lower, upper, rows, rhs = [], [], [], []

    def variable(lo, hi):
        index = len(lower)
        lower.append(lo); upper.append(hi)
        return index

    # Sharing mirrored coefficient variables states C_t[j] = C_t[m_t-1-j].
    half = [[variable(0, 2 * base - 2) for _ in range((width + 1) // 2)]
            for width in lengths]
    digits = [[variable(0, base - 1) for _ in range(width)] for width in lengths]
    carries = [[None] + [variable(0, 1) for _ in range(width - 1)] + [None]
               for width in lengths]

    def coefficient(t, j):
        return half[t][min(j, lengths[t] - 1 - j)]

    def add(row, index, multiplier):
        row[index] = row.get(index, 0) + multiplier
        if row[index] == 0:
            del row[index]

    def equation(row, value):
        rows.append(row); rhs.append(value)

    for t, width in enumerate(lengths):
        for j in range(width):
            # C[j] + a[j] - base*a[j+1] = D[j], with forced endpoint bits.
            row = {}; constant = 0
            add(row, coefficient(t, j), 1)
            add(row, digits[t][j], -1)
            if j == 0:
                constant += e[t]
            else:
                add(row, carries[t][j], 1)
            if j + 1 == width:
                constant -= base * (1 - e[t])
            else:
                add(row, carries[t][j + 1], -base)
            equation(row, -constant)

        raw_width = width + g[t]
        successor = (t + 1) % period
        for j in range(raw_width):
            # W = D when g=0; W = D ++ [(base-1)*e] when g=1.
            # The raw pair coefficient is W[j] + W[raw_width-1-j].
            row = {}; constant = 0
            for position in (j, raw_width - 1 - j):
                if position < width:
                    add(row, digits[t][position], 1)
                else:
                    constant += (base - 1) * e[t]
            if j < v[t] or j >= raw_width - v[t]:
                equation(row, base - 1 - constant)
            else:
                add(row, coefficient(successor, j - v[t]), -1)
                equation(row, -constant)
    return lengths, half, lower, upper, rows, rhs


def exact_replay(base, es, gs, vs, lengths, half, vector, lower, upper, rows, rhs):
    """Check the rounded solution using Python integers, including full edges."""
    integers = [round(float(x)) for x in vector]
    if any(abs(float(x) - value) > 1e-6 for x, value in zip(vector, integers)):
        raise RuntimeError("solver output is not sufficiently close to integers")
    if any(not lo <= value <= hi for value, lo, hi in zip(integers, lower, upper)):
        raise RuntimeError("rounded solution violates a variable bound")
    if any(sum(multiplier * integers[index] for index, multiplier in row.items()) != value
           for row, value in zip(rows, rhs)):
        raise RuntimeError("rounded solution violates an exact integer equation")
    centers = [[integers[half[t][min(j, width - 1 - j)]] for j in range(width)]
               for t, width in enumerate(lengths)]
    for t, center in enumerate(centers):
        entering, overflow, trim = int(es[t]), int(gs[t]), int(vs[t])
        integer = sum(c * base**j for j, c in enumerate(center)) + entering
        if integer // base**len(center) != 1 - entering:
            raise RuntimeError("integer center replay has an incorrect exit carry")
        word = []
        for _ in center:
            integer, digit = divmod(integer, base)
            word.append(digit)
        if overflow:
            word.append((base - 1) * entering)
        raw = [a + b for a, b in zip(word, reversed(word))]
        target = ([base - 1] * trim + centers[(t + 1) % len(centers)]
                  + [base - 1] * trim)
        if raw != target:
            raise RuntimeError("integer center replay has an incorrect target")
    return centers


def solve(args):
    import numpy as np
    import scipy
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_array

    base, e, g, v, width = parameters(args)
    lengths, half, lower, upper, rows, rhs = make_model(base, e, g, v, width)
    row_ids, column_ids, coefficients = [], [], []
    for i, row in enumerate(rows):
        for column, coefficient in row.items():
            row_ids.append(i); column_ids.append(column); coefficients.append(coefficient)
    matrix = coo_array((np.asarray(coefficients, dtype=float),
                        (np.asarray(row_ids, dtype=np.int32),
                         np.asarray(column_ids, dtype=np.int32))),
                       shape=(len(rows), len(lower))).tocsc()
    right = np.asarray(rhs, dtype=float)
    result = {"base": base, "period": len(e), "e": e, "g": g, "v": v,
              "initial_width": width, "max_phase_width": max(lengths),
              "variables": len(lower), "equalities": len(rows),
              "nonzero_coefficients": len(coefficients), "scipy_version": scipy.__version__,
              "solver_time_limit_seconds": args.seconds,
              "scope": "fixed initial width only; numerical secondary cross-check"}
    start = time.monotonic()
    with warnings.catch_warnings(record=True) as caught:
        # SciPy passes the HiGHS thread option through to its backend.
        answer = milp(np.zeros(len(lower)), integrality=np.ones(len(lower)),
                      bounds=Bounds(lower, upper),
                      constraints=LinearConstraint(matrix, right, right),
                      options={"time_limit": args.seconds, "mip_rel_gap": 0.0,
                               "presolve": True, "disp": False, "threads": 1})
    result.update(solver_status=int(answer.status), solver_message=str(answer.message),
                  wall_seconds=round(time.monotonic() - start, 6),
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  warnings=[str(item.message) for item in caught])
    if answer.status == 2:
        result["status"] = "NUMERICAL_INFEASIBLE"
    elif answer.status == 0 and answer.x is not None:
        result["centers"] = exact_replay(base, e, g, v, lengths, half, answer.x,
                                          lower, upper, rows, rhs)
        result.update(status="FEASIBLE", exact_integer_replay=True)
    else:
        result["status"] = "UNDECIDED"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=int, default=10)
    parser.add_argument("--e", default="101010010101" * 4)
    parser.add_argument("--g", default="100010001000" * 4)
    parser.add_argument("--v", default="00001000" * 6)
    parser.add_argument("--width", type=int, default=13)
    parser.add_argument("--control", action="store_true", help="known base26 four-phase positive")
    parser.add_argument("--seconds", type=float, default=120)
    parser.add_argument("--memory-gib", type=int, default=3)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not (0 < args.seconds <= 120 and 1 <= args.memory_gib <= 3):
        parser.error("per-case limits must be <=120 solver seconds and <=3 GiB")
    if args.worker:
        try:
            result = solve(args)
        except Exception as error:
            result = {"status": "UNDECIDED", "reason": type(error).__name__, "message": str(error)}
        print(json.dumps(result, sort_keys=True))
        return 2 if result["status"] == "UNDECIDED" else 0

    def limits():
        memory = args.memory_gib * 1024**3
        resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
        cpu = int(args.seconds) + 10
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))

    environment = dict(os.environ)
    environment["OPENBLAS_NUM_THREADS"] = "1"
    environment["OMP_NUM_THREADS"] = "1"
    command = [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:], "--worker"]
    try:
        process = subprocess.run(command, text=True, capture_output=True, env=environment,
                                 timeout=args.seconds + 15, preexec_fn=limits, check=False)
    except subprocess.TimeoutExpired:
        print(json.dumps({"status": "UNDECIDED", "reason": "WALL_TIMEOUT"}, sort_keys=True))
        return 2
    try:
        payload = json.loads(process.stdout)
    except (ValueError, TypeError):
        payload = None
    if (isinstance(payload, dict)
            and payload.get("status") in {"FEASIBLE", "NUMERICAL_INFEASIBLE", "UNDECIDED"}
            and process.returncode == (2 if payload["status"] == "UNDECIDED" else 0)):
        print(process.stdout, end="")
        return process.returncode
    if process.returncode != 0 or payload is None:
        print(json.dumps({"status": "UNDECIDED", "reason": "WORKER_FAILURE",
                          "returncode": process.returncode, "stdout": process.stdout,
                          "stderr": process.stderr}, sort_keys=True))
        return 2
    print(json.dumps({"status": "UNDECIDED", "reason": "UNRECOGNIZED_WORKER_RESULT"}, sort_keys=True))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
