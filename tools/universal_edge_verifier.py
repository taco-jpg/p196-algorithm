#!/usr/bin/env python3
"""Q50: exact all-length checker for one-parameter folded pairword edge cycles.

The input is a JSON object of the form
 {"base": 10, "min_m": 20, "phases": [
   {"word": [{"lit": [1, ...]}, {"rep": [9], "factor": 1, "offset": 0},
             {"lit": [...]}, ...], "delta": 0}, ...]}
A 'rep' block repeats factor*m+offset times; factor >= 0, nonnegative
integer offsets are allowed. 'delta' changes m for the NEXT phase. Every
phase is a complete low-digit-first symmetric pairword of a real integer,
not a half-word. The final phase must return to phase 0 with sum(delta)>0.

Also accepts the repository's neutral_cycle (edges/B/C/u/v/gamma) and
lattice_cycle (B_t/w_t/gam/l0/m) formats without modifying their data.

No claim is accepted from finitely many replay steps alone. A certificate
requires exact affine-segment normalization and the overlap-periodicity
proof below. Proven phase guards demand an odd pair coefficient in each
phase, which is sufficient (not necessary) for non-palindromicity.
"""
import argparse
import json
import math
import sys
from pathlib import Path

# Assertions are proof obligations; refuse optimized Python which removes them.
if not __debug__:
    raise RuntimeError("Certificate verification requires assertions: do not use python -O")


def lit(w):
    return {"lit": list(w)}


def rep(w, offset=0, factor=1):
    return {"rep": list(w), "factor": factor, "offset": offset}


def normalize_json(data):
    b = data["base"]
    if "phases" in data:
        return data
    if "edges" in data and "initial_band" in data:
        es = data["edges"]
        ps = []
        for i, e in enumerate(es):
            assert e["B_next"] == es[(i + 1) % len(es)]["B"]
            assert e["C_next"] == es[(i + 1) % len(es)]["C"]
            B, C = e["B"], e["C"]
            ps.append({"word": [lit(B), rep([b - 1]), lit(C),
                                rep([b - 1]), lit(B[::-1])],
                       "delta": e["u"] + e["v"] - e["gamma"]})
        return {"base": b, "min_m": max(1, int(data["initial_band"])), "phases": ps}
    if "B_t" in data and "w_t" in data and "gam" in data:
        wsize, total, n = data["m"], data["l0"], len(data["B_t"])
        assert len(data["w_t"]) == len(data["gam"]) == n
        assert all(len(w) == wsize for w in data["w_t"])
        offs = []
        for g in data["gam"]:
            offs.append((total // wsize, total % wsize))
            total += g
        assert total % wsize == data["l0"] % wsize
        offs.append((total // wsize, total % wsize))
        ps = []
        for i in range(n):
            B, W = data["B_t"][i], data["w_t"][i]
            k, r = offs[i]
            ps.append({"word": [lit(B), rep(W), lit(W[:r]), lit(B[::-1])],
                       "delta": offs[i + 1][0] - k})
        return {"base": b, "min_m": 2, "phases": ps}
    raise ValueError("unsupported JSON format: pass phases or repository neutral/lattice cycle")


def length(block):
    if "lit" in block:
        return 0, len(block["lit"])
    return len(block["rep"]) * block.get("factor", 1), len(block["rep"]) * block.get("offset", 0)


def total_length(blocks):
    a = z = 0
    for block in blocks:
        x, y = length(block)
        a += x
        z += y
    return a, z


def checked_blocks(blocks, b, m0):
    for block in blocks:
        assert ("lit" in block) != ("rep" in block), "block must be lit xor rep"
        w = block.get("lit", block.get("rep"))
        assert isinstance(w, list) and all(type(x) is int and 0 <= x <= 2*b-2 for x in w)
        if "rep" in block:
            assert w, "empty repeated word"
            assert type(block.get("factor", 1)) is int and block.get("factor", 1) >= 0
            assert type(block.get("offset", 0)) is int
            assert block.get("factor", 1) * m0 + block.get("offset", 0) >= 1, "empty band at minimum m"


def expand(blocks, m):
    out = []
    for z in blocks:
        out.extend(z["lit"] if "lit" in z else z["rep"] * (z.get("factor",1)*m+z.get("offset",0)))
    return out


def affine_segments(blocks):
    """(start affine (a,b), end affine (a,b), nonempty periodic word)."""
    out, a, c = [], 0, 0
    for z in blocks:
        w = z.get("lit", z.get("rep"))
        da, dc = length(z)
        if w and (da or dc):
            out.append(((a,c), (a+da,c+dc), w))
        a += da
        c += dc
    return out


def norm_one(word, carry, b):
    ds = []
    for s in word:
        v = s + carry
        ds.append(v % b)
        carry = v // b
        assert carry in (0, 1)
    return ds, carry


def normalize_symbolic(blocks, b):
    """Exact for every m in the admissible domain, not just sampled m.

    For each repeated block, carry transfer f:{0,1}->{0,1} is monotone;
    hence f is identity or constant, so the first copy either leaves the
    carry unchanged forever or enters a fixed point from the second copy.
    """
    out, carry = [], 0
    for z in blocks:
        if "lit" in z:
            digits, carry = norm_one(z["lit"], carry, b)
            if digits: out.append(lit(digits))
            continue
        w, factor, offset = z["rep"], z.get("factor", 1), z.get("offset", 0)
        one, nxt = norm_one(w, carry, b)
        if nxt == carry:
            out.append(rep(one, offset, factor))
        else:
            steady, fix = norm_one(w, nxt, b)
            assert fix == nxt, "unexpected nonmonotone carry map"
            out.extend([lit(one), rep(steady, offset - 1, factor)])
        carry = nxt
    if carry:
        out.append(lit([carry]))
    return out, carry


def reversed_blocks(blocks):
    return [({"lit": z["lit"][::-1]} if "lit" in z
             else rep(z["rep"][::-1], z.get("offset",0), z.get("factor",1)))
            for z in blocks[::-1]]


def shifted(blocks, d):
    return [lit(z["lit"]) if "lit" in z else
            rep(z["rep"], z.get("offset",0) + d*z.get("factor",1), z.get("factor",1))
            for z in blocks]


def symbolic_bound(block_sets, min_m):
    """Finite bound proving periodic overlap of ALL affine periodic segments.

    Let H=lcm of every REPEATED block's digit period, P=2H.
    Literal blocks have finite width and cannot cross a moving run after C;
    their relative coordinate is fixed in every persistent overlap.
    Beyond threshold C,
    every pair of affine block endpoints has constant ordering, including
    the midpoint of a word. Every intersection of finitely many runs is
    empty, fixed-width, or has width increasing >=1 each m. At m>=C+P,
    growing intersections contain all P positional residues. Fixed-width
    intersections translate by a multiple of P under m -> m+P. Digits
    (and centre parity) depend only on (m mod P, index mod P), so equality
    at m<=C+2P-1 implies equality for ALL larger m by induction on P.
    """
    periods = [len(z["rep"]) for bs in block_sets for z in bs if "rep" in z]
    h = math.lcm(*(p for p in periods if p > 0)) if periods else 1
    P = 2*h
    ends = []
    for blocks in block_sets:
        segs = affine_segments(blocks)
        n = total_length(blocks)
        ends.extend((2*a, 2*b) for s,e,w in segs for a,b in (s,e))
        ends.append((n[0], n[1]-1))  # (length-1)/2, doubled
    C = min_m
    for i, (a,x) in enumerate(ends):
        for d,y in ends[:i]:
            if a != d:
                C = max(C, abs(x-y)//abs(a-d)+2)
    return C + 2*P - 1, P, C


def digit_from_segments(segs, m, pos):
    for (a,c),(z,v),w in segs:
        begin, end = a*m+c, z*m+v
        if begin <= pos < end:
            return w[(pos-begin) % len(w)]
    raise AssertionError(f"position {pos} not covered at m={m}")


def validate_cycle(data, *, max_bound=10000, bigint_widths=(20,40,80,160,200), bigint_cycles=2):
    b = data["base"]
    m0 = data["min_m"]
    ps = data["phases"]
    assert type(b) is int and b >= 2 and type(m0) is int and m0 >= 1
    assert isinstance(ps, list) and ps
    for phase in ps:
        assert type(phase["delta"]) is int
        checked_blocks(phase["word"], b, m0)
    gain = sum(p["delta"] for p in ps)
    assert gain > 0, "no positive net growth"
    cumulative = 0
    all_checks = []
    for j, phase in enumerate(ps):
        before = shifted(phase["word"], cumulative)
        after = shifted(ps[(j+1)%len(ps)]["word"], cumulative + phase["delta"])
        checked_blocks(before, b, m0)
        checked_blocks(after, b, m0)
        ds, gamma = normalize_symbolic(before, b)
        assert total_length(ds) == total_length(after), f"phase {j}: length/overflow mismatch"
        if "gamma" in phase:
            assert phase["gamma"] == gamma, f"phase {j}: specified overflow mismatch"
        revP = reversed_blocks(before)
        revD = reversed_blocks(ds)
        bound, period, cutoff = symbolic_bound([before, revP, ds, revD, after], m0)
        if bound > max_bound:
            raise ValueError(f"phase {j}: exact bound {bound} exceeds ceiling {max_bound}; UNDECIDED")
        # For input realizability, symmetric pair coefficients and even middle
        # coefficients (where length odd) are required, on every m.
        # For the output, D_i+D_{n-1-i} must equal the claimed next pairword.
        segP, segRevP, segD, segRevD, segAfter = [affine_segments(s) for s in
                                                 (before, revP, ds, revD, after)]
        odd_witness = any(any(x%2 for x in z.get("lit", z.get("rep"))) for z in before)
        assert odd_witness, f"phase {j}: no guaranteed odd coefficient"
        for m in range(m0, bound+1):
            n = total_length(before)[0]*m+total_length(before)[1]
            n2 = total_length(ds)[0]*m+total_length(ds)[1]
            assert digit_from_segments(segP,m,0) > 0, f"phase {j},m={m}: zero outer coefficient"
            assert digit_from_segments(segD,m,n2-1) > 0, f"phase {j},m={m}: leading zero in normalized integer"
            if n%2:
                assert digit_from_segments(segP,m,n//2)%2==0, f"phase {j},m={m}: unrealizable centre"
            for i in range(n):
                x = digit_from_segments(segP,m,i)
                assert x == digit_from_segments(segRevP,m,i), f"phase {j},m={m},i={i}: nonsymmetric input"
            for i in range(n2):
                x = digit_from_segments(segD,m,i) + digit_from_segments(segRevD,m,i)
                assert x == digit_from_segments(segAfter,m,i), f"phase {j},m={m},i={i}: WRONG EDGE"
        all_checks.append({"phase":j,"overflow":gamma,"finite_bound":bound,
                           "period":period,"cutoff":cutoff})
        cumulative += phase["delta"]
    # Exact arithmetic independent of the pairword transducer.
    # Initial real integer is constructed by splitting symmetric coefficients.
    if bigint_cycles:
        for q in bigint_widths:
            if q < m0: continue
            P = expand(ps[0]["word"],q)
            assert P == P[::-1]
            digits = [0]*len(P)
            for i in range(len(P)//2):
                hi=min(P[i], b-1)
                digits[i]=P[i]-hi
                digits[-1-i]=hi
            if len(P)%2:digits[len(P)//2] = P[len(P)//2]//2
            assert digits[-1] != 0
            N = sum(d*b**i for i,d in enumerate(digits))
            m=q
            for t in range(len(ps)*bigint_cycles):
                j=t%len(ps)
                d=[];n=N
                while n:
                    d.append(n % b);n//=b
                observed=[d[i]+d[-1-i] for i in range(len(d))]
                assert observed == expand(ps[j]["word"],m), f"bigint pairword mismatch at width {q}, step {t}"
                assert d!=d[::-1], f"bigint palindrome at width {q}, step {t}"
                rev=sum(x*b**i for i,x in enumerate(d[::-1]))
                N+=rev
                m+=ps[j]["delta"]
    return {"label":"PAPER PROOF conditional on code correctness", "base":b,
            "phases":len(ps),"min_m":m0,"gain":gain,
            "checks":all_checks,"bigint_widths":list(bigint_widths)}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("json",nargs="+",type=Path)
    ap.add_argument("--max-bound",type=int,default=10000)
    ap.add_argument("--cycles",type=int,default=2)
    args=ap.parse_args()
    failed=False
    for path in args.json:
        try:
            data=normalize_json(json.loads(path.read_text()))
            result=validate_cycle(data,max_bound=args.max_bound,bigint_cycles=args.cycles)
            print(json.dumps({"file":str(path),"status":"ALL_LENGTH_CYCLE_PASS",**result}))
        except Exception as e:
            failed=True
            print(json.dumps({"file":str(path),"status":"NOT_CERTIFIED","reason":f"{type(e).__name__}: {e}"}))
    if failed:sys.exit(1)


if __name__ == "__main__":main()