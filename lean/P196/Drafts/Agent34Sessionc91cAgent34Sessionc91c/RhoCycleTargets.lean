import P196.Agent6CoordinateDynamics.CoordinateCycle

/-!
Agent #115: arithmetic theorem targets only; not themselves proofs.
The existing pinned source closure uses Core/Std, which does not supply
ordered field division on Rat. The exact high-rho recurrence is therefore
specified by cross-multiplication of strictly positive Nat denominators.
Do not silently treat a target Prop as a completed theorem.
-/
namespace Agent115.RhoCycle

open P196.Agent7.Finite Agent115.ExteriorFactorization Agent6.ExteriorCoordinates

def permitted (c : Nat) : Prop := c ∈ [2, 4, 6, 8, 10, 12, 14, 16]

def gamma (s : Outer) : Nat :=
  (highValue s.B + (if 10 ≤ s.c then 1 else 0)) / 10 ^ s.B.length

/-- The rational observation is rhoNumerator / rhoDenominator. -/
def rhoNumerator (s : Outer) : Nat := 9 * highValue s.B + s.c

def rhoDenominator (s : Outer) : Nat := 9 * 10 ^ s.B.length

/-- The positive rational gain is psiNumerator / psiDenominator. -/
def psiNumerator (s : Outer) : Nat :=
  let k := if 10 ≤ s.c then 1 else 0
  let t := s.c - 9 * k
  let u := s.c + lowValue s.B / 10 ^ s.B.length - 10 * k
  let r := revN s.B.length (lowValue s.B)
  90 * r + 9 * u + t

def psiDenominator (s : Outer) : Nat := 90 * 10 ^ s.B.length

/-- Equivalent to the exact rational recurrence after multiplying both sides
by 90*10^|B| and by the successor's 9*10^|B'| denominator. -/
def stepNumeratorTarget : Prop :=
  ∀ s : Outer, permitted s.c →
    (∀ x ∈ s.B, x ≤ 18) →
      10 * 10 ^ s.B.length * rhoNumerator (outerNext s) =
        10 ^ (outerNext s).B.length *
          ((if gamma s = 0 then 10 * rhoNumerator s else rhoNumerator s) +
            psiNumerator s)

def positiveFlowTarget : Prop :=
  ∀ s : Outer, permitted s.c →
    (∀ x ∈ s.B, x ≤ 18) → 0 < psiNumerator s

def cycleOverflowTarget : Prop :=
  ∀ (s : Outer) (p : Nat), permitted s.c →
    (∀ i, i < p → permitted (outerIter i s).c ∧
      (∀ x ∈ (outerIter i s).B, x ≤ 18)) →
    0 < p → outerIter p s = s →
      ∃ i, i < p ∧ gamma (outerIter i s) = 1

end Agent115.RhoCycle
