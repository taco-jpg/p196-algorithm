#!/usr/bin/env python3
"""Untrusted generator for the four-column rank-tree certificate.

Agent #119, task agent119-four-column-prefix-kernel.  Python standard library only.

Everything emitted here is *checked* by the Lean kernel (decide +kernel); this
script is not part of the trusted base.  It mirrors, definition by definition:

  SevenColumn.prefixPredecessors          (PrefixInverse.lean, Agent #104)
  SevenColumn.ShortBoundary.rawWords 1..3 and nextWord (ShortBoundary.lean)
  SevenColumn.Certificate.wordCode / lookupKey ordering (PrefixCertificate.lean)
  FourColumnKernel.rootWords               (ThreeDigitBridge.lean)

Table source: the 360-class table of
proofs/chat-6acee928/originals/p196_four_column_obstruction.md section 6,
minus the classes owned by other tasks (see EXCLUDED_TWO_DIGIT and
EXCLUDED_THREE_DIGIT).  The written bounds are compared with the bounds
recomputed here; any mismatch aborts.

Usage:  python3 generate_certificate.py [--check-only]
"""
from __future__ import annotations

import hashlib
import json
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "certificate"

# ---------------------------------------------------------------- written table
# Verbatim transcription of section 6 of p196_four_column_obstruction.md:
# first two digits -> "c:B" entries.
WRITTEN = """
10 | 0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:1, 9:1
12 | 0:7
13 | 0:1
14 | 0:1, 1:1
15 | 0:1, 1:1, 2:1
16 | 0:1, 1:1, 2:1, 3:1
17 | 0:1, 1:1, 2:1, 3:1, 4:1
18 | 0:1, 1:1, 2:1, 3:1, 4:1, 5:1
19 | 0:1, 1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:7
20 | 0:2, 1:2, 2:2, 3:2, 4:2, 5:2, 6:2, 7:2, 8:2, 9:2
21 | 4:8, 5:8
24 | 0:2, 1:8
25 | 0:9, 6:7
26 | 0:2, 1:2, 2:2
27 | 2:6, 3:7
28 | 0:2, 1:2, 2:2, 3:2, 4:2
30 | 0:1, 1:2, 2:2, 3:2, 4:2, 5:2, 6:2, 7:2, 8:2
31 | 0:13
32 | 0:1, 1:2, 2:2, 3:2, 4:2, 5:2, 6:2, 7:2, 8:2, 9:2
33 | 0:5, 1:5, 2:5, 3:5, 4:5, 5:5, 6:5, 7:5, 8:5, 9:5
34 | 0:8, 1:8, 2:8, 3:8, 4:8, 5:8, 6:8, 7:8
35 | 0:2
36 | 0:1, 1:2
37 | 0:2, 1:2, 2:2, 6:8
38 | 0:1, 1:2, 2:2, 3:2
40 | 0:3, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3
41 | 0:3, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3
42 | 3:3, 4:9, 7:3, 8:3
47 | 8:7
48 | 0:3, 1:3, 2:9
50 | 0:1, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3
52 | 0:1, 1:3, 5:3
53 | 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3
54 | 0:1, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3
56 | 0:5, 1:14
58 | 0:1, 1:3, 2:5, 9:5
59 | 1:11, 2:10
60 | 0:2, 1:2, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3
61 | 0:3, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3
62 | 0:14, 1:3, 5:3, 9:3
64 | 0:2, 1:2, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3
65 | 0:6, 1:6, 2:6, 3:6, 4:6, 5:6, 6:6, 7:6, 8:6, 9:6
67 | 6:5
68 | 0:2
69 | 0:9, 1:9, 8:5
70 | 0:1, 1:2, 2:2, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3
72 | 0:1, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3
73 | 1:12
74 | 0:1, 1:2, 2:2, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3
75 | 0:12, 4:12
76 | 0:1, 1:3, 2:3, 3:3, 4:3, 5:3, 6:3, 7:3, 8:3, 9:3
77 | 1:6, 2:6, 3:6, 4:6, 5:12, 6:12, 9:6
78 | 0:6, 1:12, 2:12
80 | 0:4, 1:4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4, 8:4, 9:4
81 | 0:4, 1:4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4, 8:4, 9:4
82 | 0:4, 1:4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4, 8:4, 9:4
83 | 0:4, 1:4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4, 8:4, 9:4
84 | 5:4, 6:4, 7:4, 8:4
85 | 0:10, 1:10, 2:4, 3:4, 4:4, 5:10
86 | 7:4, 8:4
90 | 0:1, 1:4, 2:4, 3:4, 4:11
92 | 0:1, 1:4, 2:7, 5:4
93 | 9:8
94 | 0:1, 1:4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4, 8:4
96 | 0:1, 1:4, 8:7
97 | 4:4, 5:4, 6:4
98 | 0:1, 1:4, 2:4, 3:4
"""

# Owned by Agent #113 (thirteen two-digit families): all their extensions.
EXCLUDED_TWO_DIGIT = {10, 20, 32, 40, 41, 60, 64, 65, 76, 80, 81, 82, 83}
# Owned by Agent #104 (620 claim; 739 integrated is not in this table).
EXCLUDED_THREE_DIGIT = {620}


def written_table() -> dict[int, int]:
    table: dict[int, int] = {}
    for line in WRITTEN.strip().splitlines():
        head, entries = line.split("|")
        ab = int(head)
        for item in entries.split(","):
            c, b = item.strip().split(":")
            table[10 * ab + int(c)] = int(b)
    assert len(table) == 360, len(table)
    return table


# ------------------------------------------------- mirror of PrefixInverse.lean
def carry(a: int, x: int) -> int:
    return (a + x) // 10


def low(a: int, x: int) -> int:
    return (a + x) % 10


@lru_cache(None)
def no_overflow_pred(p: tuple, x: int, y: int) -> tuple:
    if not p:
        return ((),)
    v, rest = p[0], p[1:]
    out = []
    for a in range(19):
        for z in range(2):
            if carry(a, z) == y and v == low(a, x) + low(a, z):
                out.extend((a,) + t for t in no_overflow_pred(rest, carry(a, x), z))
    return tuple(out)


@lru_cache(None)
def overflow_tail_pred(p: tuple, a: int, x: int, y: int) -> tuple:
    if not p:
        return ((),) if any(carry(a, z) == y for z in range(2)) else ()
    v, rest = p[0], p[1:]
    out = []
    for b in range(19):
        for z in range(2):
            if carry(a, z) == y and v == low(b, x) + low(a, z):
                out.extend((b,) + t for t in overflow_tail_pred(rest, b, carry(b, x), z))
    return tuple(out)


def overflow_pred(p: tuple) -> tuple:
    if not p:
        return ()
    v = p[0]
    if 0 < v <= 10:
        a = v + 9 if v <= 9 else 9
        return tuple((a,) + t for t in overflow_tail_pred(p[1:], a, carry(a, 0), 1))
    return ()


@lru_cache(None)
def prefix_predecessors(p: tuple) -> tuple:
    keep = tuple(s for s in no_overflow_pred(p, 0, 0) if (s[0] if s else 0) > 0)
    return keep + overflow_pred(p)


def long_pred4(p: tuple) -> tuple:
    return prefix_predecessors(p) if len(p) == 4 else ()


# ------------------------------------------------- mirror of ShortBoundary.lean
def raw_words(n: int) -> list:
    if n == 1:
        return [(2 * (a + 1),) for a in range(9)]
    if n == 2:
        return [(a + 1, a + 1) for a in range(18)]
    if n == 3:
        return [(a + 1, 2 * c, a + 1) for a in range(18) for c in range(10)]
    raise ValueError(n)


SHORT_WORDS3 = raw_words(1) + raw_words(2) + raw_words(3)
assert len(SHORT_WORDS3) == 207


def next_word(s: tuple) -> tuple:
    """Exact pair-sum word of the reverse-and-add output (overflow included)."""
    digits, c = [], 0
    for v in s:
        t = v + c
        digits.append(t % 10)
        c = t // 10
    if c:
        digits.append(c)
    n = len(digits)
    return tuple(digits[i] + digits[n - 1 - i] for i in range(n))


def word_code(w: tuple) -> int:
    a = 1
    for d in w:
        a = 19 * a + d
    return a


# --------------------------------------------------- mirror of ThreeDigitBridge
def growth_prefix(a: int, b: int, c: int) -> bool:
    return a == 1 and ((b == 1 and c <= 1) or (b == 2 and 1 <= c <= 2))


def root_words(a: int, b: int, c: int) -> list:
    out = [(a, b, a)] if (c == a and b % 2 == 0) else []
    return out + [(a, b, c, d) for d in range(10)]


EXTRA_ROOTS = [(3, 3)]  # width-two root for the complete two-digit class 33


def build():
    written = written_table()
    entries = sorted(k for k in written
                     if k // 10 not in EXCLUDED_TWO_DIGIT and k not in EXCLUDED_THREE_DIGIT)
    assert len(entries) == 229, len(entries)
    short_preds: dict[tuple, list] = {}
    for s in SHORT_WORDS3:
        short_preds.setdefault(next_word(s), []).append(s)

    def preds(w: tuple) -> list:
        return list(long_pred4(w)) + short_preds.get(w, [])

    roots = []
    for k in entries:
        a, b, c = k // 100, (k // 10) % 10, k % 10
        assert not growth_prefix(a, b, c)
        roots.extend(root_words(a, b, c))
    roots.extend(EXTRA_ROOTS)
    seen, stack = set(), list(roots)
    while stack:
        w = stack.pop()
        if w in seen:
            continue
        seen.add(w)
        stack.extend(preds(w))
    sys.setrecursionlimit(100000)
    rank: dict[tuple, int] = {}

    def rk(w):
        if w in rank:
            return rank[w]
        ps = preds(w)
        r = 0 if not ps else 1 + max(rk(s) for s in ps)
        rank[w] = r
        return r

    for w in seen:
        rk(w)
    # Sanity: every row and every short descent holds.
    for w in seen:
        for s in preds(w):
            assert s in rank and rank[s] < rank[w]
    bounds = {}
    for k in entries:
        a, b, c = k // 100, (k // 10) % 10, k % 10
        bounds[k] = 1 + max(rank[r] for r in root_words(a, b, c))
        assert bounds[k] == written[k], (k, bounds[k], written[k])
    assert 1 + rank[(3, 3)] <= 5
    codes = [word_code(w) for w in seen]
    assert len(set(codes)) == len(codes)
    return entries, written, rank, bounds


# ------------------------------------------------------------- Lean emission
LEAF = 48


def lean_word(w) -> str:
    return "[" + ",".join(map(str, w)) + "]"


def subtree_term(items) -> str:
    if not items:
        return ".empty"
    m = len(items) // 2
    code, w, r = items[m]
    return f"(.node {code} {lean_word(w)} {r} {subtree_term(items[:m])} {subtree_term(items[m + 1:])})"


def emit(entries, written, rank, bounds):
    OUT.mkdir(exist_ok=True)
    items = sorted((word_code(w), w, r) for w, r in rank.items())
    leaves, branches = [], []  # leaves: (name, items); branches: (name, item, left, right)

    def build_tree(lo, hi):
        if hi - lo <= LEAF:
            name = f"leaf{len(leaves):04d}"
            leaves.append((name, items[lo:hi]))
            return ("leaf", name)
        mid = (lo + hi) // 2
        left = build_tree(lo, mid)
        right = build_tree(mid + 1, hi)
        name = f"branch{len(branches):04d}"
        branches.append((name, items[mid], left, right))
        return ("branch", name)

    root = build_tree(0, len(items))
    header = ("namespace FourColumnKernel.Certificate\n"
              "open SevenColumn.Certificate\n"
              "set_option maxRecDepth 10000\n")
    data = ["import PrefixCertificate\n", "/-! Generated by generate_certificate.py; checked by the kernel elsewhere. -/\n",
            header]
    for name, its in leaves:
        data.append(f"def {name} : RankTree := {subtree_term(its)}\n")
    for name, (code, w, r), left, right in branches:
        data.append(f"def {name} : RankTree := .node {code} {lean_word(w)} {r} {left[1]} {right[1]}\n")
    data.append(f"def ranks4 : RankTree := {root[1]}\n")
    data.append("def rank4 (w : List Nat) : Option Nat := lookup ranks4 w\n")
    data.append("end FourColumnKernel.Certificate\n")
    (OUT / "Rank4Data.lean").write_text("".join(data))

    # Row-check modules: groups of leaves, then all branch rows in one module.
    group = 16
    row_modules = []
    for gi in range(0, len(leaves), group):
        mod = f"Rows4_{gi // group:03d}"
        row_modules.append(mod)
        body = ["import Rank4Data\nimport FastRowsBase\n", header,
                "set_option maxHeartbeats 100000000\n"]
        for name, _ in leaves[gi:gi + group]:
            body.append(f"theorem checked_{name} : {name}.All "
                        f"(fun p r => checkRow ranks4 (fastLongPred 4) p r = true) := by decide +kernel\n")
        body.append("end FourColumnKernel.Certificate\n")
        (OUT / f"{mod}.lean").write_text("".join(body))
    mod = "Rows4_branches"
    row_modules.append(mod)
    body = ["import Rank4Data\nimport FastRowsBase\n", header, "set_option maxHeartbeats 100000000\n"]
    for name, (code, w, r), _, _ in branches:
        body.append(f"theorem row_{name} : checkRow ranks4 (fastLongPred 4) {lean_word(w)} {r} = true "
                    f":= by decide +kernel\n")
    body.append("end FourColumnKernel.Certificate\n")
    (OUT / f"{mod}.lean").write_text("".join(body))

    def proof(node):
        kind, name = node
        if kind == "leaf":
            return f"checked_{name}"
        b = next(x for x in branches if x[0] == name)
        return f"⟨{proof(b[2])}, row_{name}, {proof(b[3])}⟩"

    agg = ["".join(f"import {m}\n" for m in row_modules), header,
           "set_option maxRecDepth 100000\n",
           f"theorem allRowsFast : CheckedRows ranks4 (fastLongPred 4) := {proof(root)}\n",
           "theorem allRows : CheckedRows ranks4 (longPred 4) := checkedRows_fast_to_long allRowsFast\n",
           "#print axioms allRowsFast\n#print axioms allRows\n",
           "end FourColumnKernel.Certificate\n"]
    (OUT / "AllRows4.lean").write_text("".join(agg))

    # Short-descent check (all 207 exact short words).
    short = ["import Rank4Data\nimport FourColumnAncestry\n", header,
             "set_option maxHeartbeats 100000000\n",
             "open FourColumnKernel\n",
             "theorem shortDescent4 : ShortDescent ranks4 :=\n"
             "  shortDescent_of_all ranks4 (by decide +kernel)\n",
             "#print axioms shortDescent4\n",
             "end FourColumnKernel.Certificate\n"]
    (OUT / "Short4.lean").write_text("".join(short))

    # The claimed table, grouped by leading two digits (statement data).
    lines = []
    by_ab: dict[int, list] = {}
    for k in entries:
        by_ab.setdefault(k // 10, []).append(k)
    for ab in sorted(by_ab):
        row = ", ".join(f"({k // 100}, {(k // 10) % 10}, {k % 10}, {bounds[k]})" for k in by_ab[ab])
        lines.append("    " + row)
    table = ["import ThreeDigitBridge\nimport Rank4Data\n",
             "/-! The 229 claimed prefix classes `(a, b, c, B)`: every palindrome whose\n"
             "canonical numeral begins `a b c` has ancestry depth at most `B`.\n"
             "Transcribed from p196_four_column_obstruction.md section 6 (classes owned by\n"
             "other tasks removed) and recomputed by generate_certificate.py. -/\n",
             "namespace FourColumnKernel.Certificate\nopen SevenColumn.Certificate\nopen FourColumnKernel\n",
             "def table4 : List (Nat × Nat × Nat × Nat) := [\n" + ",\n".join(lines) + "]\n",
             "end FourColumnKernel.Certificate\n"]
    (OUT / "Table4.lean").write_text("".join(table))

    summary = {
        "generator": "generate_certificate.py",
        "nodes": len(items),
        "short_nodes": sum(1 for _, w, _ in items if len(w) < 4),
        "leaves": len(leaves),
        "branches": len(branches),
        "max_rank": max(r for _, _, r in items),
        "rank_histogram": {str(k): sum(1 for _, _, r in items if r == k)
                           for k in range(max(r for _, _, r in items) + 1)},
        "row_predecessor_evaluations": sum(len(long_pred4(w)) for _, w, _ in items),
        "entries": len(entries),
        "table": {str(k): bounds[k] for k in entries},
        "written_bounds_match": all(bounds[k] == written[k] for k in entries),
        "extra_roots": {lean_word(w): rank[w] for w in EXTRA_ROOTS},
        "row_modules": row_modules,
    }
    files = sorted(p.name for p in OUT.glob("*.lean"))
    summary["sha256"] = {f: hashlib.sha256((OUT / f).read_bytes()).hexdigest() for f in files}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    return summary


if __name__ == "__main__":
    entries, written, rank, bounds = build()
    print("entries", len(entries), "nodes", len(rank), "max rank", max(rank.values()))
    if "--check-only" not in sys.argv:
        s = emit(entries, written, rank, bounds)
        print(json.dumps({k: s[k] for k in ("nodes", "short_nodes", "leaves", "branches",
                                            "max_rank", "row_predecessor_evaluations")}))
