#!/usr/bin/env python3
"""Anatomy of the 14 Agent117RemainingCycles witness cycles.

For each witness: is the closed walk simple, how many distinct words, how many overflow steps
(width growth) per loop, carry usage, the sequence of outer column sums q_0 along the loop, and
which witnesses share the same cycle (same node set, possibly rotated).
Prints a TSV and a short textual summary.
"""
import re
from collections import Counter
from pathlib import Path

from absref import forward_prefix, high_digits, unpack

REPO = Path(__file__).resolve().parents[2]


def overflow(s, e):
    return high_digits(s, e)[0]


def load():
    out = []
    for f in sorted((REPO / "lean/P196/Agent117RemainingCycles").glob("Cycle*_k*.lean")):
        src = f.read_text()
        k = int(re.search(r"_k(\d+)", f.name).group(1))
        prefix = int(re.search(r"Cycle(\d+)_", f.name).group(1))
        z = [int(x) for x in re.search(r"def z : List Nat := \[([^\]]*)\]", src).group(1).split(",")]
        data = [int(x) for x in re.search(r"def cycleData : List Nat := \[([^\]]*)\]", src).group(1).split(",")]
        cyc = [unpack(k, n) for n in data]
        ez = int(re.search(r"walkOK \(\(z, (\d)\) :: cycle\)", src).group(1))
        # backward walk z <- s1 <- s2 ... <- s_n = z ; forward order is the reverse.
        # forward edge s_{i+1} --e_{i+1}--> s_i
        nodes = [z] + [s for s, _ in cyc]          # z, s1, ..., s_n(=z)
        es = [ez] + [e for _, e in cyc]            # carry stored with each word = carry of its forward edge
        fwd_nodes = list(reversed(nodes))          # s_n(=z), ..., s1, z
        fwd_es = list(reversed(es))
        loop = []                                  # (word, e used to go to next)
        for i in range(len(fwd_nodes) - 1):
            w, e = fwd_nodes[i], fwd_es[i]
            assert forward_prefix(w, e) == fwd_nodes[i + 1]
            loop.append((tuple(w), e))
        out.append((prefix, k, loop))
    return out


def main():
    rows = load()
    print("prefix\tk\tlength\tdistinct_words\tsimple\toverflows\te1_steps\tq0_cycle_counts")
    sigs = {}
    for prefix, k, loop in rows:
        words = [w for w, _ in loop]
        ovs = sum(overflow(list(w), e) for w, e in loop)
        e1 = sum(e for _, e in loop)
        distinct = len(set(words))
        q0 = Counter(w[0] for w in words)
        print(f"{prefix}\t{k}\t{len(loop)}\t{distinct}\t{distinct == len(loop)}\t{ovs}\t{e1}\t"
              + ",".join(f"{a}:{q0[a]}" for a in sorted(q0)))
        sigs.setdefault((k, frozenset(words)), []).append(prefix)
    print()
    print("Witnesses sharing the same node set (same cycle up to rotation):")
    for (k, ws), ps in sigs.items():
        print(f"  k={k} |nodes|={len(ws)} prefixes={ps}")


if __name__ == "__main__":
    main()
