import CoordinateCycle

/-!
Agent #115: WIP theorem specifications only, not completed proofs.
This file is deliberately outside the accepted build. No Lean 4.19.0
compiler/rebuild was available in this session. DO NOT label LEAN-CHECKED.
-/
namespace Agent115.RhoCycle

open P196.Agent7.Finite Agent115.ExteriorFactorization Agent6.ExteriorCoordinates

def permitted (c : Nat) : Prop := c ∈ [2, 4, 6, 8, 10, 12, 14, 16]

def gamma (s : Outer) : Nat :=
  (highValue s.B + (if 10 ≤ s.c then 1 else 0)) / 10 ^ s.B.length

/-- The high rational observation, including its constant phase tail. -/
def rho (s : Outer) : Rat :=
  (↑(9 * highValue s.B + s.c) : Rat) /
    (↑(9 * 10 ^ s.B.length) : Rat)

/-- Strictly positive on the permitted positive even phases. -/
def psi (s : Outer) : Rat :=
  let k := if 10 ≤ s.c then 1 else 0
  let t := s.c - 9 * k
  let u := s.c + lowValue s.B / 10 ^ s.B.length - 10 * k
  let r := revN s.B.length (lowValue s.B)
  (↑(90 * r + 9 * u + t) : Rat) /
    (↑(90 * 10 ^ s.B.length) : Rat)

def stepLawTarget : Prop :=
  ∀ s : Outer, permitted s.c →
    (∀ x ∈ s.B, x ≤ 18) →
      rho (outerNext s) = psi s +
        (if gamma s = 0 then rho s else rho s / 10)

def positiveFlowTarget : Prop :=
  ∀ s : Outer, permitted s.c →
    (∀ x ∈ s.B, x ≤ 18) → 0 < psi s

def cycleOverflowTarget : Prop :=
  ∀ (s : Outer) (p : Nat), permitted s.c →
    (∀ i, i < p → permitted (outerIter i s).c ∧
      (∀ x ∈ (outerIter i s).B, x ≤ 18)) →
    0 < p → outerIter p s = s →
      ∃ i, i < p ∧ gamma (outerIter i s) = 1

end Agent115.RhoCycle
