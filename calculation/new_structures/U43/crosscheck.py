#!/usr/bin/env python3
"""Cross-check U43's C++ digit-vector trace against Python unbounded integers.

The comparison is exact at every state: decimal digits, the full pair-coefficient
word, palindrome status, each overflow bit, clock membership, and epoch returns.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
if not __debug__:
    raise RuntimeError("U43 cross-check requires assertions; do not run python -O")
ALPHABET = "0123456789ABCDEFGHI"


def parse_lattice(path):
    rows = [[int(x) for x in line.split()] for line in Path(path).read_text().splitlines() if line.strip()]
    p, nb, m, base = rows[0]
    assert base == 10 and len(rows) == 1 + 1 + 3*p
    gamma = rows[1]
    W_rows = rows[2:2+p]
    # A second phase table of width m is stored before B_t in this repository format.
    _middle_rows = rows[2+p:2+2*p]
    B_rows = rows[2+2*p:2+3*p]
    assert all(len(x) == m for x in W_rows) and all(len(x) == m for x in _middle_rows) and all(len(x) == nb for x in B_rows)
    return gamma, B_rows[0], W_rows[0]


def csv_word(s):
    out = [int(x) for x in s.split(",") if x.strip()]
    assert all(0 <= x <= 18 for x in out)
    return out


def expand_template(B, W, J, U, C, q, k):
    h = B + W*q + J + U*k
    return h + C + h[::-1]


def realize_pairword(p):
    assert p == p[::-1] and p and all(0 <= x <= 18 for x in p)
    d = [0] * len(p)
    for i in range(len(p)//2):
        hi = min(9, p[i]); lo = p[i]-hi
        assert 0 <= lo <= 9
        d[i], d[-1-i] = lo, hi
    if len(p) % 2:
        assert p[len(p)//2] % 2 == 0
        d[len(p)//2] = p[len(p)//2]//2
    assert d[-1] != 0
    return int("".join(str(x) for x in reversed(d)))


def encode_pairword(p):
    return "".join(ALPHABET[x] for x in p)


def first_mismatch(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y: return i
    return -1 if len(a) == len(b) else min(len(a), len(b))


def run_case(simulator, lattice, q, k, J, U, C, steps, epoch, gain):
    gamma_clock, B, W = parse_lattice(lattice)
    source = expand_template(B, W, J, U, C, q, k)
    N = realize_pairword(source)
    cmd = [str(simulator), str(lattice), str(q), str(k),
           ",".join(map(str,J)), ",".join(map(str,U)), ",".join(map(str,C)),
           str(steps), str(epoch), str(gain)]
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    lines = proc.stdout.splitlines()
    assert len(lines) == steps+1, (len(lines), steps+1, proc.stderr)
    clock_mismatches = 0
    pal_steps = []
    checkpoints = []
    total_gamma = 0
    for t, line in enumerate(lines):
        fields = line.split("\t")
        assert len(fields) == 9, (t, fields[:3])
        ct, clen, cpal, cg, cclock, ctarget_k, ccheck, cdigits, cpairs = fields
        ct, clen, cpal, cg, cclock, ctarget_k, ccheck = map(int, (ct,clen,cpal,cg,cclock,ctarget_k,ccheck))
        assert ct == t
        s = str(N)
        d = [ord(ch)-48 for ch in reversed(s)]
        p = [d[i]+d[-1-i] for i in range(len(d))]
        pal = int(s == s[::-1])
        assert clen == len(s) and cdigits == s, (q,k,t,"digits differ")
        assert cpairs == encode_pairword(p), (q,k,t,"pairword differs")
        assert cpal == pal, (q,k,t,"palindrome flag differs")
        if pal: pal_steps.append(t)
        if t < steps:
            N2 = N + int(s[::-1])
            g = len(str(N2))-len(s)
            clock_match = int(g == gamma_clock[t % len(gamma_clock)])
            assert cg == g and cclock == clock_match, (q,k,t,"overflow/clock differs",cg,g,cclock,clock_match)
            total_gamma += g
            if not clock_match: clock_mismatches += 1
        else:
            assert cg == -1 and cclock == -1
        if t % epoch == 0:
            target_k = k + gain*(t//epoch)
            target = expand_template(B,W,J,U,C,q,target_k)
            check = int(p == target)
            assert ctarget_k == target_k and ccheck == check, (q,k,t,"checkpoint differs",ctarget_k,ccheck,check)
            checkpoints.append({"step":t,"target_k":target_k,"return":bool(check),
                               "first_mismatch":first_mismatch(p,target),
                               "actual_pairword_length":len(p),"expected_pairword_length":len(target)})
        else:
            assert ctarget_k == -1 and ccheck == -1
        if t < steps: N = N2
    return {"q":q,"k":k,"steps":steps,"epochs":steps//epoch,"gain_per_epoch":gain,
            "python_bigint_vs_cpp_digit_array":"EXACT_MATCH_EVERY_STATE",
            "clock_mismatches":clock_mismatches,"overflow_total":total_gamma,
            "palindrome_steps":pal_steps,"checkpoints":checkpoints}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--simulator", required=True, type=Path)
    ap.add_argument("--lattice", required=True, type=Path)
    ap.add_argument("--J", required=True, help="comma-separated LSD-first junction coefficients")
    ap.add_argument("--U", required=True, help="comma-separated LSD-first length-three U word")
    ap.add_argument("--C", required=True, help="comma-separated LSD-first palindromic centre coefficients")
    ap.add_argument("--widths", default="20:20,40:40,80:80,160:160", help="comma-separated q:k pairs")
    ap.add_argument("--steps", type=int, default=240)
    ap.add_argument("--epoch", type=int, default=120)
    ap.add_argument("--gain", type=int, default=5)
    args = ap.parse_args()
    J,U,C = csv_word(args.J),csv_word(args.U),csv_word(args.C)
    assert len(U)==3 and sum(U)==27 and U.count(9)==1
    nine=U.index(9)
    assert U[(nine+1)%3]%2==0 and U[(nine+2)%3]==18-U[(nine+1)%3]
    assert C==C[::-1]
    results=[]
    for item in args.widths.split(","):
        q,k=map(int,item.split(":"))
        result=run_case(args.simulator,args.lattice,q,k,J,U,C,args.steps,args.epoch,args.gain)
        results.append(result)
        print(json.dumps(result,separators=(",",":")),flush=True)
    print(json.dumps({"summary":"U43_TRACE_CROSSCHECK_PASS","cases":len(results),
                      "all_states_exact":all(r["python_bigint_vs_cpp_digit_array"]=="EXACT_MATCH_EVERY_STATE" for r in results),
                      "all_clocks_compared":True,"all_checkpoints_compared":True,
                      "total_checkpoint_comparisons":sum(len(r["checkpoints"]) for r in results)},separators=(",",":")))

if __name__ == "__main__": main()
