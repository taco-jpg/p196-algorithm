#!/usr/bin/env python3
"""Bounded actual-decimal trajectory discovery; no solver answer is a proof.

Each decimal digit is a four-bit variable constrained to 0..9. Column equations
use five bits: both sides are between 0 and 19, so no modular wrap is possible.
The canonical width is explicit at every time, including trailing-zero seeds.
The reversal is a nibble permutation followed by a width-dependent right shift.
Every SAT model is independently checked by Python's ordinary integer arithmetic.
"""
from pathlib import Path
import argparse
import hashlib
import json
import resource
import sys
import time


def direct_orbit(seed, steps):
    result = [seed]
    for _ in range(steps):
        result.append(result[-1] + int(str(result[-1])[::-1]))
    return result


def model(z3, width, steps, prefix, timeout_ms, memory_mb):
    assert width >= 1 and steps >= 0 and width + steps < 64
    assert prefix and prefix.isdecimal() and prefix[0] != "0"
    solver = z3.SolverFor("QF_BV")
    solver.set(timeout=timeout_ms, random_seed=104, threads=1)
    z3.set_param("memory_max_size", memory_mb)
    widths = [z3.BitVec(f"width_{t}", 6) for t in range(steps + 1)]
    digits = [[z3.BitVec(f"d_{t}_{i}", 4) for i in range(width + t)] for t in range(steps + 1)]
    words = []
    reverses = []
    for t, row in enumerate(digits):
        size = len(row)
        word = z3.Concat(*reversed(row)) if size > 1 else row[0]
        full_reverse = z3.Concat(*row) if size > 1 else row[0]
        word_bits = 4 * size
        # The search and controls all have width>=2, hence word_bits>=6.
        assert word_bits >= 6
        shift = z3.ZeroExt(word_bits - 6, z3.BitVecVal(size, 6) - widths[t]) * 4
        reversal = z3.LShR(full_reverse, shift)
        words.append(word)
        reverses.append(reversal)
        solver.add(z3.UGE(widths[t], width), z3.ULE(widths[t], size))
        for i, digit in enumerate(row):
            solver.add(z3.ULE(digit, 9))
            solver.add(z3.Implies(z3.ULE(widths[t], i), digit == 0))
        top_shift = z3.ZeroExt(word_bits - 6, widths[t] - 1) * 4
        solver.add(z3.Extract(3, 0, z3.LShR(word, top_shift)) != 0)
    solver.add(widths[0] == width)
    for t in range(steps):
        size = len(digits[t])
        carries = [z3.BitVec(f"carry_{t}_{i}", 1) for i in range(size + 1)]
        solver.add(carries[0] == 0)
        solver.add(z3.Or(widths[t + 1] == widths[t], widths[t + 1] == widths[t] + 1))
        for i in range(size):
            rev_digit = z3.Extract(4 * i + 3, 4 * i, reverses[t])
            lhs = z3.ZeroExt(1, digits[t][i]) + z3.ZeroExt(1, rev_digit) + z3.ZeroExt(4, carries[i])
            rhs = z3.ZeroExt(1, digits[t + 1][i]) + 10 * z3.ZeroExt(4, carries[i + 1])
            solver.add(lhs == rhs)
        solver.add(digits[t + 1][size] == z3.ZeroExt(3, carries[size]))
    final_bits = words[-1].size()
    solver.add(words[-1] == reverses[-1])
    solver.add(z3.UGE(widths[-1], len(prefix)))
    for j, char in enumerate(prefix):
        shift = z3.ZeroExt(final_bits - 6, widths[-1] - 1 - j) * 4
        solver.add(z3.Extract(3, 0, z3.LShR(words[-1], shift)) == int(char))
    return solver, widths, digits


def run(args, z3):
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    solver, widths, digits = model(z3, args.width, args.steps, args.prefix, args.timeout_ms, args.memory_mb)
    if args.seed is not None:
        expected = direct_orbit(args.seed, args.steps)
        assert len(str(args.seed)) == args.width
        for i, ch in enumerate(reversed(str(args.seed))):
            solver.add(digits[0][i] == int(ch))
        if args.wrong_last is not None:
            solver.add(digits[-1][0] == args.wrong_last)
    query = solver.sexpr() + "\n(check-sat)\n"
    (output / "query.smt2").write_text(query)
    report = {
        "status": "RUNNING",
        "verification_level": "BOUNDED_SOLVER_EXPERIMENT_ONLY",
        "width": args.width, "steps": args.steps, "prefix": args.prefix,
        "solver_timeout_ms": args.timeout_ms, "solver_memory_mb": args.memory_mb,
        "solver_threads": 1, "solver_version": z3.get_full_version(),
        "seed_constraint": args.seed, "wrong_last_control": args.wrong_last,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "query_sha256": hashlib.sha256(query.encode()).hexdigest(),
        "construction_seconds": time.monotonic() - started,
    }
    (output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    answer = solver.check()
    report["status"] = str(answer)
    report["elapsed_seconds"] = time.monotonic() - started
    report["max_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    report["statistics"] = str(solver.statistics())
    if answer == z3.unknown:
        report["reason_unknown"] = solver.reason_unknown()
    if answer == z3.sat:
        assignment = solver.model()
        (output / "model.txt").write_text(str(assignment) + "\n")
        values = []
        width_values = []
        for t, row in enumerate(digits):
            w = assignment.eval(widths[t], model_completion=True).as_long()
            ds = [assignment.eval(d, model_completion=True).as_long() for d in row]
            assert all(0 <= d <= 9 for d in ds)
            value = sum(d * 10 ** i for i, d in enumerate(ds))
            assert len(str(value)) == w
            values.append(value); width_values.append(w)
        actual = direct_orbit(values[0], args.steps)
        assert values == actual, (values, actual)
        last = str(actual[-1])
        assert last == last[::-1] and last.startswith(args.prefix)
        if args.seed is not None:
            assert actual == expected
        report["ordinary_integer_replay"] = "PASS"
        report["orbit"] = [str(n) for n in actual]
        report["canonical_widths"] = width_values
    (output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "statistics"}, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solver-packages", type=Path, required=True)
    ap.add_argument("--width", type=int, required=True)
    ap.add_argument("--steps", type=int, default=12)
    ap.add_argument("--prefix", default="620")
    ap.add_argument("--timeout-ms", type=int, default=15000)
    ap.add_argument("--memory-mb", type=int, default=512)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--wrong-last", type=int)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    sys.path.insert(0, str(args.solver_packages.resolve()))
    import z3
    assert z3.get_full_version() == "4.15.4.0"
    run(args, z3)


if __name__ == "__main__":
    main()
