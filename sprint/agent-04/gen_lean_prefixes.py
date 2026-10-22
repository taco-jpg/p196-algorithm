#!/usr/bin/env python3
"""Write lean/P196/Sprint/Agent04/PrefixesK7.lean from entry7.tsv (output of `entry`).

usage: gen_lean_prefixes.py ENTRY_TSV TOP20_FILE OUT.lean
Every walk is re-checked here with the reference forward map before it is written.
"""
import csv
import sys

from absref import forward_prefix, unpack, unpack_word

Z7 = [10, 2, 3, 2, 7, 5, 0]


def main():
    rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
    top20 = [int(x) for x in open(sys.argv[2]).read().split()]
    out = []
    names = []
    for r in rows:
        if r["p0_code"] == "NONE":
            raise SystemExit(f"{r['label']}: no initial word in I_7")
        P = int(r["label"][1:])
        pre = [int(c) for c in str(P)]
        p0 = unpack_word(7, int(r["p0_code"]))
        assert p0[: len(pre)] == pre and all(x <= 9 for x in p0)
        packed = [int(x) for x in r["packed_entry"].split(",")] if r["packed_entry"] else []
        cur = p0
        for n in packed:
            s, e = unpack(7, n)
            assert forward_prefix(s, e) == cur
            cur = s
        assert cur == Z7
        tag = "top20" if P in top20 else ("named" if P == 4456 else "three")
        names.append((P, pre, tag, len(packed), int(r["n_initial_in_I"])))
        out.append(f"""
/-- Prefix {P}: initial word `{p0}`; {r['n_initial_in_I']} of the {10 ** (7 - len(pre))} long
initial words of width 7 lie in the infinite-rank part (computed, not proved here). -/
def tail_{P} : List Nat := {p0[len(pre):]}
def p0_{P} : List Nat := {pre} ++ tail_{P}
def entry_{P}Data : List Nat := [{", ".join(map(str, packed))}]
def entry_{P} : List (List Nat × Nat) := entry_{P}Data.map (unpack 7)
theorem entry_{P}_ok : walkOKk 7 ((p0_{P}, 0) :: entry_{P}) = true := by decide +kernel
theorem entry_{P}_end : (entry_{P}.getLastD (p0_{P}, 0)).1 = z7 := by decide +kernel
theorem p0_{P}_initial : p0_{P} ∈ initialWordsL 7 {pre} :=
  mem_initialWordsL_of_full 7 {pre} tail_{P} (by decide) (by decide)
theorem no_certificate_{P} {{R : List Nat → Option Nat}} (rows : RowsClosed 7 R) (bound : Nat) :
    entryOK 7 R ({pre}, bound) = false :=
  entryOK_false_of_none {pre} bound p0_{P}_initial
    (R_none_of_entry7 rows entry_{P} p0_{P} 0 entry_{P}_ok entry_{P}_end)
""")
    three = [p for p, _, t, _, _ in names if t == "three"]
    four = [p for p, _, t, _, _ in names if t != "three"]
    header = f"""import P196.Sprint.Agent04.Trap

/-!
# Sprint agent 04: width-7 method limits through ONE shared cycle

For each prefix below, an explicit initial word `p0_P ∈ initialWordsL 7 P` reaches the length-7
cycle `Sprint04.cycle7` backward (verified walk `entry_P`).  Hence, for every rank function with
`RowsClosed 7 R` (the interface consumed by `Agent124.PrefixL.entryOK` / `no_196_of_entries`),
`entryOK 7 R (P, bound) = false` for every `bound`: no width-7 certificate of the batch kind exists.

Prefixes: the {len(three)} three-digit prefixes of `Agent117RemainingCycles` other than the lead-one
prefix 112 ({", ".join(map(str, three))}; Agent #117 already proves 275 at width 8, which is
stronger), the 20 four-digit prefixes with the longest delays observed in the sprint's forward scan
(seeds < 10^6, 300 steps) among those with cycles at every width 4..7, and 4456.

Method-limit statements only; nothing here excludes or asserts a palindrome in the orbit of 196.
-/

namespace Sprint04.PrefixesK7

open SevenColumn.Certificate Agent117 Agent124.PrefixR Agent124.PrefixL Sprint04
"""
    allp = [p for p, *_ in names]
    footer = f"""
/-- All {len(allp)} prefixes at once. -/
def prefixes : List (List Nat) := [{", ".join(str([int(c) for c in str(p)]) for p in allp)}]

theorem no_certificate_all {{R : List Nat → Option Nat}} (rows : RowsClosed 7 R) (bound : Nat) :
    ∀ pre ∈ prefixes, entryOK 7 R (pre, bound) = false := by
  intro pre hpre
  simp only [prefixes, List.mem_cons, List.mem_nil_iff, or_false] at hpre
  rcases hpre with {" | ".join("rfl" for _ in allp)}
""" + "".join(f"  · exact no_certificate_{p} rows bound\n" for p in allp) + """
end Sprint04.PrefixesK7

""" + "".join(f"#print axioms Sprint04.PrefixesK7.no_certificate_{p}\n" for p in allp) + "#print axioms Sprint04.PrefixesK7.no_certificate_all\n"
    open(sys.argv[3], "w").write(header + "".join(out) + footer)
    for p, pre, tag, d, n in names:
        print(p, tag, "entry length", d, "initial words in I_7:", n)


if __name__ == "__main__":
    main()
