#!/usr/bin/env python3
"""Self-checks of absref.py.

1. For k = 1..4 exhaustively: the literal Lean inverse prefixPredecessors(p) equals the
   set {s : s_0 > 0, exists e in {0,1}, forwardPrefix(s, e) = p}  (inverse == forward relation).
2. Decode the 14 Agent117RemainingCycles witnesses from the Lean files and re-check every
   edge with the forward map; report entry length, cycle length and z.
"""
import itertools
import re
import sys
from pathlib import Path

from absref import forward_prefix, prefix_predecessors, unpack

REPO = Path(__file__).resolve().parents[2]


def check_inverse(kmax=4):
    for k in range(1, kmax + 1):
        fwd = {}
        for s in itertools.product(range(19), repeat=k):
            if s[0] == 0:
                continue
            for e in (0, 1):
                p = tuple(forward_prefix(list(s), e))
                fwd.setdefault(p, set()).add(s)
        n_targets = 0
        for p in itertools.product(range(19), repeat=k):
            inv = set(tuple(s) for s in prefix_predecessors(list(p)))
            if inv != fwd.get(p, set()):
                print(f"MISMATCH k={k} p={p} inv={sorted(inv)} fwd={sorted(fwd.get(p, set()))}")
                return False
            n_targets += bool(inv)
        print(f"k={k}: inverse == forward relation on all {19**k} targets "
              f"({n_targets} targets have predecessors)")
    return True


def parse_list(src, name):
    m = re.search(rf"def {name} : List Nat := \[([^\]]*)\]", src)
    return [int(x) for x in m.group(1).split(",")] if m.group(1).strip() else []


def parse_word(src, name):
    m = re.search(rf"def {name} : List Nat := \[([^\]]*)\]", src)
    return [int(x) for x in m.group(1).split(",")]


def check_witnesses():
    d = REPO / "lean/P196/Agent117RemainingCycles"
    rows = []
    for f in sorted(d.glob("Cycle*_k*.lean")):
        src = f.read_text()
        k = int(re.search(r"_k(\d+)", f.name).group(1))
        prefix = re.search(r"Cycle(\d+)_", f.name).group(1)
        p0 = parse_word(src, "p0")
        z = parse_word(src, "z")
        entry = [unpack(k, n) for n in parse_list(src, "entryData")]
        cyc = [unpack(k, n) for n in parse_list(src, "cycleData")]
        ez = int(re.search(r"walkOK \(\(z, (\d)\) :: cycle\)", src).group(1))
        ep = int(re.search(r"walkOK \(\(p0, (\d)\) :: entry\)", src).group(1))
        # walk check: forwardPrefix(next, e_next) == current
        def walk_ok(start, start_e, w):
            cur = start
            for (s, e) in w:
                if not (e < 2 and all(a < 19 for a in s) and s[0] > 0 and forward_prefix(s, e) == cur):
                    return False
                cur = s
            return True
        ok = walk_ok(p0, ep, entry) and (entry[-1][0] if entry else p0) == z
        ok = ok and walk_ok(z, ez, cyc) and cyc[-1][0] == z and len(cyc) > 0
        rows.append((prefix, k, p0, z, len(entry), len(cyc), ok))
        print(f"prefix {prefix} k={k} p0={p0} z={z} entry={len(entry)} cycle={len(cyc)} edges_ok={ok}")
    return all(r[-1] for r in rows), rows


if __name__ == "__main__":
    ok1 = check_inverse(int(sys.argv[1]) if len(sys.argv) > 1 else 4)
    ok2, _ = check_witnesses()
    print("ALL OK" if ok1 and ok2 else "FAILED")
