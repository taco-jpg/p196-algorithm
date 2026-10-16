"""Exact free-clock search for decimal reverse-add pumps with period-three bulk.

State t has k-digit high/low caps A_t,B_t and core length M=3m+r_t.
Core digits, from least significant upwards, are U_t[j mod 3].
The model requires a spatially periodic carry sequence in the core, so it
describes every m >= 1, not merely one finite tested length. A temporal loop
with positive growth is a Lychrel certificate when every phase is nonpalindromic.
UNSAT is scoped to the given period, cap width, growth and residue.
"""
import argparse
from functools import lru_cache
import json
import time
from pathlib import Path

import z3


def solve(period, width, growth, residue=0, seconds=20, base=10,
          rotate_after_overflow=False, bulk_start_filter=False, cnf_path=None):
    assert 0 < growth <= period and growth % 3 == 0
    assert residue in range(3)
    assert base in (2, 10)
    start = time.monotonic()
    s = z3.SolverFor("QF_BV")
    s.set(timeout=round(1000 * seconds))
    p, k = period, width
    A = [[z3.BitVec(f'a_{t}_{i}', 5) for i in range(k)] for t in range(p)]
    B = [[z3.BitVec(f'b_{t}_{i}', 5) for i in range(k)] for t in range(p)]
    U = [[z3.BitVec(f'u_{t}_{i}', 5) for i in range(3)] for t in range(p)]
    R = [z3.BitVec(f'r_{t}', 2) for t in range(p)]
    C = [[z3.BitVec(f'c_{t}_{j}', 5) for j in range(3)] for t in range(p)]
    H = [z3.Bool(f'h_{t}') for t in range(p)]
    zero, one, ten = (z3.BitVecVal(v, 5) for v in (0, 1, base))
    pick = lambda r, xs: z3.If(r == 0, xs[0], z3.If(r == 1, xs[1], xs[2]))
    s.add(R[0] == residue)
    s.add(z3.Or(U[0][0] != U[0][1], U[0][1] != U[0][2]))
    if rotate_after_overflow:
        # Every positive-growth temporal loop can be rotated to this form.
        # All residues must still be searched before making a combined claim.
        s.add(H[-1])
    if bulk_start_filter:
        candidates = bulk_loop_starts(p, growth, base)
        candidates = [u for u, r in candidates if r == residue]
        s.add(z3.Or(*[z3.And(*[U[0][j] == u[j] for j in range(3)])
                      for u in candidates]))
    for t in range(p):
        nt = (t + 1) % p
        for v in A[t] + B[t] + U[t]:
            s.add(z3.ULE(v, base-1))
        for v in C[t]:
            s.add(z3.ULE(v, 1))
        s.add(z3.ULE(R[t], 2), A[t][-1] != 0)
        mate = [pick(R[t], [U[t][(r-1-j) % 3] for r in range(3)]) for j in range(3)]
        s.add(z3.Or(*[A[t][i] != B[t][k-1-i] for i in range(k)],
                    *[U[t][j] != mate[j] for j in range(3)]))
        # Core carry closes after three positions. Five bits are sufficient:
        # every addition column lies between 0 and 19.
        for j in range(3):
            total = U[t][j] + mate[j] + C[t][j]
            carry = C[t][(j+1) % 3]
            s.add(carry == z3.If(z3.UGE(total, ten), one, zero))
            s.add(U[nt][j] == total - ten * carry)
        # Exterior addition is performed independently on both ends.
        cl, ch = zero, pick(R[t], C[t])
        high = []
        for i in range(k):
            lo = B[t][i] + A[t][k-1-i] + cl
            hi = A[t][i] + B[t][k-1-i] + ch
            cl = z3.If(z3.UGE(lo, ten), one, zero)
            ch = z3.If(z3.UGE(hi, ten), one, zero)
            s.add(B[nt][i] == lo - ten * cl)
            high.append(hi - ten * ch)
        s.add(cl == C[t][0], H[t] == (ch == one))
        for i in range(k):
            shifted = one if i == k-1 else high[i+1]
            s.add(A[nt][i] == z3.If(H[t], shifted, high[i]))
        # Overflow increases the core length by one at its high end.
        s.add(z3.Implies(H[t], high[0] == pick(R[t], U[nt])))
        next_r = z3.If(R[t] == 2, z3.BitVecVal(0, 2), R[t] + 1)
        s.add(R[nt] == z3.If(H[t], next_r, R[t]))
    count_bits = (p + 1).bit_length()
    count = sum((z3.If(h, z3.BitVecVal(1, count_bits), z3.BitVecVal(0, count_bits))
                 for h in H), z3.BitVecVal(0, count_bits))
    s.add(count == growth)
    if cnf_path is not None:
        goal = z3.Goal()
        goal.add(*s.assertions())
        transformed = z3.Then('simplify', 'bit-blast', 'tseitin-cnf')(goal)
        assert len(transformed) == 1
        Path(cnf_path).write_text(transformed[0].dimacs()+'\n')
        return dict(period=p, cap_width=k, growth=growth, initial_residue=residue,
                    base=base, rotate_after_overflow=rotate_after_overflow,
                    bulk_start_filter=bulk_start_filter, cnf_path=str(cnf_path),
                    result='exported', seconds=time.monotonic()-start)
    status = s.check()
    result = dict(period=p, cap_width=k, growth=growth, initial_residue=residue, base=base,
                  rotate_after_overflow=rotate_after_overflow,
                  bulk_start_filter=bulk_start_filter,
                  result=str(status), seconds=time.monotonic()-start)
    if status == z3.sat:
        model = s.model()
        val = lambda v: model.eval(v).as_long()
        av = [[val(v) for v in row] for row in A]
        bv = [[val(v) for v in row] for row in B]
        uv = [[val(v) for v in row] for row in U]
        rv = [val(v) for v in R]
        cv = [[val(v) for v in row] for row in C]
        hv = [int(z3.is_true(model.eval(v))) for v in H]
        def integer_at(t, length):
            digits = bv[t] + [uv[t][j % 3] for j in range(length)] + av[t]
            return sum(d * base**i for i, d in enumerate(digits))
        tested = []
        for m in (1, 2, 3, 7, 20, 101):
            length = 3*m + residue
            n = integer_at(0, length)
            for t in range(p):
                assert length % 3 == rv[t]
                assert n == integer_at(t, length)
                digits, temp = [], n
                while temp:
                    temp, digit = divmod(temp, base)
                    digits.append(digit)
                assert digits != digits[::-1]
                n += sum(d * base**i for i, d in enumerate(reversed(digits)))
                length += hv[t]
            assert length == 3*m + residue + growth
            assert n == integer_at(0, length)
            tested.append(m)
        result.update(A_low_first=av, B_low_first=bv, U_low_first=uv,
                      residues=rv, carries=cv, overflow_clock=hv,
                      integer_checked_m=tested)
    elif status == z3.unknown:
        result['reason'] = s.reason_unknown()
    return result


@lru_cache(maxsize=None)
def bulk_loop_starts(period, growth, base=10):
    """All nonconstant local start states with the desired bulk temporal loop."""
    import itertools
    edges = {}
    for U in itertools.product(range(base), repeat=3):
        for r in range(3):
            successors = []
            q = [U[j] + U[(r-1-j) % 3] for j in range(3)]
            for c0 in (0, 1):
                c, V = c0, []
                for x in q:
                    x += c
                    V.append(x % base)
                    c = x // base
                if c == c0:
                    successors.extend([((tuple(V), (r+h) % 3), h) for h in (0, 1)])
            edges[U, r] = successors
    starts = []
    for initial in edges:
        if len(set(initial[0])) == 1:
            continue
        states = {(initial, 0)}
        for _ in range(period):
            states = {(v, total+h) for u, total in states
                      for v, h in edges[u] if total+h <= growth}
        if (initial, growth) in states:
            starts.append(initial)
    return starts


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', type=int, default=10, choices=(2, 10))
    ap.add_argument('--period', type=int, default=8)
    ap.add_argument('--growth', type=int, default=3)
    ap.add_argument('--widths', default='1,2,3,4,6,8')
    ap.add_argument('--residues', default='0,1,2')
    ap.add_argument('--seconds', type=float, default=10)
    ap.add_argument('--rotate-after-overflow', action='store_true')
    ap.add_argument('--bulk-start-filter', action='store_true')
    ap.add_argument('--cnf', default=None)
    ap.add_argument('--output', default='exist_periodic_bulk_results.json')
    args = ap.parse_args()
    results = []
    for k in map(int, args.widths.split(',')):
        for r in map(int, args.residues.split(',')):
            row = solve(args.period, k, args.growth, r, args.seconds, args.base,
                        args.rotate_after_overflow, args.bulk_start_filter, args.cnf)
            results.append(row)
            Path(args.output).write_text(json.dumps(results, indent=2)+'\n')
            print(json.dumps(row), flush=True)
            if row['result'] == 'sat':
                raise SystemExit(0)
