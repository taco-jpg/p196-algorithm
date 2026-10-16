"""Exact bounded finite-center cycles for the periodic 936 carry domain.

This is a center-gluing search only. It neither supplies an exterior nor
asserts existence of a finite Lychrel integer. A SAT output is rechecked as
an exact periodic-tail/finite-patch identity by a separate evaluator.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time

import z3 as z

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "main_existence_attempt" / "morphic_return"))
from resume_renewal_bulk import transform
from domain_front import Domain


def write(path, data):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2) + "\n")
    temp.replace(path)


def left_carry(at, i):
    j = i - 1
    while at(j) == 9:
        j -= 1
    return int(at(j) >= 10)


def right_carry(at, i):
    j = i + 1
    while at(j) == 9:
        j += 1
    return int(at(j) >= 10)


def independent_step_value(domain, h, i):
    lo = (domain.at(i) + left_carry(domain.at, i)) % 10
    j = i - h
    hi = (domain.at(j) + right_carry(domain.at, j)) % 10
    return lo + hi


def audit_front():
    source = ROOT / "main_existence_attempt/morphic_return/front_525_to_936.json"
    raw = source.read_bytes()
    record = json.loads(raw)
    trace = [Domain(tuple(v["left"]), tuple(v["right"]), v["start"], tuple(v["patch"]))
             for v in record["trace"]]
    checked = 0
    for t, (old, new) in enumerate(zip(trace, trace[1:])):
        h = record["clock"][t]
        # Outside this interval both sides are periodic, and carries reset
        # at the nearest non-nine within one period. Checking three tail
        # residues plus the complete defect interval therefore covers Z.
        lo = min(old.start, new.start) - 8
        hi = max(old.end, new.end) + 8
        for i in range(lo, hi):
            assert new.at(i) == independent_step_value(old, h, i), (t, i)
            checked += 1
        assert all(x != 9 for x in old.left) or any(x != 9 for x in old.left)
        assert any(x != 9 for x in old.right)
    assert trace[4].same(trace[0].shifted(1))
    assert trace[24].same(trace[0].shifted(6))
    result = dict(status="independently_checked_exact_local_identity",
                  source=str(source), sha256=hashlib.sha256(raw).hexdigest(),
                  four_step_shift=1, twenty_four_step_shift=6,
                  clock=[0, 1, 0, 1], checked_local_positions=checked,
                  carry_method="nearest_non_nine_reset_in_each_direction",
                  finite_center_supplied=False, finite_exterior_supplied=False,
                  finite_lychrel_witness_proved=False)
    write(HERE / "front_identity_audit.json", result)
    return result


def center_orbit(blocks=100):
    row = Domain((9, 3, 6), (6, 3, 9), 0, ())
    seen = {}
    trace = []
    cycle = None
    for k in range(blocks + 1):
        key = (row.start, row.patch)
        if key in seen:
            cycle = dict(start=seen[key], period=k - seen[key])
            break
        seen[key] = k
        trace.append(dict(four_step_blocks=k, start=row.start, width=len(row.patch),
                          patch=list(row.patch) if k <= 6 else None))
        for h in (0, 1, 0, 1):
            row = row.step(h)
        row = row.shifted(-1)
    result = dict(scope="finite deterministic center orbit check; no growth theorem",
                  initial_left=[9, 3, 6], initial_right=[6, 3, 9], initial_patch=[],
                  center_axis_numerator=-1, normalized_four_step_blocks=blocks,
                  cycle=cycle, trace=trace, finite_lychrel_witness_proved=False)
    write(HERE / "empty_center_orbit.json", result)
    return result


def solve(width, phase, odd, period, seconds):
    assert width >= 0 and phase in range(3) and odd in (0, 1)
    assert period > 0 and period % 4 == 0
    started = time.monotonic()
    solver = z.SolverFor("QF_BV")
    bv = lambda n: z.BitVecVal(n, 5)
    bit = lambda p: z.If(p, bv(1), bv(0))
    bulk0 = tuple((9, 3, 6)[(i + phase) % 3] for i in range(3))
    bulks = [bulk0]
    middle = [0]
    parity = [odd]
    for t in range(period):
        h = t % 2
        bulks.append(transform(bulks[-1], h))
        middle.append(middle[-1] + (h and parity[-1]))
        parity.append(parity[-1] ^ h)
    assert parity[-1] == odd
    shift = middle[-1]
    assert all(bulks[-1][i] == bulk0[(i - shift) % 3] for i in range(3))

    rows = [[z.BitVec(f"q_{t}_{j}", 5) for j in range(width)] for t in range(period)]
    centers = [z.BitVec(f"center_{t}", 5) if parity[t] else None for t in range(period)]
    for t in range(period):
        for q in rows[t]:
            solver.add(z.ULE(q, bv(18)))
        if centers[t] is not None:
            solver.add(z.ULE(centers[t], bv(18)), centers[t] & bv(1) == bv(0))

    for t in range(period):
        h = t % 2
        following = (t + 1) % period
        bulk = bulks[t]
        cut = middle[t] - width - 3
        at = lambda i, bulk=bulk: bulk[i % 3]
        qin = [bv(at(cut + j)) for j in range(3)] + rows[t]
        a = z.BoolVal(left_carry(at, cut))
        # Backward carry b_i is the outgoing carry of column i when read
        # from the right, hence equals incoming-from-right at column i-1.
        backwards = [z.BoolVal(right_carry(at, cut - 1))]
        backwards += [z.Bool(f"back_{t}_{j}") for j in range(1, len(qin) + 1)]
        previous_hi = bv((at(cut - 1) + right_carry(at, cut - 1)) % 10)
        qout = []
        for j, q in enumerate(qin):
            next_a = z.Bool(f"forward_{t}_{j+1}")
            solver.add(next_a == z.UGE(q + bit(a), bv(10)))
            solver.add(backwards[j] == z.UGE(q + bit(backwards[j+1]), bv(10)))
            lo = q + bit(a) - bv(10) * bit(next_a)
            hi = q + bit(backwards[j+1]) - bv(10) * bit(backwards[j])
            qout.append(lo + (previous_hi if h else hi))
            previous_hi = hi
            a = next_a

        center = centers[t]
        if center is None:
            solver.add(a == backwards[-1])
            output_center = bv(2) * previous_hi if h else None
        else:
            solver.add(backwards[-1] == z.UGE(center + bit(a), bv(10)))
            digit = center + bit(a) - bv(10) * bit(backwards[-1])
            if h:
                qout.append(digit + previous_hi)
                output_center = None
            else:
                output_center = bv(2) * digit

        next_cut = middle[t+1] - width - 3
        assert next_cut - cut in (0, 1)
        next_bulk = bulks[t+1]
        target = [bv(next_bulk[(cut + j) % 3]) for j in range(next_cut - cut)]
        target += [bv(next_bulk[(next_cut + j) % 3]) for j in range(3)]
        target += rows[following]
        assert len(qout) == len(target)
        solver.add(*[x == y for x, y in zip(qout, target)])
        if output_center is None:
            assert centers[following] is None
        else:
            assert centers[following] is not None
            solver.add(output_center == centers[following])

    build_seconds = time.monotonic() - started
    solver.set(timeout=max(1, int(seconds * 1000)))
    solve_start = time.monotonic()
    status = solver.check()
    result = dict(width_in_pairs=width, bulk_phase=phase, odd_center=bool(odd),
                  period=period, shift=shift, clock=[t % 2 for t in range(period)],
                  status=str(status), build_seconds=build_seconds,
                  solver_seconds=time.monotonic() - solve_start,
                  scope="center defects supported in last W pairs at EVERY phase; middle coefficient free/even",
                  finite_lychrel_witness_proved=False)
    if status == z.unknown:
        result["reason"] = solver.reason_unknown()
    elif status == z.sat:
        model = solver.model()
        values = [model.eval(q).as_long() for q in rows[0]]
        cv = None if centers[0] is None else model.eval(centers[0]).as_long()
        patch = values + ([] if cv is None else [cv]) + values[::-1]
        axis = odd - 1
        right = tuple(bulk0[(axis - i) % 3] for i in range(3))
        start = Domain(bulk0, right, -width, tuple(patch)).trim()
        current = start
        trace = [current.serial()]
        for t in range(period):
            next_row = current.step(t % 2)
            for i in range(min(current.start, next_row.start)-8,
                           max(current.end, next_row.end)+8):
                assert next_row.at(i) == independent_step_value(current, t % 2, i)
            current = next_row
            trace.append(current.serial())
        assert current.same(start.shifted(shift)), (result, start, current)
        result.update(status="exact_center_cycle_verified", initial=start.serial(),
                      trace=trace, independent_local_verification=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=8)
    parser.add_argument("--period", type=int, default=24)
    parser.add_argument("--seconds", type=float, default=10)
    parser.add_argument("--phase", type=int)
    parser.add_argument("--odd", type=int, choices=[0, 1])
    args = parser.parse_args()
    HERE.mkdir(parents=True, exist_ok=True)
    print(json.dumps(audit_front()), flush=True)
    center_orbit()
    records = []
    for phase in range(3) if args.phase is None else [args.phase]:
        for odd in range(2) if args.odd is None else [args.odd]:
            result = solve(args.width, phase, odd, args.period, args.seconds)
            records.append(result)
            write(HERE / f"centers_period{args.period}_width{args.width}.json", records)
            print(json.dumps({k:v for k,v in result.items() if k != "trace"}), flush=True)
