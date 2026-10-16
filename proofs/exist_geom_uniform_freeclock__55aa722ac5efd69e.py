"""Exact SAT search for decimal reverse-add uniform-run pumps.

Searches A_t || d_t**m || B_t with fixed-width exteriors, arbitrary overflow
clock, periodic exterior digits, and d cycle 8,7,5,1,2,4 (or 6,3).
Any SAT model is checked with ordinary integer arithmetic at several m.
UNSAT is only for the selected temporal period and exterior width.
"""
import argparse, json, time
from pathlib import Path
import z3


def decimal_cycle(d):
    r = [d]
    while True:
        d = 2*d if d < 5 else 2*d-9
        if d == r[0]:
            return r
        if d in r:
            raise ValueError("nonperiodic initial bulk digit")
        r.append(d)


def solve(p, k, g, seconds=30, d0=8, forced_clock=None):
    start = time.monotonic()
    cyc = decimal_cycle(d0)
    assert p % len(cyc) == 0
    ds = [cyc[t % len(cyc)] for t in range(p)]
    slv = z3.SolverFor("QF_BV")
    slv.set(timeout=int(1000*seconds))
    A = [[z3.BitVec(f"a_{t}_{i}", 5) for i in range(k)] for t in range(p)]
    B = [[z3.BitVec(f"b_{t}_{i}", 5) for i in range(k)] for t in range(p)]
    H = [z3.Bool(f"h_{t}") for t in range(p)]
    z = z3.BitVecVal(0, 5)
    o = z3.BitVecVal(1, 5)
    ten = z3.BitVecVal(10, 5)
    for t in range(p):
        for v in A[t] + B[t]:
            slv.add(z3.ULE(v, 9))
        slv.add(A[t][-1] != 0)
        # The center is palindromic; an exterior mismatch is essential.
        slv.add(z3.Or([A[t][i] != B[t][k-1-i] for i in range(k)]))
        eps = o if ds[t] >= 5 else z
        nl, nh = (t+1) % p, (t+1) % p
        cl, ch = z, eps
        hi = []
        for i in range(k):
            low = B[t][i] + A[t][k-1-i] + cl
            high = A[t][i] + B[t][k-1-i] + ch
            cl = z3.If(z3.UGE(low,ten),o,z)
            ch = z3.If(z3.UGE(high,ten),o,z)
            slv.add(B[nl][i] == low - ten*cl)
            hi.append(high - ten*ch)
        slv.add(cl == eps)
        slv.add(H[t] == (ch == o))
        for i in range(k):
            shifted = o if i == k-1 else hi[i+1]
            slv.add(A[nh][i] == z3.If(H[t], shifted, hi[i]))
        slv.add(z3.Implies(H[t],hi[0] == ds[(t+1)%p]))
    # BV popcount avoids leaving QF_BV.
    width = (p+1).bit_length()
    count = sum((z3.If(x,z3.BitVecVal(1,width),z3.BitVecVal(0,width)) for x in H), z3.BitVecVal(0,width))
    slv.add(count == g)
    if forced_clock is not None:
        assert len(forced_clock) == p
        for t,x in enumerate(forced_clock):
            slv.add(H[t] == bool(x))
    result = slv.check()
    out = {"period":p,"exterior_width":k,"growth":g,"bulk_digit":d0,
           "result":str(result),"seconds":time.monotonic()-start}
    if result == z3.sat:
        model = slv.model()
        aval = ["".join(str(model.eval(v).as_long()) for v in reversed(row)) for row in A]
        bval = ["".join(str(model.eval(v).as_long()) for v in reversed(row)) for row in B]
        hval = [z3.is_true(model.eval(h)) for h in H]
        checked = []
        for m in [1,2,3,7,20,101]:
            n = int(aval[0] + str(d0)*m + bval[0])
            length = m
            for t in range(p):
                assert str(n) == aval[t] + str(ds[t])*length + bval[t]
                assert str(n) != str(n)[::-1]
                n += int(str(n)[::-1])
                length += hval[t]
            assert str(n) == aval[0] + str(d0)*(m+g) + bval[0]
            checked.append(m)
        out.update(A=aval,B=bval,clock=[int(x) for x in hval],tested_bulk_lengths=checked)
    elif result == z3.unknown:
        out['reason'] = slv.reason_unknown()
    return out


if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--period',type=int,default=24)
    ap.add_argument('--widths',default='1,2,3,4,6,8,12,16,24,32')
    ap.add_argument('--growth',type=int,default=9)
    ap.add_argument('--digit',type=int,default=8)
    ap.add_argument('--seconds',type=float,default=10)
    ap.add_argument('--output',default='exist_geom_uniform_freeclock_results.json')
    args=ap.parse_args()
    results=[]
    for k in map(int,args.widths.split(',')):
        row=solve(args.period,k,args.growth,args.seconds,args.digit)
        results.append(row)
        Path(args.output).write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps(row),flush=True)
        if row['result']=='sat': break
