import P196.Agent113TripleMaximality.TwoDigitProjection

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

/-- Constructive decidability of the recursive symbolic edge property. -/
private def chainDecidable (target : Triple) :
    (steps : List InvStep) → Decidable (ValidChain target steps)
  | [] => by
      simp only [ValidChain]
      infer_instance
  | s :: rest => by
      letI : Decidable (ValidChain (asTriple s) rest) :=
        chainDecidable (asTriple s) rest
      simp only [ValidChain]
      infer_instance

instance (target : Triple) (steps : List InvStep) :
    Decidable (ValidChain target steps) := chainDecidable target steps

instance (a b c : Nat) (steps : List InvStep) :
    Decidable (ValidFirst a b c steps) := by
  cases steps with
  | nil =>
      simp only [ValidFirst]
      infer_instance
  | cons s rest =>
      simp only [ValidFirst]
      infer_instance

-- Four explicit inverse edges, read right-to-left as forward `nextTriple`.
theorem cycle01 : nextTriple 10 4 6 0 = (1,5,10) := by decide +kernel
theorem cycle12 : nextTriple 5 2 3 0 = (10,4,6) := by decide +kernel
theorem cycle23 : nextTriple 2 11 1 0 = (5,2,3) := by decide +kernel
theorem cycle30 : nextTriple 1 5 10 1 = (2,11,1) := by decide +kernel

/-- Concrete finite inverse path for the descending prefix 21; WIP compile. -/
def path21 : List InvStep := [
  ⟨1, 0, 9, 1⟩,
  ⟨10, 9, 9, 0⟩,
  ⟨5, 4, 9, 1⟩,
  ⟨2, 12, 9, 0⟩,
  ⟨1, 6, 4, 1⟩,
  ⟨10, 14, 9, 0⟩,
  ⟨5, 7, 4, 1⟩,
  ⟨2, 13, 11, 1⟩,
  ⟨1, 6, 15, 1⟩,
  ⟨10, 5, 9, 1⟩,
  ⟨5, 2, 9, 1⟩,
  ⟨2, 11, 4, 0⟩,
  ⟨1, 5, 12, 0⟩,
  ⟨10, 4, 8, 0⟩,
  ⟨5, 2, 4, 0⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path21_valid : ValidFirst 2 1 9 path21 := by decide +kernel
#print axioms path21_valid

/-- Concrete finite inverse path for the descending prefix 30; WIP compile. -/
def path30 : List InvStep := [
  ⟨1, 10, 9, 0⟩,
  ⟨10, 18, 0, 0⟩,
  ⟨5, 9, 0, 0⟩,
  ⟨2, 9, 10, 0⟩,
  ⟨11, 7, 12, 0⟩,
  ⟨5, 13, 15, 1⟩,
  ⟨2, 16, 17, 0⟩,
  ⟨1, 8, 8, 1⟩,
  ⟨10, 7, 10, 0⟩,
  ⟨9, 17, 2, 0⟩,
  ⟨4, 18, 10, 1⟩,
  ⟨2, 9, 5, 0⟩,
  ⟨1, 4, 12, 1⟩,
  ⟨10, 3, 9, 0⟩,
  ⟨5, 1, 9, 1⟩,
  ⟨2, 10, 14, 0⟩,
  ⟨1, 5, 7, 0⟩,
  ⟨10, 4, 3, 0⟩,
  ⟨5, 2, 1, 1⟩,
  ⟨2, 11, 0, 0⟩,
  ⟨1, 5, 10, 0⟩
]
theorem path30_valid : ValidFirst 3 0 9 path30 := by decide +kernel
#print axioms path30_valid

/-- Concrete finite inverse path for the descending prefix 31; WIP compile. -/
def path31 : List InvStep := [
  ⟨1, 10, 10, 0⟩,
  ⟨10, 18, 10, 0⟩,
  ⟨5, 9, 5, 0⟩,
  ⟨2, 14, 12, 0⟩,
  ⟨1, 7, 6, 0⟩,
  ⟨10, 6, 0, 0⟩,
  ⟨5, 3, 0, 0⟩,
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path31_valid : ValidFirst 3 1 1 path31 := by decide +kernel
#print axioms path31_valid

/-- Concrete finite inverse path for the descending prefix 42; WIP compile. -/
def path42 : List InvStep := [
  ⟨2, 1, 0, 0⟩,
  ⟨1, 0, 10, 0⟩,
  ⟨10, 9, 0, 0⟩,
  ⟨9, 9, 10, 0⟩,
  ⟨4, 9, 15, 0⟩,
  ⟨2, 4, 17, 1⟩,
  ⟨1, 2, 8, 1⟩,
  ⟨10, 10, 7, 0⟩,
  ⟨5, 5, 3, 1⟩,
  ⟨2, 12, 11, 0⟩,
  ⟨1, 6, 5, 1⟩,
  ⟨10, 5, 0, 0⟩,
  ⟨5, 2, 10, 0⟩,
  ⟨2, 11, 4, 1⟩,
  ⟨1, 5, 12, 0⟩,
  ⟨10, 4, 8, 0⟩,
  ⟨5, 2, 4, 0⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path42_valid : ValidFirst 4 2 0 path42 := by decide +kernel
#print axioms path42_valid

/-- Concrete finite inverse path for the descending prefix 43; WIP compile. -/
def path43 : List InvStep := [
  ⟨2, 1, 9, 1⟩,
  ⟨11, 9, 9, 0⟩,
  ⟨5, 9, 9, 1⟩,
  ⟨2, 14, 14, 0⟩,
  ⟨1, 7, 7, 0⟩,
  ⟨10, 6, 1, 0⟩,
  ⟨5, 3, 0, 1⟩,
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path43_valid : ValidFirst 4 3 9 path43 := by decide +kernel
#print axioms path43_valid

/-- Concrete finite inverse path for the descending prefix 50; WIP compile. -/
def path50 : List InvStep := [
  ⟨2, 10, 9, 0⟩,
  ⟨1, 5, 4, 1⟩,
  ⟨10, 13, 0, 0⟩,
  ⟨5, 6, 10, 0⟩,
  ⟨2, 13, 4, 1⟩,
  ⟨1, 6, 12, 0⟩,
  ⟨10, 5, 7, 0⟩,
  ⟨5, 2, 13, 1⟩,
  ⟨2, 11, 6, 0⟩,
  ⟨1, 5, 13, 0⟩,
  ⟨10, 4, 9, 0⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path50_valid : ValidFirst 5 0 9 path50 := by decide +kernel
#print axioms path50_valid

/-- Concrete finite inverse path for the descending prefix 51; WIP compile. -/
def path51 : List InvStep := [
  ⟨2, 10, 12, 0⟩,
  ⟨1, 5, 6, 0⟩,
  ⟨10, 4, 2, 0⟩,
  ⟨5, 2, 1, 0⟩,
  ⟨2, 11, 0, 0⟩,
  ⟨1, 5, 10, 0⟩
]
theorem path51_valid : ValidFirst 5 1 5 path51 := by decide +kernel
#print axioms path51_valid

/-- Concrete finite inverse path for the descending prefix 52; WIP compile. -/
def path52 : List InvStep := [
  ⟨2, 11, 1, 0⟩
]
theorem path52_valid : ValidFirst 5 2 3 path52 := by decide +kernel
#print axioms path52_valid

/-- Concrete finite inverse path for the descending prefix 53; WIP compile. -/
def path53 : List InvStep := [
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path53_valid : ValidFirst 5 3 0 path53 := by decide +kernel
#print axioms path53_valid

/-- Concrete finite inverse path for the descending prefix 54; WIP compile. -/
def path54 : List InvStep := [
  ⟨2, 12, 9, 0⟩,
  ⟨1, 6, 4, 1⟩,
  ⟨10, 14, 9, 0⟩,
  ⟨5, 7, 4, 1⟩,
  ⟨2, 13, 11, 1⟩,
  ⟨1, 6, 15, 1⟩,
  ⟨10, 5, 9, 1⟩,
  ⟨5, 2, 9, 1⟩,
  ⟨2, 11, 4, 0⟩,
  ⟨1, 5, 12, 0⟩,
  ⟨10, 4, 8, 0⟩,
  ⟨5, 2, 4, 0⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path54_valid : ValidFirst 5 4 9 path54 := by decide +kernel
#print axioms path54_valid

/-- Concrete finite inverse path for the descending prefix 61; WIP compile. -/
def path61 : List InvStep := [
  ⟨3, 0, 9, 1⟩,
  ⟨1, 10, 9, 0⟩,
  ⟨10, 18, 0, 0⟩,
  ⟨5, 9, 0, 0⟩,
  ⟨2, 9, 10, 0⟩,
  ⟨11, 7, 12, 0⟩,
  ⟨5, 13, 15, 1⟩,
  ⟨2, 16, 17, 0⟩,
  ⟨1, 8, 8, 1⟩,
  ⟨10, 7, 10, 0⟩,
  ⟨9, 17, 2, 0⟩,
  ⟨4, 18, 10, 1⟩,
  ⟨2, 9, 5, 0⟩,
  ⟨1, 4, 12, 1⟩,
  ⟨10, 3, 9, 0⟩,
  ⟨5, 1, 9, 1⟩,
  ⟨2, 10, 14, 0⟩,
  ⟨1, 5, 7, 0⟩,
  ⟨10, 4, 3, 0⟩,
  ⟨5, 2, 1, 1⟩,
  ⟨2, 11, 0, 0⟩,
  ⟨1, 5, 10, 0⟩
]
theorem path61_valid : ValidFirst 6 1 9 path61 := by decide +kernel
#print axioms path61_valid

/-- Concrete finite inverse path for the descending prefix 62; WIP compile. -/
def path62 : List InvStep := [
  ⟨3, 1, 1, 0⟩,
  ⟨1, 10, 10, 0⟩,
  ⟨10, 18, 10, 0⟩,
  ⟨5, 9, 5, 0⟩,
  ⟨2, 14, 12, 0⟩,
  ⟨1, 7, 6, 0⟩,
  ⟨10, 6, 0, 0⟩,
  ⟨5, 3, 0, 0⟩,
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path62_valid : ValidFirst 6 2 2 path62 := by decide +kernel
#print axioms path62_valid

/-- Concrete finite inverse path for the descending prefix 63; WIP compile. -/
def path63 : List InvStep := [
  ⟨3, 1, 9, 1⟩,
  ⟨1, 10, 14, 0⟩,
  ⟨10, 18, 14, 0⟩,
  ⟨5, 9, 7, 0⟩,
  ⟨2, 14, 13, 0⟩,
  ⟨1, 7, 6, 1⟩,
  ⟨10, 6, 0, 0⟩,
  ⟨5, 3, 0, 0⟩,
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path63_valid : ValidFirst 6 3 9 path63 := by decide +kernel
#print axioms path63_valid

/-- Concrete finite inverse path for the descending prefix 70; WIP compile. -/
def path70 : List InvStep := [
  ⟨3, 10, 9, 0⟩,
  ⟨12, 7, 2, 0⟩,
  ⟨6, 3, 11, 0⟩,
  ⟨3, 1, 15, 1⟩,
  ⟨1, 10, 17, 0⟩,
  ⟨10, 18, 17, 0⟩,
  ⟨5, 9, 8, 1⟩,
  ⟨2, 14, 13, 1⟩,
  ⟨1, 7, 6, 1⟩,
  ⟨10, 6, 0, 0⟩,
  ⟨5, 3, 0, 0⟩,
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path70_valid : ValidFirst 7 0 9 path70 := by decide +kernel
#print axioms path70_valid

/-- Concrete finite inverse path for the descending prefix 71; WIP compile. -/
def path71 : List InvStep := [
  ⟨3, 10, 9, 1⟩,
  ⟨12, 7, 2, 0⟩,
  ⟨6, 3, 11, 0⟩,
  ⟨3, 1, 15, 1⟩,
  ⟨1, 10, 17, 0⟩,
  ⟨10, 18, 17, 0⟩,
  ⟨5, 9, 8, 1⟩,
  ⟨2, 14, 13, 1⟩,
  ⟨1, 7, 6, 1⟩,
  ⟨10, 6, 0, 0⟩,
  ⟨5, 3, 0, 0⟩,
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path71_valid : ValidFirst 7 1 0 path71 := by decide +kernel
#print axioms path71_valid

/-- Concrete finite inverse path for the descending prefix 72; WIP compile. -/
def path72 : List InvStep := [
  ⟨3, 11, 9, 0⟩,
  ⟨12, 17, 1, 0⟩,
  ⟨6, 8, 10, 1⟩,
  ⟨15, 2, 8, 0⟩,
  ⟨7, 11, 3, 1⟩,
  ⟨16, 13, 9, 0⟩,
  ⟨8, 6, 9, 1⟩,
  ⟨4, 3, 4, 1⟩,
  ⟨2, 1, 12, 0⟩,
  ⟨11, 9, 2, 0⟩,
  ⟨5, 9, 11, 0⟩,
  ⟨2, 14, 15, 0⟩,
  ⟨1, 7, 7, 1⟩,
  ⟨10, 6, 1, 0⟩,
  ⟨5, 3, 0, 1⟩,
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path72_valid : ValidFirst 7 2 9 path72 := by decide +kernel
#print axioms path72_valid

/-- Concrete finite inverse path for the descending prefix 73; WIP compile. -/
def path73 : List InvStep := [
  ⟨3, 11, 9, 1⟩,
  ⟨12, 17, 1, 0⟩,
  ⟨6, 8, 10, 1⟩,
  ⟨15, 2, 8, 0⟩,
  ⟨7, 11, 3, 1⟩,
  ⟨16, 13, 9, 0⟩,
  ⟨8, 6, 9, 1⟩,
  ⟨4, 3, 4, 1⟩,
  ⟨2, 1, 12, 0⟩,
  ⟨11, 9, 2, 0⟩,
  ⟨5, 9, 11, 0⟩,
  ⟨2, 14, 15, 0⟩,
  ⟨1, 7, 7, 1⟩,
  ⟨10, 6, 1, 0⟩,
  ⟨5, 3, 0, 1⟩,
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path73_valid : ValidFirst 7 3 0 path73 := by decide +kernel
#print axioms path73_valid

/-- Concrete finite inverse path for the descending prefix 74; WIP compile. -/
def path74 : List InvStep := [
  ⟨3, 12, 9, 0⟩,
  ⟨12, 18, 9, 1⟩,
  ⟨6, 9, 4, 1⟩,
  ⟨15, 3, 1, 0⟩,
  ⟨7, 11, 10, 0⟩,
  ⟨16, 13, 6, 0⟩,
  ⟨8, 6, 13, 0⟩,
  ⟨4, 3, 6, 1⟩,
  ⟨2, 1, 13, 0⟩,
  ⟨11, 9, 3, 0⟩,
  ⟨5, 9, 11, 1⟩,
  ⟨2, 14, 15, 0⟩,
  ⟨1, 7, 7, 1⟩,
  ⟨10, 6, 1, 0⟩,
  ⟨5, 3, 0, 1⟩,
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path74_valid : ValidFirst 7 4 9 path74 := by decide +kernel
#print axioms path74_valid

/-- Concrete finite inverse path for the descending prefix 75; WIP compile. -/
def path75 : List InvStep := [
  ⟨3, 12, 9, 1⟩,
  ⟨12, 18, 9, 1⟩,
  ⟨6, 9, 4, 1⟩,
  ⟨15, 3, 1, 0⟩,
  ⟨7, 11, 10, 0⟩,
  ⟨16, 13, 6, 0⟩,
  ⟨8, 6, 13, 0⟩,
  ⟨4, 3, 6, 1⟩,
  ⟨2, 1, 13, 0⟩,
  ⟨11, 9, 3, 0⟩,
  ⟨5, 9, 11, 1⟩,
  ⟨2, 14, 15, 0⟩,
  ⟨1, 7, 7, 1⟩,
  ⟨10, 6, 1, 0⟩,
  ⟨5, 3, 0, 1⟩,
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path75_valid : ValidFirst 7 5 0 path75 := by decide +kernel
#print axioms path75_valid

/-- Concrete finite inverse path for the descending prefix 84; WIP compile. -/
def path84 : List InvStep := [
  ⟨4, 2, 0, 0⟩,
  ⟨2, 1, 0, 0⟩,
  ⟨1, 0, 10, 0⟩,
  ⟨10, 9, 0, 0⟩,
  ⟨9, 9, 10, 0⟩,
  ⟨4, 9, 15, 0⟩,
  ⟨2, 4, 17, 1⟩,
  ⟨1, 2, 8, 1⟩,
  ⟨10, 10, 7, 0⟩,
  ⟨5, 5, 3, 1⟩,
  ⟨2, 12, 11, 0⟩,
  ⟨1, 6, 5, 1⟩,
  ⟨10, 5, 0, 0⟩,
  ⟨5, 2, 10, 0⟩,
  ⟨2, 11, 4, 1⟩,
  ⟨1, 5, 12, 0⟩,
  ⟨10, 4, 8, 0⟩,
  ⟨5, 2, 4, 0⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path84_valid : ValidFirst 8 4 0 path84 := by decide +kernel
#print axioms path84_valid

/-- Concrete finite inverse path for the descending prefix 85; WIP compile. -/
def path85 : List InvStep := [
  ⟨4, 2, 9, 1⟩,
  ⟨2, 1, 4, 1⟩,
  ⟨1, 0, 12, 0⟩,
  ⟨10, 9, 2, 0⟩,
  ⟨9, 9, 12, 0⟩,
  ⟨4, 9, 16, 0⟩,
  ⟨2, 4, 18, 0⟩,
  ⟨1, 2, 9, 0⟩,
  ⟨10, 10, 8, 0⟩,
  ⟨5, 5, 4, 0⟩,
  ⟨2, 12, 11, 1⟩,
  ⟨1, 6, 5, 1⟩,
  ⟨10, 5, 0, 0⟩,
  ⟨5, 2, 10, 0⟩,
  ⟨2, 11, 4, 1⟩,
  ⟨1, 5, 12, 0⟩,
  ⟨10, 4, 8, 0⟩,
  ⟨5, 2, 4, 0⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path85_valid : ValidFirst 8 5 9 path85 := by decide +kernel
#print axioms path85_valid

/-- Concrete finite inverse path for the descending prefix 86; WIP compile. -/
def path86 : List InvStep := [
  ⟨4, 3, 0, 0⟩,
  ⟨2, 1, 10, 0⟩,
  ⟨11, 9, 0, 0⟩,
  ⟨5, 9, 10, 0⟩,
  ⟨2, 14, 14, 1⟩,
  ⟨1, 7, 7, 0⟩,
  ⟨10, 6, 1, 0⟩,
  ⟨5, 3, 0, 1⟩,
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path86_valid : ValidFirst 8 6 0 path86 := by decide +kernel
#print axioms path86_valid

/-- Concrete finite inverse path for the descending prefix 87; WIP compile. -/
def path87 : List InvStep := [
  ⟨4, 3, 9, 1⟩,
  ⟨2, 1, 9, 1⟩,
  ⟨11, 9, 9, 0⟩,
  ⟨5, 9, 9, 1⟩,
  ⟨2, 14, 14, 0⟩,
  ⟨1, 7, 7, 0⟩,
  ⟨10, 6, 1, 0⟩,
  ⟨5, 3, 0, 1⟩,
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path87_valid : ValidFirst 8 7 9 path87 := by decide +kernel
#print axioms path87_valid

/-- Concrete finite inverse path for the descending prefix 90; WIP compile. -/
def path90 : List InvStep := [
  ⟨4, 10, 0, 0⟩,
  ⟨2, 5, 0, 0⟩,
  ⟨1, 2, 10, 0⟩,
  ⟨10, 10, 18, 0⟩,
  ⟨5, 5, 9, 0⟩,
  ⟨2, 12, 14, 0⟩,
  ⟨1, 6, 7, 0⟩,
  ⟨10, 5, 2, 0⟩,
  ⟨5, 2, 11, 0⟩,
  ⟨2, 11, 5, 0⟩,
  ⟨1, 5, 12, 1⟩,
  ⟨10, 4, 8, 0⟩,
  ⟨5, 2, 4, 0⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path90_valid : ValidFirst 9 0 1 path90 := by decide +kernel
#print axioms path90_valid

/-- Concrete finite inverse path for the descending prefix 91; WIP compile. -/
def path91 : List InvStep := [
  ⟨4, 10, 9, 1⟩,
  ⟨13, 15, 3, 0⟩,
  ⟨6, 17, 11, 0⟩,
  ⟨3, 8, 15, 1⟩,
  ⟨12, 5, 9, 1⟩,
  ⟨6, 2, 9, 1⟩,
  ⟨3, 1, 4, 1⟩,
  ⟨1, 10, 11, 1⟩,
  ⟨10, 18, 11, 0⟩,
  ⟨5, 9, 5, 1⟩,
  ⟨2, 14, 12, 0⟩,
  ⟨1, 7, 6, 0⟩,
  ⟨10, 6, 0, 0⟩,
  ⟨5, 3, 0, 0⟩,
  ⟨2, 11, 9, 1⟩,
  ⟨1, 5, 14, 1⟩,
  ⟨10, 4, 9, 1⟩,
  ⟨5, 2, 4, 1⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path91_valid : ValidFirst 9 1 0 path91 := by decide +kernel
#print axioms path91_valid

/-- Concrete finite inverse path for the descending prefix 92; WIP compile. -/
def path92 : List InvStep := [
  ⟨4, 11, 9, 0⟩,
  ⟨2, 5, 9, 1⟩,
  ⟨1, 2, 9, 1⟩,
  ⟨10, 10, 8, 0⟩,
  ⟨5, 5, 4, 0⟩,
  ⟨2, 12, 11, 1⟩,
  ⟨1, 6, 5, 1⟩,
  ⟨10, 5, 0, 0⟩,
  ⟨5, 2, 10, 0⟩,
  ⟨2, 11, 4, 1⟩,
  ⟨1, 5, 12, 0⟩,
  ⟨10, 4, 8, 0⟩,
  ⟨5, 2, 4, 0⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path92_valid : ValidFirst 9 2 9 path92 := by decide +kernel
#print axioms path92_valid

/-- Concrete finite inverse path for the descending prefix 93; WIP compile. -/
def path93 : List InvStep := [
  ⟨4, 11, 9, 1⟩,
  ⟨2, 5, 9, 1⟩,
  ⟨1, 2, 9, 1⟩,
  ⟨10, 10, 8, 0⟩,
  ⟨5, 5, 4, 0⟩,
  ⟨2, 12, 11, 1⟩,
  ⟨1, 6, 5, 1⟩,
  ⟨10, 5, 0, 0⟩,
  ⟨5, 2, 10, 0⟩,
  ⟨2, 11, 4, 1⟩,
  ⟨1, 5, 12, 0⟩,
  ⟨10, 4, 8, 0⟩,
  ⟨5, 2, 4, 0⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path93_valid : ValidFirst 9 3 0 path93 := by decide +kernel
#print axioms path93_valid

/-- Concrete finite inverse path for the descending prefix 94; WIP compile. -/
def path94 : List InvStep := [
  ⟨4, 12, 4, 0⟩,
  ⟨2, 6, 2, 0⟩,
  ⟨1, 3, 1, 0⟩,
  ⟨10, 11, 9, 0⟩,
  ⟨5, 5, 9, 1⟩,
  ⟨2, 12, 14, 0⟩,
  ⟨1, 6, 7, 0⟩,
  ⟨10, 5, 2, 0⟩,
  ⟨5, 2, 11, 0⟩,
  ⟨2, 11, 5, 0⟩,
  ⟨1, 5, 12, 1⟩,
  ⟨10, 4, 8, 0⟩,
  ⟨5, 2, 4, 0⟩,
  ⟨2, 11, 1, 1⟩
]
theorem path94_valid : ValidFirst 9 4 9 path94 := by decide +kernel
#print axioms path94_valid

/-- Concrete finite inverse path for the descending prefix 95; WIP compile. -/
def path95 : List InvStep := [
  ⟨4, 12, 12, 0⟩,
  ⟨2, 6, 6, 0⟩,
  ⟨1, 3, 3, 0⟩,
  ⟨10, 2, 10, 0⟩,
  ⟨5, 1, 5, 0⟩,
  ⟨2, 10, 12, 0⟩,
  ⟨1, 5, 6, 0⟩,
  ⟨10, 4, 2, 0⟩,
  ⟨5, 2, 1, 0⟩,
  ⟨2, 11, 0, 0⟩,
  ⟨1, 5, 10, 0⟩
]
theorem path95_valid : ValidFirst 9 5 5 path95 := by decide +kernel
#print axioms path95_valid

/-- Concrete finite inverse path for the descending prefix 96; WIP compile. -/
def path96 : List InvStep := [
  ⟨4, 13, 0, 0⟩,
  ⟨2, 6, 10, 0⟩,
  ⟨1, 3, 5, 0⟩,
  ⟨10, 2, 12, 0⟩,
  ⟨5, 1, 6, 0⟩,
  ⟨2, 10, 12, 1⟩,
  ⟨1, 5, 6, 0⟩,
  ⟨10, 4, 2, 0⟩,
  ⟨5, 2, 1, 0⟩,
  ⟨2, 11, 0, 0⟩,
  ⟨1, 5, 10, 0⟩
]
theorem path96_valid : ValidFirst 9 6 1 path96 := by decide +kernel
#print axioms path96_valid

/-- Concrete finite inverse path for the descending prefix 97; WIP compile. -/
def path97 : List InvStep := [
  ⟨4, 13, 9, 1⟩,
  ⟨2, 6, 9, 1⟩,
  ⟨1, 3, 4, 1⟩,
  ⟨10, 2, 11, 0⟩,
  ⟨5, 1, 5, 1⟩,
  ⟨2, 10, 12, 0⟩,
  ⟨1, 5, 6, 0⟩,
  ⟨10, 4, 2, 0⟩,
  ⟨5, 2, 1, 0⟩,
  ⟨2, 11, 0, 0⟩,
  ⟨1, 5, 10, 0⟩
]
theorem path97_valid : ValidFirst 9 7 0 path97 := by decide +kernel
#print axioms path97_valid

/-- Concrete finite inverse path for the descending prefix 98; WIP compile. -/
def path98 : List InvStep := [
  ⟨4, 14, 0, 0⟩,
  ⟨2, 7, 0, 0⟩,
  ⟨1, 3, 10, 0⟩,
  ⟨10, 2, 17, 0⟩,
  ⟨5, 1, 8, 1⟩,
  ⟨2, 10, 13, 1⟩,
  ⟨1, 5, 6, 1⟩,
  ⟨10, 4, 2, 0⟩,
  ⟨5, 2, 1, 0⟩,
  ⟨2, 11, 0, 0⟩,
  ⟨1, 5, 10, 0⟩
]
theorem path98_valid : ValidFirst 9 8 1 path98 := by decide +kernel
#print axioms path98_valid

/-- The 13 previously Lean-certified descending prefixes. -/
def original13 : List (Nat × Nat) := [
  (1,0), (2,0), (3,2), (4,0), (4,1), (6,0), (6,4), (6,5), (7,6), (8,0), (8,1), (8,2), (8,3)
]
/-- All 32 other descending two-digit prefixes. -/
def remaining32 : List (Nat × Nat) := [
  (2,1), (3,0), (3,1), (4,2), (4,3), (5,0), (5,1), (5,2), (5,3), (5,4), (6,1), (6,2), (6,3), (7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (8,4), (8,5), (8,6), (8,7), (9,0), (9,1), (9,2), (9,3), (9,4), (9,5), (9,6), (9,7), (9,8)
]
/-- Exact finite check that the two lists cover every descending pair
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
  rcases hab with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact ⟨9, by decide, path21, path21_valid⟩
  · exact ⟨9, by decide, path30, path30_valid⟩
  · exact ⟨1, by decide, path31, path31_valid⟩
  · exact ⟨0, by decide, path42, path42_valid⟩
  · exact ⟨9, by decide, path43, path43_valid⟩
  · exact ⟨9, by decide, path50, path50_valid⟩
  · exact ⟨5, by decide, path51, path51_valid⟩
  · exact ⟨3, by decide, path52, path52_valid⟩
  · exact ⟨0, by decide, path53, path53_valid⟩
  · exact ⟨9, by decide, path54, path54_valid⟩
  · exact ⟨9, by decide, path61, path61_valid⟩
  · exact ⟨2, by decide, path62, path62_valid⟩
  · exact ⟨9, by decide, path63, path63_valid⟩
  · exact ⟨9, by decide, path70, path70_valid⟩
  · exact ⟨0, by decide, path71, path71_valid⟩
  · exact ⟨9, by decide, path72, path72_valid⟩
  · exact ⟨0, by decide, path73, path73_valid⟩
  · exact ⟨9, by decide, path74, path74_valid⟩
  · exact ⟨0, by decide, path75, path75_valid⟩
  · exact ⟨0, by decide, path84, path84_valid⟩
  · exact ⟨9, by decide, path85, path85_valid⟩
  · exact ⟨0, by decide, path86, path86_valid⟩
  · exact ⟨9, by decide, path87, path87_valid⟩
  · exact ⟨1, by decide, path90, path90_valid⟩
  · exact ⟨0, by decide, path91, path91_valid⟩
  · exact ⟨9, by decide, path92, path92_valid⟩
  · exact ⟨0, by decide, path93, path93_valid⟩
  · exact ⟨9, by decide, path94, path94_valid⟩
  · exact ⟨5, by decide, path95, path95_valid⟩
  · exact ⟨1, by decide, path96, path96_valid⟩
  · exact ⟨0, by decide, path97, path97_valid⟩
  · exact ⟨1, by decide, path98, path98_valid⟩

#print axioms cover_descending_45
#print axioms remaining32_path_exists
end Agent113.TripleMaximality
