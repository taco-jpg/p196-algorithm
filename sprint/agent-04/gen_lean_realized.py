#!/usr/bin/env python3
"""Data for lean/P196/Sprint/Agent04/Realized.lean.

* orbit(10097, t), t = 220..228: width-7 outer column words and actual carries into column L-7;
  word_220 == word_228 (a closed walk of the abstraction realized by actual integers).
* orbit(10151, t), t = 5..80: same, plus the shortest abstract walk from word_5 back to the
  length-7 cycle (computed by `entry` and passed in as ENTRY_TSV).

usage: gen_lean_realized.py ENTRY_TSV_FOR_W5 OUT.lean     (prints the W5 target line if ENTRY_TSV is '-')
"""
import sys
from pathlib import Path

from absref import code, forward_prefix, unpack

K = 7
Z7 = [10, 2, 3, 2, 7, 5, 0]


def orbit(n, t):
    for _ in range(t):
        n = n + int(str(n)[::-1])
    return n


def word_carry(n, k=K):
    d = [int(c) for c in reversed(str(n))]
    L = len(d)
    q = [d[i] + d[L - 1 - i] for i in range(L)]
    c = 0
    for i in range(L - k):
        c = (q[i] + c) // 10
    return q[:k], c


def series(seed, t0, t1):
    out = []
    for t in range(t0, t1 + 1):
        out.append(word_carry(orbit(seed, t)))
    for i in range(len(out) - 1):
        w, e = out[i]
        assert forward_prefix(w, e) == out[i + 1][0], (seed, t0 + i)
    return out


def lean_list(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    a = series(10097, 220, 228)
    assert a[0][0] == a[8][0]
    b = series(10151, 5, 80)
    s81 = str(orbit(10151, 81))
    assert s81 == s81[::-1] and s81.startswith("1337")
    w5 = b[0][0]
    if sys.argv[1] == "-":
        print("W5 " + " ".join(map(str, w5)))
        return
    # abstract entry from w5 to z7
    import csv
    row = next(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
    assert int(row["p0_code"]) == code(w5)
    absent = [int(x) for x in row["packed_entry"].split(",")] if row["packed_entry"] else []
    cur = w5
    for n in absent:
        s, e = unpack(K, n)
        assert forward_prefix(s, e) == cur
        cur = s
    assert cur == Z7
    # backward walks, packed
    back_a = [2 * code(a[i][0]) + a[i][1] for i in range(7, -1, -1)]          # w227..w220
    back_b = [2 * code(b[i][0]) + b[i][1] for i in range(len(b) - 2, -1, -1)]  # w79..w5
    tmpl = open(Path(__file__).with_name("Realized.lean.in")).read()
    rep = {
        "@A_WORDS@": lean_list([lean_list(w) for w, _ in a]),
        "@A_CARRIES@": lean_list([e for _, e in a]),
        "@A_BACK@": lean_list(back_a),
        "@B_WORDS@": lean_list([lean_list(w) for w, _ in b]),
        "@B_CARRIES@": lean_list([e for _, e in b]),
        "@B_BACK@": lean_list(back_b + absent),
        "@B_LEN@": str(len(b)),
        "@P81@": s81,
    }
    for k, v in rep.items():
        tmpl = tmpl.replace(k, v)
    open(sys.argv[2], "w").write(tmpl)
    print("10097 words:", [w for w, _ in a])
    print("10151: words t=5..80:", len(b), "abstract entry from w5:", len(absent), "steps; w80 =", b[-1][0])


if __name__ == "__main__":
    main()
