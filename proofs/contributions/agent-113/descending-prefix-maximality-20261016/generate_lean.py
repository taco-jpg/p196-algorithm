#!/usr/bin/env python3
"""Deterministically generate uncompiled Lean candidate from finite witness records."""
from pathlib import Path
from check import decode, verify_witness_line
base=Path(__file__).resolve().parent
rows=[]
for row in (base/'witnesses.txt').read_text().splitlines():
    if row.strip():
        verify_witness_line(row)
        ab,c,payload=row.split(':')
        rows.append((ab,int(c),decode(payload)))
intro = '''import TwoDigitProjection

/-!
Agent #113 (2026-10-16): exact finite triple-graph certificates.

WIP UNTIL OFFICIAL LEAN COMPILE + AXIOM AUDIT. This file is generated from
witnesses.txt by generate_lean.py and imports the *original* 2026-10-15
TwoDigitProjection module (theorem and function signatures are unchanged).
All theorems concern only the outer-three-pair-sum finite overapproximation.
No integer orbit, infinite ancestry, or P196 claim is asserted.
-/

namespace Agent113.TripleMaximality
open Agent113.TwoDigit

abbrev Triple := Nat × Nat × Nat
structure InvStep where
  s0 : Nat
  s1 : Nat
  s2 : Nat
  e : Nat
  deriving Repr, DecidableEq

private def asTriple (s : InvStep) : Triple := (s.s0, s.s1, s.s2)
private def cycleStates : List Triple :=
  [(1,5,10), (10,4,6), (5,2,3), (2,11,1)]

/-- Valid symbolic inverse edges, beginning at target and ending at the
fixed four-cycle. This is strictly weaker than integer realizability. -/
def ValidChain : Triple → List InvStep → Prop
  | target, [] => target ∈ cycleStates
  | target, s :: rest =>
    1 ≤ s.s0 ∧ s.s0 ≤ 18 ∧ s.s1 ≤ 18 ∧ s.s2 ≤ 18 ∧ s.e ≤ 1 ∧
    nextTriple s.s0 s.s1 s.s2 s.e = target ∧ ValidChain (asTriple s) rest

/-- The first reverse step into a descending palindrome must be no-overflow,
which is an additional restriction not imposed on subsequent inverse edges. -/
def ValidFirst (a b c : Nat) (steps : List InvStep) : Prop :=
  match steps with
  | [] => False
  | s :: _ => topCarry s.s0 s.s1 s.s2 s.e = 0 ∧
    ValidChain (a,b,c) steps

-- Four explicit inverse edges, read right-to-left as forward `nextTriple`.
theorem cycle01 : nextTriple 10 4 6 0 = (1,5,10) := by decide +kernel
theorem cycle12 : nextTriple 5 2 3 0 = (10,4,6) := by decide +kernel
theorem cycle23 : nextTriple 2 11 1 0 = (5,2,3) := by decide +kernel
theorem cycle30 : nextTriple 1 5 10 1 = (2,11,1) := by decide +kernel

'''
lines=[intro]
for ab,c,steps in rows:
    lines.append(f'/-- Concrete finite inverse path for the descending prefix {ab}; WIP compile. -/\n')
    lines.append(f'def path{ab} : List InvStep := [\n')
    for idx,(w,e) in enumerate(steps):
        x,y,z=w
        lines.append(f'  ⟨{x}, {y}, {z}, {e}⟩'+(',' if idx<len(steps)-1 else '')+'\n')
    lines.append(']\n')
    lines.append(f'theorem path{ab}_valid : ValidFirst {ab[0]} {ab[1]} {c} path{ab} := by decide +kernel\n')
    lines.append(f'#print axioms path{ab}_valid\n\n')
lines.append('/-- The 13 previously Lean-certified descending prefixes. -/\n')
lines.append('def original13 : List (Nat × Nat) := [\n')
orig = ["10", "20", "32", "40", "41", "60", "64", "65", "76", "80", "81", "82", "83"]
lines.append('  ' + ', '.join(f'({x[0]},{x[1]})' for x in orig) + '\n]\n')
lines.append('/-- All 32 other descending two-digit prefixes. -/\n')
lines.append('def remaining32 : List (Nat × Nat) := [\n')
lines.append('  ' + ', '.join(f'({ab[0]},{ab[1]})' for ab, _, _ in rows) + '\n]\n')
lines.append("""/-- Exact finite check that the two lists cover every descending pair
with 1 <= a <= 9 and 0 <= b < a. This is NOT unbounded quantification. -/
theorem cover_descending_45 :
    (List.range 10).all (fun a =>
      (List.range 10).all (fun b =>
        decide (1 ≤ a ∧ b < a →
          (a,b) ∈ original13 ∨ (a,b) ∈ remaining32))) = true := by decide +kernel

/-- All 32 other prefixes have a finite symbolic inverse path into the
same four-state cycle. Nothing states real-integer infinite realizability. -/
theorem remaining32_path_exists :
    ∀ ab ∈ remaining32,
      ∃ c, c ≤ 9 ∧ ∃ path, ValidFirst ab.1 ab.2 c path := by
  intro ab hab
  simp only [remaining32, List.mem_cons, List.mem_nil_iff, or_false] at hab
""")
lines.append('  rcases hab with ' + ' | '.join('rfl' for _ in rows) + '\n')
for ab, c, _ in rows:
    lines.append(f'  · exact ⟨{c}, by decide, path{ab}, path{ab}_valid⟩\n')
lines.append('\n#print axioms cover_descending_45\n#print axioms remaining32_path_exists\n')
lines.append('end Agent113.TripleMaximality\n')
out=base/'Agent113TripleCycles.lean'
out.write_text(''.join(lines))
print(len(rows), out.stat().st_size, out)
