#!/usr/bin/env python3
"""Independent arbitrary-precision decimal replay for Z10 scan controls.

This is deliberately separate from scan.cpp's bit-sliced pairword engine.
It builds a canonical decimal integer, applies n <- n + reverse10(n), and
reconstructs the pairword from the resulting decimal digits at every step.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

SPACE = 19**5
US = [(8, 10, 9), (10, 9, 8)]
NEAR = [
    ((8, 10, 9), [5, 9, 10, 10, 9]),  # scan first mismatch at cut - 12
    ((10, 9, 8), [4, 4, 1, 1, 7]),    # scan first mismatch at cut - 13
]

def load_lattice(path: Path):
    lines = path.read_text().splitlines()
    header = list(map(int, lines[0].split()))
    if header != [12, 34, 9, 10]:
        raise ValueError(f"unexpected lattice header: {header}")
    gamma = list(map(int, lines[1].split()))
    rows = [list(map(int, x.split())) for x in lines[2:]]
    if len(rows) != 36 or any(len(r) not in (9, 34) for r in rows):
        raise ValueError("unexpected p12/m9 lattice row layout")
    W = rows[:12]
    B = rows[24:36]
    return gamma, B[0], W[0]

def decode_j(index: int):
    if not 0 <= index < SPACE:
        raise ValueError("J index outside 0..19^5-1")
    d = [0] * 5
    for i in range(4, -1, -1):
        d[i] = index % 19
        index //= 19
    return d

def template(B, W, J, U, q, k):
    H = list(B) + list(W) * q + list(J) + list(U) * k
    return H + [2] + H[::-1]

def canonical_seed(pairword):
    """Choose digits d_i with d_i+d_(n-1-i)=pairword[i]."""
    n = len(pairword)
    d = [0] * n
    for i in range(n // 2):
        lo = min(9, pairword[i])
        d[i] = lo
        d[n - 1 - i] = pairword[i] - lo
    if n % 2:
        assert pairword[n // 2] % 2 == 0
        d[n // 2] = pairword[n // 2] // 2
    if not d[-1]:
        raise ValueError("noncanonical source: leading digit is zero")
    return int("".join(map(str, d[::-1])))

def pairword_of_integer(n: int):
    d = [ord(c) - 48 for c in str(n)[::-1]]
    return [d[i] + d[-1 - i] for i in range(len(d))]

def replay(gamma, B, W, q, k, J, U, steps=240):
    p0 = template(B, W, J, U, q, k)
    n = canonical_seed(p0)
    clock = []
    palindrome_times = []
    first_offset = None
    full120 = None
    full240 = None
    prefix = list(B) + list(W) * q
    target120 = template(B, W, J, U, q, k + 5)
    target240 = template(B, W, J, U, q, k + 10)
    for t in range(steps + 1):
        s = str(n)
        if s == s[::-1]:
            palindrome_times.append(t)
        if t in (120, 240):
            got = pairword_of_integer(n)
            if t == 120:
                if len(got) < len(prefix):
                    first_offset = len(got) - len(prefix)
                else:
                    mismatch = next((i for i, (a, b) in enumerate(zip(got, prefix)) if a != b), None)
                    first_offset = None if mismatch is None else mismatch - len(prefix)
                full120 = got == target120
            else:
                full240 = got == target240
        if t == steps:
            break
        nxt = n + int(s[::-1])
        clock.append(len(str(nxt)) - len(s))
        n = nxt
    expected = [gamma[t % len(gamma)] for t in range(steps)]
    return {
        "q": q, "k": k, "J": J, "U": U,
        "digits_initial": len(str(canonical_seed(p0))),
        "clock120_exact": clock[:120] == expected[:120],
        "clock240_exact": clock == expected,
        "overflow_count120": sum(clock[:120]),
        "overflow_count240": sum(clock),
        "first_W9_mismatch_from_cut": first_offset,
        "full_return120": full120,
        "full_return240": full240,
        "palindrome_times": palindrome_times,
    }

def prefix64(gamma, B, W):
    expected_hist = {
        (8, 10, 9): {-23: 25, -22: 39},
        (10, 9, 8): {-23: 26, -22: 38},
    }
    out = {}
    for U in US:
        hist = {}
        for idx in range(64):
            J = decode_j(idx)
            r = replay(gamma, B, W, 14, 100, J, U, 120)
            if not r["clock120_exact"]:
                raise AssertionError(f"clock mismatch in control index {idx}, U={U}")
            off = r["first_W9_mismatch_from_cut"]
            hist[off] = hist.get(off, 0) + 1
        if hist != expected_hist[U]:
            raise AssertionError(f"bit-sliced control histogram mismatch for U={U}: {hist}")
        out[str(U)] = {"cases": 64, "clock_exact": True, "first_mismatch_histogram": hist}
    return out

def width_controls(gamma, B, W):
    cases = []
    Js = [[0, 0, 0, 0, 0], [18, 18, 18, 18, 18]]
    cases.extend((U, J) for U in US for J in Js)
    cases.extend(NEAR)
    out = []
    for U, J in cases:
        for q, k in ((14, 100), (20, 80), (40, 160), (80, 320), (160, 640)):
            r = replay(gamma, B, W, q, k, J, U, 240)
            if not r["clock120_exact"] or not r["clock240_exact"]:
                raise AssertionError(f"clock mismatch in bigint control: {r}")
            if r["full_return120"] or r["full_return240"]:
                raise AssertionError(f"unexpected full template return in bigint control: {r}")
            if r["palindrome_times"]:
                raise AssertionError(f"palindrome in bigint control: {r}")
            out.append(r)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lattice", default="calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt")
    ap.add_argument("--mode", choices=("prefix64", "width-controls", "all"), default="all")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    gamma, B, W = load_lattice(Path(args.lattice))
    if gamma != [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]:
        raise ValueError(f"unexpected phase-0 overflow clock: {gamma}")
    result = {"engine": "Python arbitrary-precision integer n + reverse10(n)", "independent_of": "scan.cpp bit-sliced coefficient engine"}
    if args.mode in ("prefix64", "all"):
        result["prefix64_crosscheck"] = prefix64(gamma, B, W)
    if args.mode in ("width-controls", "all"):
        result["width_controls"] = width_controls(gamma, B, W)
    encoded = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        Path(args.out).write_text(encoded + "\n")
    print(encoded)

if __name__ == "__main__":
    main()
